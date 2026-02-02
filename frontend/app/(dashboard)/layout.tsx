"use client";

import Link from "next/link";

import { AuthGuard } from "@/components/auth/AuthGuard";
import { UserMenu } from "@/components/auth/UserMenu";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

/**
 * Protected dashboard layout with navigation and user menu.
 *
 * Wraps all dashboard pages in AuthGuard to ensure authentication.
 * Provides consistent header with navigation and user menu.
 */
export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="sticky top-0 z-10 border-b border-gray-200 bg-white">
          <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
            {/* Logo/Brand */}
            <Link href="/tasks" className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-gray-900">
                Evolution of <span className="text-blue-600">Todo</span>
              </h1>
            </Link>

            {/* Navigation */}
            <nav className="hidden items-center gap-6 md:flex">
              <Link
                href="/tasks"
                className="text-sm font-medium text-gray-700 transition-colors hover:text-blue-600"
              >
                My Tasks
              </Link>
            </nav>

            {/* User menu */}
            <UserMenu />
          </div>
        </header>

        {/* Main content */}
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </AuthGuard>
  );
}
