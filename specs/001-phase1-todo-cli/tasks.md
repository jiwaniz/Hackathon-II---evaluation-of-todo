# Tasks: Phase I - In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-phase1-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-contract.md, quickstart.md
**Branch**: `001-phase1-todo-cli`
**Date**: 2026-01-18

**TDD Workflow**: All implementation follows Test-First Development (Red-Green-Refactor)
**Zero Manual Coding**: All code MUST be generated via Claude Code agentic tool calls

## Format: `[ID] [P?] [Story?] [TDD?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- **[TDD]**: TDD phase - RED (failing test), GREEN (implementation), REFACTOR (cleanup)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Python 3.13+ project with UV and establish directory structure

- [ ] T001 Create pyproject.toml with UV configuration at /pyproject.toml
- [ ] T002 Initialize src/ directory structure per plan.md (src/__init__.py, src/models/__init__.py, src/services/__init__.py)
- [ ] T003 [P] Initialize tests/ directory structure (tests/__init__.py, tests/unit/__init__.py, tests/integration/__init__.py)
- [ ] T004 [P] Create CLAUDE.md with @AGENTS.md redirection pattern at /CLAUDE.md
- [ ] T005 [P] Create pytest configuration in tests/conftest.py
- [ ] T006 Install dev dependencies (pytest, pytest-cov, ruff, mypy, black) via UV

**Checkpoint**: Project skeleton ready - verify `uv run pytest` executes (no tests yet)

---

## Phase 2: Foundational - Task Entity (Domain Layer)

**Purpose**: Implement Task dataclass with TDD - this is the core entity ALL user stories depend on

**⚠️ CRITICAL**: No user story CLI implementation can begin until Task entity is complete

### TDD Cycle: Task Model

- [ ] T007 [RED] Write failing tests for TaskStatus enum in tests/unit/test_task_model.py
- [ ] T008 [GREEN] Implement TaskStatus enum (PENDING, COMPLETE) in src/models/task.py
- [ ] T009 [RED] Write failing tests for Task dataclass fields (id, title, description, status, created_at) in tests/unit/test_task_model.py
- [ ] T010 [GREEN] Implement Task dataclass with all fields in src/models/task.py
- [ ] T011 [RED] Write failing tests for Task validation (__post_init__: title required, max 200 chars) in tests/unit/test_task_model.py
- [ ] T012 [GREEN] Implement Task validation in __post_init__ in src/models/task.py
- [ ] T013 [RED] Write failing tests for Task properties (is_complete, status_indicator) in tests/unit/test_task_model.py
- [ ] T014 [GREEN] Implement is_complete and status_indicator properties in src/models/task.py
- [ ] T015 [RED] Write failing tests for Task methods (mark_complete, mark_incomplete, __str__) in tests/unit/test_task_model.py
- [ ] T016 [GREEN] Implement mark_complete, mark_incomplete, and __str__ methods in src/models/task.py
- [ ] T017 [REFACTOR] Clean up Task entity code, ensure type hints and docstrings in src/models/task.py
- [ ] T018 Export Task and TaskStatus from src/models/__init__.py

**Checkpoint**: Task entity complete - all tests pass, `uv run pytest tests/unit/test_task_model.py` succeeds

---

## Phase 3: Foundational - TaskService (Application Layer)

**Purpose**: Implement TaskService with TDD - provides CRUD operations for ALL user stories

**⚠️ CRITICAL**: No CLI implementation can begin until TaskService is complete

### TDD Cycle: TaskService

- [ ] T019 [RED] Write failing tests for TaskService initialization (_tasks dict, _next_id counter) in tests/unit/test_task_service.py
- [ ] T020 [GREEN] Implement TaskService class with __init__ in src/services/task_service.py
- [ ] T021 [RED] Write failing tests for add_task(title, description) -> Task in tests/unit/test_task_service.py
- [ ] T022 [GREEN] Implement add_task method in src/services/task_service.py
- [ ] T023 [RED] Write failing tests for get_all_tasks() -> list[Task] in tests/unit/test_task_service.py
- [ ] T024 [GREEN] Implement get_all_tasks method in src/services/task_service.py
- [ ] T025 [RED] Write failing tests for get_task(task_id) -> Task | None in tests/unit/test_task_service.py
- [ ] T026 [GREEN] Implement get_task method in src/services/task_service.py
- [ ] T027 [RED] Write failing tests for update_task(task_id, title, description) -> Task | None in tests/unit/test_task_service.py
- [ ] T028 [GREEN] Implement update_task method in src/services/task_service.py
- [ ] T029 [RED] Write failing tests for delete_task(task_id) -> bool in tests/unit/test_task_service.py
- [ ] T030 [GREEN] Implement delete_task method in src/services/task_service.py
- [ ] T031 [RED] Write failing tests for mark_complete(task_id) -> Task | None in tests/unit/test_task_service.py
- [ ] T032 [GREEN] Implement mark_complete method in src/services/task_service.py
- [ ] T033 [RED] Write failing tests for mark_incomplete(task_id) -> Task | None in tests/unit/test_task_service.py
- [ ] T034 [GREEN] Implement mark_incomplete method in src/services/task_service.py
- [ ] T035 [REFACTOR] Clean up TaskService code, ensure type hints and docstrings in src/services/task_service.py
- [ ] T036 Export TaskService from src/services/__init__.py

**Checkpoint**: TaskService complete - all tests pass, `uv run pytest tests/unit/` succeeds with 100% unit test coverage

---

## Phase 4: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and optional description via CLI

**Independent Test**: Run `python -m src.main add --title "Test" --description "Desc"` and verify task is created

### TDD Cycle: Add Command

- [ ] T037 [US1] [RED] Write failing integration test for `add` command with title and description in tests/integration/test_cli.py
- [ ] T038 [US1] [RED] Write failing integration test for `add` command with title only in tests/integration/test_cli.py
- [ ] T039 [US1] [RED] Write failing integration test for `add` command error when no title in tests/integration/test_cli.py
- [ ] T040 [US1] [GREEN] Implement CLI skeleton with argparse in src/main.py (parser, subparsers structure)
- [ ] T041 [US1] [GREEN] Implement `add` subcommand with --title/-t and --description/-d arguments in src/main.py
- [ ] T042 [US1] [GREEN] Implement add_task handler that calls TaskService and prints confirmation in src/main.py
- [ ] T043 [US1] [REFACTOR] Clean up add command code, ensure proper error handling in src/main.py

**Checkpoint**: User Story 1 complete - `python -m src.main add -t "Test"` works

---

## Phase 5: User Story 2 - List Tasks (Priority: P1)

**Goal**: Users can view all tasks with status indicators via CLI

**Independent Test**: Add tasks, then run `python -m src.main list` and verify all tasks display correctly

### TDD Cycle: List Command

- [ ] T044 [US2] [RED] Write failing integration test for `list` command showing all tasks in tests/integration/test_cli.py
- [ ] T045 [US2] [RED] Write failing integration test for `list` command with empty list in tests/integration/test_cli.py
- [ ] T046 [US2] [GREEN] Implement `list` subcommand in src/main.py
- [ ] T047 [US2] [GREEN] Implement list_tasks handler that formats output per cli-contract.md in src/main.py
- [ ] T048 [US2] [REFACTOR] Clean up list command code in src/main.py

**Checkpoint**: User Story 2 complete - `python -m src.main list` displays all tasks with status indicators

---

## Phase 6: User Story 3 - Update Task (Priority: P1)

**Goal**: Users can update task title and description by ID via CLI

**Independent Test**: Add task, update it, verify changes with list command

### TDD Cycle: Update Command

- [ ] T049 [US3] [RED] Write failing integration test for `update` command changing title in tests/integration/test_cli.py
- [ ] T050 [US3] [RED] Write failing integration test for `update` command changing description in tests/integration/test_cli.py
- [ ] T051 [US3] [RED] Write failing integration test for `update` command with invalid ID in tests/integration/test_cli.py
- [ ] T052 [US3] [GREEN] Implement `update` subcommand with positional ID and optional --title/-t --description/-d in src/main.py
- [ ] T053 [US3] [GREEN] Implement update_task handler with error handling in src/main.py
- [ ] T054 [US3] [REFACTOR] Clean up update command code in src/main.py

**Checkpoint**: User Story 3 complete - `python -m src.main update 1 --title "New"` works

---

## Phase 7: User Story 4 - Delete Task (Priority: P1)

**Goal**: Users can delete tasks by ID via CLI

**Independent Test**: Add task, delete it, verify it no longer appears in list

### TDD Cycle: Delete Command

- [ ] T055 [US4] [RED] Write failing integration test for `delete` command removing task in tests/integration/test_cli.py
- [ ] T056 [US4] [RED] Write failing integration test for `delete` command with invalid ID in tests/integration/test_cli.py
- [ ] T057 [US4] [GREEN] Implement `delete` subcommand with positional ID argument in src/main.py
- [ ] T058 [US4] [GREEN] Implement delete_task handler with error handling in src/main.py
- [ ] T059 [US4] [REFACTOR] Clean up delete command code in src/main.py

**Checkpoint**: User Story 4 complete - `python -m src.main delete 1` works

---

## Phase 8: User Story 5 - Mark Complete/Incomplete (Priority: P1)

**Goal**: Users can toggle task completion status via CLI

**Independent Test**: Add task, mark complete, verify ✓ indicator, mark incomplete, verify ☐ indicator

### TDD Cycle: Complete/Incomplete Commands

- [ ] T060 [US5] [RED] Write failing integration test for `complete` command in tests/integration/test_cli.py
- [ ] T061 [US5] [RED] Write failing integration test for `incomplete` command in tests/integration/test_cli.py
- [ ] T062 [US5] [RED] Write failing integration test for complete/incomplete with invalid ID in tests/integration/test_cli.py
- [ ] T063 [US5] [GREEN] Implement `complete` subcommand with positional ID in src/main.py
- [ ] T064 [US5] [GREEN] Implement `incomplete` subcommand with positional ID in src/main.py
- [ ] T065 [US5] [GREEN] Implement mark_complete and mark_incomplete handlers in src/main.py
- [ ] T066 [US5] [REFACTOR] Clean up complete/incomplete command code in src/main.py

**Checkpoint**: User Story 5 complete - all CRUD operations functional

---

## Phase 9: Polish & Quality Assurance

**Purpose**: Final validation, code quality, and documentation

- [ ] T067 [P] Implement `--help` command output matching cli-contract.md in src/main.py
- [ ] T068 [P] Add proper exit codes (0 success, 1 error) in src/main.py
- [ ] T069 [P] Run ruff check and fix any linting issues: `uv run ruff check src tests --fix`
- [ ] T070 [P] Run black formatting: `uv run black src tests`
- [ ] T071 [P] Run mypy type checking: `uv run mypy src`
- [ ] T072 Run full test suite with coverage: `uv run pytest --cov=src --cov-report=term-missing`
- [ ] T073 Verify 90%+ test coverage target met
- [ ] T074 Update README.md with setup instructions from quickstart.md
- [ ] T075 Validate quickstart.md example session works end-to-end

**Checkpoint**: Phase I complete - all quality gates pass

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Task Entity (Domain)
    ↓
Phase 3: TaskService (Application)
    ↓
Phase 4-8: User Stories (Presentation) - can run sequentially
    ↓
Phase 9: Polish
```

### Critical Blocking Dependencies

1. **T001-T006** (Setup) → BLOCKS all other phases
2. **T007-T018** (Task Entity) → BLOCKS TaskService and CLI
3. **T019-T036** (TaskService) → BLOCKS all CLI commands
4. **T040** (CLI skeleton) → BLOCKS all CLI subcommands

### Within Each TDD Cycle

```
RED (failing test) → GREEN (implementation) → REFACTOR (cleanup)
```

- RED tasks MUST fail before proceeding to GREEN
- GREEN tasks MUST pass before proceeding to REFACTOR
- REFACTOR MUST keep all tests passing

### Parallel Opportunities

**Phase 1 (parallel after T001-T002):**
- T003, T004, T005 can run in parallel

**Phase 2 (sequential TDD cycles):**
- Each RED-GREEN pair is sequential
- T017 depends on all prior tests passing

**Phase 3 (sequential TDD cycles):**
- Each service method follows RED-GREEN sequence
- T035 depends on all prior tests passing

**Phase 4-8 (sequential by user story):**
- User stories MUST be completed in order due to shared CLI file
- Within each story: RED tests → GREEN implementation → REFACTOR

**Phase 9 (parallel):**
- T067, T068, T069, T070, T071 can run in parallel
- T072-T075 are sequential validation steps

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup → Project ready
2. Complete Phase 2: Task Entity → Domain layer ready
3. Complete Phase 3: TaskService → Application layer ready
4. Complete Phase 4: Add Task CLI → **MVP DELIVERABLE**
5. **VALIDATE**: Can add tasks via CLI

### Incremental Delivery

After MVP, each user story adds one CLI command:
- US1 (Add) → US2 (List) → US3 (Update) → US4 (Delete) → US5 (Complete/Incomplete)
- Each story is independently testable
- Full functionality after US5

### Execution Checklist

For each task:
1. ✅ Reference Task ID before generating code
2. ✅ For RED tasks: Run test, verify it FAILS
3. ✅ For GREEN tasks: Run test, verify it PASSES
4. ✅ For REFACTOR tasks: Run ALL tests, verify they PASS
5. ✅ Commit after each logical group

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T006 (6) | Setup |
| Phase 2 | T007-T018 (12) | Task Entity TDD |
| Phase 3 | T019-T036 (18) | TaskService TDD |
| Phase 4 | T037-T043 (7) | US1: Add Task |
| Phase 5 | T044-T048 (5) | US2: List Tasks |
| Phase 6 | T049-T054 (6) | US3: Update Task |
| Phase 7 | T055-T059 (5) | US4: Delete Task |
| Phase 8 | T060-T066 (7) | US5: Mark Complete |
| Phase 9 | T067-T075 (9) | Polish |
| **Total** | **75 tasks** | |

### Tasks per User Story

| User Story | Task IDs | Count |
|------------|----------|-------|
| US1: Add Task | T037-T043 | 7 |
| US2: List Tasks | T044-T048 | 5 |
| US3: Update Task | T049-T054 | 6 |
| US4: Delete Task | T055-T059 | 5 |
| US5: Mark Complete | T060-T066 | 7 |

---

## Notes

- All tasks reference specific file paths per plan.md
- TDD cycles are explicitly marked (RED/GREEN/REFACTOR)
- Zero manual coding - all via Claude Code tool calls
- Verify tests fail before implementing (TDD discipline)
- Commit after each task or logical group
- Stop at checkpoints to validate independently
