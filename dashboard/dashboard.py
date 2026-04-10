import streamlit as st
from datetime import datetime, timedelta
import random
from textwrap import dedent

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
    .dept-name { font-weight: 700; color: #1A2E4A; font-size: 0.9rem; }
    .dept-beds { font-size: 0.8rem; color: #4A5568; margin-top: 2px; }
    .beds-ok   { color: #276749; font-weight: 700; }
    .beds-warn { color: #B7580A; font-weight: 700; }
    .beds-full { color: #9B2335; font-weight: 700; }
    .patient-card {
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
        border-left: 5px solid #ccc;
    }
    .esi-1 { background-color: #FFF5F5; border-left-color: #9B2335; }
    .esi-2 { background-color: #FFF8F0; border-left-color: #B7580A; }
    .esi-3 { background-color: #FFFFF0; border-left-color: #856404; }
    .esi-4 { background-color: #F0FFF4; border-left-color: #276749; }
    .esi-5 { background-color: #F5F7FA; border-left-color: #4A5568; }
    .patient-name  { font-weight: 700; color: #1A2E4A; font-size: 0.95rem; }
    .patient-meta  { font-size: 0.8rem; color: #4A5568; margin-top: 2px; }
    .patient-complaint { font-size: 0.85rem; color: #2D3748; margin-top: 4px; }
    .esi-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 6px;
    }
    .badge-1 { background-color: #9B2335; color: white; }
    .badge-2 { background-color: #B7580A; color: white; }
    .badge-3 { background-color: #856404; color: white; }
    .badge-4 { background-color: #276749; color: white; }
    .badge-5 { background-color: #4A5568; color: white; }
    .redflag { background-color: #9B2335; color: white; border-radius: 10px;
               padding: 1px 8px; font-size: 0.72rem; font-weight: 700;
               margin-right: 4px; }
    .ai-summary { font-size: 0.8rem; color: #4A5568; margin-top: 6px;
                  font-style: italic; border-left: 3px solid #0F7B8C;
                  padding-left: 8px; }
    .time-ago { font-size: 0.75rem; color: #718096; }
</style>
""", unsafe_allow_html=True)

# ── ESI helpers ───────────────────────────────────────────────────────
ESI_LABELS = {1: "Immediate", 2: "Emergent", 3: "Urgent", 4: "Less Urgent", 5: "Non-Urgent"}

def esi_badge(score):
    return f'<span class="esi-badge badge-{score}">ESI {score} — {ESI_LABELS[score]}</span>'

def red_flag_badges(flags):
    if not flags or flags == ["none"]:
        return ""
    return " ".join(f'<span class="redflag">⚠ {f.upper()}</span>' for f in flags)

def time_ago(dt):
    diff = datetime.now() - dt
    mins = int(diff.total_seconds() / 60)
    if mins < 1:
        return "Just now"
    elif mins == 1:
        return "1 min ago"
    else:
        return f"{mins} mins ago"

# ── Session state ─────────────────────────────────────────────────────
if "allotment" not in st.session_state:
    st.session_state.allotment = {
        "Resus":  {"total": 4,  "available": 2, "doctors": 3, "nurses": 4},
        "Majors": {"total": 12, "available": 5, "doctors": 2, "nurses": 6},
        "Minors": {"total": 10, "available": 8, "doctors": 1, "nurses": 3},
        "Paeds":  {"total": 6,  "available": 3, "doctors": 1, "nurses": 2},
    }
    st.session_state.wait_times = {
        "ESI 1": 0, "ESI 2": 8, "ESI 3": 35, "ESI 4": 65, "ESI 5": 110
    }

if "patients" not in st.session_state:
    now = datetime.now()
    st.session_state.patients = [
        {
            "session_id": "aaa-001",
            "name": "John Smith",
            "age": 58,
            "gender": "Male",
            "chief_complaint": "Severe chest pain radiating to left arm",
            "esi_score": 2,
            "red_flags": ["MI"],
            "ai_summary": "58-year-old male with severe chest pain and left arm radiation. "
                          "Onset 40 mins ago. Hypertensive. High suspicion of MI.",
            "pain_score": 8,
            "is_worsening": True,
            "symptoms": ["Chest pain", "Left arm pain", "Shortness of breath"],
            "conditions": ["Hypertension"],
            "medications": ["Lisinopril"],
            "allergies": ["Penicillin"],
            "submitted_at": now - timedelta(minutes=5),
            "allocated": False,
        },
        {
            "session_id": "aaa-002",
            "name": "Sarah O'Brien",
            "age": 34,
            "gender": "Female",
            "chief_complaint": "Sudden severe headache, worst of life",
            "esi_score": 2,
            "red_flags": ["stroke"],
            "ai_summary": "34-year-old female with thunderclap headache. "
                          "Sudden onset, 10/10 severity. Stroke protocol warranted.",
            "pain_score": 10,
            "is_worsening": False,
            "symptoms": ["Severe headache", "Neck stiffness", "Photophobia"],
            "conditions": [],
            "medications": [],
            "allergies": [],
            "submitted_at": now - timedelta(minutes=12),
            "allocated": False,
        },
        {
            "session_id": "aaa-003",
            "name": "Mohammed Al-Farsi",
            "age": 72,
            "gender": "Male",
            "chief_complaint": "High fever, confusion, rapid breathing",
            "esi_score": 1,
            "red_flags": ["sepsis"],
            "ai_summary": "72-year-old male with fever 39.8C, acute confusion and tachypnoea. "
                          "Sepsis screening required immediately.",
            "pain_score": 4,
            "is_worsening": True,
            "symptoms": ["Fever", "Confusion", "Rapid breathing", "Chills"],
            "conditions": ["Diabetes", "COPD"],
            "medications": ["Metformin", "Salbutamol inhaler"],
            "allergies": ["Sulfa drugs"],
            "submitted_at": now - timedelta(minutes=2),
            "allocated": False,
        },
        {
            "session_id": "aaa-004",
            "name": "Emily Clarke",
            "age": 8,
            "gender": "Female",
            "chief_complaint": "Difficulty breathing, known asthma",
            "esi_score": 2,
            "red_flags": [],
            "ai_summary": "8-year-old with acute asthma exacerbation. "
                          "Using accessory muscles. Salbutamol given pre-arrival.",
            "pain_score": 5,
            "is_worsening": True,
            "symptoms": ["Wheeze", "Shortness of breath", "Chest tightness"],
            "conditions": ["Asthma"],
            "medications": ["Salbutamol", "Montelukast"],
            "allergies": [],
            "submitted_at": now - timedelta(minutes=18),
            "allocated": False,
        },
        {
            "session_id": "aaa-005",
            "name": "Patricia Nwosu",
            "age": 45,
            "gender": "Female",
            "chief_complaint": "Sprained ankle after fall",
            "esi_score": 4,
            "red_flags": [],
            "ai_summary": "45-year-old with right ankle sprain following a trip. "
                          "Weight-bearing limited. X-ray likely needed.",
            "pain_score": 5,
            "is_worsening": False,
            "symptoms": ["Ankle pain", "Swelling", "Bruising"],
            "conditions": [],
            "medications": [],
            "allergies": ["Ibuprofen"],
            "submitted_at": now - timedelta(minutes=30),
            "allocated": False,
        },
    ]
    # Sort by ESI score ascending (1 = most critical first)
    st.session_state.patients.sort(key=lambda x: x["esi_score"])

# ── Header ────────────────────────────────────────────────────────────
total     = len(st.session_state.patients)
critical  = sum(1 for p in st.session_state.patients if p["esi_score"] <= 2)

st.markdown(f"""
<div class="header-bar">
    <div>
        <p class="header-title">🏥 TrivaMed — ED Triage Dashboard</p>
        <p class="header-sub">Emergency Department — Nurse Command Interface</p>
    </div>
    <div style="display:flex; gap:10px;">
        <span class="esi-badge badge-1" style="padding:5px 14px; font-size:0.85rem;">
            ⚠ {critical} Critical
        </span>
        <span style="background:#0F7B8C; color:white; padding:5px 14px;
                     border-radius:20px; font-size:0.85rem; font-weight:600;">
            {total} Waiting
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">⚕️ Allotment Panel</p>', unsafe_allow_html=True)
    st.markdown("**Bed Availability**")

    for dept, data in st.session_state.allotment.items():
        avail = data["available"]
        total_beds = data["total"]
        pct = avail / total_beds
        bed_class = "beds-ok" if pct > 0.5 else "beds-warn" if pct > 0.2 else "beds-full"
        st.markdown(f"""
        <div class="dept-card">
            <div class="dept-name">{dept}</div>
            <div class="dept-beds">
                Beds: <span class="{bed_class}">{avail} available</span> / {total_beds} total
                &nbsp;|&nbsp; 👨‍⚕️ {data['doctors']}  &nbsp;|&nbsp; 👩‍⚕️ {data['nurses']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Update Availability**")
    dept_choice = st.selectbox("Department", list(st.session_state.allotment.keys()))
    new_avail   = st.number_input("Available beds", min_value=0,
                                   max_value=st.session_state.allotment[dept_choice]["total"],
                                   value=st.session_state.allotment[dept_choice]["available"])
    new_doctors = st.number_input("Doctors on shift", min_value=0, max_value=20,
                                   value=st.session_state.allotment[dept_choice]["doctors"])
    new_nurses  = st.number_input("Nurses on shift", min_value=0, max_value=40,
                                   value=st.session_state.allotment[dept_choice]["nurses"])
    if st.button("Update", use_container_width=True):
        st.session_state.allotment[dept_choice]["available"] = new_avail
        st.session_state.allotment[dept_choice]["doctors"]   = new_doctors
        st.session_state.allotment[dept_choice]["nurses"]    = new_nurses
        st.success(f"{dept_choice} updated.")

    st.divider()
    st.markdown("**Estimated Wait Times (mins)**")
    for level in st.session_state.wait_times:
        st.session_state.wait_times[level] = st.number_input(
            level, min_value=0, max_value=300,
            value=st.session_state.wait_times[level]
        )

# ── Main — Patient Queue ──────────────────────────────────────────────
st.markdown('<p class="section-title">🚨 Patient Queue</p>', unsafe_allow_html=True)

for patient in st.session_state.patients:
    esi   = patient["esi_score"]
    flags = red_flag_badges(patient["red_flags"])
    ago   = time_ago(patient["submitted_at"])

    with st.container():
        st.markdown(dedent(f"""
        <div class="patient-card esi-{esi}">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <span class="patient-name">{patient['name']}</span>
                    <span class="patient-meta">&nbsp;·&nbsp;{patient['age']}y
                          &nbsp;·&nbsp;{patient['gender']}</span>
                </div>
                <span class="time-ago">{ago}</span>
            </div>
            <div style="margin-top:5px;">{esi_badge(esi)} {flags}</div>
            <div class="patient-complaint">
                <b>Complaint:</b> {patient['chief_complaint']}
            </div>
            <div class="ai-summary">
                🤖 {patient['ai_summary']}
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        with st.expander(f"Full details — {patient['name']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Demographics**")
                st.write(f"Name: {patient['name']}")
                st.write(f"Age: {patient['age']}  |  Gender: {patient['gender']}")
                st.markdown("**Symptoms**")
                for s in patient["symptoms"]:
                    st.write(f"• {s}")
                st.write(f"Pain score: {patient['pain_score']}/10")
                st.write(f"Worsening: {'Yes' if patient['is_worsening'] else 'No'}")
            with c2:
                st.markdown("**Medical History**")
                st.write(f"Conditions: {', '.join(patient['conditions']) or 'None'}")
                st.write(f"Medications: {', '.join(patient['medications']) or 'None'}")
                st.write(f"Allergies: {', '.join(patient['allergies']) or 'None'}")
                st.markdown("**AI Summary**")
                st.info(patient["ai_summary"])