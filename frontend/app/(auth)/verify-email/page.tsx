"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState } from "react";

import { resendVerificationEmail } from "@/lib/supabase";

/**
 * Verify Email page shown after registration.
 *
 * No redirects - just shows verification instructions.
 * Users click the verification link in their email to continue.
 */
export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const [resending, setResending] = useState(false);
  const [resendSuccess, setResendSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Get email from URL params (passed from registration)
  // Use optional to avoid conditional rendering issues
  const emailParam = searchParams.get("email") || "";

  const handleResendVerification = async () => {
    if (!emailParam) {
      setError("No email address found. Please register again.");
      return;
    }

    setResending(true);
    setError(null);
    setResendSuccess(false);

    const result = await resendVerificationEmail(emailParam);

    if (result.error) {
      setError("Failed to resend verification email. Please try again.");
      console.error("[verify-email] Resend failed:", result.error);
    } else {
      setResendSuccess(true);
    }

    setResending(false);
  };

  // Show error state if no email
  const showError = !emailParam;

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

        {showError ? (
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">Invalid Link</h1>
            <p className="mt-2 text-gray-600">
              This page requires an email parameter. Please register or login.
            </p>
            <Link
              href="/register"
              className="mt-4 inline-block w-full rounded-lg bg-blue-600 py-2.5 text-white font-medium hover:bg-blue-700 transition-colors"
            >
              Go to Register
            </Link>
          </div>
        ) : (
          <>
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900">Check your email</h1>
              <p className="mt-2 text-gray-600">
                We sent a verification link to:
              </p>
              <p className="mt-1 font-medium text-gray-900">{emailParam}</p>
            </div>

            <div className="rounded-lg bg-blue-50 p-4">
              <p className="text-sm text-blue-800">
                <strong>Important:</strong> You must verify your email before you can log in.
                Click the verification link in your email to activate your account.
              </p>
            </div>

            {resendSuccess && (
              <div className="rounded-lg bg-green-50 p-4">
                <p className="text-sm text-green-800">
                  ✓ Verification email sent! Check your inbox.
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

              <Link
                href="/login"
                className="block w-full rounded-lg border border-gray-300 bg-white py-2.5 text-center text-gray-700 font-medium hover:bg-gray-50 transition-colors"
              >
                Back to Login
              </Link>
            </div>

            <p className="text-center text-xs text-gray-500">
              Didn&apos;t receive the email? Check your spam folder or try resending.
            </p>
          </>
        )}
      </div>
    </div>
  );
}
