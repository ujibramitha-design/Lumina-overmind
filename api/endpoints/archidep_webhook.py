"""
Archidep M2M Webhook Integration
================================
Webhook endpoints for receiving siteplan files from Archidep system
"""

import os
import shutil
import hashlib
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Header
from pydantic import BaseModel, Field
from prisma import Prisma

from core_modules.db_manager import prisma_manager


# Database dependency
async def get_db():
    db = await prisma_manager.get_db()
    return db


# Security
ARCHIDEP_SECRET_KEY = os.getenv("ARCHIDEP_SECRET_KEY", "default_secret_key")
ARCHIDEP_OUTPUT_DIR = os.getenv("ARCHIDEP_OUTPUT_DIR", "./output/archidep")
ARCHIDEP_PROCESSED_DIR = os.getenv("ARCHIDEP_PROCESSED_DIR", "./output/archidep/processed")


# Ensure directories exist
os.makedirs(ARCHIDEP_OUTPUT_DIR, exist_ok=True)
os.makedirs(ARCHIDEP_PROCESSED_DIR, exist_ok=True)


router = APIRouter(prefix="/api/webhooks/archidep", tags=["Archidep Webhooks"])


# Pydantic Models
class SiteplanReceive(BaseModel):
    """Model for receiving siteplan via JSON with file URL"""
    project_id: str = Field(..., description="Project ID")
    file_url: str = Field(..., description="URL to the siteplan file")
    file_type: str = Field(default="3d_model", description="File type (3d_model, siteplan, etc.)")
    file_name: str = Field(..., description="Original file name")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class SiteplanStatusUpdate(BaseModel):
    """Model for status update from Archidep"""
    project_id: str = Field(..., description="Project ID")
    file_id: str = Field(..., description="File ID from previous upload")
    status: str = Field(..., description="Status (processing, completed, failed)")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    processed_file_url: Optional[str] = Field(None, description="URL to processed file")


# Helper Functions
def verify_auth(x_archidep_secret: Optional[str] = Header(None)) -> bool:
    """Verify Archidep secret key"""
    if x_archidep_secret != ARCHIDEP_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid secret key")
    return True


def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def is_valid_file_type(file_name: str) -> bool:
    """Validate file type"""
    allowed_extensions = [".obj", ".fbx", ".gltf", ".glb", ".usd", ".usdz", ".zip", ".rar"]
    return any(file_name.lower().endswith(ext) for ext in allowed_extensions)


# API Endpoints
@router.post("/receive-siteplan")
async def receive_siteplan(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    file_type: str = Form(default="3d_model"),
    x_archidep_secret: Optional[str] = Header(None),
    db: Prisma = Depends(get_db)
):
    """
    Receive siteplan file via multipart upload
    """
    try:
        # Verify authentication
        verify_auth(x_archidep_secret)
        
        # Validate file type
        if not is_valid_file_type(file.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(ARCHIDEP_OUTPUT_DIR, safe_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Calculate file hash
        file_hash = calculate_file_hash(file_path)
        file_size = os.path.getsize(file_path)
        
        # Save to database
        siteplan_asset = await db.siteplanasset.create(
            {
                "project_name": project_id,
                "file_url": file_path,
                "file_type": file_type,
                "file_size": file_size,
                "file_hash": file_hash,
                "status": "READY_FOR_VFX",
                "metadata": {
                    "original_filename": file.filename,
                    "uploaded_at": datetime.now().isoformat(),
                    "source": "archidep_webhook"
                },
                "uploaded_by": "archidep_system",
                "uploaded_at": datetime.now()
            }
        )
        
        return {
            "status": "success",
            "message": "Siteplan file received successfully",
            "file_id": siteplan_asset.id,
            "file_path": file_path,
            "file_hash": file_hash,
            "file_size": file_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to receive siteplan: {str(e)}")


@router.post("/receive-siteplan-json")
async def receive_siteplan_json(
    data: SiteplanReceive,
    x_archidep_secret: Optional[str] = Header(None),
    db: Prisma = Depends(get_db)
):
    """
    Receive siteplan file via JSON with file URL
    """
    try:
        # Verify authentication
        verify_auth(x_archidep_secret)
        
        # Validate file type from URL
        if not is_valid_file_type(data.file_name):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{data.file_name}"
        file_path = os.path.join(ARCHIDEP_OUTPUT_DIR, safe_filename)
        
        # TODO: Download file from URL (implement with requests/httpx)
        # For now, just store the URL reference
        file_hash = hashlib.sha256(data.file_url.encode()).hexdigest()
        
        # Save to database
        siteplan_asset = await db.siteplanasset.create(
            {
                "project_name": data.project_id,
                "file_url": data.file_url,
                "file_type": data.file_type,
                "file_size": data.file_size,
                "file_hash": file_hash,
                "status": "READY_FOR_VFX",
                "metadata": {
                    "original_filename": data.file_name,
                    "uploaded_at": datetime.now().isoformat(),
                    "source": "archidep_webhook",
                    "download_url": data.file_url
                },
                "uploaded_by": "archidep_system",
                "uploaded_at": datetime.now()
            }
        )
        
        return {
            "status": "success",
            "message": "Siteplan file reference received successfully",
            "file_id": siteplan_asset.id,
            "file_url": data.file_url,
            "file_hash": file_hash
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to receive siteplan reference: {str(e)}")


@router.post("/status-update")
async def status_update(
    data: SiteplanStatusUpdate,
    x_archidep_secret: Optional[str] = Header(None),
    db: Prisma = Depends(get_db)
):
    """
    Receive status update from Archidep
    """
    try:
        # Verify authentication
        verify_auth(x_archidep_secret)
        
        # Find the siteplan asset
        siteplan_asset = await db.siteplanasset.find_first(
            where={"id": data.file_id}
        )
        
        if not siteplan_asset:
            raise HTTPException(status_code=404, detail="Siteplan asset not found")
        
        # Update status
        update_data = {
            "status": data.status.upper(),
            "processed_at": datetime.now()
        }
        
        if data.error_message:
            update_data["metadata"] = {
                **siteplan_asset.metadata,
                "error_message": data.error_message,
                "error_time": datetime.now().isoformat()
            }
        
        if data.processed_file_url:
            update_data["file_url"] = data.processed_file_url
            update_data["metadata"] = {
                **siteplan_asset.metadata,
                "processed_file_url": data.processed_file_url
            }
        
        updated_asset = await db.siteplanasset.update(
            where={"id": data.file_id},
            data=update_data
        )
        
        return {
            "status": "success",
            "message": "Status updated successfully",
            "file_id": updated_asset.id,
            "current_status": updated_asset.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for Archidep webhook"""
    return {
        "status": "healthy",
        "service": "archidep_webhook",
        "timestamp": datetime.now().isoformat(),
        "output_dir": ARCHIDEP_OUTPUT_DIR,
        "processed_dir": ARCHIDEP_PROCESSED_DIR
    }
