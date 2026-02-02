# UI Components

## Overview

React components built with Next.js 16+ App Router, TypeScript, and Tailwind CSS. Uses server components by default, client components only when interactivity is required.

## Component Library

### Layout Components

#### Header
- **Type**: Server Component
- **Location**: `components/layout/Header.tsx`
- **Purpose**: Application header with navigation and user menu
- **Props**: `user?: User`
- **Features**:
  - Logo/brand link to home
  - Navigation links (when authenticated)
  - User dropdown menu (profile, logout)
  - Login/Register buttons (when not authenticated)

#### Footer
- **Type**: Server Component
- **Location**: `components/layout/Footer.tsx`
- **Purpose**: Application footer with links and copyright
- **Props**: None

#### Sidebar
- **Type**: Client Component
- **Location**: `components/layout/Sidebar.tsx`
- **Purpose**: Collapsible sidebar for filters and navigation
- **Props**: `isOpen: boolean`, `onClose: () => void`
- **Features**:
  - Filter options (status, priority, tags)
  - Sort options
  - Mobile responsive (overlay on small screens)

---

### Authentication Components

#### LoginForm
- **Type**: Client Component
- **Location**: `components/auth/LoginForm.tsx`
- **Purpose**: Email/password login form
- **Props**: `onSuccess?: () => void`
- **Features**:
  - Email input with validation
  - Password input with visibility toggle
  - Submit button with loading state
  - Error message display
  - Link to registration

#### RegisterForm
- **Type**: Client Component
- **Location**: `components/auth/RegisterForm.tsx`
- **Purpose**: User registration form
- **Props**: `onSuccess?: () => void`
- **Features**:
  - Email input with validation
  - Password input with strength indicator
  - Confirm password field
  - Submit button with loading state
  - Error message display
  - Link to login

#### AuthGuard
- **Type**: Client Component
- **Location**: `components/auth/AuthGuard.tsx`
- **Purpose**: Protect routes requiring authentication
- **Props**: `children: React.ReactNode`
- **Features**:
  - Check session on mount
  - Redirect to login if not authenticated
  - Show loading spinner while checking

---

### Task Components

#### TaskCard
- **Type**: Client Component
- **Location**: `components/tasks/TaskCard.tsx`
- **Purpose**: Display individual task with actions
- **Props**:
  ```typescript
  {
    task: Task;
    onToggle: (id: number) => void;
    onEdit: (task: Task) => void;
    onDelete: (id: number) => void;
  }
  ```
- **Features**:
  - Checkbox for completion toggle
  - Title and description display
  - Priority badge (color-coded)
  - Tag chips
  - Edit and delete buttons
  - Strikethrough when completed
  - Hover state with actions

#### TaskList
- **Type**: Client Component
- **Location**: `components/tasks/TaskList.tsx`
- **Purpose**: Display list of tasks with loading/empty states
- **Props**:
  ```typescript
  {
    tasks: Task[];
    isLoading: boolean;
    onToggle: (id: number) => void;
    onEdit: (task: Task) => void;
    onDelete: (id: number) => void;
  }
  ```
- **Features**:
  - Map tasks to TaskCard components
  - Loading skeleton while fetching
  - Empty state with CTA to create first task
  - Pagination controls

#### TaskForm
- **Type**: Client Component
- **Location**: `components/tasks/TaskForm.tsx`
- **Purpose**: Create or edit task
- **Props**:
  ```typescript
  {
    task?: Task; // undefined for create, defined for edit
    onSubmit: (data: TaskFormData) => void;
    onCancel: () => void;
    isLoading: boolean;
  }
  ```
- **Features**:
  - Title input (required)
  - Description textarea (optional)
  - Priority dropdown
  - Tag input with autocomplete
  - Submit and cancel buttons
  - Validation messages

#### TaskModal
- **Type**: Client Component
- **Location**: `components/tasks/TaskModal.tsx`
- **Purpose**: Modal wrapper for TaskForm
- **Props**:
  ```typescript
  {
    isOpen: boolean;
    onClose: () => void;
    task?: Task;
    onSuccess: () => void;
  }
  ```
- **Features**:
  - Overlay with backdrop
  - Close on escape key
  - Close on backdrop click
  - Animated open/close

#### AddTaskButton
- **Type**: Client Component
- **Location**: `components/tasks/AddTaskButton.tsx`
- **Purpose**: Floating action button to add task
- **Props**: `onClick: () => void`
- **Features**:
  - Fixed position (bottom right)
  - Plus icon
  - Hover effect
  - Mobile friendly size

---

### Filter Components

#### SearchBar
- **Type**: Client Component
- **Location**: `components/filters/SearchBar.tsx`
- **Purpose**: Search tasks by keyword
- **Props**: `onSearch: (query: string) => void`
- **Features**:
  - Debounced input (300ms)
  - Clear button
  - Search icon
  - Placeholder text

#### FilterDropdown
- **Type**: Client Component
- **Location**: `components/filters/FilterDropdown.tsx`
- **Purpose**: Filter tasks by status/priority
- **Props**:
  ```typescript
  {
    label: string;
    options: { value: string; label: string }[];
    value: string;
    onChange: (value: string) => void;
  }
  ```

#### TagFilter
- **Type**: Client Component
- **Location**: `components/filters/TagFilter.tsx`
- **Purpose**: Filter tasks by tags
- **Props**:
  ```typescript
  {
    tags: Tag[];
    selected: string[];
    onChange: (tags: string[]) => void;
  }
  ```
- **Features**:
  - Multi-select chip buttons
  - Show tag count
  - Clear all button

#### SortDropdown
- **Type**: Client Component
- **Location**: `components/filters/SortDropdown.tsx`
- **Purpose**: Sort tasks
- **Props**:
  ```typescript
  {
    value: string;
    onChange: (value: string) => void;
  }
  ```
- **Options**:
  - Created (newest first)
  - Created (oldest first)
  - Priority (high to low)
  - Title (A-Z)

---

### Common Components

#### Button
- **Type**: Client Component
- **Location**: `components/ui/Button.tsx`
- **Variants**: primary, secondary, danger, ghost
- **Sizes**: sm, md, lg
- **Props**: `variant`, `size`, `isLoading`, `disabled`, `children`

#### Input
- **Type**: Client Component
- **Location**: `components/ui/Input.tsx`
- **Props**: `label`, `error`, `helperText`, standard input props

#### Modal
- **Type**: Client Component
- **Location**: `components/ui/Modal.tsx`
- **Props**: `isOpen`, `onClose`, `title`, `children`

#### Badge
- **Type**: Server Component
- **Location**: `components/ui/Badge.tsx`
- **Variants**: high (red), medium (yellow), low (green)
- **Props**: `variant`, `children`

#### Spinner
- **Type**: Server Component
- **Location**: `components/ui/Spinner.tsx`
- **Sizes**: sm, md, lg
- **Props**: `size`

#### Toast
- **Type**: Client Component
- **Location**: `components/ui/Toast.tsx`
- **Purpose**: Notification messages
- **Variants**: success, error, warning, info

---

## Styling Guidelines

### Tailwind CSS Classes

**Colors:**
- Primary: `bg-blue-600`, `text-blue-600`
- Success: `bg-green-600`, `text-green-600`
- Danger: `bg-red-600`, `text-red-600`
- Warning: `bg-yellow-600`, `text-yellow-600`

**Priority Colors:**
- High: `bg-red-100 text-red-800`
- Medium: `bg-yellow-100 text-yellow-800`
- Low: `bg-green-100 text-green-800`

**Spacing:**
- Component padding: `p-4`
- Section gap: `gap-6`
- Card padding: `p-6`

**Responsive:**
- Mobile first approach
- Breakpoints: `sm:`, `md:`, `lg:`, `xl:`
