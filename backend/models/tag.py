"""Tag model and TaskTag junction table for task categorization."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from models.task import Task
    from models.user import User


class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship."""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete="CASCADE")
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")


class Tag(SQLModel, table=True):
    """Tag entity - categorization labels owned by a user.

    Tags are user-specific: each user has their own set of tags.
    """

    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_tags_user_name"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    name: str = Field(max_length=50, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTag)
