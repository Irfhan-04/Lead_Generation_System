# Database Migration Setup Guide

## Prerequisites

Before running migrations, ensure you have:

1. **`.env` file** in the `backend/` directory with at least:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

2. **All required environment variables** (see `app/core/config.py` for full list):
   - `DATABASE_URL` (required for migrations)
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_SERVICE_KEY`
   - `REDIS_URL`
   - `CELERY_BROKER_URL`
   - `CELERY_RESULT_BACKEND`
   - `RESEND_API_KEY`
   - `PUBMED_EMAIL`

## Step 1: Verify Alembic Configuration

The `alembic.ini` file is already configured in `backend/alembic.ini`.

## Step 2: Verify env.py Configuration

The `alembic/env.py` file is configured to:
- Load `.env` file automatically
- Import all 5 models (User, Lead, Search, Export, Pipeline)
- Handle IPv4 resolution for database connections
- Test database connection before running migrations

## Step 3: Create Initial Migration

Once your `.env` file is set up, run:

```bash
cd backend
python -m alembic revision --autogenerate -m "Initial schema"
```

This will create a migration file in `alembic/versions/` with a name like:
`2024_12_30_1430-abc123_initial_schema.py`

## Step 4: Review Migration File

Open the generated migration file and verify it includes:
- `users` table
- `leads` table
- `searches` table
- `exports` table
- `pipelines` table

## Step 5: Apply Migration to Database

Run the migration:

```bash
python -m alembic upgrade head
```

You should see output like:
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Initial schema
```

## Step 6: Verify in Supabase

1. Go to your Supabase project dashboard
2. Navigate to Table Editor
3. You should see 5 new tables:
   - `users`
   - `leads`
   - `searches`
   - `exports`
   - `pipelines`

## Step 7: Test Models

Run the test script to verify all models work:

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

## Troubleshooting

### Issue: "DATABASE_URL is required for migrations"

**Solution**: Create a `.env` file in the `backend/` directory with your database connection string.

### Issue: IPv6 Connection Error - "Network is unreachable"

**Symptoms**: 
- Error: `connection to server at "... (2406:da1a:...), port 5432 failed: Network is unreachable`
- Warning: `Could not resolve db.xxx.supabase.co to IPv4`

**Solutions**:

#### Option 1: Use Supabase Connection Pooler (Recommended)
The connection pooler has better IPv4 support. Update your `DATABASE_URL`:

1. Go to Supabase Dashboard > Settings > Database
2. Find "Connection string" section
3. Select "Connection pooling" mode
4. Copy the connection string (it will have `pooler.supabase.com` instead of `db.xxx.supabase.co`)
5. Update your `.env` file with the new connection string

#### Option 2: Manually Set IPv4 Address
If you know the IPv4 address of your Supabase database:

1. Find the IPv4 address (you can use `nslookup` or `dig` commands)
2. Set environment variable:
   ```bash
   export DATABASE_IPV4_ADDRESS="your.ipv4.address.here"
   ```
3. Run the migration again

#### Option 3: Use Direct IPv4 Connection String
Get the direct connection string from Supabase:
1. Go to Supabase Dashboard > Settings > Database
2. Look for "Connection string" with "Direct connection" option
3. Some Supabase projects provide IPv4-specific connection strings

#### Option 4: Enable IPv6 Support
If you're in a restricted network environment (like some cloud IDEs):
1. Use a VPN that supports IPv6
2. Contact your network administrator
3. Use a different network environment

#### Option 5: Use Supabase's Transaction Mode Pooler
The transaction mode pooler often has better compatibility:

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?pgbouncer=true
```

### Issue: "relation 'users' already exists"

**Solution**: The tables already exist. You can either:
1. Drop existing tables (⚠️ **WARNING**: This deletes all data!)
2. Use `alembic stamp head` to mark current state as migrated

### Issue: Connection timeout

**Solution**: 
1. Check your `DATABASE_URL` format
2. Verify your Supabase project is active
3. Check firewall/network settings
4. Run: `python scripts/test_db_direct.py`

## Next Steps

After migrations are complete:
1. ✅ All 5 models are ready to use
2. ✅ You can start using the API endpoints
3. ✅ Background jobs can process leads
4. ✅ Export functionality is available

## Additional Resources

- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

