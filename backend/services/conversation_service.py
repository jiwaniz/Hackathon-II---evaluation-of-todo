"""Conversation persistence service for the AI chatbot."""

from datetime import datetime

from sqlmodel import Session, select

from models import Conversation, Message, MessageRole


def create_conversation(session: Session, user_id: str) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation(
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation(session: Session, conversation_id: int, user_id: str) -> Conversation | None:
    """Get a conversation by ID, scoped to user."""
    return session.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
    ).first()


def get_user_conversations(session: Session, user_id: str) -> list[Conversation]:
    """Get all conversations for a user, newest first."""
    return list(
        session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).all()
    )


def add_message(
    session: Session,
    conversation_id: int,
    user_id: str,
    role: MessageRole,
    content: str,
    tool_calls: str | None = None,
) -> Message:
    """Add a message to a conversation."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
        created_at=datetime.utcnow(),
    )
    session.add(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

    session.commit()
    session.refresh(message)
    return message


def get_messages(session: Session, conversation_id: int, user_id: str) -> list[Message]:
    """Get all messages for a conversation, in chronological order."""
    return list(
        session.exec(
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id,
            )
            .order_by(Message.created_at.asc())
        ).all()
    )
