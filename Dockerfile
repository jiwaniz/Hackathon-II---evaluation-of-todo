# Multi-stage Dockerfile for Todo App with AI Chatbot
# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder

WORKDIR /frontend

# Accept build arguments for Next.js public env vars (with defaults for build)
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ARG NEXT_PUBLIC_SUPABASE_URL=https://placeholder.supabase.co
ARG NEXT_PUBLIC_SUPABASE_ANON_KEY=placeholder
ARG BETTER_AUTH_URL=https://jiwaniz-to-do-evalution.hf.space

# Set them as environment variables for the build
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY
ENV BETTER_AUTH_URL=$BETTER_AUTH_URL
ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=2048"
ENV NEXT_TELEMETRY_DISABLED=1

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm install --include=dev --prefer-offline --no-audit

# Copy frontend source
COPY frontend/ ./

# Debug: List lib directory to verify files are copied
RUN ls -la lib/ && echo "=== lib files verified ==="

# Build Next.js app
RUN npm run build

# Stage 2: Python Backend + Serve Frontend
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
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
COPY --from=frontend-builder /frontend/node_modules /app/frontend/node_modules
COPY --from=frontend-builder /frontend/package.json /app/frontend/package.json

# Expose ports
EXPOSE 7860

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
PORT=7860 npm start &\n\
FRONTEND_PID=$!\n\
\n\
# Wait for both processes\n\
wait $BACKEND_PID $FRONTEND_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production
ENV PORT=7860
ENV BETTER_AUTH_URL=https://jiwaniz-to-do-evalution.hf.space
# RESEND_API_KEY should be set via HF Spaces secrets for email verification
ENV RESEND_API_KEY=${RESEND_API_KEY}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["/app/start.sh"]
