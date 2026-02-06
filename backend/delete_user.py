#!/usr/bin/env python3
"""
Quick script to delete users from the database for testing purposes.
Usage:
    uv run python delete_user.py <email>
    uv run python delete_user.py --all  # Delete all users (careful!)
"""

import sys
from sqlmodel import Session, select, delete

from database import get_engine
from models.user import User

# Get the database engine
engine = get_engine()


def delete_user_by_email(email: str):
    """Delete a user by email address."""
    with Session(engine) as session:
        # Find the user
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if user:
            # Delete the user (cascade will handle related records)
            session.delete(user)
            session.commit()
            print(f"✅ Deleted user: {user.email} (ID: {user.id})")
        else:
            print(f"❌ User not found: {email}")


def delete_all_users():
    """Delete all users (for testing only!)."""
    with Session(engine) as session:
        # Count users first
        count_statement = select(User)
        users = session.exec(count_statement).all()
        count = len(users)

        if count == 0:
            print("ℹ️  No users to delete")
            return

        # Confirm deletion
        print(f"⚠️  WARNING: About to delete {count} user(s)")
        confirm = input("Type 'yes' to confirm: ")

        if confirm.lower() == 'yes':
            # Delete all users
            delete_statement = delete(User)
            result = session.exec(delete_statement)
            session.commit()
            print(f"✅ Deleted {count} user(s)")
        else:
            print("❌ Deletion cancelled")


def list_users():
    """List all users in the database."""
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()

        if not users:
            print("ℹ️  No users in database")
            return

        print(f"\n📋 Users in database ({len(users)}):")
        print("-" * 80)
        for user in users:
            verified = "✅" if user.emailVerified else "❌"
            print(f"  {verified} {user.email:40} (ID: {user.id})")
        print("-" * 80)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  uv run python delete_user.py <email>         # Delete specific user")
        print("  uv run python delete_user.py --all           # Delete all users")
        print("  uv run python delete_user.py --list          # List all users")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--all":
        delete_all_users()
    elif arg == "--list":
        list_users()
    else:
        # Assume it's an email
        delete_user_by_email(arg)


if __name__ == "__main__":
    main()
