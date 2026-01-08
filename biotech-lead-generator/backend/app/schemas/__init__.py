"""
Schemas package initialization
Import all schemas for easy access
"""

# Base schemas
from app.schemas.base import (
    BaseSchema,
    TimestampSchema,
    UUIDSchema,
    SuccessResponse,
    ErrorResponse,
    MessageResponse,
    PaginationParams,
    PaginationMeta,
    PaginatedResponse,
    SortParams,
    DateRangeFilter,
    BulkOperationResponse,
    BulkDeleteRequest,
    HealthCheckResponse,
)

# Token schemas
from app.schemas.token import (
    Token,
    TokenData,
    RefreshTokenRequest,
    APIKeyCreate,
    APIKeyResponse,
    APIKeyList,
)

# User schemas
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserBase,
    UserProfile,
    UserPublic,
    UserUpdate,
    PasswordChange,
    PasswordResetRequest,
    PasswordReset,
    UserPreferences,
    UserUsageStats,
)

# Lead schemas
from app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadBase,
    LeadDetail,
    LeadList,
    LeadFilters,
    LeadQuery,
    LeadBulkCreate,
    LeadScoreUpdate,
)

# Search schemas
from app.schemas.search import (
    SearchCreate,
    SearchResponse,
)

# Export schemas
from app.schemas.export import (
    ExportCreate,
    ExportResponse,
)

# Pipeline schemas
from app.schemas.pipeline import (
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineRunRequest,
)

# Export all
__all__ = [
    # Base
    "BaseSchema",
    "TimestampSchema",
    "UUIDSchema",
    "SuccessResponse",
    "ErrorResponse",
    "MessageResponse",
    "PaginationParams",
    "PaginationMeta",
    "PaginatedResponse",
    "SortParams",
    "DateRangeFilter",
    "BulkOperationResponse",
    "BulkDeleteRequest",
    "HealthCheckResponse",
    # Token
    "Token",
    "TokenData",
    "RefreshTokenRequest",
    "APIKeyCreate",
    "APIKeyResponse",
    "APIKeyList",
    # User
    "UserRegister",
    "UserLogin",
    "UserBase",
    "UserProfile",
    "UserPublic",
    "UserUpdate",
    "PasswordChange",
    "PasswordResetRequest",
    "PasswordReset",
    "UserPreferences",
    "UserUsageStats",
    # Lead
    "LeadCreate",
    "LeadUpdate",
    "LeadBase",
    "LeadDetail",
    "LeadList",
    "LeadFilters",
    "LeadQuery",
    "LeadBulkCreate",
    "LeadScoreUpdate",
    # Search
    "SearchCreate",
    "SearchResponse",
    # Export
    "ExportCreate",
    "ExportResponse",
    # Pipeline
    "PipelineCreate",
    "PipelineUpdate",
    "PipelineResponse",
    "PipelineRunRequest",
]