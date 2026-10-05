import { priorityColor, priorityIcon } from "../utils/formatters";

interface Props {
  priority: string;
}

export default function PriorityBadge({ priority }: Props) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${priorityColor(
        priority
      )}`}
    >
      <span aria-hidden="true">{priorityIcon(priority)}</span>
      {priority}
    </span>
  );
}
