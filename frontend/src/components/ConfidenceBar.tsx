import { formatConfidence } from "../utils/formatters";

interface Props {
  confidence: number;
}

export default function ConfidenceBar({ confidence }: Props) {
  const pct = Math.min(100, Math.max(0, Math.round(confidence * 100)));
  const color = pct >= 80 ? "bg-green-500" : pct >= 55 ? "bg-yellow-500" : "bg-red-400";

  return (
    <div>
      <div className="flex justify-between items-center mb-1 text-sm">
        <span className="text-gray-500">Confidence</span>
        <span className="font-semibold text-gray-800">{formatConfidence(confidence)}</span>
      </div>
      <div className="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
