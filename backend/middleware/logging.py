"""Request/Response logging middleware for the Evolution of Todo backend.

This middleware:
- Logs all incoming requests with method, path, and headers
- Logs all responses with status code and duration
- Generates unique request IDs for tracing
- Redacts sensitive information (tokens, passwords)

Reference: T147 - Add request/response logging middleware
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from logging_config import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs all HTTP requests and responses."""

    # Headers to redact from logs
    SENSITIVE_HEADERS = {"authorization", "cookie", "x-api-key"}

    # Paths to skip logging (health checks, static files)
    SKIP_PATHS = {"/health", "/favicon.ico"}

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and log details."""
        # Skip logging for certain paths
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        # Generate request ID
        request_id = str(uuid.uuid4())[:8]

        # Extract user ID from path if present
        user_id = None
        path_parts = request.url.path.split("/")
        if len(path_parts) >= 3 and path_parts[1] == "api":
            # Path pattern: /api/{user_id}/...
            potential_user_id = path_parts[2]
            if potential_user_id not in ["auth", "health"]:
                user_id = potential_user_id

        # Prepare safe headers (redact sensitive ones)
        safe_headers = {}
        for key, value in request.headers.items():
            if key.lower() in self.SENSITIVE_HEADERS:
                safe_headers[key] = "[REDACTED]"
            else:
                safe_headers[key] = value

        # Log incoming request
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "user_id": user_id,
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent", ""),
            },
        )

        # Process request and measure duration
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            # Log response
            log_method = logger.info if response.status_code < 400 else logger.warning
            log_method(
                f"Request completed: {request.method} {request.url.path} -> {response.status_code}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "user_id": user_id,
                },
            )

            # Add request ID to response headers for tracing
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"Request failed: {request.method} {request.url.path} - {type(e).__name__}: {str(e)}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                    "user_id": user_id,
                },
                exc_info=True,
            )
            raise
