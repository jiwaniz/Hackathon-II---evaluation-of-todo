# Implementation Tasks: Phase IV - Local Kubernetes Deployment

**Feature**: Phase IV - Local Kubernetes Deployment
**Branch**: `004-phase4-k8s-deployment`
**Date**: 2026-02-21
**Status**: Ready for Implementation
**Total Tasks**: 28 tasks organized across 10 phases

---

## Task Execution Strategy

### MVP Scope (Phase 4 Minimum Viable Product)
Complete **Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3)** to achieve full local Kubernetes deployment:
- Backend containerized and running in Docker
- Frontend containerized and running in Docker
- Both services deployed to Minikube via Helm
- **Estimated Time**: 4-6 hours

### Parallel Opportunities
- **US1 + US2 (Phases 3-4)**: Dockerfiles can be created in parallel
- **US4 + US5 + US6 (Phases 6-8)**: Health checks, kubectl-ai, kagent can be integrated in parallel after core deployment
- **US7 (Phase 9)**: Registry integration can be deferred if not needed for initial deployment

### Completion Order (Dependencies)
```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
                              ↓
                            Phase 6, 7, 8 (parallel)
                                    ↓
                                  Phase 9, 10
```

---

## Phase 1: Setup & Minikube Configuration

**Goal**: Configure local development environment for Kubernetes development

**Independent Test Criteria**:
- Minikube cluster starts successfully
- Docker environment configured for Minikube
- Project structure created with all required directories

### Setup Tasks

- [x] T001 Install and verify Minikube (1.25+) and kubectl are available, document in DEPLOYMENT.md
- [x] T001c (Optional - if using Ingress) Start minikube tunnel in background terminal: `minikube tunnel` (required for todo.local access via Ingress)
- [x] T002 Create project directory structure: `helm/`, `helm/templates/`, `helm/contracts/` directories
- [x] T003 Verify Docker Desktop is installed and running, create Dockerfile templates in root for reference
- [x] T004 [P] Document Step 0: `eval $(minikube docker-env)` setup in quickstart.md (FR-016)
- [x] T005 [P] Create .dockerignore files for backend and frontend directories to optimize image builds
- [x] T006 Verify Helm 3+ is installed and create helm/Chart.yaml with chart metadata
- [x] T007 Verify kubectl-ai and kagent are available in PATH for later integration tasks
- [x] T008 [P] Create DEPLOYMENT.md guide with prerequisites and troubleshooting steps

---

## Phase 2: Foundational Infrastructure Setup

**Goal**: Create shared infrastructure components (Dockerfiles, Helm structure, RBAC)

**Independent Test Criteria**:
- Helm chart structure validates without errors
- RBAC manifests are syntactically correct
- All Helm templates can be rendered via `helm template`

### Foundational Tasks

- [x] T009 Create backend/Dockerfile with Python 3.13-alpine base, health check, and structured logging (FR-001, FR-014, FR-015)
- [x] T010 Create frontend/Dockerfile with Node.js 20-alpine, multi-stage build, and health check (FR-002, FR-014, FR-015)
- [x] T011 Create helm/values.yaml with complete configuration schema for backend/frontend replicas, resources, environment variables (FR-018)
- [x] T012 [P] Create helm/templates/rbac.yaml with ServiceAccount and ClusterRole for kubectl-ai/kagent access (FR-017)
- [x] T013 [P] Create helm/db-readiness.sh script for init container database connectivity check using postgres:15-alpine image (includes pg_isready command) (FR-019)
- [x] T014 Create helm/templates/_helpers.tpl with template helper functions for labels and selectors
- [x] T015 Create helm/Chart.yaml with version, appVersion, and metadata
- [x] T016 [P] Create helm/templates/configmap-backend.yaml with DATABASE_URL and dynamic BETTER_AUTH_URL (FR-018)
- [x] T017 [P] Create helm/templates/configmap-frontend.yaml with NEXT_PUBLIC_API_URL and TRUSTED_ORIGINS (FR-018)
- [x] T017a Update Better Auth provider dashboard: Add Minikube IP (`minikube ip`) and todo.local as valid redirect URIs before deploying to K8s (required for auth callback success in T035)
- [x] T018 Create helm/templates/secret-api-keys.yaml template for Groq, Better Auth, kubectl-ai keys
- [x] T019 Validate Helm chart: `helm lint ./helm` and `helm template todo-chatbot ./helm` must succeed

---

## Phase 3: User Story 1 - Containerize Backend Service (P1)

**Goal**: Package Phase III FastAPI backend into a production-ready Docker image

**Independent Test Criteria**:
- Docker image builds without errors
- Container starts with `docker run` and health endpoint responds
- Container accepts API requests and returns valid JSON responses

### US1 Tasks

- [x] T020 [P] [US1] Build backend Docker image: `docker build -f backend/Dockerfile -t todo-backend:latest .` from project root
- [x] T021 [US1] Verify backend image with: `docker run -p 8000:8000 -e DATABASE_URL=... -e GROQ_API_KEY=... todo-backend:latest`
- [x] T022 [US1] Test health check: curl http://localhost:8000/health returns `{"status":"healthy","timestamp":"..."}`
- [x] T023 [US1] Test API endpoint: POST to http://localhost:8000/api/{user_id}/chat with valid payload returns 200 OK with JSON response
- [x] T024 [US1] Verify structured logs: `docker logs <container-id>` shows JSON formatted logs with timestamp, level, message fields
- [x] T025 [US1] Load image into Minikube: `minikube image load todo-backend:latest` (FR-016)
- [x] T026 [US1] Document backend containerization in DEPLOYMENT.md with build and run commands

---

## Phase 4: User Story 2 - Containerize Frontend Service (P1)

**Goal**: Package Phase III Next.js frontend into a production-ready Docker image

**Independent Test Criteria**:
- Docker image builds without errors
- Container starts with `docker run` and responds to HTTP requests
- Frontend can be accessed in browser and loads chat interface

### US2 Tasks

- [x] T027 [P] [US2] Build frontend Docker image: `docker build -f frontend/Dockerfile -t todo-frontend:latest .` from project root
- [x] T028 [US2] Verify frontend image with: `docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 todo-frontend:latest`
- [x] T029 [US2] Test health check: curl http://localhost:3000/api/health returns 200 OK
- [x] T030 [US2] Browser test: Access http://localhost:3000, verify chat interface loads and welcome message displays
- [x] T031 [US2] Integration test: Send chat message from frontend UI, verify backend processes and response displays
- [x] T032 [US2] Load image into Minikube: `minikube image load todo-frontend:latest` (FR-016)
- [x] T033 [US2] Document frontend containerization in DEPLOYMENT.md with build and run commands

---

## Phase 5: User Story 3 - Deploy to Minikube with Helm (P1)

**Goal**: Deploy both containerized services to Minikube cluster using Helm charts with RBAC, init containers, and dynamic configuration

**Independent Test Criteria**:
- Helm install completes without errors
- All pods reach Running/Ready status
- Frontend and backend communicate successfully
- Services are accessible via port-forward

### US3 Tasks

- [x] T034 Create helm/templates/backend-deployment.yaml with:
  - Replicas from values.yaml
  - Resource requests/limits per FR-014
  - Init container using postgres:15-alpine image for DB readiness check via pg_isready command per FR-019
  - Health check livenessProbe and readinessProbe
  - Environment variables from ConfigMaps and Secrets
  - ServiceAccount from RBAC for AI agents (FR-017)

- [x] T035 [P] Create helm/templates/frontend-deployment.yaml with:
  - Replicas from values.yaml
  - Resource requests/limits per FR-014
  - Health check livenessProbe and readinessProbe
  - Dynamic BETTER_AUTH_URL environment variable (FR-018) set to Minikube IP or todo.local depending on Ingress mode
  - TRUSTED_ORIGINS from ConfigMap (FR-018)
- [x] T035a Configure NEXT_PUBLIC_BETTER_AUTH_URL at deployment: `helm install todo-chatbot ./helm --set frontend.environment.BETTER_AUTH_URL=http://<minikube-ip>:3000` or `http://todo.local:3000` if using Ingress (FR-018)

- [x] T036 [P] Create helm/templates/backend-service.yaml (ClusterIP, port 8000, selector app: todo-backend)

- [x] T037 [P] Create helm/templates/frontend-service.yaml (ClusterIP, port 3000, selector app: todo-frontend)

- [x] T038 [P] Create helm/templates/ingress.yaml for optional todo.local access (ingress.enabled: false by default)

- [x] T039 [US3] Create Kubernetes secrets: `kubectl create secret generic todo-secrets --from-literal=DATABASE_URL=... --from-literal=GROQ_API_KEY=... --from-literal=BETTER_AUTH_SECRET=... --from-literal=KUBECTL_AI_KEY=...` (must include KUBECTL_AI_KEY for AI agent authentication in FR-017 and BETTER_AUTH_SECRET for JWT verification)

- [x] T040 [US3] Deploy Helm chart: `helm install todo-chatbot ./helm --set frontend.environment.BETTER_AUTH_URL=...` with all required environment variables

- [x] T041 [US3] Verify deployment: `helm status todo-chatbot` returns "STATUS: deployed"

- [x] T042 [US3] Verify pods: `kubectl get pods` shows backend and frontend pods in Running/Ready status

- [x] T043 [US3] Port-forward test backend: `kubectl port-forward svc/todo-backend 8000:8000`, curl health endpoint returns 200 OK

- [x] T044 [US3] Port-forward test frontend: `kubectl port-forward svc/todo-frontend 3000:3000`, access http://localhost:3000 in browser

- [x] T045 [US3] End-to-end test: Send chat message from frontend UI, verify backend processes and response displays correctly

- [x] T046 [US3] Verify init container: Check backend pod description shows init container completed successfully (pg_isready passed)

- [x] T047 [US3] Document Minikube deployment in DEPLOYMENT.md with step-by-step instructions and troubleshooting

---

## Phase 6: User Story 4 - Health Checks and Observability (P2)

**Goal**: Set up comprehensive health monitoring and structured logging for both services

**Independent Test Criteria**:
- Health check endpoints return 200 OK from running pods
- Logs are in JSON format with required fields
- Kubernetes events and pod descriptions show clear status information

### US4 Tasks

- [x] T048 [P] [US4] Implement backend health endpoint: `GET /health` in FastAPI returns `{"status":"healthy","timestamp":"...","version":"1.0"}`

- [x] T049 [P] [US4] Implement frontend health endpoint: `GET /api/health` in Next.js returns `{"status":"healthy","timestamp":"..."}`

- [x] T050 [US4] Configure backend structured logging: Use structlog or similar to emit JSON logs with fields: timestamp, level, message, user_id, request_id, response_time_ms, endpoint

- [x] T051 [US4] Configure frontend structured logging: Emit JSON logs to console with timestamp, level, message, component

- [x] T052 [US4] Add Kubernetes liveness probe to backend deployment: `httpGet /health port 8000 initialDelaySeconds: 10 periodSeconds: 30`

- [x] T053 [US4] Add Kubernetes readiness probe to backend deployment: `httpGet /health port 8000 initialDelaySeconds: 5 periodSeconds: 10`

- [x] T054 [P] [US4] Add Kubernetes liveness probe to frontend deployment: `httpGet /api/health port 3000 initialDelaySeconds: 15 periodSeconds: 30`

- [x] T055 [P] [US4] Add Kubernetes readiness probe to frontend deployment: `httpGet /api/health port 3000 initialDelaySeconds: 5 periodSeconds: 10`

- [x] T056 [US4] Test probes: Deploy updated chart, wait for pods to be Ready, verify `kubectl describe pod <pod-name>` shows probe success events

- [x] T057 [US4] Log verification: `kubectl logs <backend-pod>` shows JSON formatted logs, parse with `jq` to extract fields

- [x] T058 [US4] Documentation: Update DEPLOYMENT.md with health check endpoints and log format specification

---

## Phase 7: User Story 5 - kubectl-ai Integration (P2)

**Goal**: Enable intelligent Kubernetes operations via kubectl-ai agent

**Independent Test Criteria**:
- kubectl-ai is installed and KUBECTL_AI_KEY is configured
- kubectl-ai commands successfully generate and execute kubectl operations
- Scaling and diagnostics work via natural language

### US5 Tasks

- [x] T059 [P] [US5] Verify kubectl-ai installation: `kubectl-ai --version` and verify API key is set (KUBECTL_AI_KEY in Kubernetes Secrets)

- [x] T060 [US5] Configure ServiceAccount for kubectl-ai: Verify RBAC permissions allow get, list, patch, describe on pods/deployments (created in T012)

- [x] T061 [US5] Test kubectl-ai scaling: Run `kubectl-ai "scale backend to 3 replicas"`, verify command executes correctly

- [x] T062 [US5] Test kubectl-ai diagnostics: Run `kubectl-ai "why is the backend pod failing?"`, verify natural language response

- [x] T063 [US5] Test kubectl-ai deployment: Run `kubectl-ai "deploy frontend with 2 replicas"`, verify pods are created

- [x] T064 [P] [US5] Document kubectl-ai setup in KUBECTL_AI_SETUP.md with installation, configuration, and example commands

- [x] T065 [US5] Verify logs: Check that kubectl-ai operations appear in `kubectl logs -l app=todo-backend` as structured events

---

## Phase 8: User Story 6 - kagent Integration (P2)

**Goal**: Enable cluster health analysis and optimization recommendations via kagent

**Independent Test Criteria**:
- kagent is installed and can access cluster
- kagent provides meaningful health reports and optimization suggestions
- Recommendations align with resource allocation (FR-014)

### US6 Tasks

- [x] T066 [P] [US6] Verify kagent installation: `kagent --version`

- [x] T067 [US6] Test kagent cluster analysis: Run `kagent "analyze the cluster health"`, verify report includes pod status, resource usage, warnings

- [x] T068 [US6] Test kagent optimization: Run `kagent "optimize resource allocation"`, verify recommendations for CPU/memory adjustments

- [x] T069 [US6] Verify resource recommendations: Compare kagent suggestions with current limits (200m CPU backend, 100m CPU frontend, etc.)

- [x] T070 [P] [US6] Document kagent setup in KUBECTL_AI_SETUP.md with analysis and optimization examples

- [x] T071 [US6] Create baseline metrics: Document initial cluster resource usage before and after kagent recommendations

---

## Phase 9: User Story 7 - Container Registry Integration (P3)

**Goal**: Enable Docker image push/pull from registry for distributed deployments

**Independent Test Criteria**:
- Images can be tagged with registry URL
- Images can be pushed to registry
- Helm charts can pull images from registry

### US7 Tasks

- [x] T072 [P] [US7] Create local Docker registry in Minikube: `docker run -d --name=registry -p 5000:5000 registry:latest`

- [x] T073 [US7] Tag backend image: `docker tag todo-backend:latest localhost:5000/todo-backend:v1.0`

- [x] T074 [US7] Tag frontend image: `docker tag todo-frontend:latest localhost:5000/todo-frontend:v1.0`

- [x] T075 [P] [US7] Push backend image: `docker push localhost:5000/todo-backend:v1.0`, verify in registry

- [x] T076 [P] [US7] Push frontend image: `docker push localhost:5000/todo-frontend:v1.0`, verify in registry

- [x] T077 [US7] Update Helm values: Set `backend.image: localhost:5000/todo-backend:v1.0` and `frontend.image: localhost:5000/todo-frontend:v1.0`

- [x] T078 [US7] Deploy from registry: `helm install todo-chatbot ./helm --values values-registry.yaml`, verify pods pull from registry

- [x] T079 [US7] Verify imagePullPolicy: Confirm `imagePullPolicy: IfNotPresent` prevents unnecessary pulls (FR-015)

---

## Phase 10: Polish & Documentation

**Goal**: Complete documentation, verify best practices, create deployment guides

**Independent Test Criteria**:
- All documentation is complete and accurate
- Deployment can be reproduced from quickstart guide
- All best practices are documented and followed

### Polish Tasks

- [x] T080 [P] Update quickstart.md with all 10 steps and troubleshooting section covering:
  - Step 0: Minikube Docker environment (FR-016)
  - Step 1: Start Minikube cluster
  - Step 2-3: Build images
  - Step 4: Create secrets
  - Step 5-6: Install Helm chart
  - Step 7-8: Verify deployment
  - Step 9: Port-forward and test
  - Step 10: Cleanup

- [x] T081 Create TROUBLESHOOTING.md with solutions for:
  - ImagePullBackOff (FR-015 - imagePullPolicy fix)
  - CrashLoopBackOff (FR-019 - init container DB check)
  - Port conflicts (port-forward alternatives)
  - Memory issues (Minikube memory increase)
  - Better Auth URL issues (FR-018 - dynamic parameterization)

- [x] T082 [P] Create KUBECTL_AI_SETUP.md documenting:
  - Installation of kubectl-ai and kagent
  - API key configuration in Kubernetes Secrets
  - RBAC setup (ServiceAccount, ClusterRole, FR-017)
  - Example commands for common operations
  - Troubleshooting for AI agent access

- [x] T083 [P] Create helm/NOTES.txt with post-install instructions:
  - Port-forward commands
  - Verify pods are running
  - Check application health
  - Next steps (scaling, monitoring)

- [x] T084 Verify all Helm templates render correctly: `helm template todo-chatbot ./helm --values values.yaml`

- [x] T085 Create helm/values-production.yaml template for Phase 5 cloud deployment

- [x] T086 [P] Document best practices in DEPLOYMENT.md:
  - Resource limits (FR-014)
  - Health checks (FR-006)
  - Structured logging (FR-007)
  - RBAC for AI agents (FR-017)
  - Dynamic configuration (FR-018)
  - Init container for DB (FR-019)

- [x] T087 [P] Create GitHub Actions workflow (.github/workflows/docker-build.yml) for automated image builds and linting

- [x] T088 Final verification: Run through entire quickstart.md from Step 0-10, document any issues

---

## Task Execution Summary

### By User Story
- **US1 (Container Backend)**: T020-T026 (7 tasks)
- **US2 (Container Frontend)**: T027-T033 (7 tasks)
- **US3 (Deploy to Minikube)**: T034-T047 (14 tasks)
- **US4 (Health Checks)**: T048-T058 (11 tasks)
- **US5 (kubectl-ai)**: T059-T065 (7 tasks)
- **US6 (kagent)**: T066-T071 (6 tasks)
- **US7 (Registry)**: T072-T079 (8 tasks)

### By Phase
- **Phase 1 (Setup)**: T001-T008 (8 tasks)
- **Phase 2 (Foundational)**: T009-T019 (11 tasks)
- **Phase 3 (US1)**: T020-T026 (7 tasks)
- **Phase 4 (US2)**: T027-T033 (7 tasks)
- **Phase 5 (US3)**: T034-T047 (14 tasks)
- **Phase 6 (US4)**: T048-T058 (11 tasks)
- **Phase 7 (US5)**: T059-T065 (7 tasks)
- **Phase 8 (US6)**: T066-T071 (6 tasks)
- **Phase 9 (US7)**: T072-T079 (8 tasks)
- **Phase 10 (Polish)**: T080-T088 (9 tasks)

**Total: 88 tasks**

---

## Parallel Execution Example (MVP)

### Critical Path (Sequential, ~4-6 hours)
```
T001-T008 (Setup) → T009-T019 (Foundational) → T020-T026 (US1) → T027-T033 (US2) → T034-T047 (US3)
```

### Parallelizable Builds (Can run simultaneously)
```
Phase 3 (T020-T026) ← Can build backend in parallel
Phase 4 (T027-T033) ← Can build frontend simultaneously
Phase 6 (T048-T058) ← Health checks can be implemented in parallel while Phase 5 deploys
Phase 7 (T059-T065) ← kubectl-ai integration after deployment
Phase 8 (T066-T071) ← kagent integration after deployment
Phase 9 (T072-T079) ← Registry setup optional for initial MVP
Phase 10 (T080-T088) ← Documentation during/after other phases
```

---

## Acceptance Criteria Mapping

| Requirement | Task(s) | Status |
|---|---|---|
| FR-001 | T020 | Backend containerized |
| FR-002 | T027 | Frontend containerized |
| FR-006 | T021-T022, T048-T052 | Health checks ✅ |
| FR-007 | T050-T051 | Structured logging ✅ |
| FR-014 | T009-T010, T034-T035 | Resource limits ✅ |
| FR-015 | T009-T010 | imagePullPolicy IfNotPresent ✅ |
| FR-016 | T004, T020, T032 | Minikube Docker env ✅ |
| FR-017 | T012, T060 | RBAC for AI agents ✅ |
| FR-018 | T016-T017, T035 | Dynamic Better Auth URL ✅ |
| FR-019 | T013, T034 | Init container for DB ✅ |

---

**Status**: ✅ Ready for Implementation
**Next Step**: Execute tasks in order, starting with Phase 1 (Setup)
