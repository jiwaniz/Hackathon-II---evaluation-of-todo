# Phase 7: kubectl-ai Integration Implementation Guide

**Tasks**: T059-T065
**User Story**: US5 - kubectl-ai Integration (P2)
**Status**: Implementation Guide (requires kubectl-ai tool)

## Overview

Phase 7 enables intelligent Kubernetes operations through `kubectl-ai`, allowing natural language commands to generate and execute Kubernetes operations. This integrates with the RBAC configuration created in Phase 2 (T012).

## Prerequisites

- **Minikube cluster** running (from Phase 5)
- **kubectl** configured and working
- **kubectl-ai** installed (`curl -sL https://aka.ms/kubectl-ai/install.sh | bash`)
- **API Key** for kubectl-ai (free tier at https://app.kubectl.sh)
- **Helm chart** deployed with RBAC (from Phase 2)

---

## Task Breakdown

### T059: Verify kubectl-ai Installation

**Steps**:

1. **Install kubectl-ai** (if not already installed):
   ```bash
   curl -sL https://aka.ms/kubectl-ai/install.sh | bash
   # Or install via Homebrew (macOS):
   brew install kubectl-ai
   ```

2. **Verify installation**:
   ```bash
   kubectl-ai --version
   # Output: kubectl-ai version X.Y.Z
   ```

3. **Configure API Key**:
   ```bash
   # Set KUBECTL_AI_KEY environment variable
   export KUBECTL_AI_KEY="sk_..."  # Get key from https://app.kubectl.sh

   # Verify key is set
   echo $KUBECTL_AI_KEY
   ```

4. **Store API key in Kubernetes Secret** (if not already created in T039):
   ```bash
   kubectl create secret generic kubectl-ai-secret \
     --from-literal=KUBECTL_AI_KEY="$KUBECTL_AI_KEY"
   ```

5. **Verify kubectl-ai can list resources**:
   ```bash
   kubectl-ai get pods
   # Should output pods without errors
   ```

---

### T060: Configure ServiceAccount for kubectl-ai

The RBAC configuration was created in Phase 2 (T012). Verify it's in place:

**Verify ServiceAccount**:
```bash
kubectl get serviceaccount
# Should show: todo-chatbot-robot

kubectl get clusterrole
# Should show: todo-chatbot-agent-role

kubectl get clusterrolebinding
# Should show: todo-chatbot-agent-rolebinding
```

**Check RBAC Permissions**:
```bash
kubectl auth can-i get pods \
  --as=system:serviceaccount:default:todo-chatbot-robot
# Output: yes

kubectl auth can-i list deployments \
  --as=system:serviceaccount:default:todo-chatbot-robot
# Output: yes

kubectl auth can-i patch pods \
  --as=system:serviceaccount:default:todo-chatbot-robot
# Output: yes
```

**RBAC Configuration** (already in `helm/templates/rbac.yaml`):
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-chatbot-robot
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: todo-chatbot-agent-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch", "describe"]
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets", "daemonsets", "replicasets"]
  verbs: ["get", "list", "watch", "describe", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: todo-chatbot-agent-rolebinding
subjects:
- kind: ServiceAccount
  name: todo-chatbot-robot
  namespace: default
roleRef:
  kind: ClusterRole
  name: todo-chatbot-agent-role
  apiGroup: rbac.authorization.k8s.io
```

---

### T061: Test kubectl-ai Scaling

**Objective**: Scale backend deployment using natural language

**Steps**:

1. **Current state**:
   ```bash
   kubectl get deployment todo-backend
   # Output shows current replicas (e.g., 1)
   ```

2. **Scale using kubectl-ai**:
   ```bash
   kubectl-ai "scale the backend deployment to 3 replicas"
   # kubectl-ai generates: kubectl scale deployment todo-backend --replicas=3
   # Prompts: [y/n] to execute?
   # Type: y
   ```

3. **Verify scaling**:
   ```bash
   kubectl get pods -l app=todo-backend
   # Output should show 3 backend pods
   ```

4. **Scale back down**:
   ```bash
   kubectl-ai "reduce backend to 1 replica"
   kubectl get pods -l app=todo-backend
   # Output should show 1 backend pod
   ```

---

### T062: Test kubectl-ai Diagnostics

**Objective**: Get AI-generated diagnostics for pod issues

**Steps**:

1. **Force an error** (optional):
   ```bash
   kubectl set env deployment/todo-backend DATABASE_URL="invalid://url"
   # Pods will likely fail to connect to database
   kubectl get pods
   ```

2. **Ask kubectl-ai for diagnostics**:
   ```bash
   kubectl-ai "why is the backend pod crashing?"
   # kubectl-ai analyzes logs and pod status, provides analysis
   ```

3. **Get optimization suggestions**:
   ```bash
   kubectl-ai "what's wrong with the backend deployment and how do I fix it?"
   # kubectl-ai suggests: rollback env var, check database connection, etc.
   ```

4. **Fix the issue** (if you created one):
   ```bash
   kubectl set env deployment/todo-backend DATABASE_URL="postgresql://..." --overwrite
   kubectl rollout status deployment/todo-backend
   ```

---

### T063: Test kubectl-ai Deployment

**Objective**: Deploy frontend using natural language

**Steps**:

1. **Current deployment**:
   ```bash
   kubectl get deployment todo-frontend
   ```

2. **Scale frontend with natural language**:
   ```bash
   kubectl-ai "deploy the frontend with 2 replicas for load balancing"
   # kubectl-ai generates: kubectl scale deployment todo-frontend --replicas=2
   # Type: y to confirm
   ```

3. **Verify deployment**:
   ```bash
   kubectl get pods -l app=todo-frontend
   # Output should show 2 frontend pods
   ```

4. **Check service endpoints**:
   ```bash
   kubectl get svc todo-frontend
   kubectl get endpoints todo-frontend
   # Output should show 2 endpoints
   ```

---

### T064: Document kubectl-ai Setup

Create comprehensive kubectl-ai setup guide. This is already in the implementation, but enhance `docs/KUBECTL_AI_SETUP.md`:

**File**: `docs/KUBECTL_AI_SETUP.md`

```markdown
# kubectl-ai Setup and Usage Guide

## Installation

### Prerequisites
- kubectl configured and connected to Minikube cluster
- curl or package manager available

### Install kubectl-ai

**Option 1: Using installation script**
```bash
curl -sL https://aka.ms/kubectl-ai/install.sh | bash
```

**Option 2: Using Homebrew (macOS)**
```bash
brew install kubectl-ai
```

**Option 3: Using Chocolatey (Windows)**
```powershell
choco install kubectl-ai
```

## Configuration

### Get API Key

1. Visit https://app.kubectl.sh
2. Sign up or log in
3. Generate API key from dashboard
4. Copy the key (starts with `sk_`)

### Set Environment Variable

```bash
export KUBECTL_AI_KEY="sk_your_api_key_here"

# Verify it's set
echo $KUBECTL_AI_KEY
```

### Persist API Key (Optional)

**Bash/Zsh**:
```bash
echo 'export KUBECTL_AI_KEY="sk_..."' >> ~/.zshrc
source ~/.zshrc
```

**Fish**:
```bash
set -Ux KUBECTL_AI_KEY "sk_..."
```

## RBAC Configuration

The Todo Chatbot Helm chart includes RBAC setup for kubectl-ai:

**ServiceAccount**: `todo-chatbot-robot`
**Permissions**:
- get, list, watch, describe pods/services/deployments
- patch deployments (for scaling, updates)

Verify permissions:
```bash
kubectl auth can-i get pods \
  --as=system:serviceaccount:default:todo-chatbot-robot
# Output: yes
```

## Example Commands

### 1. Scale Deployment
```bash
kubectl-ai "scale backend to 3 replicas"
# kubectl-ai generates and confirms:
# kubectl scale deployment todo-backend --replicas=3
```

### 2. View Pod Logs
```bash
kubectl-ai "show me the logs from the backend pod that's failing"
# kubectl-ai generates and executes:
# kubectl logs <failing-pod> -n default
```

### 3. Get Debugging Info
```bash
kubectl-ai "what's causing the frontend pod to crash?"
# kubectl-ai analyzes:
# - Pod status and events
# - Recent logs
# - Resource usage
# Provides analysis and suggestions
```

### 4. Apply Changes
```bash
kubectl-ai "update the backend with new environment variables"
# kubectl-ai can generate kubectl patch commands
```

### 5. Complex Operations
```bash
kubectl-ai "I want to scale the backend to 5 replicas but keep frontend at 2"
# kubectl-ai generates two separate scale commands
```

## Advanced Usage

### Dry-Run Mode

```bash
kubectl-ai "what command would scale backend to 5 replicas?"
# kubectl-ai outputs command without executing
```

### Interactive Mode

```bash
kubectl-ai
# Drops into interactive prompt for multiple commands
```

### Custom Context

```bash
kubectl-ai --context my-context "get all resources"
# Runs against specific context
```

## Troubleshooting

### "API Key Invalid"
```bash
# Verify key is set
echo $KUBECTL_AI_KEY

# Regenerate key at https://app.kubectl.sh
# Update environment variable
```

### "Permission Denied"
```bash
# Verify RBAC permissions
kubectl auth can-i get pods --as=system:serviceaccount:default:todo-chatbot-robot

# Ensure ServiceAccount is deployed
kubectl get serviceaccount todo-chatbot-robot
```

### "Connection Timeout"
```bash
# Verify Minikube cluster is running
minikube status

# Check kubectl connectivity
kubectl cluster-info
```

## Best Practices

1. **Always review generated commands** before executing
2. **Start with non-destructive commands** (get, describe, list)
3. **Use scaling for load testing**, not production changes
4. **Monitor logs** after each kubectl-ai operation
5. **Keep API key secure** - don't commit to version control

## Integration with Automation

Use kubectl-ai in scripts for automated operations:

```bash
#!/bin/bash
# Scale backend based on CPU usage

if [ "$(kubectl top pod -l app=todo-backend | tail -1 | awk '{print $2}' | sed 's/m//')" -gt 800 ]; then
  kubectl-ai "scale backend deployment to 3 replicas"
fi
```

## Phase Integration

kubectl-ai works with Phase 4 MVP infrastructure:

- **RBAC**: ServiceAccount + ClusterRole configured (T012)
- **Health Checks**: kubectl-ai uses /health endpoint to monitor pods
- **Logging**: kubectl-ai aggregates pod logs for diagnostics
- **Helm**: kubectl-ai can scale Helm-deployed resources
```

---

### T065: Verify Logs

**Objective**: Confirm kubectl-ai operations appear in structured logs

**Steps**:

1. **Enable operation logging** (if not configured):
   ```bash
   # Backend logs operations via middleware
   kubectl logs -l app=todo-backend -f | jq 'select(.event=="kubectl_operation")'
   ```

2. **Perform kubectl-ai operation**:
   ```bash
   kubectl-ai "scale backend to 2 replicas"
   # Type: y to confirm
   ```

3. **Check logs for operation record**:
   ```bash
   kubectl logs -l app=todo-backend | jq '.[] | select(.component=="kubectl-ai")'
   # Expected output:
   # {
   #   "timestamp": "2026-02-21T...",
   #   "level": "info",
   #   "component": "kubectl-ai",
   #   "message": "Deployment scaled",
   #   "deployment": "todo-backend",
   #   "replicas": 2
   # }
   ```

---

## Checklist

- [ ] T059: kubectl-ai installation verified
- [ ] T060: ServiceAccount and RBAC permissions verified
- [ ] T061: Scaling test passed (backend 1 → 3 → 1 replicas)
- [ ] T062: Diagnostics test passed (identified mock issue)
- [ ] T063: Deployment test passed (frontend scaled to 2 replicas)
- [ ] T064: Setup documentation created (docs/KUBECTL_AI_SETUP.md)
- [ ] T065: Operations logged to structured logs

---

## Next Steps

1. **Test all kubectl-ai commands** in Minikube
2. **Integrate kubectl-ai** into monitoring/alerting
3. **Proceed to Phase 8** (kagent integration)

---

## Files Created/Modified

- ✅ `docs/KUBECTL_AI_SETUP.md` - Comprehensive setup guide
- 🔄 Backend logging - May need updates to log kubectl-ai operations
- 🔄 `helm/templates/rbac.yaml` - Already configured (T012)
