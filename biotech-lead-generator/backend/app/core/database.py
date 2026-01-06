"""
Database configuration and session management
Supports both sync and async operations
"""

from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import NullPool

from app.core.config import settings, get_database_url, get_async_database_url


# Create base class for models
Base = declarative_base()


# ============================================================================
# SYNC DATABASE (for Alembic migrations and simple operations)
# ============================================================================

# Create sync engine
sync_engine = create_engine(
    get_database_url(),
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Create sync session factory
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting sync database session
    
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# ASYNC DATABASE (for FastAPI async endpoints - RECOMMENDED)
# ============================================================================

# Create async engine
# Note: NullPool doesn't accept pool_size, max_overflow, pool_timeout
engine_kwargs = {
    "pool_pre_ping": True,
    "echo": settings.DEBUG,
}

# Only add pooling params if not using NullPool
if settings.DEBUG:
    engine_kwargs["poolclass"] = NullPool
else:
    engine_kwargs.update({
        "pool_size": settings.DATABASE_POOL_SIZE,
        "max_overflow": settings.DATABASE_MAX_OVERFLOW,
        "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
    })

async_engine = create_async_engine(
    get_async_database_url(),
    **engine_kwargs
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(Item))
            items = result.scalars().all()
            return items
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

async def init_db() -> None:
    """
    Initialize database
    Creates all tables defined in models
    
    NOTE: In production, use Alembic migrations instead
    """
    async with async_engine.begin() as conn:
        # Import all models here to ensure they're registered
        from app.models import user, lead, search, export, pipeline
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections
    Call this on application shutdown
    """
    await async_engine.dispose()


def init_db_sync() -> None:
    """
    Synchronous database initialization
    Used by Alembic and scripts
    """
    # Import all models
    from app.models import user, lead, search, export, pipeline
    
    # Create all tables
    Base.metadata.create_all(bind=sync_engine)


# ============================================================================
# DATABASE UTILITIES
# ============================================================================

async def check_db_connection() -> bool:
    """
    Check if database is accessible
    Returns True if connection successful
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def check_db_connection_sync() -> bool:
    """
    Sync version of database connection check
    """
    try:
        with SyncSessionLocal() as session:
            session.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


# ============================================================================
# TRANSACTION HELPERS
# ============================================================================

class DatabaseTransaction:
    """
    Context manager for database transactions
    
    Usage:
        async with DatabaseTransaction() as db:
            user = User(email="test@example.com")
            db.add(user)
            # Automatically commits on success, rolls back on error
    """
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()


# ============================================================================
# PAGINATION HELPER
# ============================================================================

from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    """
    Generic pagination response
    """
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        from_attributes = True


async def paginate(
    query,
    page: int = 1,
    size: int = 50,
    max_size: int = 100
) -> tuple:
    """
    Paginate a SQLAlchemy query
    
    Returns:
        Tuple of (items, total_count)
    """
    # Limit size
    size = min(size, max_size)
    
    # Calculate offset
    offset = (page - 1) * size
    
    # Get total count
    from sqlalchemy import select, func
    total = await query.session.scalar(
        select(func.count()).select_from(query.statement.subquery())
    )
    
    # Get paginated items
    query = query.offset(offset).limit(size)
    items = (await query.session.execute(query.statement)).scalars().all()
    
    return items, total


# Export all
__all__ = [
    "Base",
    "sync_engine",
    "async_engine",
    "SyncSessionLocal",
    "AsyncSessionLocal",
    "get_db",
    "get_async_db",
    "init_db",
    "close_db",
    "init_db_sync",
    "check_db_connection",
    "check_db_connection_sync",
    "DatabaseTransaction",
    "Page",
    "paginate",
]