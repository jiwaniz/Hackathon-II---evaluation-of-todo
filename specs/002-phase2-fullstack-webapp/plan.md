# Implementation Plan: Phase II Full-Stack Web Application

**Branch**: `002-phase2-fullstack-webapp` | **Date**: 2026-01-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-phase2-fullstack-webapp/spec.md`

## Summary

Transform the Phase I in-memory Python console Todo application into a production-ready, multi-user web application with:
- **Frontend**: Next.js 16+ with Better Auth + JWT Plugin for authentication
- **Backend**: FastAPI with SQLModel ORM and UV package manager
- **Database**: Neon PostgreSQL (free tier)
- **Security**: Shared `BETTER_AUTH_SECRET` for JWT signing/verification, `/api/{user_id}/` endpoint pattern

All implementation via Claude Code with spec references (no manual coding), following TDD Red-Green-Refactor cycle.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Next.js 16+, Better Auth with JWT Plugin
**Storage**: Neon PostgreSQL (free tier - 0.5GB storage)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web (Vercel frontend, Railway backend)
**Project Type**: Web application (monorepo with frontend + backend)
**Performance Goals**: <2s task list load, <3s task creation, <1s search results
**Constraints**: Free-tier hosting only, TDD mandatory, no manual coding
**Scale/Scope**: 100 users MVP, 100 tasks per user maximum

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Phase Isolation** | ✅ PASS | Phase II standalone with own stack (Next.js, FastAPI, SQLModel, Neon) |
| **II. Spec-Driven Development** | ✅ PASS | Full SDD workflow: spec.md → plan.md → tasks.md → implement |
| **III. Test-First (TDD)** | ✅ PASS | Red-Green-Refactor mandated in spec constraints (C-005) |
| **IV. Clean Architecture** | ✅ PASS | Separation: models/, services/, routes/, middleware/ |
| **V. API-First Design** | ✅ PASS | OpenAPI spec in contracts/openapi.yaml |
| **VI. Observability** | ✅ PASS | Health endpoints, structured logging planned |
| **VII. Agentic Dev Stack** | ✅ PASS | Claude Code execution, PHR creation |

**Additional Constitution Requirements**:
- ✅ No manual coding (C-001)
- ✅ CLAUDE.md contains only `@AGENTS.md` (C-002)
- ✅ Free-tier hosting only (C-003)
- ✅ Better Auth with JWT for authentication
- ✅ User isolation via {user_id} URL pattern + JWT validation

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-fullstack-webapp/
├── spec.md              # Feature specification (11 user stories)
├── plan.md              # This file - implementation plan
├── research.md          # Phase 0 output - technology decisions
├── data-model.md        # Phase 1 output - SQLModel entities
├── quickstart.md        # Phase 1 output - setup instructions
├── contracts/           # Phase 1 output
│   └── openapi.yaml     # Full REST API specification
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration and env vars
├── database.py             # SQLModel database connection
├── models/                 # SQLModel database models
│   ├── __init__.py
│   ├── user.py             # User model (Better Auth managed)
│   ├── task.py             # Task model with Priority enum
│   └── tag.py              # Tag model + TaskTag junction
├── routes/                 # API route handlers
│   ├── __init__.py
│   ├── auth.py             # Auth routes (register, login, logout, session)
│   ├── tasks.py            # Task CRUD routes with {user_id} pattern
│   └── tags.py             # Tag routes
├── services/               # Business logic
│   ├── __init__.py
│   ├── task_service.py     # Task operations
│   └── tag_service.py      # Tag operations
├── middleware/             # Custom middleware
│   ├── __init__.py
│   └── auth.py             # JWT verification with URL validation
├── schemas/                # Pydantic request/response models
│   ├── __init__.py
│   ├── task.py             # Task schemas
│   └── auth.py             # Auth schemas
├── alembic/                # Database migrations
├── tests/                  # Test files
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   ├── test_auth.py        # Auth endpoint tests
│   └── test_tasks.py       # Task endpoint tests
└── pyproject.toml          # UV project config

frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Landing page
│   ├── (auth)/             # Auth route group (public)
│   │   ├── login/
│   │   │   └── page.tsx    # Login page
│   │   └── register/
│   │       └── page.tsx    # Registration page
│   └── (dashboard)/        # Protected route group
│       ├── layout.tsx      # Auth guard layout
│       └── tasks/
│           └── page.tsx    # Main task dashboard
├── components/             # React components
│   ├── ui/                 # Base UI components
│   ├── auth/               # Auth-related components
│   └── tasks/              # Task-related components
├── lib/                    # Utilities and configuration
│   ├── api.ts              # API client with auth
│   ├── auth.ts             # Better Auth configuration
│   └── auth-client.ts      # Client-side auth hooks
├── hooks/                  # Custom React hooks
├── types/                  # TypeScript types
├── __tests__/              # Test files
│   ├── components/
│   └── lib/
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.js
```

**Structure Decision**: Web application monorepo structure selected due to frontend (Next.js) + backend (FastAPI) separation requirement per spec.

## Complexity Tracking

> No constitution violations requiring justification. All design decisions align with Phase II requirements.

| Decision | Rationale | Simpler Alternative Rejected |
|----------|-----------|------------------------------|
| Monorepo | Spec requirement for /frontend + /backend separation | Single project doesn't meet multi-stack requirement |
| SQLModel | Hackathon standard (mandatory per spec) | Direct SQLAlchemy lacks Pydantic integration |
| Better Auth + JWT | Spec requirement for cross-service auth | Custom JWT implementation has security risks |

## Implementation Phases

### Phase 1: Project Setup & Infrastructure

**Goal**: Initialize monorepo structure with all dependencies configured

**Tasks**:
1. Initialize backend with UV (`uv init`, `uv add` dependencies)
2. Initialize frontend with Next.js 16+ and dependencies
3. Configure Neon PostgreSQL connection
4. Set up Alembic migrations
5. Configure Better Auth with JWT Plugin
6. Set up shared `BETTER_AUTH_SECRET` in both .env files
7. Create CLAUDE.md files (root, frontend, backend)

**Deliverable**: Running frontend (localhost:3000) and backend (localhost:8000)

### Phase 2: Authentication (User Stories 1)

**Goal**: Complete user registration, login, logout flow

**Tasks**:
1. Write auth endpoint tests (Red)
2. Implement User model with SQLModel
3. Implement auth routes (register, login, logout, session)
4. Implement JWT signature verification in FastAPI using the PyJWT or python-jose library, using the BETTER_AUTH_SECRET as the HMAC key to decode the token payload directly.Implement JWT middleware with URL {user_id} validation
5. Implement frontend auth pages and flows
6. Integration testing (Green)
7. Refactor for code quality

**Deliverable**: Working authentication with JWT tokens

### Phase 3: Core Task Management (User Stories 2, 3)

**Goal**: Create and view tasks with user isolation

**Tasks**:
1. Write task CRUD tests (Red)
2. Implement Task model with SQLModel
3. Implement task routes with {user_id} pattern
4. Implement task service layer
5. Build frontend task dashboard
6. Build task creation form
7. Integration testing (Green)
8. Refactor

**Deliverable**: Users can create and view their tasks

### Phase 4: Task Operations (User Stories 4, 5, 6)

**Goal**: Update, delete, and toggle task completion

**Tasks**:
1. Write update/delete/toggle tests (Red)
2. Implement task update endpoint
3. Implement task delete endpoint
4. Implement toggle completion endpoint
5. Build frontend edit and delete UI
6. Build toggle completion UI
7. Integration testing (Green)
8. Refactor

**Deliverable**: Full CRUD + toggle functionality

### Phase 5: Organization Features (User Stories 7, 8, 9, 10, 11)

**Goal**: Priority, tags, search, filter, sort

**Tasks**:
1. Write organization feature tests (Red)
2. Implement Tag model and TaskTag junction
3. Implement priority field and endpoints
4. Implement search functionality
5. Implement filter endpoints
6. Implement sort endpoints
7. Build frontend organization UI
8. Integration testing (Green)
9. Refactor

**Deliverable**: Complete task organization features

### Phase 6: Polish & Deployment Prep

**Goal**: Production readiness

**Tasks**:
1. Error handling and edge cases
2. Loading states and empty states
3. Mobile responsiveness
4. Performance optimization
5. Health check endpoints
6. Documentation updates
7. Final testing pass

**Deliverable**: Production-ready application

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Library | Better Auth + JWT Plugin | Hackathon standard, cross-service verification |
| ORM | SQLModel | Hackathon mandatory, FastAPI native integration |
| Package Manager | UV | Hackathon mandatory, 10-100x faster than pip |
| API Pattern | `/api/{user_id}/tasks` | Explicit user scoping, double validation |
| Frontend Router | App Router | Server Components, better performance |
| Database | Neon PostgreSQL | Free tier, serverless, sufficient for MVP |

## Dependencies Between Phases

```
Phase 1 (Setup) ──► Phase 2 (Auth) ──► Phase 3 (Core CRUD) ──► Phase 4 (Operations)
                                                                      │
                                                                      ▼
                                                              Phase 5 (Organization)
                                                                      │
                                                                      ▼
                                                              Phase 6 (Polish)
```

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Neon free tier limits | Medium | High | Monitor usage, optimize queries |
| JWT token mismatch | Low | High | Integration tests for auth flow |
| Railway cold starts | Medium | Medium | Health check endpoint, keep-alive |

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Feature Spec | `specs/002-phase2-fullstack-webapp/spec.md` | ✅ Complete |
| Research | `specs/002-phase2-fullstack-webapp/research.md` | ✅ Complete |
| Data Model | `specs/002-phase2-fullstack-webapp/data-model.md` | ✅ Complete |
| API Contract | `specs/002-phase2-fullstack-webapp/contracts/openapi.yaml` | ✅ Complete |
| Quickstart | `specs/002-phase2-fullstack-webapp/quickstart.md` | ✅ Complete |
| Spec-Kit Config | `.spec-kit/config.yaml` | ✅ Complete |
| Implementation Plan | `specs/002-phase2-fullstack-webapp/plan.md` | ✅ Complete |
| Tasks | `specs/002-phase2-fullstack-webapp/tasks.md` | ⏳ Pending `/sp.tasks` |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks with TDD workflow
2. Execute Phase 1 setup tasks
3. Follow Red-Green-Refactor for each user story
4. Create PHR for each significant implementation session
