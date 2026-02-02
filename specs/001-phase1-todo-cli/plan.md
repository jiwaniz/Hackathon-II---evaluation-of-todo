# Implementation Plan: Phase I - In-Memory Python Console Todo App

**Branch**: `001-phase1-todo-cli` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-todo-cli/spec.md`

## Summary

Build a command-line todo application that stores tasks in memory using Python 3.13+ and UV package manager. The application supports 5 core CRUD operations: Add, List, Update, Delete, and Mark Complete/Incomplete. All implementation follows Test-First Development (TDD) with Red-Green-Refactor cycle, Clean Architecture separation, and zero manual coding - all code generated via Claude Code agentic tool calls.

## Technical Context

**Language/Version**: Python 3.13+ (mandatory per spec)
**Package Manager**: UV (mandatory per spec)
**Primary Dependencies**: argparse (built-in CLI), dataclasses (built-in models)
**Storage**: In-memory only (Python dict/list - no persistence)
**Testing**: pytest with 90%+ coverage target
**Target Platform**: Cross-platform CLI (Linux/macOS/Windows via WSL2)
**Project Type**: Single project (CLI application)
**Performance Goals**: <1 second response for all operations, <2 second startup
**Constraints**: In-memory storage only, data lost on restart, max 100 tasks
**Scale/Scope**: Single user, single session, 5 CRUD operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **I. Phase Isolation** | Phase I runs independently | ✅ PASS - No external dependencies |
| **II. Spec-Driven Development** | Specify → Plan → Tasks → Implement | ✅ PASS - Following workflow |
| **III. Test-First (TDD)** | Red-Green-Refactor mandatory | ✅ PASS - Tests before implementation |
| **IV. Clean Architecture** | Domain/Application/Presentation layers | ✅ PASS - src/models, src/services, src/main.py |
| **V. API-First Design** | CLI interface designed before coding | ✅ PASS - CLI contract defined |
| **VI. Observability** | Logging for debugging | ✅ PASS - Simple console logging |
| **VII. Agentic Dev Stack** | No manual coding | ✅ PASS - All via Claude Code |

**Quality Gates**:
- [x] Python 3.13+ with type hints
- [x] UV package manager
- [x] PEP 8 compliance (ruff/black)
- [x] Type checking (mypy)
- [x] 90%+ test coverage
- [x] No manual coding

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-todo-cli/
├── spec.md              # Feature specification (approved)
├── plan.md              # This file
├── data-model.md        # Task entity definition
├── quickstart.md        # Setup and usage guide
├── contracts/           # CLI interface contract
│   └── cli-contract.md
└── tasks.md             # Implementation tasks (/sp.tasks)
```

### Source Code (repository root)

```text
/
├── src/
│   ├── __init__.py              # Package marker
│   ├── main.py                  # CLI entry point (Presentation Layer)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # Task entity (Domain Layer)
│   └── services/
│       ├── __init__.py
│       └── task_service.py      # Task management logic (Application Layer)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task_model.py   # Task entity tests
│   │   └── test_task_service.py # Service logic tests
│   └── integration/
│       ├── __init__.py
│       └── test_cli.py          # End-to-end CLI tests
├── pyproject.toml               # UV/Python project config
├── README.md                    # Setup instructions
├── CLAUDE.md                    # @AGENTS.md redirection
└── AGENTS.md                    # Agent behavior rules
```

**Structure Decision**: Single project layout selected (Option 1) as this is a standalone CLI application with no frontend/backend separation needed. Clean Architecture enforced through directory structure: `models/` (Domain), `services/` (Application), `main.py` (Presentation).

## Complexity Tracking

> No violations - all requirements align with constitution principles.

| Check | Status | Notes |
|-------|--------|-------|
| Max 3 projects | ✅ | Single project |
| No unnecessary abstractions | ✅ | Direct in-memory storage |
| Clean Architecture | ✅ | 3-layer separation |

## Implementation Constraints (Hackathon II Standards)

### 1. Zero-Manual Coding
- ALL code MUST be generated via `speckit_implement` agentic tool calls
- NO manual file editing allowed
- Each task references approved Task ID before code generation

### 2. Constitution Alignment
- Python 3.13+ type hints required on all functions
- UV package manager for dependency management
- PEP 8 compliance verified via ruff
- Type checking via mypy

### 3. Redirection Setup
- Root `CLAUDE.md` MUST contain `@AGENTS.md` redirection pattern
- Ensures consistent agent behavior across sessions

### 4. Architecture Enforcement
- `src/models/task.py` - Task entity (dataclass with type hints)
- `src/services/task_service.py` - In-memory CRUD logic
- `src/main.py` - argparse CLI interface
- Dependencies point inward only

### 5. Test Validation
Each implementation step requires corresponding test:

| Feature | Test File | Coverage Target |
|---------|-----------|-----------------|
| Task Model | `tests/unit/test_task_model.py` | 100% |
| Task Service | `tests/unit/test_task_service.py` | 100% |
| Add Task | `tests/integration/test_cli.py` | 100% |
| List Tasks | `tests/integration/test_cli.py` | 100% |
| Update Task | `tests/integration/test_cli.py` | 100% |
| Delete Task | `tests/integration/test_cli.py` | 100% |
| Mark Complete | `tests/integration/test_cli.py` | 100% |

## TDD Implementation Flow

For each feature, follow this exact sequence:

```
1. [RED]    Write failing test (Task ID: T0XX-RED)
2. [VERIFY] Run test - MUST fail
3. [GREEN]  Implement minimum code to pass (Task ID: T0XX-GREEN)
4. [VERIFY] Run test - MUST pass
5. [REFACTOR] Clean up while keeping tests green (Task ID: T0XX-REFACTOR)
6. [VERIFY] Run all tests - MUST pass
```

## CLI Interface Design

### Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `--title TEXT` `--description TEXT` | Add new task |
| `list` | (none) | List all tasks |
| `update` | `ID` `--title TEXT` `--description TEXT` | Update task |
| `delete` | `ID` | Delete task by ID |
| `complete` | `ID` | Mark task complete |
| `incomplete` | `ID` | Mark task incomplete |
| `help` | (none) | Show help message |

### Output Format

```
Tasks:
  [1] ☐ Buy groceries - Milk, eggs, bread
  [2] ✓ Call mom -
  [3] ☐ Finish report - Q4 summary

Task added: [1] Buy groceries
Task updated: [1] Buy organic groceries
Task deleted: [1]
Task completed: [2] ✓
Task marked incomplete: [2] ☐
Error: Task ID not found
Error: Title is required
```

## Plan Artifacts

- [data-model.md](./data-model.md) - Task entity definition
- [contracts/cli-contract.md](./contracts/cli-contract.md) - CLI interface specification
- [quickstart.md](./quickstart.md) - Setup and usage guide

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Execute tasks via `speckit_implement` in TDD order
3. Validate 90%+ test coverage
4. Run quality gates (ruff, mypy, pytest)
