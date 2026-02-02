"use client";

/**
 * TaskForm component for creating or editing tasks.
 *
 * Features:
 * - Title input (required)
 * - Description textarea (optional)
 * - Priority dropdown
 * - Submit and cancel buttons
 * - Validation messages
 *
 * Reference: specs/ui/components.md
 */

import { useState } from "react";
import type { TaskCreate, Priority } from "@/types";
import { PrioritySelect } from "@/components/ui/PrioritySelect";
import { TagInput } from "@/components/ui/TagInput";

interface TaskFormProps {
  initialData?: TaskCreate;
  onSubmit: (data: TaskCreate) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
  availableTags?: string[];
}

export function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
  availableTags = [],
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(
    initialData?.description || ""
  );
  const [priority, setPriority] = useState<Priority>(
    initialData?.priority || "medium"
  );
  const [tags, setTags] = useState<string[]>(initialData?.tags || []);
  const [errors, setErrors] = useState<{ title?: string; description?: string; general?: string }>(
    {}
  );
  const [touched, setTouched] = useState<{ title?: boolean; description?: boolean }>({});

  const validateField = (field: "title" | "description", value: string): string | undefined => {
    if (field === "title") {
      if (!value.trim()) {
        return "Title is required";
      } else if (value.trim().length < 1) {
        return "Title must be at least 1 character";
      } else if (value.length > 200) {
        return "Title must be 200 characters or less";
      }
    }
    if (field === "description") {
      if (value.length > 1000) {
        return "Description must be 1000 characters or less";
      }
    }
    return undefined;
  };

  const validateForm = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    const titleError = validateField("title", title);
    if (titleError) newErrors.title = titleError;

    const descError = validateField("description", description);
    if (descError) newErrors.description = descError;

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleBlur = (field: "title" | "description") => {
    setTouched({ ...touched, [field]: true });
    const value = field === "title" ? title : description;
    const error = validateField(field, value);
    setErrors({ ...errors, [field]: error });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        tags: tags.length > 0 ? tags : undefined,
      });
    } catch (error) {
      setErrors({
        general:
          error instanceof Error ? error.message : "An error occurred",
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {errors.general && (
        <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
          {errors.general}
        </div>
      )}

      {/* Title Input */}
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (touched.title) {
              const error = validateField("title", e.target.value);
              setErrors({ ...errors, title: error });
            }
          }}
          onBlur={() => handleBlur("title")}
          placeholder="Enter task title"
          disabled={isLoading}
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? "title-error" : undefined}
          className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed ${
            errors.title ? "border-red-500 focus:ring-red-500 focus:border-red-500" : "border-gray-300"
          }`}
          maxLength={200}
        />
        {errors.title && (
          <p id="title-error" className="mt-1 text-sm text-red-600 flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {errors.title}
          </p>
        )}
        <p className={`mt-1 text-xs ${title.length > 180 ? "text-amber-600" : "text-gray-500"}`}>
          {title.length}/200 {title.length > 180 && "(approaching limit)"}
        </p>
      </div>

      {/* Description Textarea */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => {
            setDescription(e.target.value);
            if (touched.description) {
              const error = validateField("description", e.target.value);
              setErrors({ ...errors, description: error });
            }
          }}
          onBlur={() => handleBlur("description")}
          placeholder="Enter task description (optional)"
          disabled={isLoading}
          rows={3}
          aria-invalid={!!errors.description}
          aria-describedby={errors.description ? "description-error" : undefined}
          className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed ${
            errors.description ? "border-red-500 focus:ring-red-500 focus:border-red-500" : "border-gray-300"
          }`}
          maxLength={1000}
        />
        {errors.description && (
          <p id="description-error" className="mt-1 text-sm text-red-600 flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {errors.description}
          </p>
        )}
        <p className={`mt-1 text-xs ${description.length > 900 ? "text-amber-600" : "text-gray-500"}`}>
          {description.length}/1000 {description.length > 900 && "(approaching limit)"}
        </p>
      </div>

      {/* Priority Select */}
      <div>
        <label
          htmlFor="priority"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Priority
        </label>
        <PrioritySelect
          id="priority"
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
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
        )}
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
          ) : initialData ? (
            "Update Task"
          ) : (
            "Create Task"
          )}
        </button>
      </div>
    </form>
  );
}

export default TaskForm;
