"""
Alembic migration environment with IPv4 enforcement
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import config and models
from app.core.config import settings, get_database_url
from app.core.database import Base, SYNC_CONNECT_ARGS

# Import all models so Alembic can detect them
from app.models import (
    User, Lead, Search, Export, Pipeline
)

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = Base.metadata

# Get database URL with IPv4 enforcement
database_url = get_database_url(force_ipv4=True)
config.set_main_option("sqlalchemy.url", database_url)

print(f"🔗 Using database URL: {database_url.split('@')[0]}@...")


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Get configuration
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")
    
    # Add connection pool settings
    configuration["sqlalchemy.pool_pre_ping"] = "True"
    configuration["sqlalchemy.pool_recycle"] = "3600"
    
    # Create engine with custom connect_args
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Use NullPool for migrations
        connect_args=SYNC_CONNECT_ARGS,
    )

    # Test connection before running migrations
    print("🧪 Testing database connection...")
    try:
        with connectable.connect() as test_conn:
            result = test_conn.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your DATABASE_URL in .env")
        print("2. Verify Supabase project is active")
        print("3. Run: python scripts/test_db_direct.py")
        raise

    # Run migrations
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()