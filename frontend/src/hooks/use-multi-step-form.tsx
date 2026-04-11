import {
    personalInfoSchema,
    presentingConcernSchema,
    mentalHealthSymptomsSchema,
    clinicalBackgroundSchema,
    culturalNeedsSchema,
    type Step,
    type AllFormFields,
} from "@/types"
import { Church, CircleQuestionMark, ClipboardClock, SmilePlus, User } from "lucide-react"
import { useState, useEffect } from "react"

const stepSchemas = [
    personalInfoSchema,
    presentingConcernSchema,
    mentalHealthSymptomsSchema,
    clinicalBackgroundSchema,
    culturalNeedsSchema,
]

export const steps: Step[] = [
    { id: "personal",  name: "About You",        icon: User },
    { id: "concern",   name: "Your Concern",      icon: CircleQuestionMark },
    { id: "symptoms",  name: "Symptoms",          icon: SmilePlus },
    { id: "background",name: "Background",        icon: ClipboardClock },
    { id: "cultural",  name: "Cultural Needs",    icon: Church },
]

const API_BASE = "/api/v1"

const splitList = (value: string | undefined) =>
    (value || "").split(",").map(s => s.trim()).filter(Boolean)

export function useMultiStepForm() {
    const [currentStep,  setCurrentStep]  = useState(0)
    const [formData,     setFormData]     = useState<Partial<AllFormFields>>({})
    const [isSubmitted,  setIsSubmitted]  = useState(false)
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [submitError,  setSubmitError]  = useState<string | null>(null)
    const [sessionId,    setSessionId]    = useState<string | null>(null)

    // Start a session as soon as the form mounts.
    useEffect(() => {
        fetch(`${API_BASE}/session/start`, { method: "POST" })
            .then(res => res.json())
            .then(data => setSessionId(data.session_id))
            .catch(err => console.error("Failed to start session:", err))
    }, [])

    const isFirstStep = currentStep === 0
    const isLastStep  = currentStep === steps.length - 1

    const getCurrentStepSchema = () => stepSchemas[currentStep]

    const goToNextStep     = () => { if (!isLastStep)  setCurrentStep(p => p + 1) }
    const goToPreviousStep = () => { if (!isFirstStep) setCurrentStep(p => p - 1) }

    const updateFormData = (newData: Partial<AllFormFields>) => {
        setFormData(prev => ({ ...prev, ...newData }))
    }

    const submitForm = async (data: Partial<AllFormFields>) => {
        if (!sessionId) throw new Error("Session not initialised — please refresh and try again.")

        const payload = {
            session_id:   sessionId,
            submitted_at: new Date().toISOString(),
            demographics: {
                first_name:         data.firstName,
                last_name:          data.lastName,
                date_of_birth:      data.dateOfBirth,
                gender:             data.gender,
                preferred_language: data.preferredLanguage,
                interpreter_needed: data.interpreterNeeded ?? false,
            },
            presenting_concern: {
                raw_concern_text: data.rawConcernText,
                onset:            data.onset,
                previous_episode: data.previousEpisode ?? false,
                is_crisis:        data.isCrisis ?? false,
            },
            mental_health_symptoms: {
                distress_level: data.distressLevel ?? 1,
                symptoms:       splitList(data.symptoms),
                daily_impact:   data.dailyImpact,
            },
            clinical_background: {
                current_treatment:    data.currentTreatment ?? false,
                current_medications:  splitList(data.currentMedications),
                other_conditions:     splitList(data.otherConditions),
                allergies:            splitList(data.allergies),
                previous_mh_hospital: data.previousMhHospital ?? false,
            },
            cultural_needs: {
                cultural_notes:               data.culturalNotes   || null,
                clinician_gender_preference:  data.clinicianGenderPreference,
                family_involvement:           data.familyInvolvement,
                additional_notes:             data.additionalNotes || null,
            },
        }

        setIsSubmitting(true)
        setSubmitError(null)

        const response = await fetch(`${API_BASE}/submission`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(payload),
        })

        setIsSubmitting(false)

        if (!response.ok) {
            const err = await response.json().catch(() => ({}))
            throw new Error(err.detail || "Submission failed. Please try again.")
        }

        setIsSubmitted(true)
    }

    const resetForm = () => {
        setFormData({})
        setCurrentStep(0)
        setIsSubmitted(false)
        setSubmitError(null)
    }

    return {
        currentStep,
        formData,
        isFirstStep,
        isLastStep,
        isSubmitted,
        isSubmitting,
        submitError,
        setSubmitError,
        sessionId,
        steps,

        goToNextStep,
        getCurrentStepSchema,
        goToPreviousStep,
        updateFormData,
        submitForm,
        resetForm,
    }
}
