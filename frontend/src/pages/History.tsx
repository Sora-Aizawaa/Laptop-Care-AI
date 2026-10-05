import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PriorityBadge from "../components/PriorityBadge";
import { getHistory } from "../services/api";
import { formatConfidence, formatDate } from "../utils/formatters";
import type { HistoryItem } from "../types/diagnosis";

export default function History() {
  const [items, setItems] = useState<HistoryItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHistory()
      .then(setItems)
      .catch(() => setError("Couldn't load your history right now."));
  }, []);

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Diagnosis History</h1>

      {error && <p className="text-red-600">{error}</p>}

      {items && items.length === 0 && (
        <div className="bg-white rounded-2xl border border-gray-100 p-10 text-center">
          <p className="text-gray-500 mb-4">No diagnosis history yet.</p>
          <p className="text-gray-400 text-sm mb-6">
            Describe your laptop problem to get started.
          </p>
          <Link
            to="/"
            className="inline-block px-6 py-2 rounded-lg bg-brand-600 text-white font-medium hover:bg-brand-700"
          >
            Start Diagnosis
          </Link>
        </div>
      )}

      {items && items.length > 0 && (
        <ul className="space-y-3">
          {items.map((item) => (
            <li
              key={item.diagnosis_id}
              className="bg-white rounded-xl border border-gray-100 p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"
            >
              <div className="min-w-0">
                <p className="font-semibold text-gray-800 truncate">
                  {item.problem_name || "Unresolved diagnosis"}
                </p>
                <p className="text-sm text-gray-500 truncate max-w-md">{item.complaint_text}</p>
                <p className="text-xs text-gray-400 mt-1">{formatDate(item.created_at)}</p>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="text-sm text-gray-500">{formatConfidence(item.confidence)}</span>
                <PriorityBadge priority={item.priority} />
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
