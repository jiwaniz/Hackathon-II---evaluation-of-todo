"use client";

/**
 * Hook for optimistic task updates.
 *
 * Provides optimistic update functionality for:
 * - Task toggle (immediate UI feedback)
 * - Task deletion (immediate UI removal)
 *
 * Features:
 * - Immediate UI updates before server response
 * - Automatic rollback on error
 * - Error notification callback
 *
 * Reference: T148 - Implement optimistic updates in frontend
 */

import { useState, useCallback } from "react";
import type { Task } from "@/types";
import { api } from "@/lib/api";

interface UseOptimisticTasksProps {
  userId: string;
  onError?: (message: string) => void;
}

interface UseOptimisticTasksReturn {
  tasks: Task[];
  setTasks: React.Dispatch<React.SetStateAction<Task[]>>;
  optimisticToggle: (taskId: number) => Promise<void>;
  optimisticDelete: (taskId: number) => Promise<void>;
  isToggling: Set<number>;
  isDeleting: Set<number>;
}

/**
 * Hook for optimistic task operations.
 *
 * @param userId - Current user ID for API calls
 * @param onError - Optional callback for error notifications
 * @returns Task state and optimistic update functions
 *
 * @example
 * ```tsx
 * const { tasks, setTasks, optimisticToggle, optimisticDelete, isToggling } = useOptimisticTasks({
 *   userId: user.id,
 *   onError: (msg) => toast.error(msg),
 * });
 *
 * // Optimistic toggle - UI updates immediately
 * <button onClick={() => optimisticToggle(task.id)}>
 *   {isToggling.has(task.id) ? "Saving..." : "Toggle"}
 * </button>
 * ```
 */
export function useOptimisticTasks({
  userId,
  onError,
}: UseOptimisticTasksProps): UseOptimisticTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isToggling, setIsToggling] = useState<Set<number>>(new Set());
  const [isDeleting, setIsDeleting] = useState<Set<number>>(new Set());

  /**
   * Optimistically toggle task completion.
   * Updates UI immediately, then syncs with server.
   * Rolls back on error.
   */
  const optimisticToggle = useCallback(
    async (taskId: number) => {
      // Mark as toggling
      setIsToggling((prev) => new Set(prev).add(taskId));

      // Store previous state for rollback
      const previousTasks = tasks;

      // Optimistically update UI
      setTasks((current) =>
        current.map((task) =>
          task.id === taskId
            ? { ...task, completed: !task.completed, updated_at: new Date().toISOString() }
            : task
        )
      );

      try {
        // Sync with server
        const result = await api.toggleTask(userId, taskId);

        // Update with server response (ensures consistency)
        setTasks((current) =>
          current.map((task) =>
            task.id === taskId
              ? { ...task, completed: result.completed, updated_at: result.updated_at }
              : task
          )
        );
      } catch (error) {
        // Rollback on error
        setTasks(previousTasks);
        onError?.("Failed to update task. Please try again.");
      } finally {
        setIsToggling((prev) => {
          const next = new Set(prev);
          next.delete(taskId);
          return next;
        });
      }
    },
    [tasks, userId, onError]
  );

  /**
   * Optimistically delete task.
   * Removes from UI immediately, then syncs with server.
   * Rolls back on error.
   */
  const optimisticDelete = useCallback(
    async (taskId: number) => {
      // Mark as deleting
      setIsDeleting((prev) => new Set(prev).add(taskId));

      // Store previous state for rollback
      const previousTasks = tasks;

      // Optimistically remove from UI
      setTasks((current) => current.filter((task) => task.id !== taskId));

      try {
        // Sync with server
        await api.deleteTask(userId, taskId);
      } catch (error) {
        // Rollback on error
        setTasks(previousTasks);
        onError?.("Failed to delete task. Please try again.");
      } finally {
        setIsDeleting((prev) => {
          const next = new Set(prev);
          next.delete(taskId);
          return next;
        });
      }
    },
    [tasks, userId, onError]
  );

  return {
    tasks,
    setTasks,
    optimisticToggle,
    optimisticDelete,
    isToggling,
    isDeleting,
  };
}

export default useOptimisticTasks;
