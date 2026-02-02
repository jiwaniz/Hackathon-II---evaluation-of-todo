/**
 * Debug endpoint to check session and token.
 * DELETE THIS FILE after debugging.
 */

import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const headersList = await headers();
    const session = await auth.api.getSession({
      headers: headersList,
    });

    return NextResponse.json({
      hasSession: !!session,
      session: session ? {
        userId: session.user?.id,
        userEmail: session.user?.email,
        sessionId: session.session?.id,
        sessionToken: session.session?.token?.substring(0, 20) + '...',
        // Check if there's a JWT
        keys: Object.keys(session),
        sessionKeys: session.session ? Object.keys(session.session) : [],
        userKeys: session.user ? Object.keys(session.user) : [],
      } : null,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    return NextResponse.json({ error: message });
  }
}
