"""Pydantic schemas for chat request/response validation."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    conversation_id: int | None = Field(default=None, description="Existing conversation ID")
    message: str = Field(..., min_length=1, max_length=5000, description="User's message")


class ToolCallSchema(BaseModel):
    """Schema for a single tool invocation."""

    tool: str
    input: dict
    output: dict


class ChatResponseData(BaseModel):
    """Data portion of the chat response."""

    conversation_id: int
    response: str
    tool_calls: list[ToolCallSchema] = []


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""

    data: ChatResponseData
