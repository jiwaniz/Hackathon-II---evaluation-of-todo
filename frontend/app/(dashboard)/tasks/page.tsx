"use client";

/**
 * Tasks Dashboard Page
 *
 * Main page for viewing and managing tasks.
 * Features:
 * - "Add Task" button to open create dialog
 * - Task list display with loading states
 * - Empty state when no tasks exist
 *
 * Reference: specs/ui/pages.md, specs/features/task-crud.md
 */

import { useState, useEffect, useCallback } from "react";
import { useCurrentUser } from "@/lib/auth-client";
import { api } from "@/lib/api";
import { CreateTaskDialog } from "@/components/tasks/CreateTaskDialog";
import { EditTaskDialog } from "@/components/tasks/EditTaskDialog";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { TaskList } from "@/components/tasks/TaskList";
import { FilterBar, type FilterState } from "@/components/filters/FilterBar";
import type { Task, TaskCreate, TaskUpdate, Priority } from "@/types";

export default function TasksPage() {
  const { user, isLoading: isUserLoading } = useCurrentUser();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoadingTasks, setIsLoadingTasks] = useState(true);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Filter state
  const [filters, setFilters] = useState<FilterState>({
    search: "",
    status: "all",
    priority: "all",
    tag: "",
    sort: "created_desc",
  });

  // Available tags for the filter dropdown
  const [availableTags, setAvailableTags] = useState<string[]>([]);

  // Fetch available tags
  const fetchTags = useCallback(async () => {
    if (!user?.id) return;

    try {
      const response = await api.getTags(user.id);
      setAvailableTags(response.tags.map((t) => t.name));
    } catch (error) {
      console.error("Failed to fetch tags:", error);
    }
  }, [user?.id]);

  // Fetch tags on mount
  useEffect(() => {
    if (user?.id) {
      fetchTags();
    }
  }, [user?.id, fetchTags]);

  // Fetch tasks when user is loaded or filters change
  const fetchTasks = useCallback(async () => {
    if (!user?.id) return;

    setIsLoadingTasks(true);
    setErrorMessage(null);
    try {
      const response = await api.getTasks(user.id, {
        search: filters.search || undefined,
        status: filters.status === "all" ? undefined : filters.status,
        priority: filters.priority === "all" ? undefined : (filters.priority as Priority),
        tag: filters.tag || undefined,
        sort: filters.sort,
      });
      setTasks(response.tasks);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
      setErrorMessage("Failed to load tasks. Please try again.");
    } finally {
      setIsLoadingTasks(false);
    }
  }, [user?.id, filters]);

  useEffect(() => {
    if (user?.id) {
      fetchTasks();
    }
  }, [user?.id, fetchTasks]);

  const handleCreateTask = async (data: TaskCreate) => {
    if (!user?.id) return;

    setIsCreating(true);
    try {
      const task = await api.createTask(user.id, data);
      setSuccessMessage(`Task "${task.title}" created successfully!`);
      // Refresh the task list
      await fetchTasks();
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (error) {
      console.error("Failed to create task:", error);
      throw error;
    } finally {
      setIsCreating(false);
    }
  };

  const handleToggleTask = async (taskId: number) => {
    if (!user?.id) return;

    try {
      await api.toggleTask(user.id, taskId);
      // Refresh the task list
      await fetchTasks();
    } catch (error) {
      console.error("Failed to toggle task:", error);
      setErrorMessage("Failed to update task. Please try again.");
      setTimeout(() => setErrorMessage(null), 3000);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsEditDialogOpen(true);
  };

  const handleUpdateTask = async (taskId: number, data: TaskUpdate) => {
    if (!user?.id) return;

    setIsUpdating(true);
    try {
      const updatedTask = await api.updateTask(user.id, taskId, data);
      setSuccessMessage(`Task "${updatedTask.title}" updated successfully!`);
      // Refresh the task list
      await fetchTasks();
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (error) {
      console.error("Failed to update task:", error);
      throw error;
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCloseEditDialog = () => {
    setIsEditDialogOpen(false);
    setEditingTask(null);
  };

  const handleDeleteTask = (taskId: number) => {
    const task = tasks.find((t) => t.id === taskId);
    if (task) {
      setDeletingTask(task);
      setIsDeleteDialogOpen(true);
    }
  };

  const handleConfirmDelete = async () => {
    if (!user?.id || !deletingTask) return;

    setIsDeleting(true);
    try {
      await api.deleteTask(user.id, deletingTask.id);
      setSuccessMessage(`Task "${deletingTask.title}" deleted successfully!`);
      setIsDeleteDialogOpen(false);
      setDeletingTask(null);
      // Refresh the task list
      await fetchTasks();
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (error) {
      console.error("Failed to delete task:", error);
      setErrorMessage("Failed to delete task. Please try again.");
      setTimeout(() => setErrorMessage(null), 3000);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleCancelDelete = () => {
    setIsDeleteDialogOpen(false);
    setDeletingTask(null);
  };

  if (isUserLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="flex items-center gap-2 text-gray-500">
          <svg
            className="w-5 h-5 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your tasks and stay organized
          </p>
        </div>

        {/* Add Task Button */}
        <button
          onClick={() => setIsCreateDialogOpen(true)}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          Add Task
        </button>
      </div>

      {/* Search and Filters */}
      <FilterBar
        filters={filters}
        onFilterChange={setFilters}
        availableTags={availableTags}
      />

      {/* Success Message */}
      {successMessage && (
        <div className="p-4 text-sm text-green-700 bg-green-50 border border-green-200 rounded-md">
          {successMessage}
        </div>
      )}

      {/* Error Message */}
      {errorMessage && (
        <div className="p-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded-md">
          {errorMessage}
        </div>
      )}

      {/* Task List */}
      <TaskList
        tasks={tasks}
        isLoading={isLoadingTasks}
        onToggle={handleToggleTask}
        onEdit={handleEditTask}
        onDelete={handleDeleteTask}
        onCreateTask={() => setIsCreateDialogOpen(true)}
        hasActiveFilters={
          !!filters.search ||
          filters.status !== "all" ||
          filters.priority !== "all" ||
          !!filters.tag
        }
        onClearFilters={() => {
          setFilters({
            search: "",
            status: "all",
            priority: "all",
            tag: "",
            sort: "created_desc",
          });
        }}
      />

      {/* Floating Add Button (mobile) */}
      <button
        onClick={() => setIsCreateDialogOpen(true)}
        className="fixed bottom-6 right-6 p-4 text-white bg-blue-600 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors md:hidden"
        aria-label="Add Task"
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
      </button>

      {/* Create Task Dialog */}
      <CreateTaskDialog
        isOpen={isCreateDialogOpen}
        onClose={() => setIsCreateDialogOpen(false)}
        onSubmit={handleCreateTask}
        isLoading={isCreating}
      />

      {/* Edit Task Dialog */}
      <EditTaskDialog
        isOpen={isEditDialogOpen}
        task={editingTask}
        onClose={handleCloseEditDialog}
        onSubmit={handleUpdateTask}
        isLoading={isUpdating}
      />

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        title="Delete Task"
        message={`Are you sure you want to delete "${deletingTask?.title}"? This action cannot be undone.`}
        confirmLabel="Delete"
        cancelLabel="Cancel"
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        isLoading={isDeleting}
        variant="danger"
      />
    </div>
  );
}
