#!/usr/bin/env python
"""Database connection diagnostic script.

Run this to test if the database connection works:
    cd backend && uv run python test_db_connection.py
"""

import logging
import sys
from datetime import datetime

from config import settings
from database import get_engine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_database_connection():
    """Test database connection and basic operations."""
    print("\n" + "=" * 60)
    print("EVOLUTION OF TODO - DATABASE CONNECTION DIAGNOSTIC")
    print("=" * 60 + "\n")

    # 1. Check environment variables
    print("📋 Checking Configuration:")
    print(f"   Environment: {settings.environment}")
    print(f"   Database URL: {settings.database_url[:50]}...")
    print(f"   Supabase JWT Secret: {'✅ Set' if settings.supabase_jwt_secret else '❌ Not set'}")
    print(f"   Google API Key: {'✅ Set' if settings.google_api_key else '❌ Not set'}")
    print(f"   Groq API Key: {'✅ Set' if settings.groq_api_key else '❌ Not set'}")

    # 2. Test engine creation
    print("\n🔌 Testing Engine Creation:")
    try:
        engine = get_engine()
        print("   ✅ Engine created successfully")
    except Exception as e:
        print(f"   ❌ Engine creation failed: {e}")
        return False

    # 3. Test connection
    print("\n📡 Testing Database Connection:")
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("   ✅ Connection successful")
            print(f"   Server time: {datetime.utcnow().isoformat()}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check DATABASE_URL is correct (includes ?sslmode=require for Neon)")
        print("   2. Verify Neon database is not paused")
        print("   3. Check if connection pool is exhausted")
        print("   4. Test with: psql '<DATABASE_URL>'")
        return False

    # 4. Test table creation
    print("\n🏗️  Testing Table Creation:")
    try:
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(engine)
        print("   ✅ Tables created successfully")
    except Exception as e:
        print(f"   ❌ Table creation failed: {e}")
        return False

    # 5. Test query
    print("\n🔍 Testing Queries:")
    try:
        from sqlmodel import Session, select
        from models import Task

        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            print(f"   ✅ Query successful - Found {len(tasks)} tasks")
    except Exception as e:
        print(f"   ❌ Query failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ ALL CHECKS PASSED - DATABASE IS READY")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
