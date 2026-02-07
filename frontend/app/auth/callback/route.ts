/**
 * Supabase Auth Callback Route
 *
 * Handles email verification callbacks from Supabase.
 * When users click the verification link in their email, they're redirected here.
 */

import { createClient } from "@/lib/supabase";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");

  if (code) {
    const supabase = createClient();

    // Exchange the code for a session
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (error) {
      console.error("[auth/callback] Error exchanging code:", error);
      // Redirect to login with error
      return NextResponse.redirect(
        new URL("/login?error=verification_failed", request.url)
      );
    }

    console.log("[auth/callback] Email verified successfully");
    // Redirect to tasks page after successful verification
    return NextResponse.redirect(new URL("/tasks", request.url));
  }

  // No code provided - redirect to login
  return NextResponse.redirect(new URL("/login", request.url));
}
