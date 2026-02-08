/**
 * Supabase Auth Callback Route
 *
 * Handles email verification and other auth callbacks from Supabase.
 * After user clicks verification link in email, Supabase redirects here.
 */

import { createClient } from "@/lib/supabase";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get("code");
  const next = requestUrl.searchParams.get("next") ?? "/dashboard";

  if (code) {
    const supabase = createClient();

    // Exchange the code for a session
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (!error) {
      // Successfully verified - redirect to dashboard or specified page
      return NextResponse.redirect(new URL(next, requestUrl.origin));
    }

    console.error("[auth/callback] Error exchanging code:", error);
    // If error, redirect to login with error message
    return NextResponse.redirect(
      new URL(`/login?error=verification_failed`, requestUrl.origin)
    );
  }

  // No code provided - redirect to login
  return NextResponse.redirect(new URL("/login", requestUrl.origin));
}
