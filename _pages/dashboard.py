import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render():
    st.markdown('<div class="page-heading">Final Dashboard <span class="week-badge badge-pending">Week 4</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Complete portfolio overview — allocation, projected growth, and explainability report.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(88,166,255,0.06); border:1px solid rgba(88,166,255,0.2); border-radius:6px; padding:0.7rem 1rem; font-size:0.78rem; color:#8b949e; margin-bottom:1.5rem;">
        <span style="color:#58a6ff; font-weight:500;">Preview Mode</span> — Full MVP integrates all modules in Week 4.
    </div>
    """, unsafe_allow_html=True)

    # ── Top Summary ──
    st.markdown("""
    <div style="display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap;">
        <div class="card" style="flex:1; min-width:160px; margin-bottom:0">
            <div class="card-title">Invested</div>
            <div class="card-value" style="font-size:1.05rem">PKR 5,000,000</div>
        </div>
        <div class="card" style="flex:1; min-width:160px; margin-bottom:0">
            <div class="card-title">Est. Value (5yr)</div>
            <div class="card-value" style="font-size:1.05rem">PKR 8,240,000</div>
        </div>
        <div class="card" style="flex:1; min-width:130px; margin-bottom:0">
            <div class="card-title">Expected Return</div>
            <div class="card-value" style="font-size:1.05rem">31.4%</div>
        </div>
        <div class="card" style="flex:1; min-width:130px; margin-bottom:0">
            <div class="card-title">Portfolio Risk</div>
            <div class="card-value" style="font-size:1.05rem; color:#3fb950">Low–Med</div>
        </div>
        <div class="card" style="flex:1; min-width:110px; margin-bottom:0">
            <div class="card-title">Stocks Selected</div>
            <div class="card-value" style="font-size:1.05rem">6</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-label">Projected Growth</div>', unsafe_allow_html=True)

        years = np.array([0, 1, 2, 3, 4, 5])
        values = [5_000_000, 5_820_000, 6_480_000, 7_050_000, 7_620_000, 8_240_000]
        conservative = [5_000_000, 5_520_000, 5_980_000, 6_400_000, 6_870_000, 7_350_000]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=conservative,
            name="Conservative",
            line=dict(color="#484f58", width=1.5, dash="dot"),
            mode="lines",
            fill=None,
        ))
        fig.add_trace(go.Scatter(
            x=years, y=values,
            name="Optimized Portfolio",
            line=dict(color="#58a6ff", width=2),
            mode="lines+markers",
            marker=dict(size=5, color="#58a6ff"),
            fill="tonexty",
            fillcolor="rgba(88,166,255,0.05)",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(font=dict(size=10, color="#8b949e", family="Inter"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(
                showgrid=False,
                title=dict(text="Year", font=dict(size=10, color="#484f58")),
                tickvals=years,
                ticktext=["Now", "Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5"],
                tickfont=dict(size=10, color="#484f58"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#21262d",
                title=dict(text="Portfolio Value (PKR)", font=dict(size=10, color="#484f58")),
                tickfont=dict(size=9, color="#484f58"),
                tickformat=",.0f",
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Explainability ──
        st.markdown('<div class="section-label">Explainability Report</div>', unsafe_allow_html=True)

        explanations = [
            ("MCB", 28, ["Strong 5yr historical stability", "Low volatility matches medium risk profile", "Consistent 6.2% dividend yield"]),
            ("ENGRO", 22, ["Sector diversification — fertilizer hedge", "Stable dividend payout track record", "Above-average 3yr growth trend"]),
            ("OGDC", 20, ["State-owned reduces default risk", "High 7.4% dividend yield", "Energy sector inflation hedge"]),
            ("HBL", 15, ["2nd largest bank — institutional stability", "Low volatility, reliable returns", "Strong regulatory compliance"]),
            ("PPL", 10, ["Complementary to OGDC energy exposure", "Steady cash flow generation", "Medium risk within budget constraints"]),
            ("LUCK", 5, ["Sector diversification — cement", "Kept at 5% to limit high-volatility exposure", "Growth potential in infrastructure cycle"]),
        ]

        for ticker, alloc, reasons in explanations:
            reason_html = "".join([f"<div>· {r}</div>" for r in reasons])
            st.markdown(f"""
            <div style="margin-bottom:0.8rem">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem">
                    <span style="font-family:'IBM Plex Sans',sans-serif;font-size:0.88rem;font-weight:600;color:#e6edf3">{ticker}</span>
                    <span class="tag tag-blue">{alloc}% allocated</span>
                </div>
                <div class="explain-block">{reason_html}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-label">Portfolio Allocation</div>', unsafe_allow_html=True)

        labels = ["MCB", "ENGRO", "OGDC", "HBL", "PPL", "LUCK"]
        values_pie = [28, 22, 20, 15, 10, 5]
        colors_pie = ["#58a6ff", "#3fb950", "#d2993a", "#388bfd", "#8b949e", "#484f58"]

        fig2 = go.Figure(go.Pie(
            labels=labels,
            values=values_pie,
            hole=0.55,
            marker=dict(colors=colors_pie, line=dict(color="#0f1117", width=2)),
            textinfo="label+percent",
            textfont=dict(size=10, color="#e6edf3", family="Inter"),
            showlegend=False,
            direction="clockwise",
            sort=False,
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin=dict(t=0, b=0, l=0, r=0),
            annotations=[dict(text="Allocation", x=0.5, y=0.5, font_size=11, showarrow=False, font_color="#8b949e", font_family="IBM Plex Sans")]
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-label">Optimization Method</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <div class="info-row">
                <span class="info-key">Algorithm Used</span>
                <span class="info-val" style="color:#3fb950">Simulated Annealing</span>
            </div>
            <div class="info-row">
                <span class="info-key">Iterations Run</span>
                <span class="info-val">1,000</span>
            </div>
            <div class="info-row">
                <span class="info-key">Constraints Met</span>
                <span class="info-val">5 / 5</span>
            </div>
            <div class="info-row">
                <span class="info-key">Budget Used</span>
                <span class="info-val">100%</span>
            </div>
            <div class="info-row">
                <span class="info-key">Sectors Covered</span>
                <span class="info-val">4 of 10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Constraints Satisfied</div>', unsafe_allow_html=True)
        constraints = [
            ("Budget limit", True),
            ("Max risk: Medium", True),
            ("Min sectors: 3", True),
            ("Excluded: Crypto", True),
            ("Target return: 30%+", True),
        ]
        for label, met in constraints:
            color = "#3fb950" if met else "#f85149"
            icon = "✓" if met else "✗"
            st.markdown(f"""
            <div class="info-row">
                <span class="info-key">{label}</span>
                <span style="color:{color};font-size:0.82rem;font-weight:500">{icon}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        st.button("Export Full Report", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.button("Download Allocation CSV", use_container_width=True)