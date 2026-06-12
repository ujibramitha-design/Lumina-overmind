"""
MACHINE-TO-MACHINE WEBHOOKS - Archidep Integration
Handles automated siteplan uploads from external systems
"""

import logging
import os
import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prisma import Client as PrismaClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks", tags=["M2M Webhooks"])

# Get Archidep secret key from environment
ARCHIDEP_SECRET_KEY = os.getenv("ARCHIDEP_SECRET_KEY")

# Pydantic models
class WebhookResponse(BaseModel):
    success: bool
    message: str
    siteplan_id: Optional[str] = None
    status: str

class SiteplanWebhookData(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    file_url: str = Field(..., description="URL to the siteplan file")
    file_type: str = Field(default="IMAGE", description="Type of file (IMAGE, 3D_MODEL, PDF, VIDEO)")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    project_id: Optional[str] = Field(None, description="Associated project ID")

# Database dependency
def get_db():
    db = PrismaClient()
    return db

def verify_api_key(api_key: str) -> bool:
    """Verify the API key against the secret"""
    if not ARCHIDEP_SECRET_KEY:
        logger.error("ARCHIDEP_SECRET_KEY not configured")
        return False
    
    # Constant-time comparison to prevent timing attacks
    return api_key == ARCHIDEP_SECRET_KEY

def calculate_file_hash_from_url(file_url: str) -> Optional[str]:
    """Calculate hash from file URL (fallback if direct file not available)"""
    return hashlib.sha256(file_url.encode()).hexdigest()

async def download_file_from_url(file_url: str) -> tuple[bytes, str, int]:
    """Download file from URL and return content, filename, and size"""
    try:
        import httpx
        import os.path
        
        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            response.raise_for_status()
            
            # Extract filename from URL or use default
            filename = os.path.basename(file_url.split('?')[0]) or f"siteplan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dat"
            
            file_size = len(response.content)
            file_hash = hashlib.sha256(response.content).hexdigest()
            
            return response.content, filename, file_size
            
    except Exception as e:
        logger.error(f"Failed to download file from URL {file_url}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to download file: {str(e)}")

@router.post("/archidep/receive-siteplan")
async def receive_siteplan_webhook(
    request: Request,
    x_api_key: str = Header(None, alias="X-API-KEY"),
    db: PrismaClient = Depends(get_db)
):
    """
    Machine-to-Machine webhook for receiving siteplan files from Archidep
    
    This endpoint allows Archidep system to automatically send siteplan files
    to Lumina OS for VFX processing without manual intervention.
    
    Security: Requires X-API-KEY header matching ARCHIDEP_SECRET_KEY
    """
    try:
        # Verify API key
        if not verify_api_key(x_api_key):
            logger.warning(f"Unauthorized webhook attempt from {request.client.host}")
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Invalid API key"
            )
        
        # Parse request based on content type
        content_type = request.headers.get("content-type", "")
        
        if content_type.startswith("multipart/form-data"):
            # Handle file upload
            return await handle_file_upload_webhook(request, db)
        else:
            # Handle JSON webhook
            return await handle_json_webhook(request, db)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_file_upload_webhook(request: Request, db: PrismaClient):
    """Handle multipart file upload webhook"""
    try:
        # Parse form data
        form = await request.form()
        files = await request.files()
        
        # Extract required fields
        project_name = form.get("project_name")
        if not project_name:
            raise HTTPException(status_code=400, detail="project_name is required")
        
        # Handle file upload
        if "file" not in files:
            raise HTTPException(status_code=400, detail="file is required")
        
        file = files["file"]
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="Invalid file")
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Calculate file hash
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Determine file type
        file_type = get_file_type_from_filename(file.filename)
        
        # Parse metadata
        metadata = {}
        if "metadata" in form:
            try:
                metadata = json.loads(form["metadata"])
            except json.JSONDecodeError:
                logger.warning("Invalid metadata JSON in webhook")
        
        # Save to database
        siteplan = db.importedsiteplan.create({
            'project_name': project_name,
            'file_url': f"webhook_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}",
            'file_type': file_type,
            'file_size': file_size,
            'file_hash': file_hash,
            'status': 'READY_FOR_VFX',
            'metadata': metadata,
            'uploaded_by': 'archidep_webhook'
        })
        
        logger.info(f"Siteplan received via webhook upload: {project_name} ({file_type})")
        
        # TODO: Trigger VFX processing automatically
        # from core_modules.visual.multipass_compositor import process_siteplan_webhook
        # process_siteplan_webhook(siteplan.id, file_content, metadata)
        
        return WebhookResponse(
            success=True,
            message="Siteplan uploaded successfully via webhook",
            siteplan_id=siteplan.id,
            status="READY_FOR_VFX"
        )
        
    except Exception as e:
        logger.error(f"File upload webhook failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_json_webhook(request: Request, db: PrismaClient):
    """Handle JSON webhook with file URL"""
    try:
        # Parse JSON body
        body = await request.json()
        
        # Validate required fields
        if not body.get("project_name"):
            raise HTTPException(status_code=400, detail="project_name is required")
        
        if not body.get("file_url"):
            raise HTTPException(status_code=400, detail="file_url is required")
        
        # Create webhook data model
        webhook_data = SiteplanWebhookData(**body)
        
        # Download file from URL
        file_content, filename, file_size = await download_file_from_url(webhook_data.file_url)
        
        # Calculate file hash
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Save file locally (optional - for backup)
        upload_dir = "uploads/webhook_siteplans"
        os.makedirs(upload_dir, exist_ok=True)
        
        local_file_path = os.path.join(upload_dir, f"webhook_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        
        with open(local_file_path, "wb") as f:
            f.write(file_content)
        
        # Save to database
        siteplan = db.importedsiteplan.create({
            'project_name': webhook_data.project_name,
            'file_url': webhook_data.file_url,
            'file_type': webhook_data.file_type,
            'file_size': webhook_data.file_size or file_size,
            'file_hash': file_hash,
            'status': 'READY_FOR_VFX',
            'metadata': webhook_data.metadata,
            'projectId': webhook_data.project_id,
            'uploaded_by': 'archidep_webhook'
        })
        
        logger.info(f"Siteplan received via webhook URL: {webhook_data.project_name} ({webhook_data.file_type})")
        
        # TODO: Trigger VFX processing automatically
        # from core_modules.visual.multipass_compositor import process_siteplan_webhook
        # process_siteplan_webhook(siteplan.id, file_content, webhook_data.metadata)
        
        return WebhookResponse(
            success=True,
            message="Siteplan received successfully via webhook URL",
            siteplan_id=siteplan.id,
            status="READY_FOR_VFX"
        )
        
    except Exception as e:
        logger.error(f"JSON webhook failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_file_type_from_filename(filename: str) -> str:
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

@router.post("/archidep/status-update")
async def archidep_status_update(
    request: Request,
    x_api_key: str = Header(None, alias="X-API-KEY"),
    db: PrismaClient = Depends(get_db)
):
    """
    Webhook for Archidep to update processing status
    
    Allows Archidep to receive status updates about VFX processing
    """
    try:
        # Verify API key
        if not verify_api_key(x_api_key):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        body = await request.json()
        
        siteplan_id = body.get("siteplan_id")
        status = body.get("status")
        
        if not siteplan_id or not status:
            raise HTTPException(status_code=400, detail="siteplan_id and status are required")
        
        # Validate status
        valid_statuses = ["READY_FOR_VFX", "RENDERING", "PUBLISHED", "FAILED"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Update siteplan status
        update_data = {'status': status}
        
        if status == 'RENDERING':
            update_data['processedAt'] = datetime.now()
        elif status == 'PUBLISHED':
            update_data['completedAt'] = datetime.now()
        
        siteplan = db.importedsiteplan.update(
            where={'id': siteplan_id},
            data=update_data
        )
        
        logger.info(f"Siteplan status updated via webhook: {siteplan_id} -> {status}")
        
        return {
            'success': True,
            'message': f'Status updated to {status}',
            'siteplan_id': siteplan_id,
            'updated_at': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status update webhook failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/archidep/webhook-info")
async def webhook_info():
    """
    Get webhook configuration information
    """
    try:
        return {
            'webhook_url': '/api/webhooks/archidep/receive-siteplan',
            'method': 'POST',
            'authentication': 'X-API-KEY header required',
            'supported_formats': [
                'multipart/form-data (file upload)',
                'application/json (file URL)'
            ],
            'required_fields': {
                'file_upload': ['file', 'project_name'],
                'json_webhook': ['project_name', 'file_url']
            },
            'optional_fields': [
                'file_type', 'file_size', 'metadata', 'project_id'
            ],
            'status_webhook': '/api/webhooks/archidep/status-update',
            'example_payload': {
                'project_name': 'Luxury Villa Project',
                'file_url': 'https://archidep.example.com/siteplans/luxury-villa.obj',
                'file_type': '3D_MODEL',
                'metadata': {
                    'archidep_version': '2.1.0',
                    'render_quality': 'ultra',
                    'dimensions': {'width': 1920, 'height': 1080}
                }
            },
            'security_note': 'Always verify X-API-KEY header matches ARCHIDEP_SECRET_KEY'
        }
        
    except Exception as e:
        logger.error(f"Failed to get webhook info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-webhook")
async def test_webhook(
    project_name: str = Form("Test Project"),
    test_mode: str = Form("json")
):
    """
    Test webhook endpoint for development and testing
    """
    try:
        if test_mode == "json":
            # Simulate JSON webhook
            test_data = {
                'project_name': project_name,
                'file_url': 'https://example.com/test-siteplan.obj',
                'file_type': '3D_MODEL',
                'metadata': {'test': True, 'mode': 'json'}
            }
            
            return {
                'success': True,
                'message': 'Test webhook data prepared',
                'test_data': test_data,
                'usage': 'Send this data to /api/webhooks/archidep/receive-siteplan with X-API-KEY header'
            }
        else:
            # Simulate file upload info
            return {
                'success': True,
                'message': 'Test webhook prepared',
                'usage': 'Send multipart form data to /api/webhooks/archidep/receive-siteplan with X-API-KEY header',
                'required_fields': ['file', 'project_name'],
                'example_curl': '''curl -X POST http://localhost:8000/api/webhooks/archidep/receive-siteplan \\
  -H "X-API-KEY: your-secret-key" \\
  -F "project_name=Test Project" \\
  -F "file=@/path/to/your/siteplan.obj"'''
            }
            
    except Exception as e:
        logger.error(f"Test webhook failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def webhook_health():
    """
    Health check for webhook system
    """
    try:
        return {
            'status': 'healthy',
            'webhook_system': 'operational',
            'archidep_secret_configured': bool(ARCHIDEP_SECRET_KEY),
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'receive_siteplan': '/api/webhooks/archidep/receive-siteplan',
                'status_update': '/api/webhooks/archidep/status-update',
                'webhook_info': '/api/webhooks/archidep/webhook-info',
                'test_webhook': '/api/webhooks/test-webhook'
            }
        }
        
    except Exception as e:
        logger.error(f"Webhook health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
