"use client";

/**
 * TagFilter component - dropdown to filter tasks by tag.
 *
 * Features:
 * - Select dropdown with available tags
 * - Dynamic options based on user's tags
 * - "All Tags" option to clear filter
 *
 * Reference: specs/ui/components.md, specs/features/task-crud.md
 */

interface TagFilterProps {
  value: string;
  onChange: (value: string) => void;
  availableTags: string[];
  disabled?: boolean;
  className?: string;
}

export function TagFilter({
  value,
  onChange,
  availableTags,
  disabled = false,
  className = "",
}: TagFilterProps) {
  return (
    <div className={className}>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className={`w-full px-3 py-2 text-sm border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
        aria-label="Filter by tag"
      >
        <option value="">All Tags</option>
        {availableTags.map((tag) => (
          <option key={tag} value={tag}>
            {tag}
          </option>
        ))}
      </select>
    </div>
  );
}

export default TagFilter;
