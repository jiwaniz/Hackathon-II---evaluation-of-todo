"use client";

import { useChat } from "@/hooks/useChat";
import ChatWindow from "@/components/chat/ChatWindow";

export default function ChatPage() {
  // TODO: Replace with actual user ID from Supabase auth session
  const userId = "demo-user";

  const { messages, isLoading, error, sendMessage } = useChat({ userId });

  return (
    <div className="mx-auto flex h-[calc(100vh-4rem)] max-w-3xl flex-col p-4">
      {error && (
        <div className="mb-2 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-700">
          {error}
        </div>
      )}
      <ChatWindow messages={messages} onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
}
