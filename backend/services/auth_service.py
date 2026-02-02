"""Authentication service for user registration, login, and JWT token management.

Implements:
- Password hashing with passlib bcrypt
- JWT token generation using shared BETTER_AUTH_SECRET
- User registration and authentication
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from config import settings
from models import User
from schemas.auth import AuthResponse, SessionResponse, UserCreate, UserLogin, UserResponse

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 7


class AuthService:
    """Service for handling user authentication operations."""

    def __init__(self, session: Session):
        """Initialize auth service with database session."""
        self.session = session

    def hash_password(self, password: str) -> str:
        """Hash a plain text password using bcrypt."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def create_jwt_token(self, user: User) -> tuple[str, datetime]:
        """Create a JWT token for the given user.

        Returns:
            tuple: (token_string, expiration_datetime)
        """
        expires_at = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
        payload = {
            "sub": user.id,
            "email": user.email,
            "exp": expires_at,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.better_auth_secret, algorithm=JWT_ALGORITHM)
        return token, expires_at

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Find a user by their email address."""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by their ID."""
        return self.session.get(User, user_id)

    def register(self, data: UserCreate) -> tuple[User, str, datetime]:
        """Register a new user.

        Args:
            data: User registration data (email, password, optional name)

        Returns:
            tuple: (user, token, expires_at)

        Raises:
            ValueError: If email is already registered
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")

        # Create new user with hashed password
        user = User(
            id=str(uuid4()),
            email=data.email,
            password_hash=self.hash_password(data.password),
            name=data.name,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        # Generate JWT token
        token, expires_at = self.create_jwt_token(user)

        return user, token, expires_at

    def login(self, data: UserLogin) -> Optional[tuple[User, str, datetime]]:
        """Authenticate a user with email and password.

        Args:
            data: Login credentials (email, password)

        Returns:
            tuple: (user, token, expires_at) if successful, None otherwise
        """
        user = self.get_user_by_email(data.email)
        if not user:
            return None

        if not user.password_hash:
            return None

        if not self.verify_password(data.password, user.password_hash):
            return None

        # Generate JWT token
        token, expires_at = self.create_jwt_token(user)

        return user, token, expires_at

    def get_session(self, user: User) -> tuple[User, datetime]:
        """Get current session info for a user.

        Args:
            user: The authenticated user

        Returns:
            tuple: (user, expires_at) - expires_at based on when token was created
        """
        # Return user and calculate expiration from now (token validation happens in middleware)
        expires_at = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
        return user, expires_at

    @staticmethod
    def user_to_response(user: User) -> UserResponse:
        """Convert a User model to a UserResponse schema."""
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        )

    def build_auth_response(
        self, user: User, token: str, expires_at: datetime
    ) -> dict:
        """Build the authentication response data."""
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
            }
        }

    def build_session_response(self, user: User, expires_at: datetime) -> dict:
        """Build the session response data."""
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
