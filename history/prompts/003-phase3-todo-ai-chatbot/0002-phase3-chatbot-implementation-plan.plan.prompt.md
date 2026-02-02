---
id: "0002"
title: phase3-chatbot-implementation-plan
stage: plan
date: 2026-02-01
surface: claude-code
model: claude-opus-4-5-20251101
feature: 003-phase3-todo-ai-chatbot
branch: 003-phase3-todo-ai-chatbot
user: zahra
command: /sp.plan
labels: [plan, phase3, chatbot, mcp, adk, gemini]
links:
  spec: specs/003-phase3-todo-ai-chatbot/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/003-phase3-todo-ai-chatbot/plan.md
  - specs/003-phase3-todo-ai-chatbot/research.md
  - specs/003-phase3-todo-ai-chatbot/data-model.md
  - specs/003-phase3-todo-ai-chatbot/quickstart.md
  - specs/003-phase3-todo-ai-chatbot/contracts/chat-api.yaml
  - specs/003-phase3-todo-ai-chatbot/contracts/mcp-tools.md
tests:
  - ""
---

## Prompt

/sp.plan - Generate implementation plan for Phase 3 Todo AI Chatbot. Tech stack: Google ADK + Gemini (primary), Groq (fallback), MCP Python SDK, FastAPI, SQLModel, Neon PostgreSQL, Supabase Auth, Next.js chat UI, Hugging Face deployment.

## Response snapshot

Generated complete implementation plan with: Phase 0 research (8 decisions documented), Phase 1 design artifacts (data-model with 3 entities, OpenAPI contract for chat endpoints, MCP tools contract for 5 tools, quickstart guide). Constitution check identified 1 violation (Supabase Auth vs Better Auth) with justification. Project structure extends Phase 2 monorepo with new backend/mcp_server/, chat routes, conversation models, and frontend chat components.

## Outcome

- ✅ Impact: Plan complete, ready for /sp.tasks
- 🧪 Tests: N/A (plan stage)
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, quickstart.md, chat-api.yaml, mcp-tools.md)
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: Constitution violation (Supabase vs Better Auth) documented with justification. Token-optimized by reusing existing Phase 2 structure.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASS (1 justified violation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
