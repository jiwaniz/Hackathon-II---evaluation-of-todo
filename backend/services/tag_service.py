"""Tag service - business logic for tag operations.

Reference: specs/features/task-crud.md
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from models import Tag


def get_or_create_tag(session: Session, user_id: str, tag_name: str) -> Optional[Tag]:
    """Get an existing tag or create a new one for the user.

    Args:
        session: Database session
        user_id: The user's ID
        tag_name: Tag name (will be normalized)

    Returns:
        Tag object if valid name, None if empty after normalization
    """
    # Normalize: lowercase and trim
    name = tag_name.strip().lower()
    if not name:
        return None

    # Try to find existing tag for this user
    existing_tag = session.exec(
        select(Tag).where(Tag.user_id == user_id, Tag.name == name)
    ).first()

    if existing_tag:
        return existing_tag

    # Create new tag
    new_tag = Tag(
        user_id=user_id,
        name=name,
        created_at=datetime.utcnow(),
    )
    session.add(new_tag)
    session.flush()  # Get the ID without committing

    return new_tag


def get_or_create_tags(session: Session, user_id: str, tag_names: list[str]) -> list[Tag]:
    """Get existing tags or create new ones for the user.

    Args:
        session: Database session
        user_id: The user's ID
        tag_names: List of tag names to get or create

    Returns:
        List of Tag objects (deduplicated)
    """
    tags = []
    seen_names = set()

    for tag_name in tag_names:
        tag = get_or_create_tag(session, user_id, tag_name)
        if tag and tag.name not in seen_names:
            tags.append(tag)
            seen_names.add(tag.name)

    return tags


def list_user_tags(session: Session, user_id: str) -> list[Tag]:
    """List all tags for a user, sorted alphabetically.

    Args:
        session: Database session
        user_id: The user's ID

    Returns:
        List of Tag objects sorted by name
    """
    tags = session.exec(
        select(Tag)
        .where(Tag.user_id == user_id)
        .order_by(Tag.name)
    ).all()

    return list(tags)


def get_tag_by_id(session: Session, tag_id: int, user_id: str) -> Optional[Tag]:
    """Get a tag by ID, ensuring it belongs to the specified user.

    Args:
        session: Database session
        tag_id: The tag's ID
        user_id: The user's ID

    Returns:
        Tag if found and owned by user, None otherwise
    """
    tag = session.exec(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    ).first()
    return tag


def delete_tag(session: Session, tag: Tag) -> None:
    """Delete a tag permanently.

    Args:
        session: Database session
        tag: The Tag to delete

    Note:
        This permanently removes the tag from the database.
        Related task_tags entries are automatically deleted via cascade.
    """
    session.delete(tag)
    session.commit()
