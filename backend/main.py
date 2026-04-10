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

app = FastAPI(title="TrivaMed Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def run_migrations():
    """Add any missing columns to existing SQLite tables."""
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(submissions)"))
        cols = [row[1] for row in result]
        if "seen" not in cols:
            conn.execute(text("ALTER TABLE submissions ADD COLUMN seen BOOLEAN DEFAULT 0"))
            conn.commit()


def calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


@app.get("/api/v1/health")
def health_check():
    return HealthResponse(status="ok", timestamp=datetime.now())


@app.post("/api/v1/session/start", status_code=201)
def start_session(db: DBSession = Depends(get_db)):
    session_id = str(uuid4())
    now = datetime.now()
    db_session = models.Session(session_id=session_id, created_at=now, status="pending")
    db.add(db_session)
    db.commit()
    return SessionResponse(session_id=session_id, created_at=now)


@app.post("/api/v1/submission", status_code=202)
def submit_patient_form(submission: PatientSubmission, db: DBSession = Depends(get_db)):
    sid = str(submission.session_id)

    patient_name = f"{submission.demographics.first_name} {submission.demographics.last_name}"
    age = calculate_age(submission.demographics.date_of_birth)

    db_submission = models.Submission(
        session_id=sid,
        submitted_at=submission.submitted_at,
        patient_name=patient_name,
        age=age,
        gender=submission.demographics.gender.value,
        chief_complaint=submission.chief_complaint.description,
        onset_time=submission.chief_complaint.onset_time,
        is_trauma=submission.chief_complaint.is_trauma,
        symptoms=[s.model_dump() for s in submission.symptoms.symptoms],
        pain_score=submission.symptoms.pain_score,
        is_worsening=submission.symptoms.is_worsening,
        existing_conditions=submission.medical_history.existing_conditions,
        current_medications=submission.medical_history.current_medications,
        allergies=submission.medical_history.allergies,
        recent_surgeries=submission.medical_history.recent_surgeries,
    )
    db.add(db_submission)

    # Update session status
    db_session = db.query(models.Session).filter_by(session_id=sid).first()
    if db_session:
        db_session.status = "processed"
        db_session.processed_at = datetime.now()

    db.commit()

    return SubmissionResponse(
        session_id=submission.session_id,
        status="received",
        message="Your information has been received. A nurse will be with you shortly.",
    )


@app.get("/api/v1/queue")
def get_patient_queue(db: DBSession = Depends(get_db)):
    """Dashboard polls this to get all waiting (unseen) patients."""
    submissions = (
        db.query(models.Submission)
        .filter((models.Submission.seen == False) | (models.Submission.seen == None))
        .all()
    )
    return [
        {
            "session_id": s.session_id,
            "submitted_at": s.submitted_at.isoformat(),
            "patient_name": s.patient_name,
            "age": s.age,
            "gender": s.gender,
            "chief_complaint": s.chief_complaint,
            "onset_time": s.onset_time.isoformat(),
            "is_trauma": s.is_trauma,
            "symptoms": s.symptoms,
            "pain_score": s.pain_score,
            "is_worsening": s.is_worsening,
            "existing_conditions": s.existing_conditions,
            "current_medications": s.current_medications,
            "allergies": s.allergies,
            "recent_surgeries": s.recent_surgeries,
        }
        for s in submissions
    ]


@app.patch("/api/v1/submission/{session_id}/seen")
def mark_patient_seen(session_id: str, db: DBSession = Depends(get_db)):
    """Mark a patient as seen so they leave the queue."""
    sub = db.query(models.Submission).filter_by(session_id=session_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub.seen = True
    db.commit()
    return {"status": "ok", "session_id": session_id}


@app.get("/api/v1/session/{session_id}/status")
def get_session_status(session_id: str, db: DBSession = Depends(get_db)):
    db_session = db.query(models.Session).filter_by(session_id=session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": db_session.session_id,
        "status": db_session.status,
        "processed_at": db_session.processed_at,
    }