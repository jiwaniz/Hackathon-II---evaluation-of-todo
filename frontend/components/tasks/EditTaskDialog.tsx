"use client";

/**
 * EditTaskDialog component - Modal wrapper for editing existing tasks.
 *
 * Features:
 * - Overlay with backdrop
 * - Close on escape key
 * - Close on backdrop click
 * - Pre-filled form with task data
 * - Update task via API
 *
 * Reference: specs/ui/components.md, specs/features/task-crud.md
 */

import { useEffect, useCallback, useState } from "react";
import type { Task, TaskUpdate, Priority } from "@/types";
import { PrioritySelect } from "@/components/ui/PrioritySelect";
import { TagInput } from "@/components/ui/TagInput";

interface EditTaskDialogProps {
  isOpen: boolean;
  task: Task | null;
  onClose: () => void;
  onSubmit: (taskId: number, data: TaskUpdate) => Promise<void>;
  isLoading?: boolean;
  availableTags?: string[];
}

export function EditTaskDialog({
  isOpen,
  task,
  onClose,
  onSubmit,
  isLoading = false,
  availableTags = [],
}: EditTaskDialogProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Priority>("medium");
  const [tags, setTags] = useState<string[]>([]);
  const [errors, setErrors] = useState<{ title?: string; general?: string }>({});

  // Reset form when task changes
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || "");
      setPriority(task.priority);
      setTags(task.tags || []);
      setErrors({});
    }
  }, [task]);

  // Handle escape key press
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape" && !isLoading) {
        onClose();
      }
    },
    [onClose, isLoading]
  );

  // Add/remove escape key listener
  useEffect(() => {
    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, handleKeyDown]);

  // Handle backdrop click
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && !isLoading) {
      onClose();
    }
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: { title?: string } = {};

    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.length > 200) {
      newErrors.title = "Title must be 200 characters or less";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm() || !task) {
      return;
    }

    try {
      const updateData: TaskUpdate = {};

      // Only include changed fields
      if (title.trim() !== task.title) {
        updateData.title = title.trim();
      }

      const newDescription = description.trim() || undefined;
      if (newDescription !== (task.description || undefined)) {
        updateData.description = newDescription ?? "";
      }

      if (priority !== task.priority) {
        updateData.priority = priority;
      }

      // Check if tags changed (compare sorted arrays)
      const sortedOldTags = [...(task.tags || [])].sort();
      const sortedNewTags = [...tags].sort();
      if (JSON.stringify(sortedOldTags) !== JSON.stringify(sortedNewTags)) {
        updateData.tags = tags;
      }

      // Only submit if there are changes
      if (Object.keys(updateData).length > 0) {
        await onSubmit(task.id, updateData);
      }

      onClose();
    } catch (error) {
      setErrors({
        general:
          error instanceof Error ? error.message : "An error occurred",
      });
    }
  };

  if (!isOpen || !task) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="edit-dialog-title"
    >
      <div className="w-full max-w-md bg-white rounded-lg shadow-xl animate-in zoom-in-95 duration-200">
        {/* Dialog Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2
            id="edit-dialog-title"
            className="text-lg font-semibold text-gray-900"
          >
            Edit Task
          </h2>
          <button
            onClick={onClose}
            disabled={isLoading}
            className="p-1 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Close dialog"
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
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Dialog Body */}
        <div className="p-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            {errors.general && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                {errors.general}
              </div>
            )}

            {/* Title Input */}
            <div>
              <label
                htmlFor="edit-title"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="edit-title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter task title"
                disabled={isLoading}
                className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed ${
                  errors.title ? "border-red-500" : "border-gray-300"
                }`}
                maxLength={200}
              />
              {errors.title && (
                <p className="mt-1 text-sm text-red-600">{errors.title}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">{title.length}/200</p>
            </div>

            {/* Description Textarea */}
            <div>
              <label
                htmlFor="edit-description"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Description
              </label>
              <textarea
                id="edit-description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter task description (optional)"
                disabled={isLoading}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                maxLength={1000}
              />
              <p className="mt-1 text-xs text-gray-500">
                {description.length}/1000
              </p>
            </div>

            {/* Priority Select */}
            <div>
              <label
                htmlFor="edit-priority"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Priority
              </label>
              <PrioritySelect
                id="edit-priority"
                value={priority}
                onChange={setPriority}
                disabled={isLoading}
              />
            </div>

            {/* Tags Input */}
            <div>
              <label
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Tags
              </label>
              <TagInput
                value={tags}
                onChange={setTags}
                suggestions={availableTags}
                disabled={isLoading}
                placeholder="Add tags..."
              />
            </div>

            {/* Form Actions */}
            <div className="flex justify-end gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                disabled={isLoading}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <svg
                      className="w-4 h-4 animate-spin"
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
                    Saving...
                  </span>
                ) : (
                  "Save Changes"
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default EditTaskDialog;
