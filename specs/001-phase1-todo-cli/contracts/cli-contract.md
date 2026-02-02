# CLI Contract: Phase I - In-Memory Python Console Todo App

**Date**: 2026-01-17
**Feature**: 001-phase1-todo-cli

## Interface Overview

**Entry Point**: `python -m src.main` or `uv run python -m src.main`

## Commands

### 1. Add Task

**Command**: `add`

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--title`, `-t` | string | Yes | Task title (max 200 chars) |
| `--description`, `-d` | string | No | Task description |

**Usage**:
```bash
# Add task with title only
python -m src.main add --title "Buy groceries"

# Add task with title and description
python -m src.main add --title "Buy groceries" --description "Milk, eggs, bread"

# Short form
python -m src.main add -t "Call mom" -d "Discuss weekend plans"
```

**Success Output**:
```
Task added: [1] Buy groceries
```

**Error Output**:
```
Error: Title is required
```

---

### 2. List Tasks

**Command**: `list`

**Arguments**: None

**Usage**:
```bash
python -m src.main list
```

**Success Output (with tasks)**:
```
Tasks:
  [1] ☐ Buy groceries - Milk, eggs, bread
  [2] ✓ Call mom - Discuss weekend plans
  [3] ☐ Finish report
```

**Success Output (empty)**:
```
No tasks found
```

---

### 3. Update Task

**Command**: `update`

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to update (positional) |
| `--title`, `-t` | string | No | New title |
| `--description`, `-d` | string | No | New description |

**Usage**:
```bash
# Update title only
python -m src.main update 1 --title "Buy organic groceries"

# Update description only
python -m src.main update 1 --description "Organic milk, free-range eggs"

# Update both
python -m src.main update 1 -t "Shopping" -d "Weekly groceries"
```

**Success Output**:
```
Task updated: [1] Buy organic groceries
```

**Error Output**:
```
Error: Task ID not found
Error: Invalid ID format
```

---

### 4. Delete Task

**Command**: `delete`

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to delete (positional) |

**Usage**:
```bash
python -m src.main delete 1
```

**Success Output**:
```
Task deleted: [1]
```

**Error Output**:
```
Error: Task ID not found
Error: Invalid ID format
```

---

### 5. Mark Complete

**Command**: `complete`

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to mark complete (positional) |

**Usage**:
```bash
python -m src.main complete 1
```

**Success Output**:
```
Task completed: [1] ✓
```

**Error Output**:
```
Error: Task ID not found
Error: Invalid ID format
```

---

### 6. Mark Incomplete

**Command**: `incomplete`

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to mark incomplete (positional) |

**Usage**:
```bash
python -m src.main incomplete 1
```

**Success Output**:
```
Task marked incomplete: [1] ☐
```

**Error Output**:
```
Error: Task ID not found
Error: Invalid ID format
```

---

### 7. Help

**Command**: `help` or `--help` or `-h`

**Usage**:
```bash
python -m src.main --help
python -m src.main add --help
```

**Output**:
```
usage: todo [-h] {add,list,update,delete,complete,incomplete} ...

In-Memory Todo CLI Application

positional arguments:
  {add,list,update,delete,complete,incomplete}
    add                 Add a new task
    list                List all tasks
    update              Update an existing task
    delete              Delete a task
    complete            Mark a task as complete
    incomplete          Mark a task as incomplete

optional arguments:
  -h, --help            show this help message and exit
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, task not found, etc.) |

## Error Messages

| Error | Message | Exit Code |
|-------|---------|-----------|
| Empty title | `Error: Title is required` | 1 |
| Task not found | `Error: Task ID not found` | 1 |
| Invalid ID | `Error: Invalid ID format` | 1 |
| Unknown command | `Error: Unknown command` | 1 |

## Output Format Specification

### Task Display Format

```
[{id}] {status_indicator} {title}[ - {description}]
```

Where:
- `{id}`: Integer task ID
- `{status_indicator}`: `✓` (complete) or `☐` (pending)
- `{title}`: Task title
- `{description}`: Optional, shown with ` - ` prefix if present

### List Format

```
Tasks:
  [1] ☐ Task one
  [2] ✓ Task two - with description
```

Note: 2-space indent for each task line.
