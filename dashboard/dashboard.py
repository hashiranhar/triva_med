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
    page_title="RefugeesMH — Clinician Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .block-container { padding-top: 1rem; }

    .header-bar {
        background: linear-gradient(135deg, #1B3A4B 0%, #0D2233 100%);
        padding: 1.2rem 1.8rem;
        border-radius: 10px;
        margin-bottom: 1.4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 4px solid #3EC9A7;
    }
    .header-title { color: white; font-size: 1.35rem; font-weight: 700; margin: 0; letter-spacing: -0.3px; }
    .header-sub   { color: #7EC8C0; font-size: 0.82rem; margin: 0; font-weight: 300; }

    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #7A8FA6;
        margin-bottom: 0.7rem;
        margin-top: 0.3rem;
    }

    /* Patient cards */
    .patient-card {
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 5px solid #ccc;
        background: #FAFBFC;
        border: 1px solid #E4EAF0;
        border-left-width: 5px;
        transition: box-shadow 0.15s;
    }
    .patient-card:hover { box-shadow: 0 3px 12px rgba(0,0,0,0.08); }
    .card-crisis    { border-left-color: #C0392B; background: #FFF8F7; }
    .card-high      { border-left-color: #E67E22; background: #FFFAF5; }
    .card-moderate  { border-left-color: #F1C40F; background: #FDFDF5; }
    .card-low       { border-left-color: #27AE60; background: #F6FDF9; }

    .patient-name { font-weight: 700; color: #1B3A4B; font-size: 0.98rem; }
    .patient-meta { font-size: 0.78rem; color: #6B7C93; margin-top: 2px; }
    .complaint-text {
        font-size: 0.85rem; color: #2C3E50; margin-top: 6px;
        font-style: italic; border-left: 3px solid #3EC9A7;
        padding-left: 8px; line-height: 1.5;
    }
    .time-ago { font-size: 0.72rem; color: #95A5A6; }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 2px 9px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-right: 4px;
        letter-spacing: 0.3px;
    }
    .badge-crisis    { background: #C0392B; color: white; }
    .badge-high      { background: #E67E22; color: white; }
    .badge-moderate  { background: #D4AC0D; color: #1a1a1a; }
    .badge-low       { background: #27AE60; color: white; }
    .badge-selfharm  { background: #8E44AD; color: white; }
    .badge-psychosis { background: #2980B9; color: white; }
    .badge-harm-other { background: #C0392B; color: white; }
    .badge-interpreter { background: #1B3A4B; color: #3EC9A7; }
    .badge-language  { background: #EBF5FB; color: #1B4F72; border: 1px solid #AED6F1; }
    .badge-new {
        background: #3EC9A7; color: white;
        animation: pulse 1.2s infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.55} }

    /* AI summary box */
    .ai-summary-box {
        background: #F0F9F7;
        border: 1px solid #A9DFBF;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-top: 8px;
        font-size: 0.82rem;
        color: #1E4D3A;
        line-height: 1.6;
    }
    .ai-summary-box b { color: #0E6655; }

    /* Safety flags */
    .safety-flag {
        background: #FDEDEC;
        border: 1px solid #E74C3C;
        border-radius: 6px;
        padding: 0.5rem 0.8rem;
        margin-top: 6px;
        font-size: 0.8rem;
        color: #922B21;
        font-weight: 600;
    }

    /* Distress faces */
    .distress-bar {
        display: flex; gap: 4px; margin: 4px 0;
    }
    .distress-pip {
        width: 14px; height: 14px; border-radius: 50%;
        display: inline-block;
    }
    .pip-filled-1 { background: #27AE60; }
    .pip-filled-2 { background: #A9DFBF; }
    .pip-filled-3 { background: #F4D03F; }
    .pip-filled-4 { background: #E67E22; }
    .pip-filled-5 { background: #C0392B; }
    .pip-empty    { background: #D5DBDB; }

    .detail-section-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #7A8FA6;
        margin: 0.8rem 0 0.4rem 0;
        padding-bottom: 3px;
        border-bottom: 1px solid #E4EAF0;
    }

    .symptom-chip {
        display: inline-block;
        background: #EBF5FB;
        color: #1B4F72;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin: 2px;
        border: 1px solid #AED6F1;
    }
    .symptom-chip.danger {
        background: #FDEDEC;
        color: #922B21;
        border-color: #F1948A;
    }

    /* Sidebar */
    .sidebar-stat {
        background: #F4F6F9;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stat-label { font-size: 0.78rem; color: #6B7C93; }
    .stat-value { font-size: 1.1rem; font-weight: 700; color: #1B3A4B; }
    .stat-crisis { color: #C0392B; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────

SYMPTOM_LABELS = {
    "sad_or_hopeless":           "Sad or hopeless",
    "anxiety_or_panic":          "Anxiety / panic",
    "difficulty_sleeping":       "Difficulty sleeping",
    "hearing_or_seeing_things":  "Hearing/seeing things",
    "thoughts_of_self_harm":     "Thoughts of self-harm",
    "thoughts_of_harming_others":"Thoughts of harming others",
    "difficulty_eating":         "Difficulty eating",
    "feeling_disconnected":      "Feeling disconnected",
    "overwhelming_anger":        "Overwhelming anger",
    "substance_use":             "Substance use concerns",
}

DANGER_SYMPTOMS = {
    "thoughts_of_self_harm",
    "thoughts_of_harming_others",
    "hearing_or_seeing_things",
}

ONSET_LABELS = {
    "today":       "Today",
    "this_week":   "This week",
    "this_month":  "This month",
    "longer":      "Longer than a month",
}

IMPACT_LABELS = {
    "not_at_all":      "Not at all",
    "a_little":        "A little",
    "a_lot":           "A lot",
    "cannot_function": "Cannot function",
}

LANGUAGE_FLAGS = {"en": "🇬🇧 EN", "es": "🇪🇸 ES", "ar": "🇸🇦 AR"}

DISTRESS_FACES = ["😌", "🙂", "😐", "😟", "😰"]
DISTRESS_COLORS = ["#27AE60", "#A9DFBF", "#F4D03F", "#E67E22", "#C0392B"]

# ── Seed data ──────────────────────────────────────────────────────────

SEED_PATIENTS = [
    {
        "first_name": "Amira", "last_name": "Khalil", "age": 29, "gender": "female",
        "preferred_language": "ar", "interpreter_needed": True,
        "raw_concern_text": "أشعر بالخوف الشديد طوال الوقت ولا أستطيع النوم. رأيت أشياء مروعة في بلدي.",
        "onset": "longer", "previous_episode": False, "is_crisis": False,
        "distress_level": 4,
        "symptoms": ["anxiety_or_panic", "difficulty_sleeping", "feeling_disconnected", "sad_or_hopeless"],
        "daily_impact": "a_lot",
        "current_treatment": False, "current_medications": [], "other_conditions": [],
        "allergies": [], "previous_mh_hospital": False,
        "cultural_notes": "لا أريد أن تعرف عائلتي أنني أتلقى العلاج النفسي. يعتبر هذا عاراً في ثقافتنا.",
        "clinician_gender_preference": "female", "family_involvement": "no",
        "additional_notes": None,
    },
    {
        "first_name": "Carlos", "last_name": "Mendoza", "age": 41, "gender": "male",
        "preferred_language": "es", "interpreter_needed": True,
        "raw_concern_text": "No puedo dejar de pensar en lo que pasó durante el viaje. Tengo pesadillas todos los noches y no puedo trabajar.",
        "onset": "this_month", "previous_episode": False, "is_crisis": False,
        "distress_level": 4,
        "symptoms": ["difficulty_sleeping", "anxiety_or_panic", "sad_or_hopeless", "overwhelming_anger"],
        "daily_impact": "a_lot",
        "current_treatment": False, "current_medications": [], "other_conditions": ["Hypertension"],
        "allergies": ["Penicillin"], "previous_mh_hospital": False,
        "cultural_notes": "Soy el proveedor de mi familia. Me cuesta admitir que necesito ayuda.",
        "clinician_gender_preference": "no_preference", "family_involvement": "not_now",
        "additional_notes": "Mi familia no sabe que estoy aquí.",
    },
    {
        "first_name": "Fatou", "last_name": "Diallo", "age": 23, "gender": "female",
        "preferred_language": "en", "interpreter_needed": False,
        "raw_concern_text": "I keep hearing voices that tell me bad things will happen. I'm scared of myself sometimes.",
        "onset": "this_week", "previous_episode": True, "is_crisis": True,
        "distress_level": 5,
        "symptoms": ["hearing_or_seeing_things", "thoughts_of_self_harm", "anxiety_or_panic", "feeling_disconnected"],
        "daily_impact": "cannot_function",
        "current_treatment": False, "current_medications": [], "other_conditions": [],
        "allergies": [], "previous_mh_hospital": True,
        "cultural_notes": "I am Christian. Prayer is important to me but it's not enough right now.",
        "clinician_gender_preference": "female", "family_involvement": "yes",
        "additional_notes": "My sister is here with me.",
    },
    {
        "first_name": "Hassan", "last_name": "Nur", "age": 35, "gender": "male",
        "preferred_language": "en", "interpreter_needed": False,
        "raw_concern_text": "I've been drinking a lot to cope. I know it's not good. I get very angry and my wife is scared of me.",
        "onset": "this_month", "previous_episode": False, "is_crisis": False,
        "distress_level": 3,
        "symptoms": ["substance_use", "overwhelming_anger", "thoughts_of_harming_others", "difficulty_sleeping"],
        "daily_impact": "a_lot",
        "current_treatment": False, "current_medications": [], "other_conditions": [],
        "allergies": [], "previous_mh_hospital": False,
        "cultural_notes": "Please don't involve any community members or imams. I want privacy.",
        "clinician_gender_preference": "male", "family_involvement": "no",
        "additional_notes": "I don't want my wife to come in for now.",
    },
    {
        "first_name": "Nadia", "last_name": "Osman", "age": 17, "gender": "female",
        "preferred_language": "en", "interpreter_needed": False,
        "raw_concern_text": "I don't really want to be here anymore. Everything feels pointless. I haven't eaten properly in weeks.",
        "onset": "longer", "previous_episode": True, "is_crisis": True,
        "distress_level": 5,
        "symptoms": ["thoughts_of_self_harm", "sad_or_hopeless", "difficulty_eating", "difficulty_sleeping"],
        "daily_impact": "cannot_function",
        "current_treatment": False, "current_medications": [], "other_conditions": [],
        "allergies": [], "previous_mh_hospital": False,
        "cultural_notes": "My parents don't know I'm here. I came alone.",
        "clinician_gender_preference": "female", "family_involvement": "not_now",
        "additional_notes": "I haven't told anyone about this.",
    },
]

# ── Priority helpers ───────────────────────────────────────────────────

def compute_priority(p: dict) -> int:
    """1 = crisis/immediate, 2 = high, 3 = moderate, 4 = low."""
    if p["is_crisis"]:
        return 1
    danger = set(p.get("symptoms", [])) & DANGER_SYMPTOMS
    if danger or p["distress_level"] >= 4 or p["daily_impact"] == "cannot_function":
        return 2 if p["distress_level"] >= 4 else 2
    if p["distress_level"] == 3 or p["daily_impact"] == "a_lot":
        return 3
    return 4

PRIORITY_LABELS = {1: "Crisis", 2: "High", 3: "Moderate", 4: "Low"}
PRIORITY_CARD   = {1: "card-crisis", 2: "card-high", 3: "card-moderate", 4: "card-low"}
PRIORITY_BADGE  = {1: "badge-crisis", 2: "badge-high", 3: "badge-moderate", 4: "badge-low"}

def safety_flags(p: dict) -> list:
    flags = []
    syms = set(p.get("symptoms", []))
    if "thoughts_of_self_harm" in syms:
        flags.append("⚠️ Self-harm ideation")
    if "thoughts_of_harming_others" in syms:
        flags.append("⚠️ Risk to others")
    if "hearing_or_seeing_things" in syms:
        flags.append("⚠️ Possible psychosis")
    if p["is_crisis"]:
        flags.append("🚨 Patient flagged as crisis")
    if p.get("daily_impact") == "cannot_function":
        flags.append("⚠️ Severely impaired functioning")
    return flags

def time_ago(dt: datetime) -> str:
    diff = datetime.now() - dt
    mins = int(diff.total_seconds() / 60)
    if mins < 1:   return "Just now"
    if mins == 1:  return "1 min ago"
    if mins < 60:  return f"{mins} mins ago"
    hrs = mins // 60
    return f"{hrs}h ago"

def distress_pips_html(level: int) -> str:
    colors = DISTRESS_COLORS
    pips = ""
    for i in range(1, 6):
        if i <= level:
            pips += f'<span class="distress-pip pip-filled-{i}"></span>'
        else:
            pips += '<span class="distress-pip pip-empty"></span>'
    return f'<span class="distress-bar">{pips}</span> {DISTRESS_FACES[level-1]}'

# ── Backend helpers ────────────────────────────────────────────────────

def fetch_queue() -> list:
    resp = requests.get(f"{BACKEND_URL}/api/v1/queue", timeout=5)
    resp.raise_for_status()
    return resp.json()

def mark_seen(session_id: str):
    requests.patch(f"{BACKEND_URL}/api/v1/submission/{session_id}/seen", timeout=5)

def save_summary_to_backend(session_id: str, summary: dict) -> bool:
    try:
        r = requests.patch(
            f"{BACKEND_URL}/api/v1/submission/{session_id}/summary",
            json={"summary": summary},
            timeout=5,
        )
        r.raise_for_status()
        return True
    except Exception:
        # Best-effort write: dashboard should continue even if backend endpoint is unavailable.
        return False

def submit_seed(seed: dict) -> bool:
    # Start session
    sess = requests.post(f"{BACKEND_URL}/api/v1/session/start", timeout=5)
    sess.raise_for_status()
    session_id = sess.json()["session_id"]

    birth_year = datetime.now().year - seed["age"]
    now = datetime.now()

    payload = {
        "session_id":   session_id,
        "submitted_at": (now - timedelta(minutes=random.randint(2, 45))).isoformat(),
        "demographics": {
            "first_name":         seed["first_name"],
            "last_name":          seed["last_name"],
            "date_of_birth":      f"{birth_year}-04-01",
            "gender":             seed["gender"],
            "preferred_language": seed["preferred_language"],
            "interpreter_needed": seed["interpreter_needed"],
        },
        "presenting_concern": {
            "raw_concern_text": seed["raw_concern_text"],
            "onset":            seed["onset"],
            "previous_episode": seed["previous_episode"],
            "is_crisis":        seed["is_crisis"],
        },
        "mental_health_symptoms": {
            "distress_level": seed["distress_level"],
            "symptoms":       seed["symptoms"],
            "daily_impact":   seed["daily_impact"],
        },
        "clinical_background": {
            "current_treatment":    seed["current_treatment"],
            "current_medications":  seed["current_medications"],
            "other_conditions":     seed["other_conditions"],
            "allergies":            seed["allergies"],
            "previous_mh_hospital": seed["previous_mh_hospital"],
        },
        "cultural_needs": {
            "cultural_notes":               seed.get("cultural_notes"),
            "clinician_gender_preference":  seed["clinician_gender_preference"],
            "family_involvement":           seed["family_involvement"],
            "additional_notes":             seed.get("additional_notes"),
        },
    }
    r = requests.post(f"{BACKEND_URL}/api/v1/submission", json=payload, timeout=5)
    r.raise_for_status()
    return True

def sync_from_backend():
    records = fetch_queue()
    patients = []
    for r in records:
        p = dict(r)
        p["submitted_at"] = datetime.fromisoformat(r["submitted_at"])
        p["priority"]     = compute_priority(p)
        p["summary"]      = st.session_state.get("summaries", {}).get(p["session_id"])
        patients.append(p)
    patients.sort(key=lambda x: (x["priority"], x["submitted_at"]))
    st.session_state.patients = patients

# ── AI summary ─────────────────────────────────────────────────────────

def run_ai_summary(patient: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    syms_readable = [SYMPTOM_LABELS.get(s, s) for s in patient.get("symptoms", [])]
    flags         = safety_flags(patient)

    prompt = f"""You are a clinical documentation assistant supporting a mental health clinician working with refugee patients.

A patient has submitted a self-reported intake form. Your job is to:
1. Translate any non-English text faithfully into English (do not paraphrase or omit)
2. Produce a structured clinical summary for the clinician
3. Flag any immediate safety concerns clearly at the top

You must not omit or soften anything the patient said. Preserve their meaning exactly.

--- PATIENT DATA ---
Name: {patient['patient_name']}, Age: {patient['age']}, Gender: {patient['gender']}
Language: {patient['preferred_language'].upper()} | Interpreter needed: {patient['interpreter_needed']}

PATIENT'S OWN WORDS (translate if not English):
\"\"\"{patient['raw_concern_text']}\"\"\"

Onset: {ONSET_LABELS.get(patient['onset'], patient['onset'])}
Previous episode: {patient['previous_episode']}
Self-reported crisis: {patient['is_crisis']}

Distress level: {patient['distress_level']}/5
Reported symptoms: {', '.join(syms_readable) if syms_readable else 'None'}
Daily life impact: {IMPACT_LABELS.get(patient['daily_impact'], patient['daily_impact'])}

Current treatment: {patient['current_treatment']}
Medications: {', '.join(patient['current_medications']) if patient['current_medications'] else 'None'}
Other conditions: {', '.join(patient['other_conditions']) if patient['other_conditions'] else 'None'}
Allergies: {', '.join(patient['allergies']) if patient['allergies'] else 'None'}
Previous MH hospitalisation: {patient['previous_mh_hospital']}

Cultural / personal notes (translate if not English):
\"\"\"{patient.get('cultural_notes') or 'None provided'}\"\"\"

Clinician gender preference: {patient['clinician_gender_preference']}
Family involvement: {patient['family_involvement']}

Additional notes (translate if not English):
\"\"\"{patient.get('additional_notes') or 'None'}\"\"\"

System-detected safety flags: {', '.join(flags) if flags else 'None'}
--- END ---

Return ONLY a valid JSON object with no markdown or extra text:
{{
  "translation_of_concern": "<faithful English translation of raw_concern_text — write 'Already in English' if it was already English>",
  "translation_of_cultural_notes": "<faithful English translation of cultural_notes — write 'Already in English' or 'None provided'>",
  "clinical_summary": "<2-3 sentence structured summary for the clinician. Plain clinical language, comprehensive, nothing omitted>",
  "immediate_safety_concerns": ["<list each specific concern as a short string, e.g. 'Active self-harm ideation', 'Possible psychosis (auditory hallucinations)'>"],
  "key_cultural_considerations": "<1-2 sentences on what the clinician must be aware of culturally/personally before the consultation>",
  "suggested_priority": "<Crisis | High | Moderate | Low>",
  "recommended_action": "<one sentence: what should the clinician do first>"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"error": f"Unexpected response: {raw[:200]}"}
    return result

# ── Session state init ─────────────────────────────────────────────────

if "summaries" not in st.session_state:
    st.session_state.summaries = {}

if "backend_available" not in st.session_state:
    st.session_state.backend_available = True

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

if "patients" not in st.session_state:
    try:
        sync_from_backend()
        if not st.session_state.patients:
            for seed in SEED_PATIENTS:
                try:
                    submit_seed(seed)
                except Exception:
                    pass
            sync_from_backend()
        st.session_state.backend_available = True
    except Exception:
        st.session_state.backend_available = False
        now = datetime.now()
        st.session_state.patients = []
        for i, seed in enumerate(SEED_PATIENTS):
            p = dict(seed)
            p["session_id"]   = f"local-{i}"
            p["patient_name"] = f"{seed['first_name']} {seed['last_name']}"
            p["submitted_at"] = now - timedelta(minutes=5 * (i + 1))
            p["priority"]     = compute_priority(p)
            p["summary"]      = None
            st.session_state.patients.append(p)
        st.session_state.patients.sort(key=lambda x: (x["priority"], x["submitted_at"]))

# ── Auto-refresh sync ──────────────────────────────────────────────────

if st.session_state.auto_refresh and st.session_state.backend_available:
    try:
        sync_from_backend()
        # Re-attach any cached summaries
        for p in st.session_state.patients:
            p["summary"] = st.session_state.summaries.get(p["session_id"])
    except Exception:
        pass

# ── Header ─────────────────────────────────────────────────────────────

active    = st.session_state.patients
total     = len(active)
crisis    = sum(1 for p in active if p["priority"] == 1)
need_interp = sum(1 for p in active if p.get("interpreter_needed"))

st.markdown(f"""
<div class="header-bar">
    <div>
        <p class="header-title">🧠 RefugeesMH — Clinician Dashboard</p>
        <p class="header-sub">Mental Health Intake Queue · Clinician View</p>
    </div>
    <div style="display:flex; gap:10px; align-items:center;">
        <span class="badge badge-crisis" style="padding:5px 14px; font-size:0.82rem;">
            🚨 {crisis} Crisis
        </span>
        <span class="badge" style="background:#1B3A4B; color:white; padding:5px 14px; font-size:0.82rem;">
            {total} Waiting
        </span>
        {"" if not need_interp else f'<span class="badge badge-interpreter" style="padding:5px 14px; font-size:0.82rem;">🗣 {need_interp} Need Interpreter</span>'}
        <span style="color:#7EC8C0; font-size:0.78rem;">
            {'🟢 Live' if st.session_state.auto_refresh else '⏸ Paused'}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="section-label">Queue Overview</p>', unsafe_allow_html=True)

    priorities = {1: 0, 2: 0, 3: 0, 4: 0}
    for p in active:
        priorities[p["priority"]] += 1

    for lvl, label in PRIORITY_LABELS.items():
        color_map = {1: "#C0392B", 2: "#E67E22", 3: "#D4AC0D", 4: "#27AE60"}
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<span class="stat-label">{label}</span>'
            f'<span class="stat-value" style="color:{color_map[lvl]}">{priorities[lvl]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown('<p class="section-label">AI Summary</p>', unsafe_allow_html=True)
    st.caption("Translates patient text, structures the intake, and flags safety concerns.")

    if st.button("🤖 Summarise All Unsummarised", use_container_width=True, type="primary"):
        unsummarised = [p for p in active if not p.get("summary")]
        if not unsummarised:
            st.info("All patients already have a summary.")
        else:
            with st.spinner(f"Summarising {len(unsummarised)} patient(s)..."):
                for p in unsummarised:
                    try:
                        summary = run_ai_summary(p)
                        p["summary"] = summary
                        st.session_state.summaries[p["session_id"]] = summary
                        if st.session_state.backend_available:
                            save_summary_to_backend(p["session_id"], summary)
                    except Exception as e:
                        p["summary"] = {"error": str(e)}
            st.success("Done.")
            st.rerun()

    st.divider()
    st.markdown('<p class="section-label">Live Updates</p>', unsafe_allow_html=True)
    if not st.session_state.backend_available:
        st.warning("⚠️ Backend offline — local data only.")
    else:
        st.caption("Polls backend every 5 s for new patient submissions.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Start", use_container_width=True,
                     disabled=st.session_state.auto_refresh):
            st.session_state.auto_refresh = True
            st.rerun()
    with col2:
        if st.button("⏸ Pause", use_container_width=True,
                     disabled=not st.session_state.auto_refresh):
            st.session_state.auto_refresh = False
            st.rerun()

    st.divider()
    if st.button("🔄 Refresh Queue Now", use_container_width=True):
        if st.session_state.backend_available:
            try:
                sync_from_backend()
                for p in st.session_state.patients:
                    p["summary"] = st.session_state.summaries.get(p["session_id"])
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed: {e}")

# ── Queue ───────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">Patient Queue</p>', unsafe_allow_html=True)

if not active:
    st.info("No patients currently in the queue.")

for patient in active:
    pri    = patient["priority"]
    flags  = safety_flags(patient)
    ago    = time_ago(patient["submitted_at"])
    lang   = patient.get("preferred_language", "en")
    is_new = (datetime.now() - patient["submitted_at"]).total_seconds() < 120

    # Build badge row
    badge_html = f'<span class="badge {PRIORITY_BADGE[pri]}">{PRIORITY_LABELS[pri]}</span>'
    if is_new:
        badge_html += '<span class="badge badge-new">NEW</span>'
    if patient.get("interpreter_needed"):
        badge_html += '<span class="badge badge-interpreter">🗣 Interpreter</span>'
    badge_html += f'<span class="badge badge-language">{LANGUAGE_FLAGS.get(lang, lang)}</span>'
    for f in flags:
        if "self-harm" in f.lower():
            badge_html += '<span class="badge badge-selfharm">⚠ Self-harm</span>'
        elif "psychosis" in f.lower() or "hearing" in f.lower():
            badge_html += '<span class="badge badge-psychosis">⚠ Psychosis</span>'
        elif "others" in f.lower():
            badge_html += '<span class="badge badge-harm-other">⚠ Risk to others</span>'

    # Concern preview — show translated version if available, else raw
    summary = patient.get("summary")
    concern_preview = patient["raw_concern_text"]
    if summary and "translation_of_concern" in summary and summary["translation_of_concern"] != "Already in English":
        concern_preview = summary["translation_of_concern"]

    # AI summary section
    if summary and "error" not in summary:
        ai_html = f"""
        <div class="ai-summary-box">
            <b>Summary:</b> {summary.get('clinical_summary', '')}
        """
        if summary.get("immediate_safety_concerns"):
            concerns_str = " · ".join(summary["immediate_safety_concerns"])
            ai_html += f'<div class="safety-flag">🚨 {concerns_str}</div>'
        if summary.get("recommended_action"):
            ai_html += f'<br><b>Recommended action:</b> {summary["recommended_action"]}'
        ai_html += "</div>"
    elif summary and "error" in summary:
        ai_html = f'<div class="ai-summary-box" style="color:#922B21;">⚠ Summary failed: {summary["error"]}</div>'
    else:
        ai_html = '<div style="margin-top:6px; font-size:0.78rem; color:#95A5A6;">⏳ No AI summary yet — click "Summarise All" in sidebar</div>'

    st.markdown(
        f'<div class="patient-card {PRIORITY_CARD[pri]}">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start;">'
        f'<span class="patient-name">{patient["patient_name"]}</span>'
        f'<span class="time-ago">{ago}</span>'
        f'</div>'
        f'<div class="patient-meta">{patient["age"]}y · {patient["gender"].capitalize()} · Onset: {ONSET_LABELS.get(patient["onset"], patient["onset"])}</div>'
        f'<div style="margin:5px 0;">{badge_html}</div>'
        f'<div class="complaint-text">"{concern_preview[:280]}{"..." if len(concern_preview) > 280 else ""}"</div>'
        f'{ai_html}'
        f'</div>',
        unsafe_allow_html=True
    )

    with st.expander(f"📋 Full intake — {patient['patient_name']}"):
        col_l, col_r, col_a = st.columns([2, 2, 1.2])

        with col_l:
            st.markdown('<div class="detail-section-title">Demographics</div>', unsafe_allow_html=True)
            st.write(f"**Name:** {patient['patient_name']}")
            st.write(f"**Age:** {patient['age']}  |  **Gender:** {patient['gender'].capitalize()}")
            st.write(f"**Language:** {LANGUAGE_FLAGS.get(lang, lang)}  |  **Interpreter:** {'Yes ⚠' if patient.get('interpreter_needed') else 'No'}")
            st.write(f"**Submitted:** {patient['submitted_at'].strftime('%d %b %Y, %H:%M')}")

            st.markdown('<div class="detail-section-title">Presenting Concern</div>', unsafe_allow_html=True)
            st.markdown(f"**Patient's words (original):**")
            st.info(patient["raw_concern_text"])
            if summary and summary.get("translation_of_concern") and summary["translation_of_concern"] != "Already in English":
                st.markdown("**English translation:**")
                st.success(summary["translation_of_concern"])
            st.write(f"**Onset:** {ONSET_LABELS.get(patient['onset'], patient['onset'])}")
            st.write(f"**Previous episode:** {'Yes' if patient['previous_episode'] else 'No'}")
            st.write(f"**Self-reported crisis:** {'🚨 YES' if patient['is_crisis'] else 'No'}")

            st.markdown('<div class="detail-section-title">Cultural & Personal Needs</div>', unsafe_allow_html=True)
            raw_cultural = patient.get("cultural_notes") or "None provided"
            st.markdown("**Patient's cultural notes (original):**")
            st.info(raw_cultural)
            if summary and summary.get("translation_of_cultural_notes") and summary["translation_of_cultural_notes"] not in ("Already in English", "None provided"):
                st.markdown("**English translation:**")
                st.success(summary["translation_of_cultural_notes"])
            st.write(f"**Clinician gender preference:** {patient['clinician_gender_preference'].replace('_', ' ').title()}")
            st.write(f"**Family involvement:** {patient['family_involvement'].replace('_', ' ').title()}")
            if patient.get("additional_notes"):
                st.write(f"**Additional notes:** {patient['additional_notes']}")

        with col_r:
            st.markdown('<div class="detail-section-title">Mental Health Symptoms</div>', unsafe_allow_html=True)
            st.markdown(f"**Distress level:** {distress_pips_html(patient['distress_level'])} ({patient['distress_level']}/5)", unsafe_allow_html=True)
            st.write(f"**Daily impact:** {IMPACT_LABELS.get(patient['daily_impact'], patient['daily_impact'])}")
            st.markdown("**Reported symptoms:**")
            syms_html = ""
            for sym in patient.get("symptoms", []):
                cls = "symptom-chip danger" if sym in DANGER_SYMPTOMS else "symptom-chip"
                syms_html += f'<span class="{cls}">{SYMPTOM_LABELS.get(sym, sym)}</span>'
            st.markdown(syms_html or "None", unsafe_allow_html=True)

            if flags:
                st.markdown('<div class="detail-section-title">⚠ Safety Flags</div>', unsafe_allow_html=True)
                for f in flags:
                    st.error(f)

            st.markdown('<div class="detail-section-title">Clinical Background</div>', unsafe_allow_html=True)
            st.write(f"**In treatment:** {'Yes' if patient['current_treatment'] else 'No'}")
            st.write(f"**Medications:** {', '.join(patient['current_medications']) or 'None'}")
            st.write(f"**Other conditions:** {', '.join(patient['other_conditions']) or 'None'}")
            st.write(f"**Allergies:** {', '.join(patient['allergies']) or 'None'}")
            st.write(f"**Previous MH hospitalisation:** {'Yes' if patient['previous_mh_hospital'] else 'No'}")

            if summary and "error" not in summary:
                st.markdown('<div class="detail-section-title">AI Clinical Summary</div>', unsafe_allow_html=True)
                st.success(summary.get("clinical_summary", ""))
                if summary.get("key_cultural_considerations"):
                    st.markdown("**Cultural considerations:**")
                    st.info(summary["key_cultural_considerations"])

        with col_a:
            st.markdown('<div class="detail-section-title">Actions</div>', unsafe_allow_html=True)
            st.metric("Priority", f"{PRIORITY_LABELS[pri]}")
            st.write(f"Arrived: {patient['submitted_at'].strftime('%H:%M')}")
            st.write("")

            if not patient.get("summary"):
                if st.button("🤖 Summarise", key=f"sum_{patient['session_id']}",
                             use_container_width=True):
                    with st.spinner("Summarising..."):
                        try:
                            s = run_ai_summary(patient)
                            patient["summary"] = s
                            st.session_state.summaries[patient["session_id"]] = s
                            if st.session_state.backend_available:
                                save_summary_to_backend(patient["session_id"], s)
                        except Exception as e:
                            patient["summary"] = {"error": str(e)}
                    st.rerun()

            st.write("")
            if st.button("✅ Mark as Seen", key=f"seen_{patient['session_id']}",
                         use_container_width=True, type="primary"):
                if st.session_state.backend_available:
                    try:
                        mark_seen(patient["session_id"])
                    except Exception:
                        pass
                st.session_state.patients = [
                    p for p in st.session_state.patients
                    if p["session_id"] != patient["session_id"]
                ]
                st.session_state.summaries.pop(patient["session_id"], None)
                st.rerun()

# ── Auto-refresh loop ──────────────────────────────────────────────────

if st.session_state.auto_refresh:
    time.sleep(5)
    st.rerun()