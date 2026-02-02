"use client";

/**
 * SortSelect component - dropdown to select sort order for tasks.
 *
 * Features:
 * - Select dropdown with sort options
 * - Options: Newest, Oldest, Title, Priority
 * - Follows existing styling patterns
 *
 * Reference: specs/ui/components.md, specs/features/task-crud.md
 */

export type SortOption = "created_desc" | "created_asc" | "title" | "priority";

interface SortSelectProps {
  value: SortOption;
  onChange: (value: SortOption) => void;
  disabled?: boolean;
  className?: string;
}

export function SortSelect({
  value,
  onChange,
  disabled = false,
  className = "",
}: SortSelectProps) {
  return (
    <div className={className}>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as SortOption)}
        disabled={disabled}
        className={`w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
        aria-label="Sort tasks by"
      >
        <option value="created_desc">Newest First</option>
        <option value="created_asc">Oldest First</option>
        <option value="title">Title (A-Z)</option>
        <option value="priority">Priority</option>
      </select>
    </div>
  );
}

export default SortSelect;
