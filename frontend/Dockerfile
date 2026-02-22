# Frontend Dockerfile - Phase IV Local Kubernetes Deployment
# Uses Node.js 20-alpine with multi-stage build for security and minimal size
# Implements health checks (FR-002, FR-014, FR-015)

# Stage 1: Build Next.js application
FROM node:20-slim AS build

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Build Next.js application
RUN npm run build

# Stage 2: Production runtime
FROM node:20-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy only necessary files from build stage
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json .

# Expose port 3000 for Next.js
EXPOSE 3000

# Health check endpoint for K8s liveness/readiness probes
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Default command: Start Next.js in production mode
CMD ["npm", "start"]
