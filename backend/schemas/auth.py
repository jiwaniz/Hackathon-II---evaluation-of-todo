"""Pydantic schemas for authentication request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    name: Optional[str] = Field(None, max_length=255, description="User display name (optional)")

    model_config = {"json_schema_extra": {"example": {"email": "user@example.com", "password": "securepassword123", "name": "John Doe"}}}


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    model_config = {"json_schema_extra": {"example": {"email": "user@example.com", "password": "securepassword123"}}}


class UserResponse(BaseModel):
    """Schema for user API response (excludes sensitive data)."""

    id: str
    email: str
    name: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Schema for authentication response (login/register)."""

    user: UserResponse
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration timestamp")

    model_config = {"json_schema_extra": {"example": {"user": {"id": "user-123", "email": "user@example.com", "name": "John Doe", "created_at": "2026-01-19T12:00:00Z"}, "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "expires_at": "2026-01-26T12:00:00Z"}}}


class SessionResponse(BaseModel):
    """Schema for session check response."""

    user: UserResponse
    expires_at: datetime
