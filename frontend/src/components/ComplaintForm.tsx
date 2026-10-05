import { FormEvent, useState } from "react";

interface Props {
  onSubmit: (complaint: string) => void;
  onStartGuided: () => void;
  disabled?: boolean;
}

export default function ComplaintForm({ onSubmit, onStartGuided, disabled }: Props) {
  const [text, setText] = useState("");
  const [touched, setTouched] = useState(false);

  const isEmpty = text.trim().length === 0;

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setTouched(true);
    if (isEmpty) return;
    onSubmit(text.trim());
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 text-center mb-1">
        How can we help with your laptop?
      </h1>
      <p className="text-gray-500 text-center mb-6">
        Tell us what is happening with your laptop.
      </p>

      <form onSubmit={handleSubmit}>
        <textarea
          className="w-full min-h-[120px] rounded-xl border border-gray-200 p-4 text-gray-800 focus:outline-none focus:ring-2 focus:ring-brand-400 focus:border-transparent resize-none"
          placeholder="My laptop becomes very hot and suddenly shuts down after 30 minutes..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={disabled}
        />
        {touched && isEmpty && (
          <p className="text-red-500 text-sm mt-2">
            Please describe what is happening with your laptop.
          </p>
        )}

        <button
          type="submit"
          disabled={disabled}
          className="w-full mt-4 bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white font-semibold py-3 rounded-xl transition-colors"
        >
          Analyze Problem
        </button>
      </form>

      <div className="text-center mt-6 pt-6 border-t border-gray-100">
        <p className="text-gray-500 text-sm mb-2">Don't know what to write?</p>
        <button
          onClick={onStartGuided}
          disabled={disabled}
          className="text-brand-600 font-semibold text-sm hover:underline disabled:opacity-60"
        >
          Start Guided Troubleshooting →
        </button>
      </div>
    </div>
  );
}
