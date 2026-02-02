"use client";

/**
 * PrioritySelect component - dropdown for selecting task priority.
 *
 * Features:
 * - Three priority options: high, medium, low
 * - Accessible select element
 * - Consistent styling with other form elements
 *
 * Reference: specs/ui/components.md, frontend/CLAUDE.md
 */

import type { Priority } from "@/types";

interface PrioritySelectProps {
  value: Priority;
  onChange: (priority: Priority) => void;
  disabled?: boolean;
  id?: string;
  className?: string;
}

const PRIORITY_OPTIONS: { value: Priority; label: string }[] = [
  { value: "high", label: "High" },
  { value: "medium", label: "Medium" },
  { value: "low", label: "Low" },
];

export function PrioritySelect({
  value,
  onChange,
  disabled = false,
  id,
  className = "",
}: PrioritySelectProps) {
  return (
    <select
      id={id}
      value={value}
      onChange={(e) => onChange(e.target.value as Priority)}
      disabled={disabled}
      className={`w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed ${className}`}
    >
      {PRIORITY_OPTIONS.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

export default PrioritySelect;
