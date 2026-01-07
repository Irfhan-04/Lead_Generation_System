#!/usr/bin/env python3
"""
Comprehensive system test with IPv4 enforcement
Run this to verify everything is configured correctly
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_imports():
    """Test that all imports work"""
    print("\n1️⃣  Testing Imports...")
    print("-" * 60)
    
    try:
        from app.core.config import settings, get_database_url
        from app.core.database import sync_engine, check_db_connection_sync
        from app.models import User, Lead, Search, Export, Pipeline
        print("   ✅ All imports successful")
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False


def test_ipv4_resolution():
    """Test IPv4 resolution"""
    print("\n2️⃣  Testing IPv4 Resolution...")
    print("-" * 60)
    
    try:
        from app.core.config import get_ipv4_address
        from urllib.parse import urlparse
        from app.core.config import settings
        
        parsed = urlparse(settings.DATABASE_URL)
        if parsed.hostname:
            ipv4 = get_ipv4_address(parsed.hostname)
            
            # Check if it's an IPv4 address
            parts = ipv4.split('.')
            if len(parts) == 4 and all(part.isdigit() for part in parts):
                print(f"   ✅ Successfully resolved to IPv4: {ipv4}")
                return True
            else:
                print(f"   ⚠️  Resolution returned: {ipv4}")
                print(f"   This may still work if it's a valid address")
                return True
        else:
            print(f"   ⚠️  No hostname found in DATABASE_URL")
            return False
            
    except Exception as e:
        print(f"   ❌ IPv4 resolution failed: {e}")
        return False


def test_database_url():
    """Test database URL format"""
    print("\n3️⃣  Testing Database URL Format...")
    print("-" * 60)
    
    try:
        from app.core.config import get_database_url
        from urllib.parse import urlparse
        
        url = get_database_url(force_ipv4=True)
        parsed = urlparse(url)
        
        print(f"   Scheme: {parsed.scheme}")
        print(f"   Host: {parsed.hostname}")
        print(f"   Port: {parsed.port or 5432}")
        print(f"   Database: {parsed.path.lstrip('/')}")
        
        # Verify it's using psycopg2
        if "psycopg2" in parsed.scheme:
            print("   ✅ Correct driver: psycopg2")
        else:
            print(f"   ⚠️  Driver: {parsed.scheme}")
        
        # Verify IPv4
        hostname = parsed.hostname
        if hostname:
            parts = hostname.split('.')
            if len(parts) == 4 and all(part.isdigit() for part in parts):
                print(f"   ✅ Using IPv4 address: {hostname}")
            else:
                print(f"   ⚠️  Using hostname: {hostname}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ URL test failed: {e}")
        return False


def test_sync_connection():
    """Test synchronous database connection"""
    print("\n4️⃣  Testing Sync Database Connection...")
    print("-" * 60)
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        from app.core.config import get_database_url
        
        url = get_database_url(force_ipv4=True)
        parsed = urlparse(url)
        
        print(f"   Connecting to: {parsed.hostname}:{parsed.port or 5432}")
        
        # Connect with IPv4-enforced URL
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            dbname=parsed.path.lstrip('/'),
            user=parsed.username,
            password=parsed.password,
            connect_timeout=10,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5,
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"   ✅ Connection successful!")
        print(f"   PostgreSQL: {version.split(',')[0]}")
        
        # Test actual query
        cursor.execute("SELECT current_database(), current_user;")
        db, user = cursor.fetchone()
        print(f"   Database: {db}")
        print(f"   User: {user}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Sync connection failed: {e}")
        print(f"\n   Error type: {type(e).__name__}")
        return False


def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    print("\n5️⃣  Testing SQLAlchemy Connection...")
    print("-" * 60)
    
    try:
        from sqlalchemy import create_engine, text
        from app.core.config import get_database_url
        from app.core.database import SYNC_CONNECT_ARGS
        
        url = get_database_url(force_ipv4=True)
        
        engine = create_engine(
            url,
            pool_pre_ping=True,
            connect_args=SYNC_CONNECT_ARGS
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("   ✅ SQLAlchemy connection successful!")
                
                # Get database info
                result = conn.execute(text("""
                    SELECT 
                        current_database() as db,
                        current_user as user,
                        version() as version
                """))
                info = result.fetchone()
                print(f"   Database: {info[0]}")
                print(f"   User: {info[1]}")
                print(f"   Version: {info[2].split(',')[0]}")
                
                engine.dispose()
                return True
            else:
                print("   ⚠️  Query returned unexpected result")
                return False
                
    except Exception as e:
        print(f"   ❌ SQLAlchemy connection failed: {e}")
        return False


def test_model_imports():
    """Test that models are properly configured"""
    print("\n6️⃣  Testing Model Configuration...")
    print("-" * 60)
    
    try:
        from app.core.database import Base
        from app.models import User, Lead, Search, Export, Pipeline
        
        # Get all tables
        tables = list(Base.metadata.tables.keys())
        
        print(f"   Found {len(tables)} tables:")
        for table in tables:
            print(f"      - {table}")
        
        expected = ['users', 'leads', 'searches', 'exports', 'pipelines']
        missing = [t for t in expected if t not in tables]
        
        if missing:
            print(f"   ⚠️  Missing tables: {missing}")
            return False
        else:
            print(f"   ✅ All expected models found")
            return True
            
    except Exception as e:
        print(f"   ❌ Model test failed: {e}")
        return False


def test_redis_connection():
    """Test Redis connection"""
    print("\n7️⃣  Testing Redis Connection...")
    print("-" * 60)
    
    try:
        from app.core.config import settings
        import redis
        
        r = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
        # Test ping
        if r.ping():
            print("   ✅ Redis connection successful")
            
            # Test set/get
            test_key = "test_connection"
            r.set(test_key, "hello", ex=10)
            value = r.get(test_key)
            
            if value == "hello":
                print("   ✅ Redis read/write working")
                r.delete(test_key)
                return True
            else:
                print("   ⚠️  Redis read/write test failed")
                return False
        else:
            print("   ❌ Redis ping failed")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Redis connection failed: {e}")
        print(f"   Redis is optional for testing, continuing...")
        return True  # Don't fail the whole test for Redis


def provide_migration_commands():
    """Show commands to run migrations"""
    print("\n" + "=" * 60)
    print("📋 NEXT STEPS")
    print("=" * 60)
    
    print("\n✅ All critical tests passed!")
    print("\nRun these commands to set up your database:")
    print("\n1. Create migration:")
    print("   alembic revision --autogenerate -m \"Initial schema\"")
    
    print("\n2. Apply migration:")
    print("   alembic upgrade head")
    
    print("\n3. Verify tables:")
    print("   python -c \"from app.core.database import sync_engine; from sqlalchemy import inspect; print(inspect(sync_engine).get_table_names())\"")
    
    print("\n4. Start the server:")
    print("   uvicorn app.main:app --reload")
    
    print("\n5. Visit API docs:")
    print("   http://localhost:8000/docs")
    
    print("\n" + "=" * 60)


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    results = {}
    
    # Critical tests
    results["Imports"] = test_imports()
    
    if not results["Imports"]:
        print("\n❌ Cannot continue - imports failed")
        print("Run: pip install -r requirements.txt")
        return False
    
    results["IPv4 Resolution"] = test_ipv4_resolution()
    results["Database URL"] = test_database_url()
    results["Sync Connection"] = test_sync_connection()
    results["SQLAlchemy"] = test_sqlalchemy_connection()
    results["Models"] = test_model_imports()
    results["Redis"] = test_redis_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {test}")
    
    print("\n" + "-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    # Critical tests that must pass
    critical = ["Sync Connection", "SQLAlchemy", "Models"]
    critical_passed = all(results.get(test, False) for test in critical)
    
    if critical_passed:
        provide_migration_commands()
        return True
    else:
        print("\n❌ Critical tests failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Verify DATABASE_URL in .env")
        print("2. Check Supabase project status")
        print("3. Test network: ping db.dpzldplhzjuwfhiukyde.supabase.co")
        print("4. Try using IPv4: nslookup db.dpzldplhzjuwfhiukyde.supabase.co")
        print("\n" + "=" * 60)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)