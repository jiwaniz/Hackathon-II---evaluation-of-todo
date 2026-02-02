"use client";

/**
 * TaskList component - displays a list of tasks with loading/empty states.
 *
 * Features:
 * - Map tasks to TaskCard components
 * - Loading skeleton while fetching
 * - Empty state with CTA to create first task
 * - Keyboard navigation support (T144)
 * - Pagination controls (prepared for future)
 *
 * Reference: specs/ui/components.md
 */

import { useState, useRef, useCallback, useEffect } from "react";
import type { Task } from "@/types";
import { TaskCard } from "./TaskCard";
import { EmptyState } from "@/components/ui/EmptyState";

interface TaskListProps {
  tasks: Task[];
  isLoading?: boolean;
  onToggle?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
  onCreateTask?: () => void;
  hasActiveFilters?: boolean;
  onClearFilters?: () => void;
}

function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="rounded-lg border border-gray-200 bg-white p-4 animate-pulse"
        >
          <div className="flex items-start gap-3">
            <div className="h-5 w-5 rounded bg-gray-200" />
            <div className="flex-1 space-y-2">
              <div className="flex items-center gap-2">
                <div className="h-4 w-32 rounded bg-gray-200" />
                <div className="h-5 w-16 rounded-full bg-gray-200" />
              </div>
              <div className="h-3 w-48 rounded bg-gray-200" />
              <div className="h-3 w-24 rounded bg-gray-200" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export function TaskList({
  tasks,
  isLoading = false,
  onToggle,
  onEdit,
  onDelete,
  onCreateTask,
  hasActiveFilters = false,
  onClearFilters,
}: TaskListProps) {
  const [focusedIndex, setFocusedIndex] = useState<number>(-1);
  const listRef = useRef<HTMLDivElement>(null);
  const taskRefs = useRef<(HTMLDivElement | null)[]>([]);

  // Reset focus when tasks change
  useEffect(() => {
    taskRefs.current = taskRefs.current.slice(0, tasks.length);
  }, [tasks.length]);

  // Keyboard navigation handler (T144)
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLDivElement>) => {
      if (tasks.length === 0) return;

      switch (e.key) {
        case "ArrowDown":
        case "j": // Vim-style navigation
          e.preventDefault();
          setFocusedIndex((prev) => {
            const next = prev < tasks.length - 1 ? prev + 1 : 0;
            taskRefs.current[next]?.focus();
            return next;
          });
          break;

        case "ArrowUp":
        case "k": // Vim-style navigation
          e.preventDefault();
          setFocusedIndex((prev) => {
            const next = prev > 0 ? prev - 1 : tasks.length - 1;
            taskRefs.current[next]?.focus();
            return next;
          });
          break;

        case "Enter":
        case " ": // Space
          e.preventDefault();
          if (focusedIndex >= 0 && focusedIndex < tasks.length) {
            onToggle?.(tasks[focusedIndex].id);
          }
          break;

        case "e":
          e.preventDefault();
          if (focusedIndex >= 0 && focusedIndex < tasks.length) {
            onEdit?.(tasks[focusedIndex]);
          }
          break;

        case "d":
        case "Delete":
          e.preventDefault();
          if (focusedIndex >= 0 && focusedIndex < tasks.length) {
            onDelete?.(tasks[focusedIndex].id);
          }
          break;

        case "Home":
          e.preventDefault();
          setFocusedIndex(0);
          taskRefs.current[0]?.focus();
          break;

        case "End":
          e.preventDefault();
          const lastIndex = tasks.length - 1;
          setFocusedIndex(lastIndex);
          taskRefs.current[lastIndex]?.focus();
          break;
      }
    },
    [tasks, focusedIndex, onToggle, onEdit, onDelete]
  );

  if (isLoading) {
    return <TaskListSkeleton />;
  }

  if (tasks.length === 0) {
    // Show different message when filters are active
    if (hasActiveFilters) {
      return (
        <div className="rounded-lg border border-gray-200 bg-white">
          <EmptyState
            title="No matching tasks"
            description="Try adjusting your search or filters to find what you're looking for."
            icon={
              <svg
                className="h-12 w-12"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            }
            action={
              onClearFilters
                ? { label: "Clear filters", onClick: onClearFilters }
                : undefined
            }
          />
        </div>
      );
    }

    return (
      <div className="rounded-lg border border-gray-200 bg-white">
        <EmptyState
          title="No tasks yet"
          description="Get started by creating your first task."
          icon={
            <svg
              className="h-12 w-12"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
              />
            </svg>
          }
          action={
            onCreateTask
              ? { label: "Create a task", onClick: onCreateTask }
              : undefined
          }
        />
      </div>
    );
  }

  return (
    <div
      ref={listRef}
      className="space-y-3"
      role="list"
      aria-label="Task list"
      onKeyDown={handleKeyDown}
    >
      {/* Keyboard shortcuts hint */}
      <p className="sr-only">
        Use arrow keys to navigate, Enter or Space to toggle, E to edit, D or Delete to remove
      </p>
      {tasks.map((task, index) => (
        <div
          key={task.id}
          ref={(el) => { taskRefs.current[index] = el; }}
          tabIndex={0}
          role="listitem"
          aria-selected={focusedIndex === index}
          onFocus={() => setFocusedIndex(index)}
          className={`outline-none ${
            focusedIndex === index ? "ring-2 ring-blue-500 ring-offset-2 rounded-lg" : ""
          }`}
        >
          <TaskCard
            task={task}
            onToggle={onToggle}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </div>
      ))}
    </div>
  );
}

export default TaskList;
