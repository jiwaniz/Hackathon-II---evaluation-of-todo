"""Pytest configuration and fixtures for Todo CLI tests."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from src.services.task_service import TaskService


@pytest.fixture
def task_service() -> "TaskService":
    """Provide a fresh TaskService instance for each test."""
    from src.services.task_service import TaskService

    return TaskService()


@pytest.fixture
def populated_task_service() -> "TaskService":
    """Provide a TaskService with sample tasks."""
    from src.services.task_service import TaskService

    service = TaskService()
    service.add_task("Buy groceries", "Milk, eggs, bread")
    service.add_task("Call mom", "")
    service.add_task("Finish report", "Q4 summary")
    return service
