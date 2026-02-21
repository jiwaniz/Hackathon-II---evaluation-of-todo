# Backend Dockerfile - Phase IV Local Kubernetes Deployment
# Uses Python 3.13-alpine for security and minimal size
# Implements health checks and structured logging (FR-001, FR-014, FR-015)

FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (curl for health checks, build tools if needed)
RUN apk add --no-cache curl gcc musl-dev

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Health check endpoint (K8s liveness/readiness probes)
# Returns JSON status with timestamp
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command: Start FastAPI with uvicorn
# Bind to 0.0.0.0 to be accessible from K8s pods
# Enable reload for development, can be disabled in production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
