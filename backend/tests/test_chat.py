"""Tests for the chat endpoint POST /api/{user_id}/chat.

TDD: These tests are written FIRST and should FAIL before implementation.
"""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlmodel import Session

from models import Conversation, Task, User


class TestChatEndpoint:
    """Tests for POST /api/{user_id}/chat."""

    def test_chat_create_task_intent(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Given a logged-in user, when they send 'Add a task to buy groceries',
        then the system should return a confirmation response."""
        with patch(
            "routes.chat.process_chat_message",
            new_callable=AsyncMock,
            return_value={
                "conversation_id": 1,
                "response": "I've created a task 'Buy groceries' for you!",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "input": {"title": "Buy groceries"},
                        "output": {"task_id": 1, "status": "created", "title": "Buy groceries"},
                    }
                ],
            },
        ):
            response = client.post(
                f"/api/{test_user.id}/chat",
                json={"message": "Add a task to buy groceries"},
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["conversation_id"] == 1
        assert "Buy groceries" in data["response"]
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["tool"] == "add_task"

    def test_chat_requires_auth(self, client: TestClient, test_user: User):
        """Chat endpoint should return 401 without auth."""
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Hello"},
        )
        assert response.status_code == 401

    def test_chat_empty_message_rejected(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Empty messages should be rejected with 422."""
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": ""},
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_chat_user_isolation(
        self, client: TestClient, test_user: User, other_user: User, other_auth_headers: dict
    ):
        """User cannot access another user's chat endpoint."""
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Hello"},
            headers=other_auth_headers,
        )
        assert response.status_code == 403

    def test_chat_creates_new_conversation(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """When no conversation_id is provided, a new conversation should be created."""
        with patch(
            "routes.chat.process_chat_message",
            new_callable=AsyncMock,
            return_value={
                "conversation_id": 42,
                "response": "Hello! How can I help you with your tasks?",
                "tool_calls": [],
            },
        ):
            response = client.post(
                f"/api/{test_user.id}/chat",
                json={"message": "Hello"},
                headers=auth_headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["conversation_id"] == 42

    def test_chat_continues_existing_conversation(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """When conversation_id is provided, it should continue that conversation."""
        with patch(
            "routes.chat.process_chat_message",
            new_callable=AsyncMock,
            return_value={
                "conversation_id": 5,
                "response": "Sure, I can help with that!",
                "tool_calls": [],
            },
        ):
            response = client.post(
                f"/api/{test_user.id}/chat",
                json={"conversation_id": 5, "message": "Show my tasks"},
                headers=auth_headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["conversation_id"] == 5
