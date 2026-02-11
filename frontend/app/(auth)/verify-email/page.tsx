"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";

import { createClient, resendVerificationEmail, signOut } from "@/lib/supabase";

function VerifyEmailContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get("email") || "";

  const [resending, setResending] = useState(false);
  const [resendSuccess, setResendSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [bannerVisible, setBannerVisible] = useState(true);

  // Poll every 5s to detect if user has verified their email
  useEffect(() => {
    const interval = setInterval(async () => {
      const supabase = createClient();
      const { data } = await supabase.auth.getUser();
      if (data.user?.email_confirmed_at) {
        router.push("/tasks");
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [router]);

  const handleResend = async () => {
    if (!email) return;
    setResending(true);
    setError(null);
    setResendSuccess(false);

    const result = await resendVerificationEmail(email);
    if (result.error) {
      setError("Failed to resend. Please try again.");
    } else {
      setResendSuccess(true);
      setBannerVisible(true);
    }
    setResending(false);
  };

  const handleSignOut = async () => {
    await signOut();
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top notification banner */}
      {bannerVisible && (
        <div className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between bg-blue-600 px-4 py-3 text-white shadow-md">
          <div className="flex items-center gap-3">
            {/* Email icon */}
            <svg className="h-5 w-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <span className="text-sm font-medium">
              Verification email sent to{" "}
              <span className="font-bold">{email || "your email"}</span>.
              Click the link in your email to verify.
            </span>
          </div>
          {/* Dismiss button */}
          <button
            onClick={() => setBannerVisible(false)}
            className="ml-4 shrink-0 rounded p-1 hover:bg-blue-700 transition-colors"
            aria-label="Dismiss"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Main content */}
      <div className={`flex min-h-screen items-center justify-center px-4 ${bannerVisible ? "pt-14" : ""}`}>
        <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-lg">
          {/* Email icon */}
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
            <svg className="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>

          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">Check your email</h1>
            <p className="mt-2 text-gray-600">We sent a verification link to:</p>
            <p className="mt-1 font-semibold text-blue-600">{email || "your email address"}</p>
          </div>

          <div className="rounded-lg bg-yellow-50 p-4">
            <p className="text-sm text-yellow-800">
              Click the link in your email to verify your account.
              This page will automatically redirect once verified.
            </p>
          </div>

          {resendSuccess && (
            <div className="rounded-lg bg-green-50 p-4">
              <p className="text-sm text-green-800">
                ✅ Verification email resent! Check your inbox.
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
              onClick={handleResend}
              disabled={resending}
              className="w-full rounded-lg bg-blue-600 py-2.5 text-white font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {resending ? "Sending..." : "Resend verification email"}
            </button>

            <button
              onClick={handleSignOut}
              className="w-full rounded-lg border border-gray-300 bg-white py-2.5 text-gray-700 font-medium hover:bg-gray-50 transition-colors"
            >
              Sign out
            </button>
          </div>

          <p className="text-center text-xs text-gray-500">
            Didn&apos;t receive the email? Check your spam folder or resend.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
      </div>
    }>
      <VerifyEmailContent />
    </Suspense>
  );
}
