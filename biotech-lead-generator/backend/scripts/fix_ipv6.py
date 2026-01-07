#!/usr/bin/env python3
"""
Fix IPv6 connection issues with Supabase
Resolves hostname to IPv4 and updates DATABASE_URL
"""

import sys
import os
import socket
from pathlib import Path
from urllib.parse import urlparse, urlunparse

def find_env_file():
    """Find .env file"""
    backend_dir = Path(__file__).parent.parent
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found!")
        return None
    
    return env_file

def resolve_to_ipv4(hostname):
    """Resolve hostname to IPv4 address"""
    try:
        # Get all addresses
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
        
        # Get first IPv4 address
        ipv4 = addr_info[0][4][0]
        return ipv4
    except Exception as e:
        print(f"   ❌ Failed to resolve {hostname}: {e}")
        return None

def fix_database_url_ipv6(url):
    """Fix DATABASE_URL to use IPv4"""
    parsed = urlparse(url)
    
    print(f"   Current host: {parsed.hostname}")
    
    # Resolve to IPv4
    ipv4 = resolve_to_ipv4(parsed.hostname)
    
    if not ipv4:
        return None
    
    print(f"   Resolved IPv4: {ipv4}")
    
    # Reconstruct URL with IPv4 address
    netloc = f"{parsed.username}:{parsed.password}@{ipv4}"
    if parsed.port:
        netloc += f":{parsed.port}"
    
    new_url = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    
    return new_url

def main():
    """Main function"""
    print("=" * 60)
    print("🔧 IPv6 CONNECTION FIX")
    print("=" * 60)
    
    # Find .env file
    env_file = find_env_file()
    if not env_file:
        return False
    
    print(f"\n📄 Found .env file: {env_file}")
    
    # Read content
    with open(env_file, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find and fix DATABASE_URL
    fixed_lines = []
    found = False
    
    for line in lines:
        if line.strip().startswith('DATABASE_URL='):
            found = True
            key, value = line.split('=', 1)
            
            print(f"\n🔍 Current DATABASE_URL:")
            print(f"   {value[:60]}...")
            
            print(f"\n🔧 Fixing IPv6 issue...")
            
            fixed_value = fix_database_url_ipv6(value)
            
            if fixed_value:
                print(f"\n✅ Fixed DATABASE_URL:")
                print(f"   {fixed_value[:60]}...")
                fixed_lines.append(f"{key}={fixed_value}")
            else:
                print(f"\n❌ Could not fix URL")
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    if not found:
        print("\n❌ DATABASE_URL not found in .env")
        return False
    
    # Ask to save
    print("\n" + "=" * 60)
    response = input("💾 Save changes to .env? (y/n): ")
    
    if response.lower() == 'y':
        # Backup
        backup_file = env_file.parent / f"{env_file.name}.backup"
        with open(backup_file, 'w') as f:
            f.write(content)
        print(f"✅ Backup created: {backup_file}")
        
        # Write new content
        with open(env_file, 'w') as f:
            f.write('\n'.join(fixed_lines))
        print(f"✅ Updated: {env_file}")
        
        print("\n✅ Fixed! Now run:")
        print("   python scripts/test_db_direct.py")
        return True
    else:
        print("❌ Changes not saved")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)