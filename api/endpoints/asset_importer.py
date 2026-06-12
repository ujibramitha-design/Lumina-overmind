"""
ASSET IMPORTER - Siteplan Upload and Management
Handles file uploads from Archidep system and bridges to VFX pipeline
"""

import logging
import os
import hashlib
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prisma import Client as PrismaClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/assets", tags=["Asset Importer"])

# Pydantic models
class SiteplanUploadResponse(BaseModel):
    id: str
    project_name: str
    file_url: str
    file_type: str
    file_size: int
    status: str
    uploaded_at: datetime

class SiteplanListItem(BaseModel):
    id: str
    project_name: str
    file_type: str
    file_size: Optional[int]
    status: str
    uploaded_at: datetime
    processed_at: Optional[datetime]
    completed_at: Optional[datetime]

class SiteplanStatusUpdate(BaseModel):
    status: str = Field(..., regex="^(READY_FOR_VFX|RENDERING|PUBLISHED|FAILED)$")

# Database dependency
def get_db():
    db = PrismaClient()
    return db

# File upload configuration
UPLOAD_DIR = "uploads/siteplans"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".pdf", ".obj", ".fbx", ".dae", ".3ds", ".blend", ".mp4", ".mov", ".avi"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def ensure_upload_dir():
    """Ensure upload directory exists"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_file_type(filename: str) -> str:
    """Determine file type from filename"""
    ext = os.path.splitext(filename)[1].lower()
    
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    model_extensions = {".obj", ".fbx", ".dae", ".3ds", ".blend"}
    video_extensions = {".mp4", ".mov", ".avi"}
    
    if ext in image_extensions:
        return "IMAGE"
    elif ext in model_extensions:
        return "3D_MODEL"
    elif ext in video_extensions:
        return "VIDEO"
    elif ext == ".pdf":
        return "PDF"
    else:
        return "UNKNOWN"

def calculate_file_hash(file_content: bytes) -> str:
    """Calculate SHA-256 hash of file content"""
    return hashlib.sha256(file_content).hexdigest()

@router.post("/upload-siteplan", response_model=SiteplanUploadResponse)
async def upload_siteplan(
    project_name: str = Form(...),
    file: UploadFile = File(...),
    project_id: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    db: PrismaClient = Depends(get_db)
):
    """
    Upload siteplan file from Archidep system
    
    This endpoint receives completed siteplan files from the external Archidep
    system and prepares them for VFX processing in the Lumina OS pipeline.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file_size} bytes exceeds maximum {MAX_FILE_SIZE} bytes"
            )
        
        # Calculate file hash for integrity
        file_hash = calculate_file_hash(file_content)
        
        # Ensure upload directory exists
        ensure_upload_dir()
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        # Save file locally
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Determine file type
        file_type = get_file_type(file.filename)
        
        # Parse metadata if provided
        parsed_metadata = {}
        if metadata:
            try:
                parsed_metadata = json.loads(metadata)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON metadata provided: {metadata}")
        
        # Save to database
        siteplan = db.importedsiteplan.create({
            'project_name': project_name,
            'file_url': file_path,
            'file_type': file_type,
            'file_size': file_size,
            'file_hash': file_hash,
            'status': 'READY_FOR_VFX',
            'metadata': parsed_metadata,
            'projectId': project_id
        })
        
        logger.info(f"Siteplan uploaded successfully: {project_name} ({file_type})")
        
        # TODO: Connect to core_modules.visual.multipass_compositor
        # This file will be directly thrown to our VFX machine
        # for automatic processing and enhancement
        logger.info(f"TODO: Trigger VFX processing for siteplan {siteplan.id}")
        
        return SiteplanUploadResponse(
            id=siteplan.id,
            project_name=siteplan.project_name,
            file_url=siteplan.file_url,
            file_type=siteplan.file_type,
            file_size=siteplan.file_size,
            status=siteplan.status,
            uploaded_at=siteplan.uploadedAt
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload siteplan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/siteplans", response_model=List[SiteplanListItem])
async def list_siteplans(
    status: Optional[str] = None,
    file_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: PrismaClient = Depends(get_db)
):
    """List all imported siteplans with optional filtering"""
    try:
        where_clause = {}
        
        if status:
            where_clause['status'] = status
        
        if file_type:
            where_clause['file_type'] = file_type
        
        siteplans = db.importedsiteplan.find_many(
            where=where_clause,
            order={'uploadedAt': 'desc'},
            take=limit,
            skip=offset
        )
        
        return [
            SiteplanListItem(
                id=sp.id,
                project_name=sp.project_name,
                file_type=sp.file_type,
                file_size=sp.file_size,
                status=sp.status,
                uploaded_at=sp.uploadedAt,
                processed_at=sp.processedAt,
                completed_at=sp.completedAt
            )
            for sp in siteplans
        ]
        
    except Exception as e:
        logger.error(f"Failed to list siteplans: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/siteplans/{siteplan_id}")
async def get_siteplan(
    siteplan_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Get detailed information about a specific siteplan"""
    try:
        siteplan = db.importedsiteplan.find_unique(where={'id': siteplan_id})
        
        if not siteplan:
            raise HTTPException(status_code=404, detail="Siteplan not found")
        
        return {
            'id': siteplan.id,
            'project_name': siteplan.project_name,
            'file_url': siteplan.file_url,
            'file_type': siteplan.file_type,
            'file_size': siteplan.file_size,
            'file_hash': siteplan.file_hash,
            'status': siteplan.status,
            'metadata': siteplan.metadata,
            'uploaded_by': siteplan.uploadedBy,
            'uploaded_at': siteplan.uploadedAt,
            'processed_at': siteplan.processedAt,
            'completed_at': siteplan.completedAt,
            'project_id': siteplan.projectId
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get siteplan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/siteplans/{siteplan_id}/status")
async def update_siteplan_status(
    siteplan_id: str,
    status_update: SiteplanStatusUpdate,
    db: PrismaClient = Depends(get_db)
):
    """Update siteplan processing status"""
    try:
        siteplan = db.importedsiteplan.find_unique(where={'id': siteplan_id})
        
        if not siteplan:
            raise HTTPException(status_code=404, detail="Siteplan not found")
        
        update_data = {'status': status_update.status}
        
        # Add timestamps based on status
        if status_update.status == 'RENDERING' and not siteplan.processedAt:
            update_data['processedAt'] = datetime.now()
        elif status_update.status == 'PUBLISHED' and not siteplan.completedAt:
            update_data['completedAt'] = datetime.now()
        
        updated_siteplan = db.importedsiteplan.update(
            where={'id': siteplan_id},
            data=update_data
        )
        
        logger.info(f"Siteplan status updated: {siteplan_id} -> {status_update.status}")
        
        return {
            'id': updated_siteplan.id,
            'project_name': updated_siteplan.project_name,
            'status': updated_siteplan.status,
            'updated_at': datetime.now()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update siteplan status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/siteplans/{siteplan_id}")
async def delete_siteplan(
    siteplan_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Delete a siteplan and its associated file"""
    try:
        siteplan = db.importedsiteplan.find_unique(where={'id': siteplan_id})
        
        if not siteplan:
            raise HTTPException(status_code=404, detail="Siteplan not found")
        
        # Delete file from filesystem
        if os.path.exists(siteplan.file_url):
            os.remove(siteplan.file_url)
            logger.info(f"Deleted file: {siteplan.file_url}")
        
        # Delete from database
        db.importedsiteplan.delete(where={'id': siteplan_id})
        
        logger.info(f"Siteplan deleted: {siteplan_id}")
        
        return {'message': f'Siteplan {siteplan_id} deleted successfully'}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete siteplan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/siteplans/{siteplan_id}/process")
async def trigger_vfx_processing(
    siteplan_id: str,
    db: PrismaClient = Depends(get_db)
):
    """
    Trigger VFX processing for a siteplan
    
    This endpoint initiates the VFX processing pipeline by connecting
    to the multipass_compositor module for visual enhancement.
    """
    try:
        siteplan = db.importedsiteplan.find_unique(where={'id': siteplan_id})
        
        if not siteplan:
            raise HTTPException(status_code=404, detail="Siteplan not found")
        
        if siteplan.status != 'READY_FOR_VFX':
            raise HTTPException(
                status_code=400,
                detail=f"Siteplan must be in READY_FOR_VFX status to process. Current status: {siteplan.status}"
            )
        
        # Update status to RENDERING
        updated_siteplan = db.importedsiteplan.update(
            where={'id': siteplan_id},
            data={
                'status': 'RENDERING',
                'processedAt': datetime.now()
            }
        )
        
        # TODO: Connect to core_modules.visual.multipass_compositor
        # This is where the actual VFX processing happens
        # The file will be processed through the multipass compositor
        # for effects like lens halation, cinematic grading, etc.
        
        logger.info(f"VFX processing triggered for siteplan {siteplan_id}")
        logger.info(f"TODO: Process file {siteplan.file_url} through multipass_compositor")
        
        # For now, simulate processing completion
        # In production, this would be handled by the VFX pipeline
        try:
            # Simulate VFX processing
            # TODO: Replace with actual multipass_compositor call
            # from core_modules.visual.multipass_compositor import process_siteplan
            # result = process_siteplan(siteplan.file_url, siteplan.metadata)
            
            # Mark as completed for demo
            db.importedsiteplan.update(
                where={'id': siteplan_id},
                data={
                    'status': 'PUBLISHED',
                    'completedAt': datetime.now()
                }
            )
            
        except Exception as e:
            # Mark as failed if processing fails
            db.importedsiteplan.update(
                where={'id': siteplan_id},
                data={'status': 'FAILED'}
            )
            logger.error(f"VFX processing failed for siteplan {siteplan_id}: {e}")
            raise HTTPException(status_code=500, detail="VFX processing failed")
        
        return {
            'message': 'VFX processing initiated',
            'siteplan_id': siteplan_id,
            'status': 'RENDERING',
            'file_url': siteplan.file_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger VFX processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/siteplans/{siteplan_id}/download")
async def download_siteplan(
    siteplan_id: str,
    db: PrismaClient = Depends(get_db)
):
    """Download a siteplan file"""
    try:
        siteplan = db.importedsiteplan.find_unique(where={'id': siteplan_id})
        
        if not siteplan:
            raise HTTPException(status_code=404, detail="Siteplan not found")
        
        if not os.path.exists(siteplan.file_url):
            raise HTTPException(status_code=404, detail="File not found on server")
        
        from fastapi.responses import FileResponse
        
        return FileResponse(
            siteplan.file_url,
            media_type='application/octet-stream',
            filename=f"{siteplan.project_name}_{siteplan.id}{os.path.splitext(siteplan.file_url)[1]}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to download siteplan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_import_stats(db: PrismaClient = Depends(get_db)):
    """Get statistics about imported siteplans"""
    try:
        # Count by status
        status_counts = {}
        for status in ['READY_FOR_VFX', 'RENDERING', 'PUBLISHED', 'FAILED']:
            count = db.importedsiteplan.count(where={'status': status})
            status_counts[status] = count
        
        # Count by file type
        file_type_counts = {}
        for file_type in ['IMAGE', '3D_MODEL', 'PDF', 'VIDEO']:
            count = db.importedsiteplan.count(where={'file_type': file_type})
            file_type_counts[file_type] = count
        
        # Total counts
        total_siteplans = db.importedsiteplan.count()
        total_size = db.importedsiteplan.aggregate(
            _sum={'fileSize': 'sum'}
        )['_sum']['fileSize'] or 0
        
        return {
            'total_siteplans': total_siteplans,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'status_counts': status_counts,
            'file_type_counts': file_type_counts,
            'recent_uploads': db.importedsiteplan.find_many(
                order={'uploadedAt': 'desc'},
                take=5
            )
        }
        
    except Exception as e:
        logger.error(f"Failed to get import stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
