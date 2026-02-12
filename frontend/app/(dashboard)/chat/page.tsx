"use client";

import { useChat } from "@/hooks/useChat";
import ChatWindow from "@/components/chat/ChatWindow";
import { useCurrentUser } from "@/lib/supabase";

export default function ChatPage() {
  const { user, isLoading: authLoading } = useCurrentUser();
  const userId = user?.id ?? "";

  const { messages, isLoading, error, sendMessage } = useChat({ userId });

  if (authLoading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

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
