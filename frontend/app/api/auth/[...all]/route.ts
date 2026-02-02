/**
 * Better Auth API Route Handler for Next.js App Router.
 *
 * This catch-all route handles all Better Auth requests including:
 * - POST /api/auth/sign-up (registration)
 * - POST /api/auth/sign-in (login)
 * - GET /api/auth/session (session check)
 * - POST /api/auth/sign-out (logout)
 */

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

// Export handlers for all HTTP methods
export const { GET, POST } = toNextJsHandler(auth);
