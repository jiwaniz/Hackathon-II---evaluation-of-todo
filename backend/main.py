"""FastAPI application entry point for Evolution of Todo backend."""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from database import create_db_and_tables
from logging_config import get_logger, setup_logging
from middleware.logging import RequestLoggingMiddleware
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from routes.conversations import router as conversations_router
from routes.tasks import router as tasks_router
from routes.tags import router as tags_router

# Ensure all models are registered in SQLModel metadata before create_all
import models.user  # noqa: F401
import models.task  # noqa: F401
import models.tag  # noqa: F401
import models.conversation  # noqa: F401
import models.message  # noqa: F401

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events for startup and shutdown."""
    # Startup: ensure all DB tables exist (safe to run on every start)
    logger.info(f"Starting Evolution of Todo API in {settings.environment} mode")
    logger.info(f"SUPABASE_JWT_SECRET configured: {bool(settings.supabase_jwt_secret)}")
    logger.info(f"SUPABASE_URL configured: {bool(settings.supabase_url)}")
    try:
        create_db_and_tables()
        logger.info("Database tables verified/created")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    yield
    # Shutdown
    logger.info("Shutting down Evolution of Todo API")


app = FastAPI(
    title="Evolution of Todo API",
    description="Phase II Full-Stack Web Application API with JWT authentication",
    version="2.0.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request/response logging middleware (T147)
app.add_middleware(RequestLoggingMiddleware)


# Health check endpoint (T024)
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring and deployment verification.

    Returns:
        dict: Health status with timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "auth": {
            "supabase_jwt_configured": bool(settings.supabase_jwt_secret),
            "supabase_url_configured": bool(settings.supabase_url),
        },
    }


@app.get("/api/debug/llm-status", tags=["debug"])
async def llm_status():
    """Check which LLM providers are configured."""
    return {
        "google_api_key": "SET" if settings.google_api_key else "EMPTY",
        "groq_api_key": "SET" if settings.groq_api_key else "EMPTY",
        "supabase_url": "SET" if settings.supabase_url else "EMPTY",
        "supabase_jwt_secret": "SET" if settings.supabase_jwt_secret else "EMPTY",
    }


@app.get("/api/debug/llm-test", tags=["debug"])
async def llm_test():
    """Quick test of LLM connectivity (no auth required)."""
    results = {}

    # Test Gemini
    if settings.google_api_key:
        try:
            from google import genai
            client = genai.Client(api_key=settings.google_api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Say hello in one word.",
            )
            results["gemini"] = {"status": "ok", "response": response.text[:100]}
        except Exception as e:
            results["gemini"] = {"status": "error", "error": str(e)[:300]}
    else:
        results["gemini"] = {"status": "no_key"}

    # Test Groq
    if settings.groq_api_key:
        try:
            from groq import Groq
            client = Groq(api_key=settings.groq_api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "Say hello in one word."}],
                max_tokens=10,
            )
            results["groq"] = {"status": "ok", "response": response.choices[0].message.content[:100]}
        except Exception as e:
            results["groq"] = {"status": "error", "error": str(e)[:300]}
    else:
        results["groq"] = {"status": "no_key"}

    return results


@app.get("/api/debug/groq-tools-test", tags=["debug"])
async def groq_tools_test():
    """Test Groq with the exact tool definitions used by chat."""
    if not settings.groq_api_key:
        return {"status": "no_key"}
    try:
        from groq import Groq
        from services.chat_service import _build_groq_tools, SYSTEM_PROMPT
        client = Groq(api_key=settings.groq_api_key)
        tools = _build_groq_tools()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "show my tasks"},
            ],
            tools=tools,
            tool_choice="auto",
            max_tokens=1024,
        )
        choice = response.choices[0]
        if choice.message.tool_calls:
            return {
                "status": "ok_with_tools",
                "tool_calls": [
                    {"name": tc.function.name, "args": tc.function.arguments}
                    for tc in choice.message.tool_calls
                ],
            }
        return {"status": "ok_text", "response": choice.message.content[:200]}
    except Exception as e:
        return {"status": "error", "error": str(e)[:500], "type": type(e).__name__}


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Evolution of Todo API",
        "version": "2.0.0",
        "docs": "/docs" if settings.is_development else None,
    }


# Global exception handlers (T138)
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database-related errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred. Please try again later.",
            }
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle value validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc),
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully."""
    # Log the error
    logger.error(f"Unexpected error: {type(exc).__name__}: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
            }
        },
    )


# Route registration
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(tasks_router)
app.include_router(tags_router)
