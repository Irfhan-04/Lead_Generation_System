# Migration Run Instructions

## Current Situation

✅ **Backend server is running and connected to PostgreSQL**  
✅ **All tables have been initialized**  
✅ **Alembic configuration is complete**  

⚠️ **Migration cannot be run from Windows environment** (DNS resolution issue)

## Solution: Run Migration from Server Environment

Since your backend server is running and connected, you should run the migration commands **from that environment** (Codespaces/Server) where the database connection works.

## Step-by-Step Instructions

### Step 1: Create Initial Migration

**From your server environment** (where backend is running):

```bash
cd /workspaces/Lead_Generation_System/biotech-lead-generator/backend
python -m alembic revision --autogenerate -m "Initial schema"
```

**Expected Output:**
- Migration file created: `alembic/versions/2026_01_08_XXXX-XXXXXXXX_initial_schema.py`
- File should include all 5 tables: users, leads, searches, exports, pipelines

### Step 2: Review the Generated Migration File

**Location:** `alembic/versions/[timestamp]-[revision]_initial_schema.py`

**What to Verify:**
1. ✅ `users` table with all columns
2. ✅ `leads` table with foreign key to users
3. ✅ `searches` table with foreign key to users
4. ✅ `exports` table with foreign keys
5. ✅ `pipelines` table with foreign key to users
6. ✅ All indexes are created
7. ✅ All constraints (foreign keys, unique, etc.)

**Key Things to Check:**
- UUID primary keys
- JSONB columns for flexible data
- Foreign key constraints with CASCADE delete
- Indexes on frequently queried columns
- Enum types for status fields

### Step 3: Apply Migration to Database

**If tables already exist** (which they do based on your message):

You have two options:

#### Option A: Mark Current State as Migrated (Recommended if tables match models)

```bash
python -m alembic stamp head
```

This tells Alembic that the current database state matches the migration, without actually running it.

#### Option B: Apply Migration (if you want to ensure everything matches)

```bash
python -m alembic upgrade head
```

**Note:** If you get "relation already exists" errors, use Option A instead.

### Step 4: Verify Migration Status

```bash
python -m alembic current
```

Should show the revision ID of your migration.

### Step 5: Test Models

```bash
python scripts/test_models.py
```

Expected output:
```
✅ Created user: test@example.com (ID: uuid...)
✅ Created lead: Dr. Sarah Mitchell (Score: 85)
✅ Lead priority tier: HIGH
✅ Lead tags: ['high-priority', 'conference-speaker']
...
🎉 ALL TESTS PASSED!
```

## Quick Command Summary

```bash
# 1. Create migration (from server environment)
python -m alembic revision --autogenerate -m "Initial schema"

# 2. Review the file
cat alembic/versions/*_initial_schema.py

# 3. Apply or stamp migration
python -m alembic stamp head  # If tables already exist
# OR
python -m alembic upgrade head  # To apply changes

# 4. Verify
python -m alembic current

# 5. Test
python scripts/test_models.py
```

## Troubleshooting

### If "relation already exists" error:
- Use `alembic stamp head` to mark as migrated
- Or drop tables first (⚠️ deletes data): `DROP TABLE users, leads, searches, exports, pipelines CASCADE;`

### If migration file is empty:
- Check that all models are imported in `alembic/env.py`
- Verify database connection is working
- Check for syntax errors in model files

## Next Steps After Migration

Once migration is complete:
1. ✅ Database schema is version-controlled
2. ✅ Future schema changes can use migrations
3. ✅ All 5 models are ready to use
4. ✅ API endpoints can use the database
5. ✅ Background jobs can process data
