---
id: "0020"
title: implement-us11-sort-tasks
stage: green
date: 2026-01-21
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: zahra
command: /sp.implement T131-T137
labels: [implementation, sorting, US11, frontend, backend]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - backend/tests/test_tasks.py (modified - 7 new sort tests)
  - backend/services/task_service.py (modified - sort parameter)
  - backend/routes/tasks.py (modified - sort query param)
  - frontend/components/filters/SortSelect.tsx (created)
  - frontend/components/filters/FilterBar.tsx (modified - added SortSelect)
  - frontend/app/(dashboard)/tasks/page.tsx (modified - sort state)
  - specs/002-phase2-fullstack-webapp/tasks.md (updated)
tests:
  - backend/tests/test_tasks.py::TestTaskSorting (4 tests - PASS)
  - backend/tests/test_tasks.py::TestTaskPrioritySorting (3 tests - PASS)
---

## Prompt

/sp.implement T131-T137

Implement User Story 11 (Sort Tasks) - Complete tasks T131-T137:
- T131: Contract test for sort parameter (created_desc, created_asc, title, priority)
- T132: Contract test for priority sorting order (high first, secondary sort by created_at)
- T133: Add sort functionality to task_service.py list_tasks function
- T134: Handle sort query parameter in GET /api/{user_id}/tasks route
- T135: Create SortSelect component for sort dropdown
- T136: Add sort parameter to getTasks in API client (already existed)
- T137: Add SortSelect to FilterBar component

## Response snapshot

Implementation completed successfully:

1. **Backend Tests (T131, T132)**:
   - Created TestTaskSorting class with 4 tests:
     - test_sort_by_created_desc_default
     - test_sort_by_created_asc
     - test_sort_by_title
     - test_sort_with_filters
   - Created TestTaskPrioritySorting class with 3 tests:
     - test_sort_by_priority_high_first
     - test_sort_by_priority_secondary_sort_by_created
     - test_sort_by_priority_with_pagination

2. **Backend Implementation (T133, T134)**:
   - Updated list_tasks() in task_service.py:
     - Added sort parameter with options: created_desc, created_asc, title, priority
     - Default is created_desc (newest first)
     - Title sort uses case-insensitive ordering via func.lower()
     - Priority sort uses SQLModel's case() expression (high=0, medium=1, low=2)
     - Priority sort has secondary ordering by created_at descending
   - Updated GET /api/{user_id}/tasks route:
     - Added sort query parameter
     - Passes sort to list_tasks service function

3. **Frontend Implementation (T135, T136, T137)**:
   - Created SortSelect.tsx - select dropdown for sort options:
     - Newest First (created_desc)
     - Oldest First (created_asc)
     - Title (A-Z)
     - Priority
   - T136 was already done - sort parameter existed in api.ts getTasks
   - Updated FilterBar.tsx:
     - Added SortSelect component
     - Added sort to FilterState interface
     - Updated handleClearAll to reset sort to default
   - Updated tasks page:
     - Added sort to initial filter state
     - Passes sort parameter to API call
     - Clear filters resets sort to default

4. **Verification**:
   - All 139 tests pass (7 new sort tests)
   - Frontend builds successfully
   - Updated tasks.md to mark T131-T137 as complete

## Outcome

- User Story 11 complete - tasks can be sorted by creation date, title, and priority
- Tests: 139 total tests passing (7 new sort tests)
- Files: 6 files created/modified
- All 11 user stories now implemented
- Reflection: Priority sort uses case() expression for custom ordering

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation was straightforward
- Graders run and results (PASS/FAIL): pytest PASS (139 tests), npm build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
