"""Task routes - API endpoints for task CRUD operations.

All task routes follow the /api/{user_id}/tasks pattern where user_id
is validated against the JWT token's sub claim.

Reference: specs/api/rest-endpoints.md, specs/features/task-crud.md
"""

import math

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlmodel import Session

from database import get_session
from middleware.auth import verify_user_access
from models import User
from schemas.task import TaskCreate, TaskUpdate
from services.task_service import create_task, delete_task, get_task_by_id, list_tasks, task_to_response, toggle_task, update_task

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.post("/", status_code=201)
async def create_new_task(
    user_id: str = Path(..., description="The user's ID"),
    task_data: TaskCreate = ...,
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Create a new task for the authenticated user.

    Contract (T049):
    - POST /api/{user_id}/tasks with valid title returns 201
    - Response contains task with id, title, description, completed, priority, tags
    - completed defaults to False
    - priority defaults to "medium"
    - tags defaults to empty array
    - created_at and updated_at are set

    Validation (T051):
    - Title is required (1-200 characters)
    - Description is optional (max 1000 characters)
    - Priority must be valid enum value (high/medium/low)

    Authorization (T050):
    - Requires valid JWT token
    - Returns 403 if URL user_id doesn't match JWT sub claim
    - Returns 401 if token is invalid or missing
    """
    task = create_task(session, user_id, task_data)

    return {
        "data": task_to_response(task),
        "message": "Task created successfully",
    }


@router.get("/")
async def get_tasks(
    user_id: str = Path(..., description="The user's ID"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str = Query(None, description="Search keyword for title/description"),
    status: str = Query(None, description="Filter by status: all, completed, pending"),
    priority: str = Query(None, description="Filter by priority: high, medium, low"),
    tag: str = Query(None, description="Filter by tag name (case-insensitive)"),
    sort: str = Query(None, description="Sort order: created_desc, created_asc, title, priority"),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """List all tasks for the authenticated user with pagination, search, and filters.

    Contract (T059):
    - GET /api/{user_id}/tasks returns 200
    - Response contains tasks array and pagination metadata
    - Tasks are ordered by created_at descending (newest first)

    Authorization (T060):
    - Requires valid JWT token
    - Returns 403 if URL user_id doesn't match JWT sub claim
    - Users can only see their own tasks

    Pagination (T061):
    - Default: page=1, limit=20
    - limit max is 100
    - Returns total count and pages in pagination metadata

    Search (T111, T112):
    - search parameter filters by keyword in title or description
    - Search is case-insensitive
    - Empty search returns all tasks

    Status Filter (T118):
    - status=completed returns only completed tasks
    - status=pending returns only incomplete tasks
    - status=all or no status returns all tasks

    Priority Filter (T119):
    - priority=high returns only high priority tasks
    - priority=medium returns only medium priority tasks
    - priority=low returns only low priority tasks

    Tag Filter (T120):
    - tag parameter filters by tag name (case-insensitive)
    - Returns tasks that have the specified tag

    Sort (T131, T132):
    - sort=created_desc orders by created_at descending (default)
    - sort=created_asc orders by created_at ascending
    - sort=title orders alphabetically by title (case-insensitive)
    - sort=priority orders by priority (high, medium, low)
    """
    tasks, total = list_tasks(session, user_id, page, limit, search, status, priority, tag, sort)
    pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "data": {
            "tasks": [task_to_response(task) for task in tasks],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": pages,
            },
        }
    }


@router.put("/{task_id}")
async def update_existing_task(
    user_id: str = Path(..., description="The user's ID"),
    task_id: int = Path(..., description="The task's ID"),
    task_data: TaskUpdate = ...,
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Update an existing task for the authenticated user.

    Contract (T070):
    - PUT /api/{user_id}/tasks/{task_id} with valid data returns 200
    - Response contains updated task data
    - updated_at is refreshed
    - Only provided fields are updated

    Not Found (T071):
    - Returns 404 if task does not exist
    - Returns 404 if task belongs to different user

    Authorization (T072):
    - Requires valid JWT token
    - Returns 403 if URL user_id doesn't match JWT sub claim
    - Returns 401 if token is invalid or missing
    """
    # Get the task, ensuring it belongs to the authenticated user
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with id {task_id} not found",
                }
            },
        )

    updated_task = update_task(session, task, task_data)

    return {
        "data": task_to_response(updated_task),
        "message": "Task updated successfully",
    }


@router.delete("/{task_id}")
async def delete_existing_task(
    user_id: str = Path(..., description="The user's ID"),
    task_id: int = Path(..., description="The task's ID"),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Delete a task for the authenticated user.

    Contract (T078):
    - DELETE /api/{user_id}/tasks/{task_id} returns 200 with success message
    - Task is permanently removed from database
    - Related tags associations are cascade deleted

    Not Found (T078):
    - Returns 404 if task does not exist
    - Returns 404 if task belongs to different user

    Authorization (T079):
    - Requires valid JWT token
    - Returns 403 if URL user_id doesn't match JWT sub claim
    - Returns 401 if token is invalid or missing
    """
    # Get the task, ensuring it belongs to the authenticated user
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with id {task_id} not found",
                }
            },
        )

    delete_task(session, task)

    return {
        "message": "Task deleted successfully",
    }


@router.patch("/{task_id}/toggle")
async def toggle_task_completion(
    user_id: str = Path(..., description="The user's ID"),
    task_id: int = Path(..., description="The task's ID"),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Toggle the completion status of a task.

    Contract (T085):
    - PATCH /api/{user_id}/tasks/{task_id}/toggle returns 200
    - Response contains task id, completed status, and updated_at
    - Completion status is flipped (True -> False, False -> True)

    Persistence (T086):
    - Status change persists to database immediately
    - updated_at timestamp is refreshed

    Authorization:
    - Requires valid JWT token
    - Returns 403 if URL user_id doesn't match JWT sub claim
    - Returns 404 if task not found or belongs to different user
    - Returns 401 if token is invalid or missing
    """
    # Get the task, ensuring it belongs to the authenticated user
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with id {task_id} not found",
                }
            },
        )

    updated_task = toggle_task(session, task)

    return {
        "data": {
            "id": updated_task.id,
            "completed": updated_task.completed,
            "updated_at": updated_task.updated_at.isoformat(),
        },
        "message": f"Task marked as {'completed' if updated_task.completed else 'incomplete'}",
    }
