"""Chat endpoint for the AI chatbot - POST /api/{user_id}/chat."""

from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

from database import get_session
from middleware.auth import verify_user_access
from models import User
from schemas.chat import ChatRequest, ChatResponse, ChatResponseData, ToolCallSchema
from services.chat_service import process_chat_message

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(
    body: ChatRequest,
    user_id: str = Path(...),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Send a chat message and get an AI response.

    The agent interprets the message, invokes MCP tools as needed,
    and returns a friendly confirmation or result.
    """
    result = await process_chat_message(
        session=session,
        user_id=user.id,
        message=body.message,
        conversation_id=body.conversation_id,
    )

    return ChatResponse(
        data=ChatResponseData(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=[ToolCallSchema(**tc) for tc in result.get("tool_calls", [])],
        )
    )
