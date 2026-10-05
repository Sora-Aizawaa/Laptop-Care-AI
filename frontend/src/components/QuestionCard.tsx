interface Props {
  question: string;
  onAnswer: (answer: "Yes" | "No" | "Not sure") => void;
  disabled?: boolean;
}

export default function QuestionCard({ question, onAnswer, disabled }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8 max-w-2xl mx-auto text-center">
      <p className="text-lg font-semibold text-gray-900 mb-6">{question}</p>
      <div className="flex flex-col sm:flex-row gap-3 justify-center">
        {(["Yes", "No", "Not sure"] as const).map((option) => (
          <button
            key={option}
            disabled={disabled}
            onClick={() => onAnswer(option)}
            className="flex-1 sm:flex-none sm:px-8 py-3 rounded-xl border border-gray-200 font-medium text-gray-700 hover:border-brand-400 hover:bg-brand-50 disabled:opacity-60 transition-colors"
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}
