"""Database connection and session management using SQLModel."""

from collections.abc import Generator
from functools import lru_cache

from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import Engine

from config import settings


@lru_cache
def get_engine() -> Engine:
    """Get or create the database engine (lazy, cached).

    The engine is created on first access and cached for subsequent calls.
    This allows the application to import without requiring a database connection.
    """
    return create_engine(
        settings.database_url,
        echo=settings.is_development,  # Log SQL in development
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections after 5 minutes
    )


def create_db_and_tables() -> None:
    """Create all database tables from SQLModel metadata.

    Note: In production, use Alembic migrations instead.
    """
    SQLModel.metadata.create_all(get_engine())


def get_session() -> Generator[Session, None, None]:
    """Dependency that provides a database session.

    Usage:
        @router.get("/items")
        def get_items(session: Session = Depends(get_session)):
            return session.exec(select(Item)).all()
    """
    with Session(get_engine()) as session:
        yield session
