import {z} from 'zod'

export const personalInfoSchema = z.object({
    firstName: z.string().min(1, "First name is required"),
    lastName: z.string().min(1, "Last name is required"),
    age: z.coerce.number().min(1, "Age has to be > 0"),
    gender: z.enum(["Male", "Female", "Other"]),
    language: z.enum(["EN","ES","AR"]),
    interpreterNeeded: z.enum(["Yes","No"]),
}) 

export const reasonInfoSchema = z.object({
    ownWords: z.string().min(1, "Please provide a response, or leave N/A"),
    started: z.enum(["Today","This Week","This Month", "Longer than a Month"]),
    hadBefore: z.enum(["Yes","No"]),
    emergency: z.enum(["Yes","No"])
}) 

export const feelingInfoSchema = z.object({
    feeling: z.enum(["1","2","3","4","5"]),
    checklist: z.string().min(1, "Please provide a response, or leave N/A"),
    affectOnLife: z.enum(["not at all","a little","a lot", "I can't function"])
}) 

export const backgroundInfoSchema = z.object({
    therapist: z.coerce.boolean(),
    medicationEnquiry: z.string(),
    additionalMedicationEnquiry: z.string(),
    allergiesEnquiry: z.string(),
    hospitalVisitBefore: z.enum(["Yes","No"])
}) 

export const personalNeedsInfoSchema = z.object({
    personalFactors: z.string(),
    additionalInfo: z.string(),
    preferredClinicianGender: z.enum(["Male","Female"]),
    familyAssistanceRequired: z.enum(["Yes","No","Not Yet"])
}) 

export type PersonalInfo = z.infer<typeof personalInfoSchema>;
export type ReasonInfo = z.infer<typeof reasonInfoSchema>;
export type FeelingInfo = z.infer<typeof feelingInfoSchema>;
export type BackgroundInfo = z.infer<typeof backgroundInfoSchema>;
export type PersonalNeedsInfo = z.infer<typeof personalNeedsInfoSchema>;

export type StepFormData = PersonalInfo | ReasonInfo | FeelingInfo | BackgroundInfo | PersonalNeedsInfo;

export type AllFormFields = PersonalInfo & ReasonInfo & FeelingInfo & BackgroundInfo & PersonalNeedsInfo;

export interface Step {
    id: string;
    name: string;
    icon: React.ComponentType<{ className? : string}>;
}