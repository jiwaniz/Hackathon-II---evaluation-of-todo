# Feature: Task CRUD Operations

## Overview

Core task management functionality allowing authenticated users to create, read, update, and delete their personal tasks with persistence.

## User Stories

### Create Task
- As a user, I can create a new task with a title
- As a user, I can optionally add a description to my task
- As a user, I can set priority level (high/medium/low)
- As a user, I can add tags to categorize my task

### View Tasks
- As a user, I can see all my tasks in a list
- As a user, I can see task status (complete/incomplete)
- As a user, I can see task priority with visual indicators
- As a user, I can see tags associated with each task
- As a user, I cannot see other users' tasks

### Update Task
- As a user, I can edit my task's title
- As a user, I can edit my task's description
- As a user, I can change the priority level
- As a user, I can add or remove tags

### Delete Task
- As a user, I can delete my own tasks
- As a user, I must confirm before deletion
- As a user, I cannot delete other users' tasks

### Toggle Completion
- As a user, I can mark a task as complete
- As a user, I can mark a completed task as incomplete
- As a user, I can quickly toggle status with one click

## Acceptance Criteria

### Create Task
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Default priority is "medium"
- Task is associated with authenticated user
- Created timestamp is automatically set
- Task appears immediately in user's list

### View Tasks
- Only shows tasks for authenticated user
- Displays title, status indicator, priority, tags
- Shows creation date
- Empty state message when no tasks exist
- Supports pagination for large lists (>20 items)

### Update Task
- Only task owner can update
- Title cannot be empty after edit
- Updated timestamp is automatically set
- Changes persist immediately

### Delete Task
- Only task owner can delete
- Confirmation dialog before deletion
- Task is permanently removed
- Deletion is immediate and irreversible

### Toggle Completion
- Single click toggles status
- Visual feedback on status change
- Change persists to database immediately

## Data Model Reference

See [Database Schema](../database/schema.md) for Task entity definition.

## API Reference

See [REST Endpoints](../api/rest-endpoints.md) for task-related API routes:
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion

## UI Reference

See [Components](../ui/components.md) for:
- TaskCard component
- TaskForm component
- TaskList component
