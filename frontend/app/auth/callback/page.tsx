/**
 * Auth Callback Page
 *
 * Shows a loading state while email verification is being processed.
 * The actual verification happens in route.ts which redirects the user.
 */

export default function AuthCallbackPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md space-y-8 text-center">
        {/* Loading spinner */}
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600"></div>

        {/* Title */}
        <h1 className="text-2xl font-semibold text-gray-900">
          Verifying your email...
        </h1>

        {/* Description */}
        <p className="text-sm text-gray-600">
          Please wait while we verify your email address.
          You'll be redirected automatically.
        </p>
      </div>
    </div>
  );
}
