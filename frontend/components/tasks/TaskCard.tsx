"use client";

/**
 * TaskCard component - displays individual task with status and actions.
 *
 * Features:
 * - Checkbox for completion toggle
 * - Title and description display
 * - Priority badge (color-coded)
 * - Tag chips
 * - Edit and delete buttons (prepared for future US4, US5)
 * - Strikethrough when completed
 *
 * Reference: specs/ui/components.md
 */

import type { Task } from "@/types";
import { PriorityBadge } from "@/components/ui/PriorityBadge";
import { TagBadge } from "@/components/ui/TagBadge";

interface TaskCardProps {
  task: Task;
  onToggle?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  return (
    <div
      className={`group rounded-lg border bg-white p-3 sm:p-4 shadow-sm transition-shadow hover:shadow-md ${
        task.completed ? "border-gray-200 bg-gray-50" : "border-gray-200"
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Completion Checkbox */}
        <button
          onClick={() => onToggle?.(task.id)}
          disabled={!onToggle}
          className={`mt-1 h-5 w-5 flex-shrink-0 rounded border-2 transition-colors ${
            task.completed
              ? "border-green-500 bg-green-500"
              : "border-gray-300 hover:border-blue-500"
          } ${!onToggle ? "cursor-default" : "cursor-pointer"}`}
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.completed && (
            <svg
              className="h-full w-full text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title and Priority */}
          <div className="flex items-center gap-2 flex-wrap">
            <h3
              className={`text-sm font-medium ${
                task.completed
                  ? "text-gray-500 line-through"
                  : "text-gray-900"
              }`}
            >
              {task.title}
            </h3>
            <PriorityBadge priority={task.priority} />
          </div>

          {/* Description */}
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}

          {/* Tags */}
          {task.tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {task.tags.map((tag) => (
                <TagBadge key={tag} name={tag} />
              ))}
            </div>
          )}

          {/* Timestamp */}
          <p className="mt-2 text-xs text-gray-400">
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Actions - always visible on mobile, hover on desktop (T143) */}
        <div className="flex items-center gap-1 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
          {onEdit && (
            <button
              onClick={() => onEdit(task)}
              className="p-1.5 text-gray-400 hover:text-blue-600 rounded hover:bg-blue-50 transition-colors"
              aria-label="Edit task"
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
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(task.id)}
              className="p-1.5 text-gray-400 hover:text-red-600 rounded hover:bg-red-50 transition-colors"
              aria-label="Delete task"
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
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default TaskCard;
