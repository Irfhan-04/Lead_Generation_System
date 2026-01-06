#!/usr/bin/env python3
"""
Test direct database connection
Run this BEFORE running Alembic migrations
"""

import sys
import os
from urllib.parse import urlparse

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings


def parse_db_url(url):
    """Parse and display database URL components"""
    parsed = urlparse(url)
    
    print("\n📋 Database Connection Details:")
    print("-" * 60)
    print(f"   Protocol: {parsed.scheme}")
    print(f"   Host: {parsed.hostname}")
    print(f"   Port: {parsed.port or 5432}")
    print(f"   Database: {parsed.path.lstrip('/')}")
    print(f"   Username: {parsed.username}")
    print(f"   Password: {'*' * 8 if parsed.password else 'NOT SET'}")
    print("-" * 60)


def test_psycopg2_connection():
    """Test connection using psycopg2 (what Alembic uses)"""
    print("\n1️⃣  Testing psycopg2 Connection...")
    print("-" * 60)
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        # Parse connection string
        parsed = urlparse(settings.DATABASE_URL)
        
        # Extract components
        host = parsed.hostname
        port = parsed.port or 5432
        dbname = parsed.path.lstrip('/')
        user = parsed.username
        password = parsed.password
        
        print(f"   Attempting connection to: {host}:{port}")
        print(f"   Database: {dbname}")
        
        # Try to connect with IPv4 preference
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=10,
            options="-c timezone=utc"
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"   ✅ Connection successful!")
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except ImportError:
        print("   ❌ psycopg2 not installed")
        print("   Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n   🔍 Troubleshooting:")
        print("   1. Check your DATABASE_URL in .env")
        print("   2. Verify password doesn't contain special characters")
        print("   3. Ensure Supabase project is not paused")
        print("   4. Check if IPv6 is causing issues")
        print("   5. Try resetting database password in Supabase")
        return False


def test_sqlalchemy_connection():
    """Test connection using SQLAlchemy"""
    print("\n2️⃣  Testing SQLAlchemy Connection...")
    print("-" * 60)
    
    try:
        from sqlalchemy import create_engine, text
        
        # Create engine
        database_url = settings.DATABASE_URL
        if not database_url.startswith("postgresql+psycopg2://"):
            if database_url.startswith("postgresql://"):
                database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": 10,
                "options": "-c timezone=utc"
            }
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"   ✅ SQLAlchemy connection successful!")
            
            # Get database info
            result = conn.execute(text("""
                SELECT 
                    current_database() as db,
                    current_user as user,
                    inet_server_addr() as server_ip
            """))
            row = result.fetchone()
            print(f"   Database: {row[0]}")
            print(f"   User: {row[1]}")
            print(f"   Server IP: {row[2] or 'N/A'}")
        
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"   ❌ SQLAlchemy connection failed: {e}")
        return False


def test_async_connection():
    """Test async connection"""
    print("\n3️⃣  Testing Async Connection...")
    print("-" * 60)
    
    try:
        import asyncio
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        async def test():
            # Create async engine
            database_url = settings.DATABASE_URL
            if database_url.startswith("postgresql://"):
                database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            
            engine = create_async_engine(
                database_url,
                pool_pre_ping=True
            )
            
            async with engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                print(f"   ✅ Async connection successful!")
            
            await engine.dispose()
            return True
        
        return asyncio.run(test())
        
    except ImportError:
        print("   ⚠️  asyncpg not installed (optional)")
        return True
    except Exception as e:
        print(f"   ❌ Async connection failed: {e}")
        return False


def provide_solutions():
    """Provide solutions for common issues"""
    print("\n🔧 COMMON SOLUTIONS:")
    print("=" * 60)
    
    print("\n1. IPv6 Connection Issues:")
    print("   Add to your DATABASE_URL: ?ssl=require")
    print("   Or use IP address instead of hostname")
    
    print("\n2. Password with Special Characters:")
    print("   Escape special characters in URL:")
    print("   @ → %40, # → %23, $ → %24, & → %26")
    
    print("\n3. Supabase Project Paused:")
    print("   - Go to Supabase Dashboard")
    print("   - Check project status")
    print("   - Unpause if needed")
    
    print("\n4. Reset Database Password:")
    print("   - Supabase Dashboard → Settings → Database")
    print("   - Reset password")
    print("   - Update .env file with new password")
    
    print("\n5. Check Environment Variables:")
    print("   Run: python scripts/test_config.py")
    
    print("\n6. Force IPv4 (if IPv6 fails):")
    print("   Get IPv4 address:")
    print("   Run: nslookup db.dpzldplhzjuwfhiukyde.supabase.co")
    print("   Use IP directly in DATABASE_URL")
    
    print("\n" + "=" * 60)


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 DATABASE CONNECTION DIAGNOSTIC")
    print("=" * 60)
    
    # Show database URL details
    parse_db_url(settings.DATABASE_URL)
    
    # Run tests
    results = []
    results.append(("psycopg2", test_psycopg2_connection()))
    results.append(("SQLAlchemy", test_sqlalchemy_connection()))
    results.append(("Async", test_async_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name} connection")
    
    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if results[0][1]:  # psycopg2 test passed
        print("\n✅ Database is accessible! You can now run:")
        print("   alembic revision --autogenerate -m 'Initial schema'")
        print("   alembic upgrade head")
    else:
        print("\n❌ Cannot connect to database")
        provide_solutions()
    
    print("=" * 60)
    
    return results[0][1]  # Return True if psycopg2 test passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)