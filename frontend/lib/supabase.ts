/**
 * Supabase client configuration for Phase 3 authentication.
 *
 * Provides email/password authentication with mandatory email verification.
 */

import { createBrowserClient } from "@supabase/ssr";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export function createClient() {
  return createBrowserClient(supabaseUrl, supabaseAnonKey);
}

/**
 * Get the current Supabase auth token for API calls.
 */
export async function getSupabaseToken(): Promise<string | null> {
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();
  return session?.access_token ?? null;
}

/**
 * Sign up a new user with email and password.
 * Sends email verification link automatically (mandatory).
 */
export async function signUp(email: string, password: string, name?: string) {
  const supabase = createClient();

  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        name: name || "",
      },
      // Email verification required - redirect back to app after verification
      emailRedirectTo: `${typeof window !== 'undefined' ? window.location.origin : ''}/auth/callback`,
    },
  });

  if (error) {
    console.error("[supabase] Sign up error:", error);
    return { user: null, session: null, error };
  }

  console.log("[supabase] Sign up successful - verification email sent");
  return { user: data.user, session: data.session, error: null };
}

/**
 * Sign in with email and password.
 * Requires email to be verified.
 */
export async function signInWithPassword(email: string, password: string) {
  const supabase = createClient();

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    console.error("[supabase] Sign in error:", error);
    return { user: null, session: null, error };
  }

  console.log("[supabase] Sign in successful");
  return { user: data.user, session: data.session, error: null };
}

/**
 * Sign out the current user.
 */
export async function signOut() {
  const supabase = createClient();
  const { error } = await supabase.auth.signOut();

  if (error) {
    console.error("[supabase] Sign out error:", error);
  }

  return { error };
}

/**
 * Resend verification email.
 */
export async function resendVerificationEmail(email: string) {
  const supabase = createClient();

  const { error } = await supabase.auth.resend({
    type: "signup",
    email,
    options: {
      emailRedirectTo: `${typeof window !== 'undefined' ? window.location.origin : ''}/auth/callback`,
    },
  });

  if (error) {
    console.error("[supabase] Resend verification error:", error);
    return { error };
  }

  console.log("[supabase] Verification email sent");
  return { error: null };
}

/**
 * Get current user session.
 */
export async function getSession() {
  const supabase = createClient();
  const { data, error } = await supabase.auth.getSession();

  if (error) {
    console.error("[supabase] Error getting session:", error);
    return null;
  }

  return data.session;
}

/**
 * Get current user.
 */
export async function getUser() {
  const session = await getSession();
  return session?.user ?? null;
}
