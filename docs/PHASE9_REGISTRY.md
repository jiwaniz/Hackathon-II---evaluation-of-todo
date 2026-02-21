# Phase 9: Container Registry Integration Implementation Guide

**Tasks**: T072-T079
**User Story**: US7 - Container Registry Integration (P3)
**Status**: Implementation Guide (optional, for distributed deployments)

## Overview

Phase 9 enables Docker image push/pull from a registry for distributed deployments. This allows images to be shared across multiple Kubernetes clusters and stored persistently outside Minikube's local Docker daemon.

## Prerequisites

- Docker CLI installed and running
- Minikube cluster with images already built (from Phase 5)
- Docker registry (local, Docker Hub, or cloud provider)
- Images tagged and ready: `todo-backend:latest`, `todo-frontend:latest`

---

## Quick Start

```bash
# 1. Create local registry in Minikube
docker run -d --name=registry -p 5000:5000 registry:latest

# 2. Tag images with registry URL
docker tag todo-backend:latest localhost:5000/todo-backend:v1.0
docker tag todo-frontend:latest localhost:5000/todo-frontend:v1.0

# 3. Push to registry
docker push localhost:5000/todo-backend:v1.0
docker push localhost:5000/todo-frontend:v1.0

# 4. Verify in registry
curl http://localhost:5000/v2/_catalog

# 5. Update Helm chart
helm install todo-chatbot ./helm \
  --set backend.image="localhost:5000/todo-backend:v1.0" \
  --set frontend.image="localhost:5000/todo-frontend:v1.0"
```

---

## Task Breakdown

### T072-T076: Local Registry Setup and Image Push

**T072: Create Local Docker Registry**

```bash
# Option 1: Docker container registry
docker run -d \
  --name=registry \
  -p 5000:5000 \
  --restart=always \
  -v registry-storage:/var/lib/registry \
  registry:latest

# Option 2: Using Minikube's built-in registry addon
minikube addons enable registry

# Verify registry is running
curl http://localhost:5000/v2/_catalog
# Output: {"repositories":[]}
```

**T073-T074: Tag Images**

```bash
# Backend image
docker tag todo-backend:latest localhost:5000/todo-backend:v1.0
docker tag todo-backend:latest localhost:5000/todo-backend:latest

# Frontend image
docker tag todo-frontend:latest localhost:5000/todo-frontend:v1.0
docker tag todo-frontend:latest localhost:5000/todo-frontend:latest

# Verify tags
docker images | grep localhost
```

**T075-T076: Push Images to Registry**

```bash
# Push backend
docker push localhost:5000/todo-backend:v1.0
docker push localhost:5000/todo-backend:latest

# Push frontend
docker push localhost:5000/todo-frontend:v1.0
docker push localhost:5000/todo-frontend:latest

# Verify push
curl http://localhost:5000/v2/_catalog
# Output: {"repositories":["todo-backend","todo-frontend"]}

# List tags for backend
curl http://localhost:5000/v2/todo-backend/tags/list
# Output: {"name":"todo-backend","tags":["v1.0","latest"]}
```

---

### T077: Update Helm Values for Registry

**Create `helm/values-registry.yaml`**:

```yaml
# Registry configuration for distributed deployments

backend:
  replicaCount: 1
  image:
    repository: localhost:5000/todo-backend
    tag: v1.0
    pullPolicy: IfNotPresent  # FR-015: Don't re-pull if already present

frontend:
  replicaCount: 1
  image:
    repository: localhost:5000/todo-frontend
    tag: v1.0
    pullPolicy: IfNotPresent  # FR-015

# Rest of configuration same as values.yaml
```

**Or use command-line overrides**:

```bash
helm install todo-chatbot ./helm \
  --set backend.image.repository=localhost:5000/todo-backend \
  --set backend.image.tag=v1.0 \
  --set frontend.image.repository=localhost:5000/todo-frontend \
  --set frontend.image.tag=v1.0
```

---

### T078: Deploy from Registry

```bash
# Deploy using registry images
helm install todo-chatbot ./helm \
  -f helm/values-registry.yaml \
  --wait

# Verify pods are pulling from registry
kubectl get pods -o jsonpath='{.items[*].spec.containers[0].image}'
# Output:
# localhost:5000/todo-backend:v1.0
# localhost:5000/todo-frontend:v1.0

# Check pull status
kubectl describe pod <backend-pod> | grep -A 5 "Image:"
```

---

### T079: Verify imagePullPolicy (FR-015)

```bash
# Verify imagePullPolicy is set to IfNotPresent
kubectl get pods -o jsonpath='{.items[*].spec.containers[0].imagePullPolicy}'
# Output: IfNotPresent IfNotPresent

# Benefits:
# 1. Pod starts faster (no network pull needed)
# 2. Works offline after first pull
# 3. Reduces registry bandwidth
# 4. Supports air-gapped deployments

# Test: Delete and restart pod
kubectl delete pod <backend-pod>
# Pod should restart using cached image

kubectl get pods
# Pod should be Running/Ready within seconds
```

---

## Advanced: Docker Hub Registry

For production deployments:

```bash
# Tag with Docker Hub URL
docker tag todo-backend:latest myusername/todo-backend:v1.0
docker tag todo-frontend:latest myusername/todo-frontend:v1.0

# Push to Docker Hub
docker push myusername/todo-backend:v1.0
docker push myusername/todo-frontend:v1.0

# Configure Minikube for authentication
kubectl create secret docker-registry regcred \
  --docker-server=docker.io \
  --docker-username=myusername \
  --docker-password=mypassword \
  --docker-email=myemail@example.com

# Update Helm deployment to use secret
# Add to backend/frontend container specs:
# imagePullSecrets:
# - name: regcred
```

---

## Checklist

- [ ] T072: Local Docker registry created
- [ ] T073: Backend image tagged
- [ ] T074: Frontend image tagged
- [ ] T075: Backend image pushed to registry
- [ ] T076: Frontend image pushed to registry
- [ ] T077: Helm values updated for registry
- [ ] T078: Deployment from registry verified
- [ ] T079: imagePullPolicy verified as IfNotPresent

---

## Next Steps

1. Test registry with Helm deployment
2. Document registry access credentials (if Docker Hub)
3. Set up automated image builds and pushes (CI/CD)
4. Proceed to Phase 10 (Polish & Documentation)
