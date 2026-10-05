import { useState } from "react";
import type { TroubleshootingStep } from "../types/diagnosis";

interface Props {
  steps: TroubleshootingStep[];
}

function StepItem({ step }: { step: TroubleshootingStep }) {
  const [done, setDone] = useState(false);
  return (
    <li className="flex items-start gap-3 py-3">
      <button
        onClick={() => setDone((d) => !d)}
        aria-label={done ? "Mark as not done" : "Mark as done"}
        className={`mt-0.5 w-6 h-6 shrink-0 rounded-full border-2 flex items-center justify-center text-xs font-bold transition-colors ${
          done ? "bg-brand-600 border-brand-600 text-white" : "border-gray-300 text-gray-400"
        }`}
      >
        {done ? "✓" : step.step}
      </button>
      <div className={done ? "opacity-50" : ""}>
        <p className="font-medium text-gray-800">{step.title}</p>
        <p className="text-sm text-gray-500">{step.description}</p>
        {step.warning && (
          <p className="text-sm text-amber-700 mt-1 flex items-center gap-1">
            <span>⚠️</span> {step.warning}
          </p>
        )}
      </div>
    </li>
  );
}

export default function TroubleshootingSteps({ steps }: Props) {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const basic = steps.filter((s) => !s.is_advanced);
  const advanced = steps.filter((s) => s.is_advanced);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
      <h3 className="text-lg font-bold text-gray-900 mb-1">Start Here</h3>
      <ul className="divide-y divide-gray-100">
        {basic.map((step) => (
          <StepItem key={step.step} step={step} />
        ))}
      </ul>

      {advanced.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <button
            onClick={() => setShowAdvanced((s) => !s)}
            className="text-brand-600 font-semibold text-sm hover:underline"
          >
            {showAdvanced ? "Hide" : "Show"} Advanced Troubleshooting →
          </button>
          {showAdvanced && (
            <ul className="divide-y divide-gray-100 mt-3">
              {advanced.map((step) => (
                <StepItem key={step.step} step={step} />
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
