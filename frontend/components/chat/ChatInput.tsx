"use client";

import { useState, type FormEvent, type KeyboardEvent } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [showHelp, setShowHelp] = useState(false);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = message.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setMessage("");
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <div className="border-t border-gray-200">
      {/* Collapsible help tips */}
      {showHelp && (
        <div className="bg-blue-50 px-4 py-2 text-xs text-blue-800">
          <p className="font-medium mb-1">Example commands:</p>
          <ul className="space-y-0.5 text-blue-700">
            <li>&bull; &quot;Create a task Buy groceries with high priority&quot;</li>
            <li>&bull; &quot;Show my tasks&quot;</li>
            <li>&bull; &quot;Mark Buy groceries as complete&quot;</li>
            <li>&bull; &quot;Update priority of Buy groceries to low&quot;</li>
            <li>&bull; &quot;Delete task Buy groceries&quot;</li>
          </ul>
        </div>
      )}
      <form onSubmit={handleSubmit} className="flex items-center gap-2 p-4">
        <button
          type="button"
          onClick={() => setShowHelp(!showHelp)}
          className="flex-shrink-0 rounded-full p-1.5 text-gray-400 hover:bg-gray-100 hover:text-blue-600"
          title="Show example commands"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
          </svg>
        </button>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="flex-shrink-0 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
