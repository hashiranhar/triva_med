from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON
from backend.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    processed_at = Column(DateTime, nullable=True)


class Submission(Base):
    __tablename__ = "submissions"

    session_id = Column(String, primary_key=True)
    submitted_at = Column(DateTime, nullable=False)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    chief_complaint = Column(Text, nullable=False)
    onset_time = Column(DateTime, nullable=False)
    is_trauma = Column(Boolean, nullable=False)
    symptoms = Column(JSON, nullable=False)
    pain_score = Column(Integer, nullable=False)
    is_worsening = Column(Boolean, nullable=False)
    existing_conditions = Column(JSON, nullable=False)
    current_medications = Column(JSON, nullable=False)
    allergies = Column(JSON, nullable=False)
    recent_surgeries = Column(Text, nullable=True)
    seen = Column(Boolean, default=False, nullable=True)