# Feature Specification: Phase II Full-Stack Web Application

**Feature Branch**: `002-phase2-fullstack-webapp`
**Created**: 2026-01-18
**Status**: Draft
**Phase**: Phase II of Evolution of Todo
**Input**: Transform Phase I console app into multi-user web application with persistence

## Overview

Transform the in-memory Python console Todo application (Phase I) into a production-ready, multi-user web application with persistent storage, user authentication, and a responsive modern UI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration & Authentication (Priority: P1)

A new user visits the Todo application and needs to create an account to manage their personal tasks securely. Existing users can log in to access their saved tasks.

**Why this priority**: Authentication is the foundation for multi-user support. Without it, tasks cannot be associated with users, making the entire application non-functional for the multi-user requirement.

**Independent Test**: Can be fully tested by registering a new account, logging out, and logging back in. Delivers secure access to personal task space.

**Acceptance Scenarios**:

1. **Given** a visitor on the landing page, **When** they click "Sign Up" and enter valid email/password, **Then** account is created and user is logged in automatically
2. **Given** a registered user on the login page, **When** they enter valid credentials, **Then** they are authenticated and redirected to their task dashboard
3. **Given** an authenticated user, **When** they click "Logout", **Then** their session ends and they are redirected to the landing page
4. **Given** an invalid login attempt, **When** wrong credentials are entered, **Then** user sees a clear error message without revealing which field is wrong

---

### User Story 2 - Create Task (Priority: P1)

An authenticated user wants to add a new task to their todo list with a title and optional description.

**Why this priority**: Creating tasks is the core functionality. Users cannot use the app meaningfully without being able to add tasks.

**Independent Test**: Can be tested by logging in and creating a task with title "Buy groceries" and description "Milk, eggs, bread". Task appears in the list immediately.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the dashboard, **When** they click "Add Task" and enter a title, **Then** a new task is created and appears in their task list
2. **Given** an authenticated user adding a task, **When** they provide both title and description, **Then** both are saved and visible in the task details
3. **Given** a user trying to add a task, **When** they submit without a title, **Then** validation error appears and task is not created

---

### User Story 3 - View All Tasks (Priority: P1)

An authenticated user wants to see all their tasks in a clear, organized list showing status, title, and key information.

**Why this priority**: Viewing tasks is essential for users to understand their workload and take action on items.

**Independent Test**: Can be tested by viewing the dashboard after creating multiple tasks. All tasks display with correct status indicators.

**Acceptance Scenarios**:

1. **Given** an authenticated user with tasks, **When** they visit the dashboard, **Then** they see all their tasks with status indicators (complete/incomplete)
2. **Given** a user viewing tasks, **When** they have no tasks, **Then** they see an empty state message encouraging them to create their first task
3. **Given** a user viewing their tasks, **When** another user has tasks, **Then** the first user cannot see the other user's tasks (isolation)

---

### User Story 4 - Update Task (Priority: P2)

An authenticated user wants to modify an existing task's title or description to correct mistakes or update information.

**Why this priority**: While important, updating is less critical than creating and viewing. Users can delete and recreate as a workaround.

**Independent Test**: Can be tested by editing an existing task's title from "Buy groceries" to "Buy organic groceries". Change persists after page refresh.

**Acceptance Scenarios**:

1. **Given** a user viewing their task list, **When** they click edit on a task and change the title, **Then** the updated title is saved and displayed
2. **Given** a user editing a task, **When** they clear the title field, **Then** validation prevents saving an empty title
3. **Given** a user editing task A, **When** another user tries to access the edit endpoint for task A, **Then** they receive an unauthorized error

---

### User Story 5 - Delete Task (Priority: P2)

An authenticated user wants to permanently remove a task they no longer need.

**Why this priority**: Important for list hygiene but can be worked around by marking complete. Requires confirmation to prevent accidents.

**Independent Test**: Can be tested by deleting a task and confirming it no longer appears in the list or database.

**Acceptance Scenarios**:

1. **Given** a user viewing their task list, **When** they click delete on a task and confirm, **Then** the task is permanently removed
2. **Given** a user clicking delete, **When** the confirmation dialog appears and they cancel, **Then** the task remains unchanged
3. **Given** a user attempting to delete another user's task via API, **When** the request is made, **Then** it is rejected with 403 Forbidden

---

### User Story 6 - Toggle Task Completion (Priority: P2)

An authenticated user wants to mark a task as complete or incomplete to track their progress.

**Why this priority**: Core to todo functionality but slightly less critical than CRUD basics. Simple one-click action.

**Independent Test**: Can be tested by clicking the checkbox on a pending task, seeing it marked complete, and clicking again to mark incomplete.

**Acceptance Scenarios**:

1. **Given** an incomplete task, **When** user clicks the completion toggle, **Then** task status changes to complete with visual indicator
2. **Given** a complete task, **When** user clicks the completion toggle, **Then** task status changes back to incomplete
3. **Given** a task being toggled, **When** the status changes, **Then** the change persists after page refresh

---

### User Story 7 - Set Task Priority (Priority: P3)

An authenticated user wants to assign priority levels (high, medium, low) to tasks to focus on what matters most.

**Why this priority**: Enhances organization but app is fully functional without priorities. Nice-to-have for power users.

**Independent Test**: Can be tested by creating a task and setting priority to "high", then verifying the priority indicator displays correctly.

**Acceptance Scenarios**:

1. **Given** a user creating or editing a task, **When** they select a priority level, **Then** the priority is saved and displayed with appropriate visual styling
2. **Given** a task without explicit priority, **When** viewed in the list, **Then** it defaults to "medium" priority

---

### User Story 8 - Add Tags/Categories to Tasks (Priority: P3)

An authenticated user wants to categorize tasks with tags (e.g., "work", "home", "urgent") for better organization.

**Why this priority**: Organizational enhancement. App works without tags. Can be implemented after core features.

**Independent Test**: Can be tested by adding tags "work" and "urgent" to a task, then viewing the task with both tags displayed.

**Acceptance Scenarios**:

1. **Given** a user creating or editing a task, **When** they add one or more tags, **Then** tags are saved and displayed on the task
2. **Given** a user adding tags, **When** they type a new tag name, **Then** it is created and available for future use

---

### User Story 9 - Search Tasks (Priority: P3)

An authenticated user wants to search their tasks by keyword to quickly find specific items.

**Why this priority**: Useful with many tasks but not essential for basic functionality. Users can scroll through lists initially.

**Independent Test**: Can be tested by searching for "groceries" and seeing only tasks containing that word in title or description.

**Acceptance Scenarios**:

1. **Given** a user with multiple tasks, **When** they type in the search box, **Then** task list filters to show only matching results
2. **Given** a search query, **When** no tasks match, **Then** user sees "No matching tasks found" message

---

### User Story 10 - Filter Tasks (Priority: P3)

An authenticated user wants to filter tasks by status, priority, or tags to focus on relevant items.

**Why this priority**: Enhances usability for users with many tasks. Basic viewing works without filters.

**Independent Test**: Can be tested by filtering by "completed" status and seeing only completed tasks in the list.

**Acceptance Scenarios**:

1. **Given** a user viewing tasks, **When** they select "Completed" filter, **Then** only completed tasks are displayed
2. **Given** a user with filtered results, **When** they clear filters, **Then** all tasks are shown again

---

### User Story 11 - Sort Tasks (Priority: P3)

An authenticated user wants to sort tasks by creation date, priority, or alphabetically to view them in preferred order.

**Why this priority**: Convenience feature. Default chronological order works for most use cases.

**Independent Test**: Can be tested by sorting by priority and seeing high-priority tasks appear first.

**Acceptance Scenarios**:

1. **Given** a user viewing tasks, **When** they select "Sort by Priority", **Then** tasks are reordered with high priority first
2. **Given** a user viewing tasks, **When** they select "Sort by Title", **Then** tasks are ordered alphabetically

---

### Edge Cases

- What happens when a user's session expires during task editing? (Show re-login prompt, preserve draft if possible)
- How does the system handle concurrent edits by the same user in multiple tabs? (Last write wins with timestamp check)
- What happens if the database connection fails? (Show user-friendly error, retry with exponential backoff)
- How are very long task titles handled? (Truncate at 200 characters with validation message)
- What happens when a user tries to access tasks via direct URL without authentication? (Redirect to login with return URL)

## Constraints *(mandatory)*

- **C-001**: No manual coding allowed. All implementation MUST be triggered by `@specs/features/*.md` references in Claude Code
- **C-002**: Root `CLAUDE.md` MUST strictly contain only `@AGENTS.md` as its first line (redirection pattern)
- **C-003**: All hosting MUST use free-tier services only (Vercel, Railway, Neon)
- **C-004**: Spec-driven development required - every feature requires specification first
- **C-005**: TDD mandatory - Red-Green-Refactor workflow for all implementation

## Requirements *(mandatory)*

### Technology Stack Requirements

- **TR-001**: Backend MUST use UV as the Python package manager (hackathon standard)
- **TR-002**: Backend MUST use SQLModel as the ORM for FastAPI/Neon integration (hackathon standard)
- **TR-003**: Frontend MUST use Better Auth with the JWT Plugin explicitly enabled
- **TR-004**: Backend MUST verify JWT tokens using the shared `BETTER_AUTH_SECRET` environment variable
- **TR-005**: Both frontend and backend MUST share the same `BETTER_AUTH_SECRET` for JWT signing/verification

### API Endpoint Pattern

All task endpoints MUST follow the `{user_id}` path pattern for explicit user scoping:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/toggle` | Toggle completion |

**Important**: The `{user_id}` in the URL MUST match the user ID extracted from the JWT token. Mismatches MUST return 403 Forbidden.

### Functional Requirements

**Authentication**
- **FR-001**: System MUST allow users to register with email and password
- **FR-002**: System MUST authenticate users using Better Auth with JWT Plugin and issue JWT tokens valid for 7 days
- **FR-003**: System MUST allow users to log out, invalidating their current session
- **FR-004**: System MUST require valid JWT token for all task-related API endpoints
- **FR-005**: System MUST extract user identity from JWT and filter data accordingly
- **FR-006**: FastAPI middleware MUST verify JWT signature using `BETTER_AUTH_SECRET` independently (no callback to frontend)

**Task Management**
- **FR-007**: System MUST allow authenticated users to create tasks with title (required) and description (optional)
- **FR-008**: System MUST allow authenticated users to view only their own tasks
- **FR-009**: System MUST allow authenticated users to update their own tasks
- **FR-010**: System MUST allow authenticated users to delete their own tasks
- **FR-011**: System MUST allow authenticated users to toggle task completion status
- **FR-012**: System MUST persist all task data to the database immediately upon change using SQLModel

**Organization Features**
- **FR-013**: System MUST allow users to assign priority (high/medium/low) to tasks
- **FR-014**: System MUST allow users to add multiple tags to tasks
- **FR-015**: System MUST allow users to search tasks by keyword in title and description
- **FR-016**: System MUST allow users to filter tasks by status, priority, and tags
- **FR-017**: System MUST allow users to sort tasks by creation date, priority, or title

**Security**
- **FR-018**: System MUST reject all API requests without valid Authorization header with 401 Unauthorized
- **FR-019**: System MUST reject attempts to access other users' tasks with 403 Forbidden
- **FR-020**: System MUST validate `{user_id}` in URL against JWT token user ID
- **FR-021**: System MUST validate all user input before processing
- **FR-022**: System MUST store passwords securely (never in plain text)

### Key Entities

- **User**: Represents a registered user with unique email, secure password hash, and account metadata
- **Task**: Represents a todo item belonging to a user, with title, description, completion status, priority, tags, and timestamps
- **Tag**: Represents a category label that can be applied to multiple tasks

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration and login in under 30 seconds
- **SC-002**: Creating a new task takes less than 3 seconds from click to confirmation
- **SC-003**: Task list loads within 2 seconds for up to 100 tasks
- **SC-004**: 100% of API requests without valid authentication receive 401 response
- **SC-005**: 100% of cross-user data access attempts receive 403 response
- **SC-006**: Search results appear within 1 second of typing
- **SC-007**: All user data persists correctly across browser sessions and device changes
- **SC-008**: Application remains responsive on mobile devices (320px to 768px viewport)
- **SC-009**: 95% of users can complete their first task creation without assistance

## Assumptions

- Users have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- Free-tier hosting limits are acceptable (Vercel, Railway, Neon free tiers)
- Email verification is not required for MVP (can be added later)
- Password recovery is out of scope for initial release
- Maximum 100 tasks per user is acceptable for MVP
- Tag management (delete, rename) is out of scope for initial release

## Out of Scope

- Email verification and password recovery flows
- Social login (Google, GitHub, etc.)
- Task sharing between users
- Task due dates and reminders (Phase III feature)
- Recurring tasks (Phase III feature)
- Real-time collaboration
- Mobile native apps
- Offline support

## Dependencies

- Phase I: In-Memory Console App (completed) - provides domain model reference
- Neon PostgreSQL free tier account
- Vercel free tier account for frontend hosting
- Railway or Vercel free tier for backend hosting
- Better Auth library with **JWT Plugin** for authentication
- UV package manager for Python backend
- SQLModel ORM for FastAPI/Neon integration
- Shared `BETTER_AUTH_SECRET` environment variable

## Architecture Reference

See separated specs for detailed technical specifications:

**Project Overview**
- `specs/overview.md` - Current phase, technology stack summary, and free-tier hosting details

**Feature Specifications**
- `specs/features/task-crud.md` - Task CRUD feature details
- `specs/features/authentication.md` - Authentication feature details with JWT Plugin

**Technical Specifications**
- `specs/api/rest-endpoints.md` - API endpoint specifications with `{user_id}` pattern
- `specs/database/schema.md` - SQLModel database schema design
- `specs/ui/components.md` - UI component specifications
- `specs/ui/pages.md` - Page layout specifications

**Agent Configuration**
- `CLAUDE.md` - Root file containing only `@AGENTS.md` (redirection pattern)
- `frontend/CLAUDE.md` - Next.js specific guidelines
- `backend/CLAUDE.md` - FastAPI specific guidelines with UV/SQLModel patterns
