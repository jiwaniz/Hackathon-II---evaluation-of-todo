"""Pytest fixtures for Evolution of Todo backend tests.

This module provides shared fixtures for:
- Test database setup and teardown
- Test client configuration
- Mock user authentication
- Sample data factories
"""

from collections.abc import Generator
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from config import settings
from database import get_session

# Ensure Supabase JWT path is used in tests (avoids session table lookup)
settings.supabase_jwt_secret = settings.better_auth_secret

from main import app
from models import Conversation, Message, MessageRole, Priority, Tag, Task, User


# Test database engine (in-memory SQLite for speed)
@pytest.fixture(name="engine")
def engine_fixture():
    """Create a test database engine using in-memory SQLite."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with overridden database session."""

    def get_session_override() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


# User fixtures
@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        id=str(uuid4()),
        email="test@example.com",
        name="Test User",
        email_verified=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="other_user")
def other_user_fixture(session: Session) -> User:
    """Create another test user for isolation testing."""
    user = User(
        id=str(uuid4()),
        email="other@example.com",
        name="Other User",
        email_verified=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# JWT token fixtures
@pytest.fixture(name="auth_token")
def auth_token_fixture(test_user: User) -> str:
    """Generate a valid JWT token for the test user."""
    payload = {
        "sub": test_user.id,
        "email": test_user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(auth_token: str) -> dict[str, str]:
    """Generate authorization headers with the test user's token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(name="other_auth_headers")
def other_auth_headers_fixture(other_user: User) -> dict[str, str]:
    """Generate authorization headers for the other test user."""
    payload = {
        "sub": other_user.id,
        "email": other_user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


# Supabase JWT fixtures (Phase 3)
@pytest.fixture(name="supabase_auth_token")
def supabase_auth_token_fixture(test_user: User) -> str:
    """Generate a Supabase-style JWT token for the test user."""
    payload = {
        "sub": test_user.id,
        "email": test_user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.supabase_jwt_secret or settings.better_auth_secret, algorithm="HS256")


@pytest.fixture(name="supabase_auth_headers")
def supabase_auth_headers_fixture(supabase_auth_token: str) -> dict[str, str]:
    """Generate authorization headers with Supabase JWT."""
    return {"Authorization": f"Bearer {supabase_auth_token}"}


# Conversation fixtures (Phase 3)
@pytest.fixture(name="test_conversation")
def test_conversation_fixture(session: Session, test_user: User) -> Conversation:
    """Create a test conversation."""
    conversation = Conversation(
        user_id=test_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


# Task fixtures
@pytest.fixture(name="test_task")
def test_task_fixture(session: Session, test_user: User) -> Task:
    """Create a test task for the test user."""
    task = Task(
        user_id=test_user.id,
        title="Test Task",
        description="A test task description",
        completed=False,
        priority=Priority.MEDIUM,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="completed_task")
def completed_task_fixture(session: Session, test_user: User) -> Task:
    """Create a completed test task."""
    task = Task(
        user_id=test_user.id,
        title="Completed Task",
        description="A completed task",
        completed=True,
        priority=Priority.HIGH,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="other_user_task")
def other_user_task_fixture(session: Session, other_user: User) -> Task:
    """Create a task owned by another user (for isolation testing)."""
    task = Task(
        user_id=other_user.id,
        title="Other User Task",
        description="Task belonging to another user",
        completed=False,
        priority=Priority.LOW,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# Tag fixtures
@pytest.fixture(name="test_tag")
def test_tag_fixture(session: Session, test_user: User) -> Tag:
    """Create a test tag for the test user."""
    tag = Tag(
        user_id=test_user.id,
        name="test-tag",
        created_at=datetime.utcnow(),
    )
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


# Factory fixtures for creating multiple items
@pytest.fixture(name="task_factory")
def task_factory_fixture(session: Session, test_user: User):
    """Factory fixture for creating tasks with custom attributes."""

    def create_task(**kwargs: Any) -> Task:
        defaults = {
            "user_id": test_user.id,
            "title": "Factory Task",
            "description": None,
            "completed": False,
            "priority": Priority.MEDIUM,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        defaults.update(kwargs)
        task = Task(**defaults)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    return create_task
