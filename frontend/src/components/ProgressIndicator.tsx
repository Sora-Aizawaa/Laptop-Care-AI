interface Props {
  current: number;
  total: number;
  label?: string;
}

export default function ProgressIndicator({ current, total, label }: Props) {
  return (
    <div className="max-w-2xl mx-auto mb-6 text-center">
      <p className="text-sm text-gray-500 mb-2">
        Step {current} of {total}
      </p>
      <div className="flex gap-2 justify-center mb-3">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className={`h-2 flex-1 max-w-[60px] rounded-full ${
              i < current ? "bg-brand-500" : "bg-gray-200"
            }`}
          />
        ))}
      </div>
      {label && <p className="text-gray-600 text-sm">{label}</p>}
    </div>
  );
}
