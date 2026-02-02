"""MCP tool implementations for task operations.

All tools receive user_id from the authenticated session, ensuring user-scoped queries.
Each tool returns a dict with task_id/status/title for confirmations.
"""

import json
from datetime import datetime

from sqlmodel import Session, select

from database import get_engine
from models import Task


def _get_session() -> Session:
    """Create a new database session for tool operations."""
    return Session(get_engine())


def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task for the user.

    Args:
        user_id: The authenticated user's ID
        title: Task title (required, 1-200 chars)
        description: Optional task description (max 1000 chars)

    Returns:
        JSON string with task_id, status, and title
    """
    if not title or not title.strip():
        return json.dumps({"error": "Task title is required"})

    if len(title) > 200:
        return json.dumps({"error": "Task title must be 200 characters or less"})

    with _get_session() as session:
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({"task_id": task.id, "status": "created", "title": task.title})


def list_tasks(user_id: str, status: str = "all") -> str:
    """Retrieve tasks for the user with optional status filter.

    Args:
        user_id: The authenticated user's ID
        status: Filter - "all", "pending", or "completed"

    Returns:
        JSON string with array of task objects
    """
    with _get_session() as session:
        stmt = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            stmt = stmt.where(Task.completed == False)  # noqa: E712
        elif status == "completed":
            stmt = stmt.where(Task.completed == True)  # noqa: E712

        stmt = stmt.order_by(Task.created_at.desc())
        tasks = session.exec(stmt).all()

        if not tasks:
            filter_msg = f" with status '{status}'" if status != "all" else ""
            return json.dumps({"tasks": [], "message": f"No tasks found{filter_msg}."})

        task_list = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "priority": t.priority.value if t.priority else "medium",
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in tasks
        ]
        return json.dumps({"tasks": task_list, "count": len(task_list)})


def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as complete.

    Args:
        user_id: The authenticated user's ID
        task_id: The task ID to complete

    Returns:
        JSON string with task_id, status, and title
    """
    with _get_session() as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return json.dumps({"error": f"Task {task_id} not found or access denied"})

        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        return json.dumps({"task_id": task.id, "status": "completed", "title": task.title})


def delete_task(user_id: str, task_id: int) -> str:
    """Remove a task.

    Args:
        user_id: The authenticated user's ID
        task_id: The task ID to delete

    Returns:
        JSON string with task_id, status, and title
    """
    with _get_session() as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return json.dumps({"error": f"Task {task_id} not found or access denied"})

        title = task.title
        session.delete(task)
        session.commit()
        return json.dumps({"task_id": task_id, "status": "deleted", "title": title})


def update_task(
    user_id: str, task_id: int, title: str = "", description: str = ""
) -> str:
    """Modify task title or description.

    Args:
        user_id: The authenticated user's ID
        task_id: The task ID to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        JSON string with task_id, status, and title
    """
    with _get_session() as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return json.dumps({"error": f"Task {task_id} not found or access denied"})

        if title and title.strip():
            if len(title) > 200:
                return json.dumps({"error": "Task title must be 200 characters or less"})
            task.title = title.strip()

        if description is not None and description != "":
            task.description = description.strip()

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({"task_id": task.id, "status": "updated", "title": task.title})
