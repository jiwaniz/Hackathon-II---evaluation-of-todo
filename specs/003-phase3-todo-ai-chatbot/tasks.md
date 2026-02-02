# Tasks: Todo AI Chatbot

**Input**: Design documents from `/specs/003-phase3-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD enforced per constitution. Test tasks included for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, new dependencies, and configuration for Phase 3

- [x] T001 Add Phase 3 dependencies to backend: `uv add google-genai google-adk mcp groq supabase` in backend/pyproject.toml
- [x] T002 [P] Add Supabase client dependency to frontend: `npm install @supabase/supabase-js @supabase/ssr` in frontend/package.json
- [x] T003 [P] Add Phase 3 environment variables to backend/config.py (GOOGLE_API_KEY, GROQ_API_KEY, SUPABASE_URL, SUPABASE_JWT_SECRET)
- [x] T004 [P] Add Phase 3 environment variables to frontend/.env.local (NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Warning**: No user story work can begin until this phase is complete

- [x] T005 Create Conversation SQLModel in backend/models/conversation.py per data-model.md
- [x] T006 [P] Create Message SQLModel in backend/models/message.py per data-model.md
- [x] T007 Update backend/models/__init__.py to export Conversation and Message models
- [x] T008 Create Alembic migration for Conversation and Message tables in backend/alembic/versions/
- [x] T009 Update backend/middleware/auth.py to verify Supabase JWT tokens instead of Better Auth JWT
- [x] T010 [P] Create Supabase client config in frontend/lib/supabase.ts
- [x] T011 [P] Create chat TypeScript types in frontend/types/chat.ts (ChatRequest, ChatResponse, Message, Conversation, ToolCall)
- [x] T012 Create MCP server skeleton with tool registration in backend/mcp_server/__init__.py and backend/mcp_server/server.py
- [x] T013 Implement 5 MCP tool functions (add_task, list_tasks, complete_task, delete_task, update_task) with error handling, user-scoped queries, and formatted output in backend/mcp_server/tools.py per contracts/mcp-tools.md
- [x] T014 Create conversation persistence service in backend/services/conversation_service.py (create_conversation, get_conversation, add_message, get_messages)
- [x] T015 Create chat orchestration service skeleton in backend/services/chat_service.py (initialize ADK agent with Gemini, connect to MCP tools)

**Checkpoint**: Foundation ready - MCP tools, models, auth, and services in place. User story implementation can begin.

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) MVP

**Goal**: User types "Add a task to buy groceries" in chat, system creates the task and confirms.

**Independent Test**: Send a chat message requesting task creation, verify task appears in DB and confirmation response is returned.

### Tests for User Story 1

- [x] T016 [P] [US1] Write contract test for POST /api/{user_id}/chat (create task intent) in backend/tests/test_chat.py
- [x] T017 [P] [US1] Write unit test for add_task MCP tool in backend/tests/test_mcp_tools.py

### Implementation for User Story 1

- [x] T018 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/routes/chat.py per contracts/chat-api.yaml
- [x] T019 [US1] Wire chat_service.py to receive message, fetch history from DB, run ADK agent with MCP tools, store response, return result
- [x] T020 [US1] Configure ADK agent system prompt for task creation intent recognition in backend/services/chat_service.py
- [x] T021 [US1] Register chat router in backend/main.py
- [x] T022 [P] [US1] Create ChatInput component in frontend/components/chat/ChatInput.tsx
- [x] T023 [P] [US1] Create MessageBubble component in frontend/components/chat/MessageBubble.tsx
- [x] T024 [US1] Create ChatWindow component in frontend/components/chat/ChatWindow.tsx (uses ChatInput + MessageBubble)
- [x] T025 [US1] Create useChat hook in frontend/hooks/useChat.ts (send message, receive response, manage local state)
- [x] T026 [US1] Add chat API functions to frontend/lib/api.ts (sendChatMessage)
- [x] T027 [US1] Create chat page at frontend/app/(dashboard)/chat/page.tsx using ChatWindow

**Checkpoint**: User can type a task creation message, see AI confirmation. Task is persisted in DB.

---

## Phase 4: User Story 2 - View and Query Tasks (Priority: P1)

**Goal**: User asks "Show me all my tasks" or "What's pending?" and sees filtered task list in chat.

**Independent Test**: Create tasks, then query via chat. Verify correct tasks listed in response.

### Tests for User Story 2

- [x] T028 [P] [US2] Write contract test for list_tasks MCP tool (all/pending/completed filters) in backend/tests/test_mcp_tools.py
- [x] T029 [P] [US2] Write integration test for chat list intent in backend/tests/test_chat.py

### Implementation for User Story 2

- [x] T030 [US2] Extend ADK agent system prompt to handle list/query intents with status filtering in backend/services/chat_service.py
- [x] T031 [US2] Verify list_tasks output format meets US2 acceptance criteria (status indicators, empty-state message) in backend/mcp_server/tools.py

**Checkpoint**: User can ask to see tasks with filters. Combined with US1, user can create and view tasks via chat.

---

## Phase 5: User Story 3 - Complete, Update, and Delete Tasks (Priority: P2)

**Goal**: User can mark tasks complete, update titles/descriptions, and delete tasks via natural language.

**Independent Test**: Create a task, then complete/update/delete it via chat commands. Verify DB state changes.

### Tests for User Story 3

- [x] T032 [P] [US3] Write unit tests for complete_task, update_task, delete_task MCP tools in backend/tests/test_mcp_tools.py
- [x] T033 [P] [US3] Write integration test for complete/update/delete chat intents in backend/tests/test_chat.py

### Implementation for User Story 3

- [x] T034 [US3] Extend ADK agent system prompt to handle complete/update/delete intents in backend/services/chat_service.py
- [x] T035 [US3] Verify error handling for "task not found" returns friendly messages per US3 acceptance scenario 4 in backend/mcp_server/tools.py
- [x] T036 [US3] Ensure agent confirms each action with friendly response including task details

**Checkpoint**: Full CRUD via chat. User can create, view, complete, update, and delete tasks through conversation.

---

## Phase 6: User Story 4 - Conversation Persistence (Priority: P2)

**Goal**: Chat conversations are saved and loadable after browser close or server restart.

**Independent Test**: Have a conversation, close browser, reopen chat page, verify previous messages load.

### Tests for User Story 4

- [x] T037 [P] [US4] Write test for conversation persistence (create, store messages, retrieve) in backend/tests/test_conversations.py
- [x] T038 [P] [US4] Write contract test for GET /api/{user_id}/conversations and GET /api/{user_id}/conversations/{id}/messages in backend/tests/test_conversations.py

### Implementation for User Story 4

- [x] T039 [US4] Create conversation history routes in backend/routes/conversations.py (list conversations, get messages) per contracts/chat-api.yaml
- [x] T040 [US4] Register conversations router in backend/main.py
- [x] T041 [US4] Update frontend/hooks/useChat.ts to load conversation history on mount
- [x] T042 [US4] Update frontend/lib/api.ts with getConversations and getMessages API functions
- [x] T043 [US4] Update chat page to display conversation history on load in frontend/app/(dashboard)/chat/page.tsx

**Checkpoint**: Conversations persist. User can close browser and resume where they left off.

---

## Phase 7: User Story 5 - Multi-Tool Chaining (Priority: P3)

**Goal**: User gives ambiguous commands like "Delete the meeting task" and agent chains list + delete operations.

**Independent Test**: Send "Delete the groceries task" when multiple tasks exist. Verify agent finds and deletes the correct one.

### Tests for User Story 5

- [x] T044 [P] [US5] Write integration test for multi-tool chaining (ambiguous delete) in backend/tests/test_chat.py

### Implementation for User Story 5

- [x] T045 [US5] Enhance ADK agent system prompt with instructions for chaining tools and handling ambiguity in backend/services/chat_service.py
- [x] T046 [US5] Add tool_calls field to ChatResponse and store in Message.tool_calls in backend/services/chat_service.py

**Checkpoint**: Agent handles ambiguous commands by chaining tools intelligently.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: LLM fallback, error handling, observability, and deployment readiness

- [x] T047 Implement Groq fallback in backend/services/chat_service.py (catch Gemini errors/rate limits, retry with Groq)
- [x] T048 [P] Add structured logging for chat operations in backend/services/chat_service.py
- [x] T049 [P] Add health check endpoint at /api/health in backend/main.py
- [x] T050 Handle edge cases: empty messages, non-task messages, long messages in backend/routes/chat.py
- [x] T051 [P] Add CORS configuration for Hugging Face Spaces domain in backend/main.py
- [x] T052 Validate SC-001: measure chat response time end-to-end, assert <5s for task creation intent in backend/tests/test_chat.py
- [x] T053 [P] Validate SC-002: run 10 sample NL commands (create, list, complete, update, delete x2) and assert >=9/10 correct intent mapping in backend/tests/test_chat.py
- [x] T054 Run quickstart.md validation end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2 - MVP target
- **Phase 4 (US2)**: Depends on Phase 2 - can run parallel to US1 (different intents, same infrastructure)
- **Phase 5 (US3)**: Depends on Phase 2 - can run parallel to US1/US2
- **Phase 6 (US4)**: Depends on Phase 2 + at least one of US1/US2/US3 (needs messages to persist)
- **Phase 7 (US5)**: Depends on US1 + US3 (needs create + delete to chain)
- **Phase 8 (Polish)**: Depends on all desired user stories

### User Story Dependencies

- **US1 (Task Creation)**: Independent after Phase 2
- **US2 (View Tasks)**: Independent after Phase 2
- **US3 (Complete/Update/Delete)**: Independent after Phase 2
- **US4 (Conversation Persistence)**: Needs at least one story complete (messages to persist)
- **US5 (Multi-Tool Chaining)**: Needs US1 + US3 (create then delete by name)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- MCP tool logic before agent prompt tuning
- Backend before frontend
- Core implementation before integration

### Parallel Opportunities

- T002, T003, T004 can run in parallel (different files)
- T005, T006 can run in parallel (different model files)
- T009, T010, T011 can run in parallel (different files, different stacks)
- T016, T017 can run in parallel (different test files)
- T022, T023 can run in parallel (different components)
- T028, T029 can run in parallel (different test types)
- US1, US2, US3 can all start after Phase 2 in parallel

---

## Parallel Example: User Story 1

```bash
# Launch tests in parallel:
Task: "Contract test for POST /api/{user_id}/chat in backend/tests/test_chat.py"
Task: "Unit test for add_task MCP tool in backend/tests/test_mcp_tools.py"

# Launch frontend components in parallel:
Task: "Create ChatInput in frontend/components/chat/ChatInput.tsx"
Task: "Create MessageBubble in frontend/components/chat/MessageBubble.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T015)
3. Complete Phase 3: User Story 1 (T016-T027)
4. **STOP and VALIDATE**: Test task creation via chat end-to-end
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational -> Foundation ready
2. Add US1 (Task Creation) -> Test -> Deploy (MVP!)
3. Add US2 (View Tasks) -> Test -> Deploy
4. Add US3 (Complete/Update/Delete) -> Test -> Deploy
5. Add US4 (Conversation Persistence) -> Test -> Deploy
6. Add US5 (Multi-Tool Chaining) -> Test -> Deploy
7. Polish -> Final deployment

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- TDD enforced: write tests first, verify they fail, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total: 54 tasks across 8 phases
