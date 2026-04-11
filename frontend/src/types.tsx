import { z } from 'zod'

// ── Step schemas (mirror backend enums exactly) ────────────────────────

export const personalInfoSchema = z.object({
    firstName:         z.string().min(1, "First name is required"),
    lastName:          z.string().min(1, "Last name is required"),
    dateOfBirth:       z.string().min(1, "Date of birth is required"),
    gender:            z.enum(["male", "female", "non_binary", "prefer_not_to_say"]),
    preferredLanguage: z.enum(["en", "es", "ar"]),
    interpreterNeeded: z.boolean().default(false),
})

export const presentingConcernSchema = z.object({
    rawConcernText:  z.string().min(1, "Please describe your concern"),
    onset:           z.enum(["today", "this_week", "this_month", "longer"]),
    previousEpisode: z.boolean().default(false),
    isCrisis:        z.boolean().default(false),
})

export const mentalHealthSymptomsSchema = z.object({
    // stored as comma-joined keys; split to array before sending to backend
    symptoms:     z.string().min(1, "Please select at least one symptom"),
    distressLevel: z.coerce.number().min(1, "Required").max(5),
    dailyImpact:  z.enum(["not_at_all", "a_little", "a_lot", "cannot_function"]),
})

export const clinicalBackgroundSchema = z.object({
    currentTreatment:   z.boolean().default(false),
    currentMedications: z.string(),
    otherConditions:    z.string(),
    allergies:          z.string(),
    previousMhHospital: z.boolean().default(false),
})

export const culturalNeedsSchema = z.object({
    culturalNotes:               z.string().optional(),
    clinicianGenderPreference:   z.enum(["male", "female", "no_preference"]),
    familyInvolvement:           z.enum(["yes", "no", "not_now"]),
    additionalNotes:             z.string().optional(),
})

// ── Derived types ──────────────────────────────────────────────────────

export type PersonalInfo          = z.infer<typeof personalInfoSchema>
export type PresentingConcernInfo = z.infer<typeof presentingConcernSchema>
export type MentalHealthSymptomsInfo = z.infer<typeof mentalHealthSymptomsSchema>
export type ClinicalBackgroundInfo = z.infer<typeof clinicalBackgroundSchema>
export type CulturalNeedsInfo     = z.infer<typeof culturalNeedsSchema>

export type StepFormData =
    | PersonalInfo
    | PresentingConcernInfo
    | MentalHealthSymptomsInfo
    | ClinicalBackgroundInfo
    | CulturalNeedsInfo

export type AllFormFields =
    PersonalInfo &
    PresentingConcernInfo &
    MentalHealthSymptomsInfo &
    ClinicalBackgroundInfo &
    CulturalNeedsInfo

export interface Step {
    id:   string
    name: string
    icon: React.ComponentType<{ className?: string }>
}
