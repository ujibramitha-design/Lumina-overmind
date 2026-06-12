"""
Twin-Dragon Engine - Campaigns Management API Endpoint
Multi-tenant campaign management with strict project isolation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json
from datetime import datetime
from prisma import Client as PrismaClient

# Database dependency
def get_db():
    db = PrismaClient()
    return db

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

# Pydantic Models
class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    mode: str = Field(..., regex="^(BASIC|HLR_SNIPER|EXTREME_INTELLIGENCE|PANOPTICON|LEVIATHAN|PROXY_WEALTH|TRANSITION|GAVEL|PROGRESSIVE|PINTEREST|PLASTIC|INCUBATOR)$")
    
    # Targeting
    target_area: Optional[str] = Field(None, max_length=255)
    keywords: List[str] = Field(default_factory=list)
    exclude_keywords: List[str] = Field(default_factory=list)
    
    # Project isolation (MANDATORY)
    project_id: str = Field(..., min_length=1, description="Project ID is mandatory for data isolation")
    
    # Configuration
    config: Optional[dict] = Field(default_factory=dict)
    start_date: Optional[datetime] = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = Field(True)

class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    mode: Optional[str] = Field(None, regex="^(BASIC|HLR_SNIPER|EXTREME_INTELLIGENCE|PANOPTICON|LEVIATHAN|PROXY_WEALTH|TRANSITION|GAVEL|PROGRESSIVE|PINTEREST|PLASTIC|INCUBATOR)$")
    
    # Targeting
    target_area: Optional[str] = Field(None, max_length=255)
    keywords: Optional[List[str]] = None
    exclude_keywords: Optional[List[str]] = None
    
    # Configuration
    config: Optional[dict] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class CampaignResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    mode: str
    target_area: Optional[str] = None
    keywords: List[str] = []
    exclude_keywords: List[str] = []
    project_id: str
    status: str
    leads_count: int
    hot_leads_count: int
    conversion_rate: float
    config: Optional[dict] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Helper Functions
def validate_project_exists(db: PrismaClient, project_id: str):
    """Validate that project exists and is active"""
    try:
        project = db.project.find_unique(where={'id': project_id})
        if not project:
            raise HTTPException(
                status_code=400, 
                detail=f"Project with ID {project_id} not found"
            )
        if not project.isActive:
            raise HTTPException(
                status_code=400, 
                detail=f"Project with ID {project_id} is not active"
            )
        return project
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, 
            detail="Error validating project existence"
        )

def get_campaign_mode_description(mode: str) -> str:
    """Get description for campaign mode"""
    descriptions = {
        'BASIC': 'Basic lead generation campaign',
        'HLR_SNIPER': 'High-value lead targeting',
        'EXTREME_INTELLIGENCE': 'Advanced AI-powered scouting',
        'PANOPTICON': 'Comprehensive market surveillance',
        'LEVIATHAN': 'Large-scale lead acquisition',
        'PROXY_WEALTH': 'Affluent target identification',
        'TRANSITION': 'Life-change event targeting',
        'GAVEL': 'Legal/professional service targeting',
        'PROGRESSIVE': 'Multi-property owner targeting',
        'PINTEREST': 'Design-inspiration based targeting',
        'PLASTIC': 'High-credit score targeting',
        'INCUBATOR': 'New business targeting'
    }
    return descriptions.get(mode, 'Custom campaign mode')

# API Endpoints
@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate, background_tasks: BackgroundTasks, db: PrismaClient = Depends(get_db)):
    """Create new campaign with mandatory project validation"""
    try:
        # Validate project exists and is active
        validate_project_exists(db, campaign.project_id)
        
        # Create campaign in database with project isolation
        new_campaign = await db.campaign.create({
            'name': campaign.name,
            'description': campaign.description,
            'mode': campaign.mode,
            'targetArea': campaign.target_area,
            'keywords': campaign.keywords,
            'excludeKeywords': campaign.exclude_keywords,
            'projectId': campaign.project_id,  # Mandatory project isolation
            'config': campaign.config,
            'startDate': campaign.start_date,
            'endDate': campaign.end_date,
            'isActive': campaign.is_active,
            'status': 'ACTIVE'
        })
        
        return CampaignResponse(
            id=new_campaign.id,
            name=new_campaign.name,
            description=new_campaign.description,
            mode=new_campaign.mode,
            target_area=new_campaign.targetArea,
            keywords=new_campaign.keywords,
            exclude_keywords=new_campaign.excludeKeywords,
            project_id=new_campaign.projectId,
            status=new_campaign.status,
            leads_count=new_campaign.leadsCount,
            hot_leads_count=new_campaign.hotLeadsCount,
            conversion_rate=new_campaign.conversionRate,
            config=new_campaign.config,
            start_date=new_campaign.startDate,
            end_date=new_campaign.endDate,
            is_active=new_campaign.isActive,
            created_at=new_campaign.createdAt,
            updated_at=new_campaign.updatedAt
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create campaign: {str(e)}"
        )

@router.get("/", response_model=List[CampaignResponse])
async def get_campaigns(
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None, regex="^(ACTIVE|PAUSED|COMPLETED|ARCHIVED)$"),
    mode: Optional[str] = Query(None, regex="^(BASIC|HLR_SNIPER|EXTREME_INTELLIGENCE|PANOPTICON|LEVIATHAN|PROXY_WEALTH|TRANSITION|GAVEL|PROGRESSIVE|PINTEREST|PLASTIC|INCUBATOR)$"),
    search: Optional[str] = Query(None),
    db: PrismaClient = Depends(get_db)
):
    """Get campaigns with strict project isolation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Build query with mandatory project filter
        where_clause = {
            'projectId': project_id  # MANDATORY: Always filter by project
        }
        
        # Add optional filters
        if status:
            where_clause['status'] = status
            
        if mode:
            where_clause['mode'] = mode
            
        if search:
            where_clause['OR'] = [
                {'name': {'contains': search, 'mode': 'insensitive'}},
                {'description': {'contains': search, 'mode': 'insensitive'}},
                {'targetArea': {'contains': search, 'mode': 'insensitive'}}
            ]
        
        # Query with strict project isolation
        campaigns = await db.campaign.find_many(
            where=where_clause,
            skip=skip,
            take=limit,
            order={'createdAt': 'desc'}
        )
        
        return [
            CampaignResponse(
                id=campaign.id,
                name=campaign.name,
                description=campaign.description,
                mode=campaign.mode,
                target_area=campaign.targetArea,
                keywords=campaign.keywords,
                exclude_keywords=campaign.excludeKeywords,
                project_id=campaign.projectId,
                status=campaign.status,
                leads_count=campaign.leadsCount,
                hot_leads_count=campaign.hotLeadsCount,
                conversion_rate=campaign.conversionRate,
                config=campaign.config,
                start_date=campaign.startDate,
                end_date=campaign.endDate,
                is_active=campaign.isActive,
                created_at=campaign.createdAt,
                updated_at=campaign.updatedAt
            )
            for campaign in campaigns
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch campaigns: {str(e)}"
        )

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    db: PrismaClient = Depends(get_db)
):
    """Get specific campaign with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Find campaign with project isolation
        campaign = await db.campaign.find_first(
            where={
                'id': campaign_id,
                'projectId': project_id  # MANDATORY: Ensure campaign belongs to project
            }
        )
        
        if not campaign:
            raise HTTPException(
                status_code=404, 
                detail="Campaign not found or access denied"
            )
        
        return CampaignResponse(
            id=campaign.id,
            name=campaign.name,
            description=campaign.description,
            mode=campaign.mode,
            target_area=campaign.targetArea,
            keywords=campaign.keywords,
            exclude_keywords=campaign.excludeKeywords,
            project_id=campaign.projectId,
            status=campaign.status,
            leads_count=campaign.leadsCount,
            hot_leads_count=campaign.hotLeadsCount,
            conversion_rate=campaign.conversionRate,
            config=campaign.config,
            start_date=campaign.startDate,
            end_date=campaign.endDate,
            is_active=campaign.isActive,
            created_at=campaign.createdAt,
            updated_at=campaign.updatedAt
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch campaign: {str(e)}"
        )

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: str,
    campaign_update: CampaignUpdate,
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    db: PrismaClient = Depends(get_db)
):
    """Update campaign with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Check if campaign exists and belongs to project
        existing_campaign = await db.campaign.find_first(
            where={
                'id': campaign_id,
                'projectId': project_id  # MANDATORY: Ensure campaign belongs to project
            }
        )
        
        if not existing_campaign:
            raise HTTPException(
                status_code=404, 
                detail="Campaign not found or access denied"
            )
        
        # Prepare update data
        update_data = {}
        if campaign_update.name is not None:
            update_data['name'] = campaign_update.name
        if campaign_update.description is not None:
            update_data['description'] = campaign_update.description
        if campaign_update.mode is not None:
            update_data['mode'] = campaign_update.mode
        if campaign_update.target_area is not None:
            update_data['targetArea'] = campaign_update.target_area
        if campaign_update.keywords is not None:
            update_data['keywords'] = campaign_update.keywords
        if campaign_update.exclude_keywords is not None:
            update_data['excludeKeywords'] = campaign_update.exclude_keywords
        if campaign_update.config is not None:
            update_data['config'] = campaign_update.config
        if campaign_update.start_date is not None:
            update_data['startDate'] = campaign_update.start_date
        if campaign_update.end_date is not None:
            update_data['endDate'] = campaign_update.end_date
        if campaign_update.is_active is not None:
            update_data['isActive'] = campaign_update.is_active
        
        # Update campaign
        updated_campaign = await db.campaign.update(
            where={'id': campaign_id},
            data=update_data
        )
        
        return CampaignResponse(
            id=updated_campaign.id,
            name=updated_campaign.name,
            description=updated_campaign.description,
            mode=updated_campaign.mode,
            target_area=updated_campaign.targetArea,
            keywords=updated_campaign.keywords,
            exclude_keywords=updated_campaign.excludeKeywords,
            project_id=updated_campaign.projectId,
            status=updated_campaign.status,
            leads_count=updated_campaign.leadsCount,
            hot_leads_count=updated_campaign.hotLeadsCount,
            conversion_rate=updated_campaign.conversionRate,
            config=updated_campaign.config,
            start_date=updated_campaign.startDate,
            end_date=updated_campaign.endDate,
            is_active=updated_campaign.isActive,
            created_at=updated_campaign.createdAt,
            updated_at=updated_campaign.updatedAt
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update campaign: {str(e)}"
        )

@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    db: PrismaClient = Depends(get_db)
):
    """Delete campaign with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Check if campaign exists and belongs to project
        existing_campaign = await db.campaign.find_first(
            where={
                'id': campaign_id,
                'projectId': project_id  # MANDATORY: Ensure campaign belongs to project
            }
        )
        
        if not existing_campaign:
            raise HTTPException(
                status_code=404, 
                detail="Campaign not found or access denied"
            )
        
        # Delete campaign
        await db.campaign.delete(where={'id': campaign_id})
        
        return {"message": "Campaign deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to delete campaign: {str(e)}"
        )

@router.post("/{campaign_id}/start")
async def start_campaign(
    campaign_id: str,
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    db: PrismaClient = Depends(get_db)
):
    """Start campaign with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Check if campaign exists and belongs to project
        existing_campaign = await db.campaign.find_first(
            where={
                'id': campaign_id,
                'projectId': project_id  # MANDATORY: Ensure campaign belongs to project
            }
        )
        
        if not existing_campaign:
            raise HTTPException(
                status_code=404, 
                detail="Campaign not found or access denied"
            )
        
        # Update campaign status to ACTIVE
        updated_campaign = await db.campaign.update(
            where={'id': campaign_id},
            data={
                'status': 'ACTIVE',
                'isActive': True
            }
        )
        
        return {"message": "Campaign started successfully", "status": updated_campaign.status}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to start campaign: {str(e)}"
        )

@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: str,
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    db: PrismaClient = Depends(get_db)
):
    """Pause campaign with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Check if campaign exists and belongs to project
        existing_campaign = await db.campaign.find_first(
            where={
                'id': campaign_id,
                'projectId': project_id  # MANDATORY: Ensure campaign belongs to project
            }
        )
        
        if not existing_campaign:
            raise HTTPException(
                status_code=404, 
                detail="Campaign not found or access denied"
            )
        
        # Update campaign status to PAUSED
        updated_campaign = await db.campaign.update(
            where={'id': campaign_id},
            data={
                'status': 'PAUSED',
                'isActive': False
            }
        )
        
        return {"message": "Campaign paused successfully", "status": updated_campaign.status}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to pause campaign: {str(e)}"
        )

@router.get("/stats/summary")
async def get_campaign_stats(
    project_id: str = Query(..., description="Project ID is mandatory for data isolation"),
    db: PrismaClient = Depends(get_db)
):
    """Get campaign statistics with project isolation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)
        
        # Get statistics with project isolation
        total_campaigns = await db.campaign.count(
            where={'projectId': project_id}
        )
        
        campaigns_by_status = await db.campaign.group_by(
            by=['status'],
            where={'projectId': project_id},
            count={'status': True}
        )
        
        campaigns_by_mode = await db.campaign.group_by(
            by=['mode'],
            where={'projectId': project_id},
            count={'mode': True}
        )
        
        active_campaigns = await db.campaign.count(
            where={
                'projectId': project_id,
                'isActive': True
            }
        )
        
        return {
            'project_id': project_id,
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'campaigns_by_status': {item['status']: item['_count']['status'] for item in campaigns_by_status},
            'campaigns_by_mode': {item['mode']: item['_count']['mode'] for item in campaigns_by_mode}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch campaign statistics: {str(e)}"
        )
