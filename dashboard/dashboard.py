import streamlit as st
from datetime import datetime, timedelta
import anthropic
import json
import os
import time
import uuid
import random
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
    .dept-staff { font-size: 0.78rem; color: #4A5568; margin-top: 2px; }
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

DEPT_CAPABILITIES = {
    "Resus": (
        "Full resuscitation bay. Handles immediately life-threatening conditions — "
        "cardiac arrest, major trauma, severe sepsis, anaphylaxis, stroke with active deterioration. "
        "Requires Registrar or Consultant present. Highest staff-to-patient ratio. "
        "Typically 4 beds. Each patient requires near-constant clinical attention."
    ),
    "Majors": (
        "Main ED treatment area for serious but not immediately life-threatening cases. "
        "Handles ESI 2-3 patients — chest pain, significant infections, fractures, "
        "acute neurological symptoms, moderate respiratory distress. "
        "Requires at least SHO cover; Registrar preferable for ESI 2. "
        "Can manage higher patient volumes than Resus."
    ),
    "Minors": (
        "Fast-track area for low-acuity presentations. "
        "ESI 4-5 patients — minor lacerations, sprains, mild infections, simple complaints. "
        "SHO or ACCP can manage independently. High throughput expected. "
        "Not appropriate for any patient who may deteriorate."
    ),
    "Paeds": (
        "Dedicated paediatric stream for patients under 16. "
        "Age-appropriate equipment, drug dosing, and environment. "
        "Requires at least one Paeds-trained nurse and preferably a Paeds-trained doctor. "
        "If no Paeds-trained staff are available, children should be routed to Majors with a flag. "
        "Handles full ESI range 1-5 for children."
    ),
}

NHS_GRADES = {
    "consultant": "Most senior. Overall clinical responsibility. Can manage any ESI level.",
    "registrar":  "Senior trainee (ST4+). Can lead Resus and Majors independently.",
    "sho":        "Middle grade (CT1-3/ST1-3). Can manage Majors and Minors. Needs Registrar backup for ESI 1.",
    "fy2":        "Foundation Year 2. Can manage Minors. Needs senior supervision for Majors.",
    "fy1":        "Foundation Year 1. Limited ED scope. Minors only with direct supervision.",
    "accp":       "Advanced Clinical Practitioner. Senior non-doctor. Can manage Majors and Minors independently.",
}

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

def get_queue_depth():
    """Returns count of active (non-seen) allocated patients per department."""
    depth = {"Resus": 0, "Majors": 0, "Minors": 0, "Paeds": 0}
    for p in st.session_state.patients:
        if not p.get("seen") and p.get("allocation"):
            dept = p["allocation"].get("assigned_department")
            if dept in depth:
                depth[dept] += 1
    return depth

# ── Mock patient pool ─────────────────────────────────────────────────
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

# ── Backend integration ───────────────────────────────────────────────

def infer_esi(pain_score: int, is_worsening: bool, chief_complaint: str, symptom_names: list) -> int:
    text = (chief_complaint + " " + " ".join(symptom_names)).lower()
    if any(k in text for k in ["cardiac arrest", "not breathing", "anaphylaxis", "throat swelling"]):
        return 1
    if pain_score >= 9 and is_worsening:
        return 1
    high_risk = ["chest pain", "vision loss", "facial droop", "slurred speech", "arm weakness",
                 "jaw pain", "thunderclap", "sepsis", "confusion", "rapid breathing",
                 "difficulty breathing", "stroke", "heart attack"]
    if any(k in text for k in high_risk) or (pain_score >= 7 and is_worsening):
        return 2
    if pain_score >= 4 or is_worsening:
        return 3
    if pain_score >= 2:
        return 4
    return 5


def infer_red_flags(chief_complaint: str, symptom_names: list) -> list:
    text = (chief_complaint + " " + " ".join(symptom_names)).lower()
    flags = []
    if any(k in text for k in ["stroke", "vision loss", "facial droop", "slurred speech",
                                "arm weakness", "thunderclap"]):
        flags.append("stroke")
    if any(k in text for k in ["chest pain", "jaw pain", "heart attack", "myocardial"]):
        flags.append("MI")
    if any(k in text for k in ["sepsis", "high fever", "confusion", "rapid breathing"]):
        flags.append("sepsis")
    return flags


def generate_summary(name: str, age: int, gender: str, complaint: str,
                     pain_score: int, is_worsening: bool) -> str:
    note = " Symptoms worsening." if is_worsening else ""
    return (f"{age}-year-old {gender.lower()} presenting with {complaint.lower()}. "
            f"Pain {pain_score}/10.{note}")


def transform_backend_patient(bp: dict) -> dict:
    """Convert a backend queue record into the dashboard patient format."""
    symptom_names = [
        s["name"] if isinstance(s, dict) else s
        for s in bp.get("symptoms", [])
    ]
    esi   = infer_esi(bp["pain_score"], bp["is_worsening"], bp["chief_complaint"], symptom_names)
    flags = infer_red_flags(bp["chief_complaint"], symptom_names)
    summary = generate_summary(bp["patient_name"], bp["age"], bp["gender"],
                               bp["chief_complaint"], bp["pain_score"], bp["is_worsening"])
    return {
        "session_id":     bp["session_id"],
        "name":           bp["patient_name"],
        "age":            bp["age"],
        "gender":         bp["gender"].capitalize(),
        "chief_complaint": bp["chief_complaint"],
        "esi_score":      esi,
        "red_flags":      flags,
        "ai_summary":     summary,
        "pain_score":     bp["pain_score"],
        "is_worsening":   bp["is_worsening"],
        "symptoms":       symptom_names,
        "conditions":     bp.get("existing_conditions", []),
        "medications":    bp.get("current_medications", []),
        "allergies":      bp.get("allergies", []),
        "submitted_at":   datetime.fromisoformat(bp["submitted_at"]),
        "allocated":      False,
        "allocation":     None,
    }


def fetch_queue_from_backend() -> list:
    resp = requests.get(f"{BACKEND_URL}/api/v1/queue", timeout=5)
    resp.raise_for_status()
    return resp.json()


def mark_seen_on_backend(session_id: str):
    requests.patch(f"{BACKEND_URL}/api/v1/submission/{session_id}/seen", timeout=5)


def mock_patient_to_submission(mock: dict) -> dict:
    """Convert a MOCK_INCOMING entry to the backend PatientSubmission payload."""
    parts = mock["name"].split(" ", 1)
    first, last = parts[0], parts[1] if len(parts) > 1 else "Unknown"
    birth_year = datetime.now().year - mock["age"]
    gender = {"Male": "male", "Female": "female"}.get(mock.get("gender", ""), "other")
    now = datetime.now()
    symptoms_payload = [
        {"name": s, "severity": mock["pain_score"],
         "location": None, "duration_minutes": random.randint(10, 60)}
        for s in mock["symptoms"]
    ]
    # Reserve a session first
    sess_resp = requests.post(f"{BACKEND_URL}/api/v1/session/start", timeout=5)
    sess_resp.raise_for_status()
    session_id = sess_resp.json()["session_id"]

    return {
        "session_id": session_id,
        "submitted_at": now.isoformat(),
        "demographics": {
            "first_name": first, "last_name": last,
            "date_of_birth": f"{birth_year}-06-15",
            "gender": gender,
        },
        "chief_complaint": {
            "description": mock["chief_complaint"],
            "onset_time": (now - timedelta(minutes=random.randint(5, 60))).isoformat(),
            "is_trauma": False,
        },
        "symptoms": {
            "symptoms": symptoms_payload,
            "pain_score": mock["pain_score"],
            "is_worsening": mock["is_worsening"],
        },
        "medical_history": {
            "existing_conditions": mock.get("conditions", []),
            "current_medications": mock.get("medications", []),
            "allergies":           mock.get("allergies", []),
            "recent_surgeries":    None,
        },
    }


def submit_mock_to_backend(mock: dict) -> bool:
    """Submit a mock patient entry to the backend. Returns True on success."""
    payload = mock_patient_to_submission(mock)
    resp = requests.post(f"{BACKEND_URL}/api/v1/submission", json=payload, timeout=5)
    resp.raise_for_status()
    return True


def sync_patients_from_backend():
    """Pull the live queue from backend and merge with local allocation data."""
    backend_records = fetch_queue_from_backend()
    allocations = st.session_state.get("allocations", {})
    patients = []
    for bp in backend_records:
        p = transform_backend_patient(bp)
        sid = p["session_id"]
        if sid in allocations:
            p["allocation"] = allocations[sid]
            p["allocated"]  = True
        patients.append(p)
    patients.sort(key=lambda x: x["allocation"]["final_priority"]
                  if x["allocation"] else x["esi_score"])
    st.session_state.patients = patients

# ── AI Allocation Model ───────────────────────────────────────────────
def build_allotment_context(allotment, wait_times, queue_depth, paeds_trained):
    """Builds rich dynamic context string for the prompt."""
    lines = []
    for dept, data in allotment.items():
        staff = data["staff"]
        staff_lines = []
        for grade, count in staff.items():
            if count > 0:
                staff_lines.append(f"{count} {grade.upper()}")
        staff_str = ", ".join(staff_lines) if staff_lines else "No doctors on shift"

        paeds_note = ""
        if dept == "Paeds":
            paeds_note = f" | Paeds-trained staff on shift: {'YES' if paeds_trained else 'NO — route children to Majors with flag'}"

        lines.append(
            f"  {dept}:\n"
            f"    Beds: {data['available']} available / {data['total']} total\n"
            f"    Doctors: {staff_str}\n"
            f"    Nurses: {data['nurses']}\n"
            f"    Current queue depth: {queue_depth.get(dept, 0)} active patients{paeds_note}"
        )

    wait_lines = "\n".join([f"    {k}: {v} mins" for k, v in wait_times.items()])
    return "\n".join(lines) + f"\n\n  Current estimated wait times:\n{wait_lines}"

def build_department_knowledge():
    """Builds stable medical knowledge section for the prompt."""
    dept_lines = []
    for dept, desc in DEPT_CAPABILITIES.items():
        dept_lines.append(f"  {dept}: {desc}")

    grade_lines = []
    for grade, desc in NHS_GRADES.items():
        grade_lines.append(f"  {grade.upper()}: {desc}")

    return "\n".join(dept_lines), "\n".join(grade_lines)

def run_allocation_model(patient, allotment, wait_times, paeds_trained):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    queue_depth   = get_queue_depth()
    dept_knowledge, grade_knowledge = build_department_knowledge()
    allotment_context = build_allotment_context(
        allotment, wait_times, queue_depth, paeds_trained
    )

    prompt = f"""You are a senior NHS ED triage allocation assistant for TrivaMed.
Your role is to assign each patient to the most appropriate department and bed,
based on clinical need, current department capacity, and staff capability.
You must reason carefully — your decision directly affects patient safety.

━━━ DEPARTMENT CAPABILITIES (stable medical knowledge) ━━━
{dept_knowledge}

━━━ NHS DOCTOR GRADES (stable medical knowledge) ━━━
{grade_knowledge}

━━━ CURRENT DEPARTMENT STATE (this shift) ━━━
{allotment_context}

━━━ PATIENT TRIAGE DATA ━━━
  Name:             {patient['name']}
  Age:              {patient['age']}
  Gender:           {patient['gender']}
  ESI Score:        {patient['esi_score']} — {ESI_LABELS[patient['esi_score']]}
  Red Flags:        {', '.join(patient['red_flags']) if patient['red_flags'] else 'None'}
  Chief Complaint:  {patient['chief_complaint']}
  Symptoms:         {', '.join(patient['symptoms'])}
  Pain Score:       {patient['pain_score']}/10
  Worsening:        {'Yes' if patient['is_worsening'] else 'No'}
  Conditions:       {', '.join(patient['conditions']) or 'None'}
  Medications:      {', '.join(patient['medications']) or 'None'}
  Allergies:        {', '.join(patient['allergies']) or 'None'}
  Clinical Summary: {patient['ai_summary']}

━━━ YOUR TASK ━━━
Reason through the following before deciding:
1. What does this patient clinically need — what level of care and what grade of doctor?
2. Which department is most appropriate given their presentation?
3. Is that department able to safely receive this patient right now, given bed availability,
   current queue depth, and the grades of staff currently on shift?
4. If the ideal department cannot safely receive this patient, what is the next best option
   and why?
5. Does this patient require escalation to a senior clinician immediately?

Return ONLY a valid JSON object. No explanation, no markdown, no extra text.
{{
  "final_priority":       <integer 1-5>,
  "assigned_department":  "<Resus|Majors|Minors|Paeds>",
  "assigned_bed":         "<bed identifier e.g. R1, M3, Mi5, P2>",
  "rationale":            "<2-3 sentences explaining the clinical reasoning for the nurse>",
  "escalation_required":  <true|false>,
  "required_grade":       "<minimum NHS doctor grade needed for this patient>"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.content[0].text.strip())

# ── Session state ─────────────────────────────────────────────────────
if "allotment" not in st.session_state:
    st.session_state.allotment = {
        "Resus": {
            "total": 4, "available": 2, "nurses": 4,
            "staff": {"consultant": 1, "registrar": 1, "sho": 1, "fy2": 0, "fy1": 0, "accp": 0},
        },
        "Majors": {
            "total": 12, "available": 5, "nurses": 6,
            "staff": {"consultant": 0, "registrar": 1, "sho": 2, "fy2": 1, "fy1": 0, "accp": 1},
        },
        "Minors": {
            "total": 10, "available": 8, "nurses": 3,
            "staff": {"consultant": 0, "registrar": 0, "sho": 1, "fy2": 1, "fy1": 1, "accp": 1},
        },
        "Paeds": {
            "total": 6, "available": 3, "nurses": 2,
            "staff": {"consultant": 0, "registrar": 1, "sho": 1, "fy2": 0, "fy1": 0, "accp": 0},
        },
    }
    st.session_state.wait_times = {
        "ESI 1": 0, "ESI 2": 8, "ESI 3": 35, "ESI 4": 65, "ESI 5": 110
    }
    st.session_state.paeds_trained = True

INITIAL_SEED_PATIENTS = [
    {
        "name": "John Smith", "age": 58, "gender": "Male",
        "chief_complaint": "Severe chest pain radiating to left arm",
        "pain_score": 8, "is_worsening": True,
        "symptoms": ["Chest pain", "Left arm pain", "Shortness of breath"],
        "conditions": ["Hypertension"], "medications": ["Lisinopril"], "allergies": ["Penicillin"],
    },
    {
        "name": "Sarah O'Brien", "age": 34, "gender": "Female",
        "chief_complaint": "Thunderclap headache, worst of life, sudden onset",
        "pain_score": 10, "is_worsening": False,
        "symptoms": ["Severe headache", "Neck stiffness", "Photophobia"],
        "conditions": [], "medications": [], "allergies": [],
    },
    {
        "name": "Mohammed Al-Farsi", "age": 72, "gender": "Male",
        "chief_complaint": "High fever, confusion, rapid breathing",
        "pain_score": 4, "is_worsening": True,
        "symptoms": ["Fever", "Confusion", "Rapid breathing", "Chills"],
        "conditions": ["Diabetes", "COPD"], "medications": ["Metformin", "Salbutamol inhaler"],
        "allergies": ["Sulfa drugs"],
    },
    {
        "name": "Emily Clarke", "age": 8, "gender": "Female",
        "chief_complaint": "Difficulty breathing, known asthma",
        "pain_score": 5, "is_worsening": True,
        "symptoms": ["Wheeze", "Shortness of breath", "Chest tightness"],
        "conditions": ["Asthma"], "medications": ["Salbutamol", "Montelukast"], "allergies": [],
    },
    {
        "name": "Patricia Nwosu", "age": 45, "gender": "Female",
        "chief_complaint": "Sprained ankle after fall",
        "pain_score": 5, "is_worsening": False,
        "symptoms": ["Ankle pain", "Swelling", "Bruising"],
        "conditions": [], "medications": [], "allergies": ["Ibuprofen"],
    },
]

if "allocations" not in st.session_state:
    st.session_state.allocations = {}

if "backend_available" not in st.session_state:
    st.session_state.backend_available = True

if "patients" not in st.session_state:
    try:
        sync_patients_from_backend()
        # If the DB is empty, seed initial patients so the dashboard isn't blank
        if not st.session_state.patients:
            for seed in INITIAL_SEED_PATIENTS:
                try:
                    submit_mock_to_backend(seed)
                except Exception:
                    pass
            sync_patients_from_backend()
        st.session_state.backend_available = True
    except Exception:
        # Backend not reachable — fall back to in-memory data so the UI still works
        st.session_state.backend_available = False
        now = datetime.now()
        st.session_state.patients = [
            {
                "session_id": f"local-{i}", "name": s["name"], "age": s["age"],
                "gender": s["gender"], "chief_complaint": s["chief_complaint"],
                "esi_score": infer_esi(s["pain_score"], s["is_worsening"],
                                       s["chief_complaint"], s["symptoms"]),
                "red_flags": infer_red_flags(s["chief_complaint"], s["symptoms"]),
                "ai_summary": generate_summary(s["name"], s["age"], s["gender"],
                                               s["chief_complaint"], s["pain_score"],
                                               s["is_worsening"]),
                "pain_score": s["pain_score"], "is_worsening": s["is_worsening"],
                "symptoms": s["symptoms"], "conditions": s["conditions"],
                "medications": s["medications"], "allergies": s["allergies"],
                "submitted_at": now - timedelta(minutes=5 * (i + 1)),
                "allocated": False, "allocation": None,
            }
            for i, s in enumerate(INITIAL_SEED_PATIENTS)
        ]
        st.session_state.patients.sort(key=lambda x: x["esi_score"])

if "last_arrival" not in st.session_state:
    st.session_state.last_arrival = datetime.now()

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

# ── Poll backend and simulate new arrivals ────────────────────────────
if st.session_state.auto_refresh:
    seconds_since = (datetime.now() - st.session_state.last_arrival).total_seconds()
    if seconds_since >= 30 and st.session_state.backend_available:
        # Pick a mock patient not already in the queue and submit to backend
        existing_names = {p["name"] for p in st.session_state.patients}
        pool = [p for p in MOCK_INCOMING if p["name"] not in existing_names]
        if pool:
            try:
                submit_mock_to_backend(random.choice(pool))
            except Exception:
                pass
        st.session_state.last_arrival = datetime.now()

    # Re-sync queue from backend on every auto-refresh cycle
    if st.session_state.backend_available:
        try:
            sync_patients_from_backend()
        except Exception:
            pass

# ── Header ────────────────────────────────────────────────────────────
total    = len([p for p in st.session_state.patients if not p.get("seen")])
critical = sum(1 for p in st.session_state.patients if p["esi_score"] <= 2 and not p.get("seen"))

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

    # ── Department overview cards ─────────────────────────────────────
    st.markdown("**Department Status**")
    queue_depth = get_queue_depth()
    for dept, data in st.session_state.allotment.items():
        avail      = data["available"]
        total_beds = data["total"]
        pct        = avail / total_beds
        bed_class  = "beds-ok" if pct > 0.5 else "beds-warn" if pct > 0.2 else "beds-full"
        staff      = data["staff"]
        senior     = staff.get("consultant", 0) + staff.get("registrar", 0)
        senior_str = f"{'✅' if senior > 0 else '⚠️'} {senior} senior"
        paeds_flag = " | 👶 Paeds-trained" if dept == "Paeds" and st.session_state.paeds_trained else ""
        st.markdown(
            f'<div class="dept-card">'
            f'<div class="dept-name">{dept}</div>'
            f'<div class="dept-beds">Beds: <span class="{bed_class}">{avail} free</span> / {total_beds} '
            f'| Queue: {queue_depth.get(dept, 0)}</div>'
            f'<div class="dept-staff">{senior_str} | 👩‍⚕️ {data["nurses"]} nurses{paeds_flag}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # ── Update department ─────────────────────────────────────────────
    st.markdown("**Update Department**")
    dept_choice = st.selectbox("Department", list(st.session_state.allotment.keys()))
    d = st.session_state.allotment[dept_choice]

    new_avail  = st.number_input("Available beds", min_value=0,
                                  max_value=d["total"], value=d["available"])
    new_nurses = st.number_input("Nurses on shift", min_value=0,
                                  max_value=40, value=d["nurses"])

    st.markdown("**Doctors on shift by grade**")
    new_staff = {}
    cols = st.columns(2)
    grades = list(NHS_GRADES.keys())
    for i, grade in enumerate(grades):
        with cols[i % 2]:
            new_staff[grade] = st.number_input(
                grade.upper(), min_value=0, max_value=10,
                value=d["staff"].get(grade, 0),
                key=f"staff_{dept_choice}_{grade}"
            )

    if dept_choice == "Paeds":
        st.session_state.paeds_trained = st.toggle(
            "Paeds-trained staff on shift",
            value=st.session_state.paeds_trained
        )

    if st.button("Update Department", use_container_width=True):
        st.session_state.allotment[dept_choice]["available"] = new_avail
        st.session_state.allotment[dept_choice]["nurses"]    = new_nurses
        st.session_state.allotment[dept_choice]["staff"]     = new_staff
        st.success(f"{dept_choice} updated.")
        st.rerun()

    st.divider()

    # ── Wait times ────────────────────────────────────────────────────
    st.markdown("**Estimated Wait Times (mins)**")
    for level in st.session_state.wait_times:
        st.session_state.wait_times[level] = st.number_input(
            level, min_value=0, max_value=300,
            value=st.session_state.wait_times[level]
        )

    st.divider()

    # ── AI Allocation ─────────────────────────────────────────────────
    st.markdown("**AI Allocation**")
    st.caption("Assigns department, bed and required doctor grade to all unallocated patients.")

    if st.button("🤖 Run Allocation", use_container_width=True, type="primary"):
        unallocated = [p for p in st.session_state.patients if not p["allocated"]]
        if not unallocated:
            st.info("All patients already allocated.")
        else:
            with st.spinner(f"Allocating {len(unallocated)} patient(s)..."):
                for patient in unallocated:
                    try:
                        result = run_allocation_model(
                            patient,
                            st.session_state.allotment,
                            st.session_state.wait_times,
                            st.session_state.paeds_trained,
                        )
                        patient["allocation"] = result
                        patient["allocated"]  = True
                        # Persist allocation so it survives backend re-syncs
                        st.session_state.allocations[patient["session_id"]] = result
                        dept = result["assigned_department"]
                        if dept in st.session_state.allotment:
                            current = st.session_state.allotment[dept]["available"]
                            st.session_state.allotment[dept]["available"] = max(0, current - 1)
                    except Exception as e:
                        fallback = {
                            "final_priority": patient["esi_score"],
                            "assigned_department": "Unassigned",
                            "assigned_bed": "—",
                            "rationale": f"Allocation failed: {str(e)}",
                            "escalation_required": False,
                            "required_grade": "Unknown",
                        }
                        patient["allocation"] = fallback
                        patient["allocated"]  = True
                        st.session_state.allocations[patient["session_id"]] = fallback

            st.session_state.patients.sort(
                key=lambda x: x["allocation"]["final_priority"]
                if x["allocation"] else x["esi_score"]
            )
            st.success("Allocation complete.")
            st.rerun()

    st.divider()

    # ── Live updates ──────────────────────────────────────────────────
    st.markdown("**Live Updates**")
    if st.session_state.get("backend_available", True):
        st.caption("Polls backend every 5 s. Submits a new patient to the DB every 30 s.")
    else:
        st.caption("⚠️ Backend offline — running on local data only.")
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

active_patients = [p for p in st.session_state.patients if not p.get("seen", False)]
seen_patients   = [p for p in st.session_state.patients if p.get("seen", False)]

if not active_patients:
    st.info("No patients currently in the queue.")

for patient in active_patients:
    esi   = patient["esi_score"]
    flags = red_flag_badges(patient["red_flags"])
    ago   = time_ago(patient["submitted_at"])
    alloc = patient.get("allocation")

    is_new  = (datetime.now() - patient["submitted_at"]).total_seconds() < 60
    new_tag = '<span class="new-badge">NEW</span>' if is_new else ""

    if alloc:
        dept_text  = f'<span class="allocation-badge">🏥 {alloc["assigned_department"]} — Bed {alloc["assigned_bed"]}</span>'
        grade_text = f'<span class="allocation-badge">👨‍⚕️ {alloc.get("required_grade", "").upper()}</span>'
        esc_text   = '<span class="escalation-badge">🚨 ESCALATION</span>' if alloc["escalation_required"] else ""
        alloc_html = f'<div style="margin-top:6px;">{dept_text}{grade_text}{esc_text}</div>'
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
                    f"**{alloc['assigned_department']} — Bed {alloc['assigned_bed']}**  \n"
                    f"Required grade: **{alloc.get('required_grade', '—').upper()}**  \n\n"
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
            if st.button("✅ Mark as Seen", key=f"seen_{patient['session_id']}",
                         use_container_width=True, type="primary"):
                # Tell backend this patient is done (removes from queue)
                if st.session_state.backend_available:
                    try:
                        mark_seen_on_backend(patient["session_id"])
                    except Exception:
                        pass
                # Remove from local state and clean up allocation record
                st.session_state.patients = [
                    p for p in st.session_state.patients
                    if p["session_id"] != patient["session_id"]
                ]
                st.session_state.allocations.pop(patient["session_id"], None)
                # Free the bed
                if alloc and alloc["assigned_department"] in st.session_state.allotment:
                    dept       = alloc["assigned_department"]
                    total_beds = st.session_state.allotment[dept]["total"]
                    current    = st.session_state.allotment[dept]["available"]
                    st.session_state.allotment[dept]["available"] = min(total_beds, current + 1)
                st.rerun()

# ── Seen patients ─────────────────────────────────────────────────────
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