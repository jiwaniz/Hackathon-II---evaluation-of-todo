# MCP Tools Contract

## Tool: add_task

| Field | Value |
|-------|-------|
| Purpose | Create a new task |
| Parameters | `user_id` (string, required), `title` (string, required), `description` (string, optional) |
| Returns | `{task_id, status: "created", title}` |

## Tool: list_tasks

| Field | Value |
|-------|-------|
| Purpose | Retrieve user's tasks with optional status filter |
| Parameters | `user_id` (string, required), `status` (string, optional: "all", "pending", "completed") |
| Returns | Array of `{id, title, completed, description}` |

## Tool: complete_task

| Field | Value |
|-------|-------|
| Purpose | Mark a task as complete |
| Parameters | `user_id` (string, required), `task_id` (integer, required) |
| Returns | `{task_id, status: "completed", title}` |

## Tool: delete_task

| Field | Value |
|-------|-------|
| Purpose | Remove a task |
| Parameters | `user_id` (string, required), `task_id` (integer, required) |
| Returns | `{task_id, status: "deleted", title}` |

## Tool: update_task

| Field | Value |
|-------|-------|
| Purpose | Modify task title or description |
| Parameters | `user_id` (string, required), `task_id` (integer, required), `title` (string, optional), `description` (string, optional) |
| Returns | `{task_id, status: "updated", title}` |

## Security Invariant

All tools receive `user_id` from the authenticated session (JWT sub claim), never from the AI agent's interpretation of user input. The MCP server enforces user-scoped queries.
