from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session as DBSession

from backend.schemas import (
    HealthResponse,
    SessionResponse,
    PatientSubmission,
    SubmissionResponse,
)
from backend.database import engine, Base, get_db
from backend import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RefugeesMH Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def run_migrations():
    """Ensure any columns added after initial creation are present."""
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(submissions)"))
        cols = [row[1] for row in result]
        if "seen" not in cols:
            conn.execute(
                text("ALTER TABLE submissions ADD COLUMN seen BOOLEAN DEFAULT 0")
            )
            conn.commit()


def calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )


# ── Health ─────────────────────────────────────────────────────────────

@app.get("/api/v1/health")
def health_check():
    return HealthResponse(status="ok", timestamp=datetime.now())


# ── Session ────────────────────────────────────────────────────────────

@app.post("/api/v1/session/start", status_code=201)
def start_session(db: DBSession = Depends(get_db)):
    session_id = str(uuid4())
    now = datetime.now()
    db_session = models.Session(
        session_id=session_id, created_at=now, status="pending"
    )
    db.add(db_session)
    db.commit()
    return SessionResponse(session_id=session_id, created_at=now)


@app.get("/api/v1/session/{session_id}/status")
def get_session_status(session_id: str, db: DBSession = Depends(get_db)):
    db_session = db.query(models.Session).filter_by(session_id=session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id":   db_session.session_id,
        "status":       db_session.status,
        "processed_at": db_session.processed_at,
    }


# ── Submission ─────────────────────────────────────────────────────────

@app.post("/api/v1/submission", status_code=202)
def submit_patient_form(
    submission: PatientSubmission, db: DBSession = Depends(get_db)
):
    sid = str(submission.session_id)
    d   = submission.demographics

    patient_name = f"{d.first_name} {d.last_name}"
    age          = calculate_age(d.date_of_birth)

    db_sub = models.Submission(
        session_id   = sid,
        submitted_at = submission.submitted_at,
        seen         = False,

        # demographics
        patient_name       = patient_name,
        age                = age,
        gender             = d.gender.value,
        preferred_language = d.preferred_language.value,
        interpreter_needed = d.interpreter_needed,

        # presenting concern
        raw_concern_text = submission.presenting_concern.raw_concern_text,
        onset            = submission.presenting_concern.onset.value,
        previous_episode = submission.presenting_concern.previous_episode,
        is_crisis        = submission.presenting_concern.is_crisis,

        # mental health symptoms
        distress_level = submission.mental_health_symptoms.distress_level,
        symptoms       = [s.value for s in submission.mental_health_symptoms.symptoms],
        daily_impact   = submission.mental_health_symptoms.daily_impact.value,

        # clinical background
        current_treatment    = submission.clinical_background.current_treatment,
        current_medications  = submission.clinical_background.current_medications,
        other_conditions     = submission.clinical_background.other_conditions,
        allergies            = submission.clinical_background.allergies,
        previous_mh_hospital = submission.clinical_background.previous_mh_hospital,

        # cultural needs
        cultural_notes              = submission.cultural_needs.cultural_notes,
        clinician_gender_preference = submission.cultural_needs.clinician_gender_preference.value,
        family_involvement          = submission.cultural_needs.family_involvement.value,
        additional_notes            = submission.cultural_needs.additional_notes,
    )
    db.add(db_sub)

    db_session = db.query(models.Session).filter_by(session_id=sid).first()
    if db_session:
        db_session.status       = "processed"
        db_session.processed_at = datetime.now()

    db.commit()

    return SubmissionResponse(
        session_id=submission.session_id,
        status="received",
        message="Thank you. Your information has been received. A member of our team will be with you shortly.",
    )


# ── Queue ──────────────────────────────────────────────────────────────

@app.get("/api/v1/queue")
def get_patient_queue(db: DBSession = Depends(get_db)):
    """Returns all unseen submissions ordered by submission time."""
    submissions = (
        db.query(models.Submission)
        .filter(
            (models.Submission.seen == False) | (models.Submission.seen == None)
        )
        .order_by(models.Submission.submitted_at)
        .all()
    )
    return [_serialise(s) for s in submissions]


@app.patch("/api/v1/submission/{session_id}/seen")
def mark_patient_seen(session_id: str, db: DBSession = Depends(get_db)):
    sub = db.query(models.Submission).filter_by(session_id=session_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub.seen = True
    db.commit()
    return {"status": "ok", "session_id": session_id}


@app.get("/api/v1/submission/{session_id}")
def get_submission(session_id: str, db: DBSession = Depends(get_db)):
    sub = db.query(models.Submission).filter_by(session_id=session_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return _serialise(sub)


# ── Serialiser helper ──────────────────────────────────────────────────

def _serialise(s: models.Submission) -> dict:
    return {
        "session_id":         s.session_id,
        "submitted_at":       s.submitted_at.isoformat(),
        "patient_name":       s.patient_name,
        "age":                s.age,
        "gender":             s.gender,
        "preferred_language": s.preferred_language,
        "interpreter_needed": s.interpreter_needed,

        "raw_concern_text": s.raw_concern_text,
        "onset":            s.onset,
        "previous_episode": s.previous_episode,
        "is_crisis":        s.is_crisis,

        "distress_level": s.distress_level,
        "symptoms":       s.symptoms,
        "daily_impact":   s.daily_impact,

        "current_treatment":    s.current_treatment,
        "current_medications":  s.current_medications,
        "other_conditions":     s.other_conditions,
        "allergies":            s.allergies,
        "previous_mh_hospital": s.previous_mh_hospital,

        "cultural_notes":               s.cultural_notes,
        "clinician_gender_preference":  s.clinician_gender_preference,
        "family_involvement":           s.family_involvement,
        "additional_notes":             s.additional_notes,
    }