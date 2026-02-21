# Helm Chart Configuration Contract

## Overview

The Helm chart exposes configuration through `values.yaml`. All values must be configurable without modifying templates.

## Root-Level Values Structure

```yaml
# Global settings
replicaCount: 2  # Default replicas for both services

# Backend service configuration
backend:
  image: todo-backend:latest
  imagePullPolicy: IfNotPresent
  replicas: 2
  port: 8000
  resources: {}
  environment: {}

# Frontend service configuration
frontend:
  image: todo-frontend:latest
  imagePullPolicy: IfNotPresent
  replicas: 2
  port: 3000
  resources: {}
  environment: {}

# Kubernetes ingress configuration
ingress:
  enabled: false
  hostname: todo.local

# Global secrets (created separately)
secrets:
  createFromValues: true  # Create K8s Secrets from values
```

---

## Backend Configuration

### image

```yaml
backend:
  image: todo-backend:latest
```

**Purpose**: Docker image to deploy
**Type**: string
**Default**: `todo-backend:latest`
**Requirements**: Image must be available in local Docker daemon or registry

### imagePullPolicy

```yaml
backend:
  imagePullPolicy: IfNotPresent
```

**Purpose**: K8s image pull strategy
**Type**: string
**Allowed Values**: `IfNotPresent`, `Always`, `Never`
**Default**: `IfNotPresent` (REQUIRED for Minikube)
**Note**: Must be `IfNotPresent` for local Minikube deployments

### replicas

```yaml
backend:
  replicas: 2
```

**Purpose**: Number of backend pod replicas
**Type**: integer
**Default**: 2
**Constraints**: Minimum 1, recommended 2-3 for local

### port

```yaml
backend:
  port: 8000
```

**Purpose**: Internal container port
**Type**: integer
**Default**: 8000
**Requirements**: Must match Dockerfile EXPOSE

### resources

```yaml
backend:
  resources:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 500m
      memory: 1Gi
```

**Purpose**: K8s resource requests and limits
**Type**: object
**Defaults**:
  - Request: 200m CPU, 512Mi memory
  - Limit: 500m CPU, 1Gi memory
**Constraint**: Limits ≥ Requests (K8s requirement)

### environment

```yaml
backend:
  environment:
    DATABASE_URL: postgresql://user:pass@neon.tech/db
    GROQ_API_KEY: gsk_xxxxx
    BETTER_AUTH_SECRET: secret123
    KUBECTL_AI_KEY: openai-key
```

**Purpose**: Environment variables passed to container
**Type**: object (key-value pairs)
**Requirements**:
  - DATABASE_URL: REQUIRED
  - GROQ_API_KEY: REQUIRED
  - BETTER_AUTH_SECRET: REQUIRED
  - KUBECTL_AI_KEY: Optional (for kubectl-ai integration)

**Note**: Sensitive values should be passed via K8s Secrets, not ConfigMaps

---

## Frontend Configuration

### image

```yaml
frontend:
  image: todo-frontend:latest
```

**Purpose**: Docker image to deploy
**Type**: string
**Default**: `todo-frontend:latest`

### imagePullPolicy

```yaml
frontend:
  imagePullPolicy: IfNotPresent
```

**Purpose**: K8s image pull strategy
**Type**: string
**Default**: `IfNotPresent` (REQUIRED for Minikube)

### replicas

```yaml
frontend:
  replicas: 2
```

**Purpose**: Number of frontend pod replicas
**Type**: integer
**Default**: 2

### port

```yaml
frontend:
  port: 3000
```

**Purpose**: Internal container port
**Type**: integer
**Default**: 3000

### resources

```yaml
frontend:
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 300m
      memory: 512Mi
```

**Purpose**: K8s resource requests and limits
**Type**: object
**Defaults**:
  - Request: 100m CPU, 256Mi memory
  - Limit: 300m CPU, 512Mi memory

### environment

```yaml
frontend:
  environment:
    NEXT_PUBLIC_API_URL: http://todo-backend:8000
    BETTER_AUTH_URL: http://todo-frontend:3000
    TRUSTED_ORIGINS: http://todo-frontend:3000,http://todo.local:3000
```

**Purpose**: Environment variables passed to container
**Type**: object
**Requirements**:
  - NEXT_PUBLIC_API_URL: REQUIRED (points to backend service DNS)
  - BETTER_AUTH_URL: REQUIRED and DYNAMIC (FR-018)
    - If using port-forward: `http://localhost:3000`
    - If using K8s service: `http://todo-frontend:3000`
    - If using ingress: `http://todo.local:3000`
  - TRUSTED_ORIGINS: REQUIRED (FR-018)
    - Comma-separated list of allowed origins for Better Auth
    - Must match all possible frontend URLs

**Note on Parameterization** (FR-018):
The `BETTER_AUTH_URL` should be parameterized at deployment time:
```bash
helm install todo-chatbot ./helm \
  --set frontend.environment.BETTER_AUTH_URL="http://todo-frontend:3000" \
  --set frontend.environment.TRUSTED_ORIGINS="http://todo-frontend:3000,http://todo.local:3000"
```

---

## RBAC & ServiceAccount Configuration

### rbac

```yaml
rbac:
  create: true
  serviceAccountName: todo-chatbot-agent
```

**Purpose**: Enable/disable RBAC resources for AI agents (FR-017)
**Type**: object
**Default**: `create: true` (REQUIRED for kubectl-ai/kagent)

**Permissions Granted**:
- `get`, `list`, `watch`, `describe` on pods, deployments, services
- `patch` on deployments (for scaling operations)
- `get` on secrets (with restrictions - only KUBECTL_AI_KEY)

**Note**: These permissions enable kubectl-ai and kagent to introspect cluster state and perform safe operations.

---

## Init Container Configuration

### backend.initContainer

```yaml
backend:
  initContainer:
    enabled: true
    image: postgres:15-alpine  # or busybox with nc
    database:
      host: neon.tech  # From DATABASE_URL
      port: 5432
      checkCommand: pg_isready  # or: nc -zv
```

**Purpose**: Validate Neon DB connectivity before app start (FR-019)
**Type**: object
**Default**: `enabled: true` (REQUIRED to prevent CrashLoopBackOff)

**Why**: External DB connection can fail on initial cluster startup. Init container ensures DB is reachable before FastAPI attempts to start, preventing pod restart loops.

**Check Methods**:
1. `pg_isready`: PostgreSQL-native check (recommended)
2. `nc -zv` (netcat): Generic TCP connectivity check

---

## Ingress Configuration

### enabled

```yaml
ingress:
  enabled: false
```

**Purpose**: Enable/disable Ingress resource creation
**Type**: boolean
**Default**: false
**Note**: Set to true only if Minikube tunnel is available

### hostname

```yaml
ingress:
  hostname: todo.local
```

**Purpose**: DNS hostname for Ingress
**Type**: string
**Default**: `todo.local`
**Requirements**:
  - Must be added to /etc/hosts when enabled
  - Requires `minikube tunnel` to function
  - Automatically updates BETTER_AUTH_URL when used (FR-018)

---

## Configuration Variants

### Development (Default)

```yaml
# values.yaml (default for Minikube)
backend:
  replicas: 2
  imagePullPolicy: IfNotPresent
frontend:
  replicas: 2
  imagePullPolicy: IfNotPresent
ingress:
  enabled: false
```

### Production (Phase 5)

```yaml
# values-prod.yaml
backend:
  replicas: 3
  imagePullPolicy: Always
  image: registry.example.com/todo-backend:v1.0.0
frontend:
  replicas: 3
  imagePullPolicy: Always
  image: registry.example.com/todo-frontend:v1.0.0
ingress:
  enabled: true
  hostname: todo.example.com
```

---

## Required Values Checklist

### Must Be Provided

- [ ] `backend.environment.DATABASE_URL`
- [ ] `backend.environment.GROQ_API_KEY`
- [ ] `backend.environment.BETTER_AUTH_SECRET`
- [ ] `frontend.environment.NEXT_PUBLIC_API_URL`
- [ ] `frontend.environment.BETTER_AUTH_URL` (dynamic based on access method, FR-018)
- [ ] `frontend.environment.TRUSTED_ORIGINS` (comma-separated list, FR-018)
- [ ] `backend.environment.KUBECTL_AI_KEY` (if using kubectl-ai, FR-017)

### Optional (Defaults Provided)

- [ ] `backend.replicas` (default: 2)
- [ ] `backend.imagePullPolicy` (default: IfNotPresent)
- [ ] `backend.initContainer.enabled` (default: true, FR-019)
- [ ] `frontend.replicas` (default: 2)
- [ ] `frontend.imagePullPolicy` (default: IfNotPresent)
- [ ] `rbac.create` (default: true, FR-017)
- [ ] `rbac.serviceAccountName` (default: todo-chatbot-agent, FR-017)
- [ ] `ingress.enabled` (default: false)

---

## Helm Commands

### Install with values

```bash
helm install todo-chatbot ./helm \
  --set backend.environment.DATABASE_URL=$DB_URL \
  --set backend.environment.GROQ_API_KEY=$GROQ_KEY \
  --set backend.environment.BETTER_AUTH_SECRET=$AUTH_SECRET \
  --set frontend.environment.NEXT_PUBLIC_API_URL=http://todo-backend:8000
```

### Install with values file

```bash
helm install todo-chatbot ./helm -f values-prod.yaml
```

### Upgrade

```bash
helm upgrade todo-chatbot ./helm --values values.yaml
```

### Verify Installation

```bash
helm status todo-chatbot
helm get values todo-chatbot
helm template todo-chatbot ./helm  # Preview rendered manifests
```

---

## Contract Version

**Version**: 1.0
**Last Updated**: 2026-02-21
**Status**: Approved for implementation
