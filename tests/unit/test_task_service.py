"""Unit tests for TaskService (Application Layer)."""

from src.models.task import TaskStatus
from src.services.task_service import TaskService


class TestTaskServiceInit:
    """Tests for TaskService initialization."""

    def test_taskservice_initializes_with_empty_tasks(self) -> None:
        """TaskService should initialize with empty task dict."""
        service = TaskService()
        assert service._tasks == {}

    def test_taskservice_initializes_with_next_id_1(self) -> None:
        """TaskService should initialize _next_id to 1."""
        service = TaskService()
        assert service._next_id == 1


class TestAddTask:
    """Tests for add_task method."""

    def test_add_task_returns_task_with_id(self) -> None:
        """add_task should return a Task with auto-generated ID."""
        service = TaskService()
        task = service.add_task("Buy groceries", "Milk, eggs")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs"

    def test_add_task_increments_id(self) -> None:
        """add_task should increment ID for each new task."""
        service = TaskService()
        task1 = service.add_task("Task 1", "")
        task2 = service.add_task("Task 2", "")
        assert task1.id == 1
        assert task2.id == 2

    def test_add_task_stores_task(self) -> None:
        """add_task should store the task in _tasks dict."""
        service = TaskService()
        task = service.add_task("Test", "")
        assert 1 in service._tasks
        assert service._tasks[1] == task

    def test_add_task_with_empty_description(self) -> None:
        """add_task should accept empty description."""
        service = TaskService()
        task = service.add_task("Test", "")
        assert task.description == ""


class TestGetAllTasks:
    """Tests for get_all_tasks method."""

    def test_get_all_tasks_returns_empty_list(self) -> None:
        """get_all_tasks should return empty list when no tasks."""
        service = TaskService()
        assert service.get_all_tasks() == []

    def test_get_all_tasks_returns_all_tasks(self) -> None:
        """get_all_tasks should return all tasks."""
        service = TaskService()
        service.add_task("Task 1", "")
        service.add_task("Task 2", "")
        tasks = service.get_all_tasks()
        assert len(tasks) == 2

    def test_get_all_tasks_returns_tasks_in_order(self) -> None:
        """get_all_tasks should return tasks in ID order."""
        service = TaskService()
        service.add_task("First", "")
        service.add_task("Second", "")
        tasks = service.get_all_tasks()
        assert tasks[0].title == "First"
        assert tasks[1].title == "Second"


class TestGetTask:
    """Tests for get_task method."""

    def test_get_task_returns_task_by_id(self) -> None:
        """get_task should return task with matching ID."""
        service = TaskService()
        service.add_task("Test", "")
        task = service.get_task(1)
        assert task is not None
        assert task.id == 1

    def test_get_task_returns_none_for_invalid_id(self) -> None:
        """get_task should return None for non-existent ID."""
        service = TaskService()
        assert service.get_task(999) is None


class TestUpdateTask:
    """Tests for update_task method."""

    def test_update_task_changes_title(self) -> None:
        """update_task should change task title."""
        service = TaskService()
        service.add_task("Original", "")
        task = service.update_task(1, title="Updated")
        assert task is not None
        assert task.title == "Updated"

    def test_update_task_changes_description(self) -> None:
        """update_task should change task description."""
        service = TaskService()
        service.add_task("Test", "Original desc")
        task = service.update_task(1, description="New desc")
        assert task is not None
        assert task.description == "New desc"

    def test_update_task_changes_both(self) -> None:
        """update_task should change both title and description."""
        service = TaskService()
        service.add_task("Old title", "Old desc")
        task = service.update_task(1, title="New title", description="New desc")
        assert task is not None
        assert task.title == "New title"
        assert task.description == "New desc"

    def test_update_task_returns_none_for_invalid_id(self) -> None:
        """update_task should return None for non-existent ID."""
        service = TaskService()
        assert service.update_task(999, title="Test") is None

    def test_update_task_keeps_unchanged_fields(self) -> None:
        """update_task should not change fields not specified."""
        service = TaskService()
        service.add_task("Title", "Desc")
        task = service.update_task(1, title="New Title")
        assert task is not None
        assert task.description == "Desc"


class TestDeleteTask:
    """Tests for delete_task method."""

    def test_delete_task_removes_task(self) -> None:
        """delete_task should remove task from storage."""
        service = TaskService()
        service.add_task("Test", "")
        result = service.delete_task(1)
        assert result is True
        assert 1 not in service._tasks

    def test_delete_task_returns_false_for_invalid_id(self) -> None:
        """delete_task should return False for non-existent ID."""
        service = TaskService()
        assert service.delete_task(999) is False


class TestMarkComplete:
    """Tests for mark_complete method."""

    def test_mark_complete_changes_status(self) -> None:
        """mark_complete should change task status to COMPLETE."""
        service = TaskService()
        service.add_task("Test", "")
        task = service.mark_complete(1)
        assert task is not None
        assert task.status == TaskStatus.COMPLETE

    def test_mark_complete_returns_none_for_invalid_id(self) -> None:
        """mark_complete should return None for non-existent ID."""
        service = TaskService()
        assert service.mark_complete(999) is None


class TestMarkIncomplete:
    """Tests for mark_incomplete method."""

    def test_mark_incomplete_changes_status(self) -> None:
        """mark_incomplete should change task status to PENDING."""
        service = TaskService()
        service.add_task("Test", "")
        service.mark_complete(1)
        task = service.mark_incomplete(1)
        assert task is not None
        assert task.status == TaskStatus.PENDING

    def test_mark_incomplete_returns_none_for_invalid_id(self) -> None:
        """mark_incomplete should return None for non-existent ID."""
        service = TaskService()
        assert service.mark_incomplete(999) is None
