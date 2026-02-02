"""Conversation history endpoints for the AI chatbot."""

import json

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session

from database import get_session
from middleware.auth import verify_user_access
from models import User
from services.conversation_service import get_messages, get_user_conversations

router = APIRouter(prefix="/api/{user_id}/conversations", tags=["conversations"])


@router.get("/")
async def list_conversations(
    user_id: str = Path(...),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """List all conversations for the authenticated user."""
    conversations = get_user_conversations(session, user.id)
    return {
        "data": {
            "conversations": [
                {
                    "id": c.id,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                }
                for c in conversations
            ]
        }
    }


@router.get("/{conversation_id}/messages")
async def get_conversation_messages(
    user_id: str = Path(...),
    conversation_id: int = Path(...),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Get all messages for a specific conversation."""
    messages = get_messages(session, conversation_id, user.id)
    return {
        "data": {
            "messages": [
                {
                    "id": m.id,
                    "role": m.role.value,
                    "content": m.content,
                    "tool_calls": json.loads(m.tool_calls) if m.tool_calls else None,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in messages
            ]
        }
    }
