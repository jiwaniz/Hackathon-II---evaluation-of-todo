/**
 * TagBadge component - displays a tag as a small badge/chip.
 *
 * Features:
 * - Compact gray styling
 * - Optional remove button for editable contexts
 * - Optional click handler for filtering
 *
 * Reference: specs/ui/components.md
 */

interface TagBadgeProps {
  name: string;
  onRemove?: () => void;
  onClick?: () => void;
  className?: string;
}

export function TagBadge({ name, onRemove, onClick, className = "" }: TagBadgeProps) {
  const isClickable = !!onClick;
  const isRemovable = !!onRemove;

  return (
    <span
      className={`inline-flex items-center rounded-md bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600 ${
        isClickable ? "cursor-pointer hover:bg-gray-200" : ""
      } ${className}`}
      onClick={onClick}
      role={isClickable ? "button" : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onKeyDown={
        isClickable
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
    >
      {name}
      {isRemovable && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-1 -mr-0.5 h-3.5 w-3.5 rounded-full inline-flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-gray-400"
          aria-label={`Remove ${name} tag`}
        >
          <svg
            className="h-2.5 w-2.5"
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
      )}
    </span>
  );
}

export default TagBadge;
