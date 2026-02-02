"use client";

/**
 * CreateTaskDialog component - Modal wrapper for TaskForm.
 *
 * Features:
 * - Overlay with backdrop
 * - Close on escape key
 * - Close on backdrop click
 * - Animated open/close
 *
 * Reference: specs/ui/components.md (TaskModal)
 */

import { useEffect, useCallback } from "react";
import { TaskForm } from "./TaskForm";
import type { TaskCreate } from "@/types";

interface CreateTaskDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: TaskCreate) => Promise<void>;
  isLoading?: boolean;
}

export function CreateTaskDialog({
  isOpen,
  onClose,
  onSubmit,
  isLoading = false,
}: CreateTaskDialogProps) {
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
      // Prevent body scroll when modal is open
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

  // Handle form submission
  const handleSubmit = async (data: TaskCreate) => {
    await onSubmit(data);
    onClose();
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
    >
      <div className="w-full max-w-md bg-white rounded-lg shadow-xl animate-in zoom-in-95 duration-200">
        {/* Dialog Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 id="dialog-title" className="text-lg font-semibold text-gray-900">
            Create New Task
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
          <TaskForm
            onSubmit={handleSubmit}
            onCancel={onClose}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}

export default CreateTaskDialog;
