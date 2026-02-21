# Docker Image Contracts

## Backend Service (todo-backend)

### Image Specification

**Image Name**: `todo-backend:latest`
**Base Image**: `python:3.13-alpine`
**Working Directory**: `/app`
**Port**: 8000

### Entry Point

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables (Required at Runtime)

| Variable | Required | Source | Example |
|----------|----------|--------|---------|
| `DATABASE_URL` | Yes | K8s ConfigMap | `postgresql://user:pass@neon.tech/db` |
| `GROQ_API_KEY` | Yes | K8s Secret | `gsk_...` |
| `BETTER_AUTH_SECRET` | Yes | K8s Secret | `hs256-secret-key` |
| `KUBECTL_AI_KEY` | No | K8s Secret | `openai-api-key` |

### Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-21T12:34:56.789Z"
}
```

### Exposed Ports

- **8000/tcp**: FastAPI application server

### Volumes (None Expected)

- No persistent volumes needed
- Logs → stdout (captured by `kubectl logs`)

### Runtime Requirements

- CPU: 200m (request), 500m (limit)
- Memory: 512Mi (request), 1Gi (limit)
- ephemeral storage: <100Mi

### Compliance

- ✅ No hardcoded secrets
- ✅ No privileged escalation required
- ✅ Non-root user recommended (optional for Phase 4)
- ✅ Health check present
- ✅ Graceful shutdown via SIGTERM

---

## Frontend Service (todo-frontend)

### Image Specification

**Image Name**: `todo-frontend:latest`
**Base Image**: `node:20-alpine`
**Working Directory**: `/app`
**Port**: 3000

### Build Stage

```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build
```

### Runtime Entry Point

```dockerfile
CMD ["npm", "start"]
```

### Environment Variables (Required at Runtime)

| Variable | Required | Source | Example |
|----------|----------|--------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | K8s ConfigMap | `http://todo-backend:8000` |
| `BETTER_AUTH_URL` | Yes | K8s ConfigMap | `http://todo-frontend:3000` |

### Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-21T12:34:56.789Z"
}
```

### Exposed Ports

- **3000/tcp**: Next.js application server

### Volumes (None Expected)

- No persistent volumes needed
- Logs → stdout

### Runtime Requirements

- CPU: 100m (request), 300m (limit)
- Memory: 256Mi (request), 512Mi (limit)
- ephemeral storage: <50Mi

### Compliance

- ✅ No hardcoded secrets
- ✅ No privileged escalation required
- ✅ Multi-stage build (no build tools in runtime image)
- ✅ Health check present
- ✅ Graceful shutdown via SIGTERM

---

## Shared Requirements

### Image Pull Policy

```yaml
imagePullPolicy: IfNotPresent
```

### Security

- No secrets in image
- Alpine base: minimal attack surface
- Regular image scanning/updates recommended

### Logging

All application logs to stdout (JSON format for backend, structured for frontend)

### Timezone

Use UTC internally; local timezone conversion in frontend only

### Build Context

Dockerfiles should live in:
- `backend/Dockerfile` (for backend service)
- `frontend/Dockerfile` (for frontend service)

### Build Command

```bash
# Backend
docker build -f backend/Dockerfile -t todo-backend:latest .

# Frontend
docker build -f frontend/Dockerfile -t todo-frontend:latest .
```

### Image Scanning

Before deployment, verify:
- No known vulnerabilities: `docker scan todo-backend:latest`
- Correct entry point: `docker inspect todo-backend:latest`
- Health check responds: `docker run ... todo-backend:latest` + curl

---

## Contract Version

**Version**: 1.0
**Last Updated**: 2026-02-21
**Status**: Approved for implementation
