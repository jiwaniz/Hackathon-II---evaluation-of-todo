---
id: "0019"
title: implement-us10-filter-tasks
stage: green
date: 2026-01-21
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-phase2-fullstack-webapp
branch: 002-phase2-fullstack-webapp
user: zahra
command: /sp.implement T118-T130
labels: [implementation, filters, US10, frontend, backend]
links:
  spec: specs/002-phase2-fullstack-webapp/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - backend/tests/test_tasks.py (modified - 10 new filter tests)
  - backend/services/task_service.py (modified - priority/tag filters)
  - backend/routes/tasks.py (modified - priority/tag query params)
  - frontend/components/filters/PriorityFilter.tsx (created)
  - frontend/components/filters/TagFilter.tsx (created)
  - frontend/components/filters/FilterBar.tsx (created)
  - frontend/app/(dashboard)/tasks/page.tsx (modified - uses FilterBar)
  - specs/002-phase2-fullstack-webapp/tasks.md (updated)
tests:
  - backend/tests/test_tasks.py::TestTaskPriorityFilter (5 tests - PASS)
  - backend/tests/test_tasks.py::TestTaskTagFilter (5 tests - PASS)
---

## Prompt

/sp.implement T118-T130

Implement User Story 10 (Filter Tasks) - Complete remaining tasks T118-T130:
- T118: Already done (status filter tests)
- T119: Contract test for priority filter
- T120: Contract test for tag filter
- T121: Already done (status filter in task_service)
- T122: Add priority filter to task_service.py
- T123: Add tag filter to task_service.py
- T124: Handle filter query parameters in routes (complete)
- T125: Already done (StatusFilter component)
- T126: Create PriorityFilter component
- T127: Create TagFilter component
- T128: Create FilterBar component combining all filters
- T129: Already done (filter params in api.ts)
- T130: Add FilterBar to task dashboard

## Response snapshot

Implementation completed successfully:

1. **Backend Tests (T119, T120)**:
   - Created TestTaskPriorityFilter class with 5 tests:
     - test_filter_high_priority_tasks
     - test_filter_medium_priority_tasks
     - test_filter_low_priority_tasks
     - test_no_priority_filter_returns_all
     - test_priority_filter_with_status_filter
   - Created TestTaskTagFilter class with 5 tests:
     - test_filter_tasks_by_single_tag
     - test_filter_tasks_by_tag_case_insensitive
     - test_filter_tasks_no_matching_tag
     - test_tag_filter_with_other_filters
     - test_tag_filter_user_isolation

2. **Backend Implementation (T122, T123, T124)**:
   - Updated list_tasks() in task_service.py:
     - Added priority parameter with high/medium/low filtering
     - Added tag parameter with case-insensitive matching via join
     - Uses TaskTag join to filter by tag association
   - Updated GET /api/{user_id}/tasks route:
     - Added priority query parameter
     - Added tag query parameter

3. **Frontend Implementation (T126, T127, T128, T130)**:
   - Created PriorityFilter.tsx - select dropdown for priority filtering
   - Created TagFilter.tsx - select dropdown with dynamic tag options
   - Created FilterBar.tsx - combines SearchInput, StatusFilter, PriorityFilter, TagFilter
     - Includes "Clear" button when filters are active
     - Responsive layout
   - Updated tasks page to use FilterBar:
     - Integrated filter state management
     - Fetches available tags for dropdown
     - Passes all filter params to API

4. **Fixed bcrypt/passlib compatibility**:
   - Downgraded bcrypt from 5.0.0 to 4.3.0 for passlib compatibility
   - All 23 auth tests now pass

5. **Verification**:
   - All 132 tests pass (10 new filter tests)
   - Frontend builds successfully
   - Updated tasks.md to mark T118-T130 as complete

## Outcome

- User Story 10 complete - tasks can be filtered by status, priority, and tag
- Tests: 132 total tests passing (10 new filter tests)
- Files: 8 files created/modified
- Next prompts: Implement T131-T137 (User Story 11 - Sort Tasks)
- Reflection: Tag filter uses join query for case-insensitive matching

## Evaluation notes (flywheel)

- Failure modes observed: bcrypt 5.0.0 incompatible with passlib 1.7.4 - fixed by pinning bcrypt<5.0
- Graders run and results (PASS/FAIL): pytest PASS (132 tests), npm build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
