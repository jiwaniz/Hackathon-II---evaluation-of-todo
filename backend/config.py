"""Configuration management for the Evolution of Todo backend."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Neon DB URL — same value already public in frontend/lib/auth.ts
_NEON_DB_URL = (
    "postgresql://neondb_owner:npg_VCELyK9WR3gP"
    "@ep-falling-bar-a199lzbj-pooler.ap-southeast-1.aws.neon.tech"
    "/neondb?sslmode=require"
)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default=_NEON_DB_URL,
        description="PostgreSQL connection string (Neon)",
    )

    # Authentication (Phase 2 - Better Auth)
    better_auth_secret: str = Field(
        default="development-secret-change-in-production",
        description="Shared secret with frontend for JWT signing/verification",
    )

    # Authentication (Phase 3 - Supabase Auth)
    supabase_url: str = Field(
        default="https://nqqrfchwdhjmskwmzfyc.supabase.co",
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
        default="http://localhost:3000,https://jiwaniz-to-do-evalution.hf.space",
        description="Comma-separated list of allowed origins",
    )

    # Environment
    environment: str = Field(
        default="production",
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


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance for easy import
settings = get_settings()
