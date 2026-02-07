/**
 * Better Auth server-side configuration with Email Verification.
 *
 * This file configures Better Auth for the Next.js backend (API routes).
 * Email verification is required before users can access the dashboard.
 *
 * IMPORTANT: BETTER_AUTH_SECRET must be shared with the FastAPI backend
 * for session verification to work correctly.
 */

import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Database URL - hardcoded for debugging (move back to env var after fixing)
const DATABASE_URL = process.env.DATABASE_URL || "postgresql://neondb_owner:npg_VCELyK9WR3gP@ep-falling-bar-a199lzbj-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require";

// PostgreSQL connection pool for Better Auth
const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

// Log for debugging
console.log("[auth.ts] DATABASE_URL available:", !!DATABASE_URL);

// Secret - hardcoded for debugging
const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET || "ca8f2ce4221abe0bce15b86930d22ee86b7ca24ab4a4b2c8e6d51190deae9b82";
console.log("[auth.ts] BETTER_AUTH_SECRET available:", !!BETTER_AUTH_SECRET);

// Resend API key for email verification
const RESEND_API_KEY = process.env.RESEND_API_KEY;
console.log("[auth.ts] RESEND_API_KEY available:", !!RESEND_API_KEY);

/**
 * Send email using Resend API.
 * Falls back to console logging if RESEND_API_KEY is not set (dev mode).
 */
async function sendEmail({
  to,
  subject,
  html,
}: {
  to: string;
  subject: string;
  html: string;
}) {
  console.log("[auth.ts] sendEmail called for:", to);

  // Development mode: log to console if no API key
  if (!RESEND_API_KEY) {
    console.log("\n========== EMAIL VERIFICATION (DEV MODE) ==========");
    console.log(`To: ${to}`);
    console.log(`Subject: ${subject}`);
    console.log(`Body: ${html}`);
    console.log("====================================================\n");
    return;
  }

  // Production mode: send via Resend
  try {
    console.log("[auth.ts] Sending email via Resend...");
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: process.env.EMAIL_FROM || "Todo App <onboarding@resend.dev>",
        to,
        subject,
        html,
      }),
    });

    const responseText = await response.text();
    console.log("[auth.ts] Resend response:", response.status, responseText);

    if (!response.ok) {
      console.error("[auth.ts] Failed to send email:", responseText);
      // Don't throw - let signup continue even if email fails
      // The user can resend verification later
    } else {
      console.log("[auth.ts] Email sent successfully!");
    }
  } catch (error) {
    console.error("[auth.ts] Email sending error:", error);
    // Don't throw - let signup continue
  }
}

/**
 * Better Auth instance configured with email verification.
 *
 * Features:
 * - Email/password authentication
 * - Email verification required
 * - Session-based auth (7 days)
 * - PostgreSQL database storage via Neon
 */
export const auth = betterAuth({
  // Use environment variable for the secret
  secret: BETTER_AUTH_SECRET,

  // Base URL for auth endpoints
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // PostgreSQL database adapter for user and session storage
  database: pool,

  // Email/password authentication with verification
  emailAndPassword: {
    enabled: true,
    // Password requirements
    minPasswordLength: 8,
    // Allow login without email verification (optional verification)
    requireEmailVerification: false,
  },

  // Email verification configuration
  emailVerification: {
    // Send verification email on signup
    sendOnSignUp: true,
    // Auto-signin after verification
    autoSignInAfterVerification: true,
    // Custom email sender
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email - Todo App",
        html: `
          <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #2563eb;">Verify your email</h1>
            <p>Hi ${user.name || "there"},</p>
            <p>Thanks for signing up! Please verify your email address by clicking the button below:</p>
            <a href="${url}" style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 16px 0;">
              Verify Email
            </a>
            <p>Or copy and paste this link into your browser:</p>
            <p style="color: #6b7280; word-break: break-all;">${url}</p>
            <p>This link will expire in 24 hours.</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;" />
            <p style="color: #9ca3af; font-size: 12px;">If you didn't create an account, you can safely ignore this email.</p>
          </div>
        `,
      });
    },
  },

  // Session configuration
  session: {
    // Session duration
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    // Update session on each request
    updateAge: 60 * 60 * 24, // 1 day
  },

  // Advanced options
  advanced: {
    // Generate secure cookies
    useSecureCookies: process.env.NODE_ENV === "production",
  },
});

// Export type for use in other files
export type Auth = typeof auth;
