"""
Twin-Dragon Engine - Activities API Endpoint
Project-aware activity logging and retrieval
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from prisma import Client as PrismaClient

# Database dependency
def get_db():
    db = PrismaClient()
    return db

router = APIRouter(prefix="/api/activities", tags=["activities"])

# Pydantic Models
class ActivityResponse(BaseModel):
    id: str
    action: str
    details: Optional[str] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    project_type: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: datetime
    metadata: Optional[dict] = None

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

async def log_activity(
    db: PrismaClient,
    action: str,
    details: Optional[str] = None,
    project_id: Optional[str] = None,
    user_id: Optional[str] = None,
    metadata: Optional[dict] = None
):
    """Log activity to database with project awareness"""
    try:
        # Get project details if project_id is provided
        project_name = None
        project_type = None
        
        if project_id:
            project = db.project.find_unique(where={'id': project_id})
            if project:
                project_name = project.namaProyek
                project_type = project.tipeProyek
        
        # Create activity log
        activity = await db.vrsentinellog.create({
            'action': action,
            'details': details or f"{action} operation completed",
            'projectId': project_id,
            'userId': user_id,
            'timestamp': datetime.now(),
            'gazeData': {
                'project_name': project_name,
                'project_type': project_type,
                'metadata': metadata or {}
            }
        })
        
        return activity
        
    except Exception as e:
        # Log error but don't fail the operation
        print(f"Error logging activity: {str(e)}")
        return None

# API Endpoints
@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    project_id: Optional[str] = Query(None, description="Project ID for filtering activities"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    action: Optional[str] = Query(None, description="Filter by action type"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    db: PrismaClient = Depends(get_db)
):
    """Get activities with optional project filtering"""
    try:
        # Validate project if provided
        if project_id:
            validate_project_exists(db, project_id)
        
        # Build query
        where_clause = {}
        
        if project_id:
            where_clause['projectId'] = project_id
            
        if action:
            where_clause['action'] = {'contains': action, 'mode': 'insensitive'}
            
        if user_id:
            where_clause['userId'] = user_id
        
        # Query activities
        activities = await db.vrsentinellog.find_many(
            where=where_clause,
            skip=skip,
            take=limit,
            order={'timestamp': 'desc'}
        )
        
        # Transform to response format
        response_activities = []
        for activity in activities:
            gaze_data = activity.gazeData or {}
            response_activities.append({
                'id': activity.id,
                'action': activity.action,
                'details': activity.details,
                'project_id': activity.projectId,
                'project_name': gaze_data.get('project_name'),
                'project_type': gaze_data.get('project_type'),
                'user_id': activity.userId,
                'timestamp': activity.timestamp,
                'metadata': gaze_data.get('metadata')
            })
        
        return response_activities
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch activities: {str(e)}"
        )

@router.get("/stats/summary")
async def get_activity_stats(
    project_id: Optional[str] = Query(None, description="Project ID for filtering stats"),
    db: PrismaClient = Depends(get_db)
):
    """Get activity statistics with optional project filtering"""
    try:
        # Validate project if provided
        if project_id:
            validate_project_exists(db, project_id)
        
        # Build query
        where_clause = {}
        if project_id:
            where_clause['projectId'] = project_id
        
        # Get total activities
        total_activities = await db.vrsentinellog.count(where=where_clause)
        
        # Get activities by action type
        activities_by_action = await db.vrsentinellog.group_by(
            by=['action'],
            where=where_clause,
            count={'action': True}
        )
        
        # Get recent activities (last 24 hours)
        recent_cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        recent_activities = await db.vrsentinellog.count(
            where={
                **where_clause,
                'timestamp': {'gte': recent_cutoff}
            }
        )
        
        return {
            'project_id': project_id,
            'total_activities': total_activities,
            'recent_24h': recent_activities,
            'activities_by_action': {
                item['action']: item['_count']['action'] 
                for item in activities_by_action
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch activity stats: {str(e)}"
        )

@router.post("/log")
async def create_activity_log(
    action: str = Field(..., description="Activity description"),
    details: Optional[str] = Field(None, description="Additional details"),
    project_id: Optional[str] = Field(None, description="Project ID"),
    user_id: Optional[str] = Field(None, description="User ID"),
    metadata: Optional[dict] = Field(None, description="Additional metadata"),
    db: PrismaClient = Depends(get_db)
):
    """Create activity log entry"""
    try:
        # Validate project if provided
        if project_id:
            validate_project_exists(db, project_id)
        
        # Create activity log
        activity = await log_activity(
            db=db,
            action=action,
            details=details,
            project_id=project_id,
            user_id=user_id,
            metadata=metadata
        )
        
        if activity:
            return {
                "success": True,
                "message": "Activity logged successfully",
                "activity_id": activity.id
            }
        else:
            return {
                "success": False,
                "message": "Failed to log activity"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create activity log: {str(e)}"
        )
