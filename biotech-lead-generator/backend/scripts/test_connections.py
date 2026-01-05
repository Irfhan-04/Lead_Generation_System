"""
Test connections to all configured services
Run this after setting up your .env file
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings


def test_supabase():
    """Test Supabase connection (database + storage)"""
    print("\n1️⃣  Testing Supabase Connection...")
    print("-" * 60)
    
    try:
        from supabase import create_client
        
        # Test connection
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        
        # Test database access
        try:
            # Try to query a system table
            response = client.table("_realtime_schema_migrations").select("*").limit(1).execute()
            print("   ✅ Database connection successful")
        except Exception as e:
            print(f"   ⚠️  Database query failed: {e}")
        
        # Test storage access
        try:
            buckets = client.storage.list_buckets()
            bucket_names = [b.name for b in buckets]
            
            if settings.SUPABASE_STORAGE_BUCKET in bucket_names:
                print(f"   ✅ Storage bucket '{settings.SUPABASE_STORAGE_BUCKET}' exists")
            else:
                print(f"   ⚠️  Storage bucket '{settings.SUPABASE_STORAGE_BUCKET}' not found")
                print(f"      Available buckets: {bucket_names}")
                print(f"      Create it: Supabase → Storage → Create bucket 'exports'")
        except Exception as e:
            print(f"   ⚠️  Storage access failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Supabase connection failed: {e}")
        print(f"   Check: SUPABASE_URL and SUPABASE_SERVICE_KEY")
        return False


def test_redis():
    """Test Redis/Upstash connection"""
    print("\n2️⃣  Testing Redis Connection...")
    print("-" * 60)
    
    try:
        import redis
        
        # Parse Redis URL
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Test connection with ping
        if r.ping():
            print("   ✅ Redis connection successful")
            
            # Test set/get
            test_key = "test_connection"
            test_value = "Hello from Biotech Lead Generator!"
            
            r.set(test_key, test_value, ex=10)  # Expire in 10 seconds
            retrieved = r.get(test_key)
            
            if retrieved == test_value:
                print("   ✅ Redis read/write working")
                r.delete(test_key)  # Clean up
            else:
                print("   ⚠️  Redis read/write test failed")
            
            return True
        else:
            print("   ❌ Redis ping failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Redis connection failed: {e}")
        print(f"   Check: REDIS_URL format")
        return False


def test_resend():
    """Test Resend email API"""
    print("\n3️⃣  Testing Resend Email API...")
    print("-" * 60)
    
    if not settings.RESEND_API_KEY or settings.RESEND_API_KEY == "re_xxxxxxxxxxxxx":
        print("   ⚪ Resend not configured (optional)")
        return True
    
    try:
        import resend
        
        resend.api_key = settings.RESEND_API_KEY
        
        # Test API key validity by listing domains
        try:
            domains = resend.Domains.list()
            print("   ✅ Resend API key valid")
            
            if domains and len(domains) > 0:
                print(f"   ✅ Found {len(domains)} verified domain(s)")
            else:
                print("   ⚠️  No domains configured")
                print(f"   Using test email: {settings.RESEND_FROM_EMAIL}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Resend API test failed: {e}")
            print(f"   Check: RESEND_API_KEY")
            return False
            
    except ImportError:
        print("   ⚠️  Resend package not installed")
        print("   Install with: pip install resend")
        return False


def test_sentry():
    """Test Sentry error tracking"""
    print("\n4️⃣  Testing Sentry...")
    print("-" * 60)
    
    if not settings.SENTRY_DSN or "xxxxx" in settings.SENTRY_DSN:
        print("   ⚪ Sentry not configured (optional)")
        return True
    
    try:
        import sentry_sdk
        
        # Initialize Sentry
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENVIRONMENT,
            traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        )
        
        print("   ✅ Sentry initialized")
        print(f"   Environment: {settings.SENTRY_ENVIRONMENT}")
        
        # Optional: Send a test event
        # sentry_sdk.capture_message("Test from Biotech Lead Generator", level="info")
        # print("   ✅ Test event sent to Sentry")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Sentry initialization failed: {e}")
        print(f"   Check: SENTRY_DSN")
        return False


def test_pubmed():
    """Test PubMed API access"""
    print("\n5️⃣  Testing PubMed API...")
    print("-" * 60)
    
    if not settings.PUBMED_EMAIL:
        print("   ⚠️  PubMed email not configured")
        print("   Add PUBMED_EMAIL to .env")
        return False
    
    try:
        from Bio import Entrez
        
        Entrez.email = settings.PUBMED_EMAIL
        if settings.PUBMED_API_KEY:
            Entrez.api_key = settings.PUBMED_API_KEY
        
        # Test search
        handle = Entrez.esearch(db="pubmed", term="toxicology", retmax=1)
        record = Entrez.read(handle)
        handle.close()
        
        if record and "IdList" in record:
            print(f"   ✅ PubMed API working")
            print(f"   Email: {settings.PUBMED_EMAIL}")
            if settings.PUBMED_API_KEY:
                print(f"   API Key: Configured (higher rate limits)")
            else:
                print(f"   API Key: Not set (3 requests/sec limit)")
            return True
        else:
            print("   ⚠️  PubMed search returned no results")
            return False
            
    except ImportError:
        print("   ⚠️  Biopython not installed")
        print("   Install with: pip install biopython")
        return False
    except Exception as e:
        print(f"   ❌ PubMed API test failed: {e}")
        return False


def test_optional_apis():
    """Test optional external APIs"""
    print("\n6️⃣  Testing Optional APIs...")
    print("-" * 60)
    
    apis = [
        ("Proxycurl (LinkedIn)", settings.PROXYCURL_API_KEY),
        ("Hunter.io (Email)", settings.HUNTER_API_KEY),
        ("Clearbit (Company)", settings.CLEARBIT_API_KEY),
        ("Crunchbase (Funding)", settings.CRUNCHBASE_API_KEY),
    ]
    
    configured = 0
    for name, key in apis:
        if key:
            print(f"   ✅ {name}: Configured")
            configured += 1
        else:
            print(f"   ⚪ {name}: Not configured (optional)")
    
    if configured == 0:
        print("\n   ℹ️  No optional APIs configured - that's okay!")
        print("   App works fine without them")
    else:
        print(f"\n   ✅ {configured} optional API(s) configured")
    
    return True


def test_database_connection():
    """Test PostgreSQL database connection"""
    print("\n7️⃣  Testing Database Connection...")
    print("-" * 60)
    
    try:
        from sqlalchemy import create_engine, text
        
        # Create engine
        engine = create_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"),
            pool_pre_ping=True
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result:
                print("   ✅ Database connection successful")
                
                # Get PostgreSQL version
                version = conn.execute(text("SELECT version()")).scalar()
                if version:
                    pg_version = version.split(",")[0]
                    print(f"   ✅ PostgreSQL: {pg_version}")
                
                return True
        
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        print(f"   Check: DATABASE_URL and password")
        return False


def main():
    """Run all connection tests"""
    print("=" * 60)
    print("🧪 TESTING ALL SERVICE CONNECTIONS")
    print("=" * 60)
    
    results = {}
    
    # Required services
    results["Supabase"] = test_supabase()
    results["PostgreSQL"] = test_database_connection()
    results["Redis"] = test_redis()
    
    # Optional but recommended
    results["Resend"] = test_resend()
    results["Sentry"] = test_sentry()
    results["PubMed"] = test_pubmed()
    
    # Optional APIs
    results["Optional APIs"] = test_optional_apis()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for service, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {service}")
    
    print("\n" + "-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your backend is ready to run!")
        print("\nNext steps:")
        print("1. Run database migrations: alembic upgrade head")
        print("2. Start the server: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Check .env file values")
        print("- Verify passwords don't have [YOUR-PASSWORD]")
        print("- Create Supabase storage bucket 'exports'")
        print("- Install missing packages: pip install -r requirements.txt")
    
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)