"""Pydantic schemas for task-related request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models import Priority


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title (required)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (optional)")
    priority: Priority = Field(default=Priority.MEDIUM, description="Task priority level")
    tags: list[str] = Field(default_factory=list, description="List of tag names to associate")

    model_config = {"json_schema_extra": {"example": {"title": "Buy groceries", "description": "Milk, eggs, bread", "priority": "medium", "tags": ["shopping", "home"]}}}


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[Priority] = None
    tags: Optional[list[str]] = None

    model_config = {"json_schema_extra": {"example": {"title": "Buy organic groceries", "priority": "high"}}}


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

    model_config = {"from_attributes": True}


class PaginationInfo(BaseModel):
    """Pagination metadata for list responses."""

    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of items")
    pages: int = Field(..., ge=0, description="Total number of pages")


class TaskListResponse(BaseModel):
    """Schema for paginated task list response."""

    tasks: list[TaskResponse]
    pagination: PaginationInfo
