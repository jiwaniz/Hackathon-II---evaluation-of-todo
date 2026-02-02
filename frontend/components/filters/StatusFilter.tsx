"use client";

/**
 * StatusFilter component - dropdown to filter tasks by completion status.
 *
 * Features:
 * - Select dropdown with status options
 * - Options: All, Pending, Completed
 * - Follows existing styling patterns
 *
 * Reference: specs/ui/components.md, specs/features/task-crud.md
 */

interface StatusFilterProps {
  value: "all" | "pending" | "completed";
  onChange: (value: "all" | "pending" | "completed") => void;
  disabled?: boolean;
  className?: string;
}

export function StatusFilter({
  value,
  onChange,
  disabled = false,
  className = "",
}: StatusFilterProps) {
  return (
    <div className={className}>
      <select
        value={value}
        onChange={(e) =>
          onChange(e.target.value as "all" | "pending" | "completed")
        }
        disabled={disabled}
        className={`w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
        aria-label="Filter by status"
      >
        <option value="all">All Tasks</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>
    </div>
  );
}

export default StatusFilter;
