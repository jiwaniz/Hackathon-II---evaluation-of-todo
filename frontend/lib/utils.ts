/**
 * Utility functions for the Evolution of Todo frontend.
 */

import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind CSS classes with clsx.
 * Handles conditional classes and deduplication.
 *
 * @param inputs - Class values to merge
 * @returns Merged class string
 *
 * @example
 * ```tsx
 * <div className={cn("px-4 py-2", isActive && "bg-blue-500", className)} />
 * ```
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format a date for display.
 *
 * @param date - Date to format (string or Date object)
 * @param options - Intl.DateTimeFormat options
 * @returns Formatted date string
 *
 * @example
 * ```tsx
 * formatDate("2026-01-19T12:00:00Z") // "Jan 19, 2026"
 * formatDate(new Date(), { dateStyle: "full" }) // "Sunday, January 19, 2026"
 * ```
 */
export function formatDate(
  date: string | Date,
  options: Intl.DateTimeFormatOptions = {
    month: "short",
    day: "numeric",
    year: "numeric",
  }
): string {
  const dateObj = typeof date === "string" ? new Date(date) : date;
  return new Intl.DateTimeFormat("en-US", options).format(dateObj);
}

/**
 * Format a relative time (e.g., "2 hours ago").
 *
 * @param date - Date to format
 * @returns Relative time string
 *
 * @example
 * ```tsx
 * formatRelativeTime(new Date(Date.now() - 3600000)) // "1 hour ago"
 * ```
 */
export function formatRelativeTime(date: string | Date): string {
  const dateObj = typeof date === "string" ? new Date(date) : date;
  const now = new Date();
  const diffMs = now.getTime() - dateObj.getTime();
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffSecs < 60) return "just now";
  if (diffMins < 60) return `${diffMins} minute${diffMins === 1 ? "" : "s"} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? "" : "s"} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays === 1 ? "" : "s"} ago`;

  return formatDate(dateObj);
}

/**
 * Truncate text to a maximum length.
 *
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @param suffix - Suffix to add if truncated (default: "...")
 * @returns Truncated text
 *
 * @example
 * ```tsx
 * truncate("Hello World", 5) // "Hello..."
 * ```
 */
export function truncate(
  text: string,
  maxLength: number,
  suffix: string = "..."
): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - suffix.length) + suffix;
}

/**
 * Debounce a function call.
 *
 * @param fn - Function to debounce
 * @param delay - Delay in milliseconds
 * @returns Debounced function
 *
 * @example
 * ```tsx
 * const debouncedSearch = debounce((query) => search(query), 300);
 * ```
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

/**
 * Generate a random ID.
 *
 * @param length - Length of the ID (default: 8)
 * @returns Random ID string
 */
export function generateId(length: number = 8): string {
  return Math.random()
    .toString(36)
    .substring(2, 2 + length);
}

/**
 * Check if we're running on the server.
 */
export const isServer = typeof window === "undefined";

/**
 * Check if we're running on the client.
 */
export const isClient = !isServer;

/**
 * Sleep for a given number of milliseconds.
 * Useful for testing loading states.
 *
 * @param ms - Milliseconds to sleep
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Get the priority color classes for Tailwind.
 *
 * @param priority - Priority level
 * @returns Tailwind class string for background and text color
 */
export function getPriorityClasses(priority: "high" | "medium" | "low"): string {
  switch (priority) {
    case "high":
      return "bg-red-100 text-red-800";
    case "medium":
      return "bg-yellow-100 text-yellow-800";
    case "low":
      return "bg-green-100 text-green-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
}

/**
 * Get the status color classes for Tailwind.
 *
 * @param completed - Whether the task is completed
 * @returns Tailwind class string
 */
export function getStatusClasses(completed: boolean): string {
  return completed
    ? "text-green-600 line-through"
    : "text-gray-900";
}
