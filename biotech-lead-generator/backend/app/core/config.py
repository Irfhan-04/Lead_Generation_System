"""
Core configuration for the application
Manages environment variables and settings
"""

from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import secrets


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # App Info
    APP_NAME: str = "Biotech Lead Generator API"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "Production API for biotech lead generation"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js dev
        "http://localhost:8000",  # FastAPI dev
        "https://yourdomain.com",  # Production frontend
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)
    
    # Database - Supabase PostgreSQL
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    DATABASE_URL: str  # Format: postgresql://user:pass@host:port/dbname
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Redis - Upstash
    REDIS_URL: str  # Format: redis://default:password@host:port
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    REDIS_SESSION_TTL: int = 86400  # 24 hours
    
    # Celery
    CELERY_BROKER_URL: str  # Usually same as REDIS_URL
    CELERY_RESULT_BACKEND: str  # Usually same as REDIS_URL
    
    # Email - Resend
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str = "noreply@yourdomain.com"
    
    # Object Storage - Supabase Storage (FREE alternative to R2)
    SUPABASE_STORAGE_BUCKET: str = "exports"  # Bucket name for file exports
    # Note: Uses SUPABASE_URL and SUPABASE_SERVICE_KEY from above
    
    # Monitoring - Sentry
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: str = "production"
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    
    # External APIs
    PUBMED_EMAIL: str
    PUBMED_API_KEY: Optional[str] = None
    
    PROXYCURL_API_KEY: Optional[str] = None
    HUNTER_API_KEY: Optional[str] = None
    CLEARBIT_API_KEY: Optional[str] = None
    CRUNCHBASE_API_KEY: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Subscription Limits
    FREE_TIER_LEADS_PER_MONTH: int = 100
    PRO_TIER_LEADS_PER_MONTH: int = 1000
    TEAM_TIER_LEADS_PER_MONTH: int = 5000
    
    # Scoring Weights (defaults)
    DEFAULT_ROLE_WEIGHT: int = 30
    DEFAULT_PUBLICATION_WEIGHT: int = 40
    DEFAULT_FUNDING_WEIGHT: int = 20
    DEFAULT_LOCATION_WEIGHT: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # or "text"
    
    # Feature Flags
    ENABLE_ML_SCORING: bool = False
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    ENABLE_WEBHOOKS: bool = True
    ENABLE_BACKGROUND_JOBS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Database URL construction helper
def get_database_url() -> str:
    """
    Construct database URL from Supabase credentials
    """
    return settings.DATABASE_URL


def get_async_database_url() -> str:
    """
    Construct async database URL (postgresql+asyncpg://)
    """
    url = settings.DATABASE_URL
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://")
    return url


# Redis URL helper
def get_redis_url() -> str:
    """
    Get Redis URL for connections
    """
    return settings.REDIS_URL


# Supabase client helper
def get_supabase_client():
    """
    Create Supabase client
    """
    from supabase import create_client
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


# Environment check
def is_production() -> bool:
    """Check if running in production"""
    return settings.SENTRY_ENVIRONMENT == "production"


def is_development() -> bool:
    """Check if running in development"""
    return settings.DEBUG or settings.SENTRY_ENVIRONMENT == "development"


# Export settings
__all__ = [
    "settings",
    "Settings",
    "get_database_url",
    "get_async_database_url",
    "get_redis_url",
    "get_supabase_client",
    "is_production",
    "is_development",
]