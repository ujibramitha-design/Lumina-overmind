"""
Visual API Endpoints
PDF generation, image processing, and visual design operations
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from datetime import datetime
import base64
from io import BytesIO

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Pydantic models
class PDFGenerationRequest(BaseModel):
    template_data: Dict[str, Any]
    output_filename: str
    template_type: str = "davinci"
    include_qr_code: bool = True
    use_puppeteer: bool = True

class ImageProcessingRequest(BaseModel):
    operations: List[Dict[str, Any]]
    preserve_metadata: bool = True

class ComfyUIRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    controlnet_image: Optional[str] = None
    controlnet_type: str = "mlsd"
    ic_light_image: Optional[str] = None
    supir_upscale: bool = False

# Dependency for database connection
async def get_db():
    """Get database connection"""
    try:
        from core_modules.db_manager_postgres import postgres_db_manager
        return postgres_db_manager
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@router.post("/generate-pdf")
async def generate_pdf(
    request: PDFGenerationRequest,
    db = Depends(get_db)
):
    """
    Generate PDF brochure using DaVinci layout
    """
    try:
        logger.info(f"Generating PDF: {request.output_filename}")
        
        # Submit task to Celery
        from tasks.visual_tasks import create_pdf_brochure
        task = create_pdf_brochure.s(
            template_data=request.template_data,
            output_filename=request.output_filename,
            template_type=request.template_type,
            include_qr_code=request.include_qr_code
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "output_filename": request.output_filename,
            "template_type": request.template_type,
            "message": "PDF generation task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-comfyui-image")
async def generate_comfyui_image(
    request: ComfyUIRequest,
    db = Depends(get_db)
):
    """
    Generate image using ComfyUI with ControlNet, IC-Light, SUPIR
    """
    try:
        logger.info(f"Generating ComfyUI image: {request.prompt[:50]}...")
        
        # Submit task to Celery
        from tasks.visual_tasks import generate_comfyui_image
        task = generate_comfyui_image.s(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            controlnet_image=request.controlnet_image,
            controlnet_type=request.controlnet_type,
            ic_light_image=request.ic_light_image,
            supir_upscale=request.supir_upscale
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "prompt": request.prompt,
            "controlnet_type": request.controlnet_type,
            "supir_upscale": request.supir_upscale,
            "message": "ComfyUI image generation task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"ComfyUI image generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-multipass-compositing")
async def process_multipass_compositing(
    base_image: UploadFile = File(...),
    db = Depends(get_db),
    output_filename: str = "composited_image.png",
    custom_blend_modes: Optional[Dict[str, str]] = None
):
    """
    Process multipass compositing with VFX effects
    """
    try:
        logger.info(f"Processing multipass compositing: {base_image.filename}")
        
        # Save uploaded file temporarily
        temp_path = f"temp/{base_image.filename}"
        os.makedirs("temp", exist_ok=True)
        
        with open(temp_path, "wb") as buffer:
            content = await base_image.read()
            buffer.write(content)
        
        # Submit task to Celery
        from tasks.visual_tasks import process_multipass_compositing
        task = process_multipass_compositing.s(
            base_image_path=temp_path,
            output_path=f"output/visual/{output_filename}",
            custom_blend_modes=custom_blend_modes or {}
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "input_file": base_image.filename,
            "output_filename": output_filename,
            "message": "Multipass compositing task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Multipass compositing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-cinematic-video")
async def generate_cinematic_video(
    prompt: str,
    duration: int = 10,
    style: str = "cinematic",
    db = Depends(get_db)
):
    """
    Generate cinematic video using Runway Gen-3 or Luma Dream Machine
    """
    try:
        logger.info(f"Generating cinematic video: {prompt[:50]}...")
        
        # Submit task to Celery
        from tasks.visual_tasks import generate_cinematic_video
        task = generate_cinematic_video.s(
            prompt=prompt,
            duration=duration,
            style=style
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "prompt": prompt,
            "duration": duration,
            "style": style,
            "message": "Cinematic video generation task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Cinematic video generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-image")
async def process_image(
    request: ImageProcessingRequest,
    image: UploadFile = File(...),
    db = Depends(get_db)
):
    """
    Process image with post-processing operations
    """
    try:
        logger.info(f"Processing image: {image.filename}")
        
        # Save uploaded file temporarily
        temp_path = f"temp/{image.filename}"
        os.makedirs("temp", exist_ok=True)
        
        with open(temp_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # Generate output filename
        output_filename = f"processed_{image.filename}"
        output_path = f"output/visual/{output_filename}"
        
        # Submit task to Celery
        from tasks.visual_tasks import process_image_post_processing
        task = process_image_post_processing.s(
            image_path=temp_path,
            output_path=output_path,
            operations=request.operations,
            preserve_metadata=request.preserve_metadata
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "input_file": image.filename,
            "output_filename": output_filename,
            "operations_count": len(request.operations),
            "message": "Image processing task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_pdf_templates():
    """
    Get available PDF templates
    """
    try:
        from core_modules.visual.pdf_creator import pdf_creator
        
        templates = pdf_creator.list_templates()
        
        return {
            "success": True,
            "templates": templates,
            "total": len(templates)
        }
        
    except Exception as e:
        logger.error(f"Failed to get PDF templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pdfs")
async def get_generated_pdfs():
    """
    Get list of generated PDFs
    """
    try:
        from core_modules.visual.pdf_creator import pdf_creator
        
        pdfs = pdf_creator.list_pdfs()
        
        return {
            "success": True,
            "pdfs": pdfs,
            "total": len(pdfs)
        }
        
    except Exception as e:
        logger.error(f"Failed to get PDFs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pdf/{filename}")
async def get_pdf_info(filename: str):
    """
    Get PDF file information
    """
    try:
        from core_modules.visual.pdf_creator import pdf_creator
        
        pdf_path = f"output/pdfs/{filename}"
        info = await pdf_creator.get_pdf_info(pdf_path)
        
        return {
            "success": True,
            "info": info
        }
        
    except Exception as e:
        logger.error(f"Failed to get PDF info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comfyui-status")
async def get_comfyui_status():
    """
    Check ComfyUI server status
    """
    try:
        from core_modules.visual.comfyui_orchestrator import ComfyUIOrchestrator
        
        orchestrator = ComfyUIOrchestrator()
        status = await orchestrator.check_server_status()
        
        return {
            "success": True,
            "status": status,
            "server_url": orchestrator.server_url
        }
        
    except Exception as e:
        logger.error(f"Failed to check ComfyUI status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/blend-modes")
async def get_blend_modes():
    """
    Get available blend modes for multipass compositing
    """
    try:
        from core_modules.visual.multipass_compositor import MultipassCompositor
        
        compositor = MultipassCompositor()
        blend_modes = compositor.blend_modes
        
        return {
            "success": True,
            "blend_modes": list(blend_modes.keys()),
            "total": len(blend_modes)
        }
        
    except Exception as e:
        logger.error(f"Failed to get blend modes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/controlnet-types")
async def get_controlnet_types():
    """
    Get available ControlNet types
    """
    try:
        from core_modules.visual.comfyui_orchestrator import ComfyUIOrchestrator
        
        orchestrator = ComfyUIOrchestrator()
        controlnet_types = orchestrator.controlnet_types
        
        return {
            "success": True,
            "controlnet_types": list(controlnet_types.keys()),
            "total": len(controlnet_types)
        }
        
    except Exception as e:
        logger.error(f"Failed to get ControlNet types: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}")
async def get_visual_task_status(task_id: str):
    """
    Get visual task status by ID
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

@router.get("/stats")
async def get_visual_stats(db = Depends(get_db)):
    """
    Get visual processing statistics
    """
    try:
        # Get task statistics
        from tasks.celery_app import TaskMonitor
        task_stats = TaskMonitor.get_task_stats()
        
        # Get PDF statistics
        from core_modules.visual.pdf_creator import pdf_creator
        pdf_count = len(pdf_creator.list_pdfs())
        
        return {
            "success": True,
            "task_statistics": task_stats,
            "pdf_count": pdf_count,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get visual stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
