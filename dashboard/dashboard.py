import streamlit as st

st.set_page_config(
    page_title="ED Triage Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ─────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    .header-bar {
        background-color: #1A2E4A;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    .header-sub {
        color: #9ECDD4;
        font-size: 0.85rem;
        margin: 0;
    }
    .metric-pill {
        background-color: #0F7B8C;
        color: white;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .section-title {
        color: #1A2E4A;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #0F7B8C;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <div>
        <p class="header-title">🏥 ED Triage Dashboard</p>
        <p class="header-sub">Emergency Department — Nurse Command Interface</p>
    </div>
    <div>
        <span class="metric-pill">0 Patients Waiting</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: sidebar + main ────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">Allotment Panel</p>', unsafe_allow_html=True)
    st.caption("Department availability will appear here.")

main_col, spacer = st.columns([4, 0.1])

with main_col:
    st.markdown('<p class="section-title">Patient Queue</p>', unsafe_allow_html=True)
    st.caption("Incoming patients will appear here once the queue is wired up.")