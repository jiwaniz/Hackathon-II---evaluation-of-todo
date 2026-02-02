"""Unit tests for Task entity and TaskStatus enum."""

from datetime import datetime

import pytest

from src.models.task import Task, TaskStatus


class TestTaskStatus:
    """Tests for TaskStatus enum."""

    def test_taskstatus_has_pending_value(self) -> None:
        """TaskStatus should have PENDING value."""
        assert TaskStatus.PENDING.value == "pending"

    def test_taskstatus_has_complete_value(self) -> None:
        """TaskStatus should have COMPLETE value."""
        assert TaskStatus.COMPLETE.value == "complete"

    def test_taskstatus_has_only_two_values(self) -> None:
        """TaskStatus should only have PENDING and COMPLETE values."""
        assert len(TaskStatus) == 2


class TestTaskDataclass:
    """Tests for Task dataclass fields."""

    def test_task_has_id_field(self) -> None:
        """Task should have id field."""
        task = Task(id=1, title="Test")
        assert task.id == 1

    def test_task_has_title_field(self) -> None:
        """Task should have title field."""
        task = Task(id=1, title="Buy groceries")
        assert task.title == "Buy groceries"

    def test_task_has_description_field_with_default(self) -> None:
        """Task should have description field with empty string default."""
        task = Task(id=1, title="Test")
        assert task.description == ""

    def test_task_has_description_field_with_value(self) -> None:
        """Task should accept description value."""
        task = Task(id=1, title="Test", description="Some details")
        assert task.description == "Some details"

    def test_task_has_status_field_with_default(self) -> None:
        """Task should have status field defaulting to PENDING."""
        task = Task(id=1, title="Test")
        assert task.status == TaskStatus.PENDING

    def test_task_has_status_field_with_value(self) -> None:
        """Task should accept status value."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETE)
        assert task.status == TaskStatus.COMPLETE

    def test_task_has_created_at_field(self) -> None:
        """Task should have created_at field with datetime."""
        before = datetime.now()
        task = Task(id=1, title="Test")
        after = datetime.now()
        assert before <= task.created_at <= after


class TestTaskValidation:
    """Tests for Task validation in __post_init__."""

    def test_task_raises_error_when_title_is_empty(self) -> None:
        """Task should raise ValueError when title is empty."""
        with pytest.raises(ValueError, match="Title is required"):
            Task(id=1, title="")

    def test_task_raises_error_when_title_is_whitespace(self) -> None:
        """Task should raise ValueError when title is only whitespace."""
        with pytest.raises(ValueError, match="Title is required"):
            Task(id=1, title="   ")

    def test_task_truncates_long_title(self) -> None:
        """Task should truncate title to 200 characters."""
        long_title = "x" * 250
        task = Task(id=1, title=long_title)
        assert len(task.title) == 200
        assert task.title == "x" * 200


class TestTaskProperties:
    """Tests for Task properties."""

    def test_is_complete_returns_false_for_pending(self) -> None:
        """is_complete should return False for PENDING status."""
        task = Task(id=1, title="Test", status=TaskStatus.PENDING)
        assert task.is_complete is False

    def test_is_complete_returns_true_for_complete(self) -> None:
        """is_complete should return True for COMPLETE status."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETE)
        assert task.is_complete is True

    def test_status_indicator_returns_checkbox_for_pending(self) -> None:
        """status_indicator should return ☐ for PENDING status."""
        task = Task(id=1, title="Test", status=TaskStatus.PENDING)
        assert task.status_indicator == "☐"

    def test_status_indicator_returns_checkmark_for_complete(self) -> None:
        """status_indicator should return ✓ for COMPLETE status."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETE)
        assert task.status_indicator == "✓"


class TestTaskMethods:
    """Tests for Task methods."""

    def test_mark_complete_changes_status(self) -> None:
        """mark_complete should change status to COMPLETE."""
        task = Task(id=1, title="Test")
        task.mark_complete()
        assert task.status == TaskStatus.COMPLETE

    def test_mark_incomplete_changes_status(self) -> None:
        """mark_incomplete should change status to PENDING."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETE)
        task.mark_incomplete()
        assert task.status == TaskStatus.PENDING

    def test_str_format_without_description(self) -> None:
        """__str__ should format task without description."""
        task = Task(id=1, title="Buy groceries")
        assert str(task) == "[1] ☐ Buy groceries"

    def test_str_format_with_description(self) -> None:
        """__str__ should format task with description."""
        task = Task(id=1, title="Buy groceries", description="Milk, eggs")
        assert str(task) == "[1] ☐ Buy groceries - Milk, eggs"

    def test_str_format_complete_task(self) -> None:
        """__str__ should show checkmark for complete task."""
        task = Task(id=1, title="Done task", status=TaskStatus.COMPLETE)
        assert str(task) == "[1] ✓ Done task"
