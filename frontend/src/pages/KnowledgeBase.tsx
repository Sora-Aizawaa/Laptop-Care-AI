import { useEffect, useState } from "react";
import { getProblemDetail, getProblems } from "../services/api";
import type { ProblemDetail, ProblemSummary } from "../types/diagnosis";
import PriorityBadge from "../components/PriorityBadge";

export default function KnowledgeBase() {
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [selected, setSelected] = useState<ProblemDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    getProblems().then(setProblems).catch(() => {});
  }, []);

  async function openProblem(id: number) {
    setLoadingDetail(true);
    try {
      const detail = await getProblemDetail(id);
      setSelected(detail);
    } finally {
      setLoadingDetail(false);
    }
  }

  return (
    <div className="max-w-5xl mx-auto py-10 px-4 grid md:grid-cols-[280px_1fr] gap-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900 mb-4">Knowledge Base</h1>
        <ul className="space-y-2">
          {problems.map((p) => (
            <li key={p.id}>
              <button
                onClick={() => openProblem(p.id)}
                className={`w-full text-left px-4 py-3 rounded-xl border transition-colors ${
                  selected?.id === p.id
                    ? "border-brand-400 bg-brand-50"
                    : "border-gray-100 bg-white hover:border-gray-200"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-medium text-gray-800">{p.name}</span>
                  <PriorityBadge priority={p.severity} />
                </div>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div>
        {!selected && !loadingDetail && (
          <div className="bg-white rounded-2xl border border-gray-100 p-10 text-center text-gray-400">
            Select a problem from the list to see details.
          </div>
        )}

        {loadingDetail && <div className="text-gray-400 p-10 text-center">Loading...</div>}

        {selected && !loadingDetail && (
          <div className="bg-white rounded-2xl border border-gray-100 p-6 sm:p-8">
            <div className="flex items-center gap-2 mb-2">
              <h2 className="text-xl font-bold text-gray-900">{selected.name}</h2>
              <PriorityBadge priority={selected.severity} />
            </div>
            <p className="text-gray-500 mb-1">{selected.category?.name}</p>
            <p className="text-gray-600 mb-4">{selected.description}</p>
            <p className="text-sm text-gray-400 mb-6">
              Estimated troubleshooting time: {selected.estimated_time_min}-
              {selected.estimated_time_max} minutes
            </p>

            <h3 className="font-semibold text-gray-800 mb-2">Troubleshooting Steps</h3>
            <ol className="space-y-3">
              {selected.troubleshooting_steps.map((step) => (
                <li key={step.step_number} className="flex gap-3">
                  <span className="w-6 h-6 shrink-0 rounded-full bg-brand-100 text-brand-700 text-xs font-bold flex items-center justify-center">
                    {step.step_number}
                  </span>
                  <div>
                    <p className="font-medium text-gray-800">{step.title}</p>
                    <p className="text-sm text-gray-500">{step.description}</p>
                    {step.warning && (
                      <p className="text-sm text-amber-700 mt-0.5">⚠️ {step.warning}</p>
                    )}
                  </div>
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  );
}
