import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import type { AllFormFields, StepFormData } from "@/types"
import { useMultiStepForm } from "@/hooks/use-multi-step-form"
import { useEffect } from "react"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import ProgressSteps from "./progress-steps"
import {
    PersonalInfoStep,
    ReasonInfoStep,
    FeelingInfoStep,
    BackgroundInfoStep,
    PersonalNeedsInfoStep,
} from "./steps"
import { Button } from "./button"
import { ChevronLeft, ChevronRight } from "lucide-react"

const MultiStepForm = () => {
    const {
        currentStep,
        formData,
        isFirstStep,
        isLastStep,
        isSubmitted,
        isSubmitting,
        submitError,
        setSubmitError,
        steps,
        goToNextStep,
        submitForm,
        getCurrentStepSchema,
        goToPreviousStep,
        updateFormData,
    } = useMultiStepForm()

    const {
        register,
        handleSubmit,
        formState: { errors },
        trigger,
        setValue,
        reset,
    } = useForm<StepFormData>({
        resolver:      zodResolver(getCurrentStepSchema()),
        mode:          "onChange",
        defaultValues: formData,
    })

    useEffect(() => { reset(formData) }, [currentStep, formData, reset])

    const onNext = async (data: StepFormData) => {
        const isValid = await trigger()
        if (!isValid) return

        const updatedData = { ...formData, ...data } as Partial<AllFormFields>
        updateFormData(updatedData)

        if (isLastStep) {
            try {
                await submitForm(updatedData)
            } catch (error) {
                setSubmitError(error instanceof Error ? error.message : "Submission failed.")
            }
        } else {
            goToNextStep()
        }
    }

    if (isSubmitted) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50 px-8">
                <Card className="w-full max-w-lg text-center">
                    <CardContent className="space-y-3 py-12">
                        <h2 className="text-2xl font-semibold">Thank you</h2>
                        <p className="text-gray-600">
                            Your information has been received. A member of our team will be with you shortly.
                        </p>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 pl-40 pr-40 pt-20 pb-20">
            <Card className="w-full max-w-2xl">
                <CardHeader>
                    <ProgressSteps currentStep={currentStep} steps={steps} />
                </CardHeader>
                <CardContent className="space-y-6">
                    {currentStep === 0 && <PersonalInfoStep    register={register} errors={errors} setValue={setValue} />}
                    {currentStep === 1 && <ReasonInfoStep      register={register} errors={errors} setValue={setValue} />}
                    {currentStep === 2 && <FeelingInfoStep     register={register} errors={errors} setValue={setValue} />}
                    {currentStep === 3 && <BackgroundInfoStep  register={register} errors={errors} setValue={setValue} />}
                    {currentStep === 4 && <PersonalNeedsInfoStep register={register} errors={errors} setValue={setValue} />}

                    {submitError && (
                        <p className="text-sm text-destructive">{submitError}</p>
                    )}

                    <div className="flex justify-between pt-4">
                        <Button type="button" variant="outline" onClick={goToPreviousStep} disabled={isFirstStep}>
                            <ChevronLeft className="w-4 h-4 mr-1" />
                            Previous
                        </Button>
                        <Button type="button" variant="outline" onClick={handleSubmit(onNext)} disabled={isSubmitting}>
                            {isSubmitting ? "Submitting…" : isLastStep ? "Submit" : "Next"}
                            {!isLastStep && !isSubmitting && <ChevronRight className="w-4 h-4 ml-1" />}
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default MultiStepForm
