# Feature Specification: Phase IV - Local Kubernetes Deployment

**Feature Branch**: `004-phase4-k8s-deployment`
**Created**: 2026-02-21
**Status**: Draft
**Input**: User description: "Local Kubernetes Deployment - Deploy Todo Chatbot to Minikube with Helm, Docker, and AI-assisted DevOps tools (kubectl-ai, kagent)"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Containerize Backend Service (Priority: P1)

As a DevOps engineer, I can package the Phase III FastAPI backend into a Docker image so that it can run consistently in any Kubernetes environment without dependency conflicts.

**Why this priority**: The backend is the critical component serving AI chat logic and task operations. Without containerization, the application cannot run on Kubernetes. This is the foundation for all subsequent deployment work.

**Independent Test**: Can be fully tested by building the Docker image, running it locally with `docker run`, making API calls to the container, and verifying the service responds correctly to chat requests and task operations.

**Acceptance Scenarios**:

1. **Given** I have a FastAPI backend with Groq integration, **When** I build the Docker image using `docker build -f backend/Dockerfile .`, **Then** the image builds successfully with zero errors and is tagged as `todo-backend:latest`.
2. **Given** the Docker image is built, **When** I run `docker run -p 8000:8000 todo-backend:latest`, **Then** the backend service starts and health check endpoint `/health` returns 200 OK.
3. **Given** the backend container is running, **When** I POST a chat message to `http://localhost:8000/api/{user_id}/chat`, **Then** the container responds with a valid assistant response within 5 seconds.
4. **Given** I run the container with `docker logs`, **When** the service receives requests, **Then** structured logs (JSON format) are emitted showing request/response details.

---

### User Story 2 - Containerize Frontend Service (Priority: P1)

As a DevOps engineer, I can package the Phase III Next.js frontend into a Docker image so that it can be deployed alongside the backend in Kubernetes.

**Why this priority**: The frontend is equally critical - users need a deployed UI to access the chatbot. Without containerization, the frontend cannot be orchestrated with the backend in K8s.

**Independent Test**: Can be fully tested by building the Docker image, running it locally with `docker run`, accessing the frontend in a browser, and verifying the chat interface is accessible and can communicate with a running backend service.

**Acceptance Scenarios**:

1. **Given** I have a Next.js frontend with Better Auth configuration, **When** I build the Docker image using `docker build -f frontend/Dockerfile .`, **Then** the image builds successfully and is tagged as `todo-frontend:latest`.
2. **Given** the frontend Docker image is built, **When** I run `docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 todo-frontend:latest`, **Then** the frontend service starts and responds to HTTP requests on port 3000.
3. **Given** the frontend container is running, **When** I access `http://localhost:3000` in a browser, **Then** the chat interface loads and displays the welcome message.
4. **Given** the frontend is running and backend is accessible, **When** I send a chat message from the UI, **Then** the message is transmitted to the backend and a response is displayed in the chat window.

---

### User Story 3 - Deploy to Minikube with Helm (Priority: P1)

As a DevOps engineer, I can deploy the containerized frontend and backend services to a local Minikube cluster using Helm charts so that the entire application runs in a production-like Kubernetes environment locally.

**Why this priority**: Minikube deployment is the core objective of Phase 4. It demonstrates the application works in Kubernetes before attempting cloud deployment (Phase 5). This is the critical milestone for the phase.

**Independent Test**: Can be fully tested by starting Minikube, deploying the Helm chart, verifying all pods are running and healthy, port-forwarding to the services, and performing end-to-end tests (user login, chat interaction, task CRUD operations).

**Acceptance Scenarios**:

1. **Given** Minikube is installed and running (`minikube start`), **When** I run `helm install todo-chatbot ./helm/todo-chatbot`, **Then** Helm deploys all resources (frontend deployment, backend deployment, services, configmaps) successfully with zero errors.
2. **Given** the Helm chart is deployed, **When** I run `kubectl get pods`, **Then** I see frontend pod(s) and backend pod(s) in Running state with ready status 1/1 for at least 30 seconds.
3. **Given** pods are running, **When** I run `kubectl port-forward svc/todo-frontend 3000:3000` and access `http://localhost:3000`, **Then** the frontend UI is accessible and functional.
4. **Given** frontend is running with backend port-forward (`kubectl port-forward svc/todo-backend 8000:8000`), **When** I send a chat message from the frontend UI, **Then** the message is processed by the backend and a response is returned within 5 seconds.
5. **Given** the deployment is complete, **When** I run `helm status todo-chatbot`, **Then** the output shows "STATUS: deployed" and all components are healthy.
6. **Given** Minikube tunnel is running (`minikube tunnel`) and Ingress is configured, **When** I access `http://todo.local:3000` in a browser, **Then** the frontend loads without needing manual port-forward commands.

---

### User Story 4 - Set Up Health Checks and Observability (Priority: P2)

As a DevOps engineer, I can monitor the health and behavior of containerized services through health check endpoints, structured logging, and basic metrics so that operational issues are visible and debuggable.

**Why this priority**: Production readiness requires observability. While not blocking deployment, health checks prevent silent failures and structured logging enables debugging in a containerized environment where console access is limited.

**Independent Test**: Can be tested by deploying to Minikube, accessing health check endpoints via kubectl port-forward, inspecting logs with `kubectl logs`, and verifying structured log format is JSON or similarly parseable.

**Acceptance Scenarios**:

1. **Given** backend pod is running, **When** I curl `http://pod-ip:8000/health`, **Then** it returns HTTP 200 with JSON payload `{"status": "healthy", "timestamp": "..."}`.
2. **Given** frontend pod is running, **When** I curl `http://pod-ip:3000/health`, **Then** it returns HTTP 200 indicating the service is responsive.
3. **Given** a backend pod is running and receiving requests, **When** I run `kubectl logs <backend-pod>`, **Then** I see structured JSON logs with fields: timestamp, level, message, user_id, request_id, response_time_ms.
4. **Given** containers are running, **When** I check Kubernetes events with `kubectl describe pod <pod-name>`, **Then** any restart or failure events are logged with clear timestamps and messages.

---

### User Story 5 - Use kubectl-ai for Intelligent K8s Operations (Priority: P2)

As a DevOps engineer, I can use the kubectl-ai agent to intelligently generate and execute Kubernetes commands, reducing manual complexity and enabling AI-assisted troubleshooting.

**Why this priority**: AI-assisted DevOps is a differentiator for the hackathon. While manual kubectl commands work, kubectl-ai demonstrates agentic infrastructure automation. This aligns with the hackathon's Agentic Dev Stack theme.

**Independent Test**: Can be tested by running kubectl-ai commands like "deploy the frontend with 3 replicas" and "check pod health" and verifying the agent generates correct kubectl commands and applies them successfully.

**Acceptance Scenarios**:

1. **Given** kubectl-ai is installed and configured, **When** I run `kubectl-ai "deploy the frontend with 3 replicas"`, **Then** the agent generates and executes correct Kubernetes commands resulting in 3 frontend pod replicas running.
2. **Given** pods are running, **When** I run `kubectl-ai "why is the backend pod failing?"`, **Then** the agent queries pod status, inspects logs, and provides a human-readable diagnosis.
3. **Given** I want to scale services, **When** I run `kubectl-ai "scale backend to 5 replicas to handle load"`, **Then** the agent generates `kubectl scale deployment todo-backend --replicas=5` and applies it.

---

### User Story 6 - Use kagent for Cluster Health Analysis (Priority: P2)

As a DevOps engineer, I can use the kagent agent to analyze overall cluster health, resource utilization, and recommend optimizations so that I understand the application's resource consumption in Kubernetes.

**Why this priority**: Cluster analysis provides insights into whether the local Minikube deployment is efficient and highlights any resource bottlenecks. This is secondary to basic functionality but valuable for understanding K8s behavior.

**Independent Test**: Can be tested by running kagent commands and verifying they provide meaningful cluster health reports without errors.

**Acceptance Scenarios**:

1. **Given** kagent is installed and Minikube cluster is running, **When** I run `kagent "analyze the cluster health"`, **Then** the agent returns a report showing pod status, resource requests/limits, node capacity, and any warnings.
2. **Given** a deployment is active, **When** I run `kagent "optimize resource allocation"`, **Then** the agent suggests resource tuning recommendations based on current usage.

---

### User Story 7 - Container Build and Registry Integration (Priority: P3)

As a DevOps engineer, I can push Docker images to a container registry (Docker Hub or local registry) so that Kubernetes can pull images for deployment without rebuilding locally.

**Why this priority**: Container registry integration enables true CI/CD and distributed deployments. For Phase 4 local testing, local registry is sufficient. This is lower priority because Minikube can use local Docker daemon images.

**Independent Test**: Can be tested by building images, tagging them, pushing to a registry, and deploying Helm charts that reference registry images.

**Acceptance Scenarios**:

1. **Given** Docker images are built locally, **When** I tag them as `<registry>/todo-backend:v1.0` and `<registry>/todo-frontend:v1.0`, **Then** tags are created correctly.
2. **Given** I have a local Docker registry running in Minikube, **When** I push images to the registry, **Then** they are stored and can be deployed via Helm charts using the registry URL.

### Edge Cases

- What happens if Minikube runs out of memory? System should fail gracefully with clear error messages; user can increase Minikube memory via `minikube config set memory 8192`.
- What happens if a pod crashes during deployment? Kubernetes should restart the pod automatically; health checks should detect the restart and log the event.
- What if the backend or frontend image fails to build? Error output should be clear and reference the specific Dockerfile line and missing dependency.
- What happens if port-forward conflicts with existing services on the host? System should report the port conflict and suggest alternative ports or stopping conflicting services.
- What if the user doesn't have Minikube installed? Deployment should fail with a helpful message indicating Minikube is required and providing installation instructions.
- What happens if Minikube tries to pull Docker images from a remote registry? Kubernetes may fail with "ImagePullBackOff" error. Solution: Helm charts MUST set `imagePullPolicy: IfNotPresent` to use the Minikube local Docker daemon context, avoiding unnecessary image pull attempts.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST containerize the Phase III FastAPI backend into a Docker image that includes all dependencies (Groq SDK, FastAPI, SQLModel, python-jose).
- **FR-002**: System MUST containerize the Phase III Next.js frontend into a Docker image that includes all dependencies (Next.js, React, Tailwind CSS, Better Auth).
- **FR-003**: Both images MUST be deployable to Minikube and run successfully without manual configuration changes.
- **FR-004**: System MUST expose backend API on Kubernetes service `todo-backend` on port 8000 internally, accessible via `kubectl port-forward`.
- **FR-005**: System MUST expose frontend on Kubernetes service `todo-frontend` on port 3000 internally, accessible via `kubectl port-forward`.
- **FR-006**: System MUST provide health check endpoints for both frontend (`/health`) and backend (`/health`) that return HTTP 200 when services are operational.
- **FR-007**: System MUST emit structured logs (JSON format) from backend showing request/response traces, errors, and performance metrics.
- **FR-008**: System MUST use Helm charts to define all Kubernetes resources (Deployments, Services, ConfigMaps, Secrets) in a declarative, version-controlled manner.
- **FR-009**: System MUST allow zero-downtime updates via Helm upgrades (rolling deployments).
- **FR-010**: System MUST support kubectl-ai integration for AI-assisted Kubernetes operations (deploy, scale, troubleshoot commands).
- **FR-011**: System MUST support kagent integration for cluster health analysis and optimization recommendations.
- **FR-012**: System MUST handle environment variable injection (e.g., DATABASE_URL, BETTER_AUTH_SECRET) via Kubernetes ConfigMaps and Secrets.
- **FR-013**: System MUST persist frontend and backend container images in a way that Minikube can access them (local Docker daemon or local registry).
- **FR-014**: System MUST configure resource requests and limits (CPU, Memory) for all pods in Kubernetes deployments to prevent resource starvation (recommended: backend 200m CPU / 512Mi memory request, 500m CPU / 1Gi limit; frontend 100m CPU / 256Mi memory request, 300m CPU / 512Mi limit).
- **FR-015**: System MUST set `imagePullPolicy: IfNotPresent` in Helm values and pod specifications to use Minikube's local Docker daemon for images, preventing unnecessary remote image pull attempts and "ImagePullBackOff" errors.
- **FR-016**: System MUST utilize `eval $(minikube docker-env)` before building Docker images or use `minikube image load` to ensure local images are accessible to the Minikube cluster without a remote registry (mandatory for local development).
- **FR-017**: System MUST provide a Kubernetes ServiceAccount with RBAC (Role-Based Access Control) permissions for AI agents (kubectl-ai, kagent) to perform cluster introspection (get, list, patch resources) when invoked by the chatbot or operators.
- **FR-018**: System MUST parameterize `BETTER_AUTH_URL` and `TRUSTED_ORIGINS` environment variables in Helm values.yaml to dynamically match the actual K8s service address or Ingress hostname, preventing authentication failures when accessing frontend via different URLs (localhost:3000, todo.local, etc.).
- **FR-019**: System MUST include an Init Container in the Backend Deployment that validates external Neon PostgreSQL connectivity using `pg_isready` before the FastAPI application attempts to start, preventing "CrashLoopBackOff" errors during cluster startup.

### Key Entities

- **Docker Image (Backend)**: A containerized FastAPI application with all runtime dependencies, configured to accept environment variables for external services (Neon DB, Groq API).
- **Docker Image (Frontend)**: A containerized Next.js application serving the UI, configured to communicate with backend via NEXT_PUBLIC_API_URL.
- **Kubernetes Deployment (Backend)**: A K8s resource defining the backend pod specification, replica count, resource limits, health checks, and environment variables.
- **Kubernetes Deployment (Frontend)**: A K8s resource defining the frontend pod specification, replica count, resource limits, and environment variables.
- **Kubernetes Service (Backend)**: A K8s service exposing the backend deployment internally to the frontend pods.
- **Kubernetes Service (Frontend)**: A K8s service exposing the frontend deployment for external access via port-forward or ingress.
- **Helm Chart**: A templated collection of Kubernetes manifests (values.yaml, templates/) that can be deployed and upgraded consistently.
- **Health Check Endpoint**: HTTP endpoint returning service status, allowing Kubernetes to detect and recover from failures.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Both frontend and backend Docker images build successfully with zero errors and can be run locally with `docker run` without configuration issues.
- **SC-002**: Both services deploy to Minikube via Helm in under 2 minutes and reach Running/Ready status within 1 minute.
- **SC-003**: End-to-end user journey (login → send chat message → task creation → mark complete) functions identically in Minikube as it does when running locally, with zero data loss or synchronization issues.
- **SC-004**: Health check endpoints return 200 OK status at least 99% of the time under normal operation.
- **SC-005**: Structured logs from backend are parseable and include all critical information (timestamp, level, message, user_id, request_id, response_time) needed for debugging.
- **SC-006**: kubectl-ai and kagent successfully execute at least 80% of common DevOps commands (deploy, scale, restart, analyze) without manual correction.
- **SC-007**: Helm rollback (`helm rollback todo-chatbot`) successfully reverts to previous deployment version without data loss in under 30 seconds.
- **SC-008**: Resource requests and limits are properly configured: backend pod request 200m CPU / 512Mi memory (limit 500m CPU / 1Gi), frontend pod request 100m CPU / 256Mi memory (limit 300m CPU / 512Mi); memory usage under normal load stays within requested limits.
- **SC-009**: Image pull policy is set to IfNotPresent in all Helm templates; no "ImagePullBackOff" errors occur when deploying to Minikube.
- **SC-010**: Ingress or Minikube tunnel configuration allows accessing frontend via `http://todo.local:3000` without manual port-forward commands (optional enhancement to port-forward approach).
- **SC-011**: Documentation clearly explains: Minikube setup, Helm chart structure, environment configuration, resource allocation, and troubleshooting steps for common issues (including imagePullPolicy gotchas).
- **SC-012**: Zero manual kubectl commands required; all deployment and configuration should be achievable through Helm and AI agents (kubectl-ai, kagent).

## Assumptions

- **Minikube is installed**: Users have Minikube 1.25+ installed and can start a cluster with `minikube start`.
- **Docker Desktop is installed**: For building images and local testing before Minikube deployment. Docker daemon context is used for local image builds.
- **Phase III is complete**: The Phase III chatbot (FastAPI backend, Next.js frontend, MCP tools) is fully functional and tested.
- **Database is external**: Neon PostgreSQL is used as the external database; Minikube deployments reference it via DATABASE_URL environment variable (no local Postgres in cluster).
- **API keys are available**: Groq API key, Better Auth secret, kubectl-ai API key, kagent API key, and other sensitive values are available and injected via Kubernetes Secrets (GROQ_API_KEY, BETTER_AUTH_SECRET, KUBECTL_AI_KEY, KAGENT_KEY environment variables).
- **Helm 3+ is available**: Helm package manager is installed for deploying charts.
- **kubectl is installed**: Kubernetes CLI is available for verification and debugging.
- **AI agents are available**: kubectl-ai and kagent are installed and functional in the user's environment with proper API key configuration.
- **Docker images use Alpine base**: Backend and frontend Dockerfiles use Alpine Linux (or similar lightweight) base images for security and minimal size (reducing pod memory footprint).
- **Phase Isolation**: Phase 4 runs independently; no requirement to run Phase 2 or 3 simultaneously (though they could).
- **Local Registry (Optional)**: For Phase 4, images are built on the host and used locally; no Docker Hub push is required (Phase 5 may require cloud registry).
- **Structured logging is stdout-based**: Application logs are emitted to stdout in JSON format; Kubernetes captures them via `kubectl logs` (no persistent log volume required for Phase 4).
