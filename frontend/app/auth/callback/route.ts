/**
 * Supabase Auth Callback Route
 *
 * Handles email verification and OAuth callbacks from Supabase.
 * After user clicks verification link in email, Supabase redirects here.
 */

import { createClient } from "@/lib/supabase-server";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);

  // Use HF Space URL as base, not localhost
  const origin = process.env.BETTER_AUTH_URL || "https://jiwaniz-to-do-evalution.hf.space";

  // Get parameters
  const code = requestUrl.searchParams.get("code");
  const error = requestUrl.searchParams.get("error");
  const errorDescription = requestUrl.searchParams.get("error_description");
  const next = requestUrl.searchParams.get("next") ?? "/login?verified=true";

  // Handle errors from Supabase
  if (error) {
    console.error("[auth/callback] Supabase error:", error, errorDescription);
    return NextResponse.redirect(
      new URL(`/login?error=${error}`, origin)
    );
  }

  // Handle OAuth code exchange (for social logins)
  if (code) {
    const supabase = createClient();

    const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);

    if (!exchangeError) {
      // Successfully verified - redirect to dashboard
      return NextResponse.redirect(new URL("/dashboard", origin));
    }

    console.error("[auth/callback] Error exchanging code:", exchangeError);
    return NextResponse.redirect(
      new URL(`/login?error=verification_failed`, origin)
    );
  }

  // For email verification (no code, verification already done by Supabase)
  // Just redirect to login with success message
  console.log("[auth/callback] Email verification complete, redirecting to login");
  return NextResponse.redirect(new URL("/login?verified=true", origin));
}
