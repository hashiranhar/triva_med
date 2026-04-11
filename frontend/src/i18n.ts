export type Language = "en" | "es" | "ar"

export interface T {
    language: string
    dir: "ltr" | "rtl"

    steps: {
        personal:   string
        concern:    string
        symptoms:   string
        background: string
        cultural:   string
    }

    common: {
        yes:        string
        no:         string
        select:     string
        previous:   string
        next:       string
        submit:     string
        submitting: string
    }

    success: {
        title:   string
        message: string
    }

    aboutYou: {
        title:                string
        firstName:            string
        lastName:             string
        dateOfBirth:          string
        gender:               string
        genderPlaceholder:    string
        genderMale:           string
        genderFemale:         string
        genderNonBinary:      string
        genderPreferNotToSay: string
        preferredLanguage:    string
        languagePlaceholder:  string
        interpreterNeeded:    string
    }

    yourConcern: {
        title:           string
        rawConcernText:  string
        onset:           string
        onsetPlaceholder: string
        onsetToday:      string
        onsetThisWeek:   string
        onsetThisMonth:  string
        onsetLonger:     string
        previousEpisode: string
        isCrisis:        string
    }

    symptomsStep: {
        title:               string
        symptomsLabel:       string
        sadOrHopeless:       string
        anxietyOrPanic:      string
        difficultySleeping:  string
        hearingOrSeeing:     string
        selfHarm:            string
        harmingOthers:       string
        difficultyEating:    string
        feelingDisconnected: string
        overwhelmingAnger:   string
        substanceUse:        string
        distressLevel:       string
        distressPlaceholder: string
        dailyImpact:         string
        impactPlaceholder:   string
        impactNotAtAll:      string
        impactALittle:       string
        impactALot:          string
        impactCantFunction:  string
    }

    background: {
        title:               string
        currentTreatment:    string
        currentMedications:  string
        otherConditions:     string
        allergies:           string
        previousMhHospital:  string
    }

    cultural: {
        title:                         string
        culturalNotes:                 string
        clinicianGenderPreference:     string
        clinicianGenderPlaceholder:    string
        clinicianMale:                 string
        clinicianFemale:               string
        clinicianNoPreference:         string
        familyInvolvement:             string
        familyYes:                     string
        familyNo:                      string
        familyNotNow:                  string
        additionalNotes:               string
    }
}

const en: T = {
    language: "Language",
    dir: "ltr",

    steps: {
        personal:   "About You",
        concern:    "Your Concern",
        symptoms:   "Symptoms",
        background: "Background",
        cultural:   "Cultural Needs",
    },

    common: {
        yes:        "Yes",
        no:         "No",
        select:     "Select…",
        previous:   "Previous",
        next:       "Next",
        submit:     "Submit",
        submitting: "Submitting…",
    },

    success: {
        title:   "Thank you",
        message: "Your information has been received. A member of our team will be with you shortly.",
    },

    aboutYou: {
        title:                "About You",
        firstName:            "First Name",
        lastName:             "Last Name",
        dateOfBirth:          "Date of Birth",
        gender:               "Gender",
        genderPlaceholder:    "Select gender",
        genderMale:           "Male",
        genderFemale:         "Female",
        genderNonBinary:      "Non-binary",
        genderPreferNotToSay: "Prefer not to say",
        preferredLanguage:    "Preferred Language",
        languagePlaceholder:  "Select language",
        interpreterNeeded:    "Do you need an interpreter?",
    },

    yourConcern: {
        title:            "Your Concern",
        rawConcernText:   "In your own words, what has brought you here today?",
        onset:            "How long have you been feeling this way?",
        onsetPlaceholder: "Select…",
        onsetToday:       "Today",
        onsetThisWeek:    "This week",
        onsetThisMonth:   "This month",
        onsetLonger:      "Longer than a month",
        previousEpisode:  "Have you felt this way before?",
        isCrisis:         "Are you in crisis right now?",
    },

    symptomsStep: {
        title:               "How Are You Feeling?",
        symptomsLabel:       "Which of the following have you been experiencing? (select all that apply)",
        sadOrHopeless:       "Sad or hopeless",
        anxietyOrPanic:      "Anxiety / panic",
        difficultySleeping:  "Difficulty sleeping",
        hearingOrSeeing:     "Hearing / seeing things",
        selfHarm:            "Thoughts of self-harm",
        harmingOthers:       "Thoughts of harming others",
        difficultyEating:    "Difficulty eating",
        feelingDisconnected: "Feeling disconnected",
        overwhelmingAnger:   "Overwhelming anger",
        substanceUse:        "Substance use concerns",
        distressLevel:       "Distress level (1 = low, 5 = severe)",
        distressPlaceholder: "Select 1–5",
        dailyImpact:         "How much does this affect your daily life?",
        impactPlaceholder:   "Select…",
        impactNotAtAll:      "Not at all",
        impactALittle:       "A little",
        impactALot:          "A lot",
        impactCantFunction:  "I cannot function",
    },

    background: {
        title:              "Your Background",
        currentTreatment:   "Are you currently seeing a therapist or mental health professional?",
        currentMedications: "Mental health medications (comma-separated, or leave blank)",
        otherConditions:    "Other medical conditions (comma-separated, or leave blank)",
        allergies:          "Allergies (comma-separated, or leave blank)",
        previousMhHospital: "Have you ever been hospitalised for a mental health reason?",
    },

    cultural: {
        title:                      "Cultural & Personal Needs",
        culturalNotes:              "Any religious, cultural, or personal factors you'd like the care team to know? (optional)",
        clinicianGenderPreference:  "Preferred clinician gender",
        clinicianGenderPlaceholder: "Select…",
        clinicianMale:              "Male",
        clinicianFemale:            "Female",
        clinicianNoPreference:      "No preference",
        familyInvolvement:          "Would you like a family member or support person involved in your care?",
        familyYes:                  "Yes",
        familyNo:                   "No",
        familyNotNow:               "Not right now",
        additionalNotes:            "Anything else you'd like to share? (optional)",
    },
}

const es: T = {
    language: "Idioma",
    dir: "ltr",

    steps: {
        personal:   "Sobre Ti",
        concern:    "Tu Preocupación",
        symptoms:   "Síntomas",
        background: "Historial",
        cultural:   "Necesidades Culturales",
    },

    common: {
        yes:        "Sí",
        no:         "No",
        select:     "Seleccionar…",
        previous:   "Anterior",
        next:       "Siguiente",
        submit:     "Enviar",
        submitting: "Enviando…",
    },

    success: {
        title:   "Gracias",
        message: "Su información ha sido recibida. Un miembro de nuestro equipo estará con usted en breve.",
    },

    aboutYou: {
        title:                "Sobre Ti",
        firstName:            "Nombre",
        lastName:             "Apellido",
        dateOfBirth:          "Fecha de Nacimiento",
        gender:               "Género",
        genderPlaceholder:    "Seleccionar género",
        genderMale:           "Masculino",
        genderFemale:         "Femenino",
        genderNonBinary:      "No binario",
        genderPreferNotToSay: "Prefiero no decir",
        preferredLanguage:    "Idioma Preferido",
        languagePlaceholder:  "Seleccionar idioma",
        interpreterNeeded:    "¿Necesita un intérprete?",
    },

    yourConcern: {
        title:            "Tu Preocupación",
        rawConcernText:   "En sus propias palabras, ¿qué le trajo aquí hoy?",
        onset:            "¿Cuánto tiempo lleva sintiéndose así?",
        onsetPlaceholder: "Seleccionar…",
        onsetToday:       "Hoy",
        onsetThisWeek:    "Esta semana",
        onsetThisMonth:   "Este mes",
        onsetLonger:      "Más de un mes",
        previousEpisode:  "¿Ha sentido esto antes?",
        isCrisis:         "¿Está en crisis ahora mismo?",
    },

    symptomsStep: {
        title:               "¿Cómo Se Siente?",
        symptomsLabel:       "¿Cuál de los siguientes ha experimentado? (seleccione todos los que apliquen)",
        sadOrHopeless:       "Triste o sin esperanza",
        anxietyOrPanic:      "Ansiedad / pánico",
        difficultySleeping:  "Dificultad para dormir",
        hearingOrSeeing:     "Escuchar / ver cosas",
        selfHarm:            "Pensamientos de autolesión",
        harmingOthers:       "Pensamientos de hacerle daño a otros",
        difficultyEating:    "Dificultad para comer",
        feelingDisconnected: "Sentirse desconectado",
        overwhelmingAnger:   "Ira abrumadora",
        substanceUse:        "Preocupaciones por consumo de sustancias",
        distressLevel:       "Nivel de angustia (1 = bajo, 5 = severo)",
        distressPlaceholder: "Seleccionar 1–5",
        dailyImpact:         "¿Cuánto afecta esto su vida diaria?",
        impactPlaceholder:   "Seleccionar…",
        impactNotAtAll:      "Para nada",
        impactALittle:       "Un poco",
        impactALot:          "Mucho",
        impactCantFunction:  "No puedo funcionar",
    },

    background: {
        title:              "Su Historial",
        currentTreatment:   "¿Actualmente está siendo atendido por un terapeuta o profesional de salud mental?",
        currentMedications: "Medicamentos de salud mental (separados por coma, o deje en blanco)",
        otherConditions:    "Otras condiciones médicas (separadas por coma, o deje en blanco)",
        allergies:          "Alergias (separadas por coma, o deje en blanco)",
        previousMhHospital: "¿Ha sido hospitalizado alguna vez por razones de salud mental?",
    },

    cultural: {
        title:                      "Necesidades Culturales y Personales",
        culturalNotes:              "¿Hay factores religiosos, culturales o personales que le gustaría que el equipo de atención conociera? (opcional)",
        clinicianGenderPreference:  "Género preferido del médico",
        clinicianGenderPlaceholder: "Seleccionar…",
        clinicianMale:              "Masculino",
        clinicianFemale:            "Femenino",
        clinicianNoPreference:      "Sin preferencia",
        familyInvolvement:          "¿Le gustaría que un familiar o persona de apoyo participe en su atención?",
        familyYes:                  "Sí",
        familyNo:                   "No",
        familyNotNow:               "Por ahora no",
        additionalNotes:            "¿Hay algo más que le gustaría compartir? (opcional)",
    },
}

const ar: T = {
    language: "اللغة",
    dir: "rtl",

    steps: {
        personal:   "عنك",
        concern:    "مخاوفك",
        symptoms:   "الأعراض",
        background: "الخلفية",
        cultural:   "الاحتياجات الثقافية",
    },

    common: {
        yes:        "نعم",
        no:         "لا",
        select:     "اختر…",
        previous:   "السابق",
        next:       "التالي",
        submit:     "إرسال",
        submitting: "جاري الإرسال…",
    },

    success: {
        title:   "شكراً لك",
        message: "تم استلام معلوماتك. سيكون أحد أعضاء فريقنا معك قريباً.",
    },

    aboutYou: {
        title:                "عنك",
        firstName:            "الاسم الأول",
        lastName:             "اسم العائلة",
        dateOfBirth:          "تاريخ الميلاد",
        gender:               "الجنس",
        genderPlaceholder:    "اختر الجنس",
        genderMale:           "ذكر",
        genderFemale:         "أنثى",
        genderNonBinary:      "غير ثنائي",
        genderPreferNotToSay: "أفضل عدم الإفصاح",
        preferredLanguage:    "اللغة المفضلة",
        languagePlaceholder:  "اختر اللغة",
        interpreterNeeded:    "هل تحتاج إلى مترجم؟",
    },

    yourConcern: {
        title:            "مخاوفك",
        rawConcernText:   "بكلماتك الخاصة، ما الذي أحضرك إلى هنا اليوم؟",
        onset:            "منذ متى وأنت تشعر بهذا؟",
        onsetPlaceholder: "اختر…",
        onsetToday:       "اليوم",
        onsetThisWeek:    "هذا الأسبوع",
        onsetThisMonth:   "هذا الشهر",
        onsetLonger:      "أكثر من شهر",
        previousEpisode:  "هل شعرت بهذا من قبل؟",
        isCrisis:         "هل أنت في أزمة الآن؟",
    },

    symptomsStep: {
        title:               "كيف تشعر؟",
        symptomsLabel:       "ما الأعراض التي عانيت منها؟ (اختر كل ما ينطبق)",
        sadOrHopeless:       "حزين أو يائس",
        anxietyOrPanic:      "قلق / ذعر",
        difficultySleeping:  "صعوبة في النوم",
        hearingOrSeeing:     "سماع أو رؤية أشياء",
        selfHarm:            "أفكار إيذاء النفس",
        harmingOthers:       "أفكار إيذاء الآخرين",
        difficultyEating:    "صعوبة في الأكل",
        feelingDisconnected: "الشعور بالانفصال",
        overwhelmingAnger:   "غضب شديد",
        substanceUse:        "مخاوف من تعاطي المواد",
        distressLevel:       "مستوى الضائقة (١ = منخفض، ٥ = شديد)",
        distressPlaceholder: "اختر ١–٥",
        dailyImpact:         "كيف يؤثر هذا على حياتك اليومية؟",
        impactPlaceholder:   "اختر…",
        impactNotAtAll:      "لا يؤثر على الإطلاق",
        impactALittle:       "قليلاً",
        impactALot:          "كثيراً",
        impactCantFunction:  "لا أستطيع العمل",
    },

    background: {
        title:              "خلفيتك",
        currentTreatment:   "هل تتلقى حالياً علاجاً من معالج نفسي أو متخصص في الصحة النفسية؟",
        currentMedications: "أدوية الصحة النفسية (مفصولة بفواصل، أو اتركها فارغة)",
        otherConditions:    "حالات طبية أخرى (مفصولة بفواصل، أو اتركها فارغة)",
        allergies:          "الحساسية (مفصولة بفواصل، أو اتركها فارغة)",
        previousMhHospital: "هل سبق أن دخلت المستشفى بسبب مشكلة في الصحة النفسية؟",
    },

    cultural: {
        title:                      "الاحتياجات الثقافية والشخصية",
        culturalNotes:              "هل هناك عوامل دينية أو ثقافية أو شخصية تود أن يعرفها فريق الرعاية؟ (اختياري)",
        clinicianGenderPreference:  "الجنس المفضل للطبيب",
        clinicianGenderPlaceholder: "اختر…",
        clinicianMale:              "ذكر",
        clinicianFemale:            "أنثى",
        clinicianNoPreference:      "لا تفضيل",
        familyInvolvement:          "هل تود أن يشارك أحد أفراد الأسرة أو شخص داعم في رعايتك؟",
        familyYes:                  "نعم",
        familyNo:                   "لا",
        familyNotNow:               "ليس الآن",
        additionalNotes:            "هل هناك أي شيء آخر تود مشاركته؟ (اختياري)",
    },
}

export const translations: Record<Language, T> = { en, es, ar }
