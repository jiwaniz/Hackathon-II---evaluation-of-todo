# Multi-stage Dockerfile for Todo App with AI Chatbot
# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build Next.js app
RUN npm run build

# Stage 2: Python Backend + Serve Frontend
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy backend files
COPY backend/ ./backend/
WORKDIR /app/backend

# Install Python dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Copy built frontend from previous stage
COPY --from=frontend-builder /frontend/.next /app/frontend/.next
COPY --from=frontend-builder /frontend/public /app/frontend/public
COPY --from=frontend-builder /frontend/package.json /app/frontend/
COPY --from=frontend-builder /frontend/node_modules /app/frontend/node_modules

# Expose ports
EXPOSE 7860

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create startup script that runs both services
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start backend in background\n\
echo "Starting FastAPI backend..."\n\
cd /app/backend\n\
uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
BACKEND_PID=$!\n\
\n\
# Wait a moment for backend to start\n\
sleep 5\n\
\n\
# Start frontend\n\
echo "Starting Next.js frontend..."\n\
cd /app/frontend\n\
PORT=7860 npm run start &\n\
FRONTEND_PID=$!\n\
\n\
# Wait for both processes\n\
wait $BACKEND_PID $FRONTEND_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production
ENV PORT=7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["/app/start.sh"]
