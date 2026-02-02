---
id: "0013"
title: implement-us4-update-task
stage: green
date: 2026-01-20
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: zahra
command: /sp.implement tasks T070-T077
labels: [US4, update-task, TDD, backend, frontend]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket:
  adr:
  pr:
files:
  - backend/tests/test_tasks.py
  - backend/services/task_service.py
  - backend/routes/tasks.py
  - frontend/components/tasks/EditTaskDialog.tsx
  - frontend/app/(dashboard)/tasks/page.tsx
  - specs/002-phase2-fullstack-webapp/tasks.md
tests:
  - TestTaskUpdate (10 tests)
  - TestTaskUpdateNotFound (2 tests)
  - TestTaskUpdateForbidden (4 tests)
---

## Prompt

/sp.implement tasks T070-T077

Implement User Story 4 (Update Task) following TDD approach:
- T070-T072: Write contract tests for PUT endpoint (success, 404, 403 cases)
- T073: Implement update_task function in task_service.py
- T074: Implement PUT /api/{user_id}/tasks/{task_id} route
- T075: Create EditTaskDialog frontend component
- T076-T077: Wire up API client and TaskCard integration (already implemented)

## Response snapshot

### Backend Implementation:

1. **Contract Tests (T070-T072)**: Added 16 new tests to `backend/tests/test_tasks.py`:
   - `TestTaskUpdate`: 10 tests for successful update scenarios (title, description, priority, tags, multiple fields, validation)
   - `TestTaskUpdateNotFound`: 2 tests for 404 responses
   - `TestTaskUpdateForbidden`: 4 tests for 403 and 401 responses

2. **Service Layer (T073)**: Added `update_task()` function to `backend/services/task_service.py`:
   - Updates only provided fields (partial update support)
   - Handles tag updates including clearing tags
   - Updates `updated_at` timestamp

3. **Route Handler (T074)**: Added PUT endpoint to `backend/routes/tasks.py`:
   - `PUT /api/{user_id}/tasks/{task_id}`
   - JWT validation and user_id matching
   - Returns 404 for non-existent tasks, 403 for unauthorized access

### Frontend Implementation:

4. **EditTaskDialog (T075)**: Created `frontend/components/tasks/EditTaskDialog.tsx`:
   - Modal dialog matching CreateTaskDialog pattern
   - Pre-filled form with existing task data
   - Only submits changed fields
   - Validation and error handling

5. **Integration (T076-T077)**: Already implemented - verified and wired up in tasks page:
   - `updateTask` method in `frontend/lib/api.ts`
   - Edit button and handler in TaskCard (via `onEdit` prop)
   - Added EditTaskDialog to tasks dashboard page

### Test Results:
All 42 task-related tests passing (including 16 new update tests).

## Outcome

- ✅ Impact: User Story 4 complete - users can now edit task title, description, and priority
- 🧪 Tests: 42 passed, 0 failed (16 new tests added)
- 📁 Files: 6 files modified/created
- 🔁 Next prompts: T078-T084 (User Story 5 - Delete Task)
- 🧠 Reflection: TDD workflow effective - tests written first, all passing after implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation straightforward following existing patterns
- Graders run and results (PASS/FAIL): pytest PASS (42/42)
- Prompt variant (if applicable): Standard /sp.implement with task range
- Next experiment (smallest change to try): Continue with US5 (Delete Task) using same approach
