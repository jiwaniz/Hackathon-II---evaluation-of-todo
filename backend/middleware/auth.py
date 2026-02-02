"""Authentication middleware supporting both Better Auth sessions and Supabase JWT.

Phase 2 uses Better Auth session tokens.
Phase 3 uses Supabase JWT tokens verified via the shared JWT secret.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request
from jose import JWTError, jwt
from sqlmodel import Session, select, text

from config import settings
from database import get_session
from models import User


def extract_token_from_header(authorization: Optional[str]) -> str:
    """Extract the token from the Authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={"code": "MISSING_TOKEN", "message": "Authorization header required"},
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_FORMAT", "message": "Authorization header must start with 'Bearer '"},
        )

    return authorization[7:]


def verify_supabase_jwt(token: str) -> str:
    """Verify a Supabase JWT token and return the user's sub claim.

    Args:
        token: The JWT token from Supabase Auth

    Returns:
        The user ID (sub claim) from the token

    Raises:
        HTTPException: If token is invalid or expired
    """
    if not settings.supabase_jwt_secret:
        raise HTTPException(
            status_code=500,
            detail={"code": "CONFIG_ERROR", "message": "Supabase JWT secret not configured"},
        )

    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail={"code": "INVALID_TOKEN", "message": "Token missing sub claim"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )


def verify_session_token(token: str, db_session: Session) -> str:
    """Verify a Better Auth session token by querying the database (Phase 2)."""
    stmt = text('SELECT "userId", "expiresAt" FROM session WHERE token = :token')
    result = db_session.execute(stmt, {"token": token}).first()

    if not result:
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_SESSION", "message": "Invalid or expired session"},
        )

    user_id, expires_at = result

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail={"code": "SESSION_EXPIRED", "message": "Session has expired"},
        )

    return user_id


def _resolve_user_id(token: str, db_session: Session) -> str:
    """Resolve user ID from token, trying Supabase JWT first, then Better Auth session."""
    if settings.supabase_jwt_secret:
        try:
            return verify_supabase_jwt(token)
        except HTTPException:
            pass

    return verify_session_token(token, db_session)


async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db_session: Session = Depends(get_session),
) -> User:
    """Dependency to get the current authenticated user."""
    token = extract_token_from_header(authorization)
    user_id = _resolve_user_id(token, db_session)

    user = db_session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )

    return user


async def verify_user_access(
    request: Request,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db_session: Session = Depends(get_session),
) -> User:
    """Dependency to verify token AND validate URL {user_id} matches."""
    token = extract_token_from_header(authorization)
    session_user_id = _resolve_user_id(token, db_session)

    url_user_id = request.path_params.get("user_id")
    if url_user_id and url_user_id != session_user_id:
        raise HTTPException(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "Access forbidden - user ID mismatch"},
        )

    user = db_session.get(User, session_user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )

    return user
