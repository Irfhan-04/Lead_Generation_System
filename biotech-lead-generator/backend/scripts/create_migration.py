"""
Helper script to create Alembic migration
This script handles the migration creation with proper error handling
"""

import sys
import os
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def check_env_file():
    """Check if .env file exists"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        print(f"✅ Found .env file at: {env_path}")
        return True
    else:
        print(f"❌ No .env file found at: {env_path}")
        print("💡 Please create a .env file with DATABASE_URL and other required variables")
        return False

def check_database_url():
    """Check if DATABASE_URL is set"""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"✅ DATABASE_URL is set")
        # Mask password in output
        if "@" in database_url:
            masked = database_url.split("@")[0] + "@***"
            print(f"   URL: {masked}")
        return True
    else:
        print("❌ DATABASE_URL environment variable is not set")
        return False

def create_migration():
    """Create the Alembic migration"""
    print("\n" + "=" * 60)
    print("🚀 Creating Alembic Migration")
    print("=" * 60)
    
    # Check prerequisites
    if not check_env_file():
        return False
    
    if not check_database_url():
        print("\n💡 Tip: Make sure your .env file is loaded")
        print("   You can load it with: source .env (Linux/Mac) or load in your IDE")
        return False
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.dirname(__file__))
    os.chdir(backend_dir)
    
    print("\n📝 Running: python -m alembic revision --autogenerate -m 'Initial schema'")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            ["python", "-m", "alembic", "revision", "--autogenerate", "-m", "Initial schema"],
            check=True,
            capture_output=False,
            text=True
        )
        print("\n✅ Migration created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Migration creation failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = create_migration()
    if success:
        print("\n" + "=" * 60)
        print("✅ Next Steps:")
        print("1. Review the generated migration file in alembic/versions/")
        print("2. Run: python -m alembic upgrade head")
        print("3. Verify tables in Supabase dashboard")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Migration creation failed")
        print("\n💡 Troubleshooting:")
        print("1. Ensure .env file exists with DATABASE_URL")
        print("2. Check database connection (run: python scripts/test_db_direct.py)")
        print("3. If IPv6 issue, use Supabase Connection Pooler")
        print("   See MIGRATION_SETUP.md for details")
        print("=" * 60)
        sys.exit(1)

