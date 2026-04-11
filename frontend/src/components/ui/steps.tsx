import { CardTitle } from "./card"
import FormField from "./form-field";

import type { StepFormData } from "@/types";
import type { useForm } from "react-hook-form";
import { Label } from "./label";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "./select";
import { Switch } from "./switch";
import { Field, FieldContent, FieldDescription, FieldGroup, FieldLabel, FieldTitle } from "./field";
import { useState } from "react";
import { Icon } from "lucide-react";

interface StepProps {
    register: ReturnType<typeof useForm<StepFormData>>["register"];
    errors: Record<string, { message?: string }>;
    setValue?: ReturnType<typeof useForm<StepFormData>>["setValue"];
}

const PersonalInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [gender, setGender] = useState("")
    const [language, setLanguage] = useState("")

    return (
        <div className="space-y-5">
            <CardTitle className="text-x1">About You</CardTitle>

            <div className="grid grid-cols-1 gap-5">

                <FormField
                    id="firstName"
                    label="First Name"
                    register={register}
                    errors={errors}
                />
                <FormField
                    id="lastName"
                    label="Last Name"
                    register={register}
                    errors={errors}
                />



                <FormField
                    id="age"
                    label="Age"
                    register={register}
                    errors={errors}
                    type="number"
                />



                <div className="space-y-2">
                    <Label htmlFor="gender">Select Gender</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("gender", value as Extract<StepFormData, { gender: string }>["gender"], { shouldValidate: true });
                        setGender(value)
                    }} value={gender}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select Gender" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Gender Options</SelectLabel>
                                <SelectItem value="Male">Male</SelectItem>
                                <SelectItem value="Female">Female</SelectItem>
                                <SelectItem value="Other">Other</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.gender && (
                        <p>{errors.gender.message}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="language">Preferred Language</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("language", value as Extract<StepFormData, { language: string }>["language"], { shouldValidate: true });
                        setLanguage(value)
                    }} value={language}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select Language" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Languages</SelectLabel>
                                <SelectItem value="EN">English</SelectItem>
                                <SelectItem value="ES">Español</SelectItem>
                                <SelectItem value="AR">عربي</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.language && (
                        <p>{errors.language.message}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="interpreterNeeded">Interpreter Required</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("interpreterNeeded", value as Extract<StepFormData, { interpreterNeeded: string }>["interpreterNeeded"], { shouldValidate: true });
                        setLanguage(value)
                    }} value={language}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Interpreter Needed?" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Interpreter Needed?</SelectLabel>
                                <SelectItem value="Yes">Yes</SelectItem>
                                <SelectItem value="No">No</SelectItem>

                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.interpreterNeeded && (
                        <p>{errors.interpreterNeeded.message}</p>
                    )}
                </div>




                {/* <FormField
                    id="interpreterNeeded"
                    label="Do you need an interpreter (Yes/No)"
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label htmlFor="interpreterNeeded">Do you require an Interpreter</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("interpreterNeeded", value as Extract<StepFormData, { interpreterNeeded: string }>["interpreterNeeded"]);
                    }}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Yes/No" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Interpreter Required?</SelectLabel>
                                <SelectItem value="true">Yes</SelectItem>
                                <SelectItem value="false">No</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.interpreterNeeded && (
                        <p>{errors.interpreterNeeded.message}</p>
                    )}
                </div> */}
                {/* 
                <div>
                    <FieldGroup className="w-full max-w-sm">
                        <FieldLabel htmlFor="switch-share">
                            <Field orientation="horizontal">
                                <FieldContent>
                                    <FieldTitle>Enable for Interpreter</FieldTitle>
                                    <FieldDescription>
                                        Enable this switch if you would like an interpreter during your consultation
                                    </FieldDescription>
                                </FieldContent>
                                <Switch id="switch-share" />
                            </Field>
                        </FieldLabel>
                    </FieldGroup>
                </div> */}
            </div>
        </div>
    )
}
const ReasonInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [started, setStarted] = useState("")
    const [hadBefore, setHadBefore] = useState("")
    const [emergency, setEmergency] = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-x1">What Brought You Here Today?</CardTitle>

            <div className="grid grid-cols-1 gap-5">
                <FormField
                    id="ownWords"
                    label="In your own words please describe what is the concern"
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label htmlFor="started">When did you start feeling this way?</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("started", value as Extract<StepFormData, { started: string }>["started"], { shouldValidate: true });
                        setStarted(value)
                    }} value={started}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="Today">Today</SelectItem>
                                <SelectItem value="This Week">This Week</SelectItem>
                                <SelectItem value="This Month">This Month</SelectItem>
                                <SelectItem value="Longer than a Month">Longer than a Month</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.started && (
                        <p>{errors.started.message}</p>
                    )}
                </div>
                <div className="space-y-2">
                    <Label htmlFor="hadBefore">Have you felt this way before?</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("hadBefore", value as Extract<StepFormData, { hadBefore: string }>["hadBefore"], { shouldValidate: true });
                        setHadBefore(value)
                    }} value={started}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="Yes">Yes</SelectItem>
                                <SelectItem value="No">No</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.hadBefore && (
                        <p>{errors.hadBefore.message}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="emergency">Have you felt this way before?</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("emergency", value as Extract<StepFormData, { emergency: string }>["emergency"], { shouldValidate: true });
                        setEmergency(value)
                    }} value={started}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>How serious would you rate this concern</SelectLabel>
                                <SelectItem value="No">0-3</SelectItem>
                                <SelectItem value="No">4-7</SelectItem>
                                <SelectItem value="Yes">8-10</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.emergency && (
                        <p>{errors.emergency.message}</p>
                    )}
                </div>
            </div>
        </div>
    )
}
const FeelingInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [feeling, setFeeling] = useState("")
    const [affectOnLife, setAffectOnLife] = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-x1">What Brought You Here Today?</CardTitle>

            <div className="grid grid-cols-1 gap-5">
                <div className="space-y-2">
                    <Label htmlFor="feeling">How are you feeling on a scale of 1-5</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("feeling", value as Extract<StepFormData, { feeling: string }>["feeling"], { shouldValidate: true });
                        setFeeling(value)
                    }} value={feeling}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="1">1</SelectItem>
                                <SelectItem value="2">2</SelectItem>
                                <SelectItem value="3">3</SelectItem>
                                <SelectItem value="4">4</SelectItem>
                                <SelectItem value="5">5</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.feeling && (
                        <p>{errors.feeling.message}</p>
                    )}
                </div>
                <FormField
                    id="checklist"
                    label="Please write down the experiences you have been feeling lately, seperated by commas. (e.g. Happy, Troubles, Stressed, etc...) "
                    register={register}
                    errors={errors}
                />
                <div className="space-y-2">
                    <Label htmlFor="affectOnLife">How does this affect your daily life</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("affectOnLife", value as Extract<StepFormData, { affectOnLife: string }>["affectOnLife"], { shouldValidate: true });
                        setAffectOnLife(value)
                    }} value={affectOnLife}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="not at all">not at all</SelectItem>
                                <SelectItem value="a little">a little</SelectItem>
                                <SelectItem value="a lot">a lot</SelectItem>
                                <SelectItem value="I can't function">4</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.affectOnLife && (
                        <p>{errors.affectOnLife.message}</p>
                    )}
                </div>
            </div>
        </div>
    )
}
const BackgroundInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [therapist, setTherapist] = useState("")
    const [hospitalVisitBefore, setHospitalVisitBefore] = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-x1">Your Background</CardTitle>

            <div className="grid grid-cols-1 gap-5">
                <div className="space-y-2">
                    <Label htmlFor="therapist">Have you ever been to a therapist?</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("therapist", value as Extract<StepFormData, { therapist: string }>["therapist"], { shouldValidate: true });
                        setTherapist(value)
                    }} value={therapist}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="true">Yes</SelectItem>
                                <SelectItem value="false">No</SelectItem>

                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.therapist && (
                        <p>{errors.therapist.message}</p>
                    )}
                </div>

                <FormField
                    id="medicationEnquiry"
                    label="Are you taking mental health medications?"
                    register={register}
                    errors={errors}
                />

                <FormField
                    id="additionalMedicationEnquiry"
                    label="Any other medical conditions? "
                    register={register}
                    errors={errors}
                />

                <FormField
                    id="allergiesEnquiry"
                    label="Any allergies? "
                    register={register}
                    errors={errors}
                />

                <div className="space-y-2">
                    <Label htmlFor="hospitalVisitBefore">Have you ever been to the hospital due to this?</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("hospitalVisitBefore", value as Extract<StepFormData, { hospitalVisitBefore: string }>["hospitalVisitBefore"], { shouldValidate: true });
                        setHospitalVisitBefore(value)
                    }} value={hospitalVisitBefore}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="Yes">Yes</SelectItem>
                                <SelectItem value="No">No</SelectItem>

                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.hospitalVisitBefore && (
                        <p>{errors.hospitalVisitBefore.message}</p>
                    )}
                </div>
            </div>
        </div>
    )
}
const PersonalNeedsInfoStep = ({ register, errors, setValue }: StepProps) => {
    const [preferredClinicianGender, setPreferredClinicianGender] = useState("")
    const [familyAssistanceRequired, setFamilyAssistanceRequired] = useState("")

    return (
        <div className="space-y-4">
            <CardTitle className="text-x1">Your Background</CardTitle>

            <FormField
                    id="personalFactors"
                    label="Are there any religious, cultural, or personal factors you'd like the care team to know?"
                    register={register}
                    errors={errors}
                />

            <div className="grid grid-cols-1 gap-5">
                <div className="space-y-2">
                    <Label htmlFor="preferredClinicianGender">Please select your prefered clinician gender</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("preferredClinicianGender", value as Extract<StepFormData, { preferredClinicianGender: string }>["preferredClinicianGender"], { shouldValidate: true });
                        setPreferredClinicianGender(value)
                    }} value={preferredClinicianGender}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="Male">Male</SelectItem>
                                <SelectItem value="Female">Female</SelectItem>

                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.preferredClinicianGender && (
                        <p>{errors.preferredClinicianGender.message}</p>
                    )}
                </div>


                <div className="space-y-2">
                    <Label htmlFor="familyAssistanceRequired">Would you like a family member or support person(s) involved in your care?</Label>
                    <Select onValueChange={(value) => {
                        setValue?.("familyAssistanceRequired", value as Extract<StepFormData, { familyAssistanceRequired: string }>["familyAssistanceRequired"], { shouldValidate: true });
                        setFamilyAssistanceRequired(value)
                    }} value={familyAssistanceRequired}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select One" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>Please select one from the following</SelectLabel>
                                <SelectItem value="Yes">Yes</SelectItem>
                                <SelectItem value="No">No</SelectItem>
                                <SelectItem value="Not Yet">Not Yet</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>

                    {errors.familyAssistanceRequired && (
                        <p>{errors.familyAssistanceRequired.message}</p>
                    )}
                </div>
                <FormField
                    id="additionalInfo"
                    label="Any additional information you would like to provide? "
                    register={register}
                    errors={errors}
                />
            </div>
        </div>
    )
}

export { PersonalInfoStep, ReasonInfoStep, FeelingInfoStep, BackgroundInfoStep, PersonalNeedsInfoStep };