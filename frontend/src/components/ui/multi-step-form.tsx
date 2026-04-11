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
import { useLang } from "@/context/LanguageContext"
import { type Language } from "@/i18n"
import {
    Select, SelectContent, SelectItem,
    SelectTrigger, SelectValue,
} from "@/components/ui/select"

const LANGUAGE_OPTIONS: { value: Language; label: string }[] = [
    { value: "en", label: "🇬🇧 English" },
    { value: "es", label: "🇪🇸 Español" },
    { value: "ar", label: "🇸🇦 عربي" },
]

const MultiStepForm = () => {
    const { lang, setLang, t } = useLang()

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

    // Map step ids → translated names for the progress bar
    const stepIdToName: Record<string, string> = {
        personal:   t.steps.personal,
        concern:    t.steps.concern,
        symptoms:   t.steps.symptoms,
        background: t.steps.background,
        cultural:   t.steps.cultural,
    }
    const translatedSteps = steps.map(s => ({ ...s, name: stepIdToName[s.id] ?? s.name }))

    // Language selector — fixed top-right
    const languageSelector = (
        <div className="fixed top-4 right-4 z-50 flex items-center gap-2">
            <span className="text-sm text-gray-500 font-medium">{t.language}</span>
            <Select value={lang} onValueChange={(v) => setLang(v as Language)}>
                <SelectTrigger className="w-[130px] bg-white shadow-sm">
                    <SelectValue />
                </SelectTrigger>
                <SelectContent>
                    {LANGUAGE_OPTIONS.map(o => (
                        <SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    )

    if (isSubmitted) {
        return (
            <>
                {languageSelector}
                <div
                    className="min-h-screen flex items-center justify-center bg-gray-50 px-8"
                    dir={t.dir}
                >
                    <Card className="w-full max-w-lg text-center">
                        <CardContent className="space-y-3 py-12">
                            <h2 className="text-2xl font-semibold">{t.success.title}</h2>
                            <p className="text-gray-600">{t.success.message}</p>
                        </CardContent>
                    </Card>
                </div>
            </>
        )
    }

    return (
        <>
            {languageSelector}
            <div
                className="min-h-screen flex items-center justify-center bg-gray-50 pl-40 pr-40 pt-20 pb-20"
                dir={t.dir}
            >
                <Card className="w-full max-w-2xl">
                    <CardHeader>
                        <ProgressSteps currentStep={currentStep} steps={translatedSteps} />
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
                            <Button
                                type="button"
                                variant="outline"
                                onClick={goToPreviousStep}
                                disabled={isFirstStep}
                            >
                                {t.dir === "rtl"
                                    ? <ChevronRight className="w-4 h-4 mr-1" />
                                    : <ChevronLeft  className="w-4 h-4 mr-1" />}
                                {t.common.previous}
                            </Button>
                            <Button
                                type="button"
                                variant="outline"
                                onClick={handleSubmit(onNext)}
                                disabled={isSubmitting}
                            >
                                {isSubmitting
                                    ? t.common.submitting
                                    : isLastStep
                                        ? t.common.submit
                                        : t.common.next}
                                {!isLastStep && !isSubmitting && (
                                    t.dir === "rtl"
                                        ? <ChevronLeft  className="w-4 h-4 ml-1" />
                                        : <ChevronRight className="w-4 h-4 ml-1" />
                                )}
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </>
    )
}

export default MultiStepForm
