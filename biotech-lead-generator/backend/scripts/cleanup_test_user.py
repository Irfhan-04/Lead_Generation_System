"""
Cleanup Test User
Removes any leftover test@example.com user from the database
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select


async def cleanup_test_user():
    """
    Remove test user if it exists
    """
    print("🧹 Cleaning up test data...\n")
    
    async with AsyncSessionLocal() as session:
        try:
            # Find test user
            result = await session.execute(
                select(User).where(User.email == "test@example.com")
            )
            test_user = result.scalar_one_or_none()
            
            if test_user:
                print(f"   Found test user: {test_user.email} (ID: {test_user.id})")
                
                # Delete user (cascade will delete all related records)
                await session.delete(test_user)
                await session.commit()
                
                print(f"   ✅ Deleted test user and all related records")
                
                # Verify deletion
                result = await session.execute(
                    select(User).where(User.email == "test@example.com")
                )
                if result.scalar_one_or_none() is None:
                    print(f"   ✅ Cleanup successful!\n")
                    return True
            else:
                print("   ℹ️  No test user found (already clean)\n")
                return True
                
        except Exception as e:
            print(f"   ❌ Error during cleanup: {e}")
            await session.rollback()
            return False


if __name__ == "__main__":
    result = asyncio.run(cleanup_test_user())
    if result:
        print("✅ Ready to run test_models.py again!")
    else:
        print("❌ Cleanup failed")
        sys.exit(1)