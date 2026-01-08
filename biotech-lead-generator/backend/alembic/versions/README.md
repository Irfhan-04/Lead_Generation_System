# Alembic Migration Versions

This directory contains Alembic migration files.

## Creating Your First Migration

When you have database access configured, run:

```bash
python -m alembic revision --autogenerate -m "Initial schema"
```

Or use the helper script:

```bash
python scripts/create_migration.py
```

## Expected Migration File

After running the migration command, you should see a file like:
- `2024_12_30_1430-abc123_initial_schema.py`

This file will contain the SQLAlchemy table definitions for:
- `users` table
- `leads` table  
- `searches` table
- `exports` table
- `pipelines` table

## Applying Migrations

Once the migration file is created, apply it with:

```bash
python -m alembic upgrade head
```

## Troubleshooting

If you encounter connection issues:
1. Check `MIGRATION_SETUP.md` for troubleshooting guide
2. Ensure `.env` file has `DATABASE_URL` set
3. For IPv6 issues, use Supabase Connection Pooler

