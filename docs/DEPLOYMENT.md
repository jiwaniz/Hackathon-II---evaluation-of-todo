# Phase 4: Local Kubernetes Deployment Guide

**Feature**: Local Kubernetes Deployment - Deploy Todo Chatbot to Minikube with Helm, Docker, and AI-assisted DevOps tools

**Date**: 2026-02-21

**Status**: Implementation in progress

---

## Overview

This guide provides step-by-step instructions to deploy the Phase III Todo AI Chatbot to a local Minikube cluster using Helm charts, Docker containerization, and Kubernetes best practices.

## Prerequisites

Before starting, ensure you have:

- ✅ **Minikube** 1.25+ installed: `minikube version`
- ✅ **kubectl** CLI installed: `kubectl version --client`
- ✅ **Helm** 3+ installed: `helm version`
- ✅ **Docker Desktop** installed and running
- ✅ **Phase III Todo chatbot** fully implemented and tested locally
- ✅ **Neon PostgreSQL** database configured and accessible
- ✅ **API Keys** available (Groq, Better Auth)

### Installation Verification

```bash
# Verify all tools are installed
docker --version
minikube version
kubectl version --client
helm version
```

---

## Step 0: Configure Minikube Docker Environment (MANDATORY)

**CRITICAL**: Before building any Docker images, you must configure your shell to use Minikube's Docker daemon. This ensures images are built inside the Minikube cluster, making them immediately available with `imagePullPolicy: IfNotPresent`.

```bash
# Set up shell environment to use Minikube's Docker daemon
eval $(minikube docker-env)

# Verify you're now using Minikube's Docker
docker ps  # Should show Minikube's containers
docker info | grep -i "docker root dir"  # Should show Minikube path

# To exit Minikube's Docker context later (when done):
unset DOCKER_HOST DOCKER_CERT_PATH DOCKER_TLS_VERIFY
```

**Why This Matters**:
- ✅ Images built directly in Minikube node
- ✅ No need for registry push/pull
- ✅ `imagePullPolicy: IfNotPresent` works correctly
- ❌ Without this, K8s will try remote registry pull and fail with `ImagePullBackOff`

**Note**: This configuration is shell-specific. You need to run it in each new terminal where you build images.

---

## Step 1: Start Minikube Cluster

```bash
# Start Minikube with recommended settings
minikube start \
  --memory 4096 \
  --cpus 2 \
  --driver=docker

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

**Expected Output**:
```
Kubernetes control plane is running at https://127.0.0.1:51234
...
NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   5m23s   v1.29.2
```

### Troubleshooting: Minikube Start

If Minikube fails to start:

```bash
# Check Docker daemon is running
docker ps

# Reset Minikube if needed
minikube delete
minikube start --memory 4096 --cpus 2

# Increase resources if needed (requires more RAM available)
minikube config set memory 6144
minikube config set cpus 4
```

---

## Step 2: Build Docker Images

Since you've already configured Minikube's Docker environment in Step 0, your images will be built directly inside the Minikube cluster.

### Build Backend Image

```bash
# From project root (with Minikube Docker env already set)
docker build -f backend/Dockerfile -t todo-backend:latest .

# Verify image is created in Minikube
docker images | grep todo-backend
```

**Expected Output**:
```
REPOSITORY         TAG      IMAGE ID       CREATED         SIZE
todo-backend       latest   a1b2c3d4e5f6   5 seconds ago   150MB
```

### Build Frontend Image

```bash
# From project root
docker build -f frontend/Dockerfile -t todo-frontend:latest .

# Verify image is created in Minikube
docker images | grep todo-frontend
```

**Expected Output**:
```
REPOSITORY         TAG      IMAGE ID       CREATED         SIZE
todo-frontend      latest   f6e5d4c3b2a1   10 seconds ago  100MB
```

**Key Point**: Both images are now in Minikube's Docker daemon. No push/pull needed!

### Troubleshooting: Docker Build

If builds fail:

```bash
# Verify you're in Minikube's Docker context
echo $DOCKER_HOST  # Should show Minikube path

# Re-set if needed
eval $(minikube docker-env)

# Check Dockerfile syntax
docker build -f backend/Dockerfile --dry-run .

# Check dependencies are installed
cat backend/requirements.txt
npm ci --prefix frontend

# View build logs in detail
docker build -f backend/Dockerfile --progress=plain .
```

---

## Step 3: Verify Images in Minikube

```bash
# List all images available in Minikube
minikube image ls | grep todo

# Alternative: List via docker
docker images | grep todo
```

**Expected Output**:
```
todo-backend:latest
todo-frontend:latest
```

---

## Step 4: Create Kubernetes Secrets

Store sensitive values in K8s Secrets:

```bash
# Create secrets for database and API keys
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@neon.tech/db' \
  --from-literal=GROQ_API_KEY='gsk_xxxxx' \
  --from-literal=BETTER_AUTH_SECRET='hs256-secret-key' \
  --from-literal=KUBECTL_AI_KEY='your-kubectl-ai-key'

# Verify secrets are created
kubectl get secrets
kubectl describe secret todo-secrets
```

**Expected Output**:
```
NAME           TYPE     DATA   AGE
todo-secrets   Opaque   4      5s
```

---

## Step 5: Deploy with Helm

### Install Helm Chart

```bash
# Navigate to project root (where helm/ directory exists)
helm install todo-chatbot ./helm \
  --set backend.environment.DATABASE_URL=$DATABASE_URL \
  --set backend.environment.GROQ_API_KEY=$GROQ_API_KEY \
  --set backend.environment.BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET \
  --set frontend.environment.BETTER_AUTH_URL='http://localhost:3000' \
  --set frontend.environment.TRUSTED_ORIGINS='http://localhost:3000'

# Verify Helm release
helm status todo-chatbot
helm get values todo-chatbot
```

**Expected Output**:
```
NAME: todo-chatbot
LAST DEPLOYED: Fri Feb 21 14:30:45 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
```

### Troubleshooting: Helm Install

```bash
# Dry-run to see manifests before deploying
helm install todo-chatbot ./helm --dry-run --debug

# Lint Helm chart
helm lint ./helm

# Check if values are valid YAML
cat helm/values.yaml | yaml-lint

# View Helm history
helm history todo-chatbot
```

---

## Step 6: Verify Deployment

### Check Pod Status

```bash
# Watch pods come up
kubectl get pods -w

# Get detailed pod information
kubectl describe pods

# View logs from backend
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend
```

**Expected Output**:
```
NAME                                  READY   STATUS    RESTARTS   AGE
todo-backend-5d7f8c3a9b-abc12         1/1     Running   0          30s
todo-backend-5d7f8c3a9b-def45         1/1     Running   0          30s
todo-frontend-7k8l9m0n1p-ghi67        1/1     Running   0          25s
todo-frontend-7k8l9m0n1p-jkl89        1/1     Running   0          25s
```

### Check Services

```bash
# List Kubernetes services
kubectl get svc

# Get service details
kubectl describe svc todo-backend
kubectl describe svc todo-frontend
```

**Expected Output**:
```
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    5m
todo-backend     ClusterIP   10.96.50.123    <none>        8000/TCP   30s
todo-frontend    ClusterIP   10.96.60.456    <none>        3000/TCP   30s
```

---

## Step 7: Access Application

### Option A: Port-Forward (Simple)

```bash
# Forward local 3000 to frontend service
kubectl port-forward svc/todo-frontend 3000:3000

# In another terminal, forward backend
kubectl port-forward svc/todo-backend 8000:8000

# Access frontend
open http://localhost:3000
```

### Option B: Minikube Tunnel + Ingress (Advanced)

```bash
# Start Minikube tunnel (requires sudo on Linux/Mac)
minikube tunnel

# Add hostname to /etc/hosts
echo "127.0.0.1 todo.local" | sudo tee -a /etc/hosts

# Enable Ingress in Helm values
helm upgrade todo-chatbot ./helm \
  --set ingress.enabled=true \
  --set frontend.environment.BETTER_AUTH_URL='http://todo.local:3000' \
  --set frontend.environment.TRUSTED_ORIGINS='http://todo.local:3000'

# Access via domain
open http://todo.local:3000
```

### Verify Application Works

```bash
# Test backend API
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2026-02-21T14:35:00Z"}

# Test frontend
curl http://localhost:3000

# Expected: HTML page content (Next.js app)
```

---

## Common Issues & Solutions

### Issue: ImagePullBackOff

**Symptom**: Pod status shows `ImagePullBackOff`

**Solution**:
1. Verify image is loaded in Minikube: `minikube image ls`
2. Check imagePullPolicy is `IfNotPresent`: `kubectl get pods -o yaml`
3. Rebuild and reload image:
   ```bash
   docker build -f backend/Dockerfile -t todo-backend:latest .
   minikube image load todo-backend:latest
   kubectl delete pod -l app=todo-backend  # Restart pod
   ```

### Issue: CrashLoopBackOff

**Symptom**: Pod keeps restarting

**Solution**:
1. Check logs: `kubectl logs <pod-name> --previous`
2. Common causes:
   - Missing environment variables (DATABASE_URL, etc.)
   - Wrong health check endpoint
   - Container exiting after startup
3. Verify secrets exist: `kubectl get secrets`
4. Check values passed to Helm: `helm get values todo-chatbot`

### Issue: Connection Refused

**Symptom**: Cannot connect to backend from frontend

**Solution**:
1. Verify services exist: `kubectl get svc`
2. Test internal DNS: `kubectl exec <frontend-pod> -- nslookup todo-backend`
3. Check API_URL environment variable: `kubectl exec <frontend-pod> -- env | grep API_URL`
4. Verify backend is running: `kubectl get pods -l app=todo-backend`

### Issue: Minikube Out of Memory

**Symptom**: Pods get OOMKilled or nodes become NotReady

**Solution**:
```bash
# Increase Minikube memory
minikube config set memory 6144
minikube stop
minikube start

# Or adjust resource limits in Helm values
helm upgrade todo-chatbot ./helm \
  --set backend.resources.limits.memory=512Mi \
  --set frontend.resources.limits.memory=300Mi
```

---

## Next Steps

✅ **Phase 4 Deployment Complete!**

- Review logs and ensure no errors
- Test chat functionality in browser
- Test task CRUD operations
- Review resource usage: `kubectl top pods`

**Ready for Phase 5 (Cloud Deployment)**:
- Push images to container registry (Docker Hub, GCR, ECR)
- Deploy to cloud Kubernetes (DigitalOcean, GKE, AKS)
- Add Kafka for event streaming
- Add Dapr for distributed app runtime
- Implement monitoring and logging

---

## Useful Commands Reference

```bash
# Deployment & Status
kubectl apply -f file.yaml
kubectl get pods,svc,deployments
kubectl describe pod <pod-name>
kubectl logs <pod-name> -f
kubectl exec <pod-name> -- /bin/sh

# Helm
helm list
helm status <release-name>
helm upgrade <release-name> ./helm
helm rollback <release-name>

# Debugging
kubectl port-forward svc/<service> 3000:3000
kubectl port-forward pod/<pod-name> 3000:3000
kubectl exec <pod-name> -- curl http://localhost:8000/health

# Cleanup
kubectl delete pod <pod-name>
kubectl delete svc <svc-name>
helm uninstall <release-name>
```

---

**Document Version**: 1.0
**Last Updated**: 2026-02-21
**Status**: Phase 4 MVP Implementation Guide
