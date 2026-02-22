"""Configuration management for the Evolution of Todo backend."""

import logging
import os
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(
        default="postgresql://localhost/evolution_of_todo",
        description="PostgreSQL connection string (Neon)",
    )

    # Authentication (Phase 2 - Better Auth)
    better_auth_secret: str = Field(
        default="development-secret-change-in-production",
        description="Shared secret with frontend for JWT signing/verification",
    )

    # Authentication (Phase 3 - Supabase Auth)
    supabase_url: str = Field(
        default="",
        description="Supabase project URL",
    )
    supabase_jwt_secret: str = Field(
        default="",
        description="Supabase JWT secret for token verification",
    )

    # AI Providers (Phase 3)
    google_api_key: str = Field(
        default="",
        description="Google AI Studio API key for Gemini",
    )
    groq_api_key: str = Field(
        default="",
        description="Groq API key for LLM fallback",
    )

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed origins",
    )

    # Environment
    environment: str = Field(
        default="development",
        description="Current environment (development, staging, production)",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @field_validator("database_url", mode="after")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format and log configuration."""
        if not v or v == "postgresql://localhost/evolution_of_todo":
            logger.warning("⚠️ Using default DATABASE_URL - set via env var in production")

        if "postgresql://" not in v and "postgres://" not in v:
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")

        # Check for Neon-specific requirements
        if "neon.tech" in v and "sslmode" not in v:
            logger.warning("⚠️ Neon database detected but sslmode not set - adding ?sslmode=require")
            if "?" in v:
                v = v + "&sslmode=require"
            else:
                v = v + "?sslmode=require"

        # Mask the URL for logging
        masked_url = v.split("@")[-1] if "@" in v else "***"
        logger.info(f"Database configured: {masked_url}")

        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance for easy import
settings = get_settings()
