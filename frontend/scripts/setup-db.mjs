/**
 * Setup Better Auth database tables in Neon PostgreSQL.
 * Run with: node scripts/setup-db.mjs
 */

import pg from "pg";
const { Pool } = pg;

const DATABASE_URL = process.env.DATABASE_URL ||
  "postgresql://neondb_owner:npg_VCELyK9WR3gP@ep-falling-bar-a199lzbj-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require";

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// Drop and recreate with correct schema
const dropSchema = `
DROP TABLE IF EXISTS "verification" CASCADE;
DROP TABLE IF EXISTS "account" CASCADE;
DROP TABLE IF EXISTS "session" CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
`;

// Better Auth expects camelCase column names by default
const schema = `
-- Better Auth: User table
CREATE TABLE "user" (
  "id" TEXT PRIMARY KEY,
  "name" TEXT,
  "email" TEXT UNIQUE NOT NULL,
  "emailVerified" BOOLEAN DEFAULT FALSE,
  "image" TEXT,
  "createdAt" TIMESTAMP DEFAULT NOW(),
  "updatedAt" TIMESTAMP DEFAULT NOW()
);

-- Better Auth: Session table
CREATE TABLE "session" (
  "id" TEXT PRIMARY KEY,
  "expiresAt" TIMESTAMP NOT NULL,
  "token" TEXT UNIQUE NOT NULL,
  "createdAt" TIMESTAMP DEFAULT NOW(),
  "updatedAt" TIMESTAMP DEFAULT NOW(),
  "ipAddress" TEXT,
  "userAgent" TEXT,
  "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE
);

-- Better Auth: Account table (for email/password and OAuth)
CREATE TABLE "account" (
  "id" TEXT PRIMARY KEY,
  "accountId" TEXT NOT NULL,
  "providerId" TEXT NOT NULL,
  "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
  "accessToken" TEXT,
  "refreshToken" TEXT,
  "idToken" TEXT,
  "accessTokenExpiresAt" TIMESTAMP,
  "refreshTokenExpiresAt" TIMESTAMP,
  "scope" TEXT,
  "password" TEXT,
  "createdAt" TIMESTAMP DEFAULT NOW(),
  "updatedAt" TIMESTAMP DEFAULT NOW()
);

-- Better Auth: Verification table
CREATE TABLE "verification" (
  "id" TEXT PRIMARY KEY,
  "identifier" TEXT NOT NULL,
  "value" TEXT NOT NULL,
  "expiresAt" TIMESTAMP NOT NULL,
  "createdAt" TIMESTAMP DEFAULT NOW(),
  "updatedAt" TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX "idx_session_userId" ON "session"("userId");
CREATE INDEX "idx_session_token" ON "session"("token");
CREATE INDEX "idx_account_userId" ON "account"("userId");
CREATE INDEX "idx_user_email" ON "user"("email");
`;

async function setup() {
  console.log("Connecting to database...");
  const client = await pool.connect();

  try {
    console.log("Dropping old tables...");
    await client.query(dropSchema);
    console.log("Creating Better Auth tables with snake_case columns...");
    await client.query(schema);
    console.log("✓ Better Auth tables created successfully!");

    // Verify tables exist
    const result = await client.query(`
      SELECT table_name FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_name IN ('user', 'session', 'account', 'verification')
    `);
    console.log("Tables found:", result.rows.map(r => r.table_name).join(", "));

  } catch (error) {
    console.error("Error setting up database:", error.message);
    process.exit(1);
  } finally {
    client.release();
    await pool.end();
  }
}

setup();
