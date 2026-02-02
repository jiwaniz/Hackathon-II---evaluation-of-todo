"use client";

/**
 * FilterBar component - combines all filter options for task list.
 *
 * Features:
 * - Search input for keyword search
 * - Status filter (All, Pending, Completed)
 * - Priority filter (All, High, Medium, Low)
 * - Tag filter (dynamic based on user's tags)
 * - Clear all filters button
 * - Responsive layout
 *
 * Reference: specs/ui/components.md, specs/features/task-crud.md
 */

import type { Priority } from "@/types";
import { SearchInput } from "./SearchInput";
import { StatusFilter } from "./StatusFilter";
import { PriorityFilter } from "./PriorityFilter";
import { TagFilter } from "./TagFilter";
import { SortSelect, type SortOption } from "./SortSelect";

export interface FilterState {
  search: string;
  status: "all" | "pending" | "completed";
  priority: Priority | "all";
  tag: string;
  sort: SortOption;
}

interface FilterBarProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  availableTags: string[];
  disabled?: boolean;
  className?: string;
}

export function FilterBar({
  filters,
  onFilterChange,
  availableTags,
  disabled = false,
  className = "",
}: FilterBarProps) {
  const hasActiveFilters =
    filters.search ||
    filters.status !== "all" ||
    filters.priority !== "all" ||
    filters.tag !== "";

  const handleClearAll = () => {
    onFilterChange({
      search: "",
      status: "all",
      priority: "all",
      tag: "",
      sort: "created_desc",
    });
  };

  return (
    <div className={`space-y-3 ${className}`}>
      {/* Search bar - full width */}
      <SearchInput
        value={filters.search}
        onChange={(search) => onFilterChange({ ...filters, search })}
        placeholder="Search tasks..."
        disabled={disabled}
      />

      {/* Filters row */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <StatusFilter
          value={filters.status}
          onChange={(status) => onFilterChange({ ...filters, status })}
          disabled={disabled}
          className="w-full sm:w-36"
        />

        <PriorityFilter
          value={filters.priority}
          onChange={(priority) => onFilterChange({ ...filters, priority })}
          disabled={disabled}
          className="w-full sm:w-36"
        />

        {availableTags.length > 0 && (
          <TagFilter
            value={filters.tag}
            onChange={(tag) => onFilterChange({ ...filters, tag })}
            availableTags={availableTags}
            disabled={disabled}
            className="w-full sm:w-36"
          />
        )}

        <SortSelect
          value={filters.sort}
          onChange={(sort) => onFilterChange({ ...filters, sort })}
          disabled={disabled}
          className="w-full sm:w-40"
        />

        {/* Clear filters button */}
        {hasActiveFilters && (
          <button
            type="button"
            onClick={handleClearAll}
            disabled={disabled}
            className="inline-flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Clear all filters"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            Clear
          </button>
        )}
      </div>
    </div>
  );
}

export default FilterBar;
