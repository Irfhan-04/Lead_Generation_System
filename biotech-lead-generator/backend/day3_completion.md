# 📅 DAY 3 COMPLETION - Authentication System

## ✅ What You've Created Today

You now have **complete authentication infrastructure**:

1. ✅ **Dependencies** (`app/core/deps.py`) - 300+ lines
   - JWT token extraction
   - User authentication from token/API key
   - Subscription tier checking
   - Rate limiting
   - Quota management

2. ✅ **Auth Endpoints** (`app/api/v1/endpoints/auth.py`) - 400+ lines
   - User registration
   - Login with JWT tokens
   - Token refresh
   - Email verification
   - Password reset flow
   - User profile endpoint

3. ✅ **API Router** (`app/api/v1/api.py`)
   - Organized endpoint structure
   - Ready for more endpoints

4. ✅ **Main Application** (`app/main.py`) - 250+ lines
   - FastAPI app initialization
   - Middleware configuration
   - Error handling
   - Health check
   - Database/Redis lifecycle

**Total: 1000+ lines of production-ready code!**

---

## 🎯 FILE CHECKLIST

Make sure you have these files:

- [ ] `app/core/deps.py` - Dependencies
- [ ] `app/api/v1/endpoints/__init__.py` - Empty file
- [ ] `app/api/v1/endpoints/auth.py` - Auth endpoints
- [ ] `app/api/v1/__init__.py` - Empty file
- [ ] `app/api/v1/api.py` - API router
- [ ] `app/api/__init__.py` - Empty file
- [ ] `app/main.py` - Main application

---

## 🚀 RUN YOUR API!

### Step 1: Start the Server

```bash
cd backend

# Make sure virtual environment is activated
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run the application
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Starting Biotech Lead Generator API...
Environment: development
Debug mode: True
✅ Database connection established
✅ Redis connection established
🚀 API is ready!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Visit API Documentation

Open your browser and go to:

**Swagger UI (Interactive):**
```
http://localhost:8000/docs
```

**ReDoc (Documentation):**
```
http://localhost:8000/redoc
```

You should see:
- **Authentication** section with 8 endpoints
- Interactive "Try it out" buttons
- Request/response schemas
- Example values

### Step 3: Test Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2024-12-30T12:00:00Z"
}
```

---

## 🧪 TESTING WITH POSTMAN

### Setup Postman Collection

1. **Import OpenAPI Spec**
   - Go to Postman
   - Click "Import"
   - Enter URL: `http://localhost:8000/api/v1/openapi.json`
   - Click "Import"

2. **Create Environment**
   - Name: "Biotech Lead Gen - Local"
   - Variables:
     - `base_url`: `http://localhost:8000/api/v1`
     - `access_token`: (leave empty for now)

### Test Flow:

#### 1. Register User

**Request:**
```
POST {{base_url}}/auth/register

Body (JSON):
{
  "email": "test@example.com",
  "password": "Test123!@#",
  "full_name": "Test User"
}
```

**Expected Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully...",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

**Check Console:**
You should see email verification link in server logs!

#### 2. Verify Email

**Copy token from console, then:**

```
GET {{base_url}}/auth/verify-email/YOUR_TOKEN_HERE
```

**Expected Response (200):**
```json
{
  "message": "Email verified successfully!"
}
```

#### 3. Login

**Request:**
```
POST {{base_url}}/auth/login

Body (JSON):
{
  "email": "test@example.com",
  "password": "Test123!@#"
}
```

**Expected Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Save the access_token to your Postman environment!**

#### 4. Get Profile (Protected Route)

**Request:**
```
GET {{base_url}}/auth/me

Headers:
Authorization: Bearer {{access_token}}
```

**Expected Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "test@example.com",
  "full_name": "Test User",
  "subscription_tier": "free",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-12-30T12:00:00Z",
  ...
}
```

#### 5. Test Token Refresh

**Request:**
```
POST {{base_url}}/auth/refresh

Body (JSON):
{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

**Expected Response (200):**
```json
{
  "access_token": "NEW_ACCESS_TOKEN",
  "refresh_token": "SAME_REFRESH_TOKEN",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### 6. Test Password Reset Flow

**Request Reset:**
```
POST {{base_url}}/auth/forgot-password

Body (JSON):
{
  "email": "test@example.com"
}
```

**Check console for reset link, then:**

```
POST {{base_url}}/auth/reset-password

Body (JSON):
{
  "token": "RESET_TOKEN_FROM_CONSOLE",
  "new_password": "NewPass456@"
}
```

**Try logging in with new password!**

---

## 🧪 AUTOMATED TESTING SCRIPT

Create `scripts/test_auth.py`:

```python
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
```

**Run the test:**
```bash
pip install requests  # If not installed
python scripts/test_auth.py
```

Expected output:
```
🧪 Testing Authentication Flow

============================================================

1️⃣  Testing Registration...
✅ Registration successful
   User ID: 123e4567-e89b-12d3-a456-426614174000

2️⃣  Testing Login...
✅ Login successful
   Access token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Expires in: 86400 seconds

3️⃣  Testing Get Profile...
✅ Got user profile
   Email: autotest@example.com
   Name: Auto Test User
   Tier: free
   Verified: False

4️⃣  Testing Token Refresh...
✅ Token refresh successful
   New token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

5️⃣  Testing Logout...
✅ Logout successful

6️⃣  Testing Invalid Token...
✅ Invalid token correctly rejected

============================================================
🎉 Authentication Tests Complete!
```

---

## 📚 UNDERSTANDING WHAT YOU BUILT

### Authentication Flow

```
User Registration
    ↓
Email Verification (optional for testing)
    ↓
Login → Receive JWT Tokens
    ↓
Use Access Token for API Requests
    ↓
Token Expires? → Use Refresh Token
    ↓
Continue Making Requests
```

### JWT Token Structure

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user_id",        # Subject (user ID)
  "exp": 1735574400,       # Expiration timestamp
  "iat": 1735488000,       # Issued at timestamp
  "type": "access"         # Token type
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)
```

### Dependency Injection

```python
# Without authentication
@app.get("/public")
async def public_route():
    return {"message": "Anyone can access"}

# Requires authentication
@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello {user.email}"}

# Requires specific subscription
@app.post("/premium")
async def premium_route(user: User = Depends(require_pro)):
    return {"message": "Pro users only"}
```

### Security Layers

1. **Password Hashing** - Passwords never stored in plaintext
2. **JWT Tokens** - Stateless authentication
3. **Token Expiration** - Access tokens expire in 24h
4. **Refresh Tokens** - Long-lived (7d) for getting new access tokens
5. **Email Verification** - Confirm user owns email
6. **Rate Limiting** - Prevent abuse
7. **Quota Management** - Subscription-based limits

---

## ✅ DAY 3 CHECKLIST

- [ ] All auth files created
- [ ] API starts without errors
- [ ] Can access `/docs` endpoint
- [ ] Health check returns "healthy"
- [ ] Can register a new user
- [ ] Can login and receive tokens
- [ ] Can access protected `/auth/me` route
- [ ] Token refresh works
- [ ] Password reset flow works
- [ ] Automated test script passes

---

## 🚀 WHAT'S NEXT - DAY 4

Tomorrow we'll build:

**User & Lead Management Endpoints**

1. **User Endpoints** (`app/api/v1/endpoints/users.py`)
   - `PUT /users/me` - Update profile
   - `PUT /users/me/password` - Change password
   - `PUT /users/me/preferences` - Update preferences
   - `GET /users/me/usage` - Get usage stats
   - `POST /users/me/api-keys` - Generate API key
   - `DELETE /users/me` - Delete account

2. **Lead Endpoints** (`app/api/v1/endpoints/leads.py`)
   - `GET /leads` - List leads (with pagination)
   - `POST /leads` - Create lead
   - `GET /leads/{id}` - Get lead details
   - `PUT /leads/{id}` - Update lead
   - `DELETE /leads/{id}` - Delete lead
   - `POST /leads/bulk` - Bulk import

**Why This Order?**
- Auth is working, now build on top of it
- Users can manage their accounts
- Leads are the core feature
- Once CRUD works, we can add advanced features

---

## 🆘 TROUBLESHOOTING

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure you're in backend/ directory
cd backend

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Database connection fails

**Solution:**
1. Check `.env` has correct `DATABASE_URL`
2. Verify Supabase project is running
3. Test connection: `python -c "from app.core.database import check_db_connection_sync; print(check_db_connection_sync())"`

### Issue: Redis connection fails

**Solution:**
1. Check `.env` has correct `REDIS_URL`
2. Test Upstash dashboard shows database is active
3. Try: `redis-cli -u $REDIS_URL ping`

### Issue: JWT token errors

**Solution:**
1. Check `SECRET_KEY` in `.env` is set
2. Make sure token hasn't expired
3. Verify token format: `Bearer <token>`

### Issue: Email verification not working

**Solution:**
- For now, emails are logged to console
- Check server logs for verification links
- In production, integrate real email service (Resend)

---

## 📊 PROGRESS TRACKER

```
Week 1: Backend Foundation
├── Day 1: Database Models ✅
├── Day 2: Pydantic Schemas ✅
├── Day 3: Authentication ✅  ← YOU ARE HERE
└── Day 4: CRUD Endpoints (Tomorrow)

Progress: 75% of Week 1 complete! 🎉
```

---

## 🎓 KEY CONCEPTS LEARNED

### 1. FastAPI Dependencies

Powerful way to inject reusable logic:
- Authentication
- Database sessions
- Permission checks
- Rate limiting

### 2. JWT Authentication

Stateless tokens that contain user info:
- No database lookup needed
- Can be verified with secret key
- Include expiration time
- Can't be revoked (implement blacklist if needed)

### 3. Middleware

Functions that run before/after requests:
- CORS (cross-origin requests)
- Timing (performance monitoring)
- Logging (request/response tracking)
- Error handling (global exception catching)

### 4. Async/Await

All database and Redis operations are async:
- Better performance
- Handle multiple requests concurrently
- Non-blocking I/O

---

## ✅ YOU'RE READY FOR DAY 4!

Excellent work! Your authentication system is **production-ready**! 🎉

You now have:
- ✅ Secure user registration
- ✅ JWT-based authentication
- ✅ Email verification
- ✅ Password reset
- ✅ Protected endpoints
- ✅ Subscription tier checking
- ✅ Rate limiting & quotas

**Questions before we continue?**

Ready to say: **"Day 3 complete, ready for Day 4"** ? 🚀
