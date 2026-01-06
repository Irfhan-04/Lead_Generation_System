#!/usr/bin/env python3
"""
Automatic Database URL Fixer
Fixes common DATABASE_URL issues in your .env file
"""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse, quote_plus, urlunparse

def find_env_file():
    """Find .env file"""
    backend_dir = Path(__file__).parent.parent
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print(f"   Expected location: {env_file}")
        print("\n   Create it by copying .env.example:")
        print("   cp .env.example .env")
        return None
    
    return env_file


def read_env_file(env_file):
    """Read .env file"""
    with open(env_file, 'r') as f:
        return f.read()


def write_env_file(env_file, content):
    """Write .env file"""
    # Backup first
    backup_file = env_file.parent / f"{env_file.name}.backup"
    with open(backup_file, 'w') as f:
        f.write(content)
    print(f"✅ Backup created: {backup_file}")
    
    # Write new content
    with open(env_file, 'w') as f:
        f.write(content)
    print(f"✅ Updated: {env_file}")


def fix_database_url(url):
    """Fix common DATABASE_URL issues"""
    issues_found = []
    
    # Issue 1: Missing driver specification
    if url.startswith("postgresql://") and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        issues_found.append("Added psycopg2 driver specification")
    
    # Issue 2: Check for placeholder password
    if "[YOUR-PASSWORD]" in url or "YOUR-PASSWORD" in url:
        issues_found.append("⚠️  PLACEHOLDER PASSWORD DETECTED - You must replace it!")
        return url, issues_found, False
    
    # Issue 3: Parse and check for special characters in password
    try:
        parsed = urlparse(url)
        if parsed.password:
            # Check if password has unescaped special characters
            special_chars = ['@', '#', '$', '&', ':', '/', '?', '=']
            has_special = any(char in parsed.password for char in special_chars)
            
            if has_special:
                # Re-encode the password
                encoded_password = quote_plus(parsed.password)
                if encoded_password != parsed.password:
                    # Reconstruct URL with encoded password
                    netloc = f"{parsed.username}:{encoded_password}@{parsed.hostname}"
                    if parsed.port:
                        netloc += f":{parsed.port}"
                    
                    url = urlunparse((
                        parsed.scheme,
                        netloc,
                        parsed.path,
                        parsed.params,
                        parsed.query,
                        parsed.fragment
                    ))
                    issues_found.append("Escaped special characters in password")
    except Exception as e:
        issues_found.append(f"⚠️  Could not parse URL: {e}")
        return url, issues_found, False
    
    return url, issues_found, True


def main():
    """Main function"""
    print("=" * 60)
    print("🔧 DATABASE URL FIXER")
    print("=" * 60)
    
    # Find .env file
    env_file = find_env_file()
    if not env_file:
        return False
    
    print(f"\n📄 Found .env file: {env_file}")
    
    # Read content
    content = read_env_file(env_file)
    lines = content.split('\n')
    
    # Find and fix DATABASE_URL
    fixed_lines = []
    found_db_url = False
    all_valid = True
    
    for line in lines:
        if line.strip().startswith('DATABASE_URL='):
            found_db_url = True
            key, value = line.split('=', 1)
            
            print(f"\n🔍 Found DATABASE_URL")
            print(f"   Original: {value[:50]}...")
            
            # Fix it
            fixed_value, issues, valid = fix_database_url(value)
            
            if issues:
                print(f"\n   Issues found:")
                for issue in issues:
                    print(f"   - {issue}")
            
            if not valid:
                all_valid = False
                print(f"\n   ⚠️  Manual action required!")
            else:
                print(f"\n   Fixed: {fixed_value[:50]}...")
            
            fixed_lines.append(f"{key}={fixed_value}")
        else:
            fixed_lines.append(line)
    
    if not found_db_url:
        print("\n❌ DATABASE_URL not found in .env file!")
        print("   Add it manually:")
        print("   DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db")
        return False
    
    # Ask to save
    if all_valid:
        print("\n" + "=" * 60)
        response = input("💾 Save changes? (y/n): ")
        
        if response.lower() == 'y':
            new_content = '\n'.join(fixed_lines)
            write_env_file(env_file, new_content)
            
            print("\n✅ Fixed! Now run:")
            print("   python scripts/test_db_direct.py")
            return True
        else:
            print("❌ Changes not saved")
            return False
    else:
        print("\n⚠️  Cannot auto-fix - manual action required:")
        print("   1. Replace [YOUR-PASSWORD] with your actual password")
        print("   2. Get password from: Supabase Dashboard → Settings → Database")
        print("   3. Run this script again")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)