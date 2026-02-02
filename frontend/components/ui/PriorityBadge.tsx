/**
 * PriorityBadge component - displays task priority with color-coded styling.
 *
 * Features:
 * - Color-coded badges: red for high, yellow for medium, green for low
 * - Compact pill design
 * - Optional size variants
 *
 * Reference: specs/ui/components.md, frontend/CLAUDE.md
 */

import type { Priority } from "@/types";

interface PriorityBadgeProps {
  priority: Priority;
  size?: "sm" | "md";
  className?: string;
}

const PRIORITY_STYLES: Record<Priority, string> = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-green-100 text-green-800",
};

const PRIORITY_LABELS: Record<Priority, string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
};

const SIZE_STYLES = {
  sm: "px-1.5 py-0.5 text-xs",
  md: "px-2 py-0.5 text-xs",
};

export function PriorityBadge({
  priority,
  size = "md",
  className = "",
}: PriorityBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full font-medium ${PRIORITY_STYLES[priority]} ${SIZE_STYLES[size]} ${className}`}
    >
      {PRIORITY_LABELS[priority]}
    </span>
  );
}

export default PriorityBadge;
