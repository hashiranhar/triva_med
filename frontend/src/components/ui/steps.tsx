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
import { useLang } from "@/context/LanguageContext"

interface StepProps {
    register:  ReturnType<typeof useForm<StepFormData>>["register"]
    errors:    Record<string, { message?: string }>
    setValue?: ReturnType<typeof useForm<StepFormData>>["setValue"]
}

// ── Reusable Yes / No select ───────────────────────────────────────────

const BoolSelect = ({
    label, field, setValue, errors,
}: {
    label:     string
    field:     string
    setValue?: StepProps["setValue"]
    errors:    StepProps["errors"]
}) => {
    const { t } = useLang()
    const [val, setVal] = useState("")
    return (
        <div className="space-y-2">
            <Label htmlFor={field}>{label}</Label>
            <Select onValueChange={(v) => {
                setVal(v)
                setValue?.(field as never, (v === "true") as never, { shouldValidate: true })
            }} value={val}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder={t.common.select} />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="true">{t.common.yes}</SelectItem>
                        <SelectItem value="false">{t.common.no}</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
            {errors[field] && <p className="text-sm text-destructive">{errors[field].message}</p>}
        </div>
    )
}

// ── Step 1 — About You ─────────────────────────────────────────────────

const PersonalInfoStep = ({ register, errors, setValue }: StepProps) => {
    const { t } = useLang()
    const [gender,   setGender]   = useState("")
    const [language, setLanguage] = useState("")
    const [interp,   setInterp]   = useState("")

    return (
        <div className="space-y-5">
            <CardTitle className="text-xl">{t.aboutYou.title}</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <FormField id="firstName"   label={t.aboutYou.firstName}   register={register} errors={errors} />
                <FormField id="lastName"    label={t.aboutYou.lastName}    register={register} errors={errors} />
                <FormField id="dateOfBirth" label={t.aboutYou.dateOfBirth} register={register} errors={errors} type="date" />

                <div className="space-y-2">
                    <Label>{t.aboutYou.gender}</Label>
                    <Select onValueChange={(v) => { setGender(v); setValue?.("gender", v as never, { shouldValidate: true }) }} value={gender}>
                        <SelectTrigger className="w-[220px]">
                            <SelectValue placeholder={t.aboutYou.genderPlaceholder} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>{t.aboutYou.gender}</SelectLabel>
                                <SelectItem value="male">{t.aboutYou.genderMale}</SelectItem>
                                <SelectItem value="female">{t.aboutYou.genderFemale}</SelectItem>
                                <SelectItem value="non_binary">{t.aboutYou.genderNonBinary}</SelectItem>
                                <SelectItem value="prefer_not_to_say">{t.aboutYou.genderPreferNotToSay}</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.gender && <p className="text-sm text-destructive">{errors.gender.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>{t.aboutYou.preferredLanguage}</Label>
                    <Select onValueChange={(v) => { setLanguage(v); setValue?.("preferredLanguage", v as never, { shouldValidate: true }) }} value={language}>
                        <SelectTrigger className="w-[220px]">
                            <SelectValue placeholder={t.aboutYou.languagePlaceholder} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>{t.aboutYou.preferredLanguage}</SelectLabel>
                                <SelectItem value="en">🇬🇧 English</SelectItem>
                                <SelectItem value="es">🇪🇸 Español</SelectItem>
                                <SelectItem value="ar">🇸🇦 عربي</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.preferredLanguage && <p className="text-sm text-destructive">{errors.preferredLanguage.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>{t.aboutYou.interpreterNeeded}</Label>
                    <Select onValueChange={(v) => { setInterp(v); setValue?.("interpreterNeeded", (v === "true") as never, { shouldValidate: true }) }} value={interp}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder={t.common.select} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="true">{t.common.yes}</SelectItem>
                                <SelectItem value="false">{t.common.no}</SelectItem>
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
    const { t } = useLang()
    const [onset,  setOnset]  = useState("")
    const [crisis, setCrisis] = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">{t.yourConcern.title}</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <FormField
                    id="rawConcernText"
                    label={t.yourConcern.rawConcernText}
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label>{t.yourConcern.onset}</Label>
                    <Select onValueChange={(v) => { setOnset(v); setValue?.("onset", v as never, { shouldValidate: true }) }} value={onset}>
                        <SelectTrigger className="w-[260px]">
                            <SelectValue placeholder={t.yourConcern.onsetPlaceholder} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="today">{t.yourConcern.onsetToday}</SelectItem>
                                <SelectItem value="this_week">{t.yourConcern.onsetThisWeek}</SelectItem>
                                <SelectItem value="this_month">{t.yourConcern.onsetThisMonth}</SelectItem>
                                <SelectItem value="longer">{t.yourConcern.onsetLonger}</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.onset && <p className="text-sm text-destructive">{errors.onset.message}</p>}
                </div>

                <BoolSelect label={t.yourConcern.previousEpisode} field="previousEpisode" setValue={setValue} errors={errors} />

                <div className="space-y-2">
                    <Label>{t.yourConcern.isCrisis}</Label>
                    <Select onValueChange={(v) => { setCrisis(v); setValue?.("isCrisis", (v === "true") as never, { shouldValidate: true }) }} value={crisis}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder={t.common.select} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="true">{t.common.yes}</SelectItem>
                                <SelectItem value="false">{t.common.no}</SelectItem>
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
    const { t } = useLang()
    const [selected, setSelected] = useState<Set<string>>(new Set())
    const [distress, setDistress] = useState("")
    const [impact,   setImpact]   = useState("")

    const SYMPTOMS: { key: string; label: string }[] = [
        { key: "sad_or_hopeless",            label: t.symptomsStep.sadOrHopeless },
        { key: "anxiety_or_panic",           label: t.symptomsStep.anxietyOrPanic },
        { key: "difficulty_sleeping",        label: t.symptomsStep.difficultySleeping },
        { key: "hearing_or_seeing_things",   label: t.symptomsStep.hearingOrSeeing },
        { key: "thoughts_of_self_harm",      label: t.symptomsStep.selfHarm },
        { key: "thoughts_of_harming_others", label: t.symptomsStep.harmingOthers },
        { key: "difficulty_eating",          label: t.symptomsStep.difficultyEating },
        { key: "feeling_disconnected",       label: t.symptomsStep.feelingDisconnected },
        { key: "overwhelming_anger",         label: t.symptomsStep.overwhelmingAnger },
        { key: "substance_use",              label: t.symptomsStep.substanceUse },
    ]

    const toggleSymptom = (key: string) => {
        const next = new Set(selected)
        if (next.has(key)) next.delete(key); else next.add(key)
        setSelected(next)
        setValue?.("symptoms", Array.from(next).join(",") as never, { shouldValidate: true })
    }

    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">{t.symptomsStep.title}</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <div className="space-y-2">
                    <Label>{t.symptomsStep.symptomsLabel}</Label>
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
                    <Label>{t.symptomsStep.distressLevel}</Label>
                    <Select onValueChange={(v) => { setDistress(v); setValue?.("distressLevel", Number(v) as never, { shouldValidate: true }) }} value={distress}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder={t.symptomsStep.distressPlaceholder} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>{t.symptomsStep.distressLevel}</SelectLabel>
                                {[1, 2, 3, 4, 5].map(n => (
                                    <SelectItem key={n} value={String(n)}>{n}</SelectItem>
                                ))}
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.distressLevel && <p className="text-sm text-destructive">{errors.distressLevel.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>{t.symptomsStep.dailyImpact}</Label>
                    <Select onValueChange={(v) => { setImpact(v); setValue?.("dailyImpact", v as never, { shouldValidate: true }) }} value={impact}>
                        <SelectTrigger className="w-[260px]">
                            <SelectValue placeholder={t.symptomsStep.impactPlaceholder} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="not_at_all">{t.symptomsStep.impactNotAtAll}</SelectItem>
                                <SelectItem value="a_little">{t.symptomsStep.impactALittle}</SelectItem>
                                <SelectItem value="a_lot">{t.symptomsStep.impactALot}</SelectItem>
                                <SelectItem value="cannot_function">{t.symptomsStep.impactCantFunction}</SelectItem>
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

const BackgroundInfoStep = ({ register, errors, setValue }: StepProps) => {
    const { t } = useLang()
    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">{t.background.title}</CardTitle>
            <div className="grid grid-cols-1 gap-5">
                <BoolSelect label={t.background.currentTreatment}   field="currentTreatment"   setValue={setValue} errors={errors} />
                <FormField  id="currentMedications" label={t.background.currentMedications} register={register} errors={errors} />
                <FormField  id="otherConditions"    label={t.background.otherConditions}    register={register} errors={errors} />
                <FormField  id="allergies"          label={t.background.allergies}          register={register} errors={errors} />
                <BoolSelect label={t.background.previousMhHospital} field="previousMhHospital" setValue={setValue} errors={errors} />
            </div>
        </div>
    )
}

// ── Step 5 — Cultural Needs ────────────────────────────────────────────

const PersonalNeedsInfoStep = ({ register, errors, setValue }: StepProps) => {
    const { t } = useLang()
    const [clinGender,   setClinicianGender]   = useState("")
    const [familyInvolv, setFamilyInvolvement] = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-xl">{t.cultural.title}</CardTitle>
            <div className="grid grid-cols-1 gap-5">

                <FormField
                    id="culturalNotes"
                    label={t.cultural.culturalNotes}
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label>{t.cultural.clinicianGenderPreference}</Label>
                    <Select onValueChange={(v) => { setClinicianGender(v); setValue?.("clinicianGenderPreference", v as never, { shouldValidate: true }) }} value={clinGender}>
                        <SelectTrigger className="w-[220px]">
                            <SelectValue placeholder={t.cultural.clinicianGenderPlaceholder} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>{t.cultural.clinicianGenderPreference}</SelectLabel>
                                <SelectItem value="male">{t.cultural.clinicianMale}</SelectItem>
                                <SelectItem value="female">{t.cultural.clinicianFemale}</SelectItem>
                                <SelectItem value="no_preference">{t.cultural.clinicianNoPreference}</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.clinicianGenderPreference && <p className="text-sm text-destructive">{errors.clinicianGenderPreference.message}</p>}
                </div>

                <div className="space-y-2">
                    <Label>{t.cultural.familyInvolvement}</Label>
                    <Select onValueChange={(v) => { setFamilyInvolvement(v); setValue?.("familyInvolvement", v as never, { shouldValidate: true }) }} value={familyInvolv}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder={t.common.select} />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="yes">{t.cultural.familyYes}</SelectItem>
                                <SelectItem value="no">{t.cultural.familyNo}</SelectItem>
                                <SelectItem value="not_now">{t.cultural.familyNotNow}</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    {errors.familyInvolvement && <p className="text-sm text-destructive">{errors.familyInvolvement.message}</p>}
                </div>

                <FormField
                    id="additionalNotes"
                    label={t.cultural.additionalNotes}
                    register={register}
                    errors={errors}
                />

            </div>
        </div>
    )
}

export { PersonalInfoStep, ReasonInfoStep, FeelingInfoStep, BackgroundInfoStep, PersonalNeedsInfoStep }
