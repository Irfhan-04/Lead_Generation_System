"""
Test if all environment variables are configured correctly
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

def test_config():
    print("🧪 Testing Configuration\n")
    print("=" * 70)
    
    # Required settings
    required = {
        "SECRET_KEY": settings.SECRET_KEY,
        "SUPABASE_URL": settings.SUPABASE_URL,
        "SUPABASE_KEY": settings.SUPABASE_KEY,
        "DATABASE_URL": settings.DATABASE_URL,
        "REDIS_URL": settings.REDIS_URL,
    }
    
    print("\n✅ REQUIRED SETTINGS:")
    for key, value in required.items():
        status = "✅" if value and value != "GENERATE" else "❌"
        masked = value[:20] + "..." if value and len(value) > 20 else value
        print(f"  {status} {key}: {masked}")
    
    # Optional settings
    optional = {
        "RESEND_API_KEY": settings.RESEND_API_KEY,
        "SENTRY_DSN": settings.SENTRY_DSN,
        "PROXYCURL_API_KEY": settings.PROXYCURL_API_KEY,
        "HUNTER_API_KEY": settings.HUNTER_API_KEY,
    }
    
    print("\n⚙️  OPTIONAL SETTINGS:")
    for key, value in optional.items():
        status = "✅" if value else "⚪"
        masked = value[:20] + "..." if value and len(value) > 20 else "Not set"
        print(f"  {status} {key}: {masked}")
    
    print("\n" + "=" * 70)
    
    # Check if all required are set
    all_required = all(v and "GENERATE" not in str(v) for v in required.values())
    
    if all_required:
        print("\n🎉 Configuration looks good!")
        print("✅ All required settings are configured")
        print("\nNext: Run 'python scripts/test_connections.py' to verify services")
    else:
        print("\n⚠️  Some required settings are missing!")
        print("Please update your .env file")
    
    return all_required

if __name__ == "__main__":
    test_config()