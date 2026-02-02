"""Task service - business logic for task operations.

Reference: specs/features/task-crud.md, specs/api/rest-endpoints.md
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from models import Priority, Tag, Task, User
from models.tag import TaskTag
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from services.tag_service import get_or_create_tags


def task_to_response(task: Task) -> TaskResponse:
    """Convert a Task model to TaskResponse schema.

    Args:
        task: The Task model instance

    Returns:
        TaskResponse with tag names instead of Tag objects
    """
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        tags=[tag.name for tag in task.tags],
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
    """Create a new task for a user.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        task_data: Task creation data

    Returns:
        The created Task with relationships loaded
    """
    # Create the task
    task = Task(
        user_id=user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        priority=task_data.priority,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(task)
    session.flush()  # Get the task ID

    # Handle tags if provided
    if task_data.tags:
        tags = get_or_create_tags(session, user_id, task_data.tags)
        task.tags = tags

    session.commit()
    session.refresh(task)

    return task


def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """Get a task by ID, ensuring it belongs to the specified user.

    Args:
        session: Database session
        task_id: The task's ID
        user_id: The authenticated user's ID

    Returns:
        The Task if found and owned by user, None otherwise
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    return task


def list_tasks(
    session: Session,
    user_id: str,
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    sort: Optional[str] = None,
) -> tuple[list[Task], int]:
    """List tasks for a user with pagination, search, filters, and sorting.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        page: Page number (1-based)
        limit: Number of tasks per page (default 20, max 100)
        search: Search keyword to filter by title or description (case-insensitive)
        status: Filter by status ('all', 'completed', 'pending')
        priority: Filter by priority ('high', 'medium', 'low')
        tag: Filter by tag name (case-insensitive)
        sort: Sort order ('created_desc', 'created_asc', 'title', 'priority')

    Returns:
        Tuple of (list of tasks, total count)
    """
    from sqlmodel import case, func, or_

    # Ensure valid pagination values
    page = max(1, page)
    limit = min(max(1, limit), 100)
    offset = (page - 1) * limit

    # Build base query conditions
    conditions = [Task.user_id == user_id]

    # Add search filter (case-insensitive search in title and description)
    if search and search.strip():
        search_term = f"%{search.strip().lower()}%"
        conditions.append(
            or_(
                func.lower(Task.title).like(search_term),
                func.lower(Task.description).like(search_term),
            )
        )

    # Add status filter
    if status == "completed":
        conditions.append(Task.completed == True)  # noqa: E712
    elif status == "pending":
        conditions.append(Task.completed == False)  # noqa: E712
    # 'all' or None means no status filter

    # Add priority filter
    if priority and priority in ("high", "medium", "low"):
        conditions.append(Task.priority == Priority(priority))

    # Handle tag filter separately as it requires a join
    if tag and tag.strip():
        tag_name = tag.strip().lower()
        # Get task IDs that have this tag
        task_ids_with_tag = session.exec(
            select(TaskTag.task_id)
            .join(Tag, TaskTag.tag_id == Tag.id)
            .where(func.lower(Tag.name) == tag_name, Tag.user_id == user_id)
        ).all()

        if task_ids_with_tag:
            conditions.append(Task.id.in_(task_ids_with_tag))
        else:
            # No tasks have this tag, return empty result
            return [], 0

    # Count total tasks matching filters
    total = session.exec(
        select(func.count()).select_from(Task).where(*conditions)
    ).one()

    # Build query with conditions
    query = select(Task).where(*conditions)

    # Apply sorting
    if sort == "created_asc":
        query = query.order_by(Task.created_at.asc())
    elif sort == "title":
        query = query.order_by(func.lower(Task.title).asc())
    elif sort == "priority":
        # Priority order: high (0) -> medium (1) -> low (2), then by created_at desc
        priority_order = case(
            (Task.priority == Priority.HIGH, 0),
            (Task.priority == Priority.MEDIUM, 1),
            (Task.priority == Priority.LOW, 2),
            else_=3,
        )
        query = query.order_by(priority_order, Task.created_at.desc())
    else:
        # Default: created_at descending (newest first)
        query = query.order_by(Task.created_at.desc())

    # Apply pagination
    tasks = session.exec(query.offset(offset).limit(limit)).all()

    return list(tasks), total


def update_task(
    session: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    """Update an existing task.

    Args:
        session: Database session
        task: The existing Task to update
        task_data: TaskUpdate schema with fields to update

    Returns:
        The updated Task with relationships loaded
    """
    # Update only fields that are provided (not None)
    if task_data.title is not None:
        task.title = task_data.title.strip()

    if task_data.description is not None:
        # Empty string clears the description
        task.description = task_data.description.strip() if task_data.description else None

    if task_data.priority is not None:
        task.priority = task_data.priority

    # Handle tags if provided (including empty list to clear tags)
    if task_data.tags is not None:
        if task_data.tags:
            tags = get_or_create_tags(session, task.user_id, task_data.tags)
            task.tags = tags
        else:
            # Clear all tags
            task.tags = []

    # Update the timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task: Task) -> None:
    """Delete a task permanently.

    Args:
        session: Database session
        task: The Task to delete

    Note:
        This permanently removes the task from the database.
        Related task_tags entries are automatically deleted via cascade.
    """
    session.delete(task)
    session.commit()


def toggle_task(session: Session, task: Task) -> Task:
    """Toggle the completion status of a task.

    Args:
        session: Database session
        task: The Task to toggle

    Returns:
        The updated Task with toggled completion status
    """
    # Flip the completed status
    task.completed = not task.completed

    # Update the timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
