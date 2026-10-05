import { useState } from "react";
import { submitFeedback } from "../services/api";

interface Props {
  diagnosisId: number;
}

const ALTERNATIVES = [
  "Fan Problem",
  "Battery",
  "RAM",
  "Motherboard",
  "Software Issue",
  "Other",
];

export default function FeedbackWidget({ diagnosisId }: Props) {
  const [status, setStatus] = useState<"idle" | "asking_actual" | "submitted">("idle");
  const [submitting, setSubmitting] = useState(false);

  async function handleYes() {
    setSubmitting(true);
    await submitFeedback(diagnosisId, true);
    setSubmitting(false);
    setStatus("submitted");
  }

  function handleNo() {
    setStatus("asking_actual");
  }

  async function handleActual(actual: string) {
    setSubmitting(true);
    await submitFeedback(diagnosisId, false, actual);
    setSubmitting(false);
    setStatus("submitted");
  }

  if (status === "submitted") {
    return (
      <div className="bg-white rounded-2xl border border-gray-100 p-5 text-center text-sm text-gray-600">
        Thanks for the feedback — this helps us improve future diagnoses. 🙏
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-5">
      {status === "idle" && (
        <>
          <p className="text-sm font-semibold text-gray-800 mb-3 text-center">
            Was this diagnosis correct?
          </p>
          <div className="flex gap-3 justify-center">
            <button
              disabled={submitting}
              onClick={handleYes}
              className="px-6 py-2 rounded-lg bg-green-50 text-green-700 font-medium hover:bg-green-100 disabled:opacity-60"
            >
              Yes
            </button>
            <button
              disabled={submitting}
              onClick={handleNo}
              className="px-6 py-2 rounded-lg bg-red-50 text-red-700 font-medium hover:bg-red-100 disabled:opacity-60"
            >
              No
            </button>
          </div>
        </>
      )}

      {status === "asking_actual" && (
        <>
          <p className="text-sm font-semibold text-gray-800 mb-3 text-center">
            What was the actual problem?
          </p>
          <div className="flex flex-wrap gap-2 justify-center">
            {ALTERNATIVES.map((alt) => (
              <button
                key={alt}
                disabled={submitting}
                onClick={() => handleActual(alt)}
                className="px-4 py-1.5 rounded-full border border-gray-200 text-sm text-gray-700 hover:border-brand-400 hover:bg-brand-50 disabled:opacity-60"
              >
                {alt}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
