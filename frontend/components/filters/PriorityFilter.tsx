"use client";

/**
 * PriorityFilter component - dropdown to filter tasks by priority level.
 *
 * Features:
 * - Select dropdown with priority options
 * - Options: All, High, Medium, Low
 * - Follows existing styling patterns
 *
 * Reference: specs/ui/components.md, specs/features/task-crud.md
 */

import type { Priority } from "@/types";

interface PriorityFilterProps {
  value: Priority | "all";
  onChange: (value: Priority | "all") => void;
  disabled?: boolean;
  className?: string;
}

export function PriorityFilter({
  value,
  onChange,
  disabled = false,
  className = "",
}: PriorityFilterProps) {
  return (
    <div className={className}>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as Priority | "all")}
        disabled={disabled}
        className={`w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
        aria-label="Filter by priority"
      >
        <option value="all">All Priorities</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
    </div>
  );
}

export default PriorityFilter;
