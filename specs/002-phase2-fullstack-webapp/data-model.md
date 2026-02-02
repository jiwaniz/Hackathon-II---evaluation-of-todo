# Data Model: Phase II Full-Stack Web Application

**Feature**: 002-phase2-fullstack-webapp
**Date**: 2026-01-18
**ORM**: SQLModel (mandatory per spec)
**Database**: Neon PostgreSQL (free tier)

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
│─────────────────│
│ id: str (PK)    │
│ email: str (UQ) │
│ name: str?      │
│ created_at: dt  │
│ updated_at: dt  │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐       N:M       ┌─────────────────┐
│      Task       │◄───────────────►│       Tag       │
│─────────────────│    (task_tags)  │─────────────────│
│ id: int (PK)    │                 │ id: int (PK)    │
│ user_id: str(FK)│                 │ user_id: str(FK)│
│ title: str      │                 │ name: str       │
│ description: str│                 │ created_at: dt  │
│ completed: bool │                 └─────────────────┘
│ priority: str   │
│ created_at: dt  │
│ updated_at: dt  │
└─────────────────┘
```

## SQLModel Definitions

### User Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """User entity - managed by Better Auth, referenced by tasks."""
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # UUID from Better Auth
    email: str = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
```

### Task Model

```python
from enum import Enum

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    """Task entity - core todo item owned by a user."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False, index=True)
    priority: Priority = Field(default=Priority.MEDIUM, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(
        back_populates="tasks",
        link_model="TaskTag"
    )

    def __post_init__(self):
        """Validation after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        if len(self.title) > 200:
            self.title = self.title[:200]
```

### Tag Model

```python
class Tag(SQLModel, table=True):
    """Tag entity - categorization labels owned by a user."""
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model="TaskTag"
    )

    class Config:
        # Unique constraint: user can't have duplicate tag names
        table_args = (UniqueConstraint("user_id", "name"),)
```

### TaskTag Link Model

```python
class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship."""
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
```

## Pydantic Schemas (Request/Response)

### Task Schemas

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Priority.MEDIUM
    tags: list[str] = Field(default_factory=list)

class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[Priority] = None
    tags: Optional[list[str]] = None

class TaskResponse(BaseModel):
    """Schema for task API response."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """Schema for paginated task list response."""
    tasks: list[TaskResponse]
    pagination: "PaginationInfo"

class PaginationInfo(BaseModel):
    """Pagination metadata."""
    page: int
    limit: int
    total: int
    pages: int
```

### Auth Schemas

```python
class UserCreate(BaseModel):
    """Schema for user registration."""
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    """Schema for user login."""
    email: str
    password: str

class UserResponse(BaseModel):
    """Schema for user API response."""
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

class AuthResponse(BaseModel):
    """Schema for authentication response."""
    user: UserResponse
    token: str
    expires_at: datetime
```

## Database Indexes

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| users | idx_users_email | email | Login lookup |
| tasks | idx_tasks_user_id | user_id | Filter by user |
| tasks | idx_tasks_completed | completed | Status filter |
| tasks | idx_tasks_priority | priority | Priority filter |
| tasks | idx_tasks_created_at | created_at | Sort by date |
| tags | idx_tags_user_id | user_id | Filter by user |
| tags | idx_tags_name | name | Tag lookup |

## Constraints

| Constraint | Table | Type | Description |
|------------|-------|------|-------------|
| pk_users | users | PRIMARY KEY | id |
| uq_users_email | users | UNIQUE | email |
| pk_tasks | tasks | PRIMARY KEY | id |
| fk_tasks_user | tasks | FOREIGN KEY | user_id → users.id (CASCADE) |
| chk_tasks_priority | tasks | CHECK | priority IN ('high', 'medium', 'low') |
| pk_tags | tags | PRIMARY KEY | id |
| fk_tags_user | tags | FOREIGN KEY | user_id → users.id (CASCADE) |
| uq_tags_user_name | tags | UNIQUE | (user_id, name) |
| pk_task_tags | task_tags | PRIMARY KEY | (task_id, tag_id) |
| fk_task_tags_task | task_tags | FOREIGN KEY | task_id → tasks.id (CASCADE) |
| fk_task_tags_tag | task_tags | FOREIGN KEY | tag_id → tags.id (CASCADE) |

## Cascade Delete Rules

1. **User deleted** → All user's tasks, tags, and task_tags are deleted
2. **Task deleted** → All task_tags for that task are deleted
3. **Tag deleted** → All task_tags for that tag are deleted

## Migration Strategy

Use Alembic for database migrations:

```bash
# Initialize Alembic
uv run alembic init alembic

# Generate migration
uv run alembic revision --autogenerate -m "initial schema"

# Apply migration
uv run alembic upgrade head

# Rollback
uv run alembic downgrade -1
```

## Data Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| User.email | Valid email format | "Invalid email format" |
| User.email | Unique | "Email already registered" |
| Task.title | Required, 1-200 chars | "Title is required and must be 1-200 characters" |
| Task.description | Optional, max 1000 chars | "Description must be under 1000 characters" |
| Task.priority | Enum: high/medium/low | "Priority must be high, medium, or low" |
| Tag.name | Required, 1-50 chars | "Tag name must be 1-50 characters" |
| Tag.name | Unique per user | "Tag already exists" |
