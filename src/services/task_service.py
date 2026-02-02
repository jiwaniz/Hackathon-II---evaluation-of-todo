"""TaskService - Application Layer for Todo CLI application."""

from src.models.task import Task


class TaskService:
    """Manages task storage and CRUD operations."""

    def __init__(self) -> None:
        """Initialize TaskService with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with auto-generated ID.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            The newly created Task
        """
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks sorted by ID.

        Returns:
            List of all tasks in ID order
        """
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task | None:
        """
        Get a task by ID.

        Args:
            task_id: The task ID to find

        Returns:
            The Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task | None:
        """
        Update a task's title and/or description.

        Args:
            task_id: The task ID to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> Task | None:
        """
        Mark a task as complete.

        Args:
            task_id: The task ID to mark complete

        Returns:
            The updated Task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.mark_complete()
        return task

    def mark_incomplete(self, task_id: int) -> Task | None:
        """
        Mark a task as incomplete/pending.

        Args:
            task_id: The task ID to mark incomplete

        Returns:
            The updated Task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.mark_incomplete()
        return task
