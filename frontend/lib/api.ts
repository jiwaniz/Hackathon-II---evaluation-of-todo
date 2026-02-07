/**
 * API client for communicating with the FastAPI backend.
 *
 * This client automatically injects the Authorization header with the JWT token
 * and handles common error scenarios.
 */

import type { Task, TaskCreate, TaskUpdate, Priority, Tag } from "../types";
import { getAuthToken } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * API response wrapper type.
 */
interface ApiResponse<T> {
  data: T;
  message?: string;
}

/**
 * API error response type.
 */
interface ApiError {
  error: {
    code: string;
    message: string;
  };
}

/**
 * Pagination info from list responses.
 */
interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  pages: number;
}

/**
 * Task list response with pagination.
 */
interface TaskListResponse {
  tasks: Task[];
  pagination: PaginationInfo;
}

/**
 * Tag list response.
 */
interface TagListResponse {
  tags: Tag[];
}

/**
 * Custom error class for API errors.
 */
export class ApiClientError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

/**
 * Get the auth token from Better Auth session.
 * This should be called from client components.
 */
async function getToken(): Promise<string | null> {
  if (typeof window !== "undefined") {
    return getAuthToken();
  }
  return null;
}

/**
 * Make an authenticated API request.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({
      error: { code: "UNKNOWN", message: "An unknown error occurred" },
    }));

    // Handle session expiration (T140)
    if (response.status === 401) {
      // Clear the stored token
      if (typeof window !== "undefined") {
        localStorage.removeItem("auth_token");
        // Redirect to login page
        window.location.href = "/login?expired=true";
      }
    }

    throw new ApiClientError(
      errorData.error.code,
      errorData.error.message,
      response.status
    );
  }

  return response.json();
}

/**
 * API client object with all available methods.
 */
export const api = {
  // ============================================
  // Task Operations
  // ============================================

  /**
   * Get all tasks for a user.
   */
  async getTasks(
    userId: string,
    options?: {
      status?: "all" | "pending" | "completed";
      priority?: Priority;
      tag?: string;
      search?: string;
      sort?: "created_desc" | "created_asc" | "priority" | "title";
      page?: number;
      limit?: number;
    }
  ): Promise<TaskListResponse> {
    const params = new URLSearchParams();
    if (options?.status) params.set("status", options.status);
    if (options?.priority) params.set("priority", options.priority);
    if (options?.tag) params.set("tag", options.tag);
    if (options?.search) params.set("search", options.search);
    if (options?.sort) params.set("sort", options.sort);
    if (options?.page) params.set("page", options.page.toString());
    if (options?.limit) params.set("limit", options.limit.toString());

    const queryString = params.toString();
    const endpoint = `/api/${userId}/tasks${queryString ? `?${queryString}` : ""}`;

    const response = await fetchApi<ApiResponse<TaskListResponse>>(endpoint);
    return response.data;
  },

  /**
   * Get a single task by ID.
   */
  async getTask(userId: string, taskId: number): Promise<Task> {
    const response = await fetchApi<ApiResponse<Task>>(
      `/api/${userId}/tasks/${taskId}`
    );
    return response.data;
  },

  /**
   * Create a new task.
   */
  async createTask(userId: string, data: TaskCreate): Promise<Task> {
    const response = await fetchApi<ApiResponse<Task>>(
      `/api/${userId}/tasks`,
      {
        method: "POST",
        body: JSON.stringify(data),
      }
    );
    return response.data;
  },

  /**
   * Update an existing task.
   */
  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdate
  ): Promise<Task> {
    const response = await fetchApi<ApiResponse<Task>>(
      `/api/${userId}/tasks/${taskId}`,
      {
        method: "PUT",
        body: JSON.stringify(data),
      }
    );
    return response.data;
  },

  /**
   * Delete a task.
   */
  async deleteTask(userId: string, taskId: number): Promise<void> {
    await fetchApi(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  },

  /**
   * Toggle task completion status.
   */
  async toggleTask(
    userId: string,
    taskId: number
  ): Promise<{ id: number; completed: boolean; updated_at: string }> {
    const response = await fetchApi<
      ApiResponse<{ id: number; completed: boolean; updated_at: string }>
    >(`/api/${userId}/tasks/${taskId}/toggle`, {
      method: "PATCH",
    });
    return response.data;
  },

  // ============================================
  // Tag Operations
  // ============================================

  /**
   * Get all tags for a user.
   */
  async getTags(userId: string): Promise<TagListResponse> {
    const response = await fetchApi<ApiResponse<TagListResponse>>(
      `/api/${userId}/tags`
    );
    return response.data;
  },

  // ============================================
  // Chat Operations (Phase 3)
  // ============================================

  /**
   * Send a chat message to the AI assistant.
   */
  async sendChatMessage(
    userId: string,
    data: { message: string; conversation_id?: number }
  ): Promise<{
    data: {
      conversation_id: number;
      response: string;
      tool_calls: Array<{ tool: string; input: Record<string, unknown>; output: Record<string, unknown> }>;
    };
  }> {
    return fetchApi(`/api/${userId}/chat`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  /**
   * Get all conversations for a user.
   */
  async getConversations(
    userId: string
  ): Promise<{
    data: {
      conversations: Array<{ id: number; created_at: string; updated_at: string; message_count?: number }>;
    };
  }> {
    return fetchApi(`/api/${userId}/conversations`);
  },

  /**
   * Get messages for a conversation.
   */
  async getConversationMessages(
    userId: string,
    conversationId: number
  ): Promise<{
    data: {
      messages: Array<{
        id: number;
        role: "user" | "assistant";
        content: string;
        tool_calls?: Array<{ tool: string; input: Record<string, unknown>; output: Record<string, unknown> }>;
        created_at: string;
      }>;
    };
  }> {
    return fetchApi(`/api/${userId}/conversations/${conversationId}/messages`);
  },

  // ============================================
  // Health Check
  // ============================================

  /**
   * Check if the API is healthy.
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return fetchApi("/health");
  },
};

export default api;
