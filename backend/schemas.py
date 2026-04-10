from pydantic import BaseModel, UUID4
from datetime import datetime, date
from typing import List, Optional
from enum import Enum
from uuid import UUID


# ── Enums ──────────────────────────────────────────────────────────────

class Gender(str, Enum):
    male = "male"
    female = "female"
    non_binary = "non_binary"
    prefer_not_to_say = "prefer_not_to_say"


class PreferredLanguage(str, Enum):
    en = "en"
    es = "es"
    ar = "ar"


class OnsetDuration(str, Enum):
    today = "today"
    this_week = "this_week"
    this_month = "this_month"
    longer = "longer"


class DailyImpact(str, Enum):
    not_at_all = "not_at_all"
    a_little = "a_little"
    a_lot = "a_lot"
    cannot_function = "cannot_function"


class ClinicianGenderPreference(str, Enum):
    male = "male"
    female = "female"
    no_preference = "no_preference"


class FamilyInvolvement(str, Enum):
    yes = "yes"
    no = "no"
    not_now = "not_now"


class MHSymptom(str, Enum):
    sad_or_hopeless = "sad_or_hopeless"
    anxiety_or_panic = "anxiety_or_panic"
    difficulty_sleeping = "difficulty_sleeping"
    hearing_or_seeing_things = "hearing_or_seeing_things"
    thoughts_of_self_harm = "thoughts_of_self_harm"
    thoughts_of_harming_others = "thoughts_of_harming_others"
    difficulty_eating = "difficulty_eating"
    feeling_disconnected = "feeling_disconnected"
    overwhelming_anger = "overwhelming_anger"
    substance_use = "substance_use"


# ── Nested models ──────────────────────────────────────────────────────

class PatientDemographics(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    preferred_language: PreferredLanguage
    interpreter_needed: bool


class PresentingConcern(BaseModel):
    raw_concern_text: str           # free text in their language
    onset: OnsetDuration
    previous_episode: bool
    is_crisis: bool


class MentalHealthSymptoms(BaseModel):
    distress_level: int             # 1–5
    symptoms: List[MHSymptom]
    daily_impact: DailyImpact


class ClinicalBackground(BaseModel):
    current_treatment: bool
    current_medications: List[str]
    other_conditions: List[str]
    allergies: List[str]
    previous_mh_hospital: bool


class CulturalNeeds(BaseModel):
    cultural_notes: Optional[str] = None
    clinician_gender_preference: ClinicianGenderPreference
    family_involvement: FamilyInvolvement
    additional_notes: Optional[str] = None


# ── Request / Response models ──────────────────────────────────────────

class PatientSubmission(BaseModel):
    session_id: UUID4
    submitted_at: datetime
    demographics: PatientDemographics
    presenting_concern: PresentingConcern
    mental_health_symptoms: MentalHealthSymptoms
    clinical_background: ClinicalBackground
    cultural_needs: CulturalNeeds


class SubmissionResponse(BaseModel):
    session_id: UUID4
    status: str
    message: str


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class SessionResponse(BaseModel):
    session_id: UUID
    created_at: datetime