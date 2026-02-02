---
id: "0016"
title: implement-us7-priority-tasks
stage: green
date: 2026-01-20
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: zahra
command: /sp.implement tasks T092-T099
labels: [implementation, priority, US7, frontend, backend]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - frontend/components/ui/PriorityBadge.tsx (created)
  - frontend/components/ui/PrioritySelect.tsx (created)
  - frontend/components/tasks/TaskForm.tsx (modified)
  - frontend/components/tasks/EditTaskDialog.tsx (modified)
  - frontend/components/tasks/TaskCard.tsx (modified)
  - frontend/lib/auth.ts (fixed import)
  - specs/002-phase2-fullstack-webapp/tasks.md (updated)
tests:
  - backend/tests/test_tasks.py::TestTaskPriorityCreation (5 tests - PASS)
  - backend/tests/test_tasks.py::TestTaskPriorityUpdate (4 tests - PASS)
---

## Prompt

/sp.implement tasks T092-T099

Implement User Story 7 (Set Task Priority) - Tasks T092 through T099:
- T092: Contract test for priority in task creation
- T093: Contract test for priority update
- T094: Add priority handling to task service
- T095: Update task routes for priority parameter
- T096: Create PriorityBadge component
- T097: Create PrioritySelect component
- T098: Add priority selector to TaskForm and EditTaskDialog
- T099: Display PriorityBadge in TaskCard

## Response snapshot

Implementation completed successfully:

1. **Backend (T092-T095)**: Already implemented and passing. All 9 priority-related tests pass:
   - Task creation with default/custom priority
   - Priority validation (rejects invalid values)
   - Priority update persistence
   - Case-sensitive validation

2. **Frontend (T096-T099)**:
   - Created reusable `PriorityBadge.tsx` component with color-coded styling (red/yellow/green)
   - Created reusable `PrioritySelect.tsx` component with high/medium/low options
   - Refactored `TaskForm.tsx` to use new PrioritySelect component
   - Refactored `EditTaskDialog.tsx` to use new PrioritySelect component
   - Refactored `TaskCard.tsx` to use new PriorityBadge component
   - Fixed `auth.ts` import path (`better-auth/plugins` instead of `@better-auth/jwt`)

3. **Verification**:
   - All 68 backend task tests pass
   - Frontend builds successfully with `npm run build`
   - Updated tasks.md to mark T092-T099 as complete

## Outcome

- ✅ Impact: User Story 7 complete - tasks can have priority levels (high/medium/low)
- 🧪 Tests: 68 task tests passing (9 priority-specific tests)
- 📁 Files: 7 files modified/created
- 🔁 Next prompts: Implement T100-T110 (User Story 8 - Add Tags)
- 🧠 Reflection: Backend was already complete; frontend needed reusable component extraction

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation was straightforward
- Graders run and results (PASS/FAIL): pytest PASS, npm build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
