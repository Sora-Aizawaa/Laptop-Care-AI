import ConfidenceBar from "./ConfidenceBar";
import PriorityBadge from "./PriorityBadge";
import type { DiagnosisResponse } from "../types/diagnosis";

interface Props {
  result: DiagnosisResponse;
  technicianMode?: boolean;
}

const CATEGORY_EMOJI: Record<string, string> = {
  Hardware: "🔧",
  Network: "📶",
  Display: "🖥️",
  Battery: "🔋",
  "Operating System": "💽",
  Performance: "⚡",
};

export default function DiagnosisCard({ result, technicianMode }: Props) {
  const { diagnosis, priority, estimated_time } = result;
  const emoji = diagnosis.category ? CATEGORY_EMOJI[diagnosis.category] || "🔎" : "🔎";

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-6 sm:p-8">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">
          Possible Problem
        </p>
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <span>{emoji}</span> {diagnosis.problem}
        </h2>

        <div className="mb-4">
          <ConfidenceBar confidence={diagnosis.confidence} />
        </div>

        <div className="flex flex-wrap gap-3 mb-5">
          <div className="text-sm">
            <span className="text-gray-400">Category: </span>
            <span className="font-medium text-gray-700">{diagnosis.category}</span>
          </div>
          <div className="text-sm">
            <span className="text-gray-400">Priority: </span>
            <PriorityBadge priority={priority} />
          </div>
          <div className="text-sm">
            <span className="text-gray-400">Est. time: </span>
            <span className="font-medium text-gray-700">{estimated_time}</span>
          </div>
        </div>

        {result.reasoning.length > 0 && (
          <div className="bg-brand-50 rounded-xl p-4 mb-4">
            <p className="text-sm font-semibold text-brand-900 mb-2">Why we think this?</p>
            <ul className="space-y-1">
              {result.reasoning.map((reason, i) => (
                <li key={i} className="text-sm text-brand-800 flex items-start gap-2">
                  <span>✓</span> {reason}
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.possible_causes.length > 0 && (
          <div className="mb-2">
            <p className="text-sm font-semibold text-gray-700 mb-2">Possible Causes</p>
            <ul className="list-disc list-inside space-y-1">
              {result.possible_causes.map((cause, i) => (
                <li key={i} className="text-sm text-gray-600">
                  {cause}
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.safety_warning && (
          <div className="mt-4 bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-3">
            <span className="text-xl">⚠️</span>
            <div>
              <p className="text-sm font-semibold text-amber-900 mb-0.5">Safety Notice</p>
              <p className="text-sm text-amber-800">{result.safety_warning}</p>
            </div>
          </div>
        )}

        {technicianMode && (
          <div className="mt-5 pt-5 border-t border-gray-100">
            <p className="text-sm font-semibold text-gray-700 mb-2">Top predictions (technician view)</p>
            <div className="space-y-1">
              {Object.entries(result.top_predictions).map(([label, score]) => (
                <div key={label} className="flex justify-between text-sm text-gray-600">
                  <span className="capitalize">{label.replace(/_/g, " ")}</span>
                  <span>{Math.round(score * 100)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
