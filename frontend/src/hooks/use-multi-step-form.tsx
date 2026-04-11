import { personalInfoSchema, reasonInfoSchema, feelingInfoSchema, backgroundInfoSchema, personalNeedsInfoSchema, type Step, type StepFormData } from "@/types";
import { Church, CircleQuestionMark, ClipboardClock, SmilePlus, User } from "lucide-react";
import { useState } from "react";

const stepSchemas = [
    personalInfoSchema,
    reasonInfoSchema,
    feelingInfoSchema,
    backgroundInfoSchema,
    personalNeedsInfoSchema
]

export const steps: Step[] = [
    {id: "personal", name: "Personal Info", icon: User},
    {id: "why", name: "Reason Info", icon: CircleQuestionMark},
    {id: "feeling", name: "Feeling Info", icon: SmilePlus},
    {id: "background", name: "Background Info", icon: ClipboardClock},
    {id: "culture", name: "Personal Needs Info", icon: Church},
]

export function useMultiStepForm()  {

    const [ currentStep, setCurrentStep ] = useState(0);
    const [ formData, setFormData ] = useState<Partial<StepFormData>>({});
    const [ isSubmitted, setIsSubmitted ] = useState(false);

    const isFirstStep = currentStep === 0 
    const isLastStep = currentStep === steps.length - 1;

    const getCurrentStepSchema = () => stepSchemas[currentStep];

    const goToNextStep = () => {
        if (!isLastStep) setCurrentStep((prev) => prev +1 )
    }

    const goToPreviousStep = () => {
        if(!isFirstStep) setCurrentStep((prev) => prev -1 )
    }

    const updateFormData = (newData: Partial<StepFormData>) => {
        setFormData((prev) => ({...prev, ...newData}))
    }

    const submitForm = (data: StepFormData) => {
        console.log("data is =: ", data)
        setIsSubmitted(true)
    }

    const resetForm = () => {
        setFormData({});
        setCurrentStep(0);
        setIsSubmitted(false);
    }

    return{
        currentStep,
        formData,
        isFirstStep,
        isLastStep,
        isSubmitted,
        steps,

        goToNextStep,
        getCurrentStepSchema,
        goToPreviousStep,
        updateFormData,
        submitForm,
        resetForm
    }

}