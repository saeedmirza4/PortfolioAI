import streamlit as st

st.set_page_config(
    page_title="PortfolioAI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
[data-testid="stSidebar"] {
    margin-left: 0 !important;
    transform: none !important;
    visibility: visible !important;
    width: 220px !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    margin-left: 0 !important;
    transform: translateX(0) !important;
}
</style>
""", unsafe_allow_html=True)
# ── Global Styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=Inter:wght@300;400;500&display=swap');

/* Reset & Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f1117;
    color: #e6edf3;
}

/* Dot grid background */
.stApp {
    background-color: #0f1117;
    background-image: radial-gradient(circle, #21262d 1px, transparent 1px);
    background-size: 28px 28px;
}

/* Fade the dot grid at edges */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at center, transparent 40%, #0f1117 100%);
    pointer-events: none;
    z-index: 0;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
button[data-testid="stSidebarCollapseButton"] { display: none !important; }
svg[data-testid="stSidebarCollapseButton"] { display: none !important; }
.st-emotion-cache-eczf16 { display: none !important; }

.block-container {
    padding: 2rem 2.5rem 2rem 2.5rem;
    max-width: 1100px;
    position: relative;
    z-index: 1;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #21262d !important;
    padding-top: 0 !important;
    position: relative;
    z-index: 2;
}
/* Blue top accent bar on sidebar */
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, #58a6ff 0%, #1f6feb 60%, transparent 100%);
    margin-bottom: 1.5rem;
}
[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif; }

/* Sidebar brand */
.sidebar-brand {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #e6edf3;
    letter-spacing: 0.04em;
    padding: 0 1.2rem 1.8rem 1.2rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.2rem;
}
.sidebar-brand span {
    color: #58a6ff;
}
.sidebar-label {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #484f58;
    padding: 0 1.2rem;
    margin-bottom: 0.4rem;
}

/* Nav buttons */
.stRadio > div { gap: 0 !important; }
.stRadio label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    color: #8b949e !important;
    padding: 0.5rem 1.2rem !important;
    border-radius: 4px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    display: block !important;
    width: 100% !important;
}
.stRadio label:hover { color: #e6edf3 !important; background: #161b22 !important; }
[data-testid="stRadio"] input:checked + div p {
    color: #e6edf3 !important;
    font-weight: 500 !important;
}

/* Page heading */
.page-heading {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #e6edf3;
    letter-spacing: -0.01em;
    margin-bottom: 0.25rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #21262d;
    position: relative;
}
.page-heading::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 48px;
    height: 2px;
    background: #58a6ff;
    border-radius: 2px;
}
.page-subheading {
    font-size: 0.82rem;
    color: #8b949e;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
}

/* Card */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03);
    transition: border-color 0.2s ease;
}
.card:hover { border-color: #484f58; }
.card-title {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #484f58;
    margin-bottom: 0.5rem;
}
.card-value {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #e6edf3;
    line-height: 1.2;
}
.card-value span {
    font-size: 0.8rem;
    font-weight: 400;
    color: #8b949e;
    margin-left: 0.3rem;
}
.card-delta-pos {
    font-size: 0.75rem;
    color: #3fb950;
    margin-top: 0.3rem;
}
.card-delta-neg {
    font-size: 0.75rem;
    color: #f85149;
    margin-top: 0.3rem;
}

/* Section label */
.section-label {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #484f58;
    margin-bottom: 0.8rem;
    margin-top: 1.6rem;
}

/* Form inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 2px rgba(88,166,255,0.1) !important;
}

/* Slider */
[data-testid="stSlider"] {
    padding: 0.5rem 0;
}

/* Button */
.stButton > button {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background-color: #30363d !important;
    border-color: #58a6ff !important;
    color: #58a6ff !important;
}

/* Primary button */
.primary-btn > button {
    background-color: #1f6feb !important;
    border: 1px solid #1f6feb !important;
    color: #ffffff !important;
    white-space: nowrap !important;
    min-width: 220px !important;
}
.primary-btn > button:hover {
    background-color: #388bfd !important;
    border-color: #388bfd !important;
    color: #ffffff !important;
    white-space: nowrap !important;
}

/* Table */
[data-testid="stDataFrame"] {
    border: 1px solid #30363d;
    border-radius: 8px;
    overflow: hidden;
}

/* Metric override */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.03);
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, #1f6feb, transparent);
}
[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #484f58 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 1.5rem !important;
    color: #e6edf3 !important;
}

/* Tag / badge */
.tag {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 500;
    color: #8b949e;
    padding: 0.15rem 0.5rem;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
    letter-spacing: 0.03em;
}
.tag-blue {
    background: rgba(88,166,255,0.08);
    border-color: rgba(88,166,255,0.25);
    color: #58a6ff;
}
.tag-green {
    background: rgba(63,185,80,0.08);
    border-color: rgba(63,185,80,0.25);
    color: #3fb950;
}
.tag-red {
    background: rgba(248,81,73,0.08);
    border-color: rgba(248,81,73,0.25);
    color: #f85149;
}
.tag-yellow {
    background: rgba(210,153,34,0.08);
    border-color: rgba(210,153,34,0.25);
    color: #d2993a;
}

/* Status dot */
.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}

/* Explanation block */
.explain-block {
    background: #0d1117;
    border: 1px solid #21262d;
    border-left: 3px solid #58a6ff;
    border-radius: 0 6px 6px 0;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #8b949e;
    line-height: 1.6;
    margin-top: 0.5rem;
}

/* Info row */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid #21262d;
    font-size: 0.82rem;
}
.info-row:last-child { border-bottom: none; }
.info-key { color: #8b949e; }
.info-val { color: #e6edf3; font-weight: 500; font-family: 'IBM Plex Sans', sans-serif; }

/* Progress bar custom */
.progress-wrap {
    background: #21262d;
    border-radius: 3px;
    height: 4px;
    margin-top: 0.4rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 3px;
    background: #58a6ff;
}

/* Algo comparison */
.algo-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
}
.algo-name {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.8rem;
}

/* Week status badge */
.week-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 3px;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.badge-done { background: rgba(63,185,80,0.12); color: #3fb950; border: 1px solid rgba(63,185,80,0.25); }
.badge-active { background: rgba(88,166,255,0.12); color: #58a6ff; border: 1px solid rgba(88,166,255,0.25); }
.badge-pending { background: rgba(72,79,88,0.3); color: #484f58; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Portfolio<span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Investor Profile", "Recommendations", "Portfolio Optimizer", "Final Dashboard"],
        label_visibility="collapsed"
    )

  

# ── Page Router ────────────────────────────────────────────────────────────────
import importlib

if page == "Investor Profile":
    from _pages import profile
    importlib.reload(profile)
    profile.render()
elif page == "Recommendations":
    from _pages import recommendations
    importlib.reload(recommendations)
    recommendations.render()
elif page == "Portfolio Optimizer":
    from _pages import optimizer
    importlib.reload(optimizer)
    optimizer.render()
elif page == "Final Dashboard":
    from _pages import dashboard
    importlib.reload(dashboard)
    dashboard.render()