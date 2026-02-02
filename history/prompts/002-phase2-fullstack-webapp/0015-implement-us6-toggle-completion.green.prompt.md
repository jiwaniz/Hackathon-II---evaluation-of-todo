---
id: "0015"
title: implement-us6-toggle-completion
stage: green
date: 2026-01-20
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: zahra
command: /sp.implement tasks T085-T091
labels: [US6, toggle, TDD, backend, frontend]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket:
  adr:
  pr:
files:
  - backend/tests/test_tasks.py
  - backend/services/task_service.py
  - backend/routes/tasks.py
  - specs/002-phase2-fullstack-webapp/tasks.md
tests:
  - TestTaskToggle (5 tests)
  - TestTaskTogglePersistence (3 tests)
---

## Prompt

/sp.implement tasks T085-T091

Implement User Story 6 (Toggle Task Completion) following TDD approach:
- T085: Contract test for PATCH /api/{user_id}/tasks/{task_id}/toggle
- T086: Contract test for toggle persistence
- T087: Implement toggle_task function in task_service.py
- T088: Implement PATCH toggle route in tasks.py
- T089-T091: Frontend already implemented (toggleTask in API client, checkbox handler, visual feedback)

## Response snapshot

### Backend Implementation:

1. **Contract Tests (T085-T086)**: Added 8 new tests to `backend/tests/test_tasks.py`:
   - `TestTaskToggle`: 5 tests for toggle endpoint (incomplete->complete, complete->incomplete, not found, other user's task, no auth)
   - `TestTaskTogglePersistence`: 3 tests for persistence (persists to DB, double toggle returns to original, updates timestamp)

2. **Service Layer (T087)**: Added `toggle_task()` function to `backend/services/task_service.py`:
   - Flips `task.completed` status (True->False, False->True)
   - Updates `updated_at` timestamp
   - Commits and refreshes task

3. **Route Handler (T088)**: Added PATCH endpoint to `backend/routes/tasks.py`:
   - `PATCH /api/{user_id}/tasks/{task_id}/toggle`
   - JWT validation and user_id matching
   - Returns 404 for non-existent tasks, 403 for unauthorized access
   - Returns minimal response: id, completed, updated_at

### Frontend (T089-T091): Already Implemented

- `toggleTask` method exists in `frontend/lib/api.ts`
- Checkbox with `onToggle` handler exists in `TaskCard.tsx`
- Visual feedback (strikethrough, checkmark, gray background) exists

### Test Results:
All 59 task-related tests passing (8 new toggle tests added).

## Outcome

- ✅ Impact: User Story 6 complete - users can toggle tasks complete/incomplete with one click
- 🧪 Tests: 59 passed, 0 failed (8 new tests added)
- 📁 Files: 4 files modified
- 🔁 Next prompts: T092+ (User Story 7 - Set Task Priority)
- 🧠 Reflection: Frontend was already implemented; only backend needed - shows importance of checking existing code first

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation straightforward
- Graders run and results (PASS/FAIL): pytest PASS (59/59)
- Prompt variant (if applicable): Standard /sp.implement with task range
- Next experiment (smallest change to try): Continue with US7 (Set Task Priority) - priority already partially implemented in create/update
