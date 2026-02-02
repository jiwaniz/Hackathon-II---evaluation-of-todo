# Research: Phase II Full-Stack Web Application

**Feature**: 002-phase2-fullstack-webapp
**Date**: 2026-01-18
**Status**: Complete

## Research Summary

This document consolidates research findings for the Phase II implementation, resolving all technical unknowns identified during planning.

---

## 1. Better Auth + JWT Plugin Integration

### Decision
Use Better Auth with the `@better-auth/jwt` plugin for authentication, sharing `BETTER_AUTH_SECRET` between frontend and backend.

### Rationale
- Better Auth is designed for Next.js and provides built-in session management
- JWT Plugin enables stateless token issuance for cross-service verification
- Shared secret allows FastAPI backend to verify tokens independently without callback to frontend
- Free and open source with active maintenance

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| NextAuth.js | Less flexible JWT configuration, harder to share with Python backend |
| Auth0 | Free tier limits (7,000 MAU), adds external dependency |
| Clerk | Free tier limits (10,000 MAU), proprietary |
| Custom JWT | More code to maintain, security risks with DIY implementation |

### Implementation Pattern
```
Frontend (Next.js):
1. Install: npm install better-auth @better-auth/jwt
2. Configure in lib/auth.ts with JWT plugin enabled
3. Set BETTER_AUTH_SECRET in .env.local

Backend (FastAPI):
1. Install: uv add python-jose passlib
2. Create middleware to decode JWT using same secret
3. Validate URL {user_id} matches token sub claim
```

---

## 2. SQLModel + Neon PostgreSQL Integration

### Decision
Use SQLModel as the ORM for FastAPI with Neon Serverless PostgreSQL (free tier).

### Rationale
- SQLModel combines SQLAlchemy power with Pydantic validation
- Native FastAPI integration (same author)
- Type hints for better IDE support
- Neon free tier: 0.5GB storage, 3GB RAM - sufficient for MVP

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| SQLAlchemy alone | No Pydantic integration, more boilerplate |
| Tortoise ORM | Less mature, smaller community |
| Prisma (Python) | Early stage, better for Node.js |
| Supabase | More complex setup, overkill for MVP |

### Connection Pattern
```python
# database.py
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

### Neon Free Tier Limits
- Storage: 0.5 GB
- Compute: 0.25 CU
- Branches: 10
- Suitable for: ~100 users with 100 tasks each

---

## 3. UV Package Manager for Python

### Decision
Use UV as the Python package manager for the backend (hackathon standard).

### Rationale
- 10-100x faster than pip
- Built-in virtual environment management
- Lock file for reproducible builds
- Drop-in replacement for pip commands
- Actively maintained by Astral (ruff creators)

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| pip + venv | Slower, no lock file by default |
| Poetry | Slower than UV, more complex |
| PDM | Less adoption, fewer features than UV |
| Conda | Overkill for web apps, larger footprint |

### Usage Pattern
```bash
# Initialize project
cd backend
uv init

# Add dependencies
uv add fastapi sqlmodel uvicorn python-jose passlib alembic psycopg2-binary

# Run commands
uv run uvicorn main:app --reload
uv run pytest
uv run alembic upgrade head
```

---

## 4. API Endpoint Pattern with {user_id}

### Decision
All task endpoints use `/api/{user_id}/tasks` pattern with JWT validation.

### Rationale
- Explicit user scoping in URL for clarity
- Double validation: JWT token + URL parameter match
- RESTful resource hierarchy (users own tasks)
- Prevents accidental cross-user access via URL manipulation

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| `/api/tasks` (user from token only) | Less explicit, harder to debug |
| `/api/me/tasks` | Requires token parsing for every URL |
| `/api/users/{id}/tasks` | Verbose, same as chosen pattern |

### Security Pattern
```python
def verify_user_access(request: Request, authorization: str):
    # 1. Decode JWT token
    payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
    jwt_user_id = payload.get("sub")

    # 2. Get user_id from URL
    url_user_id = request.path_params.get("user_id")

    # 3. Validate match
    if url_user_id != jwt_user_id:
        raise HTTPException(status_code=403)
```

---

## 5. Next.js 16+ App Router

### Decision
Use Next.js 16+ with App Router for the frontend.

### Rationale
- Server Components by default (better performance)
- Simplified data fetching with async components
- Built-in loading and error states
- File-based routing with layouts
- Vercel free tier hosting optimized

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Next.js Pages Router | Legacy approach, less flexible |
| Remix | Smaller ecosystem, less Vercel optimization |
| Astro | Less suited for dynamic apps |
| SvelteKit | Smaller community, learning curve |

### Project Structure
```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── (auth)/             # Auth group
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   └── (dashboard)/        # Protected group
│       ├── layout.tsx      # Auth guard layout
│       └── tasks/page.tsx
├── components/
├── lib/
│   ├── api.ts              # API client
│   └── auth.ts             # Better Auth config
└── package.json
```

---

## 6. Monorepo Structure

### Decision
Single repository with `/frontend` and `/backend` directories, shared `/specs`.

### Rationale
- Single context for Claude Code (easier navigation)
- Shared specifications referenced by both apps
- Coordinated versioning and releases
- Simplified CI/CD pipeline

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Separate repos | Harder to coordinate, multiple contexts |
| Turborepo/Nx | Overkill for 2 projects |
| pnpm workspaces | Only for JS, excludes Python backend |

### Structure
```
/
├── frontend/           # Next.js app
│   ├── CLAUDE.md      # Frontend-specific guidelines
│   └── ...
├── backend/           # FastAPI app
│   ├── CLAUDE.md      # Backend-specific guidelines
│   └── ...
├── specs/             # Shared specifications
├── .spec-kit/         # Spec-Kit Plus config
├── CLAUDE.md          # Root (contains only @AGENTS.md)
└── AGENTS.md          # Project-wide agent rules
```

---

## 7. Free Tier Hosting Strategy

### Decision
Deploy frontend to Vercel, backend to Railway, database on Neon.

### Rationale
- All services have generous free tiers
- Vercel optimized for Next.js
- Railway supports Python/FastAPI with easy deployment
- Neon provides serverless PostgreSQL

### Free Tier Limits
| Service | Free Tier Limits |
|---------|------------------|
| Vercel | 100GB bandwidth/month, unlimited deploys |
| Railway | $5 credit/month (~500 hours) |
| Neon | 0.5GB storage, 3GB RAM |

### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|-----------------|
| Render | Slower cold starts on free tier |
| Fly.io | More complex setup |
| Heroku | No longer has free tier |

---

## 8. Testing Strategy

### Decision
TDD with pytest (backend) and Jest/React Testing Library (frontend).

### Rationale
- pytest: Python standard, excellent FastAPI support
- Jest: React ecosystem standard
- Both support async testing
- Integration tests for API endpoints
- Unit tests for business logic

### Test Structure
```
backend/tests/
├── unit/
│   ├── test_models.py
│   └── test_services.py
├── integration/
│   └── test_api.py
└── conftest.py

frontend/__tests__/
├── components/
├── pages/
└── lib/
```

---

## Resolved Unknowns

| Unknown | Resolution |
|---------|------------|
| Auth method | Better Auth + JWT Plugin |
| ORM choice | SQLModel (mandatory per spec) |
| Package manager | UV (mandatory per spec) |
| API pattern | /api/{user_id}/tasks |
| Frontend framework | Next.js 16+ App Router |
| Database | Neon PostgreSQL (free tier) |
| Hosting | Vercel + Railway + Neon |
| Testing | pytest + Jest |

---

## Next Steps

1. Generate `data-model.md` with SQLModel entity definitions
2. Generate `contracts/openapi.yaml` with full API specification
3. Generate `quickstart.md` with setup instructions
4. Complete `plan.md` with all sections filled
