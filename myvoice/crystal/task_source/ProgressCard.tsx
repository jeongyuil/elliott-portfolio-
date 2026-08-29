/**
 * ProgressCard Component
 * Design Philosophy: Clean progress visualization with semantic colors
 * - Green for mission completion
 * - Blue for weekly progress
 * - Clear percentage display
 */

interface ProgressCardProps {
  label: string;
  current: number;
  total: number;
  color?: "green" | "blue";
}

export default function ProgressCard({ label, current, total, color = "green" }: ProgressCardProps) {
  const percentage = Math.round((current / total) * 100);

  return (
    <div className="mb-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-semibold text-[var(--duo-text)]">{label}</span>
        <span className="text-sm font-bold text-[var(--duo-text-secondary)]">
          {current}/{total} <span className="text-xs">({percentage}%)</span>
        </span>
      </div>
      <div className="duo-progress">
        <div
          className={`duo-progress-bar ${color === "blue" ? "blue" : ""}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
