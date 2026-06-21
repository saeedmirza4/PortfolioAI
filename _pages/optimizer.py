import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
import sys

# ── Fix import path ───────────────────────────────────────────────────────────
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from scorer import score_stocks
from optimizer_engine import hill_climbing, simulated_annealing

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "stocks.csv")


def render():

    st.markdown(
        '<div class="page-heading">Portfolio Optimizer <span class="week-badge badge-active">Week 3</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subheading">Hill Climbing vs Simulated Annealing</div>',
        unsafe_allow_html=True
    )

    # ── Profile ───────────────────────────────────────────────────────────────
    profile = {
        "risk_appetite": st.session_state.get("risk_appetite", "Medium"),
        "preferred_sectors": st.session_state.get("preferred_sectors", []),
        "excluded_sectors": st.session_state.get("excluded_sectors", []),
        "target_return": st.session_state.get("target_return", 25),
        "dividend_preference": st.session_state.get("dividend_preference", False),
        "enforce_diversification": st.session_state.get("enforce_diversification", True),
    }

    # ── Load data ─────────────────────────────────────────────────────────────
    df = pd.read_csv(DATA_PATH)
    scored_df = score_stocks(df, profile)

    # ── Controls ──────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        iterations = st.slider("Iterations", 100, 1000, 500)

    with c2:
        temp = st.slider("SA Temperature", 10, 200, 100)

    with c3:
        st.selectbox("Goal", ["Balanced", "Maximize Return", "Minimize Risk"])

    # ── BUTTON (FIXED — ALWAYS WORKS) ─────────────────────────────────────────
    run = st.button("Run Optimization", use_container_width=True)

    if run:

        st.write("Running optimization...")

        # ── Run algorithms ────────────────────────────────────────────────────
        hc = hill_climbing(scored_df, profile, iterations)
        sa = simulated_annealing(scored_df, profile, iterations, temp)

        # ── DEBUG SAFETY ───────────────────────────────────────────────────────
        st.write("HC Score:", hc["score"])
        st.write("SA Score:", sa["score"])

        # ── Convergence plot ───────────────────────────────────────────────────
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            y=hc["history"],
            mode="lines",
            name="Hill Climbing",
            line=dict(color="#58a6ff")
        ))

        fig.add_trace(go.Scatter(
            y=sa["history"],
            mode="lines",
            name="Simulated Annealing",
            line=dict(color="#3fb950")
        ))

        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis_title="Iterations",
            yaxis_title="Score"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ── Results ────────────────────────────────────────────────────────────
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Hill Climbing")
            st.metric("Score", f"{hc['score']:.2f}")

        with col2:
            st.subheader("Simulated Annealing")
            st.metric("Score", f"{sa['score']:.2f}")

        # ── Allocation (SA) ────────────────────────────────────────────────────
        st.subheader("Optimized Allocation (SA)")

        for ticker, weight in sa["allocation"].items():
            st.write(f"{ticker}: {weight*100:.2f}%")

        # ── Winner ─────────────────────────────────────────────────────────────
        winner = "Simulated Annealing" if sa["score"] > hc["score"] else "Hill Climbing"

        st.success(f"Winner: {winner}")