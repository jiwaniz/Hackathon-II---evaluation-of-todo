"use client";

/**
 * Skeleton component - loading placeholders for content.
 *
 * Features:
 * - Animated pulse effect
 * - Various preset shapes (text, card, avatar, etc.)
 * - Customizable width, height, and styling
 * - Accessible with aria-busy and aria-label
 *
 * Reference: specs/ui/components.md (T142)
 */

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  variant?: "text" | "circular" | "rectangular" | "rounded";
}

export function Skeleton({
  className = "",
  width,
  height,
  variant = "text",
}: SkeletonProps) {
  const baseClasses = "animate-pulse bg-gray-200";

  const variantClasses = {
    text: "rounded",
    circular: "rounded-full",
    rectangular: "",
    rounded: "rounded-lg",
  };

  const style: React.CSSProperties = {};
  if (width) style.width = typeof width === "number" ? `${width}px` : width;
  if (height) style.height = typeof height === "number" ? `${height}px` : height;

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      style={style}
      aria-busy="true"
      aria-label="Loading..."
    />
  );
}

/**
 * TaskCardSkeleton - skeleton placeholder for a task card.
 */
export function TaskCardSkeleton() {
  return (
    <div className="p-4 bg-white border border-gray-200 rounded-lg" aria-busy="true">
      <div className="flex items-start gap-3">
        {/* Checkbox placeholder */}
        <Skeleton variant="circular" width={20} height={20} className="mt-1 flex-shrink-0" />

        <div className="flex-1 min-w-0">
          {/* Title */}
          <Skeleton variant="text" height={20} className="w-3/4 mb-2" />

          {/* Description */}
          <Skeleton variant="text" height={14} className="w-full mb-1" />
          <Skeleton variant="text" height={14} className="w-2/3 mb-3" />

          {/* Tags and metadata */}
          <div className="flex items-center gap-2">
            <Skeleton variant="rounded" width={60} height={20} />
            <Skeleton variant="rounded" width={50} height={20} />
            <Skeleton variant="text" width={80} height={12} className="ml-auto" />
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2 flex-shrink-0">
          <Skeleton variant="rounded" width={32} height={32} />
          <Skeleton variant="rounded" width={32} height={32} />
        </div>
      </div>
    </div>
  );
}

/**
 * TaskListSkeleton - skeleton placeholder for a list of tasks.
 */
export function TaskListSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading tasks...">
      {Array.from({ length: count }).map((_, index) => (
        <TaskCardSkeleton key={index} />
      ))}
    </div>
  );
}

/**
 * FilterBarSkeleton - skeleton placeholder for the filter bar.
 */
export function FilterBarSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true">
      {/* Search bar */}
      <Skeleton variant="rounded" height={40} className="w-full" />

      {/* Filters row */}
      <div className="flex flex-col gap-3 sm:flex-row">
        <Skeleton variant="rounded" height={38} className="w-full sm:w-36" />
        <Skeleton variant="rounded" height={38} className="w-full sm:w-36" />
        <Skeleton variant="rounded" height={38} className="w-full sm:w-36" />
        <Skeleton variant="rounded" height={38} className="w-full sm:w-40" />
      </div>
    </div>
  );
}

/**
 * PageHeaderSkeleton - skeleton placeholder for page headers.
 */
export function PageHeaderSkeleton() {
  return (
    <div className="flex items-center justify-between" aria-busy="true">
      <div>
        <Skeleton variant="text" width={150} height={28} className="mb-2" />
        <Skeleton variant="text" width={250} height={16} />
      </div>
      <Skeleton variant="rounded" width={100} height={40} />
    </div>
  );
}

export default Skeleton;
