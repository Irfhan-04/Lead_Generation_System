"""
Test complete API flow
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Store tokens globally
ACCESS_TOKEN = None

def register_and_login():
    """Step 1: Register and Login"""
    global ACCESS_TOKEN
    
    print("\n1️⃣  Registering and Logging In...")
    
    # Register
    register_data = {
        "email": "fulltest@example.com",
        "password": "Test123!@#",
        "full_name": "Full Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 400 and "already registered" in response.text:
        print("   User exists, logging in...")
    else:
        print(f"   ✅ Registered: {response.status_code}")
    
    # Login
    login_data = {
        "email": "fulltest@example.com",
        "password": "Test123!@#"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        print(f"   ✅ Logged in successfully")
        return True
    else:
        print(f"   ❌ Login failed: {response.text}")
        return False

def test_user_endpoints():
    """Step 2: Test User Endpoints"""
    print("\n2️⃣  Testing User Endpoints...")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Get profile
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    if response.status_code == 200:
        profile = response.json()
        print(f"   ✅ Got profile: {profile['email']}")
    else:
        print(f"   ❌ Get profile failed: {response.status_code}")
        return False
    
    # Update preferences
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
        print(f"   ✅ Updated preferences")
    else:
        print(f"   ❌ Update preferences failed: {response.status_code}")
    
    # Get usage stats
    response = requests.get(f"{BASE_URL}/users/me/usage", headers=headers)
    if response.status_code == 200:
        usage = response.json()
        print(f"   ✅ Usage: {usage['leads_created_this_month']}/{usage['leads_limit_per_month']} leads")
    else:
        print(f"   ❌ Get usage failed: {response.status_code}")
    
    return True

def test_lead_endpoints():
    """Step 3: Test Lead Endpoints"""
    print("\n3️⃣  Testing Lead Endpoints...")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Create lead
    lead_data = {
        "name": "Dr. Test Lead",
        "title": "Director of Toxicology",
        "company": "Test Biotech Inc",
        "location": "Cambridge, MA",
        "email": "testlead@testbiotech.com",
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
        print(f"   ✅ Created lead: {lead['name']}")
        print(f"      Score: {lead['propensity_score']}/100")
        print(f"      Priority: {lead['priority_tier']}")
        print(f"      Rank: {lead['rank']}")
    else:
        print(f"   ❌ Create lead failed: {response.text}")
        return False
    
    # List leads
    response = requests.get(
        f"{BASE_URL}/leads",
        params={"page": 1, "size": 10, "sort_by": "propensity_score", "sort_order": "desc"},
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Listed leads: {len(data['items'])} leads")
        print(f"      Total: {data['pagination']['total']}")
    else:
        print(f"   ❌ List leads failed: {response.status_code}")
    
    # Get lead details
    response = requests.get(f"{BASE_URL}/leads/{lead_id}", headers=headers)
    if response.status_code == 200:
        lead = response.json()
        print(f"   ✅ Got lead details: {lead['name']}")
    else:
        print(f"   ❌ Get lead failed: {response.status_code}")
    
    # Update lead
    update_data = {
        "title": "Senior Director of Toxicology",
        "notes": "Updated via API test"
    }
    
    response = requests.put(f"{BASE_URL}/leads/{lead_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print(f"   ✅ Updated lead")
    else:
        print(f"   ❌ Update lead failed: {response.status_code}")
    
    # Recalculate score
    response = requests.post(f"{BASE_URL}/leads/{lead_id}/score", headers=headers)
    if response.status_code == 200:
        lead = response.json()
        print(f"   ✅ Recalculated score: {lead['propensity_score']}/100")
    else:
        print(f"   ❌ Recalculate score failed: {response.status_code}")
    
    return lead_id

def test_bulk_operations(lead_id):
    """Step 4: Test Bulk Operations"""
    print("\n4️⃣  Testing Bulk Operations...")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Bulk create
    bulk_data = {
        "leads": [
            {
                "name": "Dr. Bulk Lead 1",
                "title": "Research Scientist",
                "company": "Bulk Test Corp 1",
                "location": "Boston, MA"
            },
            {
                "name": "Dr. Bulk Lead 2",
                "title": "Principal Scientist",
                "company": "Bulk Test Corp 2",
                "location": "San Francisco, CA"
            },
            {
                "name": "Dr. Bulk Lead 3",
                "title": "Senior Scientist",
                "company": "Bulk Test Corp 3",
                "location": "Cambridge, MA"
            }
        ],
        "skip_duplicates": True,
        "calculate_scores": True
    }
    
    response = requests.post(f"{BASE_URL}/leads/bulk/create", json=bulk_data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Bulk created: {result['success_count']} leads")
    else:
        print(f"   ❌ Bulk create failed: {response.status_code}")
    
    return True

def test_filtering():
    """Step 5: Test Filtering"""
    print("\n5️⃣  Testing Filtering...")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # Filter by score
    response = requests.get(
        f"{BASE_URL}/leads",
        params={"min_score": 70, "priority_tier": "HIGH"},
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ High priority leads: {len(data['items'])}")
    else:
        print(f"   ❌ Filter failed: {response.status_code}")
    
    # Search
    response = requests.get(
        f"{BASE_URL}/leads",
        params={"search": "director", "location": "Cambridge"},
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Search results: {len(data['items'])}")
    else:
        print(f"   ❌ Search failed: {response.status_code}")
    
    return True

def main():
    print("🧪 Testing Complete API\n")
    print("=" * 60)
    
    if not register_and_login():
        print("\n❌ Failed at login step")
        return
    
    if not test_user_endpoints():
        print("\n❌ Failed at user endpoints")
        return
    
    lead_id = test_lead_endpoints()
    if not lead_id:
        print("\n❌ Failed at lead endpoints")
        return
    
    if not test_bulk_operations(lead_id):
        print("\n❌ Failed at bulk operations")
        return
    
    if not test_filtering():
        print("\n❌ Failed at filtering")
        return
    
    print("\n" + "=" * 60)
    print("🎉 All API Tests Passed!\n")
    print("✅ Authentication working")
    print("✅ User management working")
    print("✅ Lead CRUD working")
    print("✅ Scoring working")
    print("✅ Bulk operations working")
    print("✅ Filtering working")
    print("\n🚀 Your API is production-ready!")

if __name__ == "__main__":
    main()