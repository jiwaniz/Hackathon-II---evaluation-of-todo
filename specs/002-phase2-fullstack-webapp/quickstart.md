# Quickstart: Phase II Full-Stack Web Application

**Feature**: 002-phase2-fullstack-webapp
**Date**: 2026-01-18
**Status**: Ready for Implementation

## Prerequisites

### Required Software
- **Node.js 20+** (for Next.js frontend)
- **Python 3.13+** (for FastAPI backend)
- **UV** (Python package manager - mandatory)
- **Git** (version control)

### Required Accounts (Free Tier)
- **Neon** (https://neon.tech) - PostgreSQL database
- **Vercel** (https://vercel.com) - Frontend hosting (optional for dev)
- **Railway** (https://railway.app) - Backend hosting (optional for dev)

---

## 1. Clone and Structure

```bash
# Ensure you're in the project root
cd /path/to/evolution-of-todo

# Verify monorepo structure exists
ls -la frontend/ backend/
```

---

## 2. Backend Setup (FastAPI + SQLModel)

### 2.1 Initialize Python Project with UV

```bash
cd backend

# Initialize UV project
uv init

# Add dependencies
uv add fastapi sqlmodel uvicorn python-jose passlib alembic psycopg2-binary

# Add dev dependencies
uv add --dev pytest pytest-asyncio httpx
```

### 2.2 Environment Configuration

Create `backend/.env`:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Authentication (shared with frontend)
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars

# CORS
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

### 2.3 Database Setup

```bash
# Initialize Alembic for migrations
uv run alembic init alembic

# Configure alembic.ini with DATABASE_URL
# Edit alembic/env.py to import SQLModel models

# Generate initial migration
uv run alembic revision --autogenerate -m "initial schema"

# Apply migration
uv run alembic upgrade head
```

### 2.4 Run Backend

```bash
# Development server with hot reload
uv run uvicorn main:app --reload --port 8000

# Verify: http://localhost:8000/docs (OpenAPI UI)
```

---

## 3. Frontend Setup (Next.js 16+ with Better Auth)

### 3.1 Initialize Next.js Project

```bash
cd frontend

# Create Next.js app (if not exists)
npx create-next-app@latest . --typescript --tailwind --app --src-dir

# Install dependencies
npm install better-auth @better-auth/jwt
npm install --save-dev @types/node
```

### 3.2 Environment Configuration

Create `frontend/.env.local`:

```env
# Better Auth
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database (for Better Auth session storage)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
```

### 3.3 Configure Better Auth

Create `frontend/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "@better-auth/jwt";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [
    jwt({
      // JWT tokens for API authentication
      expiresIn: "7d",
    }),
  ],
  // Additional configuration...
});
```

### 3.4 Run Frontend

```bash
# Development server
npm run dev

# Verify: http://localhost:3000
```

---

## 4. Neon Database Setup

### 4.1 Create Neon Project

1. Go to https://neon.tech and sign up/login
2. Create new project: "evolution-of-todo"
3. Copy connection string from dashboard

### 4.2 Connection String Format

```
postgresql://[user]:[password]@[host].neon.tech/[database]?sslmode=require
```

### 4.3 Free Tier Limits

| Resource | Limit |
|----------|-------|
| Storage | 0.5 GB |
| Compute | 0.25 CU |
| Branches | 10 |

---

## 5. Verify Installation

### 5.1 Backend Health Check

```bash
# Should return {"status": "healthy"}
curl http://localhost:8000/health
```

### 5.2 Frontend Health Check

```bash
# Open in browser
open http://localhost:3000
```

### 5.3 Database Connection Test

```bash
cd backend
uv run python -c "from database import engine; print('Connected!')"
```

---

## 6. Development Workflow

### TDD Red-Green-Refactor Cycle

```bash
# Backend tests
cd backend
uv run pytest -v                    # Run all tests
uv run pytest tests/test_tasks.py   # Run specific test file
uv run pytest -k "test_create"      # Run tests matching pattern

# Frontend tests
cd frontend
npm test                            # Run Jest tests
npm run test:watch                  # Watch mode
```

### API Development

```bash
# Backend API docs (auto-generated)
open http://localhost:8000/docs      # Swagger UI
open http://localhost:8000/redoc     # ReDoc
```

---

## 7. Common Commands Reference

### Backend (UV)

| Command | Description |
|---------|-------------|
| `uv run uvicorn main:app --reload` | Start dev server |
| `uv run pytest` | Run tests |
| `uv run alembic upgrade head` | Apply migrations |
| `uv run alembic revision --autogenerate -m "msg"` | Create migration |
| `uv add <package>` | Add dependency |

### Frontend (npm)

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm test` | Run tests |
| `npm run lint` | Lint code |

---

## 8. Troubleshooting

### CORS Issues
Ensure `CORS_ORIGINS` in backend `.env` includes frontend URL.

### JWT Verification Fails
1. Verify `BETTER_AUTH_SECRET` is identical in both `.env` files
2. Check token expiration
3. Ensure Bearer prefix in Authorization header

### Database Connection Issues
1. Verify Neon project is active (auto-pauses after inactivity)
2. Check `sslmode=require` in connection string
3. Verify IP allowlist in Neon dashboard

### Import Errors (Python)
```bash
# Ensure virtual environment is active
uv sync
uv run python -c "import fastapi; print('OK')"
```

---

## 9. Project Structure Reference

```
evolution-of-todo/
├── frontend/                    # Next.js 16+ App
│   ├── app/                     # App Router pages
│   │   ├── (auth)/              # Auth route group
│   │   ├── (dashboard)/         # Protected route group
│   │   └── layout.tsx
│   ├── components/              # React components
│   ├── lib/                     # Utilities & auth
│   └── package.json
│
├── backend/                     # FastAPI App
│   ├── main.py                  # Entry point
│   ├── config.py                # Settings
│   ├── database.py              # DB connection
│   ├── models/                  # SQLModel models
│   ├── routes/                  # API routes
│   ├── services/                # Business logic
│   ├── middleware/              # Auth middleware
│   ├── schemas/                 # Pydantic schemas
│   └── pyproject.toml
│
├── specs/                       # Specifications
│   └── 002-phase2-fullstack-webapp/
│
└── CLAUDE.md                    # Agent instructions
```

---

## Next Steps

After setup is complete:

1. Run `/sp.tasks` to generate implementation tasks
2. Follow TDD workflow for each user story
3. Implement features per spec priority (P1 → P2 → P3)
