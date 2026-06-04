import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render():
    st.markdown('<div class="page-heading">Portfolio Optimizer <span class="week-badge badge-pending">Week 3</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Hill Climbing vs Simulated Annealing — portfolio allocation optimization and comparison.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(88,166,255,0.06); border:1px solid rgba(88,166,255,0.2); border-radius:6px; padding:0.7rem 1rem; font-size:0.78rem; color:#8b949e; margin-bottom:1.5rem;">
        <span style="color:#58a6ff; font-weight:500;">Preview Mode</span> — Showing simulated optimization results. Real algorithms connect in Week 3.
    </div>
    """, unsafe_allow_html=True)

    # ── Controls ──
    ctrl1, ctrl2, ctrl3 = st.columns(3, gap="medium")
    with ctrl1:
        iterations = st.select_slider("Iterations", options=[100, 500, 1000, 2000, 5000], value=1000)
    with ctrl2:
        temp = st.select_slider("Initial Temperature (SA)", options=[10, 50, 100, 500, 1000], value=100)
    with ctrl3:
        constraint = st.selectbox("Optimization Goal", ["Maximize Return", "Minimize Risk", "Balanced"])

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.6, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-label">Convergence Comparison</div>', unsafe_allow_html=True)

        # Dummy convergence curves
        np.random.seed(42)
        x = np.arange(0, iterations + 1, max(1, iterations // 100))

        hc_curve = 60 + 20 * (1 - np.exp(-x / (iterations * 0.15)))
        hc_curve += np.random.normal(0, 0.3, len(x))
        hc_curve = np.clip(hc_curve, 60, 82)

        sa_curve = 58 + 26 * (1 - np.exp(-x / (iterations * 0.25)))
        sa_curve += np.random.normal(0, 0.5, len(x))
        sa_curve = np.clip(sa_curve, 55, 90)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=hc_curve,
            name="Hill Climbing",
            line=dict(color="#58a6ff", width=1.5),
            mode="lines"
        ))
        fig.add_trace(go.Scatter(
            x=x, y=sa_curve,
            name="Simulated Annealing",
            line=dict(color="#3fb950", width=1.5),
            mode="lines"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(
                font=dict(size=11, color="#8b949e", family="Inter"),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(
                showgrid=False,
                title=dict(text="Iterations", font=dict(size=10, color="#484f58", family="Inter")),
                tickfont=dict(size=10, color="#484f58"),
                tickcolor="#30363d"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#21262d",
                gridwidth=1,
                title=dict(text="Portfolio Score", font=dict(size=10, color="#484f58", family="Inter")),
                tickfont=dict(size=10, color="#484f58"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Algorithm cards ──
        st.markdown('<div class="section-label">Algorithm Results</div>', unsafe_allow_html=True)
        ac1, ac2 = st.columns(2, gap="medium")

        with ac1:
            st.markdown("""
            <div class="algo-card">
                <div class="algo-name" style="color:#58a6ff">Hill Climbing</div>
                <div class="info-row">
                    <span class="info-key">Final Score</span>
                    <span class="info-val">81.4</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Est. Return</span>
                    <span class="info-val">26.8%</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Portfolio Risk</span>
                    <span class="info-val" style="color:#d2993a">Medium</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Convergence</span>
                    <span class="info-val">Iter 420</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Local Optima</span>
                    <span class="info-val" style="color:#f85149">Stuck × 3</span>
                </div>
                <div style="margin-top:0.8rem;font-size:0.72rem;color:#484f58;line-height:1.5">
                    Fast convergence. Gets stuck in local optima — may miss globally optimal allocation.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with ac2:
            st.markdown("""
            <div class="algo-card">
                <div class="algo-name" style="color:#3fb950">Simulated Annealing</div>
                <div class="info-row">
                    <span class="info-key">Final Score</span>
                    <span class="info-val">87.2</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Est. Return</span>
                    <span class="info-val">31.4%</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Portfolio Risk</span>
                    <span class="info-val" style="color:#3fb950">Low–Med</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Convergence</span>
                    <span class="info-val">Iter 780</span>
                </div>
                <div class="info-row">
                    <span class="info-key">Escapes</span>
                    <span class="info-val" style="color:#3fb950">7 escapes</span>
                </div>
                <div style="margin-top:0.8rem;font-size:0.72rem;color:#484f58;line-height:1.5">
                    Slower but explores broader solution space. Escapes local optima via temperature decay.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Optimized Allocation ──
        st.markdown('<div class="section-label">Optimized Allocation (Simulated Annealing)</div>', unsafe_allow_html=True)
        allocations = [
            ("MCB", "Banking", 28),
            ("ENGRO", "Fertilizer", 22),
            ("OGDC", "Energy", 20),
            ("HBL", "Banking", 15),
            ("PPL", "Energy", 10),
            ("LUCK", "Cement", 5),
        ]
        for ticker, sector, pct in allocations:
            st.markdown(f"""
            <div class="info-row">
                <span class="info-key"><span style="font-family:'IBM Plex Sans',sans-serif;color:#e6edf3;font-weight:500;width:48px;display:inline-block">{ticker}</span> <span style="font-size:0.72rem">{sector}</span></span>
                <span style="display:flex;align-items:center;gap:0.8rem">
                    <span style="width:120px;display:inline-block">
                        <div class="progress-wrap"><div class="progress-fill" style="width:{pct*3}%;background:#58a6ff"></div></div>
                    </span>
                    <span class="info-val">{pct}%</span>
                </span>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        # ── Risk-Return scatter ──
        st.markdown('<div class="section-label">Risk vs Return</div>', unsafe_allow_html=True)

        np.random.seed(7)
        n = 40
        risks = np.random.uniform(1, 4, n)
        returns = risks * 6 + np.random.normal(0, 3, n)
        returns = np.clip(returns, 5, 40)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=risks, y=returns,
            mode="markers",
            marker=dict(color="#30363d", size=5, line=dict(color="#484f58", width=0.5)),
            name="Portfolios",
            showlegend=False,
        ))
        # Highlight optimal
        fig3.add_trace(go.Scatter(
            x=[2.1], y=[31.4],
            mode="markers",
            marker=dict(color="#3fb950", size=10, symbol="diamond"),
            name="SA Optimal",
        ))
        fig3.add_trace(go.Scatter(
            x=[2.8], y=[26.8],
            mode="markers",
            marker=dict(color="#58a6ff", size=10, symbol="circle"),
            name="HC Result",
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=220,
            margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(font=dict(size=9, color="#8b949e", family="Inter"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(
                showgrid=False,
                title=dict(text="Risk Level", font=dict(size=10, color="#484f58")),
                tickfont=dict(size=9, color="#484f58"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#21262d",
                title=dict(text="Expected Return %", font=dict(size=10, color="#484f58")),
                tickfont=dict(size=9, color="#484f58"),
            ),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        # ── Summary comparison ──
        st.markdown('<div class="section-label">Comparison Summary</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <div class="info-row">
                <span class="info-key">Winner</span>
                <span class="info-val" style="color:#3fb950">Simulated Annealing</span>
            </div>
            <div class="info-row">
                <span class="info-key">Score Improvement</span>
                <span class="info-val">+5.8 pts</span>
            </div>
            <div class="info-row">
                <span class="info-key">Return Improvement</span>
                <span class="info-val">+4.6%</span>
            </div>
            <div class="info-row">
                <span class="info-key">Constraints Met</span>
                <span class="info-val">5 / 5</span>
            </div>
            <div class="info-row">
                <span class="info-key">Runtime (HC)</span>
                <span class="info-val">0.4s</span>
            </div>
            <div class="info-row">
                <span class="info-key">Runtime (SA)</span>
                <span class="info-val">1.2s</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="explain-block">
            Simulated Annealing outperforms Hill Climbing by escaping local optima through probabilistic acceptance of worse solutions during early iterations, allowing broader exploration of the portfolio allocation space.
        </div>
        """, unsafe_allow_html=True)
