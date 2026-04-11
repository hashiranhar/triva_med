import type { Step } from "@/types";
import { Check } from "lucide-react";

const ProgressSteps = ({
    currentStep,
    steps
}: {
    currentStep: number;
    steps: Step[];
}) => {
    return <div className="flex justify-between items-center">
        {steps.map((step, index) => {
            const Icon = step.icon;
            const isCompleted = index < currentStep;
            const isCurrent = index === currentStep;

            return <div key={step.id} className="flex items-center flex-1">
                <div className="flex flex-col items-center">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${isCompleted
                            ? "bg-purple-900 text-primary-foreground"
                            : isCurrent
                                ? "bg-indigo-300 text-primary-foreground"
                                : "bg-purple-200 text-purple-600"
                        }`}>
                        {isCompleted ? (
                            <Check className="w-5 h-5" />
                        ) : (
                            <Icon className="w-5 h-5" />
                        )}
                    </div>
                    <span className="text-xs mt-2 font-medium">{step.name}</span>
                </div>

                {index < steps.length - 1 && (
                    <div
                        className={`flex-1 h-[3px] mx-2 transition-colours ${
                            isCompleted ? "bg-purple-600" : "bg-pink-200"
                        }`} 
                    />


                )}

            </div>

        })}


    </div>;
}

export default ProgressSteps