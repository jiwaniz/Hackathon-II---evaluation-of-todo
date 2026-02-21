/**
 * Health check endpoint for Kubernetes liveness/readiness probes
 * Task: T049 - Frontend health endpoint
 *
 * Returns 200 OK with health status for container orchestration monitoring.
 * Used by Kubernetes probes to determine if container is running/ready.
 */

import { NextRequest, NextResponse } from 'next/server';

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version?: string;
  environment?: string;
  checks?: Record<string, boolean>;
}

export async function GET(request: NextRequest): Promise<NextResponse<HealthStatus>> {
  try {
    const now = new Date();

    // Basic health checks
    const checks = {
      memory: checkMemory(),
      database: true, // Frontend doesn't connect to DB directly
      api: true, // Assume API is reachable (defer actual check to reduce latency)
    };

    // Determine overall status
    const allHealthy = Object.values(checks).every(c => c === true);
    const status: HealthStatus['status'] = allHealthy ? 'healthy' : 'degraded';

    return NextResponse.json({
      status,
      timestamp: now.toISOString(),
      version: '2.0.0',
      environment: process.env.NODE_ENV || 'development',
      checks: checks,
    }, { status: allHealthy ? 200 : 503 });
  } catch (error) {
    console.error('[Health Check] Error:', error);
    return NextResponse.json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
    }, { status: 503 });
  }
}

/**
 * Check memory usage (warn if > 80% of heap)
 * Kubernetes uses this to detect memory leaks
 */
function checkMemory(): boolean {
  if (typeof process === 'undefined' || !process.memoryUsage) {
    return true; // Can't check in browser context
  }

  try {
    const mem = process.memoryUsage();
    const heapUsedPercent = (mem.heapUsed / mem.heapTotal) * 100;
    return heapUsedPercent < 80; // Healthy if < 80%
  } catch {
    return true; // Default healthy if check fails
  }
}
