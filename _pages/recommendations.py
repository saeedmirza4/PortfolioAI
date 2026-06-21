"""
recommendations.py — Page 2: AI Recommendations
PortfolioAI · Week 2

Connects investor profile (session_state) → scorer → live charts + explainability.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

# ── Import scorer (self-contained fallback if Student 1 hasn't delivered yet) ──
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scorer import score_stocks

# ── Constants ──────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "stocks.csv")

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8b949e", size=11),
    margin=dict(l=0, r=0, t=30, b=0),
)

TOP_N = 7  # stocks shown as top (blue bars)


# ── Helpers ────────────────────────────────────────────────────────────────────
def _load_data():
    if not os.path.exists(DATA_PATH):
        st.error("stocks.csv not found in data/ folder.")
        st.stop()
    return pd.read_csv(DATA_PATH)


def _get_profile():
    """Pull investor profile from session_state, return defaults if not set."""
    s = st.session_state
    return {
        "risk_appetite":          s.get("risk_appetite", "Medium"),
        "preferred_sectors":      s.get("preferred_sectors", []),
        "excluded_sectors":       s.get("excluded_sectors", []),
        "target_return":          s.get("target_return", 25),
        "dividend_preference":    s.get("dividend_preference", False),
        "enforce_diversification": s.get("enforce_diversification", True),
        "investment_amount":      s.get("investment_amount", 5000000),
    }


def _risk_color(label):
    return {"Low": "#3fb950", "Medium": "#d2993a", "High": "#f85149"}.get(label, "#8b949e")


def _score_bar_chart(scored_df):
    tickers = scored_df["Ticker"].tolist()
    scores  = scored_df["Score"].tolist()
    colors  = ["#58a6ff" if i < TOP_N else "#30363d" for i in range(len(tickers))]

    fig = go.Figure(go.Bar(
        x=tickers,
        y=scores,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{s:.0f}" for s in scores],
        textposition="outside",
        textfont=dict(color="#8b949e", size=10),
    ))
    fig.update_layout(
        **PLOTLY_BASE,
        height=240,
        yaxis=dict(range=[0, 110], showgrid=True, gridcolor="#21262d",
                   zeroline=False, tickfont=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#e6edf3")),
        bargap=0.35,
    )
    return fig


def _sector_pie(scored_df):
    top = scored_df.head(TOP_N)
    sector_counts = top["Sector"].value_counts().reset_index()
    sector_counts.columns = ["Sector", "Count"]

    COLORS = ["#58a6ff", "#3fb950", "#d2993a", "#f85149", "#a371f7",
              "#79c0ff", "#56d364", "#ffa657"]

    fig = go.Figure(go.Pie(
        labels=sector_counts["Sector"],
        values=sector_counts["Count"],
        hole=0.55,
        marker=dict(colors=COLORS[:len(sector_counts)],
                    line=dict(color="#0f1117", width=2)),
        textinfo="label+percent",
        textfont=dict(size=10, color="#e6edf3"),
        hovertemplate="<b>%{label}</b><br>%{value} stock(s)<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_BASE, height=220,
                      showlegend=False,
                      annotations=[dict(text="Sectors", x=0.5, y=0.5,
                                        font=dict(size=11, color="#8b949e"),
                                        showarrow=False)])
    return fig


# ── Main render ────────────────────────────────────────────────────────────────
def render():
    st.markdown('<h1 class="page-heading">Recommendations <span class="week-badge badge-active">WEEK 2</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheading">AI-scored stocks based on your investor profile.</p>', unsafe_allow_html=True)

    # Load & score
    raw_df  = _load_data()
    profile = _get_profile()
    scored  = score_stocks(raw_df, profile)

    if scored.empty:
        st.warning("All stocks were excluded by your sector filters. Adjust excluded sectors on the Investor Profile page.")
        return

    top_stocks    = scored.head(TOP_N)
    avg_score     = top_stocks["Score"].mean()
    avg_dividend  = top_stocks["Dividend_Yield"].mean()
    total_analyzed = len(scored)

    # ── Profile source notice ──
    if not st.session_state.get("profile_saved", False):
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-left:3px solid #d2993a;
        border-radius:0 6px 6px 0;padding:0.7rem 1rem;font-size:0.8rem;color:#8b949e;margin-bottom:1.5rem;">
        <b style="color:#d2993a;">Using default profile</b> — go to Investor Profile and click
        <b>Save Profile</b> to personalise these recommendations.
        </div>""", unsafe_allow_html=True)

    # ── Metric row ─────────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Stocks Analyzed", total_analyzed, f"PSX dataset")
    with m2:
        st.metric("Recommended", TOP_N, "Above threshold")
    with m3:
        st.metric("Avg Score", f"{avg_score:.1f}", f"+{avg_score - 50:.1f} vs baseline")
    with m4:
        st.metric("Avg Dividend Yield", f"{avg_dividend:.1f}%", "Target: 5%+")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Charts row ─────────────────────────────────────────────────────────────
    col_chart, col_pie = st.columns([3, 2], gap="large")

    with col_chart:
        st.markdown('<div class="section-label">Scored Stock List</div>', unsafe_allow_html=True)
        st.plotly_chart(_score_bar_chart(scored), use_container_width=True, config={"displayModeBar": False})

    with col_pie:
        st.markdown('<div class="section-label">Sector Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(_sector_pie(scored), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Stock cards ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Top Recommended Stocks</div>', unsafe_allow_html=True)

    for _, row in top_stocks.iterrows():
        risk_col   = _risk_color(str(row["Volatility_Label"]))
        score_pct  = int(row["Score"])
        reasons    = row["Reasons"]  # list of strings

        with st.expander(f"**{row['Ticker']}** — {row['Company']}   |   Score: {score_pct}", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"""
                <div class="card-title">Score</div>
                <div class="card-value" style="color:#58a6ff;">{score_pct}<span>/ 100</span></div>
                <div class="progress-wrap" style="margin-top:0.5rem;">
                  <div class="progress-fill" style="width:{score_pct}%;"></div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="card-title">Sector</div>
                <div style="margin-top:0.3rem;">
                  <span class="tag tag-blue">{row['Sector']}</span>
                </div>
                <div style="font-size:0.75rem;color:#8b949e;margin-top:0.4rem;">
                  Growth: <b style="color:#e6edf3;">{row['Avg_Annual_Growth']:.1f}%</b>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="card-title">Volatility</div>
                <div style="margin-top:0.3rem;">
                  <span class="tag" style="color:{risk_col};border-color:{risk_col}33;
                  background:{risk_col}11;">{row['Volatility_Label']}</span>
                </div>
                <div style="font-size:0.75rem;color:#8b949e;margin-top:0.4rem;">
                  {row['Volatility_Pct']:.1f}% std dev
                </div>""", unsafe_allow_html=True)
            with c4:
                st.markdown(f"""
                <div class="card-title">Dividend Yield</div>
                <div class="card-value">{row['Dividend_Yield']:.1f}<span>%</span></div>
                <div style="font-size:0.75rem;color:#8b949e;margin-top:0.2rem;">
                  Stability: {row['Stability_Score']}/100
                </div>""", unsafe_allow_html=True)

            # Explainability block
            reason_html = "".join(f"<li>{r}</li>" for r in reasons)
            st.markdown(f"""
            <div class="explain-block">
              <b style="color:#58a6ff;">{row['Ticker']}</b> was selected because of:<br>
              <ul style="margin:0.4rem 0 0 1rem;padding:0;line-height:1.8;">
                {reason_html}
              </ul>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Risk profile match card ────────────────────────────────────────────────
    st.markdown('<div class="section-label">Risk Profile Match</div>', unsafe_allow_html=True)

    risk = profile["risk_appetite"]
    high_risk_count = len(top_stocks[top_stocks["Volatility_Label"].astype(str) == "High"])
    low_risk_count  = len(top_stocks[top_stocks["Volatility_Label"].astype(str) == "Low"])

    st.markdown(f"""
    <div class="card">
      <div class="info-row">
        <span class="info-key">Investor Risk Appetite</span>
        <span class="info-val">{risk}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Low Volatility Stocks in Portfolio</span>
        <span class="info-val" style="color:#3fb950;">{low_risk_count} of {TOP_N}</span>
      </div>
      <div class="info-row">
        <span class="info-key">High Volatility Stocks in Portfolio</span>
        <span class="info-val" style="color:#f85149;">{high_risk_count} of {TOP_N}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Preferred Sectors</span>
        <span class="info-val">{", ".join(profile["preferred_sectors"]) if profile["preferred_sectors"] else "None specified"}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Excluded Sectors</span>
        <span class="info-val">{", ".join(profile["excluded_sectors"]) if profile["excluded_sectors"] else "None"}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Dividend Preference</span>
        <span class="info-val">{"Yes" if profile["dividend_preference"] else "No"}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
