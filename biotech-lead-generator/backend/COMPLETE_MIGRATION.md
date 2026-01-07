# Complete Migration Tasks - Step by Step Guide

## ✅ What's Already Done

1. ✅ Alembic configuration (`alembic.ini` and `alembic/env.py`)
2. ✅ Enhanced IPv4 resolution and error handling
3. ✅ Helper script created (`scripts/create_migration.py`)
4. ✅ Versions directory created (`alembic/versions/`)
5. ✅ Model testing script (`scripts/test_models.py`)
6. ✅ Documentation and troubleshooting guides

## 🎯 Tasks to Complete

### Task 1: Create Initial Alembic Migration

**Prerequisites:**
- `.env` file in `backend/` directory with `DATABASE_URL`
- Database connection working (IPv4 compatible)

**Option A: Using Helper Script (Recommended)**
```bash
cd backend
python scripts/create_migration.py
```

**Option B: Direct Alembic Command**
```bash
cd backend
python -m alembic revision --autogenerate -m "Initial schema"
```

**Expected Output:**
- Migration file created in `alembic/versions/`
- File name like: `2024_12_30_1430-abc123_initial_schema.py`
- Should include all 5 tables: users, leads, searches, exports, pipelines

**If You Get IPv6 Connection Error:**
1. Use Supabase Connection Pooler (see `MIGRATION_SETUP.md`)
2. Or set `DATABASE_IPV4_ADDRESS` environment variable
3. Or use transaction mode pooler endpoint

---

### Task 2: Review the Generated Migration File

**Location:** `alembic/versions/[timestamp]-[revision]_initial_schema.py`

**What to Check:**
1. ✅ `users` table creation
2. ✅ `leads` table creation with foreign key to users
3. ✅ `searches` table creation with foreign key to users
4. ✅ `exports` table creation with foreign keys
5. ✅ `pipelines` table creation with foreign key to users
6. ✅ All indexes are created
7. ✅ All constraints are correct

**Example Migration Structure:**
```python
def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        # ... more columns
    )
    
    # Create leads table
    op.create_table('leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        # ... more columns
    )
    
    # ... other tables
```

**If Something Looks Wrong:**
- Review the model files in `app/models/`
- Compare with the migration file
- You can edit the migration file before applying it

---

### Task 3: Apply Migration to Database

**Command:**
```bash
cd backend
python -m alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Initial schema
```

**Verify in Supabase:**
1. Go to Supabase Dashboard → Table Editor
2. You should see 5 new tables:
   - ✅ `users`
   - ✅ `leads`
   - ✅ `searches`
   - ✅ `exports`
   - ✅ `pipelines`

**Test the Models:**
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

---

## 🔧 Troubleshooting

### Issue: "DATABASE_URL is required"
**Solution:** Create `.env` file with your database connection string

### Issue: IPv6 Connection Error
**Solution:** See `MIGRATION_SETUP.md` for detailed solutions:
- Use Supabase Connection Pooler (recommended)
- Set `DATABASE_IPV4_ADDRESS` environment variable
- Use transaction mode pooler

### Issue: "relation 'users' already exists"
**Solution:** Tables already exist. Options:
1. Drop tables (⚠️ deletes data): `DROP TABLE users, leads, searches, exports, pipelines CASCADE;`
2. Mark as migrated: `python -m alembic stamp head`

### Issue: Migration file not generated
**Check:**
1. Database connection is working
2. All models are imported in `alembic/env.py`
3. No syntax errors in model files

---

## 📋 Quick Checklist

- [ ] `.env` file created with `DATABASE_URL`
- [ ] Database connection tested (no IPv6 errors)
- [ ] Migration file created (`alembic revision --autogenerate`)
- [ ] Migration file reviewed (all 5 tables present)
- [ ] Migration applied (`alembic upgrade head`)
- [ ] Tables verified in Supabase dashboard
- [ ] Models tested (`python scripts/test_models.py`)

---

## 🚀 Once Complete

After completing all 3 tasks:
1. ✅ Database schema is ready
2. ✅ All 5 models are functional
3. ✅ API endpoints can use the database
4. ✅ Background jobs can process data
5. ✅ Export functionality is available

**Next Steps:**
- Start using the API
- Seed initial data if needed
- Set up background workers
- Configure additional features

---

## 📚 Additional Resources

- `MIGRATION_SETUP.md` - Detailed setup guide
- `MIGRATION_STATUS.md` - Current status summary
- `scripts/create_migration.py` - Helper script
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)

