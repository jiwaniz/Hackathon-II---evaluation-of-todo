"use client";

import type { ChatMessage } from "@/types/chat";

interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div
        className={`max-w-[75%] rounded-lg px-4 py-2 text-sm ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-gray-100 text-gray-900"
        }`}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>
        {message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-2 border-t border-gray-200 pt-1 text-xs opacity-70">
            {message.tool_calls.map((tc, i) => (
              <span key={i} className="mr-2 inline-block rounded bg-gray-200 px-1 text-gray-700">
                {tc.tool}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
