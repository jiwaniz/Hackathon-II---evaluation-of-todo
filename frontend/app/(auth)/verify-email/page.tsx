"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useCurrentUser, handleSignOut, authClient } from "@/lib/auth-client";

/**
 * Verify Email page shown to users who haven't verified their email.
 *
 * Users can:
 * - Resend the verification email
 * - Sign out and try a different account
 */
export default function VerifyEmailPage() {
  const { user, isLoading, isEmailVerified } = useCurrentUser();
  const router = useRouter();
  const [resending, setResending] = useState(false);
  const [resendSuccess, setResendSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Redirect to dashboard if already verified
  if (!isLoading && isEmailVerified) {
    router.push("/tasks");
    return null;
  }

  // Redirect to login if not authenticated
  if (!isLoading && !user) {
    router.push("/login");
    return null;
  }

  const handleResendVerification = async () => {
    setResending(true);
    setError(null);
    setResendSuccess(false);

    try {
      await authClient.sendVerificationEmail({
        email: user?.email || "",
        callbackURL: "/tasks",
      });
      setResendSuccess(true);
    } catch (err) {
      setError("Failed to resend verification email. Please try again.");
      console.error("[verify-email] Resend failed:", err);
    } finally {
      setResending(false);
    }
  };

  const handleLogout = async () => {
    await handleSignOut();
    router.push("/login");
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-lg">
        {/* Email icon */}
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
          <svg
            className="h-8 w-8 text-blue-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>

        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900">Verify your email</h1>
          <p className="mt-2 text-gray-600">
            We sent a verification link to:
          </p>
          <p className="mt-1 font-medium text-gray-900">{user?.email}</p>
        </div>

        <div className="rounded-lg bg-yellow-50 p-4">
          <p className="text-sm text-yellow-800">
            Please check your inbox and click the verification link to continue.
            The link will expire in 24 hours.
          </p>
        </div>

        {resendSuccess && (
          <div className="rounded-lg bg-green-50 p-4">
            <p className="text-sm text-green-800">
              Verification email sent! Check your inbox.
            </p>
          </div>
        )}

        {error && (
          <div className="rounded-lg bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="space-y-3">
          <button
            onClick={handleResendVerification}
            disabled={resending}
            className="w-full rounded-lg bg-blue-600 py-2.5 text-white font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {resending ? "Sending..." : "Resend verification email"}
          </button>

          <button
            onClick={handleLogout}
            className="w-full rounded-lg border border-gray-300 bg-white py-2.5 text-gray-700 font-medium hover:bg-gray-50 transition-colors"
          >
            Sign out
          </button>
        </div>

        <p className="text-center text-xs text-gray-500">
          Didn&apos;t receive the email? Check your spam folder or try resending.
        </p>
      </div>
    </div>
  );
}
