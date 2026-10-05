import { useEffect, useState } from "react";

const MESSAGES = [
  "Understanding symptoms...",
  "Checking possible problems...",
  "Preparing troubleshooting steps...",
];

export default function LoadingDiagnosis() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((i) => (i + 1) % MESSAGES.length);
    }, 1200);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-14 h-14 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin mb-6" />
      <p className="text-lg font-semibold text-gray-800 mb-1">Analyzing your laptop problem...</p>
      <p className="text-gray-500 transition-opacity duration-300">{MESSAGES[index]}</p>
    </div>
  );
}
