"""Tag routes - API endpoints for tag operations.

All tag routes follow the /api/{user_id}/tags pattern where user_id
is validated against the JWT token's sub claim.

Reference: specs/api/rest-endpoints.md
"""

from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel
from sqlmodel import Session

from database import get_session
from middleware.auth import verify_user_access
from models import User
from services.tag_service import list_user_tags

router = APIRouter(prefix="/api/{user_id}/tags", tags=["tags"])


class TagResponse(BaseModel):
    """Schema for tag API response."""
    id: int
    name: str
    created_at: str

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """Schema for tag list response."""
    tags: list[TagResponse]


@router.get("/")
async def get_tags(
    user_id: str = Path(..., description="The user's ID"),
    user: User = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """List all tags for the authenticated user.

    Contract (T100):
    - GET /api/{user_id}/tags returns 200
    - Response contains tags array sorted alphabetically
    - Each tag has id, name, and created_at

    Authorization:
    - Requires valid JWT token
    - Returns 403 if URL user_id doesn't match JWT sub claim
    - Users can only see their own tags
    """
    tags = list_user_tags(session, user_id)

    return {
        "data": {
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "created_at": tag.created_at.isoformat(),
                }
                for tag in tags
            ]
        }
    }
