"""
Test authentication flow
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_auth_flow():
    """Test complete authentication flow"""
    
    print("🧪 Testing Authentication Flow\n")
    print("=" * 60)
    
    # 1. Register
    print("\n1️⃣  Testing Registration...")
    register_data = {
        "email": "autotest@example.com",
        "password": "Test123!@#",
        "full_name": "Auto Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    
    if response.status_code == 201:
        print("✅ Registration successful")
        user_id = response.json()["data"]["user_id"]
        print(f"   User ID: {user_id}")
    elif response.status_code == 400 and "already registered" in response.text:
        print("⚠️  User already exists, continuing...")
    else:
        print(f"❌ Registration failed: {response.text}")
        return
    
    # 2. Login
    print("\n2️⃣  Testing Login...")
    login_data = {
        "email": "autotest@example.com",
        "password": "Test123!@#"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        print("✅ Login successful")
        tokens = response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        print(f"   Access token: {access_token[:50]}...")
        print(f"   Expires in: {tokens['expires_in']} seconds")
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    # 3. Get Profile
    print("\n3️⃣  Testing Get Profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        print("✅ Got user profile")
        profile = response.json()
        print(f"   Email: {profile['email']}")
        print(f"   Name: {profile['full_name']}")
        print(f"   Tier: {profile['subscription_tier']}")
        print(f"   Verified: {profile['is_verified']}")
    else:
        print(f"❌ Get profile failed: {response.text}")
    
    # 4. Test Token Refresh
    print("\n4️⃣  Testing Token Refresh...")
    refresh_data = {"refresh_token": refresh_token}
    
    response = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_data)
    
    if response.status_code == 200:
        print("✅ Token refresh successful")
        new_token = response.json()["access_token"]
        print(f"   New token: {new_token[:50]}...")
    else:
        print(f"❌ Token refresh failed: {response.text}")
    
    # 5. Test Logout
    print("\n5️⃣  Testing Logout...")
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    
    if response.status_code == 200:
        print("✅ Logout successful")
    else:
        print(f"❌ Logout failed: {response.text}")
    
    # 6. Test Invalid Token
    print("\n6️⃣  Testing Invalid Token...")
    bad_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=bad_headers)
    
    if response.status_code == 401:
        print("✅ Invalid token correctly rejected")
    else:
        print(f"❌ Should have rejected invalid token: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("🎉 Authentication Tests Complete!\n")


if __name__ == "__main__":
    test_auth_flow()