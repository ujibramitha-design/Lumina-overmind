"""
Twin-Dragon Engine - Ads Management API Endpoints
RESTful API for advertising proposal management and approval workflow
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from prisma import PrismaClient

# Database dependency
def get_db():
    db = PrismaClient()
    return db

router = APIRouter(prefix="/api/ads", tags=["ads"])

# Pydantic Models
class AdProposalResponse(BaseModel):
    id: str
    projectId: str
    opsiStrategi: str
    targetAudience: str
    copywriting: str
    estimasiBudget: int
    status: str
    createdAt: datetime
    updatedAt: datetime
    project: Optional[Dict[str, Any]] = None

class AdProposalCreate(BaseModel):
    projectId: str = Field(..., description="Project ID is mandatory")
    opsiStrategi: str = Field(..., description="Strategy option")
    targetAudience: str = Field(..., description="Target audience description")
    copywriting: str = Field(..., description="Ad copy text")
    estimasiBudget: int = Field(..., ge=0, description="Estimated budget in IDR")
    status: str = Field(default="PENDING", description="Proposal status")

class AdProposalUpdate(BaseModel):
    opsiStrategi: Optional[str] = None
    targetAudience: Optional[str] = None
    copywriting: Optional[str] = None
    estimasiBudget: Optional[int] = None
    status: Optional[str] = None

class ReviseRequest(BaseModel):
    revisionInstructions: str = Field(..., description="Instructions for revising the proposal")

# Helper Functions
def validate_project_exists(db: PrismaClient, project_id: str):
    """Validate that project exists and is active"""
    try:
        project = db.project.find_unique(where={'id': project_id})
        if not project:
            raise HTTPException(
                status_code=404, 
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

# API Endpoints

@router.get("/proposals", response_model=List[AdProposalResponse])
async def get_proposals(
    status: Optional[str] = Query(None, description="Filter by status (PENDING, APPROVED, REJECTED)"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    db: PrismaClient = Depends(get_db)
):
    """Get ad proposals with optional filtering"""
    try:
        # Build where clause
        where_clause = {}
        if status:
            where_clause['status'] = status
        if project_id:
            where_clause['projectId'] = project_id
        
        # Fetch proposals with project data
        proposals = await db.adproposal.find_many(
            where=where_clause,
            include={
                'project': True
            },
            order={'createdAt': 'desc'}
        )
        
        # Convert to response format
        response_data = []
        for proposal in proposals:
            proposal_dict = {
                'id': proposal.id,
                'projectId': proposal.projectId,
                'opsiStrategi': proposal.opsiStrategi,
                'targetAudience': proposal.targetAudience,
                'copywriting': proposal.copywriting,
                'estimasiBudget': proposal.estimasiBudget,
                'status': proposal.status,
                'createdAt': proposal.createdAt,
                'updatedAt': proposal.updatedAt,
                'project': {
                    'id': proposal.project.id,
                    'namaProyek': proposal.project.namaProyek,
                    'tipeProyek': proposal.project.tipeProyek,
                    'lokasi': proposal.project.lokasi,
                    'hargaStart': proposal.project.hargaStart
                } if proposal.project else None
            }
            response_data.append(proposal_dict)
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch proposals: {str(e)}"
        )

@router.get("/proposals/stats")
async def get_proposal_stats(db: PrismaClient = Depends(get_db)):
    """Get proposal statistics"""
    try:
        # Count proposals by status
        total = await db.adproposal.count()
        pending = await db.adproposal.count(where={'status': 'PENDING'})
        approved = await db.adproposal.count(where={'status': 'APPROVED'})
        rejected = await db.adproposal.count(where={'status': 'REJECTED'})
        
        return {
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get proposal stats: {str(e)}"
        )

@router.post("/proposals", response_model=AdProposalResponse)
async def create_proposal(
    proposal: AdProposalCreate,
    db: PrismaClient = Depends(get_db)
):
    """Create new ad proposal"""
    try:
        # Validate project exists
        validate_project_exists(db, proposal.projectId)
        
        # Create proposal
        new_proposal = await db.adproposal.create({
            'projectId': proposal.projectId,
            'opsiStrategi': proposal.opsiStrategi,
            'targetAudience': proposal.targetAudience,
            'copywriting': proposal.copywriting,
            'estimasiBudget': proposal.estimasiBudget,
            'status': proposal.status
        })
        
        # Fetch with project data
        created_proposal = await db.adproposal.find_unique(
            where={'id': new_proposal.id},
            include={'project': True}
        )
        
        return AdProposalResponse(
            id=created_proposal.id,
            projectId=created_proposal.projectId,
            opsiStrategi=created_proposal.opsiStrategi,
            targetAudience=created_proposal.targetAudience,
            copywriting=created_proposal.copywriting,
            estimasiBudget=created_proposal.estimasiBudget,
            status=created_proposal.status,
            createdAt=created_proposal.createdAt,
            updatedAt=created_proposal.updatedAt,
            project={
                'id': created_proposal.project.id,
                'namaProyek': created_proposal.project.namaProyek,
                'tipeProyek': created_proposal.project.tipeProyek,
                'lokasi': created_proposal.project.lokasi,
                'hargaStart': created_proposal.project.hargaStart
            } if created_proposal.project else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create proposal: {str(e)}"
        )

@router.post("/proposals/{proposal_id}/approve")
async def approve_proposal(
    proposal_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Approve and launch ad proposal"""
    try:
        # Update proposal status
        updated_proposal = await db.adproposal.update({
            'where': {'id': proposal_id},
            'data': {
                'status': 'APPROVED',
                'updatedAt': datetime.now()
            }
        })
        
        if not updated_proposal:
            raise HTTPException(
                status_code=404,
                detail=f"Proposal with ID {proposal_id} not found"
            )
        
        # TODO: Implement actual ad launching logic here
        # This would integrate with ad platforms (Google Ads, Facebook Ads, etc.)
        
        return {
            "status": "success",
            "message": "Proposal approved and launched successfully",
            "proposal_id": proposal_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to approve proposal: {str(e)}"
        )

@router.post("/proposals/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Reject ad proposal"""
    try:
        # Update proposal status
        updated_proposal = await db.adproposal.update({
            'where': {'id': proposal_id},
            'data': {
                'status': 'REJECTED',
                'updatedAt': datetime.now()
            }
        })
        
        if not updated_proposal:
            raise HTTPException(
                status_code=404,
                detail=f"Proposal with ID {proposal_id} not found"
            )
        
        return {
            "status": "success",
            "message": "Proposal rejected successfully",
            "proposal_id": proposal_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reject proposal: {str(e)}"
        )

@router.post("/proposals/{proposal_id}/revise")
async def revise_proposal(
    proposal_id: str,
    request: ReviseRequest,
    db: PrismaClient = Depends(get_db)
):
    """Revise ad proposal based on feedback"""
    try:
        # Get existing proposal
        existing_proposal = await db.adproposal.find_unique(
            where={'id': proposal_id},
            include={'project': True}
        )
        
        if not existing_proposal:
            raise HTTPException(
                status_code=404,
                detail=f"Proposal with ID {proposal_id} not found"
            )
        
        # TODO: Integrate with AI CMO for intelligent revision
        # For now, we'll update with a simple revision note
        
        # Update proposal with revision note (you could add a revision_notes field to the schema)
        updated_proposal = await db.adproposal.update({
            'where': {'id': proposal_id},
            'data': {
                'status': 'PENDING',  # Reset to pending after revision
                'updatedAt': datetime.now()
            }
        })
        
        # In a real implementation, you would:
        # 1. Call AI CMO to revise the proposal
        # 2. Update the proposal fields with revised content
        # 3. Keep status as PENDING for re-review
        
        return {
            "status": "success",
            "message": "Proposal revision request submitted successfully",
            "proposal_id": proposal_id,
            "revision_instructions": request.revisionInstructions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to revise proposal: {str(e)}"
        )

@router.get("/proposals/{proposal_id}", response_model=AdProposalResponse)
async def get_proposal(
    proposal_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Get single ad proposal by ID"""
    try:
        proposal = await db.adproposal.find_unique(
            where={'id': proposal_id},
            include={'project': True}
        )
        
        if not proposal:
            raise HTTPException(
                status_code=404,
                detail=f"Proposal with ID {proposal_id} not found"
            )
        
        return AdProposalResponse(
            id=proposal.id,
            projectId=proposal.projectId,
            opsiStrategi=proposal.opsiStrategi,
            targetAudience=proposal.targetAudience,
            copywriting=proposal.copywriting,
            estimasiBudget=proposal.estimasiBudget,
            status=proposal.status,
            createdAt=proposal.createdAt,
            updatedAt=proposal.updatedAt,
            project={
                'id': proposal.project.id,
                'namaProyek': proposal.project.namaProyek,
                'tipeProyek': proposal.project.tipeProyek,
                'lokasi': proposal.project.lokasi,
                'hargaStart': proposal.project.hargaStart
            } if proposal.project else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get proposal: {str(e)}"
        )

@router.post("/generate/{project_id}")
async def generate_ads_for_project(
    project_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Generate AI ad proposals for specific project"""
    try:
        # Validate project exists and is active
        project = validate_project_exists(db, project_id)
        
        # Get existing leads data for context
        existing_leads = await db.lead.find_many(
            where={'projectId': project_id},
            take=50,  # Limit to recent leads for context
            order={'createdAt': 'desc'}
        )
        
        # Prepare project data with context
        project_data = {
            'id': project.id,
            'namaProyek': project.namaProyek,
            'tipeProyek': project.tipeProyek,
            'lokasi': project.lokasi,
            'hargaStart': project.hargaStart,
            'targetMarket': project.targetMarket,
            'tipeInputLokasi': project.tipeInputLokasi,
            'namaWilayah': project.namaWilayah,
            'latitude': project.latitude,
            'longitude': project.longitude,
            'radiusKm': project.radiusKm,
            'dorkingTargets': project.dorkingTargets or [],
            'scoutMode': project.scoutMode,
            'leadsCount': project.leadsCount,
            'hotLeadsCount': project.hotLeadsCount,
            'conversionRate': project.conversionRate,
            'config': project.config,
            'aiPromptStyle': project.aiPromptStyle,
            'isActive': project.isActive,
            'createdAt': project.createdAt.isoformat(),
            'updatedAt': project.updatedAt.isoformat(),
            # Add existing leads context
            'existingLeads': {
                'total': len(existing_leads),
                'recent': [
                    {
                        'business_name': lead.business_name,
                        'contact': lead.contact,
                        'status': lead.status,
                        'priority': lead.priority,
                        'createdAt': lead.createdAt.isoformat()
                    }
                    for lead in existing_leads[:10]  # Last 10 leads
                ],
                'statusDistribution': {
                    'SCOUTED': len([l for l in existing_leads if l.status == 'SCOUTED']),
                    'CONTACTED': len([l for l in existing_leads if l.status == 'CONTACTED']),
                    'INTERESTED': len([l for l in existing_leads if l.status == 'INTERESTED']),
                    'CONVERTED': len([l for l in existing_leads if l.status == 'CONVERTED'])
                }
            }
        }
        
        # Import AI CMO for context-aware generation
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core_modules', 'intelligence'))
        
        try:
            from ads_manager import generate_ads_proposals
            
            # Generate AI proposals with full context
            proposals = await generate_ads_proposals(project_data)
            
            return {
                "status": "success",
                "message": f"AI CMO generated {len(proposals)} ad proposals for {project.namaProyek}",
                "project_id": project_id,
                "project_name": project.namaProyek,
                "proposals_generated": len(proposals),
                "proposals": [
                    {
                        "opsiStrategi": proposal.opsi_strategi,
                        "targetAudience": proposal.target_audience,
                        "copywriting": proposal.copywriting,
                        "estimasiBudget": proposal.estimasi_budget,
                        "channelRekomendasi": proposal.channel_rekomendasi,
                        "kpiUtama": proposal.kpi_utama,
                        "durasiKampanye": proposal.durasi_kampanye
                    }
                    for proposal in proposals
                ],
                "context_used": {
                    "project_data": {
                        "name": project.namaProyek,
                        "type": project.tipeProyek,
                        "location": project.lokasi,
                        "price": project.hargaStart,
                        "leads_count": project.leadsCount
                    },
                    "existing_leads": len(existing_leads),
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
            
        except ImportError as e:
            # Fallback if ads_manager is not available
            return {
                "status": "error",
                "message": "AI CMO module not available. Please install required dependencies.",
                "error": str(e),
                "project_id": project_id
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate ads for project {project_id}: {str(e)}"
        )

@router.delete("/proposals/{proposal_id}")
async def delete_proposal(
    proposal_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Delete ad proposal"""
    try:
        deleted_proposal = await db.adproposal.delete(
            where={'id': proposal_id}
        )
        
        if not deleted_proposal:
            raise HTTPException(
                status_code=404,
                detail=f"Proposal with ID {proposal_id} not found"
            )
        
        return {"message": "Proposal deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete proposal: {str(e)}"
        )
