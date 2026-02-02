# Quickstart: Phase I - In-Memory Python Console Todo App

**Date**: 2026-01-17
**Feature**: 001-phase1-todo-cli

## Prerequisites

- Python 3.13+ installed
- UV package manager installed
- WSL2 (for Windows users)

### Install UV (if not installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verify Installation

```bash
python --version  # Should be 3.13+
uv --version      # Should show UV version
```

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd "Hackathon II - evaluation of todo"
```

### 2. Create Virtual Environment

```bash
uv venv
```

### 3. Activate Virtual Environment

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
uv pip install -e ".[dev]"
```

## Usage

### Run the Application

```bash
# Using UV
uv run python -m src.main <command>

# Or with activated venv
python -m src.main <command>
```

### Basic Commands

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

## Example Session

```bash
$ python -m src.main add -t "Buy groceries" -d "Milk, eggs, bread"
Task added: [1] Buy groceries

$ python -m src.main add -t "Call mom"
Task added: [2] Call mom

$ python -m src.main list
Tasks:
  [1] ☐ Buy groceries - Milk, eggs, bread
  [2] ☐ Call mom

$ python -m src.main complete 1
Task completed: [1] ✓

$ python -m src.main list
Tasks:
  [1] ✓ Buy groceries - Milk, eggs, bread
  [2] ☐ Call mom

$ python -m src.main update 2 -d "Discuss weekend plans"
Task updated: [2] Call mom

$ python -m src.main delete 1
Task deleted: [1]

$ python -m src.main list
Tasks:
  [2] ☐ Call mom - Discuss weekend plans
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_task_model.py

# Run with verbose output
uv run pytest -v
```

## Development Commands

```bash
# Format code
uv run black src tests

# Lint code
uv run ruff check src tests

# Type checking
uv run mypy src

# Run all quality checks
uv run black src tests && uv run ruff check src tests && uv run mypy src && uv run pytest
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
├── README.md
└── CLAUDE.md
```

## Important Notes

⚠️ **In-Memory Storage**: All tasks are stored in memory only. Data is **lost** when the application exits.

⚠️ **Single Session**: This is a single-user, single-session application. Each run starts fresh.

⚠️ **Phase I Only**: This is the basic version. Advanced features (persistence, priorities, tags) are planned for Phase II.

## Troubleshooting

### Python Version Error

```
Error: Python 3.13+ required
```

**Solution**: Install Python 3.13+ using pyenv or official installer.

### UV Not Found

```
uv: command not found
```

**Solution**: Install UV using the curl command above and restart terminal.

### Module Not Found

```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Install package in editable mode:
```bash
uv pip install -e .
```
