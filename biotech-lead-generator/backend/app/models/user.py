"""
User Model - Authentication and user management
"""

from sqlalchemy import Boolean, Column, String, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class SubscriptionTier(str, enum.Enum):
    """
    Subscription tiers for the platform
    """
    FREE = "free"
    PRO = "pro"
    TEAM = "team"
    ENTERPRISE = "enterprise"


class User(Base):
    """
    User model for authentication and user management
    
    Attributes:
        id: Unique user identifier (UUID)
        email: User's email address (unique)
        password_hash: Hashed password (never store plain passwords!)
        full_name: User's full name
        subscription_tier: Current subscription level
        is_active: Whether user account is active
        is_verified: Whether email is verified
        is_superuser: Admin privileges
        api_keys: JSON array of API keys (hashed)
        usage_stats: JSON object tracking usage
        preferences: JSON object for user preferences
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login_at: Last login timestamp
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # Authentication
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    password_hash = Column(
        String(255),
        nullable=False
    )
    
    # Profile Information
    full_name = Column(String(255), nullable=True)
    
    # Subscription & Status
    subscription_tier = Column(
        SQLEnum(SubscriptionTier),
        default=SubscriptionTier.FREE,
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # API Keys (stored as hashed values in JSON array)
    api_keys = Column(JSONB, default=list, nullable=False)
    # Example: [{"name": "prod-key", "hash": "xxx", "created_at": "2024-01-01"}]
    
    # Usage Tracking (JSON for flexibility)
    usage_stats = Column(JSONB, default=dict, nullable=False)
    # Example: {
    #   "leads_created_this_month": 45,
    #   "searches_this_month": 12,
    #   "api_calls_today": 150,
    #   "last_reset_date": "2024-01-01"
    # }
    
    # User Preferences (JSON for flexibility)
    preferences = Column(JSONB, default=dict, nullable=False)
    # Example: {
    #   "email_notifications": true,
    #   "theme": "dark",
    #   "default_export_format": "csv",
    #   "scoring_weights": {"role": 30, "publication": 40, ...}
    # }
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    last_login_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    leads = relationship("Lead", back_populates="user", cascade="all, delete-orphan")
    searches = relationship("Search", back_populates="user", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="user", cascade="all, delete-orphan")
    pipelines = relationship("Pipeline", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.subscription_tier})>"
    
    # Helper Methods
    def get_monthly_lead_limit(self) -> int:
        """
        Get the monthly lead limit based on subscription tier
        """
        limits = {
            SubscriptionTier.FREE: 100,
            SubscriptionTier.PRO: 1000,
            SubscriptionTier.TEAM: 5000,
            SubscriptionTier.ENTERPRISE: 999999  # Effectively unlimited
        }
        return limits.get(self.subscription_tier, 100)
    
    def has_reached_lead_limit(self) -> bool:
        """
        Check if user has reached their monthly lead limit
        """
        leads_this_month = self.usage_stats.get("leads_created_this_month", 0)
        return leads_this_month >= self.get_monthly_lead_limit()
    
    def increment_usage(self, metric: str, amount: int = 1):
        """
        Increment a usage metric
        
        Args:
            metric: The metric to increment (e.g., "leads_created_this_month")
            amount: Amount to increment by (default: 1)
        """
        if not self.usage_stats:
            self.usage_stats = {}
        
        current_value = self.usage_stats.get(metric, 0)
        self.usage_stats[metric] = current_value + amount
    
    def reset_monthly_usage(self):
        """
        Reset monthly usage counters
        Call this at the start of each month
        """
        self.usage_stats["leads_created_this_month"] = 0
        self.usage_stats["searches_this_month"] = 0
        self.usage_stats["exports_this_month"] = 0
        self.usage_stats["last_reset_date"] = func.now()
    
    def get_preference(self, key: str, default=None):
        """
        Get a user preference
        """
        return self.preferences.get(key, default)
    
    def set_preference(self, key: str, value):
        """
        Set a user preference
        """
        if not self.preferences:
            self.preferences = {}
        
        self.preferences[key] = value