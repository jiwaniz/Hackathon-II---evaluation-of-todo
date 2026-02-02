# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/002-phase2-fullstack-webapp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml, quickstart.md

**Tests**: Tests are included as this project mandates TDD (spec constraint C-005: Red-Green-Refactor workflow).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` (FastAPI with UV)
- **Frontend**: `frontend/` (Next.js 16+)
- **Specs**: `specs/002-phase2-fullstack-webapp/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend

- [x] T001 Create monorepo directory structure per plan.md (backend/, frontend/ directories)
- [x] T002 [P] Initialize backend Python project with UV in backend/pyproject.toml
- [x] T003 [P] Initialize frontend Next.js 16+ project in frontend/
- [x] T004 [P] Add backend dependencies: fastapi, sqlmodel, uvicorn, python-jose, passlib, alembic, psycopg2-binary in backend/pyproject.toml
- [x] T005 [P] Add frontend dependencies: better-auth, @better-auth/jwt in frontend/package.json
- [x] T006 [P] Create backend environment configuration in backend/.env.example
- [x] T007 [P] Create frontend environment configuration in frontend/.env.example
- [x] T008 [P] Configure Tailwind CSS in frontend/tailwind.config.ts
- [x] T009 [P] Create root CLAUDE.md with @AGENTS.md reference
- [x] T010 [P] Create backend/CLAUDE.md with FastAPI guidelines
- [x] T011 [P] Create frontend/CLAUDE.md with Next.js guidelines

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T012 Create database configuration in backend/config.py (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS)
- [x] T013 Create database connection with SQLModel in backend/database.py
- [x] T014 Initialize Alembic migrations in backend/alembic/
- [x] T015 [P] Create User SQLModel in backend/models/user.py (id, email, name, created_at, updated_at)
- [x] T016 [P] Create Priority enum and Task SQLModel in backend/models/task.py (id, user_id, title, description, completed, priority, created_at, updated_at)
- [x] T017 [P] Create Tag SQLModel and TaskTag link model in backend/models/tag.py
- [x] T018 Create models __init__.py exporting all models in backend/models/__init__.py
- [ ] T019 Generate initial Alembic migration for users, tasks, tags, task_tags tables
- [x] T020 Create JWT verification middleware in backend/middleware/auth.py (verify token + URL user_id match)
- [x] T021 [P] Create Pydantic schemas for tasks in backend/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse, TaskListResponse)
- [x] T022 [P] Create Pydantic schemas for auth in backend/schemas/auth.py (UserCreate, UserLogin, UserResponse, AuthResponse)
- [x] T023 Create FastAPI app entry point in backend/main.py with CORS and router configuration
- [x] T024 Create health check endpoint in backend/main.py (GET /health)
- [x] T025 [P] Create test fixtures in backend/tests/conftest.py (test database, test client, mock user)

### Frontend Foundation

- [x] T026 Configure Better Auth with JWT Plugin in frontend/lib/auth.ts
- [x] T027 Create Better Auth client hooks in frontend/lib/auth-client.ts
- [x] T028 Create API client with auth header injection in frontend/lib/api.ts
- [x] T029 Create utility functions in frontend/lib/utils.ts
- [x] T030 Create TypeScript types for Task, User, Priority in frontend/types/index.ts
- [x] T031 Create root layout with providers in frontend/app/layout.tsx
- [x] T032 Create landing page in frontend/app/page.tsx
- [x] T033 Create global styles in frontend/app/globals.css

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration & Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register, login, logout, and access their personal task space

**Independent Test**: Register new account, logout, login again - user session persists correctly

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T034 [P] [US1] Contract test for POST /api/auth/register in backend/tests/test_auth.py
- [x] T035 [P] [US1] Contract test for POST /api/auth/login in backend/tests/test_auth.py
- [x] T036 [P] [US1] Contract test for POST /api/auth/logout in backend/tests/test_auth.py
- [x] T037 [P] [US1] Contract test for GET /api/auth/session in backend/tests/test_auth.py
- [x] T038 [P] [US1] Contract test for 401 on invalid/missing token in backend/tests/test_auth.py

### Backend Implementation for User Story 1

- [x] T039 [US1] Implement user registration logic in backend/services/auth_service.py (password hashing with passlib)
- [x] T040 [US1] Implement auth routes in backend/routes/auth.py (register, login, logout, session endpoints)
- [x] T041 [US1] Register auth router in backend/main.py

### Frontend Implementation for User Story 1

- [x] T042 [P] [US1] Create AuthGuard component in frontend/components/auth/AuthGuard.tsx
- [x] T043 [P] [US1] Create LoginForm component in frontend/components/auth/LoginForm.tsx
- [x] T044 [P] [US1] Create RegisterForm component in frontend/components/auth/RegisterForm.tsx
- [x] T045 [US1] Create login page in frontend/app/(auth)/login/page.tsx
- [x] T046 [US1] Create register page in frontend/app/(auth)/register/page.tsx
- [x] T047 [US1] Create protected layout with AuthGuard in frontend/app/(dashboard)/layout.tsx
- [x] T048 [US1] Create user menu/logout button component in frontend/components/auth/UserMenu.tsx

**Checkpoint**: User Story 1 complete - users can register, login, logout, and access protected routes

---

## Phase 4: User Story 2 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks with title and optional description

**Independent Test**: Login, create task "Buy groceries" with description "Milk, eggs, bread", task appears in list

### Tests for User Story 2 ⚠️

- [x] T049 [P] [US2] Contract test for POST /api/{user_id}/tasks in backend/tests/test_tasks.py
- [x] T050 [P] [US2] Contract test for 403 when URL user_id doesn't match JWT in backend/tests/test_tasks.py
- [x] T051 [P] [US2] Contract test for 400 on missing/invalid title in backend/tests/test_tasks.py

### Backend Implementation for User Story 2

- [x] T052 [US2] Implement task creation in backend/services/task_service.py (create_task function)
- [x] T053 [US2] Implement POST /api/{user_id}/tasks route in backend/routes/tasks.py
- [x] T054 [US2] Register tasks router in backend/main.py

### Frontend Implementation for User Story 2

- [x] T055 [P] [US2] Create TaskForm component in frontend/components/tasks/TaskForm.tsx
- [x] T056 [US2] Add createTask method to API client in frontend/lib/api.ts
- [x] T057 [US2] Create task creation modal/dialog in frontend/components/tasks/CreateTaskDialog.tsx
- [x] T058 [US2] Add "Add Task" button to dashboard in frontend/app/(dashboard)/tasks/page.tsx

**Checkpoint**: User Story 2 complete - users can create tasks

---

## Phase 5: User Story 3 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can see all their tasks with status indicators

**Independent Test**: View dashboard with multiple tasks, verify each shows title, status, priority correctly

### Tests for User Story 3 ⚠️

- [x] T059 [P] [US3] Contract test for GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [x] T060 [P] [US3] Contract test for user isolation (cannot see other user's tasks) in backend/tests/test_tasks.py
- [x] T061 [P] [US3] Contract test for pagination in backend/tests/test_tasks.py

### Backend Implementation for User Story 3

- [x] T062 [US3] Implement task listing with pagination in backend/services/task_service.py (list_tasks function)
- [x] T063 [US3] Implement GET /api/{user_id}/tasks route in backend/routes/tasks.py

### Frontend Implementation for User Story 3

- [x] T064 [P] [US3] Create TaskCard component in frontend/components/tasks/TaskCard.tsx
- [x] T065 [P] [US3] Create TaskList component in frontend/components/tasks/TaskList.tsx
- [x] T066 [P] [US3] Create EmptyState component in frontend/components/ui/EmptyState.tsx
- [x] T067 [US3] Add getTasks method to API client in frontend/lib/api.ts
- [x] T068 [US3] Create main task dashboard page in frontend/app/(dashboard)/tasks/page.tsx
- [x] T069 [US3] Implement loading states in TaskList component

**Checkpoint**: User Story 3 complete - MVP (US1 + US2 + US3) delivers functional task creation and viewing

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Authenticated users can modify their task's title or description

**Independent Test**: Edit existing task title from "Buy groceries" to "Buy organic groceries", change persists after refresh

### Tests for User Story 4 ⚠️

- [x] T070 [P] [US4] Contract test for PUT /api/{user_id}/tasks/{task_id} in backend/tests/test_tasks.py
- [x] T071 [P] [US4] Contract test for 404 on non-existent task in backend/tests/test_tasks.py
- [x] T072 [P] [US4] Contract test for 403 when updating another user's task in backend/tests/test_tasks.py

### Backend Implementation for User Story 4

- [x] T073 [US4] Implement task update in backend/services/task_service.py (update_task function)
- [x] T074 [US4] Implement PUT /api/{user_id}/tasks/{task_id} route in backend/routes/tasks.py

### Frontend Implementation for User Story 4

- [x] T075 [US4] Create EditTaskDialog component in frontend/components/tasks/EditTaskDialog.tsx
- [x] T076 [US4] Add updateTask method to API client in frontend/lib/api.ts
- [x] T077 [US4] Add edit button and handler to TaskCard component

**Checkpoint**: User Story 4 complete - users can edit their tasks

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Authenticated users can permanently remove tasks with confirmation

**Independent Test**: Delete a task, confirm dialog appears, task removed from list after confirmation

### Tests for User Story 5 ⚠️

- [x] T078 [P] [US5] Contract test for DELETE /api/{user_id}/tasks/{task_id} in backend/tests/test_tasks.py
- [x] T079 [P] [US5] Contract test for 403 when deleting another user's task in backend/tests/test_tasks.py

### Backend Implementation for User Story 5

- [x] T080 [US5] Implement task deletion in backend/services/task_service.py (delete_task function)
- [x] T081 [US5] Implement DELETE /api/{user_id}/tasks/{task_id} route in backend/routes/tasks.py

### Frontend Implementation for User Story 5

- [x] T082 [P] [US5] Create ConfirmDialog component in frontend/components/ui/ConfirmDialog.tsx
- [x] T083 [US5] Add deleteTask method to API client in frontend/lib/api.ts
- [x] T084 [US5] Add delete button with confirmation to TaskCard component

**Checkpoint**: User Story 5 complete - users can delete tasks with confirmation

---

## Phase 8: User Story 6 - Toggle Task Completion (Priority: P2)

**Goal**: Users can mark tasks complete/incomplete with one click

**Independent Test**: Click checkbox on pending task, status changes to complete, click again to revert

### Tests for User Story 6 ⚠️

- [x] T085 [P] [US6] Contract test for PATCH /api/{user_id}/tasks/{task_id}/toggle in backend/tests/test_tasks.py
- [x] T086 [P] [US6] Contract test for toggle persistence in backend/tests/test_tasks.py

### Backend Implementation for User Story 6

- [x] T087 [US6] Implement task toggle in backend/services/task_service.py (toggle_task function)
- [x] T088 [US6] Implement PATCH /api/{user_id}/tasks/{task_id}/toggle route in backend/routes/tasks.py

### Frontend Implementation for User Story 6

- [x] T089 [US6] Add toggleTask method to API client in frontend/lib/api.ts
- [x] T090 [US6] Add completion checkbox with toggle handler to TaskCard component
- [x] T091 [US6] Add visual feedback for completed tasks (strikethrough, checkmark)

**Checkpoint**: User Story 6 complete - Full CRUD + toggle functionality

---

## Phase 9: User Story 7 - Set Task Priority (Priority: P3)

**Goal**: Users can assign priority levels (high/medium/low) to tasks

**Independent Test**: Create task with "high" priority, verify priority indicator displays correctly

### Tests for User Story 7 ⚠️

- [x] T092 [P] [US7] Contract test for priority in task creation in backend/tests/test_tasks.py
- [x] T093 [P] [US7] Contract test for priority update in backend/tests/test_tasks.py

### Backend Implementation for User Story 7

- [x] T094 [US7] Add priority handling to task creation/update in backend/services/task_service.py
- [x] T095 [US7] Update task routes to handle priority parameter in backend/routes/tasks.py

### Frontend Implementation for User Story 7

- [x] T096 [P] [US7] Create PriorityBadge component in frontend/components/ui/PriorityBadge.tsx
- [x] T097 [P] [US7] Create PrioritySelect component in frontend/components/ui/PrioritySelect.tsx
- [x] T098 [US7] Add priority selector to TaskForm and EditTaskDialog components
- [x] T099 [US7] Display PriorityBadge in TaskCard component

**Checkpoint**: User Story 7 complete - tasks can have priority levels

---

## Phase 10: User Story 8 - Add Tags/Categories to Tasks (Priority: P3)

**Goal**: Users can categorize tasks with tags for better organization

**Independent Test**: Add tags "work" and "urgent" to a task, both tags display on the task

### Tests for User Story 8 ⚠️

- [x] T100 [P] [US8] Contract test for GET /api/{user_id}/tags in backend/tests/test_tags.py
- [x] T101 [P] [US8] Contract test for tags in task creation/update in backend/tests/test_tasks.py

### Backend Implementation for User Story 8

- [x] T102 [US8] Implement tag service in backend/services/tag_service.py (get_or_create_tag, list_user_tags)
- [x] T103 [US8] Implement tag routes in backend/routes/tags.py (GET /api/{user_id}/tags)
- [x] T104 [US8] Update task service to handle tag associations in backend/services/task_service.py
- [x] T105 [US8] Register tags router in backend/main.py

### Frontend Implementation for User Story 8

- [x] T106 [P] [US8] Create TagBadge component in frontend/components/ui/TagBadge.tsx
- [x] T107 [P] [US8] Create TagInput component in frontend/components/ui/TagInput.tsx
- [x] T108 [US8] Add getTags method to API client in frontend/lib/api.ts
- [x] T109 [US8] Add TagInput to TaskForm and EditTaskDialog components
- [x] T110 [US8] Display TagBadges in TaskCard component

**Checkpoint**: User Story 8 complete - tasks can be tagged

---

## Phase 11: User Story 9 - Search Tasks (Priority: P3)

**Goal**: Users can search tasks by keyword in title and description

**Independent Test**: Search for "groceries", only tasks containing that word appear

### Tests for User Story 9 ⚠️

- [x] T111 [P] [US9] Contract test for search parameter in GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [x] T112 [P] [US9] Contract test for search across title and description in backend/tests/test_tasks.py

### Backend Implementation for User Story 9

- [x] T113 [US9] Add search functionality to task listing in backend/services/task_service.py
- [x] T114 [US9] Handle search query parameter in GET /api/{user_id}/tasks route

### Frontend Implementation for User Story 9

- [x] T115 [US9] Create SearchInput component in frontend/components/filters/SearchInput.tsx
- [x] T116 [US9] Add search parameter to getTasks in frontend/lib/api.ts
- [x] T117 [US9] Add SearchInput to task dashboard and integrate with task list

**Checkpoint**: User Story 9 complete - tasks can be searched

---

## Phase 12: User Story 10 - Filter Tasks (Priority: P3)

**Goal**: Users can filter tasks by status, priority, or tags

**Independent Test**: Filter by "completed" status, only completed tasks display

### Tests for User Story 10 ⚠️

- [x] T118 [P] [US10] Contract test for status filter in GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [x] T119 [P] [US10] Contract test for priority filter in GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [x] T120 [P] [US10] Contract test for tag filter in GET /api/{user_id}/tasks in backend/tests/test_tasks.py

### Backend Implementation for User Story 10

- [x] T121 [US10] Add status filter to task listing in backend/services/task_service.py
- [x] T122 [US10] Add priority filter to task listing in backend/services/task_service.py
- [x] T123 [US10] Add tag filter to task listing in backend/services/task_service.py
- [x] T124 [US10] Handle filter query parameters in GET /api/{user_id}/tasks route

### Frontend Implementation for User Story 10

- [x] T125 [P] [US10] Create StatusFilter component in frontend/components/filters/StatusFilter.tsx
- [x] T126 [P] [US10] Create PriorityFilter component in frontend/components/filters/PriorityFilter.tsx
- [x] T127 [P] [US10] Create TagFilter component in frontend/components/filters/TagFilter.tsx
- [x] T128 [US10] Create FilterBar component combining all filters in frontend/components/filters/FilterBar.tsx
- [x] T129 [US10] Add filter parameters to getTasks in frontend/lib/api.ts
- [x] T130 [US10] Add FilterBar to task dashboard with URL state management

**Checkpoint**: User Story 10 complete - tasks can be filtered

---

## Phase 13: User Story 11 - Sort Tasks (Priority: P3)

**Goal**: Users can sort tasks by creation date, priority, or title

**Independent Test**: Sort by priority, high-priority tasks appear first

### Tests for User Story 11 ⚠️

- [x] T131 [P] [US11] Contract test for sort parameter in GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [x] T132 [P] [US11] Contract test for priority sorting order in backend/tests/test_tasks.py

### Backend Implementation for User Story 11

- [x] T133 [US11] Add sort functionality to task listing in backend/services/task_service.py
- [x] T134 [US11] Handle sort query parameter in GET /api/{user_id}/tasks route

### Frontend Implementation for User Story 11

- [x] T135 [US11] Create SortSelect component in frontend/components/filters/SortSelect.tsx
- [x] T136 [US11] Add sort parameter to getTasks in frontend/lib/api.ts
- [x] T137 [US11] Add SortSelect to task dashboard FilterBar

**Checkpoint**: User Story 11 complete - all user stories implemented

---

## Phase 14: Polish & Cross-Cutting Concerns

**Purpose**: Production readiness and quality improvements

### Error Handling & Edge Cases

- [x] T138 [P] Add comprehensive error handling in backend routes
- [x] T139 [P] Add error boundary component in frontend/components/ui/ErrorBoundary.tsx
- [x] T140 [P] Implement session expiration handling in frontend
- [x] T141 Add input validation messages in TaskForm

### UI/UX Polish

- [x] T142 [P] Add loading skeletons in frontend/components/ui/Skeleton.tsx
- [x] T143 [P] Ensure mobile responsiveness (320px-768px viewport)
- [x] T144 Add keyboard navigation support to task list
- [x] T145 Add toast notifications in frontend/components/ui/Toast.tsx

### Performance & Observability

- [x] T146 [P] Add structured logging in backend using Python logging
- [x] T147 [P] Add request/response logging middleware in backend
- [x] T148 Implement optimistic updates in frontend for toggle/delete
- [x] T149 Add API response caching strategy in frontend

### Final Validation

- [x] T150 Run all backend tests and ensure 100% pass
- [x] T151 Run all frontend tests and ensure 100% pass
- [x] T152 Run quickstart.md validation (verify all setup steps work)
- [x] T153 Manual testing of all 11 user stories end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-13)**: All depend on Foundational phase completion
  - US1 (Auth) → US2, US3 (Create/View) - These 3 form the MVP
  - US4, US5, US6 (Update/Delete/Toggle) can start after foundational
  - US7-11 (Organization) can start after foundational but benefit from US2/US3
- **Polish (Phase 14)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (Auth - P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (Create - P1)**: Depends on US1 (needs auth for protected routes)
- **User Story 3 (View - P1)**: Depends on US2 (needs tasks to view)
- **User Story 4 (Update - P2)**: Can start after Foundational - May use US3 list view
- **User Story 5 (Delete - P2)**: Can start after Foundational - May use US3 list view
- **User Story 6 (Toggle - P2)**: Can start after Foundational - May use US3 list view
- **User Story 7 (Priority - P3)**: Can start after Foundational - Extends TaskForm from US2
- **User Story 8 (Tags - P3)**: Can start after Foundational - Requires new Tag model
- **User Story 9 (Search - P3)**: Can start after Foundational - Extends list from US3
- **User Story 10 (Filter - P3)**: Can start after Foundational - Extends list from US3
- **User Story 11 (Sort - P3)**: Can start after Foundational - Extends list from US3

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD Red-Green-Refactor)
- Backend implementation before frontend implementation
- Models before services, services before routes
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Within Phase 1 (Setup):**
```
T002, T003 (backend/frontend init) - parallel
T004, T005 (dependencies) - parallel
T006, T007 (env configs) - parallel
T009, T010, T011 (CLAUDE.md files) - parallel
```

**Within Phase 2 (Foundational):**
```
Backend models (T015, T016, T017) - parallel
Pydantic schemas (T021, T022) - parallel
Frontend config (T026, T027, T028, T029, T030) - parallel after T025
```

**Across User Stories (after Phase 2):**
```
US4, US5, US6 - can be developed in parallel (different endpoints)
US7, US8, US9, US10, US11 - can be developed in parallel (different features)
```

---

## Parallel Example: MVP Sprint (US1 + US2 + US3)

```bash
# After Phase 2 completion, launch US1 tests:
Task: T034 "Contract test for POST /api/auth/register"
Task: T035 "Contract test for POST /api/auth/login"
Task: T036 "Contract test for POST /api/auth/logout"
Task: T037 "Contract test for GET /api/auth/session"
Task: T038 "Contract test for 401 on invalid token"

# After US1 tests pass, launch frontend components in parallel:
Task: T042 "Create AuthGuard component"
Task: T043 "Create LoginForm component"
Task: T044 "Create RegisterForm component"

# Continue with US2 and US3 similarly...
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Create Task)
5. Complete Phase 5: User Story 3 (View Tasks)
6. **STOP and VALIDATE**: Test MVP independently - users can register, login, create, and view tasks
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Test → Deploy (authentication works)
3. Add US2 + US3 (Create/View) → Test → Deploy/Demo (MVP complete!)
4. Add US4, US5, US6 (Update/Delete/Toggle) → Test → Deploy (full CRUD)
5. Add US7-US11 (Organization) → Test → Deploy (complete feature set)
6. Each story adds value without breaking previous stories

### Suggested MVP Scope

**Minimum Viable Product consists of:**
- Phase 1: Setup (T001-T011)
- Phase 2: Foundational (T012-T033)
- Phase 3: User Story 1 - Authentication (T034-T048)
- Phase 4: User Story 2 - Create Task (T049-T058)
- Phase 5: User Story 3 - View Tasks (T059-T069)

**Total MVP tasks: 69 tasks**

---

## Summary

| Phase | User Story | Priority | Task Count | Cumulative |
|-------|-----------|----------|------------|------------|
| 1 | Setup | - | 11 | 11 |
| 2 | Foundational | - | 22 | 33 |
| 3 | US1 - Authentication | P1 | 15 | 48 |
| 4 | US2 - Create Task | P1 | 10 | 58 |
| 5 | US3 - View Tasks | P1 | 11 | 69 |
| 6 | US4 - Update Task | P2 | 8 | 77 |
| 7 | US5 - Delete Task | P2 | 7 | 84 |
| 8 | US6 - Toggle Completion | P2 | 7 | 91 |
| 9 | US7 - Set Priority | P3 | 8 | 99 |
| 10 | US8 - Add Tags | P3 | 11 | 110 |
| 11 | US9 - Search Tasks | P3 | 7 | 117 |
| 12 | US10 - Filter Tasks | P3 | 13 | 130 |
| 13 | US11 - Sort Tasks | P3 | 7 | 137 |
| 14 | Polish | - | 16 | 153 |

**Total: 153 tasks**

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD mandatory: Write tests first, verify they fail, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP (US1 + US2 + US3) delivers core value: authenticated task creation and viewing
