"""
API v1 Router
Combines all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth
# from app.api.v1.endpoints import users  # We'll create this on Day 4
# from app.api.v1.endpoints import leads  # We'll create this on Day 4
# from app.api.v1.endpoints import search
# from app.api.v1.endpoints import export
# from app.api.v1.endpoints import scoring
# from app.api.v1.endpoints import enrichment
# from app.api.v1.endpoints import pipelines


# Create main API router
api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Include user endpoints (Day 4)
from app.api.v1.endpoints import users
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

# Include lead endpoints (Day 4)
from app.api.v1.endpoints import leads
api_router.include_router(
    leads.router,
    prefix="/leads",
    tags=["Leads"]
)

# Include search endpoints (Day 5)
# api_router.include_router(
#     search.router,
#     prefix="/search",
#     tags=["Search"]
# )

# Include export endpoints (Day 5)
# api_router.include_router(
#     export.router,
#     prefix="/export",
#     tags=["Export"]
# )

# Include scoring endpoints (Day 5)
# api_router.include_router(
#     scoring.router,
#     prefix="/scoring",
#     tags=["Scoring"]
# )

# Include enrichment endpoints (Day 6)
# api_router.include_router(
#     enrichment.router,
#     prefix="/enrich",
#     tags=["Enrichment"]
# )

# Include pipeline endpoints (Day 6)
# api_router.include_router(
#     pipelines.router,
#     prefix="/pipelines",
#     tags=["Pipelines"]
# )