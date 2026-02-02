"""Tests for conversation persistence and history endpoints.

TDD: Written before implementation of conversation routes.
"""

from fastapi.testclient import TestClient
from sqlmodel import Session

from models import Conversation, Message, MessageRole, User
from services.conversation_service import add_message, create_conversation, get_messages


class TestConversationService:
    """Tests for conversation persistence service."""

    def test_create_conversation(self, session: Session, test_user: User):
        """Creating a conversation returns a valid conversation object."""
        conv = create_conversation(session, test_user.id)
        assert conv.id is not None
        assert conv.user_id == test_user.id

    def test_add_and_get_messages(self, session: Session, test_user: User):
        """Messages can be added and retrieved in order."""
        conv = create_conversation(session, test_user.id)
        add_message(session, conv.id, test_user.id, MessageRole.USER, "Hello")
        add_message(session, conv.id, test_user.id, MessageRole.ASSISTANT, "Hi there!")

        messages = get_messages(session, conv.id, test_user.id)
        assert len(messages) == 2
        assert messages[0].role == MessageRole.USER
        assert messages[1].role == MessageRole.ASSISTANT

    def test_conversation_user_isolation(
        self, session: Session, test_user: User, other_user: User
    ):
        """Users cannot see each other's conversations."""
        conv = create_conversation(session, test_user.id)
        add_message(session, conv.id, test_user.id, MessageRole.USER, "Secret")

        messages = get_messages(session, conv.id, other_user.id)
        assert len(messages) == 0


class TestConversationEndpoints:
    """Tests for GET /api/{user_id}/conversations endpoints."""

    def test_list_conversations(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict,
        test_conversation: Conversation,
    ):
        """Should list user's conversations."""
        response = client.get(
            f"/api/{test_user.id}/conversations",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert "conversations" in data

    def test_get_conversation_messages(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict,
        test_conversation: Conversation,
    ):
        """Should return messages for a conversation."""
        add_message(session, test_conversation.id, test_user.id, MessageRole.USER, "Test msg")

        response = client.get(
            f"/api/{test_user.id}/conversations/{test_conversation.id}/messages",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data["messages"]) >= 1

    def test_conversations_require_auth(self, client: TestClient, test_user: User):
        """Conversations endpoint requires auth."""
        response = client.get(f"/api/{test_user.id}/conversations")
        assert response.status_code == 401
