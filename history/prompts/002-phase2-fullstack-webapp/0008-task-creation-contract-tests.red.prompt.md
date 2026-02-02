---
id: "0008"
title: "task-creation-contract-tests"
stage: red
date: 2026-01-20
surface: cli
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: user
command: /sp.implement tasks T049-T051
labels: [tdd, backend, tests, task-creation, us2]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket:
  adr:
  pr:
files:
  - path: backend/tests/test_tasks.py
    action: created
  - path: backend/models/task.py
    action: modified
  - path: backend/models/__init__.py
    action: modified
  - path: specs/002-phase2-fullstack-webapp/tasks.md
    action: modified
tests:
  - name: TestTaskCreation
    count: 5
    status: failing
  - name: TestTaskCreationUserIdMismatch
    count: 3
    status: failing
  - name: TestTaskCreationValidation
    count: 9
    status: failing
---

## Prompt

User requested implementation of tasks T049-T051 for User Story 2 (Create Task):
- T049: Contract test for POST /api/{user_id}/tasks in backend/tests/test_tasks.py
- T050: Contract test for 403 when URL user_id doesn't match JWT in backend/tests/test_tasks.py
- T051: Contract test for 400 on missing/invalid title in backend/tests/test_tasks.py

These are TDD "red phase" tests that should fail until the endpoint is implemented.

## Response snapshot

Created `backend/tests/test_tasks.py` with 17 comprehensive contract tests organized into three test classes:

1. **TestTaskCreation** (T049) - 5 tests for successful task creation:
   - test_create_task_success: Full validation of 201 response with task data
   - test_create_task_with_priority: Custom priority handling
   - test_create_task_with_tags: Tag association
   - test_create_task_minimal: Title-only request
   - test_create_task_full_payload: All optional fields

2. **TestTaskCreationUserIdMismatch** (T050) - 3 tests for authorization:
   - test_create_task_forbidden_user_id_mismatch: 403 when URL user_id != JWT sub
   - test_create_task_requires_auth: 401 without Authorization header
   - test_create_task_invalid_token: 401 with invalid JWT

3. **TestTaskCreationValidation** (T051) - 9 tests for validation:
   - test_create_task_missing_title: 400/422 when title missing
   - test_create_task_empty_title: 400/422 for empty string
   - test_create_task_whitespace_only_title: Whitespace handling
   - test_create_task_title_too_long: 400/422 for >200 chars
   - test_create_task_title_at_max_length: 200 chars accepted
   - test_create_task_description_too_long: 400/422 for >1000 chars
   - test_create_task_invalid_priority: Invalid enum value
   - test_create_task_null_title: Explicit null title
   - test_create_task_empty_body: Empty request body

Also fixed circular import issue in models by:
- Updating models/__init__.py import order
- Using direct TaskTag import in task.py instead of string reference

## Outcome

- Impact: Created complete TDD test suite for task creation endpoint
- Tests: 17 tests written, all failing (TDD Red phase confirmed)
- Files: 4 files modified/created
- Next prompts: T052-T054 to implement the endpoint (Green phase)
- Reflection: Tests cover all contract requirements from openapi.yaml

## Evaluation notes (flywheel)

- Failure modes observed: Initial circular import issue with link_model string reference
- Graders run and results (PASS/FAIL): N/A (Red phase - tests expected to fail)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement POST /api/{user_id}/tasks endpoint
