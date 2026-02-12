/**
 * Next.js catch-all proxy route for FastAPI backend.
 *
 * Forwards all /api/* requests to the FastAPI backend on localhost:8000.
 * This runs server-side, so localhost:8000 is reachable even though
 * the browser can only access port 7860 (the HF Space external port).
 *
 * Specific routes like /api/auth/* take priority over this catch-all.
 */

import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = "http://localhost:8000";

async function proxy(request: NextRequest, params: { path: string[] }) {
  const { path } = await params;
  const pathStr = path.join("/");
  const search = request.nextUrl.search;
  const targetUrl = `${BACKEND_URL}/api/${pathStr}${search}`;

  // Forward Authorization and Content-Type headers
  const headers: Record<string, string> = {};
  const auth = request.headers.get("Authorization");
  if (auth) headers["Authorization"] = auth;
  const contentType = request.headers.get("Content-Type");
  if (contentType) headers["Content-Type"] = contentType;

  const hasBody = request.method !== "GET" && request.method !== "HEAD";
  const body = hasBody ? await request.arrayBuffer() : undefined;

  try {
    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body,
    });

    const data = await response.arrayBuffer();
    return new NextResponse(data, {
      status: response.status,
      headers: { "Content-Type": response.headers.get("Content-Type") || "application/json" },
    });
  } catch (error) {
    console.error("[api-proxy] Backend unreachable:", targetUrl, error);
    return NextResponse.json(
      { error: { code: "BACKEND_UNREACHABLE", message: "Backend service unavailable" } },
      { status: 503 }
    );
  }
}

export async function GET(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return proxy(request, await params);
}

export async function POST(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return proxy(request, await params);
}

export async function PUT(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return proxy(request, await params);
}

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return proxy(request, await params);
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  return proxy(request, await params);
}
