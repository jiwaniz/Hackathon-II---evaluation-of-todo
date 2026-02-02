# Agent Rules for Evolution of Todo

## Core Rules

- Always reference tasks from specs before implementation
- Stop code generation until Task ID is approved
- Follow Spec-Driven Development (Specify → Plan → Tasks → Implement)
- Phase-specific specs only
- Only generate code if a Task ID is referenced
- No manual coding - all implementation via Claude Code with spec references

## Current Phase

**Phase II: Full-Stack Web Application** - Multi-user web app with authentication and persistence.

## Context Routing

**When working in a specific directory, follow that directory's CLAUDE.md:**

| Context | Guidelines File | Focus |
|---------|-----------------|-------|
| `/frontend/*` | `frontend/CLAUDE.md` | Next.js 16+, Better Auth, TypeScript, Tailwind |
| `/backend/*` | `backend/CLAUDE.md` | FastAPI, UV, SQLModel, JWT verification |
| Root/specs | This file (AGENTS.md) | Project-wide rules, spec references |

## Monorepo Structure

```
/frontend  → Next.js 16+ App (see frontend/CLAUDE.md)
/backend   → FastAPI Server (see backend/CLAUDE.md)
/specs     → Separated specifications (features, api, database, ui)
/src       → Phase I console app (legacy reference)
```

## Spec-Kit Structure

Specifications are organized in `/specs`:
- `/specs/overview.md` - Project overview and stack
- `/specs/features/` - Feature specs (task-crud.md, authentication.md)
- `/specs/api/` - API endpoint specs (rest-endpoints.md)
- `/specs/database/` - Schema specs (schema.md)
- `/specs/ui/` - UI specs (components.md, pages.md)

## How to Use Specs

1. Always read relevant spec before implementing
2. Reference specs with: @specs/features/task-crud.md
3. Update specs if requirements change
4. No implementation without spec reference

## Active Technologies

### Phase II (Current)
- Frontend: Next.js 16+, TypeScript, Tailwind CSS (Vercel Free Tier)
- Backend: Python FastAPI with UV, SQLModel ORM (Railway/Vercel Free Tier)
- Database: Neon Serverless PostgreSQL (Free Tier)
- Auth: Better Auth + JWT Plugin (shared BETTER_AUTH_SECRET)

### Phase I (Legacy)
- Python 3.13+ + argparse, dataclasses (001-phase1-todo-cli)
- In-memory only (Python dict/list)

## Development Workflow

1. Read spec: @specs/features/[feature].md
2. Implement backend: @backend/CLAUDE.md
3. Implement frontend: @frontend/CLAUDE.md
4. Test and iterate

## Commands

- Frontend: `cd frontend && npm run dev`
- Backend: `cd backend && uv run uvicorn main:app --reload`
- Phase I CLI: `uv run python -m src.main`

## Recent Changes
- 002-phase2-fullstack-webapp: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth JWT
- 001-phase1-todo-cli: Python 3.13+ console app with 62 tests passing
