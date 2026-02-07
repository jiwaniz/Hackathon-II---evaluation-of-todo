/**
 * Better Auth client-side hooks and utilities.
 *
 * This file provides React hooks for authentication state management
 * and client-side auth operations.
 */

"use client";

import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client instance.
 *
 * Provides hooks for:
 * - useSession: Get current user session
 * - signIn: Sign in with email/password
 * - signUp: Register new user
 * - signOut: Sign out current user
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

// Export individual hooks for convenience
export const {
  useSession,
  signIn,
  signUp,
  signOut,
} = authClient;

/**
 * Hook to get the current user from session.
 *
 * @returns Object with user data, loading state, and verification status
 *
 * @example
 * ```tsx
 * const { user, isLoading, isEmailVerified } = useCurrentUser();
 * if (isLoading) return <Loading />;
 * if (!user) return <LoginPrompt />;
 * if (!isEmailVerified) return <VerifyEmailPrompt />;
 * return <Dashboard user={user} />;
 * ```
 */
export function useCurrentUser() {
  const { data: session, isPending } = useSession();

  return {
    user: session?.user ?? null,
    isLoading: isPending,
    isAuthenticated: !!session?.user,
    isEmailVerified: session?.user?.emailVerified ?? false,
  };
}

/**
 * Sign in with email and password.
 *
 * @param email - User email
 * @param password - User password
 * @returns Promise resolving to session data or error
 *
 * @example
 * ```tsx
 * const result = await signInWithEmail("user@example.com", "password");
 * if (result.error) {
 *   console.error(result.error);
 * } else {
 *   router.push("/tasks");
 * }
 * ```
 */
export async function signInWithEmail(email: string, password: string) {
  return signIn.email({
    email,
    password,
  });
}

/**
 * Register a new user with email and password.
 *
 * @param email - User email
 * @param password - User password
 * @param name - Optional display name
 * @returns Promise resolving to session data or error
 *
 * @example
 * ```tsx
 * const result = await registerWithEmail("user@example.com", "password", "John");
 * if (result.error) {
 *   console.error(result.error);
 * } else {
 *   router.push("/tasks");
 * }
 * ```
 */
export async function registerWithEmail(
  email: string,
  password: string,
  name?: string
) {
  return signUp.email({
    email,
    password,
    name: name ?? "",
  });
}

/**
 * Sign out the current user.
 *
 * @returns Promise resolving when sign out is complete
 *
 * @example
 * ```tsx
 * await handleSignOut();
 * router.push("/");
 * ```
 */
export async function handleSignOut() {
  return signOut();
}

/**
 * Get the session token for API calls to the backend.
 * The backend validates this by querying the shared session table.
 *
 * @returns The session token or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    const result = await authClient.getSession();
    const session = result?.data;
    const token = session?.session?.token || (session as { token?: string })?.token;
    return token || null;
  } catch (err) {
    console.error("[auth-client] Error getting session token:", err);
    return null;
  }
}
