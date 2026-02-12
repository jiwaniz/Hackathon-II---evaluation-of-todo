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
  const url = `${BACKEND_URL}/api/${pathStr}${search}`;

  // Forward Authorization and Content-Type headers
  const headers: Record<string, string> = {};
  const auth = request.headers.get("Authorization");
  if (auth) headers["Authorization"] = auth;
  const contentType = request.headers.get("Content-Type");
  if (contentType) headers["Content-Type"] = contentType;

  // Read body as text for non-GET methods (avoids detached ArrayBuffer issue)
  const hasBody = request.method !== "GET" && request.method !== "HEAD";
  const bodyText = hasBody ? await request.text() : undefined;

  // Try the URL as-is first; if we get a 307 redirect, follow it manually
  // preserving the body (Node.js fetch drops the body on redirect)
  async function doFetch(targetUrl: string): Promise<Response> {
    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body: bodyText,
      redirect: "manual",
    });

    // Manually follow 307/308 redirects to preserve body
    if (response.status === 307 || response.status === 308) {
      const location = response.headers.get("Location");
      if (location) {
        const redirectUrl = location.startsWith("http")
          ? location
          : `${BACKEND_URL}${location}`;
        return fetch(redirectUrl, {
          method: request.method,
          headers,
          body: bodyText,
          redirect: "manual",
        });
      }
    }

    return response;
  }

  try {
    const response = await doFetch(url);

    const data = await response.arrayBuffer();
    return new NextResponse(Buffer.from(data), {
      status: response.status,
      headers: { "Content-Type": response.headers.get("Content-Type") || "application/json" },
    });
  } catch (error) {
    console.error("[api-proxy] Backend unreachable:", url, error);
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
