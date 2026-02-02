"""Task entity - Domain Layer for Todo CLI application."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task completion status."""

    PENDING = "pending"
    COMPLETE = "complete"


@dataclass
class Task:
    """
    Represents a single todo item stored in memory.

    Attributes:
        id: Unique sequential identifier (auto-generated, resets on restart)
        title: Task title (required, max 200 characters)
        description: Task description (optional)
        status: Completion status (pending/complete)
        created_at: Timestamp when task was created
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        if len(self.title) > 200:
            self.title = self.title[:200]

    @property
    def is_complete(self) -> bool:
        """Check if task is marked as complete."""
        return self.status == TaskStatus.COMPLETE

    @property
    def status_indicator(self) -> str:
        """Return visual status indicator."""
        return "✓" if self.is_complete else "☐"

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETE

    def mark_incomplete(self) -> None:
        """Mark task as incomplete/pending."""
        self.status = TaskStatus.PENDING

    def __str__(self) -> str:
        """String representation for display."""
        desc = f" - {self.description}" if self.description else ""
        return f"[{self.id}] {self.status_indicator} {self.title}{desc}"
