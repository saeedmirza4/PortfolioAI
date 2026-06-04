import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

DUMMY_STOCKS = [
    {"ticker": "MCB", "name": "MCB Bank Ltd", "sector": "Banking", "score": 87, "growth": 18.4, "volatility": "Low", "dividend": 6.2, "risk": "Low", "stability": 92},
    {"ticker": "ENGRO", "name": "Engro Corporation", "sector": "Fertilizer", "score": 81, "growth": 15.1, "volatility": "Medium", "dividend": 5.8, "risk": "Medium", "stability": 85},
    {"ticker": "HBL", "name": "Habib Bank Ltd", "sector": "Banking", "score": 79, "growth": 14.7, "volatility": "Low", "dividend": 5.1, "risk": "Low", "stability": 88},
    {"ticker": "OGDC", "name": "Oil & Gas Dev Corp", "sector": "Energy", "score": 76, "growth": 12.3, "volatility": "Medium", "dividend": 7.4, "risk": "Medium", "stability": 80},
    {"ticker": "PPL", "name": "Pakistan Petroleum", "sector": "Energy", "score": 72, "growth": 11.8, "volatility": "Medium", "dividend": 6.9, "risk": "Medium", "stability": 78},
    {"ticker": "LUCK", "name": "Lucky Cement", "sector": "Cement", "score": 68, "growth": 10.5, "volatility": "High", "dividend": 3.2, "risk": "High", "stability": 70},
    {"ticker": "PSO", "name": "Pakistan State Oil", "sector": "Energy", "score": 65, "growth": 9.8, "volatility": "Medium", "dividend": 4.5, "risk": "Medium", "stability": 74},
]

EXPLANATIONS = {
    "MCB": ["Strong 5-year historical stability (92/100)", "Consistent dividend yield of 6.2%", "Low volatility — suitable for medium risk profile", "Leading position in banking sector"],
    "ENGRO": ["Diversified revenue across fertilizer and energy", "Stable dividend payout history", "Sector diversification benefit to portfolio", "Above-average growth trend over 3 years"],
    "HBL": ["Second largest bank by assets in Pakistan", "Strong regulatory compliance record", "Low volatility with consistent returns", "High dividend reliability score"],
    "OGDC": ["State-owned — lower default risk", "High dividend yield of 7.4%", "Energy sector hedge against inflation", "Consistent cash flow generation"],
}

def render():
    st.markdown('<div class="page-heading">Recommendations <span class="week-badge badge-pending">Week 2</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">AI-scored stocks based on your investor profile. Full logic active from Week 2.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(88,166,255,0.06); border:1px solid rgba(88,166,255,0.2); border-radius:6px; padding:0.7rem 1rem; font-size:0.78rem; color:#8b949e; margin-bottom:1.5rem;">
        <span style="color:#58a6ff; font-weight:500;">Preview Mode</span> — Showing sample data. Real scoring engine connects in Week 2.
    </div>
    """, unsafe_allow_html=True)

    # ── Top metrics ──
    m1, m2, m3, m4 = st.columns(4, gap="medium")
    with m1:
        st.metric("Stocks Analyzed", "47", "PSX dataset")
    with m2:
        st.metric("Recommended", "7", "Above threshold")
    with m3:
        st.metric("Avg Score", "75.4", "+12 vs baseline")
    with m4:
        st.metric("Avg Dividend Yield", "5.6%", "Target: 5%+")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.8, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-label">Scored Stock List</div>', unsafe_allow_html=True)

        df = pd.DataFrame(DUMMY_STOCKS)

        # Score bar chart
        fig = go.Figure()
        colors = ["#58a6ff" if s >= 80 else "#8b949e" if s >= 70 else "#484f58" for s in df["score"]]
        fig.add_trace(go.Bar(
            x=df["ticker"],
            y=df["score"],
            marker_color=colors,
            marker_line_width=0,
            text=df["score"],
            textposition="outside",
            textfont=dict(color="#8b949e", size=11, family="IBM Plex Sans"),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=0, r=0),
            height=220,
            yaxis=dict(showgrid=False, showticklabels=False, range=[0, 105]),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(color="#8b949e", size=11, family="IBM Plex Sans"),
                tickcolor="#30363d"
            ),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Stock table
        for stock in DUMMY_STOCKS:
            vol_tag = {
                "Low": "tag-green",
                "Medium": "tag-yellow",
                "High": "tag-red"
            }.get(stock["volatility"], "tag")

            risk_tag = {
                "Low": "tag-green",
                "Medium": "tag-yellow",
                "High": "tag-red"
            }.get(stock["risk"], "tag")

            score_color = "#58a6ff" if stock["score"] >= 80 else "#8b949e" if stock["score"] >= 70 else "#484f58"
            score_pct = stock["score"]

            with st.expander(f"**{stock['ticker']}** — {stock['name']}", expanded=(stock['ticker'] == 'MCB')):
                ec1, ec2, ec3 = st.columns([1, 1, 1])
                with ec1:
                    st.markdown(f"""
                    <div class="card-title">Heuristic Score</div>
                    <div style="font-family:'IBM Plex Sans',sans-serif;font-size:1.8rem;font-weight:600;color:{score_color}">{stock['score']}<span style="font-size:0.8rem;color:#8b949e">/100</span></div>
                    <div class="progress-wrap" style="margin-top:0.5rem"><div class="progress-fill" style="width:{score_pct}%;background:{score_color}"></div></div>
                    """, unsafe_allow_html=True)
                with ec2:
                    st.markdown(f"""
                    <div class="card-title">Sector</div>
                    <div style="font-size:0.85rem;color:#e6edf3;margin-bottom:0.5rem">{stock['sector']}</div>
                    <div class="card-title" style="margin-top:0.5rem">Volatility</div>
                    <span class="tag {vol_tag}">{stock['volatility']}</span>
                    """, unsafe_allow_html=True)
                with ec3:
                    st.markdown(f"""
                    <div class="card-title">Avg Growth</div>
                    <div style="font-size:0.85rem;color:#3fb950;margin-bottom:0.5rem">+{stock['growth']}% / yr</div>
                    <div class="card-title" style="margin-top:0.5rem">Dividend Yield</div>
                    <div style="font-size:0.85rem;color:#e6edf3">{stock['dividend']}%</div>
                    """, unsafe_allow_html=True)

                if stock["ticker"] in EXPLANATIONS:
                    reasons = "".join([f"<div>· {r}</div>" for r in EXPLANATIONS[stock["ticker"]]])
                    st.markdown(f"""
                    <div class="explain-block">
                        <div style="font-size:0.7rem;font-weight:500;letter-spacing:0.06em;text-transform:uppercase;color:#58a6ff;margin-bottom:0.4rem">Why selected</div>
                        {reasons}
                    </div>
                    """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-label">Sector Distribution</div>', unsafe_allow_html=True)

        sector_counts = df.groupby("sector").size().reset_index(name="count")
        fig2 = go.Figure(go.Pie(
            labels=sector_counts["sector"],
            values=sector_counts["count"],
            hole=0.6,
            marker=dict(
                colors=["#58a6ff", "#3fb950", "#d2993a", "#8b949e", "#388bfd"],
                line=dict(color="#0f1117", width=2)
            ),
            textinfo="label+percent",
            textfont=dict(size=10, color="#8b949e", family="Inter"),
            showlegend=False,
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0, b=0, l=0, r=0),
            height=220,
            annotations=[dict(text="Sectors", x=0.5, y=0.5, font_size=11, showarrow=False, font_color="#8b949e", font_family="IBM Plex Sans")]
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        # Risk summary
        st.markdown('<div class="section-label">Risk Profile Match</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <div class="info-row">
                <span class="info-key">Your Profile</span>
                <span class="info-val" style="color:#d2993a">Medium</span>
            </div>
            <div class="info-row">
                <span class="info-key">Portfolio Risk</span>
                <span class="info-val" style="color:#3fb950">Low–Medium</span>
            </div>
            <div class="info-row">
                <span class="info-key">Match Score</span>
                <span class="info-val">92%</span>
            </div>
            <div class="info-row">
                <span class="info-key">Est. Return</span>
                <span class="info-val">28–34%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Top Picks</div>', unsafe_allow_html=True)
        for s in DUMMY_STOCKS[:4]:
            score_color = "#58a6ff" if s["score"] >= 80 else "#8b949e"
            st.markdown(f"""
            <div class="info-row">
                <span class="info-key"><span style="font-family:'IBM Plex Sans',sans-serif;color:#e6edf3;font-weight:500">{s['ticker']}</span> · {s['sector']}</span>
                <span style="font-family:'IBM Plex Sans',sans-serif;font-size:0.82rem;font-weight:600;color:{score_color}">{s['score']}</span>
            </div>
            """, unsafe_allow_html=True)
