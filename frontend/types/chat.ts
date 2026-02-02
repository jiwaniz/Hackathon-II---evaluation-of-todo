/**
 * TypeScript types for the Phase 3 AI chatbot.
 */

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ToolCall {
  tool: "add_task" | "list_tasks" | "complete_task" | "delete_task" | "update_task";
  input: Record<string, unknown>;
  output: Record<string, unknown>;
}

export interface ChatResponse {
  data: {
    conversation_id: number;
    response: string;
    tool_calls: ToolCall[];
  };
}

export interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

export interface Conversation {
  id: number;
  created_at: string;
  updated_at: string;
  message_count?: number;
}

export interface ConversationListResponse {
  data: {
    conversations: Conversation[];
  };
}

export interface MessageListResponse {
  data: {
    messages: ChatMessage[];
  };
}
