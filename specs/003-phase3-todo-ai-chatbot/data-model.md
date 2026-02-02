# Data Model: Todo AI Chatbot

**Date**: 2026-02-01 | **Feature**: 003-phase3-todo-ai-chatbot

## Entities

### Task (existing - Phase 2)

| Field | Type | Constraints | Notes |
|-------|------|------------|-------|
| id | integer | PK, auto-increment | |
| user_id | string | FK → User.id, indexed | Owner |
| title | string | required, max 200 chars | |
| description | string | optional, max 1000 chars | |
| completed | boolean | default false, indexed | |
| priority | enum | high/medium/low, default medium | |
| created_at | datetime | auto-set | |
| updated_at | datetime | auto-set on change | |

### Conversation (new)

| Field | Type | Constraints | Notes |
|-------|------|------------|-------|
| id | integer | PK, auto-increment | |
| user_id | string | FK → User.id, indexed | Owner |
| created_at | datetime | auto-set | |
| updated_at | datetime | auto-set on change | |

**Relationships**: Has many Messages. Belongs to User.

### Message (new)

| Field | Type | Constraints | Notes |
|-------|------|------------|-------|
| id | integer | PK, auto-increment | |
| conversation_id | integer | FK → Conversation.id, indexed | Parent conversation |
| user_id | string | FK → User.id, indexed | Owner (for query filtering) |
| role | enum | "user" or "assistant", required | Message sender |
| content | string | required, text (unlimited) | Message body |
| tool_calls | json | optional | MCP tools invoked (for assistant messages) |
| created_at | datetime | auto-set | |

**Relationships**: Belongs to Conversation. Belongs to User.

## State Transitions

### Task
- pending → completed (via complete_task tool)
- completed → pending (not in Phase 3 MCP tools, but toggle exists in Phase 2)

### Conversation
- created → active (implicit, on first message)
- active → continued (on subsequent messages)

## Validation Rules

- Task title: 1-200 characters, required
- Task description: 0-1000 characters, optional
- Message content: non-empty string, required
- Message role: must be "user" or "assistant"
- Conversation user_id must match authenticated user
- All queries filtered by user_id from JWT
