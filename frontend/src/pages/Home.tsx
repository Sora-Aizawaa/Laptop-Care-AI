import { useState } from "react";
import ComplaintForm from "../components/ComplaintForm";
import DiagnosisCard from "../components/DiagnosisCard";
import FeedbackWidget from "../components/FeedbackWidget";
import LoadingDiagnosis from "../components/LoadingDiagnosis";
import ProgressIndicator from "../components/ProgressIndicator";
import QuestionCard from "../components/QuestionCard";
import TroubleshootingSteps from "../components/TroubleshootingSteps";
import { useDiagnosis } from "../hooks/useDiagnosis";

const GUIDED_INTRO_QUESTIONS: { id: string; question: string; phrase: string }[] = [
  { id: "turns_on", question: "Is your laptop turning on at all?", phrase: "laptop tidak menyala" },
  { id: "gets_hot", question: "Does the laptop become very hot during use?", phrase: "laptop sangat panas" },
  { id: "screen_shows", question: "Is your screen showing anything at all?", phrase: "layar tidak menampilkan apa apa" },
  { id: "network_issue", question: "Are you having trouble with WiFi or Bluetooth?", phrase: "wifi atau bluetooth tidak berfungsi" },
  { id: "runs_slow", question: "Does the laptop feel unusually slow?", phrase: "laptop sangat lambat" },
];

type Mode = "idle" | "describe" | "guided_intro";

export default function Home() {
  const { loading, error, result, analyze, answerFollowUp, reset } = useDiagnosis();
  const [mode, setMode] = useState<Mode>("idle");
  const [guidedStep, setGuidedStep] = useState(0);
  const [guidedPhrases, setGuidedPhrases] = useState<string[]>([]);
  const [technicianMode, setTechnicianMode] = useState(false);

  function handleStartOver() {
    reset();
    setMode("idle");
    setGuidedStep(0);
    setGuidedPhrases([]);
  }

  function handleGuidedAnswer(answer: "Yes" | "No" | "Not sure") {
    const q = GUIDED_INTRO_QUESTIONS[guidedStep];
    const nextPhrases = answer === "Yes" ? [...guidedPhrases, q.phrase] : guidedPhrases;
    setGuidedPhrases(nextPhrases);

    const isLast = guidedStep === GUIDED_INTRO_QUESTIONS.length - 1;
    if (isLast) {
      const complaintText =
        nextPhrases.length > 0
          ? `Laptop saya mengalami: ${nextPhrases.join(", ")}.`
          : "Laptop saya bermasalah tapi saya tidak yakin gejalanya.";
      analyze(complaintText);
    } else {
      setGuidedStep((s) => s + 1);
    }
  }

  const showGuidedIntro = mode === "guided_intro" && !result && !loading;

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      {!result && !loading && mode === "idle" && (
        <ComplaintForm
          onSubmit={(text) => {
            setMode("describe");
            analyze(text);
          }}
          onStartGuided={() => setMode("guided_intro")}
        />
      )}

      {showGuidedIntro && (
        <>
          <ProgressIndicator
            current={guidedStep + 1}
            total={GUIDED_INTRO_QUESTIONS.length}
            label="Let's check a few things before diagnosing the problem."
          />
          <QuestionCard
            question={GUIDED_INTRO_QUESTIONS[guidedStep].question}
            onAnswer={handleGuidedAnswer}
          />
        </>
      )}

      {loading && <LoadingDiagnosis />}

      {error && !loading && (
        <div className="bg-white rounded-2xl shadow-sm border border-red-100 p-8 text-center max-w-2xl mx-auto">
          <p className="text-red-600 font-semibold mb-1">Something went wrong.</p>
          <p className="text-gray-500 mb-4">{error}</p>
          <button
            onClick={handleStartOver}
            className="px-6 py-2 rounded-lg bg-brand-600 text-white font-medium hover:bg-brand-700"
          >
            Try Again
          </button>
        </div>
      )}

      {result && !loading && (
        <div className="space-y-5">
          {result.diagnosis.is_low_confidence && result.follow_up_questions.length > 0 ? (
            <>
              <div className="bg-white rounded-2xl border border-gray-100 p-4 text-center text-sm text-gray-500 max-w-2xl mx-auto">
                We need more information to determine the problem confidently.
              </div>
              <QuestionCard
                question={result.follow_up_questions[0].question}
                onAnswer={(ans) => answerFollowUp(result.follow_up_questions[0].id, ans)}
                disabled={loading}
              />
            </>
          ) : (
            <>
              <DiagnosisCard result={result} technicianMode={technicianMode} />
              {result.troubleshooting_steps.length > 0 && (
                <TroubleshootingSteps steps={result.troubleshooting_steps} />
              )}
              {result.diagnosis_id && <FeedbackWidget diagnosisId={result.diagnosis_id} />}

              <div className="flex items-center justify-between max-w-2xl mx-auto pt-2">
                <label className="flex items-center gap-2 text-sm text-gray-500">
                  <input
                    type="checkbox"
                    checked={technicianMode}
                    onChange={(e) => setTechnicianMode(e.target.checked)}
                    className="rounded border-gray-300"
                  />
                  Technician mode
                </label>
                <button
                  onClick={handleStartOver}
                  className="text-brand-600 font-semibold text-sm hover:underline"
                >
                  Start a new diagnosis →
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
