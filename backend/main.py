"""FastAPI application entry point for Evolution of Todo backend."""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from logging_config import get_logger, setup_logging
from middleware.logging import RequestLoggingMiddleware
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from routes.conversations import router as conversations_router
from routes.tasks import router as tasks_router
from routes.tags import router as tags_router

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events for startup and shutdown."""
    # Startup
    logger.info(f"Starting Evolution of Todo API in {settings.environment} mode")
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
    }


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
