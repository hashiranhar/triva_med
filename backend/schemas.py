from pydantic import BaseModel, UUID4
from datetime import datetime, date
from typing import List, Optional
from enum import Enum
from uuid import UUID


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class SessionResponse(BaseModel):
    session_id: UUID
    created_at: datetime


# --- Enums ---

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class RedFlag(str, Enum):
    stroke = "stroke"
    sepsis = "sepsis"
    mi = "MI"
    none = "none"


class TriageStatus(str, Enum):
    pending = "pending"
    processed = "processed"
    error = "error"


# --- Nested models ---

class PatientDemographics(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    contact_number: Optional[str] = None


class ChiefComplaint(BaseModel):
    description: str
    onset_time: datetime
    is_trauma: bool


class Symptom(BaseModel):
    name: str
    severity: int
    location: Optional[str] = None
    duration_minutes: int


class SymptomDetails(BaseModel):
    symptoms: List[Symptom]
    pain_score: int
    is_worsening: bool


class MedicalHistory(BaseModel):
    existing_conditions: List[str]
    current_medications: List[str]
    allergies: List[str]
    recent_surgeries: Optional[str] = None


# --- Request / Response models ---

class PatientSubmission(BaseModel):
    session_id: UUID4
    submitted_at: datetime
    demographics: PatientDemographics
    chief_complaint: ChiefComplaint
    symptoms: SymptomDetails
    medical_history: MedicalHistory


class SubmissionResponse(BaseModel):
    session_id: UUID4
    status: str
    message: str


class TriageResult(BaseModel):
    session_id: UUID4
    esi_score: int
    red_flags: List[RedFlag]
    ai_summary: str
    submitted_at: datetime
    patient_name: str
    age: int
    chief_complaint_description: str