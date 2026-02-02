/**
 * TypeScript types for the Evolution of Todo frontend.
 *
 * These types mirror the backend Pydantic schemas and SQLModel models.
 */

// ============================================
// Enums
// ============================================

/**
 * Task priority levels.
 */
export type Priority = "high" | "medium" | "low";

/**
 * Task status filter options.
 */
export type TaskStatus = "all" | "pending" | "completed";

/**
 * Task sort options.
 */
export type TaskSort = "created_desc" | "created_asc" | "priority" | "title";

// ============================================
// User Types
// ============================================

/**
 * User object from the API.
 */
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
}

/**
 * User registration data.
 */
export interface UserCreate {
  email: string;
  password: string;
  name?: string;
}

/**
 * User login data.
 */
export interface UserLogin {
  email: string;
  password: string;
}

/**
 * Authentication response from login/register.
 */
export interface AuthResponse {
  user: User;
  token: string;
  expires_at: string;
}

/**
 * Session response from session check.
 */
export interface SessionResponse {
  user: User;
  expires_at: string;
}

// ============================================
// Task Types
// ============================================

/**
 * Task object from the API.
 */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
  tags: string[];
  created_at: string;
  updated_at: string;
}

/**
 * Data for creating a new task.
 */
export interface TaskCreate {
  title: string;
  description?: string;
  priority?: Priority;
  tags?: string[];
}

/**
 * Data for updating an existing task.
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: Priority;
  tags?: string[];
}

/**
 * Task toggle response.
 */
export interface TaskToggleResponse {
  id: number;
  completed: boolean;
  updated_at: string;
}

// ============================================
// Tag Types
// ============================================

/**
 * Tag object from the API.
 */
export interface Tag {
  id: number;
  name: string;
  created_at: string;
}

// ============================================
// Pagination Types
// ============================================

/**
 * Pagination metadata.
 */
export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  pages: number;
}

/**
 * Paginated task list response.
 */
export interface TaskListResponse {
  tasks: Task[];
  pagination: PaginationInfo;
}

// ============================================
// Filter Types
// ============================================

/**
 * Task filter options for the API.
 */
export interface TaskFilters {
  status?: TaskStatus;
  priority?: Priority;
  tag?: string;
  search?: string;
  sort?: TaskSort;
  page?: number;
  limit?: number;
}

// ============================================
// API Response Types
// ============================================

/**
 * Standard API success response wrapper.
 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

/**
 * Standard API error response.
 */
export interface ApiError {
  error: {
    code: string;
    message: string;
  };
}

// ============================================
// Component Props Types
// ============================================

/**
 * Props for components that need the current user.
 */
export interface WithUserProps {
  user: User;
}

/**
 * Props for task-related components.
 */
export interface TaskCardProps {
  task: Task;
  onToggle?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

/**
 * Props for the task form.
 */
export interface TaskFormProps {
  initialData?: TaskCreate;
  onSubmit: (data: TaskCreate) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
}

/**
 * Props for filter components.
 */
export interface FilterProps {
  value: string;
  onChange: (value: string) => void;
}
