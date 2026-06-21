import streamlit as st

def render():
    st.markdown('<div class="page-heading">Investor Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Define your investment parameters to generate a personalized portfolio recommendation.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.6, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-label">Investment Parameters</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            amount = st.number_input(
                "Investment Amount (PKR)",
                min_value=100000,
                max_value=100000000,
                value=st.session_state.get("investment_amount", 5000000),
                step=100000,
                help="Minimum 100,000 PKR"
            )
        with c2:
            durations = ["1 Year", "2 Years", "3 Years", "5 Years", "7 Years", "10 Years"]
            duration = st.selectbox(
                "Investment Duration",
                durations,
                index=durations.index(st.session_state.get("investment_duration", "5 Years"))
            )

        c3, c4 = st.columns(2, gap="medium")
        with c3:
            risk = st.select_slider(
                "Risk Appetite",
                options=["Conservative", "Low", "Medium", "High", "Aggressive"],
                value=st.session_state.get("risk_appetite", "Medium")
            )
        with c4:
            target_return = st.number_input(
                "Target Return (%)",
                min_value=5,
                max_value=100,
                value=st.session_state.get("target_return", 30),
                step=5
            )

        st.markdown('<div class="section-label">Sector Preferences</div>', unsafe_allow_html=True)

        all_sectors = ["Banking", "Technology", "Energy", "Cement", "Textile", "Pharmaceuticals", "Fertilizer", "Automobile", "Telecom", "FMCG"]

        c5, c6 = st.columns(2, gap="medium")
        with c5:
            preferred = st.multiselect(
                "Preferred Sectors",
                all_sectors,
                default=st.session_state.get("preferred_sectors", ["Banking", "Energy"])
            )
        with c6:
            excluded_options = [s for s in all_sectors if s not in preferred]
            excluded = st.multiselect(
                "Excluded Sectors",
                excluded_options,
                default=[s for s in st.session_state.get("excluded_sectors", []) if s not in preferred]
            )

        st.markdown('<div class="section-label">Additional Preferences</div>', unsafe_allow_html=True)

        c7, c8 = st.columns(2, gap="medium")
        with c7:
            dividend_pref = st.checkbox("Prefer dividend-paying stocks", value=st.session_state.get("dividend_preference", True))
        with c8:
            diversify = st.checkbox("Enforce sector diversification", value=st.session_state.get("enforce_diversification", True))

        notes = st.text_area(
            "Custom Notes (optional)",
            value=st.session_state.get("custom_notes", ""),
            placeholder="e.g. Avoid crypto-related stocks. Focus on blue-chip companies.",
            height=80
        )

        st.markdown("<br>", unsafe_allow_html=True)
        bcol1, bcol2, bcol3 = st.columns([3, 1.2, 2])
        with bcol1:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            generate = st.button("Generate Recommendation", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with bcol2:
            save = st.button("Save Profile", use_container_width=True)

        # ── Save to session_state ──────────────────────────────────────────────
        if save or generate:
            st.session_state["investment_amount"]       = amount
            st.session_state["investment_duration"]     = duration
            st.session_state["risk_appetite"]           = risk
            st.session_state["target_return"]           = target_return
            st.session_state["preferred_sectors"]       = preferred
            st.session_state["excluded_sectors"]        = excluded
            st.session_state["dividend_preference"]     = dividend_pref
            st.session_state["enforce_diversification"] = diversify
            st.session_state["custom_notes"]            = notes
            st.session_state["profile_saved"]           = True
            st.success("Profile saved. Navigate to **Recommendations** to view results.")

    with col_right:
        st.markdown('<div class="section-label">Profile Summary</div>', unsafe_allow_html=True)

        risk_colors = {
            "Conservative": "#3fb950",
            "Low": "#3fb950",
            "Medium": "#d2993a",
            "High": "#f85149",
            "Aggressive": "#f85149"
        }
        risk_color = risk_colors.get(risk, "#8b949e")
        formatted_amount = f"{amount:,.0f}"

        st.markdown(f"""
        <div class="card">
            <div class="card-title">Investment Amount</div>
            <div class="card-value">PKR {formatted_amount}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="info-row">
                <span class="info-key">Duration</span>
                <span class="info-val">{duration}</span>
            </div>
            <div class="info-row">
                <span class="info-key">Risk Appetite</span>
                <span class="info-val" style="color:{risk_color}">{risk}</span>
            </div>
            <div class="info-row">
                <span class="info-key">Target Return</span>
                <span class="info-val">{target_return}%</span>
            </div>
            <div class="info-row">
                <span class="info-key">Dividend Preference</span>
                <span class="info-val">{"Yes" if dividend_pref else "No"}</span>
            </div>
            <div class="info-row">
                <span class="info-key">Diversification</span>
                <span class="info-val">{"Enforced" if diversify else "Flexible"}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if preferred:
            st.markdown('<div class="section-label">Preferred Sectors</div>', unsafe_allow_html=True)
            tags_html = "".join([f'<span class="tag tag-green">{s}</span>' for s in preferred])
            st.markdown(f'<div style="margin-bottom:0.8rem">{tags_html}</div>', unsafe_allow_html=True)

        if excluded:
            st.markdown('<div class="section-label">Excluded Sectors</div>', unsafe_allow_html=True)
            tags_html = "".join([f'<span class="tag tag-red">{s}</span>' for s in excluded])
            st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Heuristic Scoring Weights</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <div class="info-row">
                <span class="info-key">Long-Term Growth</span>
                <span class="info-val">+30</span>
            </div>
            <div class="progress-wrap"><div class="progress-fill" style="width:100%"></div></div>
            <div class="info-row" style="margin-top:0.6rem">
                <span class="info-key">Sector Diversification</span>
                <span class="info-val">+20</span>
            </div>
            <div class="progress-wrap"><div class="progress-fill" style="width:67%"></div></div>
            <div class="info-row" style="margin-top:0.6rem">
                <span class="info-key">Low Volatility</span>
                <span class="info-val">+20</span>
            </div>
            <div class="progress-wrap"><div class="progress-fill" style="width:67%"></div></div>
            <div class="info-row" style="margin-top:0.6rem">
                <span class="info-key">Dividend Stability</span>
                <span class="info-val">+15</span>
            </div>
            <div class="progress-wrap"><div class="progress-fill" style="width:50%"></div></div>
            <div class="info-row" style="margin-top:0.6rem">
                <span class="info-key">Momentum Trend</span>
                <span class="info-val">+15</span>
            </div>
            <div class="progress-wrap"><div class="progress-fill" style="width:50%"></div></div>
        </div>
        """, unsafe_allow_html=True)