"""
Test script to verify schemas work correctly
"""

from app.schemas import (
    UserRegister, UserLogin, LeadCreate,
    Token, LeadFilters, PaginationParams
)
from pydantic import ValidationError
import json


def test_user_registration():
    """Test user registration validation"""
    print("\n=== Testing User Registration ===")
    
    # Valid registration
    try:
        user = UserRegister(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        print(f"✅ Valid registration: {user.email}")
    except ValidationError as e:
        print(f"❌ Error: {e}")
    
    # Invalid password (no special char)
    try:
        user = UserRegister(
            email="test@example.com",
            password="SecurePass123",
            full_name="Test User"
        )
        print("❌ Should have failed - password missing special char")
    except ValidationError as e:
        print(f"✅ Correctly rejected weak password")
    
    # Invalid email
    try:
        user = UserRegister(
            email="not-an-email",
            password="SecurePass123!",
            full_name="Test User"
        )
        print("❌ Should have failed - invalid email")
    except ValidationError as e:
        print(f"✅ Correctly rejected invalid email")


def test_lead_creation():
    """Test lead creation validation"""
    print("\n=== Testing Lead Creation ===")
    
    # Valid lead
    try:
        lead = LeadCreate(
            name="Dr. Sarah Mitchell",
            title="Director of Toxicology",
            company="Moderna",
            email="sarah@modernatx.com",
            tags=["high-priority", "conference-speaker"]
        )
        print(f"✅ Valid lead created: {lead.name}")
        print(f"   Tags (cleaned): {lead.tags}")
    except ValidationError as e:
        print(f"❌ Error: {e}")
    
    # Test tag cleaning
    try:
        lead = LeadCreate(
            name="Test Lead",
            tags=["  High Priority  ", "CONFERENCE SPEAKER", "  "]
        )
        print(f"✅ Tags cleaned: {lead.tags}")
    except ValidationError as e:
        print(f"❌ Error: {e}")


def test_pagination():
    """Test pagination parameters"""
    print("\n=== Testing Pagination ===")
    
    # Valid pagination
    try:
        pagination = PaginationParams(page=2, size=50)
        print(f"✅ Valid pagination: page {pagination.page}, size {pagination.size}")
        print(f"   Offset: {pagination.get_offset()}")
    except ValidationError as e:
        print(f"❌ Error: {e}")
    
    # Invalid page (< 1)
    try:
        pagination = PaginationParams(page=0, size=50)
        print("❌ Should have failed - page < 1")
    except ValidationError as e:
        print(f"✅ Correctly rejected invalid page")
    
    # Invalid size (> 100)
    try:
        pagination = PaginationParams(page=1, size=200)
        print("❌ Should have failed - size > 100")
    except ValidationError as e:
        print(f"✅ Correctly rejected invalid size")


def test_filters():
    """Test lead filters"""
    print("\n=== Testing Lead Filters ===")
    
    try:
        filters = LeadFilters(
            search="director toxicology",
            min_score=70,
            priority_tier="HIGH",
            has_email=True,
            tags=["high-priority"]
        )
        print(f"✅ Valid filters created")
        print(f"   Search: {filters.search}")
        print(f"   Min score: {filters.min_score}")
        print(f"   Priority: {filters.priority_tier}")
    except ValidationError as e:
        print(f"❌ Error: {e}")


def test_json_serialization():
    """Test JSON serialization"""
    print("\n=== Testing JSON Serialization ===")
    
    lead = LeadCreate(
        name="Dr. Test",
        title="Scientist",
        company="Test Corp",
        email="test@example.com",
        tags=["test"]
    )
    
    # Convert to JSON
    json_str = lead.model_dump_json()
    print(f"✅ Serialized to JSON:")
    print(f"   {json_str[:100]}...")
    
    # Parse from JSON
    parsed = LeadCreate.model_validate_json(json_str)
    print(f"✅ Parsed from JSON: {parsed.name}")


if __name__ == "__main__":
    print("🧪 Testing Pydantic Schemas\n")
    print("=" * 60)
    
    test_user_registration()
    test_lead_creation()
    test_pagination()
    test_filters()
    test_json_serialization()
    
    print("\n" + "=" * 60)
    print("🎉 All schema tests completed!")