# Phase 0: Research & Technical Decisions

**Date**: 2026-02-21
**Status**: Complete - No clarifications needed

## Overview

The Phase 4 specification contains no "NEEDS CLARIFICATION" items. All technical decisions are resolved through the specification and project context (Phase 1-3 completed work).

## Research Summary

### 1. Containerization Strategy: Docker with Alpine Base

**Decision**: Use Docker with Alpine Linux (3.13-alpine for Python, node:20-alpine for Node.js)

**Rationale**:
- Alpine is minimal (~5MB base), reducing pod memory footprint and startup time
- Industry standard for Kubernetes workloads
- Security: Minimal attack surface vs. full OS
- Cost-effective: Smaller images mean faster pulls and less storage

**Alternatives Considered**:
- Full Python/Node images (python:3.13, node:20): ~800MB each, unnecessary overhead
- Distroless images (google/distroless/python3.11): 100% size reduction but harder to debug in production
- ✅ **Chosen**: Alpine - best balance of size, security, debuggability

**Implementation Notes**:
- Multi-stage build for frontend (build stage + runtime stage)
- Health check in Dockerfile (curl /health endpoint)
- No secrets in image (injected at runtime via K8s)

---

### 2. Orchestration Platform: Kubernetes + Minikube (Local)

**Decision**: Use Kubernetes orchestration with Minikube for local development

**Rationale**:
- Minikube provides full Kubernetes environment locally without cloud costs
- Phase 5 will use cloud K8s (DigitalOcean DOKS, GKE, AKS)
- Helm charts developed for Minikube work unchanged in production
- Aligns with hackathon Phase 4 requirements

**Alternatives Considered**:
- Docker Compose (simpler, not K8s): Doesn't meet hackathon requirement
- K3s (lighter K8s variant): More complex setup than Minikube for beginners
- ✅ **Chosen**: Minikube - standard tool, easy setup, fully K8s-compliant

**Resource Allocation** (Minikube default):
- Memory: 4GB (configurable if needed)
- CPU: 2 cores (configurable)
- Sufficient for 2 replicas of backend + 2 replicas of frontend

---

### 3. Package Manager: Helm 3

**Decision**: Use Helm 3 for declaring and managing Kubernetes resources

**Rationale**:
- Industry standard for K8s package management
- Helm charts are reusable (Phase 5 cloud deployment uses same charts)
- values.yaml allows environment-specific configuration (dev, staging, prod)
- Built-in templating (Jinja2-like syntax) for reducing YAML boilerplate

**Alternatives Considered**:
- Raw kubectl YAML: More verbose, less reusable, manual templating
- Kustomize: Good but more complex than Helm
- ✅ **Chosen**: Helm 3 - mature, standardized, charts ecosystem

**Chart Structure**:
- values.yaml with all configurable parameters
- templates/ with K8s resource manifests
- Chart.yaml for metadata

---

### 4. Resource Limits Configuration

**Decision**: Enforce CPU and memory requests/limits per FR-014

**Rationale**:
- Prevents one pod from consuming all cluster resources
- Minikube cluster (~4GB total) needs fair allocation
- Kubernetes scheduler can make smart decisions with limits defined
- Prevents ImagePullBackOff and OOMKilled errors

**Allocation Strategy**:

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|----|
| Backend | 200m | 500m | 512Mi | 1Gi |
| Frontend | 100m | 300m | 256Mi | 512Mi |
| **Total** | **300m** | **800m** | **768Mi** | **1.5Gi** |

**Justification**:
- 2 backend pods: 400m-1000m CPU, 1Gi-2Gi memory
- 2 frontend pods: 200m-600m CPU, 512Mi-1Gi memory
- Comfortable fit in 4GB Minikube cluster
- Leaves room for system pods (kube-system, default namespace)

**Best Practice**: Requests = guaranteed resources, Limits = maximum allowed

---

### 5. Image Pull Policy: IfNotPresent

**Decision**: Set imagePullPolicy: IfNotPresent per FR-015

**Rationale**:
- Minikube uses local Docker daemon for image building
- Setting IfNotPresent tells K8s to use local images first
- Prevents "ImagePullBackOff" error when K8s tries to pull from remote registry
- Faster pod startup (no network delay)

**Implementation**:
```yaml
# In Helm values.yaml
backend:
  imagePullPolicy: IfNotPresent

frontend:
  imagePullPolicy: IfNotPresent
```

**Alternative**: Always pull remote images (imagePullPolicy: Always)
- Not suitable for Minikube local development
- Would require Docker Hub registry or local registry setup

---

### 6. Health Checks: Liveness & Readiness Probes

**Decision**: Implement HTTP health checks in both backend and frontend

**Rationale**:
- Kubernetes can detect and restart unhealthy pods automatically
- HTTP GET /health is simplest, most reliable probe type
- Reduces manual debugging ("why is my pod in CrashLoopBackOff?")
- Required for production-grade deployments

**Implementation**:

**Backend** (FastAPI):
```python
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

**Frontend** (Next.js):
```javascript
// pages/api/health.ts
export default function handler(req, res) {
  res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() })
}
```

**Kubernetes Probe Configuration**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
  timeoutSeconds: 3
  failureThreshold: 3
```

---

### 7. Logging Strategy: stdout → kubectl logs

**Decision**: Emit all logs to stdout in JSON format; Kubernetes captures via `kubectl logs`

**Rationale**:
- Twelve-factor app principle: Apps write to stdout, runtime captures
- No local PersistentVolumeClaim needed (simplifies Phase 4)
- `kubectl logs` automatically collects container output
- Easy to pipe to external logging service in Phase 5 (Cloud)

**Implementation**:

**Backend** (FastAPI + structlog):
```python
import structlog
logger = structlog.get_logger()
# Logs automatically emit JSON to stdout
logger.info("chat_message_received", user_id=user_id, message_length=len(msg))
```

**Frontend** (Next.js):
```javascript
// JSON structured logs to console
console.log(JSON.stringify({
  timestamp: new Date().toISOString(),
  level: 'info',
  message: 'page_loaded'
}))
```

**Viewing Logs**:
```bash
kubectl logs <pod-name>
# For streaming/follow:
kubectl logs -f <pod-name>
# For all pods in deployment:
kubectl logs -l app=todo-backend
```

---

### 8. Ingress Configuration (Optional): Minikube Tunnel

**Decision**: Provide optional Ingress resource for `http://todo.local` access (alternative to port-forward)

**Rationale**:
- User Story 3, Scenario 6 (acceptance criteria)
- More professional for demos (vs. manual port-forward)
- Minikube tunnel + local DNS entry enables this seamlessly
- Optional: Users can still use port-forward if preferred

**Implementation**:

**Enable in values.yaml**:
```yaml
ingress:
  enabled: true
  hostname: todo.local
```

**Setup steps**:
1. Run `minikube tunnel` (in background)
2. Add to /etc/hosts: `127.0.0.1 todo.local`
3. Access: `http://todo.local:3000`

**Alternative**: kubectl port-forward
```bash
kubectl port-forward svc/todo-frontend 3000:3000
```

---

### 9. AI-Assisted DevOps Integration

**Decision**: Support kubectl-ai and kagent for intelligent K8s operations

**Rationale**:
- Hackathon emphasizes Agentic Dev Stack
- FR-010 and FR-011 require this integration
- kubectl-ai generates correct kubectl commands from natural language
- kagent analyzes cluster health and recommends optimizations

**Setup** (from assumptions):
```bash
# Assuming kubectl-ai and kagent are installed
export KUBECTL_AI_KEY=<your-api-key>
export KAGENT_KEY=<your-api-key>

# Example usage
kubectl-ai "deploy the frontend with 3 replicas"
kagent "analyze the cluster health"
```

**K8s Integration**:
- Store API keys in K8s Secrets
- Inject as env vars for future CLI usage
- Document setup in quickstart.md

---

## Decisions Summary Table

| Area | Decision | Status |
|------|----------|--------|
| Base Image | Alpine Linux | ✅ Confirmed |
| Orchestration | Kubernetes + Minikube | ✅ Confirmed |
| Package Manager | Helm 3 | ✅ Confirmed |
| Resource Limits | FR-014 (defined) | ✅ Confirmed |
| Image Pull | IfNotPresent (FR-015) | ✅ Confirmed |
| Health Checks | HTTP /health endpoints | ✅ Confirmed |
| Logging | stdout → kubectl logs | ✅ Confirmed |
| Ingress | Optional (Minikube tunnel) | ✅ Confirmed |
| AI-Ops | kubectl-ai + kagent | ✅ Confirmed |

## Next Steps

✅ **Research Complete** → Proceed to Phase 1: Design & Contracts
- Generate data-model.md
- Create contract files (Helm, Dockerfile, K8s manifests)
- Write quickstart.md with setup instructions
