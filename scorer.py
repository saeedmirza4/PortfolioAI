"""
PortfolioAI — Stock Scoring System
Student 1: Muhammad Omer (BCS233066) — Data & Knowledge Engineer
Week 2 Deliverable

Heuristic scoring engine. No ML, no sklearn — pure weighted formula.
Place this file in the project root (same level as app.py).
"""

import pandas as pd
import numpy as np


# ── Scoring weights by risk appetite ──────────────────────────────────────────

BASE_WEIGHTS = {
    "growth":      30,
    "diversity":   20,
    "volatility":  20,
    "dividend":    15,
    "momentum":    15,
}

RISK_OVERRIDES = {
    "Conservative": {"growth": 20, "volatility": 30},
    "Low":          {"growth": 25, "volatility": 25},
    "Medium":       {},
    "High":         {"growth": 35, "volatility": 12},
    "Aggressive":   {"growth": 40, "volatility":  8},
}


def _get_weights(risk_appetite: str) -> dict:
    weights = BASE_WEIGHTS.copy()
    overrides = RISK_OVERRIDES.get(risk_appetite, {})
    weights.update(overrides)
    return weights


def _minmax(series: pd.Series, invert: bool = False) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    scaled = (series - lo) / (hi - lo)
    return 1 - scaled if invert else scaled


def _sector_diversity_score(df: pd.DataFrame) -> pd.Series:
    counts = df["Sector"].map(df["Sector"].value_counts())
    return _minmax(counts, invert=True)


def score_stocks(df: pd.DataFrame, profile: dict) -> pd.DataFrame:
    """
    Score every stock in df against the investor profile.

    Parameters
    ----------
    df : pd.DataFrame
        Columns: Ticker, Company, Sector, Price_PKR,
        Avg_Annual_Growth, Volatility_Pct, Volatility_Label,
        Dividend_Yield, Stability_Score, Risk_Score, Momentum_Score

    profile : dict
        Keys: risk_appetite, preferred_sectors, excluded_sectors,
              target_return, dividend_preference, enforce_diversification

    Returns
    -------
    pd.DataFrame
        Original df + Score (float 0-100) + Reasons (list of str)
        Sorted by Score descending.
    """

    df = df.copy()

    risk        = profile.get("risk_appetite", "Medium")
    preferred   = [s.strip() for s in profile.get("preferred_sectors", [])]
    excluded    = [s.strip() for s in profile.get("excluded_sectors", [])]
    target_ret  = profile.get("target_return", 10)
    div_pref    = profile.get("dividend_preference", False)
    enforce_div = profile.get("enforce_diversification", False)

    weights = _get_weights(risk)

    # ── Component scores (normalised 0–1) ─────────────────────────────────────
    growth_norm    = _minmax(df["Avg_Annual_Growth"])
    diversity_norm = _sector_diversity_score(df)
    vol_norm       = _minmax(df["Volatility_Pct"], invert=True)
    div_norm       = _minmax(
        0.6 * _minmax(df["Dividend_Yield"]) + 0.4 * _minmax(df["Stability_Score"])
    )
    momentum_norm  = _minmax(df["Momentum_Score"])

    # ── Weighted raw score ────────────────────────────────────────────────────
    raw = (
        growth_norm    * weights["growth"]     +
        diversity_norm * weights["diversity"]  +
        vol_norm       * weights["volatility"] +
        div_norm       * weights["dividend"]   +
        momentum_norm  * weights["momentum"]
    )
    scores = raw.copy()

    # ── Profile adjustments ───────────────────────────────────────────────────
    if preferred:
        scores[df["Sector"].isin(preferred)] += 8
    if excluded:
        scores[df["Sector"].isin(excluded)] = 0
    if div_pref:
        scores[df["Dividend_Yield"] > 0] += 5
    scores[df["Avg_Annual_Growth"] < (target_ret * 0.6)] -= 5
    if enforce_div:
        counts = df["Sector"].map(df["Sector"].value_counts())
        scores[counts > 3] -= 4

    scores = scores.clip(0, 100).round(2)

    # ── Reason generation ─────────────────────────────────────────────────────
    def _build_reasons(row, g_norm, v_norm, d_norm, m_norm) -> list:
        reasons = []
        growth = row["Avg_Annual_Growth"]

        if g_norm >= 0.7:
            reasons.append(f"Strong long-term growth of {growth:.1f}% CAGR — well above portfolio average.")
        elif g_norm >= 0.4:
            reasons.append(f"Moderate growth of {growth:.1f}% CAGR — meets typical expectations.")
        else:
            reasons.append(f"Below-average growth ({growth:.1f}% CAGR) — limited upside potential.")

        vol_label = row["Volatility_Label"]
        vol_pct   = row["Volatility_Pct"]
        if v_norm >= 0.7:
            reasons.append(f"Low volatility ({vol_label}, {vol_pct:.1f}%) — suitable for capital preservation.")
        elif v_norm >= 0.4:
            reasons.append(f"Moderate volatility ({vol_label}, {vol_pct:.1f}%) — balanced risk profile.")
        else:
            reasons.append(f"High volatility ({vol_label}, {vol_pct:.1f}%) — may not suit conservative investors.")

        div = row["Dividend_Yield"]
        if div_pref and div > 0:
            reasons.append(f"Dividend yield of {div:.1f}% matches your preference for income-generating stocks.")
        elif div > 5:
            reasons.append(f"Above-average dividend yield of {div:.1f}%.")
        elif div == 0:
            reasons.append("No dividend payout — growth-focused stock.")

        sector = row["Sector"]
        if preferred and sector in preferred:
            reasons.append(f"In your preferred sector: {sector}.")
        if excluded and sector in excluded:
            reasons.append(f"WARNING: Sector ({sector}) is on your exclusion list — scored zero.")

        if m_norm >= 0.7:
            reasons.append("Positive price momentum — trending upward recently.")
        elif m_norm < 0.3:
            reasons.append("Weak momentum — price trend has been declining.")

        if growth >= target_ret:
            reasons.append(f"Meets your target return of {target_ret}% (actual: {growth:.1f}%).")
        else:
            reasons.append(f"Does not meet your {target_ret}% target return (actual: {growth:.1f}%).")

        return reasons

    reasons_list = []
    for i, row in df.iterrows():
        reasons_list.append(_build_reasons(
            row,
            float(growth_norm[i]),
            float(vol_norm[i]),
            float(div_norm[i]),
            float(momentum_norm[i]),
        ))

    df["Score"]   = scores.values
    df["Reasons"] = reasons_list

    return df.sort_values("Score", ascending=False).reset_index(drop=True)
