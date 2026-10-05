export function formatConfidence(confidence: number): string {
  return `${Math.round(confidence * 100)}%`;
}

export function formatDate(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function priorityColor(priority: string): string {
  switch (priority) {
    case "CRITICAL":
      return "bg-red-100 text-red-800 border-red-300";
    case "HIGH":
      return "bg-orange-100 text-orange-800 border-orange-300";
    case "MEDIUM":
      return "bg-yellow-100 text-yellow-800 border-yellow-300";
    case "LOW":
      return "bg-green-100 text-green-800 border-green-300";
    default:
      return "bg-gray-100 text-gray-700 border-gray-300";
  }
}

export function priorityIcon(priority: string): string {
  switch (priority) {
    case "CRITICAL":
      return "⛔";
    case "HIGH":
      return "⚠️";
    case "MEDIUM":
      return "🟡";
    case "LOW":
      return "🟢";
    default:
      return "❔";
  }
}
