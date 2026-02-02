"""Authentication routes for user registration, login, logout, and session management.

Endpoints:
- POST /api/auth/register - Create a new user account
- POST /api/auth/login - Authenticate and receive JWT token
- POST /api/auth/logout - Invalidate current session
- GET /api/auth/session - Get current session info
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from middleware.auth import get_current_user
from models import User
from schemas.auth import UserCreate, UserLogin
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user account.

    Creates a new user with hashed password and returns a JWT token
    for immediate authentication.

    Args:
        data: User registration data (email, password, optional name)
        session: Database session

    Returns:
        dict: User info and JWT token

    Raises:
        HTTPException: 409 if email already exists
    """
    auth_service = AuthService(session)

    try:
        user, token, expires_at = auth_service.register(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "EMAIL_EXISTS", "message": str(e)},
        )

    return {
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat(),
            },
            "token": token,
            "expires_at": expires_at.isoformat(),
        },
        "message": "Account created successfully",
    }


@router.post("/login")
async def login(data: UserLogin, session: Session = Depends(get_session)):
    """Authenticate a user and receive JWT token.

    Validates credentials and returns a JWT token for subsequent
    authenticated requests.

    Args:
        data: Login credentials (email, password)
        session: Database session

    Returns:
        dict: User info and JWT token

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    auth_service = AuthService(session)
    result = auth_service.login(data)

    if not result:
        # Generic message to not reveal which field is incorrect
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"},
        )

    user, token, expires_at = result

    return {
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat(),
            },
            "token": token,
            "expires_at": expires_at.isoformat(),
        },
        "message": "Login successful",
    }


@router.post("/logout")
async def logout(user: User = Depends(get_current_user)):
    """Log out the current user.

    Since we use stateless JWT tokens, logout is a client-side operation.
    This endpoint verifies the token is valid and confirms logout.

    Args:
        user: The authenticated user (from JWT token)

    Returns:
        dict: Logout confirmation message
    """
    # With stateless JWT, we can't invalidate the token server-side
    # The client should remove the token from storage
    # In production, you might add the token to a blacklist
    return {"message": "Logged out successfully"}


@router.get("/session")
async def get_session_info(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get current session information.

    Returns the current user's information and token expiration.

    Args:
        user: The authenticated user (from JWT token)
        session: Database session

    Returns:
        dict: User info and token expiration
    """
    auth_service = AuthService(session)
    user, expires_at = auth_service.get_session(user)

    return {
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat(),
            },
            "expires_at": expires_at.isoformat(),
        }
    }
