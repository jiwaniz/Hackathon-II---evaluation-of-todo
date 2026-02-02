"""Integration tests for CLI commands.

Note: Each test runs in a fresh process with a new TaskService instance.
This is correct behavior for an in-memory application where data is lost on restart.
Tests verify individual command behavior, not cross-command state persistence.
"""

import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI with given arguments and return result."""
    return subprocess.run(
        [sys.executable, "-m", "src.main", *args],
        capture_output=True,
        text=True,
    )


class TestAddCommand:
    """Integration tests for add command."""

    def test_add_with_title_and_description(self) -> None:
        """Add command should create task with title and description."""
        result = run_cli(
            "add", "--title", "Buy groceries", "--description", "Milk, eggs"
        )
        assert result.returncode == 0
        assert "Task added:" in result.stdout
        assert "Buy groceries" in result.stdout

    def test_add_with_title_only(self) -> None:
        """Add command should create task with title only."""
        result = run_cli("add", "--title", "Call mom")
        assert result.returncode == 0
        assert "Task added:" in result.stdout
        assert "Call mom" in result.stdout

    def test_add_with_short_flags(self) -> None:
        """Add command should accept short flags -t and -d."""
        result = run_cli("add", "-t", "Test task", "-d", "Description")
        assert result.returncode == 0
        assert "Task added:" in result.stdout

    def test_add_without_title_shows_error(self) -> None:
        """Add command without title should show error."""
        result = run_cli("add")
        assert result.returncode != 0

    def test_add_assigns_id_1_to_first_task(self) -> None:
        """First task should get ID 1."""
        result = run_cli("add", "-t", "First task")
        assert result.returncode == 0
        assert "[1]" in result.stdout


class TestListCommand:
    """Integration tests for list command."""

    def test_list_empty(self) -> None:
        """List command with no tasks should show message."""
        result = run_cli("list")
        assert result.returncode == 0
        assert "No tasks found" in result.stdout

    def test_list_returns_success(self) -> None:
        """List command should return success code."""
        result = run_cli("list")
        assert result.returncode == 0


class TestUpdateCommand:
    """Integration tests for update command."""

    def test_update_invalid_id(self) -> None:
        """Update command with invalid ID should show error."""
        result = run_cli("update", "999", "--title", "Test")
        assert result.returncode != 0
        assert (
            "not found" in result.stdout.lower() or "not found" in result.stderr.lower()
        )

    def test_update_requires_id_argument(self) -> None:
        """Update command should require ID argument."""
        result = run_cli("update")
        assert result.returncode != 0


class TestDeleteCommand:
    """Integration tests for delete command."""

    def test_delete_invalid_id(self) -> None:
        """Delete command with invalid ID should show error."""
        result = run_cli("delete", "999")
        assert result.returncode != 0
        assert (
            "not found" in result.stdout.lower() or "not found" in result.stderr.lower()
        )

    def test_delete_requires_id_argument(self) -> None:
        """Delete command should require ID argument."""
        result = run_cli("delete")
        assert result.returncode != 0


class TestCompleteCommand:
    """Integration tests for complete command."""

    def test_complete_invalid_id(self) -> None:
        """Complete command with invalid ID should show error."""
        result = run_cli("complete", "999")
        assert result.returncode != 0
        assert (
            "not found" in result.stdout.lower() or "not found" in result.stderr.lower()
        )

    def test_complete_requires_id_argument(self) -> None:
        """Complete command should require ID argument."""
        result = run_cli("complete")
        assert result.returncode != 0


class TestIncompleteCommand:
    """Integration tests for incomplete command."""

    def test_incomplete_invalid_id(self) -> None:
        """Incomplete command with invalid ID should show error."""
        result = run_cli("incomplete", "999")
        assert result.returncode != 0
        assert (
            "not found" in result.stdout.lower() or "not found" in result.stderr.lower()
        )

    def test_incomplete_requires_id_argument(self) -> None:
        """Incomplete command should require ID argument."""
        result = run_cli("incomplete")
        assert result.returncode != 0


class TestHelpCommand:
    """Integration tests for help command."""

    def test_help_shows_usage(self) -> None:
        """Help should show usage information."""
        result = run_cli("--help")
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "todo" in result.stdout.lower()

    def test_no_command_shows_interactive_menu(self) -> None:
        """Running without command should show interactive menu."""
        result = run_cli()
        # Interactive menu requires input, so it exits with error on EOF
        # But we can verify the menu was displayed
        assert "TODO CLI" in result.stdout
        assert "Add Task" in result.stdout
        assert "List All Tasks" in result.stdout

    def test_help_shows_all_commands(self) -> None:
        """Help should list all available commands."""
        result = run_cli("--help")
        assert result.returncode == 0
        assert "add" in result.stdout
        assert "list" in result.stdout
        assert "update" in result.stdout
        assert "delete" in result.stdout
        assert "complete" in result.stdout
        assert "incomplete" in result.stdout
