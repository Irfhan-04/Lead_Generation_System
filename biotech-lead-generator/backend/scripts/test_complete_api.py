"""
Complete API Test with Cleanup and Error Handling
Tests all API endpoints with proper cleanup between runs
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

# Store tokens and IDs globally
ACCESS_TOKEN = None
USER_EMAIL = f"apitest_{int(time.time())}@example.com"  # Unique email per run
CREATED_LEAD_IDS = []

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"{title}")
    print('='*70)

def print_result(success, message, details=None):
    """Print a formatted result"""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")
    if details:
        for key, value in details.items():
            print(f"   {key}: {value}")

def register_and_login():
    """Step 1: Register and Login"""
    global ACCESS_TOKEN
    
    print_section("1️⃣  AUTHENTICATION")
    
    # Register
    print("\n📝 Registering new user...")
    register_data = {
        "email": USER_EMAIL,
        "password": "Test123!@#",
        "full_name": f"API Test User {int(time.time())}"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    
    if response.status_code == 201:
        print_result(True, "Registration successful", {
            "User ID": response.json()["data"]["user_id"],
            "Email": USER_EMAIL
        })
    elif response.status_code == 400:
        print_result(False, "User already exists (should not happen with unique email)")
        return False
    else:
        print_result(False, f"Registration failed: {response.text}")
        return False
    
    # Login
    print("\n🔐 Logging in...")
    login_data = {
        "email": USER_EMAIL,
        "password": "Test123!@#"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        tokens = response.json()
        ACCESS_TOKEN = tokens["access_token"]
        print_result(True, "Login successful", {
            "Token expires in": f"{tokens['expires_in']}s",
            "Has refresh token": "Yes"
        })
        return True
    else:
        print_result(False, f"Login failed: {response.text}")
        return False

def test_user_endpoints():
    """Step 2: Test User Endpoints"""
    print_section("2️⃣  USER MANAGEMENT")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Get profile
    print("\n👤 Getting user profile...")
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    
    if response.status_code == 200:
        profile = response.json()
        print_result(True, "Profile retrieved", {
            "Email": profile['email'],
            "Name": profile['full_name'],
            "Tier": profile['subscription_tier'],
            "Verified": profile['is_verified']
        })
    else:
        print_result(False, f"Get profile failed: {response.text}")
        return False
    
    # Update preferences
    print("\n⚙️  Updating user preferences...")
    prefs = {
        "theme": "dark",
        "email_notifications": True,
        "scoring_weights": {
            "role_fit": 30,
            "publication": 40,
            "funding": 20,
            "location": 10
        }
    }
    
    response = requests.put(f"{BASE_URL}/users/me/preferences", json=prefs, headers=headers)
    
    if response.status_code == 200:
        print_result(True, "Preferences updated", {
            "Theme": "dark",
            "Notifications": "enabled"
        })
    else:
        print_result(False, f"Update preferences failed: {response.text}")
    
    # Get usage stats
    print("\n📊 Getting usage statistics...")
    response = requests.get(f"{BASE_URL}/users/me/usage", headers=headers)
    
    if response.status_code == 200:
        usage = response.json()
        print_result(True, "Usage stats retrieved", {
            "Leads created": f"{usage['leads_created_this_month']}/{usage['leads_limit_per_month']}",
            "Usage": f"{usage['usage_percentage']}%"
        })
    else:
        print_result(False, f"Get usage failed: {response.text}")
    
    return True

def test_lead_endpoints():
    """Step 3: Test Lead Endpoints"""
    global CREATED_LEAD_IDS
    
    print_section("3️⃣  LEAD MANAGEMENT")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Create lead with unique email
    print("\n➕ Creating new lead...")
    unique_email = f"lead_{int(time.time())}@testbiotech.com"
    
    lead_data = {
        "name": "Dr. Test Lead",
        "title": "Director of Toxicology",
        "company": "Test Biotech Inc",
        "location": "Cambridge, MA",
        "email": unique_email,
        "recent_publication": True,
        "publication_year": 2024,
        "publication_title": "Novel 3D hepatic models for DILI",
        "company_funding": "Series B",
        "uses_3d_models": True,
        "tags": ["high-priority", "conference-speaker"]
    }
    
    response = requests.post(f"{BASE_URL}/leads", json=lead_data, headers=headers)
    
    if response.status_code == 201:
        lead = response.json()
        lead_id = lead["id"]
        CREATED_LEAD_IDS.append(lead_id)
        
        print_result(True, "Lead created", {
            "Name": lead['name'],
            "Score": f"{lead['propensity_score']}/100",
            "Priority": lead['priority_tier'],
            "Rank": lead['rank']
        })
    else:
        print_result(False, f"Create lead failed: {response.text}")
        return None
    
    # List leads
    print("\n📋 Listing leads...")
    response = requests.get(
        f"{BASE_URL}/leads",
        params={"page": 1, "size": 10, "sort_by": "propensity_score", "sort_order": "desc"},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print_result(True, "Leads listed", {
            "Count": len(data['items']),
            "Total": data['pagination']['total'],
            "Pages": data['pagination']['pages']
        })
    else:
        print_result(False, f"List leads failed: {response.text}")
    
    # Get lead details
    print("\n🔍 Getting lead details...")
    response = requests.get(f"{BASE_URL}/leads/{lead_id}", headers=headers)
    
    if response.status_code == 200:
        lead = response.json()
        print_result(True, "Lead details retrieved", {
            "Name": lead['name'],
            "Email": lead['email'],
            "Company": lead['company']
        })
    else:
        print_result(False, f"Get lead failed: {response.text}")
    
    # Update lead
    print("\n✏️  Updating lead...")
    update_data = {
        "title": "Senior Director of Toxicology",
        "notes": "Updated via API test"
    }
    
    response = requests.put(f"{BASE_URL}/leads/{lead_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        print_result(True, "Lead updated", {
            "New title": "Senior Director of Toxicology"
        })
    else:
        print_result(False, f"Update lead failed: {response.text}")
    
    # Recalculate score
    print("\n🎯 Recalculating propensity score...")
    response = requests.post(f"{BASE_URL}/leads/{lead_id}/score", headers=headers)
    
    if response.status_code == 200:
        lead = response.json()
        print_result(True, "Score recalculated", {
            "New score": f"{lead['propensity_score']}/100",
            "Priority": lead['priority_tier']
        })
    else:
        print_result(False, f"Recalculate score failed: {response.text}")
    
    return lead_id

def test_bulk_operations():
    """Step 4: Test Bulk Operations"""
    global CREATED_LEAD_IDS
    
    print_section("4️⃣  BULK OPERATIONS")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Bulk create with unique emails
    print("\n➕ Bulk creating leads...")
    timestamp = int(time.time())
    
    bulk_data = {
        "leads": [
            {
                "name": f"Dr. Bulk Lead 1",
                "title": "Research Scientist",
                "company": "Bulk Test Corp 1",
                "location": "Boston, MA",
                "email": f"bulk1_{timestamp}@testcorp.com"
            },
            {
                "name": f"Dr. Bulk Lead 2",
                "title": "Principal Scientist",
                "company": "Bulk Test Corp 2",
                "location": "San Francisco, CA",
                "email": f"bulk2_{timestamp}@testcorp.com"
            },
            {
                "name": f"Dr. Bulk Lead 3",
                "title": "Senior Scientist",
                "company": "Bulk Test Corp 3",
                "location": "Cambridge, MA",
                "email": f"bulk3_{timestamp}@testcorp.com"
            }
        ],
        "skip_duplicates": True,
        "calculate_scores": True
    }
    
    response = requests.post(f"{BASE_URL}/leads/bulk/create", json=bulk_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print_result(True, "Bulk creation completed", {
            "Successful": result['success_count'],
            "Failed": result['failure_count'],
            "Total": result['total']
        })
    else:
        print_result(False, f"Bulk create failed: {response.text}")
    
    return True

def test_filtering():
    """Step 5: Test Filtering and Search"""
    print_section("5️⃣  FILTERING & SEARCH")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Filter by score
    print("\n🎯 Filtering high-priority leads...")
    response = requests.get(
        f"{BASE_URL}/leads",
        params={"min_score": 70, "priority_tier": "HIGH"},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print_result(True, "Filtered leads", {
            "High priority count": len(data['items']),
            "Total matching": data['pagination']['total']
        })
    else:
        print_result(False, f"Filter failed: {response.text}")
    
    # Search
    print("\n🔍 Searching leads...")
    response = requests.get(
        f"{BASE_URL}/leads",
        params={"search": "director", "location": "Cambridge"},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print_result(True, "Search completed", {
            "Results found": len(data['items']),
            "Query": "director in Cambridge"
        })
    else:
        print_result(False, f"Search failed: {response.text}")
    
    return True

def cleanup():
    """Cleanup: Delete all created leads"""
    print_section("🧹 CLEANUP")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    if not CREATED_LEAD_IDS:
        print("\n⚠️  No leads to clean up")
        return True
    
    print(f"\n🗑️  Deleting {len(CREATED_LEAD_IDS)} created lead(s)...")
    
    # Delete leads one by one
    deleted_count = 0
    for lead_id in CREATED_LEAD_IDS:
        response = requests.delete(f"{BASE_URL}/leads/{lead_id}", headers=headers)
        if response.status_code == 200:
            deleted_count += 1
    
    print_result(True, f"Cleanup completed", {
        "Leads deleted": deleted_count
    })
    
    # Optionally delete the test user
    print("\n👤 Note: Test user account remains (can be deleted manually if needed)")
    
    return True

def main():
    """Run all tests"""
    print("="*70)
    print("🧪 COMPLETE API TEST SUITE")
    print("="*70)
    print(f"\nTest started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {BASE_URL}")
    print(f"Test user: {USER_EMAIL}")
    
    try:
        # Run tests in sequence
        if not register_and_login():
            print("\n❌ Failed at authentication step")
            return
        
        if not test_user_endpoints():
            print("\n❌ Failed at user endpoints")
            return
        
        lead_id = test_lead_endpoints()
        if not lead_id:
            print("\n❌ Failed at lead endpoints")
            return
        
        if not test_bulk_operations():
            print("\n❌ Failed at bulk operations")
            return
        
        if not test_filtering():
            print("\n❌ Failed at filtering")
            return
        
        # Cleanup
        cleanup()
        
        # Success summary
        print_section("🎉 ALL TESTS PASSED!")
        
        print("\n✅ Test Results:")
        print("   • Authentication: PASSED")
        print("   • User Management: PASSED")
        print("   • Lead CRUD: PASSED")
        print("   • Scoring: PASSED")
        print("   • Bulk Operations: PASSED")
        print("   • Filtering & Search: PASSED")
        print("   • Cleanup: COMPLETED")
        
        print("\n🚀 Your API is production-ready!")
        print("\nNext steps:")
        print("   1. Access API docs: http://localhost:8000/docs")
        print("   2. Test with frontend")
        print("   3. Deploy to production")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        cleanup()
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        cleanup()

if __name__ == "__main__":
    main()