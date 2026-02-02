# End-to-End Testing Checklist

**Feature**: Phase II Full-Stack Web Application
**Date**: 2026-01-22
**Purpose**: Manual validation of all 11 user stories

## Prerequisites

- [ ] Backend running: `cd backend && uv run uvicorn main:app --reload --port 8000`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Database connection verified via `/health` endpoint

---

## User Story 1: User Registration & Authentication (P1 - MVP)

### US1.1: Registration
- [ ] Navigate to `/register`
- [ ] Enter valid email and password
- [ ] Submit form and verify redirect to tasks page
- [ ] Verify user appears in header/menu

### US1.2: Login
- [ ] Logout (if logged in)
- [ ] Navigate to `/login`
- [ ] Enter registered credentials
- [ ] Verify successful login and redirect

### US1.3: Logout
- [ ] Click logout button in user menu
- [ ] Verify redirect to login/landing page
- [ ] Verify protected routes are inaccessible

### US1.4: Session Persistence
- [ ] Login and refresh the page
- [ ] Verify session persists
- [ ] Verify user data still displayed

---

## User Story 2: Create Task (P1 - MVP)

### US2.1: Create Task with Title Only
- [ ] Click "Add Task" button
- [ ] Enter title "Test Task 1"
- [ ] Submit and verify task appears in list

### US2.2: Create Task with Description
- [ ] Click "Add Task" button
- [ ] Enter title and description
- [ ] Submit and verify both display correctly

### US2.3: Validation
- [ ] Try to submit empty title
- [ ] Verify error message appears
- [ ] Verify form doesn't submit

---

## User Story 3: View All Tasks (P1 - MVP)

### US3.1: View Task List
- [ ] Create multiple tasks (if not already)
- [ ] Verify all tasks display in list
- [ ] Verify title, status, priority visible for each

### US3.2: Empty State
- [ ] Delete all tasks (or use new user)
- [ ] Verify "No tasks yet" message displays
- [ ] Verify CTA button to create task

### US3.3: User Isolation
- [ ] Create task as User A
- [ ] Logout and login as User B
- [ ] Verify User B cannot see User A's tasks

---

## User Story 4: Update Task (P2)

### US4.1: Edit Title
- [ ] Click edit button on a task
- [ ] Change title
- [ ] Save and verify title updated

### US4.2: Edit Description
- [ ] Click edit button
- [ ] Change/add description
- [ ] Save and verify description updated

### US4.3: Edit Priority
- [ ] Click edit button
- [ ] Change priority level
- [ ] Save and verify priority badge updated

---

## User Story 5: Delete Task (P2)

### US5.1: Delete with Confirmation
- [ ] Click delete button on a task
- [ ] Verify confirmation dialog appears
- [ ] Confirm deletion
- [ ] Verify task removed from list

### US5.2: Cancel Deletion
- [ ] Click delete button
- [ ] Click "Cancel" in dialog
- [ ] Verify task still present

---

## User Story 6: Toggle Task Completion (P2)

### US6.1: Mark Complete
- [ ] Click checkbox on incomplete task
- [ ] Verify checkbox becomes checked
- [ ] Verify task shows completed styling (strikethrough)

### US6.2: Mark Incomplete
- [ ] Click checkbox on completed task
- [ ] Verify checkbox unchecks
- [ ] Verify strikethrough removed

### US6.3: Persistence
- [ ] Toggle a task
- [ ] Refresh page
- [ ] Verify state persisted

---

## User Story 7: Set Task Priority (P3)

### US7.1: Create with Priority
- [ ] Create task with "High" priority
- [ ] Verify red priority badge displays
- [ ] Create task with "Low" priority
- [ ] Verify green priority badge displays

### US7.2: Update Priority
- [ ] Edit existing task
- [ ] Change priority from Medium to High
- [ ] Save and verify badge color changes

---

## User Story 8: Add Tags/Categories (P3)

### US8.1: Add Single Tag
- [ ] Create or edit task
- [ ] Add tag "work"
- [ ] Save and verify tag displays

### US8.2: Add Multiple Tags
- [ ] Edit task
- [ ] Add tags "urgent", "personal"
- [ ] Save and verify all tags display

### US8.3: Remove Tags
- [ ] Edit task with tags
- [ ] Remove a tag
- [ ] Save and verify tag removed

---

## User Story 9: Search Tasks (P3)

### US9.1: Search by Title
- [ ] Enter search term matching a task title
- [ ] Verify matching tasks display
- [ ] Verify non-matching tasks hidden

### US9.2: Search by Description
- [ ] Search for text in task description
- [ ] Verify matching task displays

### US9.3: Clear Search
- [ ] Clear search input
- [ ] Verify all tasks display again

---

## User Story 10: Filter Tasks (P3)

### US10.1: Filter by Status
- [ ] Select "Completed" status filter
- [ ] Verify only completed tasks show
- [ ] Select "Pending" status filter
- [ ] Verify only incomplete tasks show

### US10.2: Filter by Priority
- [ ] Select "High" priority filter
- [ ] Verify only high priority tasks show

### US10.3: Filter by Tag
- [ ] Select a tag filter
- [ ] Verify only tasks with that tag show

### US10.4: Combined Filters
- [ ] Apply status + priority filter
- [ ] Verify filters combine correctly

### US10.5: Clear Filters
- [ ] Click "Clear filters" or reset
- [ ] Verify all tasks display

---

## User Story 11: Sort Tasks (P3)

### US11.1: Sort by Created Date
- [ ] Select "Newest first" sort
- [ ] Verify tasks ordered by creation date descending
- [ ] Select "Oldest first" sort
- [ ] Verify order reversed

### US11.2: Sort by Priority
- [ ] Select "Priority" sort
- [ ] Verify high priority tasks appear first

### US11.3: Sort by Title
- [ ] Select "Title A-Z" sort
- [ ] Verify alphabetical ordering

---

## Cross-Cutting Concerns

### Error Handling
- [ ] Disconnect network and try action
- [ ] Verify error message displays
- [ ] Reconnect and retry

### Mobile Responsiveness
- [ ] Test on 320px viewport width
- [ ] Verify floating add button appears
- [ ] Verify touch targets are adequate

### Keyboard Navigation
- [ ] Navigate task list with arrow keys
- [ ] Toggle task with Enter/Space
- [ ] Edit task with 'e' key
- [ ] Delete task with 'd' key

### Session Expiration
- [ ] Let session expire (or manually clear token)
- [ ] Try to perform action
- [ ] Verify redirect to login

---

## Test Results Summary

| User Story | Tests | Passed | Failed | Status |
|------------|-------|--------|--------|--------|
| US1 - Auth | 4 | - | - | - |
| US2 - Create | 3 | - | - | - |
| US3 - View | 3 | - | - | - |
| US4 - Update | 3 | - | - | - |
| US5 - Delete | 2 | - | - | - |
| US6 - Toggle | 3 | - | - | - |
| US7 - Priority | 2 | - | - | - |
| US8 - Tags | 3 | - | - | - |
| US9 - Search | 3 | - | - | - |
| US10 - Filter | 5 | - | - | - |
| US11 - Sort | 3 | - | - | - |
| Cross-Cutting | 4 | - | - | - |
| **Total** | **38** | - | - | - |

**Tester**: _______________
**Date**: _______________
**Result**: [ ] PASS / [ ] FAIL
