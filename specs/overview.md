# Evolution of Todo - Project Overview

## Purpose

A progressive Todo application demonstrating the evolution from simple in-memory Python CLI to a production-grade distributed system. This project serves as a learning platform for Spec-Driven Development (SDD) and modern full-stack architecture.

## Current Phase

**Phase II: Full-Stack Web Application**

Transform the Phase I console app into a multi-user web application with persistent storage.

## Technology Stack (Free-Tier Optimized)

| Layer | Technology | Hosting | Free Tier Limits |
|-------|------------|---------|------------------|
| Frontend | Next.js 16+ (App Router), TypeScript, Tailwind CSS | Vercel | 100GB bandwidth/month |
| Backend | Python FastAPI, SQLModel | Railway/Vercel | 500 hours/month |
| Database | Neon Serverless PostgreSQL | Neon | 0.5GB storage, 3GB RAM |
| Auth | Better Auth + JWT Plugin | N/A (library) | Unlimited |

## Phase Evolution

### Phase I: Console App (Completed)
- In-memory Python CLI
- 5 core CRUD operations
- TDD with 62 tests passing

### Phase II: Full-Stack Web (Current)
- Multi-user authentication
- Persistent PostgreSQL storage
- RESTful API with JWT security
- Responsive Next.js frontend

### Phase III: AI Chatbot (Future)
- MCP integration
- Natural language task management
- Voice interface

## Project Structure

```
hackathon-todo/
├── specs/                    # Separated specifications
│   ├── overview.md           # This file
│   ├── features/             # Feature specifications
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/                  # API specifications
│   │   └── rest-endpoints.md
│   ├── database/             # Database specifications
│   │   └── schema.md
│   └── ui/                   # UI specifications
│       ├── components.md
│       └── pages.md
├── frontend/                 # Next.js application
│   ├── CLAUDE.md
│   ├── app/
│   ├── components/
│   └── lib/
├── backend/                  # FastAPI application
│   ├── CLAUDE.md
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── services/
├── CLAUDE.md                 # Root instructions
└── AGENTS.md                 # Agent rules
```

## Development Workflow

1. **Specify** → Write/update feature specs in `/specs`
2. **Plan** → Generate implementation plan with `/sp.plan`
3. **Tasks** → Break into actionable tasks with `/sp.tasks`
4. **Implement** → Execute via Claude Code with `/sp.implement`

## Key Constraints

- **Free-tier only**: All hosting must use free tiers
- **No manual coding**: All implementation via Claude Code
- **Spec-driven**: Every feature requires specification first
- **TDD mandatory**: Red-Green-Refactor workflow
- **User isolation**: Strict data separation per user

## References

- [Phase II Spec](./002-phase2-fullstack-webapp/spec.md)
- [Constitution](../.specify/memory/constitution.md)
- [Better Auth Docs](https://www.better-auth.com/)
- [Neon Docs](https://neon.tech/docs)
