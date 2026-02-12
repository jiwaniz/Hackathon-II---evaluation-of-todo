"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect } from "react";

import { LoginForm } from "@/components/auth/LoginForm";
import { useCurrentUser } from "@/lib/supabase";

/**
 * Inner login content that uses search params.
 * Wrapped in Suspense for Next.js 16+ compatibility.
 */
function LoginContent() {
  const { isAuthenticated, isLoading } = useCurrentUser();
  const router = useRouter();

  // Redirect already-authenticated users to tasks
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace("/tasks");
    }
  }, [isLoading, isAuthenticated, router]);
  const searchParams = useSearchParams();
  const isSessionExpired = searchParams.get("expired") === "true";
  const isVerified = searchParams.get("verified") === "true";

  return (
    <div className="w-full max-w-md space-y-8">
      {/* Email verified success message */}
      {isVerified && (
        <div className="p-4 text-sm text-green-700 bg-green-50 border border-green-200 rounded-md">
          ✅ Email verified successfully! You can now sign in.
        </div>
      )}

      {/* Session expired message */}
      {isSessionExpired && (
        <div className="p-4 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-md">
          Your session has expired. Please sign in again.
        </div>
      )}

      {/* Header */}
      <div className="text-center">
        <Link href="/" className="inline-block">
          <h1 className="text-3xl font-bold text-gray-900">
            Evolution of <span className="text-blue-600">Todo</span>
          </h1>
        </Link>
        <h2 className="mt-6 text-2xl font-semibold text-gray-900">
          Sign in to your account
        </h2>
        <p className="mt-2 text-sm text-gray-600">
          Welcome back! Please enter your credentials.
        </p>
      </div>

      {/* Login form card */}
      <div className="rounded-xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
        <LoginForm />
      </div>
    </div>
  );
}

/**
 * Login page with centered form layout.
 */
export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <Suspense fallback={<div className="w-full max-w-md text-center">Loading...</div>}>
        <LoginContent />
      </Suspense>
    </div>
  );
}
