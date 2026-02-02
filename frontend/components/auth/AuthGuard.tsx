"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useCurrentUser } from "@/lib/auth-client";

interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  /** If true, also requires email to be verified */
  requireVerified?: boolean;
}

/**
 * AuthGuard component that protects routes requiring authentication.
 *
 * Redirects unauthenticated users to the login page.
 * Redirects unverified users to the verify-email page (if requireVerified=true).
 * Shows a loading state while checking authentication.
 *
 * @example
 * ```tsx
 * <AuthGuard requireVerified>
 *   <ProtectedContent />
 * </AuthGuard>
 * ```
 */
export function AuthGuard({ children, fallback, requireVerified = true }: AuthGuardProps) {
  const { user, isLoading, isAuthenticated, isEmailVerified } = useCurrentUser();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push("/login");
      } else if (requireVerified && !isEmailVerified) {
        router.push("/verify-email");
      }
    }
  }, [isLoading, isAuthenticated, isEmailVerified, requireVerified, router]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      fallback || (
        <div className="flex min-h-screen items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
            <p className="text-sm text-gray-500">Loading...</p>
          </div>
        </div>
      )
    );
  }

  // Don't render children if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  // Don't render children if email not verified (when required)
  if (requireVerified && !isEmailVerified) {
    return null;
  }

  return <>{children}</>;
}

export default AuthGuard;
