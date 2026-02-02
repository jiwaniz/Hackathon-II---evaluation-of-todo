"""SQLModel database models for Evolution of Todo.

All models are exported from this module for easy importing:
    from models import User, Task, Tag, TaskTag, Priority

Import order is critical to avoid circular import issues:
1. User (no dependencies)
2. TaskTag (junction table, depends only on table names)
3. Tag (depends on TaskTag class)
4. Task (depends on TaskTag class)
"""

from models.user import User
from models.tag import TaskTag, Tag
from models.task import Priority, Task
from models.conversation import Conversation
from models.message import Message, MessageRole

__all__ = [
    "User",
    "Task",
    "Tag",
    "TaskTag",
    "Priority",
    "Conversation",
    "Message",
    "MessageRole",
]
