"""CLI entry point for Todo application - Presentation Layer."""

import argparse
import sys

from src.services.task_service import TaskService

# Global TaskService instance (in-memory, resets on each run)
_service = TaskService()


def print_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("       TODO CLI - In-Memory Task Manager")
    print("=" * 50)
    print("\nPlease select an option:\n")
    print("  1. Add Task")
    print("  2. List All Tasks")
    print("  3. Update Task")
    print("  4. Delete Task")
    print("  5. Mark Task Complete")
    print("  6. Mark Task Incomplete")
    print("  7. Exit")
    print("\n" + "-" * 50)


def get_input(prompt: str, required: bool = True) -> str:
    """Get user input with optional requirement check."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please enter a value.")


def get_int_input(prompt: str) -> int | None:
    """Get integer input from user."""
    while True:
        value = input(prompt).strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")


def menu_add_task() -> None:
    """Interactive add task."""
    print("\n--- Add New Task ---\n")
    title = get_input("Enter task title (required): ", required=True)
    description = get_input("Enter task description (optional, press Enter to skip): ", required=False)

    task = _service.add_task(title, description)
    print(f"\n✓ Task added successfully: [{task.id}] {task.title}")


def menu_list_tasks() -> None:
    """Interactive list tasks."""
    print("\n--- All Tasks ---\n")
    tasks = _service.get_all_tasks()

    if not tasks:
        print("No tasks found. Add some tasks first!")
        return

    print(f"{'ID':<5} {'Status':<8} {'Title':<30} {'Description'}")
    print("-" * 70)
    for task in tasks:
        status = "✓ Done" if task.is_complete else "☐ Todo"
        desc = task.description[:25] + "..." if len(task.description) > 25 else task.description
        print(f"{task.id:<5} {status:<8} {task.title:<30} {desc}")
    print(f"\nTotal: {len(tasks)} task(s)")


def menu_update_task() -> None:
    """Interactive update task."""
    print("\n--- Update Task ---\n")

    # Show current tasks first
    tasks = _service.get_all_tasks()
    if not tasks:
        print("No tasks to update. Add some tasks first!")
        return

    print("Current tasks:")
    for task in tasks:
        print(f"  [{task.id}] {task.title}")
    print()

    task_id = get_int_input("Enter task ID to update: ")
    if task_id is None:
        print("Cancelled.")
        return

    # Check if task exists
    existing_task = _service.get_task(task_id)
    if existing_task is None:
        print(f"\n✗ Error: Task ID {task_id} not found.")
        return

    print(f"\nCurrent title: {existing_task.title}")
    print(f"Current description: {existing_task.description or '(none)'}\n")

    new_title = get_input("Enter new title (press Enter to keep current): ", required=False)
    new_description = get_input("Enter new description (press Enter to keep current): ", required=False)

    task = _service.update_task(
        task_id,
        title=new_title if new_title else None,
        description=new_description if new_description else None
    )

    if task:
        print(f"\n✓ Task updated: [{task.id}] {task.title}")


def menu_delete_task() -> None:
    """Interactive delete task."""
    print("\n--- Delete Task ---\n")

    # Show current tasks first
    tasks = _service.get_all_tasks()
    if not tasks:
        print("No tasks to delete. Add some tasks first!")
        return

    print("Current tasks:")
    for task in tasks:
        print(f"  [{task.id}] {task.title}")
    print()

    task_id = get_int_input("Enter task ID to delete: ")
    if task_id is None:
        print("Cancelled.")
        return

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    if _service.delete_task(task_id):
        print(f"\n✓ Task {task_id} deleted successfully.")
    else:
        print(f"\n✗ Error: Task ID {task_id} not found.")


def menu_complete_task() -> None:
    """Interactive mark task complete."""
    print("\n--- Mark Task Complete ---\n")

    # Show only incomplete tasks
    tasks = [t for t in _service.get_all_tasks() if not t.is_complete]
    if not tasks:
        print("No incomplete tasks to mark as complete!")
        return

    print("Incomplete tasks:")
    for task in tasks:
        print(f"  [{task.id}] ☐ {task.title}")
    print()

    task_id = get_int_input("Enter task ID to mark complete: ")
    if task_id is None:
        print("Cancelled.")
        return

    task = _service.mark_complete(task_id)
    if task:
        print(f"\n✓ Task completed: [{task.id}] {task.title}")
    else:
        print(f"\n✗ Error: Task ID {task_id} not found.")


def menu_incomplete_task() -> None:
    """Interactive mark task incomplete."""
    print("\n--- Mark Task Incomplete ---\n")

    # Show only complete tasks
    tasks = [t for t in _service.get_all_tasks() if t.is_complete]
    if not tasks:
        print("No completed tasks to mark as incomplete!")
        return

    print("Completed tasks:")
    for task in tasks:
        print(f"  [{task.id}] ✓ {task.title}")
    print()

    task_id = get_int_input("Enter task ID to mark incomplete: ")
    if task_id is None:
        print("Cancelled.")
        return

    task = _service.mark_incomplete(task_id)
    if task:
        print(f"\n✓ Task marked incomplete: [{task.id}] {task.title}")
    else:
        print(f"\n✗ Error: Task ID {task_id} not found.")


def run_interactive_menu() -> int:
    """Run the interactive menu loop."""
    print("\nWelcome to Todo CLI!")
    print("Note: This is an in-memory app. Tasks will be lost when you exit.\n")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            menu_add_task()
        elif choice == "2":
            menu_list_tasks()
        elif choice == "3":
            menu_update_task()
        elif choice == "4":
            menu_delete_task()
        elif choice == "5":
            menu_complete_task()
        elif choice == "6":
            menu_incomplete_task()
        elif choice == "7":
            print("\nGoodbye! Your tasks have been cleared (in-memory storage).")
            return 0
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 7.")

        input("\nPress Enter to continue...")


# ============================================================
# Command-line interface (for scripting and testing)
# ============================================================

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="In-Memory Todo CLI Application",
    )

    parser.add_argument(
        "--menu", "-m",
        action="store_true",
        help="Run in interactive menu mode"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument(
        "--title", "-t", required=True, help="Task title (required)"
    )
    add_parser.add_argument(
        "--description", "-d", default="", help="Task description (optional)"
    )

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    update_parser.add_argument("--title", "-t", help="New title")
    update_parser.add_argument("--description", "-d", help="New description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID to mark complete")

    # Incomplete command
    incomplete_parser = subparsers.add_parser(
        "incomplete", help="Mark a task as incomplete"
    )
    incomplete_parser.add_argument("id", type=int, help="Task ID to mark incomplete")

    return parser


def handle_add(args: argparse.Namespace) -> int:
    """Handle the add command."""
    task = _service.add_task(args.title, args.description)
    print(f"Task added: [{task.id}] {task.title}")
    return 0


def handle_list(args: argparse.Namespace) -> int:
    """Handle the list command."""
    tasks = _service.get_all_tasks()
    if not tasks:
        print("No tasks found")
        return 0

    print("Tasks:")
    for task in tasks:
        print(f"  {task}")
    return 0


def handle_update(args: argparse.Namespace) -> int:
    """Handle the update command."""
    task = _service.update_task(args.id, title=args.title, description=args.description)
    if task is None:
        print("Error: Task ID not found", file=sys.stderr)
        return 1
    print(f"Task updated: [{task.id}] {task.title}")
    return 0


def handle_delete(args: argparse.Namespace) -> int:
    """Handle the delete command."""
    if _service.delete_task(args.id):
        print(f"Task deleted: [{args.id}]")
        return 0
    print("Error: Task ID not found", file=sys.stderr)
    return 1


def handle_complete(args: argparse.Namespace) -> int:
    """Handle the complete command."""
    task = _service.mark_complete(args.id)
    if task is None:
        print("Error: Task ID not found", file=sys.stderr)
        return 1
    print(f"Task completed: [{task.id}] {task.status_indicator}")
    return 0


def handle_incomplete(args: argparse.Namespace) -> int:
    """Handle the incomplete command."""
    task = _service.mark_incomplete(args.id)
    if task is None:
        print("Error: Task ID not found", file=sys.stderr)
        return 1
    print(f"Task marked incomplete: [{task.id}] {task.status_indicator}")
    return 0


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # If no command provided or --menu flag, run interactive mode
    if args.command is None:
        if args.menu or len(sys.argv) == 1:
            return run_interactive_menu()
        parser.print_help()
        return 0

    handlers = {
        "add": handle_add,
        "list": handle_list,
        "update": handle_update,
        "delete": handle_delete,
        "complete": handle_complete,
        "incomplete": handle_incomplete,
    }

    handler = handlers.get(args.command)
    if handler:
        return handler(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
