# 📅 DAY 2 COMPLETION - Pydantic Schemas

## ✅ What You've Created Today

You now have **complete API contract layer**:

1. ✅ **Base Schemas** - Reusable patterns
2. ✅ **Token Schemas** - JWT authentication
3. ✅ **User Schemas** - Registration, login, profile
4. ✅ **Lead Schemas** - CRUD operations with validation
5. ✅ **Search/Export/Pipeline Schemas** - Supporting features

**Total: 40+ schema classes** with full validation!

---

## 🎯 FILE CHECKLIST

Make sure you have these files in `backend/app/schemas/`:

- [ ] `__init__.py` - Package initialization
- [ ] `base.py` - Base schemas and common patterns
- [ ] `token.py` - Authentication tokens
- [ ] `user.py` - User management
- [ ] `lead.py` - Lead operations
- [ ] Create `search.py` - Extract from the combined file
- [ ] Create `export.py` - Extract from the combined file
- [ ] Create `pipeline.py` - Extract from the combined file

---

## 📝 QUICK TASK: Split the Combined Schema File

The `schema_remaining` artifact contains 3 schemas in one file. Let's split them:

### Create `app/schemas/search.py`:

```python
"""Search Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from app.schemas.base import BaseSchema, TimestampSchema

# Copy the SearchCreate and SearchResponse classes here
# (from the schema_remaining artifact)
```

### Create `app/schemas/export.py`:

```python
"""Export Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.export import ExportFormat, ExportStatus

# Copy the ExportCreate and ExportResponse classes here
```

### Create `app/schemas/pipeline.py`:

```python
"""Pipeline Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.pipeline import PipelineStatus, PipelineSchedule

# Copy the Pipeline classes here
```

Then update `app/schemas/__init__.py` to import from these files.

---

## 🧪 TEST YOUR SCHEMAS

Create `scripts/test_schemas.py`:

```python
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
```

Run the test:

```bash
cd backend
python scripts/test_schemas.py
```

Expected output:
```
🧪 Testing Pydantic Schemas

============================================================

=== Testing User Registration ===
✅ Valid registration: test@example.com
✅ Correctly rejected weak password
✅ Correctly rejected invalid email

=== Testing Lead Creation ===
✅ Valid lead created: Dr. Sarah Mitchell
   Tags (cleaned): ['high-priority', 'conference-speaker']
✅ Tags cleaned: ['high priority', 'conference speaker']

=== Testing Pagination ===
✅ Valid pagination: page 2, size 50
   Offset: 50
✅ Correctly rejected invalid page
✅ Correctly rejected invalid size

=== Testing Lead Filters ===
✅ Valid filters created
   Search: director toxicology
   Min score: 70
   Priority: HIGH

=== Testing JSON Serialization ===
✅ Serialized to JSON:
   {"name":"Dr. Test","title":"Scientist","company":"Test Corp",...
✅ Parsed from JSON: Dr. Test

============================================================
🎉 All schema tests completed!
```

---

## 📚 UNDERSTANDING WHAT YOU BUILT

### Schema Types

**1. Request Schemas (Input)**
- `UserRegister`, `UserLogin` - Validate incoming data
- `LeadCreate`, `LeadUpdate` - API requests
- No `id` or timestamps (server generates these)

**2. Response Schemas (Output)**
- `UserProfile`, `LeadDetail` - Full data with timestamps
- `LeadList` - Simplified for list views
- Includes `id`, `created_at`, `updated_at`

**3. Filter/Query Schemas**
- `LeadFilters` - Search criteria
- `PaginationParams` - Page & size
- `SortParams` - Sorting options

**4. Wrapper Schemas**
- `SuccessResponse` - Standard success format
- `ErrorResponse` - Standard error format
- `PaginatedResponse` - Paginated data

### Validation Features

**Automatic:**
- Email format validation
- String length limits
- Number ranges (min/max)
- Enum validation

**Custom Validators:**
- Password strength checks
- Tag cleaning (lowercase, trim)
- URL format validation
- Scoring weight totals

### Schema Inheritance

```python
BaseSchema
├── TimestampSchema (adds created_at, updated_at)
├── UUIDSchema (adds id)
└── UserBase
    └── UserProfile (adds timestamps, preferences)
```

---

## 🎓 KEY CONCEPTS

### 1. Separation of Concerns

```
Database Model (ORM) ≠ API Schema (Pydantic)

User Model:
- password_hash ✅ (stored)
- usage_stats ✅ (internal)

UserProfile Schema:
- password_hash ❌ (never expose!)
- usage_stats ✅ (safe to show)
```

### 2. Request vs Response

```python
# Request (no ID, user provides data)
class LeadCreate(BaseModel):
    name: str
    email: EmailStr

# Response (includes ID, server adds metadata)
class LeadResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
    propensity_score: int  # Server calculated
```

### 3. Validation Layers

```
HTTP Request
    ↓
FastAPI receives JSON
    ↓
Pydantic validates (LeadCreate)
    ↓
If valid → convert to dict
    ↓
Create ORM model (Lead)
    ↓
Save to database
    ↓
Query database
    ↓
Load ORM model
    ↓
Convert to schema (LeadResponse)
    ↓
Return JSON
```

---

## 💡 BEST PRACTICES YOU'RE USING

### 1. Field Descriptions
```python
email: EmailStr = Field(..., description="User email address")
```
→ Auto-generates API documentation

### 2. Examples
```python
model_config = {
    "json_schema_extra": {
        "example": {"email": "user@example.com"}
    }
}
```
→ Shows in Swagger UI

### 3. Validators
```python
@field_validator('email')
@classmethod
def lowercase_email(cls, v: str) -> str:
    return v.lower()
```
→ Automatic data cleaning

### 4. Re-usable Patterns
```python
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 50
```
→ Use everywhere pagination is needed

---

## ✅ DAY 2 CHECKLIST

- [ ] All schema files created
- [ ] `__init__.py` exports all schemas
- [ ] Test script runs successfully
- [ ] All validations working
- [ ] JSON serialization works
- [ ] Understand request vs response schemas
- [ ] Know how to add custom validators

---

## 🚀 WHAT'S NEXT - DAY 3

Tomorrow we'll build:

**Dependencies & Authentication Endpoints**

1. **Dependencies** (`app/core/deps.py`)
   - `get_current_user` - Extract user from JWT
   - `get_current_active_user` - Verify user is active
   - `require_subscription_tier` - Check user tier
   - `get_db` - Database session dependency

2. **Auth Endpoints** (`app/api/v1/endpoints/auth.py`)
   - `POST /register` - User registration
   - `POST /login` - User login
   - `POST /logout` - User logout
   - `POST /refresh` - Refresh token
   - `POST /forgot-password` - Request reset
   - `POST /reset-password` - Reset with token

**Why This Order?**
- Dependencies are used by all endpoints
- Auth endpoints are simplest (good starting point)
- Once auth works, we can test entire flow

---

## 🎯 PREPARE FOR DAY 3

**Review these concepts:**
1. How JWT tokens work
2. Dependency injection in FastAPI
3. Password hashing (we already have it in `security.py`)
4. Database queries with async SQLAlchemy

---

## 🆘 TROUBLESHOOTING

### Issue: Import errors between schemas

**Solution:**
Put common schemas in `base.py`, import from there:
```python
# In lead.py
from app.schemas.base import BaseSchema, TimestampSchema
```

### Issue: Circular imports

**Solution:**
Use `from typing import TYPE_CHECKING` and string annotations:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.user import UserProfile

# Use string annotation
def get_user() -> "UserProfile":
    ...
```

### Issue: Validation not working

**Solution:**
Make sure validator is a classmethod:
```python
@field_validator('email')
@classmethod  # Don't forget this!
def lowercase_email(cls, v: str) -> str:
    return v.lower()
```

---

## 📊 PROGRESS TRACKER

```
Week 1: Backend Foundation
├── Day 1: Database Models ✅
├── Day 2: Pydantic Schemas ✅  ← YOU ARE HERE
├── Day 3: Dependencies & Auth (Tomorrow)
└── Day 4: First API Endpoints

Progress: 50% of Week 1 complete! 🎉
```

---

## ✅ YOU'RE READY FOR DAY 3!

Excellent progress! You now have:
- ✅ Database layer (Models)
- ✅ API contract layer (Schemas)
- 🔄 Next: Glue layer (Dependencies) + Auth

**Questions before we continue?** 

Ready to say: **"Day 2 complete, ready for Day 3"** ? 🚀
