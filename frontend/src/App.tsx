import MultiStepForm from "./components/ui/multi-step-form"
import { LanguageProvider } from "./context/LanguageContext"

function App() {
  return (
    <LanguageProvider>
      <MultiStepForm />
    </LanguageProvider>
  )
}

export default App
