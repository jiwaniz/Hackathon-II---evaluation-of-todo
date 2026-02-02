"use client";

import { useCallback, useState } from "react";
import type { ChatMessage, ChatResponse } from "@/types/chat";
import { api } from "@/lib/api";

interface UseChatOptions {
  userId: string;
}

export function useChat({ userId }: UseChatOptions) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      // Optimistically add user message
      const tempId = Date.now();
      const userMessage: ChatMessage = {
        id: tempId,
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        const response = await api.sendChatMessage(userId, {
          message: content,
          conversation_id: conversationId ?? undefined,
        });

        const data = response.data;
        setConversationId(data.conversation_id);

        const assistantMessage: ChatMessage = {
          id: tempId + 1,
          role: "assistant",
          content: data.response,
          tool_calls: data.tool_calls,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const errorMsg =
          err instanceof Error ? err.message : "Failed to send message";
        setError(errorMsg);
        // Remove optimistic user message on error
        setMessages((prev) => prev.filter((m) => m.id !== tempId));
      } finally {
        setIsLoading(false);
      }
    },
    [userId, conversationId, isLoading]
  );

  const loadConversation = useCallback(
    async (convId: number) => {
      try {
        const response = await api.getConversationMessages(userId, convId);
        setMessages(response.data.messages);
        setConversationId(convId);
      } catch {
        setError("Failed to load conversation");
      }
    },
    [userId]
  );

  return {
    messages,
    conversationId,
    isLoading,
    error,
    sendMessage,
    loadConversation,
  };
}
