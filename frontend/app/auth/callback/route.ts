/**
 * Supabase Auth Callback Route
 *
 * Handles email verification and OAuth callbacks from Supabase.
 * After user clicks verification link in email, Supabase redirects here.
 *
 * NOTE: The HF Space runs on localhost:7860 internally. We hardcode the
 * public Space URL to ensure correct redirects.
 */

import { createClient } from "@/lib/supabase-server";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Public URL of the app - never use requestUrl.origin (it will be localhost inside Docker)
const APP_URL = "https://jiwaniz-to-do-evalution.hf.space";

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);

  const code = requestUrl.searchParams.get("code");
  const error = requestUrl.searchParams.get("error");
  const errorDescription = requestUrl.searchParams.get("error_description");

  // Handle explicit errors from Supabase
  if (error) {
    console.error("[auth/callback] Supabase error:", error, errorDescription);
    return NextResponse.redirect(new URL(`/login?error=${error}`, APP_URL));
  }

  if (code) {
    const supabase = await createClient();
    const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);

    if (!exchangeError) {
      // Session created - redirect to tasks
      return NextResponse.redirect(new URL("/tasks", APP_URL));
    }

    // PKCE verifier missing means the email IS verified (Supabase confirmed it)
    // but the code exchange failed due to session context mismatch.
    // Redirect to login with verified message so user can log in normally.
    if (exchangeError.code === "pkce_code_verifier_not_found") {
      console.log("[auth/callback] Email verified but PKCE session mismatch - redirecting to login");
      return NextResponse.redirect(new URL("/login?verified=true", APP_URL));
    }

    console.error("[auth/callback] Unexpected error:", exchangeError);
    return NextResponse.redirect(new URL("/login?error=verification_failed", APP_URL));
  }

  // No code - email already verified by Supabase, redirect to login
  return NextResponse.redirect(new URL("/login?verified=true", APP_URL));
}
