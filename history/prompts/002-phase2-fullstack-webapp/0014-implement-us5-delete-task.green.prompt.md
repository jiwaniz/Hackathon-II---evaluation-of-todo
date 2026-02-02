---
id: "0014"
title: implement-us5-delete-task
stage: green
date: 2026-01-20
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: zahra
command: /sp.implement tasks T078-T084
labels: [US5, delete-task, TDD, backend, frontend, confirmation-dialog]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket:
  adr:
  pr:
files:
  - backend/tests/test_tasks.py
  - backend/services/task_service.py
  - backend/routes/tasks.py
  - frontend/components/ui/ConfirmDialog.tsx
  - frontend/app/(dashboard)/tasks/page.tsx
  - specs/002-phase2-fullstack-webapp/tasks.md
tests:
  - TestTaskDeletion (5 tests)
  - TestTaskDeletionForbidden (4 tests)
---

## Prompt

/sp.implement tasks T078-T084

Implement User Story 5 (Delete Task) following TDD approach:
- T078-T079: Write contract tests for DELETE endpoint (success, 404, 403 cases)
- T080: Implement delete_task function in task_service.py
- T081: Implement DELETE /api/{user_id}/tasks/{task_id} route
- T082: Create ConfirmDialog component for delete confirmation
- T083: deleteTask already exists in API client
- T084: Wire up delete with confirmation in TaskCard

## Response snapshot

### Backend Implementation:

1. **Contract Tests (T078-T079)**: Added 9 new tests to `backend/tests/test_tasks.py`:
   - `TestTaskDeletion`: 5 tests for successful deletion scenarios (success, not found, removes from list, with tags, double delete)
   - `TestTaskDeletionForbidden`: 4 tests for 403/401 responses (other user's task, URL mismatch, no auth, invalid token)

2. **Service Layer (T080)**: Added `delete_task()` function to `backend/services/task_service.py`:
   - Simple deletion with session.delete()
   - Commits transaction
   - Relies on cascade delete for task_tags

3. **Route Handler (T081)**: Added DELETE endpoint to `backend/routes/tasks.py`:
   - `DELETE /api/{user_id}/tasks/{task_id}`
   - JWT validation and user_id matching
   - Returns 404 for non-existent tasks, 403 for unauthorized access
   - Returns success message on deletion

### Frontend Implementation:

4. **ConfirmDialog (T082)**: Created `frontend/components/ui/ConfirmDialog.tsx`:
   - Reusable confirmation dialog component
   - Supports "default" and "danger" variants
   - Customizable title, message, button labels
   - Loading state and escape key handling

5. **API Client (T083)**: Already implemented - verified `deleteTask` method exists

6. **Integration (T084)**: Wired up delete with confirmation in tasks page:
   - Added `handleDeleteTask` to open confirm dialog
   - Added `handleConfirmDelete` to execute deletion
   - Added `handleCancelDelete` to close dialog
   - Passed `onDelete` prop to TaskList component

### Test Results:
All 51 task-related tests passing (9 new deletion tests added).

## Outcome

- ✅ Impact: User Story 5 complete - users can now delete tasks with confirmation dialog
- 🧪 Tests: 51 passed, 0 failed (9 new tests added)
- 📁 Files: 6 files modified/created
- 🔁 Next prompts: T085-T091 (User Story 6 - Toggle Task Completion)
- 🧠 Reflection: TDD workflow effective - all tests pass on first implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation straightforward following existing patterns
- Graders run and results (PASS/FAIL): pytest PASS (51/51)
- Prompt variant (if applicable): Standard /sp.implement with task range
- Next experiment (smallest change to try): Continue with US6 (Toggle Completion) using same approach
