"""Authentication middleware supporting both Better Auth sessions and Supabase JWT.

Phase 2 uses Better Auth session tokens.
Phase 3 uses Supabase JWT tokens verified via the shared JWT secret.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request
from jose import JWTError, jwt
from sqlmodel import Session, select, text

from config import settings
from database import get_session
from models import User

logger = logging.getLogger(__name__)


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


def verify_supabase_jwt(token: str) -> dict:
    """Verify a Supabase JWT token and return the full payload.

    Args:
        token: The JWT token from Supabase Auth

    Returns:
        The decoded payload dict (contains sub, email, user_metadata, etc.)

    Raises:
        HTTPException: If token is invalid or expired
    """
    if not settings.supabase_jwt_secret:
        raise HTTPException(
            status_code=401,
            detail={"code": "CONFIG_ERROR", "message": "Supabase JWT secret not configured"},
        )

    import base64

    # Try raw secret first, then base64-decoded
    secrets_to_try = [settings.supabase_jwt_secret]
    try:
        decoded_secret = base64.b64decode(settings.supabase_jwt_secret)
        secrets_to_try.append(decoded_secret)
    except Exception:
        pass

    last_error = None
    for i, secret in enumerate(secrets_to_try):
        try:
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
            if not payload.get("sub"):
                raise HTTPException(
                    status_code=401,
                    detail={"code": "INVALID_TOKEN", "message": "Token missing sub claim"},
                )
            if i == 1:
                logger.info("JWT verified with base64-decoded secret")
            return payload
        except JWTError as e:
            last_error = e
            logger.warning(f"JWT verify attempt {i} failed: {type(e).__name__}: {e}")
            continue

    logger.error(f"All JWT verification attempts failed. Last error: {last_error}")
    raise HTTPException(
        status_code=401,
        detail={"code": "INVALID_TOKEN", "message": f"Invalid or expired token: {last_error}"},
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


def _resolve_user_id(token: str, db_session: Session) -> tuple[str, dict]:
    """Resolve user ID from token.

    Phase 3 uses Supabase JWT exclusively. Better Auth session fallback is
    only attempted if SUPABASE_JWT_SECRET is not configured AND the session
    table exists (Phase 2 compatibility).

    Returns:
        Tuple of (user_id, jwt_payload). jwt_payload is empty dict for Better Auth sessions.
    """
    if settings.supabase_jwt_secret:
        # Phase 3: verify Supabase JWT
        payload = verify_supabase_jwt(token)
        return payload["sub"], payload

    # Phase 2 fallback: Better Auth session token
    # Wrapped to avoid 500 if session table doesn't exist
    from sqlalchemy.exc import SQLAlchemyError
    try:
        user_id = verify_session_token(token, db_session)
        return user_id, {}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=401,
            detail={"code": "AUTH_UNAVAILABLE", "message": "Authentication service not configured"},
        )


def _get_or_provision_user(user_id: str, jwt_payload: dict, db_session: Session) -> User:
    """Get user from DB or auto-provision from Supabase JWT payload on first login."""
    user = db_session.get(User, user_id)
    if user:
        return user

    # Auto-provision: create a local user record for this Supabase user
    if not jwt_payload:
        raise HTTPException(
            status_code=401,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )

    email = jwt_payload.get("email", "")
    name = (jwt_payload.get("user_metadata") or {}).get("name", "")
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    user = User(
        id=user_id,
        email=email,
        name=name or None,
        emailVerified=True,
        createdAt=now,
        updatedAt=now,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db_session: Session = Depends(get_session),
) -> User:
    """Dependency to get the current authenticated user."""
    token = extract_token_from_header(authorization)
    user_id, jwt_payload = _resolve_user_id(token, db_session)
    return _get_or_provision_user(user_id, jwt_payload, db_session)


async def verify_user_access(
    request: Request,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db_session: Session = Depends(get_session),
) -> User:
    """Dependency to verify token AND validate URL {user_id} matches."""
    token = extract_token_from_header(authorization)
    session_user_id, jwt_payload = _resolve_user_id(token, db_session)

    url_user_id = request.path_params.get("user_id")
    if url_user_id and url_user_id != session_user_id:
        raise HTTPException(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "Access forbidden - user ID mismatch"},
        )

    return _get_or_provision_user(session_user_id, jwt_payload, db_session)
