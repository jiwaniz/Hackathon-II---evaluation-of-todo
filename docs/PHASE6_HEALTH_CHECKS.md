# Phase 6: Health Checks and Observability Implementation Guide

**Tasks**: T048-T058
**User Story**: US4 - Health Checks and Observability (P2)
**Status**: Implementation Guide (requires Kubernetes environment)

## Overview

Phase 6 implements comprehensive health monitoring and structured logging for both backend and frontend services. This enables Kubernetes to:

1. **Detect failures** via liveness probes (restart unhealthy containers)
2. **Route traffic** via readiness probes (wait for startup completion)
3. **Monitor health** via health endpoints (`/health`, `/api/health`)
4. **Troubleshoot issues** via structured JSON logs

---

## Task Breakdown

### T048-T049: Health Endpoints (✅ COMPLETE)

**Status**: Both health endpoints implemented and ready

#### Backend (/health)
- **Location**: `backend/main.py:73-88`
- **Response Format**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-02-21T15:30:45.123456",
    "environment": "development",
    "auth": {
      "supabase_jwt_configured": true,
      "supabase_url_configured": true
    }
  }
  ```
- **Test**: `curl http://localhost:8000/health`

#### Frontend (/api/health)
- **Location**: `frontend/app/api/health/route.ts`
- **Response Format**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-02-21T15:30:45.123Z",
    "version": "2.0.0",
    "environment": "development",
    "checks": {
      "memory": true,
      "database": true,
      "api": true
    }
  }
  ```
- **Test**: `curl http://localhost:3000/api/health`

---

### T050-T051: Structured Logging Configuration

#### Backend Structured Logging (T050)

The backend already uses structured logging via `logging_config.py`. To enhance with JSON output:

**Implementation Steps**:

1. **Install structlog** (if not already installed):
   ```bash
   cd backend
   uv add structlog
   ```

2. **Update `backend/logging_config.py`** to configure JSON logging:
   ```python
   import structlog
   import logging

   def setup_structured_logging():
       """Configure structlog for JSON output to stdout."""
       structlog.configure(
           processors=[
               structlog.stdlib.filter_by_level,
               structlog.stdlib.add_logger_name,
               structlog.stdlib.add_log_level,
               structlog.stdlib.PositionalArgumentsFormatter(),
               structlog.processors.TimeStamper(fmt="iso"),
               structlog.processors.StackInfoRenderer(),
               structlog.processors.format_exc_info,
               structlog.processors.UnicodeDecoder(),
               structlog.processors.JSONRenderer()
           ],
           context_class=dict,
           logger_factory=structlog.stdlib.LoggerFactory(),
           cache_logger_on_first_use=True,
       )
   ```

3. **Update `backend/middleware/logging.py`** to log request/response metadata:
   ```python
   # Add request_id, user_id, response_time_ms to JSON logs
   logger = structlog.get_logger()
   logger.info(
       "request_completed",
       request_id=request.headers.get("X-Request-ID"),
       endpoint=request.url.path,
       method=request.method,
       status=response.status_code,
       response_time_ms=duration_ms,
   )
   ```

4. **Verify JSON output**:
   ```bash
   uv run uvicorn main:app --reload 2>&1 | head -20
   # Output should include JSON logs like:
   # {"event":"request_completed","timestamp":"2026-02-21T15:30:45.123Z",...}
   ```

**Expected Log Fields**:
- `timestamp` - ISO 8601 timestamp
- `level` - Log level (INFO, ERROR, DEBUG)
- `message` - Log message
- `user_id` - User making the request
- `request_id` - Unique request identifier
- `response_time_ms` - Request duration
- `endpoint` - API endpoint path

---

#### Frontend Structured Logging (T051)

The frontend logs to browser console. To structure for `kubectl logs` compatibility:

**Implementation Steps**:

1. **Create `frontend/lib/logger.ts`**:
   ```typescript
   interface StructuredLog {
     timestamp: string;
     level: 'debug' | 'info' | 'warn' | 'error';
     message: string;
     component?: string;
     data?: Record<string, any>;
   }

   export function createLogger(component: string) {
     return {
       info: (message: string, data?: Record<string, any>) => {
         const log: StructuredLog = {
           timestamp: new Date().toISOString(),
           level: 'info',
           message,
           component,
           data,
         };
         console.log(JSON.stringify(log));
       },
       error: (message: string, error?: Error, data?: Record<string, any>) => {
         const log: StructuredLog = {
           timestamp: new Date().toISOString(),
           level: 'error',
           message,
           component,
           data: { ...data, error: error?.message },
         };
         console.error(JSON.stringify(log));
       },
     };
   }
   ```

2. **Use in components** (e.g., `frontend/components/chat/ChatWindow.tsx`):
   ```typescript
   import { createLogger } from '@/lib/logger';

   const logger = createLogger('ChatWindow');

   const handleSendMessage = async (message: string) => {
     logger.info('Sending message', { message_length: message.length });
     // ... send message
   };
   ```

3. **Verify logs appear in `kubectl logs`**:
   ```bash
   kubectl logs -f deployment/todo-frontend
   # Output: {"timestamp":"2026-02-21T...","level":"info",...}
   ```

---

### T052-T055: Kubernetes Probe Configuration

The backend and frontend deployments already have probe configuration in the Helm templates:

**Backend Deployment Probes** (`helm/templates/backend-deployment.yaml`):
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
  timeoutSeconds: 3
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 2
```

**Frontend Deployment Probes** (`helm/templates/frontend-deployment.yaml`):
```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 30
  timeoutSeconds: 3
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 2
```

**Probe Explanation**:
- **livenessProbe**: Restarts container if probe fails 3 times
  - Checks every 30 seconds after 10 second startup delay
  - Useful for detecting deadlocks or memory leaks
- **readinessProbe**: Removes from load balancer if probe fails 2 times
  - Checks every 10 seconds after 5 second startup delay
  - Prevents traffic routing to containers still initializing

---

### T056: Test Probes

**Steps to Test**:

1. **Deploy updated chart with probes**:
   ```bash
   helm install todo-chatbot ./helm --set ingress.enabled=false
   ```

2. **Wait for pods to stabilize** (should see Ready 1/1):
   ```bash
   watch -n 1 kubectl get pods
   # Output:
   # NAME                              READY   STATUS    RESTARTS   AGE
   # todo-backend-64f5d5b4f-xxxxx      1/1     Running   0          2m
   # todo-frontend-7d9c8f9f8-xxxxx     1/1     Running   0          2m
   ```

3. **Check probe success events**:
   ```bash
   kubectl describe pod <backend-pod-name>
   # Look for "Liveness probe succeeded" and "Readiness probe succeeded"
   ```

4. **Test manual failure**:
   ```bash
   # Force container to fail (for testing)
   kubectl exec <backend-pod-name> -- killall -9 uvicorn
   # Watch pod restart automatically within 30 seconds
   watch -n 1 kubectl get pods
   ```

---

### T057: Log Verification

**Steps to Verify JSON Logs**:

1. **Get backend logs**:
   ```bash
   kubectl logs <backend-pod-name> -f --timestamps=true
   ```

2. **Parse with jq** to extract fields:
   ```bash
   kubectl logs <backend-pod-name> | jq '.timestamp, .level, .message, .user_id'
   # Output:
   # "2026-02-21T15:30:45.123Z"
   # "INFO"
   # "request_completed"
   # "user-123"
   ```

3. **Filter by log level**:
   ```bash
   kubectl logs <backend-pod-name> | jq 'select(.level=="ERROR")'
   ```

4. **Monitor frontend logs**:
   ```bash
   kubectl logs <frontend-pod-name> -f | jq '.component, .message'
   ```

---

### T058: Documentation

**Add to `docs/DEPLOYMENT.md`** (Health Checks & Logging Section):

```markdown
## Health Checks and Observability

### Health Endpoints

Both services expose health endpoints for Kubernetes probes:

- **Backend**: `GET /health` → Returns JSON with status, timestamp, environment
- **Frontend**: `GET /api/health` → Returns JSON with status, checks (memory, database, api)

Test manually:
```bash
# Backend health
curl -s http://localhost:8000/health | jq '.'

# Frontend health
curl -s http://localhost:3000/api/health | jq '.'
```

### Kubernetes Probes

Both deployments are configured with liveness and readiness probes:

- **Liveness Probe**: Detects stuck/crashed containers, triggers restart
- **Readiness Probe**: Detects initialization time, prevents early traffic

Monitor probe status:
```bash
kubectl describe pod <pod-name> | grep -A 5 "Probe"
```

### Structured Logging

Logs are JSON-formatted for machine parsing:

```bash
# View raw logs
kubectl logs <pod-name> -f

# Pretty-print with jq
kubectl logs <pod-name> | jq '.'

# Filter by level
kubectl logs <pod-name> | jq 'select(.level=="ERROR")'

# Extract specific fields
kubectl logs <pod-name> | jq '{timestamp, level, message, endpoint}'
```

Expected log fields:
- `timestamp` - ISO 8601 timestamp
- `level` - DEBUG, INFO, WARN, ERROR
- `message` - Log message
- `user_id` - User context (if applicable)
- `endpoint` - API endpoint (backend only)
- `response_time_ms` - Request duration (backend only)
- `component` - UI component (frontend only)
```

---

## Checklist

- [x] T048: Backend health endpoint (implemented in main.py:73-88)
- [x] T049: Frontend health endpoint (implemented in app/api/health/route.ts)
- [ ] T050: Backend structured logging (implement in logging_config.py, requires structlog)
- [ ] T051: Frontend structured logging (implement in lib/logger.ts)
- [ ] T052: Backend liveness probe (configured in backend-deployment.yaml)
- [ ] T053: Backend readiness probe (configured in backend-deployment.yaml)
- [ ] T054: Frontend liveness probe (configured in frontend-deployment.yaml)
- [ ] T055: Frontend readiness probe (configured in frontend-deployment.yaml)
- [ ] T056: Test probes (manual validation in Minikube)
- [ ] T057: Log verification (manual validation with kubectl logs + jq)
- [ ] T058: Documentation (add to DEPLOYMENT.md)

---

## Next Steps

After implementing Phase 6:

1. **Deploy to Minikube** with updated Helm chart
2. **Verify probes** are working (kubectl describe pod)
3. **Test logs** are in JSON format (kubectl logs + jq)
4. **Monitor** pod restarts and readiness transitions
5. **Proceed to Phase 7** (kubectl-ai integration)

---

## Files Modified/Created

- ✅ `frontend/app/api/health/route.ts` - Created
- 🔄 `backend/logging_config.py` - Requires update (structured logging)
- 🔄 `frontend/lib/logger.ts` - Requires creation
- ✅ `helm/templates/backend-deployment.yaml` - Already configured
- ✅ `helm/templates/frontend-deployment.yaml` - Already configured
- 🔄 `docs/DEPLOYMENT.md` - Requires update (health checks section)
