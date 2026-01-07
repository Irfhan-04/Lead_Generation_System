"""
Core configuration for the application
Manages environment variables and settings with IPv4 enforcement
"""

from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import secrets
import socket
import os


def get_ipv4_address(hostname: str) -> str:
    """
    Resolve hostname to IPv4 address to avoid IPv6 issues
    This is critical for environments that don't support IPv6
    """
    try:
        # Force IPv4 resolution
        addr_info = socket.getaddrinfo(
            hostname, 
            None, 
            socket.AF_INET,  # Force IPv4
            socket.SOCK_STREAM
        )
        if addr_info:
            ipv4_address = addr_info[0][4][0]
            print(f"✅ Resolved {hostname} to IPv4: {ipv4_address}")
            return ipv4_address
    except Exception as e:
        print(f"⚠️  Could not resolve {hostname} to IPv4: {e}")
    
    return hostname


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
        "http://localhost:3000",
        "http://localhost:8000",
        "https://yourdomain.com",
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
    
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Force IPv4 for database connections
    USE_IPV4_ONLY: bool = True
    
    # Redis - Upstash
    REDIS_URL: str
    REDIS_CACHE_TTL: int = 3600
    REDIS_SESSION_TTL: int = 86400
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # Email - Resend
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str = "noreply@yourdomain.com"
    
    # Object Storage
    SUPABASE_STORAGE_BUCKET: str = "exports"
    
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
    
    # Scoring Weights
    DEFAULT_ROLE_WEIGHT: int = 30
    DEFAULT_PUBLICATION_WEIGHT: int = 40
    DEFAULT_FUNDING_WEIGHT: int = 20
    DEFAULT_LOCATION_WEIGHT: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
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


def get_database_url(force_ipv4: bool = None) -> str:
    """
    Get database URL with IPv4 enforcement
    """
    if force_ipv4 is None:
        force_ipv4 = settings.USE_IPV4_ONLY
    
    url = settings.DATABASE_URL
    
    # Ensure psycopg2 driver for sync operations
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
    
    # Force IPv4 if enabled
    if force_ipv4:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        
        # Get IPv4 address for hostname
        if parsed.hostname and not parsed.hostname.replace('.', '').isdigit():
            ipv4_address = get_ipv4_address(parsed.hostname)
            
            # Rebuild netloc with IPv4
            netloc = f"{parsed.username}:{parsed.password}@{ipv4_address}"
            if parsed.port:
                netloc += f":{parsed.port}"
            
            # Reconstruct URL
            url = urlunparse((
                parsed.scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
    
    return url


def get_async_database_url() -> str:
    """
    Get async database URL (asyncpg driver)
    """
    url = get_database_url(force_ipv4=True)
    
    # Convert to asyncpg for async operations
    if url.startswith("postgresql+psycopg2://"):
        url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    
    return url


def get_redis_url() -> str:
    """
    Get Redis URL
    """
    return settings.REDIS_URL


def get_supabase_client():
    """
    Create Supabase client
    """
    from supabase import create_client
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


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