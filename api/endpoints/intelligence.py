"""
Intelligence API Endpoints
Lead scouting, market analysis, and intelligence operations
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Pydantic models
class LeadScoutRequest(BaseModel):
    campaign_mode: str
    area: str
    keywords: List[str]
    max_results: int = 100
    use_proxy: bool = True
    target_region: Optional[str] = None

class MarketAnalysisRequest(BaseModel):
    days: int = 30
    area: Optional[str] = None
    include_entity_analysis: bool = True

class AreaIntelligenceRequest(BaseModel):
    coordinates: tuple
    area_name: str
    include_gov_analysis: bool = True
    include_urban_analysis: bool = True

class LeadData(BaseModel):
    url: str
    title: str
    content: str
    score: float
    status: str
    contact_info: Dict[str, Any]

# Dependency for database connection
async def get_db():
    """Get database connection"""
    try:
        from core_modules.db_manager_postgres import postgres_db_manager
        return postgres_db_manager
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@router.post("/scout-leads")
async def scout_leads(
    request: LeadScoutRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Scout leads using 48-Radar Scout Engine
    """
    try:
        logger.info(f"Starting lead scouting: {request.campaign_mode} in {request.area}")
        
        # Submit task to Celery
        from tasks.intelligence_tasks import scout_leads
        task = scout_leads.s(
            campaign_mode=request.campaign_mode,
            area=request.area,
            keywords=request.keywords,
            max_results=request.max_results,
            use_proxy=request.use_proxy,
            target_region=request.target_region
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "campaign_mode": request.campaign_mode,
            "area": request.area,
            "keywords": request.keywords,
            "message": "Lead scouting task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Lead scouting failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-market")
async def analyze_market(
    request: MarketAnalysisRequest,
    db = Depends(get_db)
):
    """
    Analyze market trends and generate intelligence reports
    """
    try:
        logger.info(f"Starting market analysis: {request.days} days")
        
        # Submit task to Celery
        from tasks.intelligence_tasks import analyze_market_trends
        task = analyze_market_trends.s(
            days=request.days,
            area=request.area,
            include_entity_analysis=request.include_entity_analysis
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "analysis_period": request.days,
            "area": request.area,
            "message": "Market analysis task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Market analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-area-intelligence")
async def generate_area_intelligence(
    request: AreaIntelligenceRequest,
    db = Depends(get_db)
):
    """
    Generate comprehensive area intelligence report
    """
    try:
        logger.info(f"Generating area intelligence: {request.area_name}")
        
        # Submit task to Celery
        from tasks.intelligence_tasks import generate_area_intelligence_report
        task = generate_area_intelligence_report.s(
            coordinates=request.coordinates,
            area_name=request.area_name,
            include_gov_analysis=request.include_gov_analysis,
            include_urban_analysis=request.include_urban_analysis
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "area_name": request.area_name,
            "coordinates": request.coordinates,
            "message": "Area intelligence task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Area intelligence generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads")
async def get_leads(
    status: Optional[str] = None,
    limit: int = 100,
    db = Depends(get_db)
):
    """
    Get leads from database
    """
    try:
        if status:
            from prisma.enums import LeadStatus
            leads = await db.get_leads_by_status(LeadStatus(status.upper()), limit)
        else:
            # Get all leads
            from core_modules.db_manager_postgres import postgres_db_manager
            leads = await postgres_db_manager.execute_query(
                "SELECT * FROM leads ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
        
        return {
            "success": True,
            "leads": leads,
            "total": len(leads),
            "status": status or "all"
        }
        
    except Exception as e:
        logger.error(f"Failed to get leads: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/leads")
async def create_lead(
    lead_data: LeadData,
    db = Depends(get_db)
):
    """
    Create new lead
    """
    try:
        result = await db.create_lead({
            'url': lead_data.url,
            'title': lead_data.title,
            'content': lead_data.content,
            'score': lead_data.score,
            'status': lead_data.status,
            'contact_info': lead_data.contact_info
        })
        
        if result['success']:
            return {
                "success": True,
                "lead_id": result['lead_id'],
                "message": "Lead created successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
        
    except Exception as e:
        logger.error(f"Failed to create lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads/{lead_id}")
async def get_lead(
    lead_id: str,
    db = Depends(get_db)
):
    """
    Get specific lead by ID
    """
    try:
        lead = await db.get_lead_by_id(lead_id)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return {
            "success": True,
            "lead": lead
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/leads/{lead_id}/status")
async def update_lead_status(
    lead_id: str,
    status: str,
    db = Depends(get_db)
):
    """
    Update lead status
    """
    try:
        from prisma.enums import LeadStatus
        
        success = await db.update_lead_status(lead_id, LeadStatus(status.upper()))
        
        if success:
            return {
                "success": True,
                "message": f"Lead status updated to {status}"
            }
        else:
            raise HTTPException(status_code=404, detail="Lead not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update lead status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaigns")
async def get_campaigns(db = Depends(get_db)):
    """
    Get all campaigns
    """
    try:
        campaigns = await db.execute_query("SELECT * FROM campaigns ORDER BY created_at DESC")
        
        return {
            "success": True,
            "campaigns": campaigns,
            "total": len(campaigns)
        }
        
    except Exception as e:
        logger.error(f"Failed to get campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/campaigns")
async def create_campaign(
    campaign_data: Dict[str, Any],
    db = Depends(get_db)
):
    """
    Create new campaign
    """
    try:
        result = await db.create_campaign(campaign_data)
        
        if result['success']:
            return {
                "success": True,
                "campaign_id": result['campaign_id'],
                "message": "Campaign created successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
        
    except Exception as e:
        logger.error(f"Failed to create campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_intelligence_stats(db = Depends(get_db)):
    """
    Get intelligence statistics
    """
    try:
        stats = await db.get_system_statistics()
        
        return {
            "success": True,
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get intelligence stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hlr-regions")
async def get_hlr_regions():
    """
    Get available HLR regions for targeting
    """
    try:
        from core_modules.intelligence.telecom_hlr_db import INDONESIA_HLR_MAPPING, get_hlr_summary
        
        regions = list(INDONESIA_HLR_MAPPING.keys())
        summary = get_hlr_summary()
        
        return {
            "success": True,
            "regions": regions,
            "summary": summary,
            "total_regions": len(regions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get HLR regions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hlr-regions/{region}")
async def get_hlr_region_details(region: str):
    """
    Get HLR details for specific region
    """
    try:
        from core_modules.intelligence.telecom_hlr_db import get_region_prefixes, analyze_hlr_distribution
        
        prefixes = get_region_prefixes(region)
        analysis = analyze_hlr_distribution(region)
        
        return {
            "success": True,
            "region": region,
            "prefixes": prefixes,
            "analysis": analysis,
            "total_prefixes": len(prefixes)
        }
        
    except Exception as e:
        logger.error(f"Failed to get HLR region details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Get task status by ID
    """
    try:
        from tasks.celery_app import celery_app
        
        result = celery_app.AsyncResult(task_id)
        
        return {
            "success": True,
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
            "ready": result.ready()
        }
        
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
