"""Contract tests for authentication endpoints (User Story 1).

TDD: These tests should FAIL initially and pass after implementation.

Tests:
- T034: POST /api/auth/register
- T035: POST /api/auth/login
- T036: POST /api/auth/logout
- T037: GET /api/auth/session
- T038: 401 on invalid/missing token
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session

from config import settings
from models import User


# =============================================================================
# T034: Contract test for POST /api/auth/register
# =============================================================================
class TestRegister:
    """Tests for POST /api/auth/register endpoint."""

    def test_register_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123",
                "name": "New User",
            },
        )

        assert response.status_code == 201
        data = response.json()

        # Check response structure
        assert "data" in data
        assert "user" in data["data"]
        assert "token" in data["data"]

        # Check user fields
        user = data["data"]["user"]
        assert user["email"] == "newuser@example.com"
        assert user["name"] == "New User"
        assert "id" in user
        assert "created_at" in user

        # Check token is valid JWT
        token = data["data"]["token"]
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
        assert payload["sub"] == user["id"]
        assert payload["email"] == user["email"]

    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """Test registration with existing email returns 409."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user.email,  # Already exists
                "password": "SecurePass123",
            },
        )

        assert response.status_code == 409
        data = response.json()
        assert "error" in data or "detail" in data

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email returns 400."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass123",
            },
        )

        assert response.status_code == 422  # Pydantic validation error

    def test_register_weak_password(self, client: TestClient):
        """Test registration with weak password returns 400."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "weakpass@example.com",
                "password": "short",  # Too short (< 8 chars)
            },
        )

        assert response.status_code == 422  # Pydantic validation error

    def test_register_missing_email(self, client: TestClient):
        """Test registration without email returns 422."""
        response = client.post(
            "/api/auth/register",
            json={"password": "SecurePass123"},
        )

        assert response.status_code == 422

    def test_register_missing_password(self, client: TestClient):
        """Test registration without password returns 422."""
        response = client.post(
            "/api/auth/register",
            json={"email": "nopass@example.com"},
        )

        assert response.status_code == 422


# =============================================================================
# T035: Contract test for POST /api/auth/login
# =============================================================================
class TestLogin:
    """Tests for POST /api/auth/login endpoint."""

    def test_login_success(self, client: TestClient, session: Session):
        """Test successful login with valid credentials."""
        # First register a user
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "logintest@example.com",
                "password": "SecurePass123",
            },
        )
        assert register_response.status_code == 201

        # Now login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "logintest@example.com",
                "password": "SecurePass123",
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "data" in data
        assert "user" in data["data"]
        assert "token" in data["data"]
        assert "expires_at" in data["data"]

        # Check user fields
        user = data["data"]["user"]
        assert user["email"] == "logintest@example.com"
        assert "id" in user

        # Check token is valid JWT
        token = data["data"]["token"]
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
        assert payload["sub"] == user["id"]

    def test_login_invalid_password(self, client: TestClient, session: Session):
        """Test login with wrong password returns 401."""
        # First register a user
        client.post(
            "/api/auth/register",
            json={
                "email": "wrongpass@example.com",
                "password": "CorrectPass123",
            },
        )

        # Login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "email": "wrongpass@example.com",
                "password": "WrongPassword123",
            },
        )

        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent email returns 401."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "AnyPassword123",
            },
        )

        assert response.status_code == 401

    def test_login_missing_email(self, client: TestClient):
        """Test login without email returns 422."""
        response = client.post(
            "/api/auth/login",
            json={"password": "SecurePass123"},
        )

        assert response.status_code == 422

    def test_login_missing_password(self, client: TestClient):
        """Test login without password returns 422."""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com"},
        )

        assert response.status_code == 422


# =============================================================================
# T036: Contract test for POST /api/auth/logout
# =============================================================================
class TestLogout:
    """Tests for POST /api/auth/logout endpoint."""

    def test_logout_success(self, client: TestClient, auth_headers: dict):
        """Test successful logout with valid token."""
        response = client.post("/api/auth/logout", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_logout_without_token(self, client: TestClient):
        """Test logout without token returns 401."""
        response = client.post("/api/auth/logout")

        assert response.status_code == 401

    def test_logout_with_invalid_token(self, client: TestClient):
        """Test logout with invalid token returns 401."""
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401


# =============================================================================
# T037: Contract test for GET /api/auth/session
# =============================================================================
class TestSession:
    """Tests for GET /api/auth/session endpoint."""

    def test_session_success(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test getting current session with valid token."""
        response = client.get("/api/auth/session", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "data" in data
        assert "user" in data["data"]
        assert "expires_at" in data["data"]

        # Check user matches token
        user = data["data"]["user"]
        assert user["id"] == test_user.id
        assert user["email"] == test_user.email

    def test_session_without_token(self, client: TestClient):
        """Test session check without token returns 401."""
        response = client.get("/api/auth/session")

        assert response.status_code == 401

    def test_session_with_invalid_token(self, client: TestClient):
        """Test session check with invalid token returns 401."""
        response = client.get(
            "/api/auth/session",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401


# =============================================================================
# T038: Contract test for 401 on invalid/missing token
# =============================================================================
class TestUnauthorized:
    """Tests for 401 responses on invalid/missing tokens."""

    def test_missing_authorization_header(self, client: TestClient):
        """Test request without Authorization header returns 401."""
        response = client.get("/api/auth/session")
        assert response.status_code == 401

    def test_malformed_authorization_header(self, client: TestClient):
        """Test request with malformed Authorization header returns 401."""
        response = client.get(
            "/api/auth/session",
            headers={"Authorization": "NotBearer token123"},
        )
        assert response.status_code == 401

    def test_invalid_jwt_signature(self, client: TestClient):
        """Test request with token signed by wrong secret returns 401."""
        # Create token with wrong secret
        payload = {
            "sub": "fake-user-id",
            "email": "fake@example.com",
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
        }
        fake_token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")

        response = client.get(
            "/api/auth/session",
            headers={"Authorization": f"Bearer {fake_token}"},
        )
        assert response.status_code == 401

    def test_expired_token(self, client: TestClient, test_user: User):
        """Test request with expired token returns 401."""
        # Create expired token
        payload = {
            "sub": test_user.id,
            "email": test_user.email,
            "exp": datetime.utcnow() - timedelta(hours=1),  # Expired
            "iat": datetime.utcnow() - timedelta(days=8),
        }
        expired_token = jwt.encode(
            payload, settings.better_auth_secret, algorithm="HS256"
        )

        response = client.get(
            "/api/auth/session",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401

    def test_empty_bearer_token(self, client: TestClient):
        """Test request with empty Bearer token returns 401."""
        response = client.get(
            "/api/auth/session",
            headers={"Authorization": "Bearer "},
        )
        assert response.status_code == 401

    def test_logout_requires_auth(self, client: TestClient):
        """Test logout endpoint requires authentication."""
        response = client.post("/api/auth/logout")
        assert response.status_code == 401
