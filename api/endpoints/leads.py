"""
Twin-Dragon Engine - Leads Management API Endpoint
Multi-tenant lead management with strict project isolation
"""

import json
import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from prisma import Prisma

from core_modules.db_manager import prisma_manager


# Database dependency
async def get_db():
    db = await prisma_manager.get_db()
    return db


router = APIRouter(prefix="/api/leads", tags=["leads"])


# Pydantic Models
class LeadCreate(BaseModel):
    # Core lead information
    business_name: str = Field(..., min_length=1, max_length=255)
    contact: str = Field(..., min_length=1, max_length=255)
    url: Optional[str] = Field(None, max_length=500)
    keywords: List[str] = Field(default_factory=list)
    source: str = Field(default="manual", max_length=50)
    area: Optional[str] = Field(None, max_length=255)

    # Project isolation (MANDATORY)
    project_id: str = Field(
        ..., min_length=1, description="Project ID is mandatory for data isolation"
    )

    # Lead intelligence
    score: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = Field("new", pattern="^(new|contacted|qualified|closed)$")

    # Platform enrichment
    platform_sumber: Optional[str] = Field(None, max_length=50)
    jabatan: Optional[str] = Field(None, max_length=255)
    nomor_hp: Optional[str] = Field(
        None, max_length=20, description="Phone number for duplicate prevention"
    )

    # Additional data
    notes: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high|urgent)$")


class LeadUpdate(BaseModel):
    business_name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[str] = Field(None, max_length=500)
    keywords: Optional[List[str]] = None
    source: Optional[str] = Field(None, max_length=50)
    area: Optional[str] = Field(None, max_length=255)

    # Lead intelligence
    score: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = Field(None, pattern="^(new|contacted|qualified|closed)$")
    notes: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")


class LeadResponse(BaseModel):
    id: str
    business_name: str
    contact: str
    url: Optional[str] = None
    keywords: List[str] = []
    source: str
    area: Optional[str] = None
    project_id: str
    score: Optional[int] = None
    status: str
    platform_sumber: Optional[str] = None
    jabatan: Optional[str] = None
    nomor_hp: Optional[str] = None
    notes: Optional[str] = None
    priority: str
    date_found: datetime
    created_at: datetime
    updated_at: datetime


# Helper Functions
def validate_project_exists(db: PrismaClient, project_id: str):
    """Validate that project exists and is active"""
    try:
        project = db.project.find_unique(where={"id": project_id})
        if not project:
            raise HTTPException(
                status_code=400, detail=f"Project with ID {project_id} not found"
            )
        if not project.isActive:
            raise HTTPException(
                status_code=400, detail=f"Project with ID {project_id} is not active"
            )
        return project
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error validating project existence"
        )


def check_duplicate_lead(db: PrismaClient, nomor_hp: str, project_id: str):
    """Check if lead with same phone number already exists in the project"""
    try:
        existing_lead = db.lead.find_first(
            where={"nomorHp": nomor_hp, "projectId": project_id}
        )
        return existing_lead is not None
    except Exception as e:
        # If error occurs, allow creation (fail-safe)
        return False


# API Endpoints
@router.post("/", response_model=LeadResponse)
async def create_lead(
    lead: LeadCreate,
    background_tasks: BackgroundTasks,
    db: PrismaClient = Depends(get_db),
):
    """Create new lead with mandatory project validation"""
    try:
        # Validate project exists and is active
        validate_project_exists(db, lead.project_id)

        # Check for duplicate phone number within the same project
        if lead.nomor_hp:
            is_duplicate = check_duplicate_lead(db, lead.nomor_hp, lead.project_id)
            if is_duplicate:
                raise HTTPException(
                    status_code=409,  # Conflict
                    detail=f"Lead with phone number {lead.nomor_hp} already exists in this project",
                )

        # Create lead in database with project isolation
        new_lead = await db.lead.create(
            {
                "business_name": lead.business_name,
                "contact": lead.contact,
                "url": lead.url,
                "keywords": lead.keywords,
                "source": lead.source,
                "area": lead.area,
                "projectId": lead.project_id,  # Mandatory project isolation
                "score": lead.score,
                "status": lead.status,
                "priority": lead.priority.upper(),
                "platformSumber": lead.platform_sumber,
                "jabatan": lead.jabatan,
                "nomorHp": lead.nomor_hp,
                "date_found": datetime.now(),
                "encryptedData": json.dumps(
                    {
                        "business_name": lead.business_name,
                        "contact": lead.contact,
                        "url": lead.url,
                        "keywords": lead.keywords,
                        "area": lead.area,
                        "notes": lead.notes,
                    }
                ),
            }
        )

        # Update project lead count
        await db.project.update(
            {"where": {"id": lead.project_id}, "data": {"leadsCount": {"increment": 1}}}
        )

        return LeadResponse(
            id=new_lead.id,
            business_name=new_lead.business_name,
            contact=new_lead.contact,
            url=new_lead.url,
            keywords=new_lead.keywords,
            source=new_lead.source,
            area=new_lead.area,
            project_id=new_lead.projectId,
            score=new_lead.score,
            status=new_lead.status,
            platform_sumber=new_lead.platformSumber,
            jabatan=new_lead.jabatan,
            nomor_hp=new_lead.nomorHp,
            notes=lead.notes,
            priority=new_lead.priority,
            date_found=new_lead.dateFound,
            created_at=new_lead.createdAt,
            updated_at=new_lead.updatedAt,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lead: {str(e)}")


@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    project_id: str = Query(
        ..., description="Project ID is mandatory for data isolation"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None, pattern="^(new|contacted|qualified|closed)$"),
    search: Optional[str] = Query(None),
    db: PrismaClient = Depends(get_db),
):
    """Get leads with strict project isolation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)

        # Build query with mandatory project filter
        where_clause = {
            "projectId": project_id  # MANDATORY: Always filter by project
        }

        # Add optional filters
        if status:
            where_clause["status"] = status

        if search:
            where_clause["OR"] = [
                {"business_name": {"contains": search, "mode": "insensitive"}},
                {"contact": {"contains": search, "mode": "insensitive"}},
                {"area": {"contains": search, "mode": "insensitive"}},
            ]

        # Query with strict project isolation
        leads = await db.lead.find_many(
            where=where_clause, skip=skip, take=limit, order={"createdAt": "desc"}
        )

        return [
            LeadResponse(
                id=lead.id,
                business_name=lead.business_name,
                contact=lead.contact,
                url=lead.url,
                keywords=lead.keywords,
                source=lead.source,
                area=lead.area,
                project_id=lead.projectId,
                score=lead.score,
                status=lead.status,
                priority=lead.priority,
                date_found=lead.dateFound,
                created_at=lead.createdAt,
                updated_at=lead.updatedAt,
            )
            for lead in leads
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leads: {str(e)}")


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    project_id: str = Query(
        ..., description="Project ID is mandatory for data isolation"
    ),
    db: PrismaClient = Depends(get_db),
):
    """Get specific lead with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)

        # Find lead with project isolation
        lead = await db.lead.find_first(
            where={
                "id": lead_id,
                "projectId": project_id,  # MANDATORY: Ensure lead belongs to project
            }
        )

        if not lead:
            raise HTTPException(
                status_code=404, detail="Lead not found or access denied"
            )

        return LeadResponse(
            id=lead.id,
            business_name=lead.business_name,
            contact=lead.contact,
            url=lead.url,
            keywords=lead.keywords,
            source=lead.source,
            area=lead.area,
            project_id=lead.projectId,
            score=lead.score,
            status=lead.status,
            priority=lead.priority,
            date_found=lead.dateFound,
            created_at=lead.createdAt,
            updated_at=lead.updatedAt,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lead: {str(e)}")


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    lead_update: LeadUpdate,
    project_id: str = Query(
        ..., description="Project ID is mandatory for data isolation"
    ),
    db: PrismaClient = Depends(get_db),
):
    """Update lead with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)

        # Check if lead exists and belongs to project
        existing_lead = await db.lead.find_first(
            where={
                "id": lead_id,
                "projectId": project_id,  # MANDATORY: Ensure lead belongs to project
            }
        )

        if not existing_lead:
            raise HTTPException(
                status_code=404, detail="Lead not found or access denied"
            )

        # Prepare update data
        update_data = {}
        if lead_update.business_name is not None:
            update_data["business_name"] = lead_update.business_name
        if lead_update.contact is not None:
            update_data["contact"] = lead_update.contact
        if lead_update.url is not None:
            update_data["url"] = lead_update.url
        if lead_update.keywords is not None:
            update_data["keywords"] = lead_update.keywords
        if lead_update.source is not None:
            update_data["source"] = lead_update.source
        if lead_update.area is not None:
            update_data["area"] = lead_update.area
        if lead_update.score is not None:
            update_data["score"] = lead_update.score
        if lead_update.status is not None:
            update_data["status"] = lead_update.status
        if lead_update.notes is not None:
            update_data["encryptedData"] = json.dumps(
                {
                    "business_name": lead_update.business_name
                    or existing_lead.business_name,
                    "contact": lead_update.contact or existing_lead.contact,
                    "url": lead_update.url or existing_lead.url,
                    "keywords": lead_update.keywords or existing_lead.keywords,
                    "area": lead_update.area or existing_lead.area,
                    "notes": lead_update.notes,
                }
            )
        if lead_update.priority is not None:
            update_data["priority"] = lead_update.priority.upper()

        # Update lead
        updated_lead = await db.lead.update(where={"id": lead_id}, data=update_data)

        return LeadResponse(
            id=updated_lead.id,
            business_name=updated_lead.business_name,
            contact=updated_lead.contact,
            url=updated_lead.url,
            keywords=updated_lead.keywords,
            source=updated_lead.source,
            area=updated_lead.area,
            project_id=updated_lead.projectId,
            score=updated_lead.score,
            status=updated_lead.status,
            priority=updated_lead.priority,
            date_found=updated_lead.dateFound,
            created_at=updated_lead.createdAt,
            updated_at=updated_lead.updatedAt,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update lead: {str(e)}")


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: str,
    project_id: str = Query(
        ..., description="Project ID is mandatory for data isolation"
    ),
    db: PrismaClient = Depends(get_db),
):
    """Delete lead with project validation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)

        # Check if lead exists and belongs to project
        existing_lead = await db.lead.find_first(
            where={
                "id": lead_id,
                "projectId": project_id,  # MANDATORY: Ensure lead belongs to project
            }
        )

        if not existing_lead:
            raise HTTPException(
                status_code=404, detail="Lead not found or access denied"
            )

        # Delete lead
        await db.lead.delete(where={"id": lead_id})

        # Update project lead count
        await db.project.update(
            {"where": {"id": project_id}, "data": {"leadsCount": {"decrement": 1}}}
        )

        return {"message": "Lead deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete lead: {str(e)}")


@router.post("/public-submit")
async def public_submit_lead(
    nama: str,
    nomor_hp: str,
    project_id: str,
    project_type: str,
    source: str = "landing_page_public",
    db: PrismaClient = Depends(get_db),
):
    """
    Public webhook endpoint for lead submission from landing page
    No authentication required - accessible by public
    """
    try:
        # Validate project exists and is active
        validate_project_exists(db, project_id)

        # Check for duplicate phone number within the same project
        if nomor_hp:
            is_duplicate = check_duplicate_lead(db, nomor_hp, project_id)
            if is_duplicate:
                return {
                    "status": "duplicate",
                    "message": f"Lead with phone number {nomor_hp} already exists in this project",
                    "lead_id": None,
                }

        # Create lead in database
        new_lead = await db.lead.create(
            {
                "business_name": nama,  # Use nama as business_name for simplicity
                "contact": nomor_hp,  # Use nomor_hp as contact
                "url": "",  # Empty URL for public submission
                "keywords": [project_type, source],
                "source": source,
                "area": "",  # Will be filled from project data if needed
                "projectId": project_id,
                "status": "NEW",  # Set status to NEW for public submissions
                "priority": "MEDIUM",
                "platformSumber": None,
                "jabatan": None,
                "nomorHp": nomor_hp,  # Store phone number for deduplication
                "dateFound": datetime.now(),
                "encryptedData": json.dumps(
                    {
                        "nama": nama,
                        "nomor_hp": nomor_hp,
                        "project_id": project_id,
                        "project_type": project_type,
                        "source": source,
                        "submission_time": datetime.now().isoformat(),
                    }
                ),
            }
        )

        # Update project lead count
        await db.project.update(
            {"where": {"id": project_id}, "data": {"leadsCount": {"increment": 1}}}
        )

        # Log activity (optional, won't fail if not available)
        try:
            from prisma import PrismaClient as PrismaLogClient

            log_db = PrismaLogClient()
            log_db.vrsentinellog.create(
                {
                    "action": "public_lead_submit",
                    "details": f"Public lead submission: {nama} - {nomor_hp}",
                    "gazeData": {
                        "source": source,
                        "project_id": project_id,
                        "project_type": project_type,
                        "lead_id": new_lead.id,
                    },
                    "timestamp": datetime.now(),
                }
            )
            log_db.disconnect()
        except Exception as log_error:
            # Don't fail the main operation if logging fails
            print(f"Warning: Failed to log activity: {str(log_error)}")

        return {
            "status": "success",
            "message": "Lead submitted successfully",
            "lead_id": new_lead.id,
            "data": {
                "id": new_lead.id,
                "nama": nama,
                "nomor_hp": nomor_hp,
                "project_id": project_id,
                "project_type": project_type,
                "status": "NEW",
                "created_at": new_lead.createdAt.isoformat(),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to submit lead: {str(e)}",
            "lead_id": None,
        }


@router.get("/stats/summary")
async def get_lead_stats(
    project_id: str = Query(
        ..., description="Project ID is mandatory for data isolation"
    ),
    db: PrismaClient = Depends(get_db),
):
    """Get lead statistics with project isolation"""
    try:
        # Validate project exists
        validate_project_exists(db, project_id)

        # Get statistics with project isolation
        total_leads = await db.lead.count(where={"projectId": project_id})

        leads_by_status = await db.lead.group_by(
            by=["status"], where={"projectId": project_id}, count={"status": True}
        )

        hot_leads = await db.lead.count(
            where={"projectId": project_id, "score": {"gte": 80}}
        )

        return {
            "project_id": project_id,
            "total_leads": total_leads,
            "hot_leads": hot_leads,
            "leads_by_status": {
                item["status"]: item["_count"]["status"] for item in leads_by_status
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch lead statistics: {str(e)}"
        )
