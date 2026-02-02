# Research: Todo AI Chatbot

**Date**: 2026-02-01 | **Feature**: 003-phase3-todo-ai-chatbot

## R-001: AI Agent Framework

**Decision**: Google Agent Development Kit (ADK) with Gemini as primary LLM
**Rationale**: Free tier generous (15 RPM, 1M tokens/day via Google AI Studio). ADK provides built-in MCP client support for connecting to MCP tool servers.
**Alternatives considered**:
- OpenAI Agents SDK: Requires paid API key, spec originally specified this
- LangChain: More complex, heavier dependency
- Direct Gemini API calls: No agent orchestration built-in

## R-002: LLM Fallback Provider

**Decision**: Groq as fallback when Gemini is rate-limited or unavailable
**Rationale**: Groq free tier provides fast inference with Llama/Mixtral models. ADK supports model swapping.
**Alternatives considered**:
- Ollama (local): Requires local GPU, not suitable for deployment
- No fallback: Single point of failure unacceptable

## R-003: MCP Server Implementation

**Decision**: Official MCP Python SDK (`mcp` package) with stdio transport, running in-process
**Rationale**: Standard protocol for AI-tool communication. The MCP server exposes 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) that the ADK agent invokes.
**Alternatives considered**:
- FastAPI direct tool functions: Loses MCP standardization benefit
- Separate MCP server process: Adds deployment complexity for no gain at this scale

## R-004: Authentication Migration

**Decision**: Supabase Auth replacing Better Auth from Phase 2
**Rationale**: User preference. Supabase provides free tier auth with JWT, email/password, and social login. Backend verifies Supabase JWTs.
**Alternatives considered**:
- Keep Better Auth: User explicitly chose Supabase
- Auth0: Paid beyond free limits

## R-005: Chat Frontend Approach

**Decision**: Custom Next.js chat component within existing frontend
**Rationale**: Fits existing monorepo structure. Simple chat UI (message list + input) doesn't need a heavy library. Tailwind CSS for styling.
**Alternatives considered**:
- OpenAI ChatKit: Requires OpenAI domain key setup, tied to OpenAI ecosystem
- Vercel AI SDK: Additional dependency, overkill for simple chat
- Streamlit: Python-based, doesn't fit Next.js frontend

## R-006: Deployment Platform

**Decision**: Hugging Face Spaces for backend deployment
**Rationale**: User preference. Free tier available. Supports Docker-based deployments for FastAPI apps.
**Alternatives considered**:
- Vercel: Frontend already there from Phase 2
- Railway: User chose Hugging Face

## R-007: Database Schema Extension

**Decision**: Add Conversation and Message tables to existing Neon PostgreSQL
**Rationale**: Reuse existing database. Task table already exists from Phase 2. New tables for chat persistence.
**Alternatives considered**:
- Supabase PostgreSQL: Would require migrating existing data
- Separate database: Unnecessary complexity

## R-008: Stateless Architecture Pattern

**Decision**: Each chat request fetches conversation history from DB, processes with agent, stores result
**Rationale**: Per spec requirements. Enables horizontal scaling, resilience to server restarts, independent request handling.
**Alternatives considered**:
- In-memory session state: Doesn't survive restarts, can't scale horizontally
