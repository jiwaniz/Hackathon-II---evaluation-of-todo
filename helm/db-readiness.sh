#!/bin/bash
# Database Readiness Check Init Container Script
# Purpose: Validate Neon PostgreSQL connectivity before FastAPI startup (FR-019)
# Usage: Called as init container in backend deployment
# This prevents CrashLoopBackOff when database is temporarily unavailable

set -e

# Configuration from environment variables
DB_HOST=${DB_HOST:-neon.tech}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-}
DB_USER=${DB_USER:-}
MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_INTERVAL=${RETRY_INTERVAL:-2}

echo "[$(date)] Starting database readiness check..."
echo "Checking connectivity to PostgreSQL at ${DB_HOST}:${DB_PORT}"

# Retry logic: Try to connect MAX_RETRIES times with RETRY_INTERVAL seconds between attempts
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" 2>/dev/null; then
    echo "[$(date)] ✓ Database is ready"
    echo "[$(date)] Init container completed successfully"
    exit 0
  fi

  RETRY_COUNT=$((RETRY_COUNT + 1))
  REMAINING=$((MAX_RETRIES - RETRY_COUNT))

  if [ $REMAINING -gt 0 ]; then
    echo "[$(date)] Database not ready. Retrying... ($REMAINING attempts remaining)"
    sleep "$RETRY_INTERVAL"
  fi
done

# If we get here, database connectivity failed after all retries
echo "[$(date)] ✗ Failed to connect to database after $MAX_RETRIES attempts"
echo "[$(date)] This init container will exit with code 1, causing the pod to fail"
echo "[$(date)] The Kubernetes controller will retry the pod with exponential backoff"
exit 1
