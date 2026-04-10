import streamlit as st

st.set_page_config(
    page_title="TrivaMed — ED Dashboard",
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
    .header-title { color: white; font-size: 1.4rem; font-weight: 700; margin: 0; }
    .header-sub   { color: #9ECDD4; font-size: 0.85rem; margin: 0; }
    .metric-pill  {
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
    .dept-card {
        background-color: #F5F7FA;
        border: 1px solid #C4D0D8;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.6rem;
    }
    .dept-name  { font-weight: 700; color: #1A2E4A; font-size: 0.9rem; }
    .dept-beds  { font-size: 0.8rem; color: #4A5568; margin-top: 2px; }
    .beds-ok    { color: #276749; font-weight: 700; }
    .beds-warn  { color: #B7580A; font-weight: 700; }
    .beds-full  { color: #9B2335; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Session state — allotment data ────────────────────────────────────
if "allotment" not in st.session_state:
    st.session_state.allotment = {
        "Resus":   {"total": 4,  "available": 2, "doctors": 3, "nurses": 4},
        "Majors":  {"total": 12, "available": 5, "doctors": 2, "nurses": 6},
        "Minors":  {"total": 10, "available": 8, "doctors": 1, "nurses": 3},
        "Paeds":   {"total": 6,  "available": 3, "doctors": 1, "nurses": 2},
    }
    st.session_state.wait_times = {
        "ESI 1": 0, "ESI 2": 8, "ESI 3": 35, "ESI 4": 65, "ESI 5": 110
    }

# ── Header ────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <div>
        <p class="header-title">🏥 TrivaMed — ED Triage Dashboard</p>
        <p class="header-sub">Emergency Department — Nurse Command Interface</p>
    </div>
    <div>
        <span class="metric-pill">0 Patients Waiting</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar — Allotment Panel ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">⚕️ Allotment Panel</p>', unsafe_allow_html=True)

    # Department beds
    st.markdown("**Bed Availability**")
    for dept, data in st.session_state.allotment.items():
        avail = data["available"]
        total = data["total"]
        pct   = avail / total

        if pct > 0.5:
            bed_class = "beds-ok"
        elif pct > 0.2:
            bed_class = "beds-warn"
        else:
            bed_class = "beds-full"

        st.markdown(f"""
        <div class="dept-card">
            <div class="dept-name">{dept}</div>
            <div class="dept-beds">
                Beds: <span class="{bed_class}">{avail} available</span> / {total} total
                &nbsp;|&nbsp; 👨‍⚕️ {data['doctors']} doctors
                &nbsp;|&nbsp; 👩‍⚕️ {data['nurses']} nurses
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Manual overrides
    st.markdown("**Update Availability**")
    dept_choice = st.selectbox("Department", list(st.session_state.allotment.keys()))
    new_avail   = st.number_input(
        "Available beds",
        min_value=0,
        max_value=st.session_state.allotment[dept_choice]["total"],
        value=st.session_state.allotment[dept_choice]["available"],
    )
    new_doctors = st.number_input(
        "Doctors on shift",
        min_value=0, max_value=20,
        value=st.session_state.allotment[dept_choice]["doctors"],
    )
    new_nurses  = st.number_input(
        "Nurses on shift",
        min_value=0, max_value=40,
        value=st.session_state.allotment[dept_choice]["nurses"],
    )

    if st.button("Update", use_container_width=True):
        st.session_state.allotment[dept_choice]["available"] = new_avail
        st.session_state.allotment[dept_choice]["doctors"]   = new_doctors
        st.session_state.allotment[dept_choice]["nurses"]    = new_nurses
        st.success(f"{dept_choice} updated.")

    st.divider()

    # Wait times
    st.markdown("**Estimated Wait Times (mins)**")
    for level, mins in st.session_state.wait_times.items():
        st.session_state.wait_times[level] = st.number_input(
            level, min_value=0, max_value=300, value=mins
        )

# ── Main panel ────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Patient Queue</p>', unsafe_allow_html=True)
st.caption("Incoming patients will appear here in the next step.")