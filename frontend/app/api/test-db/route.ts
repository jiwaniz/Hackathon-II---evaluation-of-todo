/**
 * Test endpoint to verify database connection.
 * DELETE THIS FILE after debugging.
 */

import { Pool } from "pg";
import { NextResponse } from "next/server";

export async function GET() {
  const dbUrl = process.env.DATABASE_URL;

  if (!dbUrl) {
    return NextResponse.json({ error: "DATABASE_URL not set", env: Object.keys(process.env).filter(k => k.includes('DATABASE') || k.includes('BETTER')) });
  }

  try {
    const pool = new Pool({
      connectionString: dbUrl,
      ssl: { rejectUnauthorized: false },
    });

    const result = await pool.query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'");
    await pool.end();

    return NextResponse.json({
      success: true,
      tables: result.rows.map(r => r.table_name),
      dbUrlPrefix: dbUrl.substring(0, 30) + "..."
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    return NextResponse.json({ error: message });
  }
}
