import random
import math

# ─────────────────────────────────────────────
# Weights (objective function tuning)
# ─────────────────────────────────────────────
RETURN_WEIGHT = 1.0
RISK_WEIGHT = 1.0
QUALITY_WEIGHT = 0.5
SECTOR_WEIGHT = 2.0

TARGET_MISS_PENALTY = 5.0
HARD_CONSTRAINT_PENALTY = 200.0

RISK_CAP = {
    "Conservative": 10.0,
    "Low": 15.0,
    "Medium": 20.0,
    "High": 30.0,
    "Aggressive": 40.0,
}


# ─────────────────────────────────────────────
# Objective Function
# ─────────────────────────────────────────────
def evaluate_allocation(allocation, stocks_df, profile):

    expected_return = 0
    risk_penalty = 0
    quality_bonus = 0
    sectors = set()

    for ticker, weight in allocation.items():

        row = stocks_df[stocks_df["Ticker"] == ticker].iloc[0]

        expected_return += weight * row["Avg_Annual_Growth"]
        risk_penalty += weight * row["Volatility_Pct"]
        quality_bonus += weight * row["Score"]

        sectors.add(row["Sector"])

    sector_bonus = len(sectors) * SECTOR_WEIGHT

    score = (
        RETURN_WEIGHT * expected_return
        - RISK_WEIGHT * risk_penalty
        + QUALITY_WEIGHT * (quality_bonus / 100)
        + sector_bonus
    )

    if expected_return < profile.get("target_return", 0):
        score -= TARGET_MISS_PENALTY

    if violates_constraints(allocation, stocks_df, profile):
        score -= HARD_CONSTRAINT_PENALTY

    return score


# ─────────────────────────────────────────────
# Constraint Checker
# ─────────────────────────────────────────────
def violates_constraints(allocation, stocks_df, profile):

    total = sum(allocation.values())

    # allow small floating error
    if abs(total - 1.0) > 0.15:
        return True

    sectors = set()
    weighted_vol = 0

    for ticker, weight in allocation.items():

        row = stocks_df[stocks_df["Ticker"] == ticker].iloc[0]

        if row["Sector"] in profile.get("excluded_sectors", []):
            return True

        sectors.add(row["Sector"])
        weighted_vol += weight * row["Volatility_Pct"]

        if weight > 0.50:
            return True

    if profile.get("enforce_diversification", False):
        if len(sectors) < 2:
            return True

    risk_limit = RISK_CAP.get(profile.get("risk_appetite", "Medium"), 20.0)

    if weighted_vol > risk_limit * 1.6:
        return True

    return False


# ─────────────────────────────────────────────
# Random Allocation Generator
# ─────────────────────────────────────────────
def generate_random_valid_allocation(stocks_df, profile):

    eligible = stocks_df[
        ~stocks_df["Sector"].isin(profile.get("excluded_sectors", []))
    ]

    tickers = eligible["Ticker"].tolist()

    if len(tickers) < 3:
        tickers = stocks_df["Ticker"].tolist()

    selected = random.sample(tickers, min(5, len(tickers)))

    weights = [random.random() for _ in selected]
    total = sum(weights)

    return {t: w / total for t, w in zip(selected, weights)}


# ─────────────────────────────────────────────
# Neighbor Generator
# ─────────────────────────────────────────────
def tweak_allocation(allocation):

    new_alloc = allocation.copy()

    if len(new_alloc) < 2:
        return new_alloc

    a, b = random.sample(list(new_alloc.keys()), 2)

    move = random.uniform(0.01, 0.05)
    move = min(move, new_alloc[a])

    new_alloc[a] -= move
    new_alloc[b] += move

    total = sum(new_alloc.values())

    if total == 0:
        return allocation

    return {k: v / total for k, v in new_alloc.items()}


# ─────────────────────────────────────────────
# Hill Climbing
# ─────────────────────────────────────────────
def hill_climbing(stocks_df, profile, iterations=300):

    current = generate_random_valid_allocation(stocks_df, profile)
    current_score = evaluate_allocation(current, stocks_df, profile)

    history = [current_score]

    for _ in range(iterations):

        neighbor = tweak_allocation(current)

        if violates_constraints(neighbor, stocks_df, profile):
            continue

        score = evaluate_allocation(neighbor, stocks_df, profile)

        if score > current_score:
            current = neighbor
            current_score = score

        history.append(current_score)

    return {
        "allocation": current,
        "score": current_score,
        "history": history
    }


# ─────────────────────────────────────────────
# Simulated Annealing (FIXED)
# ─────────────────────────────────────────────
def simulated_annealing(stocks_df, profile, iterations=300, temp=80):

    current = generate_random_valid_allocation(stocks_df, profile)
    current_score = evaluate_allocation(current, stocks_df, profile)

    best = current.copy()
    best_score = current_score

    history = [current_score]

    cooling = 0.98

    for _ in range(iterations):

        neighbor = tweak_allocation(current)

        if violates_constraints(neighbor, stocks_df, profile):
            continue

        score = evaluate_allocation(neighbor, stocks_df, profile)

        delta = score - current_score

        # stable acceptance probability
        prob = math.exp(delta / max(temp, 1.0))

        if delta > 0 or random.random() < prob:
            current = neighbor
            current_score = score

        if current_score > best_score:
            best = current.copy()
            best_score = current_score

        history.append(best_score)

        temp = max(temp * cooling, 1.0)

    return {
        "allocation": best,
        "score": best_score,
        "history": history
    }