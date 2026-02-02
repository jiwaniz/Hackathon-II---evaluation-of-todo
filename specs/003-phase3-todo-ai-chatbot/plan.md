# Implementation Plan: Todo AI Chatbot

**Branch**: `003-phase3-todo-ai-chatbot` | **Date**: 2026-02-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-phase3-todo-ai-chatbot/spec.md`

## Summary

AI-powered chatbot that manages todos through natural language. Users type messages in a chat interface; a Google ADK agent with Gemini interprets intent and invokes MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) that operate on the existing Neon PostgreSQL database. Conversations persist statelessly via database-backed history. Supabase Auth replaces Better Auth. Groq serves as LLM fallback.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Google ADK, MCP Python SDK, Groq SDK, Supabase Auth
**Storage**: Neon PostgreSQL (existing, extended with Conversation + Message tables)
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web application (Hugging Face Spaces backend, Vercel frontend)
**Project Type**: web (monorepo: /backend + /frontend)
**Performance Goals**: <5s response time for chat messages (includes LLM inference)
**Constraints**: Gemini free tier 15 RPM, 1M tokens/day; Groq free tier as fallback
**Scale/Scope**: Single-user demo, <100 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Phase Isolation | PASS | Phase 3 standalone, extends Phase 2 DB but runs independently |
| Spec-Driven Development | PASS | Spec complete, plan in progress |
| Test-First (TDD) | PASS | Will enforce Red-Green-Refactor in tasks |
| Clean Architecture | PASS | Domain (models) → Services → API routes → MCP tools |
| API-First Design | PASS | OpenAPI contract defined in contracts/chat-api.yaml |
| Observability | PASS | Structured logging, health endpoint planned |
| Agentic Dev Stack | PASS | Using SDD workflow, PHR records |
| Better Auth (constitution) | VIOLATION | Supabase Auth chosen instead - see Complexity Tracking |
| Statelessness | PASS | Each chat request is independent, state in DB |
| User Isolation | PASS | All queries filtered by JWT user_id |

## Project Structure

### Documentation (this feature)

```text
specs/003-phase3-todo-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoints
│   └── mcp-tools.md     # MCP tool contracts
├── checklists/          # Quality checklists
│   └── requirements.md
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py                 # FastAPI app (extend with chat routes)
├── config.py               # Add Gemini/Groq/Supabase config
├── database.py             # Existing DB connection
├── models/
│   ├── task.py             # Existing Task model
│   ├── user.py             # Existing User model
│   ├── conversation.py     # NEW: Conversation model
│   └── message.py          # NEW: Message model
├── routes/
│   ├── tasks.py            # Existing task routes
│   ├── chat.py             # NEW: Chat endpoint
│   └── conversations.py    # NEW: Conversation history endpoints
├── services/
│   ├── task_service.py     # Existing task operations
│   ├── chat_service.py     # NEW: Agent orchestration
│   └── conversation_service.py  # NEW: Conversation persistence
├── mcp_server/
│   ├── __init__.py
│   ├── server.py           # NEW: MCP server with tool definitions
│   └── tools.py            # NEW: MCP tool implementations
├── middleware/
│   └── auth.py             # UPDATE: Supabase JWT verification
├── tests/
│   ├── test_chat.py        # NEW: Chat endpoint tests
│   ├── test_mcp_tools.py   # NEW: MCP tool tests
│   └── test_conversations.py  # NEW: Conversation tests
└── alembic/                # Migration for new tables

frontend/
├── app/
│   └── (dashboard)/
│       └── chat/
│           └── page.tsx    # NEW: Chat page
├── components/
│   └── chat/
│       ├── ChatWindow.tsx  # NEW: Chat message display
│       ├── ChatInput.tsx   # NEW: Message input
│       └── MessageBubble.tsx # NEW: Single message
├── lib/
│   ├── api.ts              # UPDATE: Add chat API calls
│   └── supabase.ts         # NEW: Supabase client config
├── hooks/
│   └── useChat.ts          # NEW: Chat state hook
└── types/
    └── chat.ts             # NEW: Chat TypeScript types
```

**Structure Decision**: Extends existing Phase 2 monorepo. Backend gets new `mcp_server/` directory for MCP tools, new models for chat persistence, and new routes for the chat endpoint. Frontend gets a new chat page and components.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Supabase Auth instead of Better Auth | User explicitly chose Supabase for Phase 3. Supabase provides free tier auth with built-in JWT, dashboard, and social login. | Better Auth would work but user has preference for Supabase's managed service and free tier. Constitution amendment recommended. |
