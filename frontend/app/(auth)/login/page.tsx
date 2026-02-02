"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

import { LoginForm } from "@/components/auth/LoginForm";

/**
 * Inner login content that uses search params.
 * Wrapped in Suspense for Next.js 16+ compatibility.
 */
function LoginContent() {
  const searchParams = useSearchParams();
  const isSessionExpired = searchParams.get("expired") === "true";

  return (
    <div className="w-full max-w-md space-y-8">
      {/* Session expired message (T140) */}
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
