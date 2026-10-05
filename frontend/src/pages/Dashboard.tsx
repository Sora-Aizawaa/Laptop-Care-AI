import { useEffect, useState } from "react";
import { getDashboardStats } from "../services/api";
import type { DashboardStats } from "../types/diagnosis";

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-5">
      <p className="text-sm text-gray-500 mb-1">{label}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    getDashboardStats().then(setStats).catch(() => {});
  }, []);

  if (!stats) {
    return <div className="max-w-5xl mx-auto py-10 px-4 text-gray-400">Loading dashboard...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Diagnoses" value={stats.total_diagnoses} />
        <StatCard label="Resolved" value={stats.resolved} />
        <StatCard label="High Priority" value={stats.high_priority} />
        <StatCard label="AI Accuracy" value={stats.ai_accuracy != null ? `${stats.ai_accuracy}%` : "N/A"} />
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 p-6">
        <h2 className="font-semibold text-gray-800 mb-4">Most Common Problems</h2>
        {stats.most_common_problems.length === 0 ? (
          <p className="text-gray-400 text-sm">No diagnoses recorded yet.</p>
        ) : (
          <div className="space-y-3">
            {stats.most_common_problems.map((p) => (
              <div key={p.name}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-700">{p.name}</span>
                  <span className="text-gray-500">{p.percentage}%</span>
                </div>
                <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-brand-500 rounded-full"
                    style={{ width: `${p.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
