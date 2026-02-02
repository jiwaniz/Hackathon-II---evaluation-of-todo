# Todo CLI - Phase I

In-Memory Python Console Todo Application

## Description

A command-line todo application that stores tasks in memory using Python 3.13+ and UV package manager.

## Features

- Add tasks with title and description
- List all tasks with status indicators
- Update task details
- Delete tasks by ID
- Mark tasks as complete/incomplete

## Setup

### Prerequisites

- Python 3.13+
- UV package manager

### Installation

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -e ".[dev]"
```

## Usage

```bash
# Add a task
python -m src.main add --title "Buy groceries" --description "Milk, eggs, bread"

# List all tasks
python -m src.main list

# Update a task
python -m src.main update 1 --title "Buy organic groceries"

# Mark task complete
python -m src.main complete 1

# Mark task incomplete
python -m src.main incomplete 1

# Delete a task
python -m src.main delete 1

# Get help
python -m src.main --help
```

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Format code
uv run black src tests

# Lint code
uv run ruff check src tests

# Type checking
uv run mypy src
```

## Project Structure

```
/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task entity
│   └── services/
│       ├── __init__.py
│       └── task_service.py  # CRUD logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_task_model.py
│   │   └── test_task_service.py
│   └── integration/
│       └── test_cli.py
├── pyproject.toml
└── README.md
```

## Note

This is Phase I - In-memory storage only. All tasks are lost when the application exits.
