# Backend Dockerfile - Phase IV Local Kubernetes Deployment
# Uses Python 3.13-alpine for security and minimal size
# Implements health checks and structured logging (FR-001, FR-014, FR-015)

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (curl for health checks, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy backend directory
COPY backend/ .

# Install Python dependencies from pyproject.toml requirements
RUN pip install --no-cache-dir \
    fastapi>=0.128.0 \
    uvicorn>=0.40.0 \
    sqlmodel>=0.0.31 \
    alembic>=1.18.1 \
    passlib>=1.7.4 \
    python-jose>=3.5.0 \
    bcrypt>=4.0.0 \
    pydantic-settings>=2.12.0 \
    psycopg2-binary>=2.9.11 \
    email-validator>=2.3.0 \
    groq>=1.0.0 \
    google-genai>=1.61.0 \
    google-adk>=1.18.0 \
    mcp>=1.26.0 \
    supabase>=2.27.2

# Expose port 8000 for FastAPI
EXPOSE 8000

# Health check endpoint (K8s liveness/readiness probes)
# Returns JSON status with timestamp
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command: Start FastAPI with uvicorn
# Bind to 0.0.0.0 to be accessible from K8s pods
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
