"""Tests for MCP tool implementations.

TDD: These tests are written FIRST and should FAIL before implementation.
"""

import json

from sqlmodel import Session

from models import Task, User


class TestAddTask:
    """Tests for the add_task MCP tool."""

    def test_add_task_creates_task(self, session: Session, test_user: User, engine):
        """add_task should create a task in the database."""
        # Patch the engine used by tools
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import add_task

            result = json.loads(add_task(user_id=test_user.id, title="Buy groceries"))

        assert result["status"] == "created"
        assert result["title"] == "Buy groceries"
        assert "task_id" in result

    def test_add_task_with_description(self, session: Session, test_user: User, engine):
        """add_task should support optional description."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import add_task

            result = json.loads(
                add_task(
                    user_id=test_user.id,
                    title="Buy milk",
                    description="Get 2% milk from store",
                )
            )

        assert result["status"] == "created"
        assert result["title"] == "Buy milk"

    def test_add_task_empty_title_rejected(self, session: Session, test_user: User, engine):
        """add_task should reject empty titles."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import add_task

            result = json.loads(add_task(user_id=test_user.id, title=""))

        assert "error" in result

    def test_add_task_long_title_rejected(self, session: Session, test_user: User, engine):
        """add_task should reject titles over 200 chars."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import add_task

            result = json.loads(add_task(user_id=test_user.id, title="x" * 201))

        assert "error" in result


class TestListTasks:
    """Tests for the list_tasks MCP tool."""

    def test_list_tasks_returns_user_tasks(
        self, session: Session, test_user: User, test_task: Task, engine
    ):
        """list_tasks should return tasks for the user."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import list_tasks

            result = json.loads(list_tasks(user_id=test_user.id, status="all"))

        assert len(result["tasks"]) >= 1
        assert result["tasks"][0]["title"] == "Test Task"

    def test_list_tasks_empty_state(self, session: Session, test_user: User, engine):
        """list_tasks should return friendly message when no tasks exist."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import list_tasks

            result = json.loads(list_tasks(user_id=test_user.id, status="all"))

        assert result["tasks"] == []
        assert "message" in result

    def test_list_tasks_filters_by_status(
        self, session: Session, test_user: User, test_task: Task, completed_task: Task, engine
    ):
        """list_tasks should filter by pending/completed status."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import list_tasks

            pending = json.loads(list_tasks(user_id=test_user.id, status="pending"))
            completed = json.loads(list_tasks(user_id=test_user.id, status="completed"))

        assert all(not t["completed"] for t in pending["tasks"])
        assert all(t["completed"] for t in completed["tasks"])


class TestCompleteTask:
    """Tests for the complete_task MCP tool."""

    def test_complete_task_marks_done(
        self, session: Session, test_user: User, test_task: Task, engine
    ):
        """complete_task should mark the task as completed."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import complete_task

            result = json.loads(complete_task(user_id=test_user.id, task_id=test_task.id))

        assert result["status"] == "completed"
        assert result["title"] == "Test Task"

    def test_complete_task_not_found(self, session: Session, test_user: User, engine):
        """complete_task should return error for non-existent task."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import complete_task

            result = json.loads(complete_task(user_id=test_user.id, task_id=99999))

        assert "error" in result


class TestDeleteTask:
    """Tests for the delete_task MCP tool."""

    def test_delete_task_removes_task(
        self, session: Session, test_user: User, test_task: Task, engine
    ):
        """delete_task should remove the task."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import delete_task

            result = json.loads(delete_task(user_id=test_user.id, task_id=test_task.id))

        assert result["status"] == "deleted"

    def test_delete_task_user_isolation(
        self, session: Session, test_user: User, other_user_task: Task, engine
    ):
        """delete_task should not delete another user's task."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import delete_task

            result = json.loads(delete_task(user_id=test_user.id, task_id=other_user_task.id))

        assert "error" in result


class TestUpdateTask:
    """Tests for the update_task MCP tool."""

    def test_update_task_changes_title(
        self, session: Session, test_user: User, test_task: Task, engine
    ):
        """update_task should update the task title."""
        from unittest.mock import patch

        with patch("mcp_server.tools.get_engine", return_value=engine):
            from mcp_server.tools import update_task

            result = json.loads(
                update_task(user_id=test_user.id, task_id=test_task.id, title="Updated Title")
            )

        assert result["status"] == "updated"
        assert result["title"] == "Updated Title"
