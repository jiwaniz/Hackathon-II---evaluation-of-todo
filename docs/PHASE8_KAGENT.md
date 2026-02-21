# Phase 8: kagent Integration Implementation Guide

**Tasks**: T066-T071
**User Story**: US6 - kagent Integration (P2)
**Status**: Implementation Guide (requires kagent tool)

## Overview

Phase 8 enables cluster health analysis and optimization recommendations via `kagent`. kagent analyzes resource usage, identifies bottlenecks, and provides actionable optimization suggestions aligned with FR-014 resource limits.

## Prerequisites

- **Minikube cluster** running with todo-chatbot deployed
- **kubectl** configured and working
- **kagent** installed (available from Krew plugin manager)
- **Metrics Server** running (for resource usage data)
- **Health checks** from Phase 6 operational

---

## Task Breakdown

### T066: Verify kagent Installation

**Steps**:

1. **Install Krew** (Kubernetes plugin manager):
   ```bash
   # Check if Krew is installed
   kubectl krew version

   # If not, install Krew
   (
     set -x; cd "$(mktemp -d)" &&
     OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
     ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/arm.*$/arm/')" &&
     KREW="krew-${OS}_${ARCH}" &&
     curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
     tar zxf "${KREW}.tar.gz" &&
     ./"${KREW}" install krew
   )
   ```

2. **Install kagent via Krew**:
   ```bash
   kubectl krew install krew-ai
   # or
   kubectl krew install kagent
   ```

3. **Verify installation**:
   ```bash
   kubectl kagent --version
   # Output: kagent version X.Y.Z
   ```

4. **Verify Metrics Server** (required for resource analysis):
   ```bash
   kubectl get deployment metrics-server -n kube-system
   # If not installed, install via Minikube addon:
   minikube addons enable metrics-server

   # Wait for metrics to be available
   kubectl top nodes
   kubectl top pods
   ```

---

### T067: Test kagent Cluster Analysis

**Objective**: Get AI-generated cluster health analysis

**Steps**:

1. **Ensure cluster is running with pods**:
   ```bash
   kubectl get pods
   # Should show: todo-backend and todo-frontend pods running
   ```

2. **Request cluster health analysis**:
   ```bash
   kubectl kagent "analyze the cluster health"
   # kagent outputs:
   # - Overall cluster status (healthy/degraded/critical)
   # - Pod health summary
   # - Resource utilization (CPU, memory)
   # - Current issues or warnings
   # - Recommendations
   ```

3. **Example output**:
   ```
   Cluster Health Analysis
   =======================
   Overall Status: HEALTHY

   Pods:
   - todo-backend: Running (1/1 Ready)
   - todo-frontend: Running (1/1 Ready)

   Resource Usage:
   - CPU: 125m/2000m (6%)
   - Memory: 384Mi/4096Mi (9%)

   Warnings:
   - None detected

   Recommendations:
   - Current resource allocation is optimal
   - Consider increasing replicas for HA
   ```

4. **Deep dive analysis**:
   ```bash
   kubectl kagent "what are the resource bottlenecks in the cluster?"
   # kagent analyzes and reports:
   # - Highest CPU consumers
   # - Highest memory consumers
   # - Pods near resource limits
   # - Optimization suggestions
   ```

---

### T068: Test kagent Optimization

**Objective**: Get resource allocation optimization recommendations

**Steps**:

1. **Request optimization suggestions**:
   ```bash
   kubectl kagent "optimize resource allocation for the cluster"
   # kagent analyzes current usage patterns and provides suggestions
   ```

2. **Example optimization recommendations**:
   ```
   Resource Optimization Recommendations
   =====================================

   Current Allocation:
   - Backend: 200m CPU / 512Mi memory (request), 500m/1Gi (limit)
   - Frontend: 100m CPU / 256Mi memory (request), 300m/512Mi (limit)

   Analysis:
   - Backend average usage: 75m CPU, 280Mi memory (37.5% of request)
   - Frontend average usage: 25m CPU, 128Mi memory (50% of request)

   Recommendations:
   1. Reduce backend CPU request to 100m (currently over-allocated)
   2. Increase frontend memory limit to 768Mi (near limit at 128Mi usage)
   3. Add horizontal pod autoscaling (HPA) for automatic scaling
   4. Implement memory caching to reduce database queries

   Expected Impact:
   - Cost reduction: ~15% (fewer unused resources)
   - Performance improvement: ~20% (from caching)
   - Stability improvement: ~10% (less memory pressure)
   ```

3. **Get specific recommendations**:
   ```bash
   # Ask about specific service
   kubectl kagent "what CPU and memory should the backend use?"

   # Ask about scaling
   kubectl kagent "should I scale the frontend horizontally or vertically?"

   # Ask about efficiency
   kubectl kagent "how can I reduce resource waste in this cluster?"
   ```

---

### T069: Verify Resource Recommendations

**Objective**: Compare kagent suggestions with current FR-014 limits

**Current Resource Allocation** (from `helm/values.yaml`):

**Backend**:
- Request: 200m CPU, 512Mi memory
- Limit: 500m CPU, 1Gi memory

**Frontend**:
- Request: 100m CPU, 256Mi memory
- Limit: 300m CPU, 512Mi memory

**Verification Steps**:

1. **Check current allocation**:
   ```bash
   kubectl get pods -o=jsonpath='{.items[*].spec.containers[0].resources}'
   # Output shows request/limit for each pod
   ```

2. **Check actual usage**:
   ```bash
   kubectl top pods
   # Output:
   # NAME                                CPU(cores)   MEMORY(bytes)
   # todo-backend-64f5d5b4f-xxxxx       75m          280Mi
   # todo-frontend-7d9c8f9f8-xxxxx      25m          128Mi
   ```

3. **Calculate utilization rates**:
   ```bash
   # Backend: 75m / 200m = 37.5% of request
   # Frontend: 25m / 100m = 25% of request
   # Overall: Well-provisioned with headroom
   ```

4. **Document findings**:
   ```markdown
   ## Resource Utilization Report

   | Service | CPU Request | CPU Actual | CPU Usage % | Memory Request | Memory Actual | Memory Usage % |
   |---------|-------------|-----------|-----------|----------------|--------------|----------------|
   | Backend | 200m | 75m | 37.5% | 512Mi | 280Mi | 54.7% |
   | Frontend | 100m | 25m | 25% | 256Mi | 128Mi | 50% |

   ### Observations:
   - CPU is under-utilized (37.5% for backend, 25% for frontend)
   - Memory usage is balanced (54.7%, 50%)
   - No pods hitting limits
   - Cluster has capacity for 2-3x current load

   ### Recommendations from kagent:
   - ✅ Current allocation appropriate for this workload size
   - Consider horizontal scaling (add replicas) before vertical (increase limits)
   - Monitor memory usage for frontend (approaching 50% of request)
   ```

---

### T070: Document kagent Setup

Create comprehensive kagent setup guide:

**File**: `docs/KAGENT_SETUP.md`

```markdown
# kagent Setup and Usage Guide

## Installation

### Prerequisites
- kubectl configured and connected to Minikube cluster
- curl or package manager available
- Metrics Server running in cluster

### Install kagent via Krew

1. **Install Krew** (if not already installed):
   ```bash
   (
     set -x; cd "$(mktemp -d)" &&
     OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
     ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/arm.*$/arm/')" &&
     KREW="krew-${OS}_${ARCH}" &&
     curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
     tar zxf "${KREW}.tar.gz" &&
     ./"${KREW}" install krew
   )
   ```

2. **Install kagent**:
   ```bash
   kubectl krew install krew-ai
   # or
   kubectl krew install kagent
   ```

3. **Verify installation**:
   ```bash
   kubectl kagent --version
   ```

## Prerequisites: Metrics Server

kagent requires Kubernetes Metrics Server for resource usage data:

```bash
# Check if Metrics Server is running
kubectl get deployment metrics-server -n kube-system

# If not, install via Minikube addon
minikube addons enable metrics-server

# Wait for metrics to be available (may take 60-90 seconds)
kubectl top nodes
kubectl top pods
```

## Configuration

kagent uses your kubectl context and doesn't require additional API keys. It analyzes local cluster data.

## Example Commands

### 1. Cluster Health Analysis
```bash
kubectl kagent "analyze the cluster health"
# kagent outputs:
# - Overall cluster status
# - Pod health summary
# - Resource utilization
# - Any issues or warnings
```

### 2. Resource Bottleneck Analysis
```bash
kubectl kagent "what are the resource bottlenecks?"
# kagent identifies:
# - Highest CPU consumers
# - Highest memory consumers
# - Pods near limits
```

### 3. Optimization Recommendations
```bash
kubectl kagent "optimize resource allocation"
# kagent provides:
# - Specific request/limit recommendations
# - Scaling suggestions (horizontal vs vertical)
# - Cost optimization advice
```

### 4. Service-Specific Analysis
```bash
kubectl kagent "analyze the backend deployment"
# kagent focuses on todo-backend resources and performance
```

### 5. Scaling Recommendations
```bash
kubectl kagent "how many replicas should the frontend have?"
# kagent considers:
# - Current load
# - Resource constraints
# - High availability requirements
```

## Advanced Usage

### Compare Recommendations with Current

```bash
# Get current resource allocation
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].resources}{"\n"}{end}'

# Get actual usage
kubectl top pods

# Ask kagent
kubectl kagent "should I adjust these resource limits based on actual usage?"
```

### Monitor Over Time

```bash
# Create baseline
kubectl top pods > baseline.txt

# Wait 1 hour
sleep 3600

# Create comparison
kubectl top pods > current.txt

# Ask kagent
kubectl kagent "compare these two resource snapshots and recommend optimizations"
# Provide both files for analysis
```

## Integration with Phase 4 MVP

kagent analyzes the todo-chatbot deployed from Phase 4 Helm chart:

- **Deployment 1**: todo-backend (FR-014: 200m/512Mi request, 500m/1Gi limit)
- **Deployment 2**: todo-frontend (FR-014: 100m/256Mi request, 300m/512Mi limit)
- **Services**: ClusterIP services for backend and frontend
- **Init Container**: Database readiness check (no resource overhead)

## Typical Output

```
=== Cluster Health Report ===

Cluster Status: HEALTHY
Last Updated: 2026-02-21 15:30:45 UTC

Nodes:
  - minikube: Ready (CPU: 2000m, Memory: 4096Mi)

Pods:
  Running:
    - todo-backend-64f5d5b4f-xxxxx (1/1 Ready)
    - todo-frontend-7d9c8f9f8-xxxxx (1/1 Ready)

  Resource Usage:
    - Total CPU: 100m / 2000m (5%)
    - Total Memory: 408Mi / 4096Mi (10%)

Recommendations:
  1. Scale horizontally for resilience (add pod replicas)
  2. Increase frontend memory limit monitoring
  3. Implement HPA for automatic scaling
  4. Configure network policies for security

Risk Assessment: LOW
  - No pods hitting resource limits
  - Cluster has 3-4x capacity headroom
  - All services are healthy
```

## Troubleshooting

### "Metrics not available"
```bash
# Metrics Server may not be ready
kubectl rollout status deployment/metrics-server -n kube-system

# If not deployed
minikube addons enable metrics-server

# Wait for metrics
watch -n 2 'kubectl top pods'
```

### "kagent command not found"
```bash
# Verify installation
kubectl krew list | grep kagent

# Reinstall if needed
kubectl krew uninstall kagent
kubectl krew install kagent
```

### "No recommendations generated"
```bash
# kagent may need more data
# Run workload for 5-10 minutes to generate metrics

# Trigger some activity
for i in {1..100}; do
  curl http://localhost:3000/api/health
done

# Wait 30 seconds for metrics to update
sleep 30

# Try analysis again
kubectl kagent "analyze resource usage"
```

## Best Practices

1. **Run regularly** - Schedule weekly analysis for trend monitoring
2. **Act on recommendations** - Implement high-impact suggestions
3. **Test changes** - Use Minikube for testing before production
4. **Monitor impact** - Check metrics after implementing changes
5. **Keep notes** - Document what recommendations were implemented and results
```

---

### T071: Create Baseline Metrics

**Objective**: Document initial cluster resource usage before and after optimizations

**Steps**:

1. **Create initial baseline**:
   ```bash
   # Capture current state
   mkdir -p docs/metrics

   # Get pod resources
   kubectl describe pods > docs/metrics/pods-initial.txt

   # Get current resource usage
   kubectl top pods > docs/metrics/usage-initial.txt

   # Get deployment specs
   kubectl get deployments -o yaml > docs/metrics/deployments-initial.yaml

   # Timestamp
   date > docs/metrics/baseline-timestamp.txt
   ```

2. **Document findings**:
   ```markdown
   # Cluster Baseline Metrics (2026-02-21 15:30 UTC)

   ## Current Resource Allocation

   ### Backend Deployment
   - Replicas: 1
   - CPU Request: 200m
   - CPU Limit: 500m
   - Memory Request: 512Mi
   - Memory Limit: 1Gi

   ### Frontend Deployment
   - Replicas: 1
   - CPU Request: 100m
   - CPU Limit: 300m
   - Memory Request: 256Mi
   - Memory Limit: 512Mi

   ## Actual Usage

   | Pod | CPU | Memory | CPU % | Memory % |
   |-----|-----|--------|-------|----------|
   | todo-backend | 75m | 280Mi | 37.5% | 54.7% |
   | todo-frontend | 25m | 128Mi | 25% | 50% |

   ## Cluster Capacity

   | Resource | Total | Used | Available | Utilization |
   |----------|-------|------|-----------|-------------|
   | CPU | 2000m | 100m | 1900m | 5% |
   | Memory | 4096Mi | 408Mi | 3688Mi | 10% |

   ## kagent Recommendations

   1. Horizontal scaling is preferred over vertical
   2. Monitor frontend memory (approaching request)
   3. Implement HPA for automatic scaling
   4. Add pod affinity rules for better distribution

   ## Next Steps

   1. Test scaling to 2 replicas
   2. Monitor resource usage under load
   3. Implement HPA configuration
   4. Re-run analysis after 1 week
   ```

3. **Ongoing monitoring**:
   ```bash
   # Create monitoring script
   cat > docs/metrics/monitor.sh << 'EOF'
   #!/bin/bash
   TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

   echo "=== Metrics at $TIMESTAMP ===" >> docs/metrics/history.log
   kubectl top pods >> docs/metrics/history.log
   echo "" >> docs/metrics/history.log

   # Also save full snapshot
   kubectl get pods -o json > docs/metrics/pods-$TIMESTAMP.json
   EOF

   chmod +x docs/metrics/monitor.sh

   # Run periodically (e.g., every hour)
   watch -n 3600 ./docs/metrics/monitor.sh
   ```

---

## Checklist

- [ ] T066: kagent installation verified
- [ ] T067: Cluster analysis test passed
- [ ] T068: Optimization test passed
- [ ] T069: Resource recommendations verified against current allocation
- [ ] T070: Setup documentation created (docs/KAGENT_SETUP.md)
- [ ] T071: Baseline metrics documented (docs/metrics/baseline-*)

---

## Next Steps

1. **Run all kagent analyses** in Minikube
2. **Document optimization recommendations**
3. **Implement high-impact changes** (e.g., HPA)
4. **Monitor results** over 1-2 weeks
5. **Proceed to Phase 9** (Container Registry)

---

## Files Created/Modified

- ✅ `docs/KAGENT_SETUP.md` - Comprehensive setup guide
- ✅ `docs/metrics/` - Directory for baseline and ongoing metrics
- 🔄 `docs/DEPLOYMENT.md` - May include kagent section
