import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import type { Step, StepFormData } from "@/types";
import { useMultiStepForm } from "@/hooks/use-multi-step-form";
import { useEffect } from "react";
import {
    Card,
    CardContent,
    CardHeader,
} from "@/components/ui/card"
import ProgressSteps from "./progress-steps";
import { PersonalInfoStep, ReasonInfoStep, FeelingInfoStep, BackgroundInfoStep, PersonalNeedsInfoStep } from "./steps";
import { Button } from "./button";
import { ChevronLeft, ChevronRight } from "lucide-react";


const MultiStepForm = () => {

    const {
        currentStep,
        formData,
        isFirstStep,
        isLastStep,
        // isSubmitted,
        steps,
        goToNextStep,
        submitForm,
        // resetForm,
        getCurrentStepSchema,
        goToPreviousStep,
        updateFormData
    } = useMultiStepForm();

    const {
        register,
        handleSubmit,
        formState: { errors },
        trigger,
        setValue,
        reset,
    } = useForm<StepFormData>({
        resolver: zodResolver(getCurrentStepSchema()),
        mode: "onChange",
        defaultValues: formData
    });

    useEffect(() => { reset(formData) }, [currentStep, formData, reset])

    const onNext = async (data: StepFormData) => {
        const isValid = await trigger();
        if (!isValid) return;

        console.log(data, formData);
        const updatedData = {...formData, ...data};
        updateFormData(updatedData)

        if (isLastStep){
            try {
                submitForm(updatedData)
            } catch (error) {
                console.error("submission failed", error)
            }
        } else {
            goToNextStep();
        }

    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 pl-40 pr-40 pt-20 pb-20">

            <Card className="w-full max-w-2x1">
                <CardHeader>
                    <ProgressSteps currentStep={currentStep} steps={steps} />
                </CardHeader>
                <CardContent className="space-y-6">
                    {currentStep === 0 && (<PersonalInfoStep register={register} errors={errors} setValue={setValue}/>)}
                    {currentStep === 1 && (<ReasonInfoStep register={register} errors={errors} setValue={setValue}/>)}
                    {currentStep === 2 && (<FeelingInfoStep register={register} errors={errors} setValue={setValue}/>)}
                    {currentStep === 3 && (<BackgroundInfoStep register={register} errors={errors} setValue={setValue}/>)}
                    {currentStep === 4 && (<PersonalNeedsInfoStep register={register} errors={errors} setValue={setValue}/>)}

                    <div className="flex justify-between pt-4">
                        <Button type="button" variant="outline" onClick={goToPreviousStep} disabled={isFirstStep}>
                            <ChevronLeft className="w-4 h-4 mr-1" />
                            Previous
                        </Button>
                        <Button type="button" onClick={handleSubmit(onNext)} variant="outline">
                            {isLastStep ? "Submit" : "Next"}
                            {!isLastStep && <ChevronRight className="w-4 h-4 ml-1" />}                                                
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );


}

export default MultiStepForm