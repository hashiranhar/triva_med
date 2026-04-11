import type { AllFormFields, StepFormData } from "@/types";
import { Input } from "./input";
import type { useForm } from "react-hook-form";
import { Label } from "./label";



const FormField = ({
    id,
    label,
    register,
    errors,
    type = "",
    maxLength
}: {
    id: keyof AllFormFields;
    label: string;
    register: ReturnType<typeof useForm<StepFormData>>["register"];
    errors?: Record<string, {message?: string}>;
    type?: string,
    maxLength?: number;
}) => {
    return(
        <div>
            <Label htmlFor={id}>{label}</Label>
            <Input id={id} type={type} maxLength={maxLength} {...register(id)}/>
            {errors[id] && (
                <p className="text-sm text-destructive">{errors[id]?.message}</p>
            )}
        </div>
    )
}

export default FormField;