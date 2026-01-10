"""
Lead Management Endpoints - FIXED ASYNC VERSION
CRUD operations for leads with scoring
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import List, Optional
from uuid import UUID

from app.core.deps import get_db, get_current_active_user, check_lead_quota
from app.models.user import User
from app.models.lead import Lead
from app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadDetail,
    LeadList,
    LeadFilters,
    LeadBulkCreate,
    LeadScoreUpdate,
)
from app.schemas.base import (
    MessageResponse,
    SuccessResponse,
    PaginatedResponse,
    PaginationParams,
    BulkOperationResponse,
    BulkDeleteRequest,
)
from app.services.scoring_service import ScoringService


router = APIRouter()


# ============================================================================
# LIST LEADS (with pagination, filtering, sorting)
# ============================================================================

@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List leads",
    description="Get paginated list of leads with filtering and sorting"
)
async def list_leads(
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Items per page"),
    
    # Sorting
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    
    # Filters
    search: Optional[str] = Query(None, description="Search in name, title, company"),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    max_score: Optional[int] = Query(None, ge=0, le=100),
    priority_tier: Optional[str] = Query(None, regex="^(HIGH|MEDIUM|LOW)$"),
    status: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    has_email: Optional[bool] = Query(None),
    has_publication: Optional[bool] = Query(None),
    
    # Dependencies
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List user's leads with pagination, filtering, and sorting
    """
    
    # Build base query
    query = select(Lead).where(Lead.user_id == current_user.id)
    
    # Apply filters
    if search:
        search_filter = or_(
            Lead.name.ilike(f"%{search}%"),
            Lead.title.ilike(f"%{search}%"),
            Lead.company.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    if min_score is not None:
        query = query.where(Lead.propensity_score >= min_score)
    
    if max_score is not None:
        query = query.where(Lead.propensity_score <= max_score)
    
    if priority_tier:
        query = query.where(Lead.priority_tier == priority_tier)
    
    if status:
        query = query.where(Lead.status == status)
    
    if location:
        query = query.where(Lead.location.ilike(f"%{location}%"))
    
    if has_email is not None:
        if has_email:
            query = query.where(Lead.email.isnot(None))
        else:
            query = query.where(Lead.email.is_(None))
    
    if has_publication is not None:
        query = query.where(Lead.recent_publication == has_publication)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply sorting
    sort_column = getattr(Lead, sort_by, Lead.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Apply pagination
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)
    
    # Execute query
    result = await db.execute(query)
    leads = result.scalars().all()
    
    # Convert to list schema (accessing attributes here in async context)
    lead_list = []
    for lead in leads:
        lead_list.append(LeadList(
            id=lead.id,
            name=lead.name,
            title=lead.title,
            company=lead.company,
            email=lead.email,
            propensity_score=lead.propensity_score,
            priority_tier=lead.priority_tier,
            tags=lead.tags or [],
            created_at=lead.created_at
        ))
    
    # Return paginated response
    return PaginatedResponse.create(
        items=lead_list,
        page=page,
        size=size,
        total=total
    )


# ============================================================================
# CREATE LEAD
# ============================================================================

@router.post(
    "",
    response_model=LeadDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create lead",
    description="Create new lead with automatic scoring"
)
async def create_lead(
    lead_data: LeadCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(check_lead_quota)
):
    """
    Create new lead with automatic scoring
    """
    
    # Check for duplicate email
    if lead_data.email:
        result = await db.execute(
            select(Lead).where(
                and_(
                    Lead.user_id == current_user.id,
                    Lead.email == lead_data.email
                )
            )
        )
        existing_lead = result.scalar_one_or_none()
        
        if existing_lead:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lead with this email already exists"
            )
    
    # Create lead
    lead = Lead(
        user_id=current_user.id,
        **lead_data.model_dump()
    )
    
    # Calculate propensity score
    scoring_service = ScoringService()
    lead.propensity_score = scoring_service.calculate_score(lead)
    lead.update_priority_tier()
    
    # Add data source
    lead.add_data_source("manual")
    
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    
    # Update ranks for all user's leads
    await update_lead_ranks(current_user.id, db)
    
    # Increment usage counter
    current_user.increment_usage("leads_created_this_month")
    await db.commit()
    
    # IMPORTANT: Access all attributes while in async context
    # Convert to dict to avoid lazy loading issues
    lead_dict = {
        "id": lead.id,
        "name": lead.name,
        "title": lead.title,
        "company": lead.company,
        "location": lead.location,
        "email": lead.email,
        "propensity_score": lead.propensity_score,
        "rank": lead.rank,
        "priority_tier": lead.priority_tier,
        "status": lead.status,
        "company_hq": lead.company_hq,
        "phone": lead.phone,
        "linkedin_url": lead.linkedin_url,
        "twitter_url": lead.twitter_url,
        "website": lead.website,
        "recent_publication": lead.recent_publication,
        "publication_year": lead.publication_year,
        "publication_title": lead.publication_title,
        "publication_count": lead.publication_count,
        "company_funding": lead.company_funding,
        "company_size": lead.company_size,
        "uses_3d_models": lead.uses_3d_models,
        "data_sources": lead.data_sources or [],
        "enrichment_data": lead.enrichment_data or {},
        "custom_fields": lead.custom_fields or {},
        "tags": lead.tags or [],
        "notes": lead.notes,
        "last_contacted_at": lead.last_contacted_at,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at
    }
    
    return LeadDetail(**lead_dict)


# ============================================================================
# GET LEAD DETAILS
# ============================================================================

@router.get(
    "/{lead_id}",
    response_model=LeadDetail,
    summary="Get lead",
    description="Get detailed lead information"
)
async def get_lead(
    lead_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get lead details
    """
    
    result = await db.execute(
        select(Lead).where(
            and_(
                Lead.id == lead_id,
                Lead.user_id == current_user.id
            )
        )
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Convert to dict in async context
    lead_dict = {
        "id": lead.id,
        "name": lead.name,
        "title": lead.title,
        "company": lead.company,
        "location": lead.location,
        "email": lead.email,
        "propensity_score": lead.propensity_score,
        "rank": lead.rank,
        "priority_tier": lead.priority_tier,
        "status": lead.status,
        "company_hq": lead.company_hq,
        "phone": lead.phone,
        "linkedin_url": lead.linkedin_url,
        "twitter_url": lead.twitter_url,
        "website": lead.website,
        "recent_publication": lead.recent_publication,
        "publication_year": lead.publication_year,
        "publication_title": lead.publication_title,
        "publication_count": lead.publication_count,
        "company_funding": lead.company_funding,
        "company_size": lead.company_size,
        "uses_3d_models": lead.uses_3d_models,
        "data_sources": lead.data_sources or [],
        "enrichment_data": lead.enrichment_data or {},
        "custom_fields": lead.custom_fields or {},
        "tags": lead.tags or [],
        "notes": lead.notes,
        "last_contacted_at": lead.last_contacted_at,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at
    }
    
    return LeadDetail(**lead_dict)


# ============================================================================
# UPDATE LEAD
# ============================================================================

@router.put(
    "/{lead_id}",
    response_model=LeadDetail,
    summary="Update lead",
    description="Update lead information"
)
async def update_lead(
    lead_id: UUID,
    lead_updates: LeadUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update lead
    """
    
    result = await db.execute(
        select(Lead).where(
            and_(
                Lead.id == lead_id,
                Lead.user_id == current_user.id
            )
        )
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Update fields
    update_data = lead_updates.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
    
    await db.commit()
    await db.refresh(lead)
    
    # Convert to dict in async context
    lead_dict = {
        "id": lead.id,
        "name": lead.name,
        "title": lead.title,
        "company": lead.company,
        "location": lead.location,
        "email": lead.email,
        "propensity_score": lead.propensity_score,
        "rank": lead.rank,
        "priority_tier": lead.priority_tier,
        "status": lead.status,
        "company_hq": lead.company_hq,
        "phone": lead.phone,
        "linkedin_url": lead.linkedin_url,
        "twitter_url": lead.twitter_url,
        "website": lead.website,
        "recent_publication": lead.recent_publication,
        "publication_year": lead.publication_year,
        "publication_title": lead.publication_title,
        "publication_count": lead.publication_count,
        "company_funding": lead.company_funding,
        "company_size": lead.company_size,
        "uses_3d_models": lead.uses_3d_models,
        "data_sources": lead.data_sources or [],
        "enrichment_data": lead.enrichment_data or {},
        "custom_fields": lead.custom_fields or {},
        "tags": lead.tags or [],
        "notes": lead.notes,
        "last_contacted_at": lead.last_contacted_at,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at
    }
    
    return LeadDetail(**lead_dict)


# ============================================================================
# DELETE LEAD
# ============================================================================

@router.delete(
    "/{lead_id}",
    response_model=MessageResponse,
    summary="Delete lead",
    description="Delete a lead"
)
async def delete_lead(
    lead_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete lead
    """
    
    result = await db.execute(
        select(Lead).where(
            and_(
                Lead.id == lead_id,
                Lead.user_id == current_user.id
            )
        )
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    await db.delete(lead)
    await db.commit()
    
    # Update ranks
    await update_lead_ranks(current_user.id, db)
    
    return MessageResponse(message="Lead deleted successfully")


# ============================================================================
# BULK DELETE
# ============================================================================

@router.post(
    "/bulk/delete",
    response_model=BulkOperationResponse,
    summary="Bulk delete leads",
    description="Delete multiple leads at once"
)
async def bulk_delete_leads(
    request: BulkDeleteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Bulk delete leads
    """
    
    success_count = 0
    errors = []
    
    for lead_id in request.ids:
        try:
            result = await db.execute(
                select(Lead).where(
                    and_(
                        Lead.id == lead_id,
                        Lead.user_id == current_user.id
                    )
                )
            )
            lead = result.scalar_one_or_none()
            
            if lead:
                await db.delete(lead)
                success_count += 1
            else:
                errors.append({
                    "id": str(lead_id),
                    "error": "Lead not found"
                })
        except Exception as e:
            errors.append({
                "id": str(lead_id),
                "error": str(e)
            })
    
    await db.commit()
    
    # Update ranks
    await update_lead_ranks(current_user.id, db)
    
    return BulkOperationResponse(
        success_count=success_count,
        failure_count=len(errors),
        total=len(request.ids),
        errors=errors
    )


# ============================================================================
# BULK CREATE
# ============================================================================

@router.post(
    "/bulk/create",
    response_model=BulkOperationResponse,
    summary="Bulk create leads",
    description="Create multiple leads at once"
)
async def bulk_create_leads(
    request: LeadBulkCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(check_lead_quota)
):
    """
    Bulk create leads
    """
    
    success_count = 0
    errors = []
    scoring_service = ScoringService() if request.calculate_scores else None
    
    for idx, lead_data in enumerate(request.leads):
        try:
            # Check for duplicate
            if request.skip_duplicates and lead_data.email:
                result = await db.execute(
                    select(Lead).where(
                        and_(
                            Lead.user_id == current_user.id,
                            Lead.email == lead_data.email
                        )
                    )
                )
                if result.scalar_one_or_none():
                    errors.append({
                        "row": idx + 1,
                        "error": "Duplicate email"
                    })
                    continue
            
            # Create lead
            lead = Lead(
                user_id=current_user.id,
                **lead_data.model_dump()
            )
            
            # Calculate score
            if scoring_service:
                lead.propensity_score = scoring_service.calculate_score(lead)
                lead.update_priority_tier()
            
            lead.add_data_source("bulk_import")
            
            db.add(lead)
            success_count += 1
            
        except Exception as e:
            errors.append({
                "row": idx + 1,
                "error": str(e)
            })
    
    await db.commit()
    
    # Update ranks
    if success_count > 0:
        await update_lead_ranks(current_user.id, db)
        
        # Update usage
        current_user.increment_usage("leads_created_this_month", success_count)
        await db.commit()
    
    return BulkOperationResponse(
        success_count=success_count,
        failure_count=len(errors),
        total=len(request.leads),
        errors=errors
    )


# ============================================================================
# RECALCULATE SCORE
# ============================================================================

@router.post(
    "/{lead_id}/score",
    response_model=LeadDetail,
    summary="Recalculate lead score",
    description="Recalculate lead's propensity score"
)
async def recalculate_score(
    lead_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Recalculate lead score
    """
    
    result = await db.execute(
        select(Lead).where(
            and_(
                Lead.id == lead_id,
                Lead.user_id == current_user.id
            )
        )
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Recalculate score
    scoring_service = ScoringService()
    lead.propensity_score = scoring_service.calculate_score(lead)
    lead.update_priority_tier()
    
    await db.commit()
    await db.refresh(lead)
    
    # Update ranks
    await update_lead_ranks(current_user.id, db)
    
    # Convert to dict in async context
    lead_dict = {
        "id": lead.id,
        "name": lead.name,
        "title": lead.title,
        "company": lead.company,
        "location": lead.location,
        "email": lead.email,
        "propensity_score": lead.propensity_score,
        "rank": lead.rank,
        "priority_tier": lead.priority_tier,
        "status": lead.status,
        "company_hq": lead.company_hq,
        "phone": lead.phone,
        "linkedin_url": lead.linkedin_url,
        "twitter_url": lead.twitter_url,
        "website": lead.website,
        "recent_publication": lead.recent_publication,
        "publication_year": lead.publication_year,
        "publication_title": lead.publication_title,
        "publication_count": lead.publication_count,
        "company_funding": lead.company_funding,
        "company_size": lead.company_size,
        "uses_3d_models": lead.uses_3d_models,
        "data_sources": lead.data_sources or [],
        "enrichment_data": lead.enrichment_data or {},
        "custom_fields": lead.custom_fields or {},
        "tags": lead.tags or [],
        "notes": lead.notes,
        "last_contacted_at": lead.last_contacted_at,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at
    }
    
    return LeadDetail(**lead_dict)


@router.post(
    "/bulk/recalculate-scores",
    response_model=SuccessResponse,
    summary="Recalculate all scores",
    description="Recalculate scores for all leads"
)
async def recalculate_all_scores(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Recalculate all lead scores
    """
    
    result = await db.execute(
        select(Lead).where(Lead.user_id == current_user.id)
    )
    leads = result.scalars().all()
    
    # Recalculate scores
    scoring_service = ScoringService()
    
    for lead in leads:
        lead.propensity_score = scoring_service.calculate_score(lead)
        lead.update_priority_tier()
    
    await db.commit()
    
    # Update ranks
    await update_lead_ranks(current_user.id, db)
    
    return SuccessResponse(
        message=f"Recalculated scores for {len(leads)} leads",
        data={"leads_updated": len(leads)}
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def update_lead_ranks(user_id: UUID, db: AsyncSession):
    """
    Update rank for all user's leads based on propensity_score
    """
    result = await db.execute(
        select(Lead)
        .where(Lead.user_id == user_id)
        .order_by(Lead.propensity_score.desc())
    )
    leads = result.scalars().all()
    
    for rank, lead in enumerate(leads, start=1):
        lead.rank = rank
    
    await db.commit()