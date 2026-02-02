"""User model - managed by Better Auth, referenced by tasks."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, Text, Boolean, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.conversation import Conversation
    from models.message import Message
    from models.tag import Tag
    from models.task import Task


class User(SQLModel, table=True):
    """User entity - managed by Better Auth, referenced by tasks.

    The id is a UUID string provided by Better Auth during registration.
    Note: Column names use camelCase to match Better Auth's schema.
    """

    __tablename__ = "user"  # Better Auth uses singular table name

    id: str = Field(sa_column=Column(Text, primary_key=True))
    email: str = Field(sa_column=Column(Text, unique=True, index=True))
    name: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    emailVerified: bool = Field(default=False, sa_column=Column("emailVerified", Boolean, default=False))
    image: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    createdAt: Optional[datetime] = Field(sa_column=Column("createdAt", DateTime, nullable=True))
    updatedAt: Optional[datetime] = Field(sa_column=Column("updatedAt", DateTime, nullable=True))

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")
    messages: list["Message"] = Relationship(back_populates="user")
