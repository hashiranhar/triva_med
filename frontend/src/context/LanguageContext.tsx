import { createContext, useContext, useState, type ReactNode } from "react"
import { translations, type Language, type T } from "@/i18n"

interface LanguageContextValue {
    lang: Language
    setLang: (l: Language) => void
    t: T
}

const LanguageContext = createContext<LanguageContextValue>({
    lang: "en",
    setLang: () => {},
    t: translations.en,
})

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [lang, setLang] = useState<Language>("en")
    return (
        <LanguageContext.Provider value={{ lang, setLang, t: translations[lang] }}>
            {children}
        </LanguageContext.Provider>
    )
}

export function useLang(): LanguageContextValue {
    return useContext(LanguageContext)
}
