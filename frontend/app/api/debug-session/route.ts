/**
 * Debug endpoint to check session state.
 * DELETE THIS FILE after debugging.
 */

import { cookies } from "next/headers";
import { Pool } from "pg";
import { NextResponse } from "next/server";

export async function GET() {
  const cookieStore = await cookies();
  const allCookies = cookieStore.getAll();

  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false },
  });

  try {
    const sessions = await pool.query('SELECT id, token, "userId", "expiresAt" FROM session');
    const users = await pool.query('SELECT id, email, name FROM "user"');
    await pool.end();

    return NextResponse.json({
      cookies: allCookies.map(c => ({ name: c.name, value: c.value.substring(0, 20) + '...' })),
      sessions: sessions.rows,
      users: users.rows,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    return NextResponse.json({ error: message, cookies: allCookies.map(c => c.name) });
  }
}
