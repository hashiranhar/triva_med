import streamlit as st
from datetime import datetime, timedelta
from textwrap import dedent
import anthropic
import json
import os
import time
import uuid
import random
from dotenv import load_dotenv

load_dotenv()

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
    .redflag {
        background-color: #9B2335; color: white; border-radius: 10px;
        padding: 1px 8px; font-size: 0.72rem; font-weight: 700; margin-right: 4px;
    }
    .ai-summary {
        font-size: 0.8rem; color: #4A5568; margin-top: 6px;
        font-style: italic; border-left: 3px solid #0F7B8C; padding-left: 8px;
    }
    .time-ago { font-size: 0.75rem; color: #718096; }
    .allocation-badge {
        display: inline-block;
        background-color: #1A2E4A;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 5px;
        margin-right: 5px;
    }
    .escalation-badge {
        display: inline-block;
        background-color: #9B2335;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 5px;
    }
    .new-badge {
        display: inline-block;
        background-color: #0F7B8C;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-left: 6px;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0%   { opacity: 1; }
        50%  { opacity: 0.5; }
        100% { opacity: 1; }
    }
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

# ── Mock patient pool (simulates incoming WebSocket events) ───────────
MOCK_INCOMING = [
    {
        "name": "David Okafor", "age": 45, "gender": "Male",
        "chief_complaint": "Sudden vision loss in left eye",
        "esi_score": 2, "red_flags": ["stroke"],
        "ai_summary": "45-year-old male with sudden unilateral vision loss. Stroke protocol required.",
        "pain_score": 2, "is_worsening": True,
        "symptoms": ["Vision loss", "Headache"],
        "conditions": ["Hypertension"], "medications": ["Amlodipine"], "allergies": [],
    },
    {
        "name": "Fatima Hassan", "age": 28, "gender": "Female",
        "chief_complaint": "Severe allergic reaction, throat swelling",
        "esi_score": 1, "red_flags": [],
        "ai_summary": "28-year-old with anaphylaxis. Throat swelling and urticaria after eating shellfish.",
        "pain_score": 6, "is_worsening": True,
        "symptoms": ["Throat swelling", "Urticaria", "Difficulty breathing"],
        "conditions": [], "medications": [], "allergies": ["Shellfish"],
    },
    {
        "name": "George Patel", "age": 61, "gender": "Male",
        "chief_complaint": "Nausea, sweating, jaw pain",
        "esi_score": 2, "red_flags": ["MI"],
        "ai_summary": "61-year-old with atypical MI presentation. Diaphoresis and jaw pain. High risk.",
        "pain_score": 5, "is_worsening": True,
        "symptoms": ["Nausea", "Sweating", "Jaw pain"],
        "conditions": ["Diabetes", "High cholesterol"],
        "medications": ["Metformin", "Atorvastatin"], "allergies": [],
    },
    {
        "name": "Lily Nguyen", "age": 6, "gender": "Female",
        "chief_complaint": "High fever and rash",
        "esi_score": 3, "red_flags": [],
        "ai_summary": "6-year-old with 39.5C fever and maculopapular rash. Sepsis screening advisable.",
        "pain_score": 4, "is_worsening": False,
        "symptoms": ["Fever", "Rash", "Irritability"],
        "conditions": [], "medications": [], "allergies": ["Amoxicillin"],
    },
    {
        "name": "Robert Kamau", "age": 38, "gender": "Male",
        "chief_complaint": "Laceration to forearm from glass",
        "esi_score": 4, "red_flags": [],
        "ai_summary": "38-year-old with 4cm forearm laceration. Bleeding controlled. Sutures likely needed.",
        "pain_score": 4, "is_worsening": False,
        "symptoms": ["Laceration", "Bleeding"],
        "conditions": [], "medications": [], "allergies": [],
    },
    {
        "name": "Amara Diallo", "age": 52, "gender": "Female",
        "chief_complaint": "Slurred speech and facial drooping",
        "esi_score": 1, "red_flags": ["stroke"],
        "ai_summary": "52-year-old with acute facial droop and dysarthria. FAST positive. Immediate review.",
        "pain_score": 0, "is_worsening": True,
        "symptoms": ["Facial drooping", "Slurred speech", "Arm weakness"],
        "conditions": ["Atrial fibrillation"], "medications": ["Warfarin"], "allergies": [],
    },
]

def get_next_mock_patient():
    """Returns a new mock patient not already in the queue."""
    existing_names = {p["name"] for p in st.session_state.patients}
    pool = [p for p in MOCK_INCOMING if p["name"] not in existing_names]
    if not pool:
        return None
    template = random.choice(pool)
    return {
        **template,
        "session_id": str(uuid.uuid4()),
        "submitted_at": datetime.now(),
        "allocated": False,
        "allocation": None,
    }

# ── AI Allocation Model ───────────────────────────────────────────────
def run_allocation_model(patient, allotment, wait_times):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    allotment_text = "\n".join([
        f"  {dept}: {data['available']} beds available / {data['total']} total, "
        f"{data['doctors']} doctors, {data['nurses']} nurses"
        for dept, data in allotment.items()
    ])
    wait_text = ", ".join([f"{k}={v}min" for k, v in wait_times.items()])

    prompt = f"""
You are an ED triage allocation assistant for TrivaMed.
Given a patient's triage result and the current department allotment state,
return a JSON allocation decision. Follow these rules:
- ESI 1 → Resus only
- ESI 2 with cardiac/stroke red flags → Resus if available, else Majors
- ESI 2 with no red flags, age < 16 → Paeds
- ESI 2 with no red flags, age >= 16 → Majors
- ESI 3 → Majors if available, else Minors
- ESI 4 and 5 → Minors
- If target department has 0 beds, assign to next best and explain in rationale
- escalation_required = true if ESI 1 or red flags present

Patient Triage Data:
  Name: {patient['name']}
  Age: {patient['age']}
  ESI Score: {patient['esi_score']}
  Red Flags: {patient['red_flags']}
  Chief Complaint: {patient['chief_complaint']}
  Symptoms: {', '.join(patient['symptoms'])}
  Pain Score: {patient['pain_score']}/10
  Worsening: {patient['is_worsening']}
  Conditions: {', '.join(patient['conditions']) or 'None'}
  Medications: {', '.join(patient['medications']) or 'None'}
  Allergies: {', '.join(patient['allergies']) or 'None'}
  AI Summary: {patient['ai_summary']}

Current Allotment State:
{allotment_text}

Wait Times: {wait_text}

Respond ONLY with a valid JSON object, no explanation, no markdown, no extra text.
Format:
{{
  "final_priority": <integer 1-5>,
  "assigned_department": "<Resus|Majors|Minors|Paeds>",
  "assigned_bed": "<bed identifier e.g. R1, M3, Mi5, P2>",
  "rationale": "<one or two sentence plain-English explanation for the nurse>",
  "escalation_required": <true|false>
}}
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.content[0].text.strip())

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
            "name": "John Smith", "age": 58, "gender": "Male",
            "chief_complaint": "Severe chest pain radiating to left arm",
            "esi_score": 2, "red_flags": ["MI"],
            "ai_summary": "58-year-old male with severe chest pain and left arm radiation. Onset 40 mins ago. Hypertensive. High suspicion of MI.",
            "pain_score": 8, "is_worsening": True,
            "symptoms": ["Chest pain", "Left arm pain", "Shortness of breath"],
            "conditions": ["Hypertension"], "medications": ["Lisinopril"], "allergies": ["Penicillin"],
            "submitted_at": now - timedelta(minutes=5), "allocated": False, "allocation": None,
        },
        {
            "session_id": "aaa-002",
            "name": "Sarah O'Brien", "age": 34, "gender": "Female",
            "chief_complaint": "Sudden severe headache, worst of life",
            "esi_score": 2, "red_flags": ["stroke"],
            "ai_summary": "34-year-old female with thunderclap headache. Sudden onset, 10/10 severity. Stroke protocol warranted.",
            "pain_score": 10, "is_worsening": False,
            "symptoms": ["Severe headache", "Neck stiffness", "Photophobia"],
            "conditions": [], "medications": [], "allergies": [],
            "submitted_at": now - timedelta(minutes=12), "allocated": False, "allocation": None,
        },
        {
            "session_id": "aaa-003",
            "name": "Mohammed Al-Farsi", "age": 72, "gender": "Male",
            "chief_complaint": "High fever, confusion, rapid breathing",
            "esi_score": 1, "red_flags": ["sepsis"],
            "ai_summary": "72-year-old male with fever 39.8C, acute confusion and tachypnoea. Sepsis screening required immediately.",
            "pain_score": 4, "is_worsening": True,
            "symptoms": ["Fever", "Confusion", "Rapid breathing", "Chills"],
            "conditions": ["Diabetes", "COPD"], "medications": ["Metformin", "Salbutamol inhaler"], "allergies": ["Sulfa drugs"],
            "submitted_at": now - timedelta(minutes=2), "allocated": False, "allocation": None,
        },
        {
            "session_id": "aaa-004",
            "name": "Emily Clarke", "age": 8, "gender": "Female",
            "chief_complaint": "Difficulty breathing, known asthma",
            "esi_score": 2, "red_flags": [],
            "ai_summary": "8-year-old with acute asthma exacerbation. Using accessory muscles. Salbutamol given pre-arrival.",
            "pain_score": 5, "is_worsening": True,
            "symptoms": ["Wheeze", "Shortness of breath", "Chest tightness"],
            "conditions": ["Asthma"], "medications": ["Salbutamol", "Montelukast"], "allergies": [],
            "submitted_at": now - timedelta(minutes=18), "allocated": False, "allocation": None,
        },
        {
            "session_id": "aaa-005",
            "name": "Patricia Nwosu", "age": 45, "gender": "Female",
            "chief_complaint": "Sprained ankle after fall",
            "esi_score": 4, "red_flags": [],
            "ai_summary": "45-year-old with right ankle sprain following a trip. Weight-bearing limited. X-ray likely needed.",
            "pain_score": 5, "is_worsening": False,
            "symptoms": ["Ankle pain", "Swelling", "Bruising"],
            "conditions": [], "medications": [], "allergies": ["Ibuprofen"],
            "submitted_at": now - timedelta(minutes=30), "allocated": False, "allocation": None,
        },
    ]
    st.session_state.patients.sort(key=lambda x: x["esi_score"])

if "last_arrival" not in st.session_state:
    st.session_state.last_arrival = datetime.now()

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

# ── Simulate new patient arriving every 30 seconds ────────────────────
if st.session_state.auto_refresh:
    seconds_since = (datetime.now() - st.session_state.last_arrival).total_seconds()
    if seconds_since >= 30:
        new_patient = get_next_mock_patient()
        if new_patient:
            st.session_state.patients.append(new_patient)
            st.session_state.patients.sort(
                key=lambda x: x["allocation"]["final_priority"]
                if x["allocation"] else x["esi_score"]
            )
            st.session_state.last_arrival = datetime.now()

# ── Header ────────────────────────────────────────────────────────────
total    = len(st.session_state.patients)
critical = sum(1 for p in st.session_state.patients if p["esi_score"] <= 2)

st.markdown(f"""
<div class="header-bar">
    <div>
        <p class="header-title">🏥 TrivaMed — ED Triage Dashboard</p>
        <p class="header-sub">Emergency Department — Nurse Command Interface</p>
    </div>
    <div style="display:flex; gap:10px; align-items:center;">
        <span class="esi-badge badge-1" style="padding:5px 14px; font-size:0.85rem;">
            ⚠ {critical} Critical
        </span>
        <span style="background:#0F7B8C; color:white; padding:5px 14px;
                     border-radius:20px; font-size:0.85rem; font-weight:600;">
            {total} Waiting
        </span>
        <span style="color:#9ECDD4; font-size:0.8rem;">
            {'🟢 Live' if st.session_state.auto_refresh else '⏸ Paused'}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">⚕️ Allotment Panel</p>', unsafe_allow_html=True)
    st.markdown("**Bed Availability**")

    for dept, data in st.session_state.allotment.items():
        avail      = data["available"]
        total_beds = data["total"]
        pct        = avail / total_beds
        bed_class  = "beds-ok" if pct > 0.5 else "beds-warn" if pct > 0.2 else "beds-full"
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

    st.divider()
    st.markdown("**AI Allocation**")
    st.caption("Run the AI model to assign departments and beds to all unallocated patients.")

    if st.button("🤖 Run Allocation", use_container_width=True, type="primary"):
        unallocated = [p for p in st.session_state.patients if not p["allocated"]]
        if not unallocated:
            st.info("All patients are already allocated.")
        else:
            with st.spinner(f"Allocating {len(unallocated)} patient(s)..."):
                for patient in unallocated:
                    try:
                        result = run_allocation_model(
                            patient,
                            st.session_state.allotment,
                            st.session_state.wait_times
                        )
                        patient["allocation"] = result
                        patient["allocated"]  = True
                        dept = result["assigned_department"]
                        if dept in st.session_state.allotment:
                            current = st.session_state.allotment[dept]["available"]
                            st.session_state.allotment[dept]["available"] = max(0, current - 1)
                    except Exception as e:
                        patient["allocation"] = {
                            "final_priority": patient["esi_score"],
                            "assigned_department": "Unassigned",
                            "assigned_bed": "—",
                            "rationale": f"Allocation failed: {str(e)}",
                            "escalation_required": False,
                        }
                        patient["allocated"] = True

            st.session_state.patients.sort(
                key=lambda x: x["allocation"]["final_priority"]
                if x["allocation"] else x["esi_score"]
            )
            st.success("Allocation complete.")
            st.rerun()

    st.divider()
    st.markdown("**Live Updates**")
    st.caption("When enabled, a new mock patient arrives every 30 seconds.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Start", use_container_width=True,
                     disabled=st.session_state.auto_refresh):
            st.session_state.auto_refresh = True
            st.session_state.last_arrival = datetime.now()
            st.rerun()
    with col2:
        if st.button("⏸ Pause", use_container_width=True,
                     disabled=not st.session_state.auto_refresh):
            st.session_state.auto_refresh = False
            st.rerun()

# ── Main — Patient Queue ──────────────────────────────────────────────
st.markdown('<p class="section-title">🚨 Patient Queue</p>', unsafe_allow_html=True)

# Filter out seen patients
active_patients = [p for p in st.session_state.patients if not p.get("seen", False)]
seen_patients   = [p for p in st.session_state.patients if p.get("seen", False)]

if not active_patients:
    st.info("No patients currently in the queue.")

for patient in active_patients:
    esi   = patient["esi_score"]
    flags = red_flag_badges(patient["red_flags"])
    ago   = time_ago(patient["submitted_at"])
    alloc = patient.get("allocation")

    is_new = (datetime.now() - patient["submitted_at"]).total_seconds() < 60
    new_tag = '<span class="new-badge">NEW</span>' if is_new else ""

    if alloc:
        dept_text  = f'<span class="allocation-badge">🏥 {alloc["assigned_department"]} — Bed {alloc["assigned_bed"]}</span>'
        esc_text   = '<span class="escalation-badge">🚨 ESCALATION</span>' if alloc["escalation_required"] else ""
        alloc_html = f'<div style="margin-top:6px;">{dept_text}{esc_text}</div>'
    else:
        alloc_html = '<div style="margin-top:6px; font-size:0.78rem; color:#718096;">⏳ Awaiting allocation</div>'

    st.markdown(
        f'<div class="patient-card esi-{esi}">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start;">'
        f'<div><span class="patient-name">{patient["name"]}</span>{new_tag}'
        f'<span class="patient-meta">&nbsp;·&nbsp;{patient["age"]}y&nbsp;·&nbsp;{patient["gender"]}</span></div>'
        f'<span class="time-ago">{ago}</span></div>'
        f'<div style="margin-top:5px;">{esi_badge(esi)} {flags}</div>'
        f'<div class="patient-complaint"><b>Complaint:</b> {patient["chief_complaint"]}</div>'
        f'<div class="ai-summary">🤖 {patient["ai_summary"]}</div>'
        f'{alloc_html}</div>',
        unsafe_allow_html=True
    )

    with st.expander(f"Full details — {patient['name']}"):
        c1, c2, c3 = st.columns([2, 2, 1])

        with c1:
            st.markdown("**Demographics**")
            st.write(f"Name: {patient['name']}")
            st.write(f"Age: {patient['age']}  |  Gender: {patient['gender']}")
            st.divider()
            st.markdown("**Symptoms**")
            for s in patient["symptoms"]:
                st.write(f"• {s}")
            st.write(f"Pain score: {patient['pain_score']}/10")
            st.write(f"Worsening: {'Yes ⚠' if patient['is_worsening'] else 'No'}")

        with c2:
            st.markdown("**Medical History**")
            st.write(f"Conditions: {', '.join(patient['conditions']) or 'None'}")
            st.write(f"Medications: {', '.join(patient['medications']) or 'None'}")
            st.write(f"Allergies: {', '.join(patient['allergies']) or 'None'}")
            st.divider()
            st.markdown("**AI Clinical Summary**")
            st.info(patient["ai_summary"])
            if alloc:
                st.markdown("**Allocation Rationale**")
                st.success(
                    f"**{alloc['assigned_department']} — Bed {alloc['assigned_bed']}**\n\n"
                    f"{alloc['rationale']}"
                )

        with c3:
            st.markdown("**Actions**")
            st.write(f"Arrived: {patient['submitted_at'].strftime('%H:%M')}")
            if alloc:
                st.metric("Priority", f"ESI {alloc['final_priority']}")
            else:
                st.metric("Priority", f"ESI {esi}")

            st.write("")
            if st.button(f"✅ Mark as Seen", key=f"seen_{patient['session_id']}",
                         use_container_width=True, type="primary"):
                patient["seen"] = True
                # Free up the bed when patient is seen
                if alloc and alloc["assigned_department"] in st.session_state.allotment:
                    dept = alloc["assigned_department"]
                    total_beds = st.session_state.allotment[dept]["total"]
                    current    = st.session_state.allotment[dept]["available"]
                    st.session_state.allotment[dept]["available"] = min(total_beds, current + 1)
                st.rerun()

# ── Seen patients (collapsed) ─────────────────────────────────────────
if seen_patients:
    st.divider()
    with st.expander(f"✅ Seen patients ({len(seen_patients)})"):
        for patient in seen_patients:
            alloc = patient.get("allocation")
            dept  = alloc["assigned_department"] if alloc else "Unassigned"
            bed   = alloc["assigned_bed"] if alloc else "—"
            st.write(
                f"**{patient['name']}** · {patient['age']}y · {patient['gender']} "
                f"· ESI {patient['esi_score']} · {dept} Bed {bed} "
                f"· {patient['submitted_at'].strftime('%H:%M')}"
            )

# ── Auto-refresh loop ─────────────────────────────────────────────────
if st.session_state.auto_refresh:
    time.sleep(5)
    st.rerun()