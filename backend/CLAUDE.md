# Backend Guidelines

## Stack (Hackathon Standards)

- **Python 3.13+** with **UV package manager** (mandatory)
- **FastAPI** (web framework)
- **SQLModel** (ORM - mandatory for FastAPI/Neon integration)
- **Neon PostgreSQL** (database - free tier)
- **python-jose** (JWT verification using BETTER_AUTH_SECRET)

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration and env vars
├── database.py             # Database connection
├── models/                 # SQLModel database models
│   ├── __init__.py
│   ├── user.py             # User model (Better Auth managed)
│   ├── task.py             # Task model
│   └── tag.py              # Tag model
├── routes/                 # API route handlers
│   ├── __init__.py
│   ├── auth.py             # Auth routes
│   ├── tasks.py            # Task CRUD routes
│   └── tags.py             # Tag routes
├── services/               # Business logic
│   ├── __init__.py
│   ├── task_service.py     # Task operations
│   └── tag_service.py      # Tag operations
├── middleware/             # Custom middleware
│   ├── __init__.py
│   └── auth.py             # JWT verification middleware
├── schemas/                # Pydantic request/response models
│   ├── __init__.py
│   ├── task.py             # Task schemas
│   └── auth.py             # Auth schemas
└── tests/                  # Test files
    ├── __init__.py
    ├── test_tasks.py
    └── test_auth.py
```

## Patterns

### Route Handlers (with {user_id} pattern)
```python
from fastapi import APIRouter, Depends, HTTPException, Path
from middleware.auth import verify_user_access

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("/")
async def list_tasks(
    user_id: str = Path(...),
    user: User = Depends(verify_user_access),  # Verifies JWT and URL match
    session: Session = Depends(get_session)
):
    """List all tasks for the specified user."""
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"data": {"tasks": tasks}}
```

### JWT Authentication (with URL {user_id} validation)
```python
from jose import jwt, JWTError
from fastapi import Request, HTTPException, Header
from config import settings

def verify_user_access(
    request: Request,
    authorization: str = Header(...),
    session: Session = Depends(get_session)
) -> User:
    """Verify JWT token AND match URL {user_id} with token's sub claim."""
    try:
        # Extract and verify token
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,  # Shared secret with frontend
            algorithms=["HS256"]
        )
        jwt_user_id = payload.get("sub")

        # Validate URL {user_id} matches JWT sub claim
        url_user_id = request.path_params.get("user_id")
        if url_user_id != jwt_user_id:
            raise HTTPException(status_code=403, detail="Access forbidden")

        # Fetch and return user
        user = session.get(User, jwt_user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Database Operations
```python
from sqlmodel import Session, select
from database import get_session

# Create
task = Task(user_id=user.id, title=data.title)
session.add(task)
session.commit()
session.refresh(task)

# Read
task = session.get(Task, task_id)
tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()

# Update
task.title = new_title
session.add(task)
session.commit()

# Delete
session.delete(task)
session.commit()
```

## API Conventions

- All task routes under `/api/{user_id}/` pattern (mandatory)
- Auth routes under `/api/auth/` (no user_id required)
- Return JSON responses with `{"data": ...}` or `{"error": ...}`
- Use Pydantic/SQLModel for request/response validation
- Handle errors with HTTPException
- Always validate URL {user_id} matches JWT sub claim
- Filter all queries by validated user_id

### Response Format
```python
# Success
return {"data": task, "message": "Task created"}

# Error
raise HTTPException(
    status_code=404,
    detail={"code": "NOT_FOUND", "message": "Task not found"}
)
```

## Security

- Validate JWT on every protected route using `BETTER_AUTH_SECRET`
- Validate URL `{user_id}` matches JWT `sub` claim (mandatory)
- Extract user_id from token, never trust client input
- Filter all queries by user_id from validated JWT
- Return 401 for invalid/missing/expired token
- Return 403 if URL `{user_id}` doesn't match JWT `sub` claim
- Never log passwords, tokens, or BETTER_AUTH_SECRET

## Environment Variables

```
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
BETTER_AUTH_SECRET=<shared-secret-with-frontend>
CORS_ORIGINS=http://localhost:3000
```

## Commands (using UV)

```bash
# Initialize project with UV
uv init
uv add fastapi sqlmodel python-jose passlib uvicorn alembic psycopg2-binary

# Development server
uv run uvicorn main:app --reload --port 8000

# Run tests
uv run pytest

# Database migrations
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"
```

## Spec References

- API Endpoints: @specs/api/rest-endpoints.md
- Database Schema: @specs/database/schema.md
- Task Features: @specs/features/task-crud.md
- Auth Flow: @specs/features/authentication.md
