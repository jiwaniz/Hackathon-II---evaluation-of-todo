# Implementation Plan: Phase IV - Local Kubernetes Deployment

**Branch**: `004-phase4-k8s-deployment` | **Date**: 2026-02-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-phase4-k8s-deployment/spec.md`

**Note**: This plan
translates the Phase 4 specification into technical architecture and implementation roadmap.

## Summary

**Objective**: Deploy the Phase III Todo AI Chatbot to a local Kubernetes cluster using Minikube, Helm Charts, and AI-assisted DevOps tools.

**Approach**:
1. Containerize existing FastAPI backend and Next.js frontend applications using Docker
2. Create Helm charts for declarative Kubernetes resource management
3. Deploy to local Minikube cluster with health checks and observability
4. Integrate kubectl-ai and kagent for AI-assisted cluster operations
5. Establish best practices for K8s deployments (resource limits, image pull policies, ingress access patterns)

## Technical Context

**Languages/Versions**:
- Backend: Python 3.13+ (FastAPI, existing from Phase III)
- Frontend: TypeScript + Next.js 16+ (existing from Phase III)
- Infrastructure: Docker, Helm 3+, Kubernetes (Minikube)

**Primary Dependencies**:
- **Backend**: FastAPI, SQLModel, Groq SDK, python-jose, uvicorn
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS, Better Auth
- **DevOps**: Docker, Helm, kubectl, kubectl-ai, kagent, Minikube

**Storage**:
- Neon PostgreSQL (external, Phase III)
- No local persistence needed (logs → stdout, no stateful storage)

**Testing**:
- Backend: pytest (existing from Phase III)
- Frontend: Jest/testing-library (existing from Phase III)
- Infrastructure: Helm test charts, kubectl dry-run validation, e2e tests via docker-compose and minikube

**Target Platform**: Linux (Minikube on local development machine)

**Project Type**: Web application (frontend + backend + Kubernetes orchestration)

**Performance Goals**:
- Deployment: <2 minutes from `helm install` to Running/Ready state
- API Response: <5 seconds for chat messages (same as Phase III)
- Health checks: 99% uptime
- Resource efficiency: Backend <500MB, Frontend <300MB at rest

**Constraints**:
- Minikube local cluster (limited resources: ~4-8 GB RAM, 2-4 CPU cores)
- No cloud registry dependency (use local Docker daemon)
- imagePullPolicy: IfNotPresent (avoid remote image pulls)
- Resource limits enforced (prevent pod eviction)

**Scale/Scope**:
- 1-3 users (local demo)
- ~50 Helm templates
- ~10 K8s manifests (Deployments, Services, ConfigMaps, Secrets)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase Isolation ✅ PASS
- Phase 4 runs independently on local Minikube
- No runtime dependencies on Phase 2 or Phase 3
- Uses external Neon PostgreSQL (no local DB cluster)
- Justification: Minikube can start fresh; only needs Docker daemon and existing images

### Spec-Driven Development ✅ PASS
- Specification complete (spec.md with 7 user stories, 15 FR, 12 SC)
- Implementation planning underway (this plan.md)
- Tasks phase will follow (sp.tasks)
- Code generation only after task approval

### Test-First (Non-Negotiable) ✅ PASS
- TDD pattern applies to Helm charts (test values, dry-run validation)
- Dockerfile linting and image scanning
- kubectl manifest validation
- E2E tests: docker-compose locally, then minikube deployment

### Clean Architecture ✅ PASS
- Backend code (Phase III) maintains separation of concerns
- Frontend code (Phase III) maintains component/page separation
- Infrastructure code (Helm, Dockerfiles) follows standard K8s patterns
- No mixing of concerns (infra config in K8s manifests, app logic in containers)

### API-First Design ✅ PASS
- Helm chart interfaces defined (values.yaml with all configurable parameters)
- Docker image contracts defined (exposed ports, environment variables)
- K8s service contracts defined (service names, port mappings)
- Health check endpoints defined (Phase III requirement)

### Observability ✅ PASS
- Structured JSON logging from backend (Phase III requirement)
- Health check endpoints (`/health`) for liveness/readiness probes
- Kubernetes events captured via kubectl describe
- Metrics available via kubectl top
- Helm status monitoring

### Agentic Dev Stack ✅ PASS
- kubectl-ai integration (FR-010) for intelligent K8s operations
- kagent integration (FR-011) for cluster analysis
- No manual kubectl commands required (SC-012)
- MCP tools available to backend (Phase III chatbot can invoke operations)

## Project Structure

### Documentation (this feature)

```text
specs/004-phase4-k8s-deployment/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file - technical architecture
├── research.md          # Phase 0 output (TO BE CREATED)
├── data-model.md        # Phase 1 output (TO BE CREATED)
├── quickstart.md        # Phase 1 output (TO BE CREATED)
├── contracts/           # Phase 1 output (TO BE CREATED)
│   ├── helm-values-schema.json
│   ├── dockerfile-contract.md
│   └── kubernetes-manifests.md
├── checklists/
│   └── requirements.md   # Quality checklist (complete)
└── tasks.md             # Phase 2 output (sp.tasks command)
```

### Source Code (repository root)

**Structure Decision**: Web application with infrastructure-as-code (Helm)

```text
# Existing application code (Phase III)
backend/
├── main.py              # FastAPI app (Phase III)
├── Dockerfile           # NEW: Backend container image
├── .dockerignore         # NEW: Docker build optimization
├── models/              # Database models (existing)
├── routes/              # API endpoints (existing)
└── services/            # Business logic (existing)

frontend/
├── app/                 # Next.js app (Phase III)
├── Dockerfile           # NEW: Frontend container image
├── .dockerignore         # NEW: Docker build optimization
└── next.config.js       # Next.js config (existing)

# Infrastructure code (NEW for Phase 4)
helm/
├── Chart.yaml           # Helm chart metadata
├── values.yaml          # Default chart values (dev, staging, prod variants)
└── templates/
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── configmap-backend.yaml
    ├── configmap-frontend.yaml
    ├── secret-api-keys.yaml
    ├── ingress.yaml         # Optional: for todo.local access
    ├── _helpers.tpl         # Helm template helpers
    └── NOTES.txt            # Post-install instructions

docker-compose.yml      # NEW: Local multi-container testing (before Minikube)

docs/
├── DEPLOYMENT.md        # NEW: Step-by-step Minikube deployment guide
├── TROUBLESHOOTING.md   # NEW: Common issues and solutions
└── KUBECTL_AI_SETUP.md  # NEW: kubectl-ai and kagent configuration guide

.github/workflows/
├── docker-build.yml     # CI: Build and validate Docker images
└── helm-lint.yml        # CI: Validate Helm charts
```

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────┐
│           MINIKUBE KUBERNETES CLUSTER                   │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  Frontend Pod    │         │   Backend Pod    │     │
│  │  (Next.js)       │         │   (FastAPI)      │     │
│  │  - Replicas: 2   │         │   - Replicas: 2  │     │
│  │  - Port: 3000    │         │   - Port: 8000   │     │
│  │  - Limits:       │         │   - Limits:      │     │
│  │    100m/256Mi    │         │     200m/512Mi   │     │
│  └──────────────────┘         └──────────────────┘     │
│           ↓                            ↓                 │
│  ┌──────────────────────────────────────────┐           │
│  │   Kubernetes Services (Internal)         │           │
│  │   - todo-frontend (ClusterIP)            │           │
│  │   - todo-backend (ClusterIP)             │           │
│  │   - Health check endpoints (/health)     │           │
│  └──────────────────────────────────────────┘           │
│           ↓                                              │
│  ┌──────────────────────────────────────────┐           │
│  │   Ingress (Optional: todo.local)         │           │
│  │   - Routes traffic to frontend service   │           │
│  │   - Requires: minikube tunnel             │           │
│  └──────────────────────────────────────────┘           │
│                                                          │
│  ┌──────────────────────────────────────────┐           │
│  │   ConfigMaps & Secrets                   │           │
│  │   - DB_URL (configmap)                   │           │
│  │   - GROQ_API_KEY (secret)                │           │
│  │   - BETTER_AUTH_SECRET (secret)          │           │
│  │   - KUBECTL_AI_KEY (secret)              │           │
│  └──────────────────────────────────────────┘           │
│                                                          │
└─────────────────────────────────────────────────────────┘
           ↓
    ┌───────────────┐
    │  Neon DB      │ (External, Phase III)
    │  PostgreSQL   │
    └───────────────┘
```

### Component Design

#### Dockerfile (Backend)

```dockerfile
FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Decisions**:
- Alpine base: Minimal size (~150MB), secure
- Health check: Kubernetes liveness probe
- No secrets in image: Injected at runtime

#### Dockerfile (Frontend)

```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json .
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
CMD ["npm", "start"]
```

**Key Decisions**:
- Multi-stage build: Reduces final image size (~100MB)
- Alpine base: Security and efficiency
- Environment variables injected via K8s

#### Helm Chart Structure

**Chart.yaml**: Metadata
```yaml
apiVersion: v2
name: todo-chatbot
version: 1.0.0
appVersion: "1.0.0"
```

**values.yaml**: Configuration with defaults
```yaml
backend:
  image: todo-backend:latest
  imagePullPolicy: IfNotPresent
  replicas: 2
  resources:
    requests: { cpu: 200m, memory: 512Mi }
    limits: { cpu: 500m, memory: 1Gi }
  environment:
    DATABASE_URL: $NEON_DATABASE_URL
    GROQ_API_KEY: $GROQ_API_KEY
    # other env vars

frontend:
  image: todo-frontend:latest
  imagePullPolicy: IfNotPresent
  replicas: 2
  resources:
    requests: { cpu: 100m, memory: 256Mi }
    limits: { cpu: 300m, memory: 512Mi }
  environment:
    NEXT_PUBLIC_API_URL: http://todo-backend:8000

ingress:
  enabled: false  # Optional: set to true for todo.local access
  hostname: todo.local
```

#### Kubernetes Manifests (via Helm)

1. **Deployments**: Backend and frontend with replicas, resource limits, health checks
2. **Services**: ClusterIP services for internal communication
3. **ConfigMaps**: Non-sensitive config (DB_URL)
4. **Secrets**: API keys (GROQ_API_KEY, BETTER_AUTH_SECRET, KUBECTL_AI_KEY)
5. **Ingress** (optional): Route external traffic to frontend

## Phase 0: Research & Clarification

**No NEEDS CLARIFICATION items in specification**

All technical decisions are resolved:
- ✅ Containerization: Docker (Alpine base for security)
- ✅ Orchestration: Kubernetes (Minikube for local)
- ✅ Package Manager: Helm 3
- ✅ Resource Limits: Defined in FR-014
- ✅ Image Pull Policy: IfNotPresent (FR-015)
- ✅ AI Integration: kubectl-ai + kagent (FR-010, FR-011)

**Output**: research.md (empty or minimal - no unknowns)

## Phase 1: Design & Contracts

**Deliverables**:
1. **data-model.md**: K8s resource model (not application data)
2. **contracts/helm-values-schema.md**: Helm configuration schema
3. **contracts/dockerfile-contract.md**: Container image specifications
4. **contracts/kubernetes-manifests.md**: K8s resource definitions (OpenAPI-like)
5. **quickstart.md**: Getting started guide (Minikube setup, Helm install, verification)

## Phase 2: Implementation Planning

**Output**: tasks.md (generated by `/sp.tasks`)

Expected task breakdown:
- T-001: Create Dockerfile for backend
- T-002: Create Dockerfile for frontend
- T-003: Create Helm chart structure
- T-004: Define K8s manifests (Deployments, Services)
- T-005: Configure ConfigMaps and Secrets
- T-006: Set up health checks
- T-007: Configure Ingress (optional)
- T-008: Create deployment documentation
- T-009: Integration tests (docker-compose)
- T-010: Minikube end-to-end tests

## Complexity Tracking

> **No violations detected. All Constitution gates PASS.**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
