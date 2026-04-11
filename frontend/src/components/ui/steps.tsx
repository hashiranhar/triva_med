import { CardTitle } from "./card"
import FormField from "./form-field"
import type { StepFormData } from "@/types"
import type { useForm } from "react-hook-form"
import { Label } from "./label"
import {
    Select, SelectContent, SelectGroup, SelectItem,
    SelectLabel, SelectTrigger, SelectValue,
} from "./select"
import { useState } from "react"

interface StepProps {
    register:  ReturnType<typeof useForm<StepFormData>>["register"]
    errors:    Record<string, { message?: string }>
    setValue?: ReturnType<typeof useForm<StepFormData>>["setValue"]
}

// ── Helpers ────────────────────────────────────────────────────────────

const BoolSelect = ({
    label, field, setValue, errors,
}: {
    label: string
    field: string
    setValue?: StepProps["setValue"]
    errors: StepProps["errors"]
}) => {
    const [val, setVal] = useState("")
    return (
        <div className="space-y-2">
            <Label htmlFor={field}>{label}</Label>
            <Select onValueChange={(v) => {
                setVal(v)
                setValue?.(field as never, (v === "true") as never, { shouldValidate: true })
            }} value={val}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select..." />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="true">Yes</SelectItem>
                        <SelectItem value="false">No</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
            {errors[field] && <p className="text-sm text-destructive">{errors[field].message}</p>}
        </div>
    )
}

// ── Mental health symptom list (matches backend MHSymptom enum) ────────

const SYMPTOMS: { key: string; label: string }[] = [
    { key: "sad_or_hopeless",            label: "Sad or hopeless" },
    { key: "anxiety_or_panic",           label: "Anxiety / panic" },
    { key: "difficulty_sleeping",        label: "Difficulty sleeping" },
    { key: "hearing_or_seeing_things",   label: "Hearing / seeing things" },
    { key: "thoughts_of_self_harm",      label: "Thoughts of self-harm" },
    { key: "thoughts_of_harming_others", label: "Thoughts of harming others" },
    { key: "difficulty_eating",          label: "Difficulty eating" },
    { key: "feeling_disconnected",       label: "Feeling disconnected" },
    { key: "overwhelming_anger",         label: "Overwhelming anger" },
    { key: "substance_use",              label: "Substance use concerns" },
]

// ── Step 1 — About You ─────────────────────────────────────────────────

const PersonalInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [gender,    setGender]    = useState("")
    const [language,  setLanguage]  = useState("")
    const [interp,    setInterp]    = useState("")

    return (
        <div className="space-y-5">
            <CardTitle className="text-xl">About You</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <FormField id="firstName"   label="First Name"    register={register} errors={errors} />
                <FormField id="lastName"    label="Last Name"     register={register} errors={errors} />
                <FormField id="dateOfBirth" label="Date of Birth" register={register} errors={errors} type="date" />

                <div className="space-y-2">
                    <Label>Gender</Label>
                    <Select onValueChange={(v) => { setGender(v); setValue?.("gender", v as never, { shouldValidate: true }) }} value={gender}>
                        <SelectTrigger className="w-[220px]"><SelectValue placeholder="Select gender" /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Gender</SelectLabel>
                                <SelectItem value="male">Male</SelectItem>
                                <SelectItem value="female">Female</SelectItem>
                                <SelectItem value="non_binary">Non-binary</SelectItem>
                                <SelectItem value="prefer_not_to_say">Prefer not to say</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.gender && <p className="text-sm text-destructive">{errors.gender.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>Preferred Language</Label>
                    <Select onValueChange={(v) => { setLanguage(v); setValue?.("preferredLanguage", v as never, { shouldValidate: true }) }} value={language}>
                        <SelectTrigger className="w-[220px]"><SelectValue placeholder="Select language" /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Language</SelectLabel>
                                <SelectItem value="en">English</SelectItem>
                                <SelectItem value="es">Español</SelectItem>
                                <SelectItem value="ar">عربي</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.preferredLanguage && <p className="text-sm text-destructive">{errors.preferredLanguage.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>Do you need an interpreter?</Label>
                    <Select onValueChange={(v) => { setInterp(v); setValue?.("interpreterNeeded", (v === "true") as never, { shouldValidate: true }) }} value={interp}>
                        <SelectTrigger className="w-[180px]"><SelectValue placeholder="Select..." /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="true">Yes</SelectItem>
                                <SelectItem value="false">No</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.interpreterNeeded && <p className="text-sm text-destructive">{errors.interpreterNeeded.message}</p>}
                </div>

            </div>
        </div>
    )
}

// ── Step 2 — Your Concern ──────────────────────────────────────────────

const ReasonInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [onset,   setOnset]   = useState("")
    const [prevEp,  setPrevEp]  = useState("")
    const [crisis,  setCrisis]  = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">Your Concern</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <FormField
                    id="rawConcernText"
                    label="In your own words, what has brought you here today?"
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label>How long have you been feeling this way?</Label>
                    <Select onValueChange={(v) => { setOnset(v); setValue?.("onset", v as never, { shouldValidate: true }) }} value={onset}>
                        <SelectTrigger className="w-[240px]"><SelectValue placeholder="Select..." /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Duration</SelectLabel>
                                <SelectItem value="today">Today</SelectItem>
                                <SelectItem value="this_week">This week</SelectItem>
                                <SelectItem value="this_month">This month</SelectItem>
                                <SelectItem value="longer">Longer than a month</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.onset && <p className="text-sm text-destructive">{errors.onset.message}</p>}
                </div>

                <BoolSelect label="Have you felt this way before?" field="previousEpisode" setValue={setValue} errors={errors} />
                <div className="space-y-2">
                    <Label>Are you in crisis right now?</Label>
                    <Select onValueChange={(v) => { setCrisis(v); setValue?.("isCrisis", (v === "true") as never, { shouldValidate: true }) }} value={crisis}>
                        <SelectTrigger className="w-[180px]"><SelectValue placeholder="Select..." /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="true">Yes</SelectItem>
                                <SelectItem value="false">No</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.isCrisis && <p className="text-sm text-destructive">{errors.isCrisis.message}</p>}
                </div>

            </div>
        </div>
    )
}

// ── Step 3 — Symptoms ──────────────────────────────────────────────────

const FeelingInfoStep = ({ errors, setValue }: StepProps) => {
    const [selected, setSelected] = useState<Set<string>>(new Set())
    const [distress,  setDistress]  = useState("")
    const [impact,    setImpact]    = useState("")

    const toggleSymptom = (key: string) => {
        const next = new Set(selected)
        if (next.has(key)) next.delete(key); else next.add(key)
        setSelected(next)
        setValue?.("symptoms", Array.from(next).join(",") as never, { shouldValidate: true })
    }

    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">How Are You Feeling?</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <div className="space-y-2">
                    <Label>Which of the following have you been experiencing? (select all that apply)</Label>
                    <div className="grid grid-cols-2 gap-2 pt-1">
                        {SYMPTOMS.map(({ key, label }) => (
                            <label key={key} className="flex items-center gap-2 cursor-pointer text-sm">
                                <input
                                    type="checkbox"
                                    checked={selected.has(key)}
                                    onChange={() => toggleSymptom(key)}
                                    className="rounded"
                                />
                                {label}
                            </label>
                        ))}
                    </div>
                    {errors.symptoms && <p className="text-sm text-destructive">{errors.symptoms.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>Distress level (1 = low, 5 = severe)</Label>
                    <Select onValueChange={(v) => { setDistress(v); setValue?.("distressLevel", Number(v) as never, { shouldValidate: true }) }} value={distress}>
                        <SelectTrigger className="w-[180px]"><SelectValue placeholder="Select 1–5" /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Distress Level</SelectLabel>
                                {[1, 2, 3, 4, 5].map(n => (
                                    <SelectItem key={n} value={String(n)}>{n}</SelectItem>
                                ))}
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.distressLevel && <p className="text-sm text-destructive">{errors.distressLevel.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>How much does this affect your daily life?</Label>
                    <Select onValueChange={(v) => { setImpact(v); setValue?.("dailyImpact", v as never, { shouldValidate: true }) }} value={impact}>
                        <SelectTrigger className="w-[240px]"><SelectValue placeholder="Select..." /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Daily Impact</SelectLabel>
                                <SelectItem value="not_at_all">Not at all</SelectItem>
                                <SelectItem value="a_little">A little</SelectItem>
                                <SelectItem value="a_lot">A lot</SelectItem>
                                <SelectItem value="cannot_function">I cannot function</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.dailyImpact && <p className="text-sm text-destructive">{errors.dailyImpact.message}</p>}
                </div>

            </div>
        </div>
    )
}

// ── Step 4 — Clinical Background ───────────────────────────────────────

const BackgroundInfoStep = ({ register, errors, setValue }: StepProps) => (
    <div className="space-y-4">
        <CardTitle className="text-xl">Your Background</CardTitle>
        <div className="grid grid-cols-1 gap-5">
            <BoolSelect label="Are you currently seeing a therapist or mental health professional?" field="currentTreatment"   setValue={setValue} errors={errors} />
            <FormField  id="currentMedications" label="Mental health medications (comma-separated, or leave blank)" register={register} errors={errors} />
            <FormField  id="otherConditions"    label="Other medical conditions (comma-separated, or leave blank)"  register={register} errors={errors} />
            <FormField  id="allergies"          label="Allergies (comma-separated, or leave blank)"                 register={register} errors={errors} />
            <BoolSelect label="Have you ever been hospitalised for a mental health reason?" field="previousMhHospital" setValue={setValue} errors={errors} />
        </div>
    </div>
)

// ── Step 5 — Cultural Needs ────────────────────────────────────────────

const PersonalNeedsInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [clinGender,   setClinicianGender]    = useState("")
    const [familyInvolv, setFamilyInvolvement]  = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">Cultural &amp; Personal Needs</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <FormField
                    id="culturalNotes"
                    label="Any religious, cultural, or personal factors you'd like the care team to know? (optional)"
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label>Preferred clinician gender</Label>
                    <Select onValueChange={(v) => { setClinicianGender(v); setValue?.("clinicianGenderPreference", v as never, { shouldValidate: true }) }} value={clinGender}>
                        <SelectTrigger className="w-[220px]"><SelectValue placeholder="Select..." /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Clinician gender preference</SelectLabel>
                                <SelectItem value="male">Male</SelectItem>
                                <SelectItem value="female">Female</SelectItem>
                                <SelectItem value="no_preference">No preference</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.clinicianGenderPreference && <p className="text-sm text-destructive">{errors.clinicianGenderPreference.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>Would you like a family member or support person involved in your care?</Label>
                    <Select onValueChange={(v) => { setFamilyInvolvement(v); setValue?.("familyInvolvement", v as never, { shouldValidate: true }) }} value={familyInvolv}>
                        <SelectTrigger className="w-[180px]"><SelectValue placeholder="Select..." /></SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Family involvement</SelectLabel>
                                <SelectItem value="yes">Yes</SelectItem>
                                <SelectItem value="no">No</SelectItem>
                                <SelectItem value="not_now">Not right now</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.familyInvolvement && <p className="text-sm text-destructive">{errors.familyInvolvement.message}</p>}
                </div>

                <FormField
                    id="additionalNotes"
                    label="Anything else you'd like to share? (optional)"
                    register={register}
                    errors={errors}
                />

            </div>
        </div>
    )
}

export { PersonalInfoStep, ReasonInfoStep, FeelingInfoStep, BackgroundInfoStep, PersonalNeedsInfoStep }
