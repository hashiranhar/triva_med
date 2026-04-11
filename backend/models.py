from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON
from backend.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id   = Column(String, primary_key=True)
    created_at   = Column(DateTime, nullable=False)
    status       = Column(String, default="pending")
    processed_at = Column(DateTime, nullable=True)


class Submission(Base):
    __tablename__ = "submissions"

    # identity
    session_id   = Column(String, primary_key=True)
    submitted_at = Column(DateTime, nullable=False)
    seen         = Column(Boolean, default=False, nullable=True)

    # demographics
    patient_name         = Column(String, nullable=False)
    age                  = Column(Integer, nullable=False)
    gender               = Column(String, nullable=False)
    preferred_language   = Column(String, nullable=False)
    interpreter_needed   = Column(Boolean, nullable=False)

    # presenting concern
    raw_concern_text  = Column(Text, nullable=False)
    onset             = Column(String, nullable=False)
    previous_episode  = Column(Boolean, nullable=False)
    is_crisis         = Column(Boolean, nullable=False)

    # mental health symptoms
    distress_level = Column(Integer, nullable=False)
    symptoms       = Column(JSON, nullable=False)   # list of MHSymptom strings
    daily_impact   = Column(String, nullable=False)

    # clinical background
    current_treatment    = Column(Boolean, nullable=False)
    current_medications  = Column(JSON, nullable=False)
    other_conditions     = Column(JSON, nullable=False)
    allergies            = Column(JSON, nullable=False)
    previous_mh_hospital = Column(Boolean, nullable=False)

    # cultural needs
    cultural_notes                = Column(Text, nullable=True)
    clinician_gender_preference   = Column(String, nullable=False)
    family_involvement            = Column(String, nullable=False)
    additional_notes              = Column(Text, nullable=True)

    # dashboard state
    seen       = Column(Boolean, default=False, nullable=True)
    ai_summary = Column(JSON, nullable=True)