"use client";

/**
 * TagInput component - input field for adding/removing tags.
 *
 * Features:
 * - Text input for new tags
 * - Enter or comma to add tag
 * - Display existing tags as removable badges
 * - Suggestions dropdown from existing user tags
 *
 * Reference: specs/ui/components.md
 */

import { useState, useRef, useEffect } from "react";
import { TagBadge } from "./TagBadge";

interface TagInputProps {
  value: string[];
  onChange: (tags: string[]) => void;
  suggestions?: string[];
  placeholder?: string;
  disabled?: boolean;
  className?: string;
}

export function TagInput({
  value,
  onChange,
  suggestions = [],
  placeholder = "Add tags...",
  disabled = false,
  className = "",
}: TagInputProps) {
  const [inputValue, setInputValue] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Filter suggestions based on input and exclude already selected tags
  const filteredSuggestions = suggestions.filter(
    (s) =>
      s.toLowerCase().includes(inputValue.toLowerCase()) &&
      !value.includes(s.toLowerCase())
  );

  // Close suggestions on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const addTag = (tagName: string) => {
    const normalized = tagName.trim().toLowerCase();
    if (normalized && !value.includes(normalized)) {
      onChange([...value, normalized]);
    }
    setInputValue("");
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  const removeTag = (tagName: string) => {
    onChange(value.filter((t) => t !== tagName));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      if (inputValue.trim()) {
        addTag(inputValue);
      }
    } else if (e.key === "Backspace" && !inputValue && value.length > 0) {
      // Remove last tag when backspacing on empty input
      removeTag(value[value.length - 1]);
    } else if (e.key === "Escape") {
      setShowSuggestions(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    // Check for comma and add tag if present
    if (newValue.includes(",")) {
      const parts = newValue.split(",");
      parts.forEach((part, index) => {
        if (index < parts.length - 1 && part.trim()) {
          addTag(part);
        }
      });
      setInputValue(parts[parts.length - 1]);
    } else {
      setInputValue(newValue);
    }
    setShowSuggestions(true);
  };

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      <div
        className={`flex flex-wrap gap-1 p-2 border border-gray-300 rounded-md bg-white focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
        onClick={() => inputRef.current?.focus()}
      >
        {/* Selected tags */}
        {value.map((tag) => (
          <TagBadge
            key={tag}
            name={tag}
            onRemove={disabled ? undefined : () => removeTag(tag)}
          />
        ))}

        {/* Input field */}
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(true)}
          placeholder={value.length === 0 ? placeholder : ""}
          disabled={disabled}
          className="flex-1 min-w-[100px] border-none outline-none text-sm bg-transparent disabled:cursor-not-allowed"
          aria-label="Tag input"
        />
      </div>

      {/* Suggestions dropdown */}
      {showSuggestions && filteredSuggestions.length > 0 && !disabled && (
        <ul
          className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-48 overflow-auto"
          role="listbox"
        >
          {filteredSuggestions.map((suggestion) => (
            <li
              key={suggestion}
              onClick={() => addTag(suggestion)}
              className="px-3 py-2 text-sm cursor-pointer hover:bg-gray-100"
              role="option"
              aria-selected="false"
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}

      {/* Help text */}
      <p className="mt-1 text-xs text-gray-500">
        Press Enter or comma to add a tag
      </p>
    </div>
  );
}

export default TagInput;
