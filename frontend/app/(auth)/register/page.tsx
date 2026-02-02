import Link from "next/link";

import { RegisterForm } from "@/components/auth/RegisterForm";

export const metadata = {
  title: "Register - Evolution of Todo",
  description: "Create your Evolution of Todo account",
};

/**
 * Registration page with centered form layout.
 */
export default function RegisterPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        {/* Header */}
        <div className="text-center">
          <Link href="/" className="inline-block">
            <h1 className="text-3xl font-bold text-gray-900">
              Evolution of <span className="text-blue-600">Todo</span>
            </h1>
          </Link>
          <h2 className="mt-6 text-2xl font-semibold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Start organizing your tasks today.
          </p>
        </div>

        {/* Register form card */}
        <div className="rounded-xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
          <RegisterForm />
        </div>
      </div>
    </div>
  );
}
