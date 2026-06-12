"""
VR API Endpoints
Virtual Reality, 3D models, and gaze tracking operations
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from datetime import datetime
import json

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Pydantic models
class VRSentinelLogRequest(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    campaign_id: Optional[str] = None
    gaze_data: Dict[str, Any]
    object_name: Optional[str] = None
    focus_duration: Optional[float] = None
    interaction_type: str = "VIEW"
    position: Optional[Dict[str, float]] = None
    rotation: Optional[Dict[str, float]] = None
    viewport: Optional[Dict[str, Any]] = None
    lead_intent: Optional[str] = None
    confidence: Optional[float] = None
    tags: Optional[List[str]] = None

class VRSessionRequest(BaseModel):
    user_id: Optional[str] = None
    campaign_id: Optional[str] = None
    model_path: str
    skybox_image: Optional[str] = None
    enable_gaze_tracking: bool = True
    enable_time_sync: bool = True

# Dependency for database connection
async def get_db():
    """Get database connection"""
    try:
        from core_modules.db_manager_postgres import postgres_db_manager
        return postgres_db_manager
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@router.post("/log-gaze-data")
async def log_gaze_data(
    request: VRSentinelLogRequest,
    db = Depends(get_db)
):
    """
    Log VR Sentinel gaze tracking data
    """
    try:
        logger.info(f"Logging gaze data for session: {request.session_id}")
        
        # Submit task to Celery
        from tasks.maintenance_tasks import process_vr_gaze_data
        task = process_vr_gaze_data.s(
            session_id=request.session_id,
            user_id=request.user_id,
            campaign_id=request.campaign_id,
            gaze_data=request.gaze_data,
            object_name=request.object_name,
            focus_duration=request.focus_duration,
            interaction_type=request.interaction_type,
            position=request.position,
            rotation=request.rotation,
            viewport=request.viewport,
            lead_intent=request.lead_intent,
            confidence=request.confidence,
            tags=request.tags or []
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "session_id": request.session_id,
            "object_name": request.object_name,
            "message": "Gaze data logged successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to log gaze data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-vr-session")
async def create_vr_session(
    request: VRSessionRequest,
    db = Depends(get_db)
):
    """
    Create new VR session
    """
    try:
        logger.info(f"Creating VR session: {request.model_path}")
        
        # Generate session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # Create session record
        session_data = {
            'session_id': session_id,
            'user_id': request.user_id,
            'campaign_id': request.campaign_id,
            'model_path': request.model_path,
            'skybox_image': request.skybox_image,
            'enable_gaze_tracking': request.enable_gaze_tracking,
            'enable_time_sync': request.enable_time_sync,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        return {
            "success": True,
            "session_id": session_id,
            "vr_config": session_data,
            "message": "VR session created successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to create VR session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_vr_session(
    session_id: str,
    db = Depends(get_db)
):
    """
    Get VR session details
    """
    try:
        # In a real implementation, this would query the database
        # For now, return mock session data
        session_data = {
            'session_id': session_id,
            'user_id': 'user_123',
            'campaign_id': 'campaign_456',
            'model_path': '/models/masterplan.glb',
            'skybox_image': '/skyboxes/daytime.jpg',
            'enable_gaze_tracking': True,
            'enable_time_sync': True,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        return {
            "success": True,
            "session": session_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get VR session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/gaze-logs")
async def get_gaze_logs(
    session_id: str,
    limit: int = 100,
    db = Depends(get_db)
):
    """
    Get gaze logs for a session
    """
    try:
        # Query VR Sentinel logs
        logs = await db.execute_query(
            """
            SELECT * FROM VRSentinelLog 
            WHERE sessionId = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
            """,
            (session_id, limit)
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "logs": logs,
            "total": len(logs)
        }
        
    except Exception as e:
        logger.error(f"Failed to get gaze logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_available_models():
    """
    Get available 3D models for VR
    """
    try:
        # Scan models directory
        models_dir = "models/3d"
        models = []
        
        if os.path.exists(models_dir):
            for file in os.listdir(models_dir):
                if file.endswith(('.glb', '.gltf', '.fbx')):
                    models.append({
                        'name': file,
                        'path': f"{models_dir}/{file}",
                        'type': file.split('.')[-1]
                    })
        
        return {
            "success": True,
            "models": models,
            "total": len(models)
        }
        
    except Exception as e:
        logger.error(f"Failed to get available models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skyboxes")
async def get_available_skyboxes():
    """
    Get available skybox images for VR
    """
    try:
        # Scan skybox directory
        skybox_dir = "assets/skyboxes"
        skyboxes = []
        
        if os.path.exists(skybox_dir):
            for file in os.listdir(skybox_dir):
                if file.endswith(('.jpg', '.jpeg', '.png', '.hdr')):
                    skyboxes.append({
                        'name': file,
                        'path': f"{skybox_dir}/{file}",
                        'type': file.split('.')[-1]
                    })
        
        return {
            "success": True,
            "skyboxes": skyboxes,
            "total": len(skyboxes)
        }
        
    except Exception as e:
        logger.error(f"Failed to get available skyboxes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-gaze-patterns")
async def analyze_gaze_patterns(
    session_id: str,
    db = Depends(get_db)
):
    """
    Analyze gaze patterns for a session
    """
    try:
        logger.info(f"Analyzing gaze patterns for session: {session_id}")
        
        # Get gaze logs
        logs = await db.execute_query(
            """
            SELECT * FROM VRSentinelLog 
            WHERE sessionId = ? 
            ORDER BY timestamp ASC
            """,
            (session_id,)
        )
        
        if not logs:
            return {
                "success": True,
                "session_id": session_id,
                "analysis": {
                    "total_gaze_points": 0,
                    "most_viewed_objects": [],
                    "average_focus_duration": 0,
                    "interaction_types": {},
                    "lead_intent_confidence": 0
                }
            }
        
        # Analyze patterns
        object_views = {}
        total_duration = 0
        interaction_types = {}
        lead_intents = []
        
        for log in logs:
            object_name = log.get('objectName', 'unknown')
            duration = log.get('focusDuration', 0) or 0
            interaction_type = log.get('interactionType', 'VIEW')
            lead_intent = log.get('leadIntent')
            confidence = log.get('confidence', 0) or 0
            
            # Count object views
            if object_name not in object_views:
                object_views[object_name] = {'count': 0, 'total_duration': 0}
            object_views[object_name]['count'] += 1
            object_views[object_name]['total_duration'] += duration
            
            # Track interaction types
            if interaction_type not in interaction_types:
                interaction_types[interaction_type] = 0
            interaction_types[interaction_type] += 1
            
            # Track lead intents
            if lead_intent and confidence > 0.5:
                lead_intents.append((lead_intent, confidence))
            
            total_duration += duration
        
        # Calculate statistics
        most_viewed_objects = sorted(
            object_views.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:5]
        
        avg_duration = total_duration / len(logs) if logs else 0
        
        avg_confidence = sum(conf for _, conf in lead_intents) / len(lead_intents) if lead_intents else 0
        
        analysis = {
            "total_gaze_points": len(logs),
            "most_viewed_objects": [
                {"name": name, "stats": stats} 
                for name, stats in most_viewed_objects
            ],
            "average_focus_duration": avg_duration,
            "interaction_types": interaction_types,
            "lead_intent_confidence": avg_confidence,
            "high_confidence_intents": len([c for _, c in lead_intents if c > 0.8])
        }
        
        return {
            "success": True,
            "session_id": session_id,
            "analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Failed to analyze gaze patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/gaze-tracking/{session_id}")
async def websocket_gaze_tracking(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time gaze tracking
    """
    await websocket.accept()
    logger.info(f"WebSocket connected for gaze tracking: {session_id}")
    
    try:
        while True:
            # Receive gaze data
            data = await websocket.receive_text()
            gaze_data = json.loads(data)
            
            # Process gaze data
            processed_data = {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                **gaze_data
            }
            
            # Send acknowledgment
            await websocket.send_text(json.dumps({
                "status": "received",
                "session_id": session_id,
                "timestamp": processed_data["timestamp"]
            }))
            
            # Here you would typically:
            # 1. Log to database
            # 2. Trigger gaze effects
            # 3. Update lead scoring
            # 4. Send notifications if high intent detected
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

@router.get("/stats")
async def get_vr_stats(db = Depends(get_db)):
    """
    Get VR statistics
    """
    try:
        # Get VR session statistics
        total_sessions = await db.execute_query("SELECT COUNT(*) as count FROM VRSession")
        total_gaze_logs = await db.execute_query("SELECT COUNT(*) as count FROM VRSentinelLog")
        
        # Get recent activity
        recent_sessions = await db.execute_query(
            "SELECT * FROM VRSession ORDER BY createdAt DESC LIMIT 10"
        )
        
        return {
            "success": True,
            "statistics": {
                "total_sessions": total_sessions[0]['count'] if total_sessions else 0,
                "total_gaze_logs": total_gaze_logs[0]['count'] if total_gaze_logs else 0,
                "recent_sessions": recent_sessions
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get VR stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}")
async def get_vr_task_status(task_id: str):
    """
    Get VR task status by ID
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
