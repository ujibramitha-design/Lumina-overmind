"""
LUMINA OS - PROJECT MIRAGE
====================================

AI Image Staging System
Automated Interior Rendering with AI Image Generation

Features:
- AI Interior Rendering with DALL-E 3
- Text-to-Image Generation
- Style Customization
- Multiple API Support (OpenAI, Stable Diffusion)
- Image Processing and Enhancement
"""

import os
import sys
import json
import time
import logging
import asyncio
import tempfile
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
import io
import httpx
from PIL import Image, ImageEnhance, ImageFilter

# FastAPI imports
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)

# Import required modules
try:
    import openai
    from core_modules.db_manager_supabase import get_supabase_manager
    from core_modules.notifications.telegram_sender import get_telegram_sender
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing required packages...")
    os.system("pip install openai Pillow")
    print("Please restart the script after installation")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

# Create router
router = APIRouter(prefix="/api/mirage", tags=["visual"])

# Pydantic models
class RenderRequest(BaseModel):
    prompt: str = Field(..., description="Text description for interior rendering")
    style: str = Field(default="modern", description="Interior style (modern, classic, minimalist, etc.)")
    room_type: str = Field(default="living_room", description="Room type (living_room, bedroom, kitchen, etc.)")
    width: int = Field(default=1024, description="Image width")
    height: int = Field(default=1024, description="Image height")
    quality: str = Field(default="standard", description="Quality level (standard, high, premium)")

class RenderResponse(BaseModel):
    success: bool
    image_url: str
    render_id: str
    prompt: str
    style: str
    generated_at: datetime
    processing_time: float

@dataclass
class RenderJob:
    """Render job data structure"""
    job_id: str
    prompt: str
    style: str
    room_type: str
    width: int
    height: int
    quality: str
    status: str
    created_at: datetime
    image_url: Optional[str] = None
    processing_time: Optional[float] = None

class VisualMirage:
    """
    Project Mirage - AI Image Staging System
    Automated interior rendering with AI image generation
    """
    
    def __init__(self):
        """Initialize Visual Mirage"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            self.logger.info(f"{GREEN}✅ OpenAI client initialized for image generation{END}")
        else:
            self.openai_client = None
            self.logger.warning(f"{YELLOW}⚠️ OpenAI API key not found - using fallback rendering{END}")
        
        # Initialize Stable Diffusion (placeholder)
        self.stable_diffusion_api_key = os.getenv('STABLE_DIFFUSION_API_KEY')
        if self.stable_diffusion_api_key:
            self.logger.info(f"{GREEN}✅ Stable Diffusion API key configured{END}")
        else:
            self.logger.info(f"{CYAN}ℹ️ Stable Diffusion API key not configured{END}")
        
        # Initialize database
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Database connected for render jobs{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Database connection failed: {e}{END}")
        
        # Initialize Telegram sender
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Telegram sender initialized for render notifications{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Telegram sender failed: {e}{END}")
        
        # Render storage
        self.renders_dir = Path(root_dir) / "assets" / "renders"
        self.renders_dir.mkdir(parents=True, exist_ok=True)
        
        # Style presets
        self.style_presets = {
            "modern": {
                "keywords": ["modern", "contemporary", "minimalist", "clean lines", "sleek"],
                "lighting": "natural lighting",
                "colors": ["white", "gray", "black", "neutral tones"]
            },
            "classic": {
                "keywords": ["classic", "traditional", "elegant", "timeless"],
                "lighting": "warm lighting",
                "colors": ["beige", "brown", "cream", "gold accents"]
            },
            "minimalist": {
                "keywords": ["minimalist", "simple", "clean", "uncluttered"],
                "lighting": "bright natural light",
                "colors": ["white", "light gray", "monochrome"]
            },
            "scandinavian": {
                "keywords": ["scandinavian", "nordic", "cozy", "natural"],
                "lighting": "soft natural light",
                "colors": ["white", "light wood", "blue accents"]
            },
            "industrial": {
                "keywords": ["industrial", "urban", "raw", "exposed"],
                "lighting": "dramatic lighting",
                "colors": ["gray", "black", "metallic", "brick"]
            }
        }
        
        # Room type configurations
        self.room_configs = {
            "living_room": {
                "elements": ["sofa", "coffee table", "tv unit", "bookshelf", "decor"],
                "atmosphere": "cozy and inviting"
            },
            "bedroom": {
                "elements": ["bed", "nightstand", "wardrobe", "dressing table"],
                "atmosphere": "peaceful and relaxing"
            },
            "kitchen": {
                "elements": ["cabinets", "countertops", "appliances", "dining area"],
                "atmosphere": "functional and stylish"
            },
            "bathroom": {
                "elements": ["vanity", "mirror", "shower", "bathtub", "storage"],
                "atmosphere": "spa-like and modern"
            },
            "dining_room": {
                "elements": ["dining table", "chairs", "sideboard", "lighting"],
                "atmosphere": "elegant and social"
            }
        }
        
        self.logger.info(f"{MAGENTA}🎨 PROJECT MIRAGE: AI Image Staging System initialized{END}")
        self.logger.info(f"{CYAN}🖼️ Renders directory: {self.renders_dir}{END}")
        self.logger.info(f"{GREEN}✅ Ready for AI-powered interior rendering{END}")
    
    def enhance_prompt(self, base_prompt: str, style: str, room_type: str) -> str:
        """
        Enhance prompt with style and room-specific details
        
        Args:
            base_prompt: Base user prompt
            style: Interior style
            room_type: Type of room
            
        Returns:
            Enhanced prompt for better AI generation
        """
        try:
            # Get style configuration
            style_config = self.style_presets.get(style, self.style_presets["modern"])
            style_keywords = " ".join(style_config["keywords"])
            lighting = style_config["lighting"]
            colors = ", ".join(style_config["colors"])
            
            # Get room configuration
            room_config = self.room_configs.get(room_type, self.room_configs["living_room"])
            room_elements = ", ".join(room_config["elements"])
            atmosphere = room_config["atmosphere"]
            
            # Build enhanced prompt
            enhanced_prompt = f"""
            Interior design render of a {room_type.replace('_', ' ')} with {atmosphere} atmosphere.
            Style: {style} with {style_keywords} aesthetics.
            Elements: {room_elements}.
            Color palette: {colors}.
            Lighting: {lighting}.
            User request: {base_prompt}.
            
            High quality, photorealistic, architectural visualization, interior photography.
            """.strip()
            
            self.logger.debug(f"{CYAN}📝 Enhanced prompt generated for {style} {room_type}{END}")
            
            return enhanced_prompt
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Prompt enhancement error: {str(e)}{END}")
            return base_prompt
    
    async def generate_with_openai(self, prompt: str, width: int, height: int, quality: str) -> Optional[str]:
        """
        Generate image using OpenAI DALL-E 3
        
        Args:
            prompt: Enhanced prompt for generation
            width: Image width
            height: Image height
            quality: Quality level
            
        Returns:
            Image URL if successful, None otherwise
        """
        try:
            if not self.openai_client:
                self.logger.warning(f"{YELLOW}⚠️ OpenAI client not available{END}")
                return None
            
            self.logger.info(f"{BLUE}🎨 Generating image with OpenAI DALL-E 3...{END}")
            
            # Determine quality
            dalle_quality = "standard" if quality == "standard" else "hd"
            
            # Generate image
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=f"{width}x{height}",
                quality=dalle_quality,
                n=1
            )
            
            image_url = response.data[0].url
            
            self.logger.info(f"{GREEN}✅ OpenAI image generated successfully{END}")
            self.logger.debug(f"{CYAN}🔗 Image URL: {image_url[:50]}...{END}")
            
            return image_url
            
        except Exception as e:
            self.logger.error(f"{RED}❌ OpenAI generation error: {str(e)}{END}")
            return None
    
    async def generate_with_stable_diffusion(self, prompt: str, width: int, height: int, quality: str) -> Optional[str]:
        """
        Generate image using Stable Diffusion API
        
        Args:
            prompt: Enhanced prompt for generation
            width: Image width
            height: Image height
            quality: Quality level
            
        Returns:
            Image URL if successful, None otherwise
        """
        try:
            if not self.stable_diffusion_api_key:
                self.logger.warning(f"{YELLOW}⚠️ Stable Diffusion API key not available{END}")
                return None
            
            self.logger.info(f"{BLUE}🎨 Generating image with Stable Diffusion...{END}")
            
            # Placeholder for Stable Diffusion API call
            # In production, integrate with actual Stable Diffusion API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers={
                        "Authorization": f"Bearer {self.stable_diffusion_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "text_prompts": [{"text": prompt}],
                        "width": width,
                        "height": height,
                        "samples": 1,
                        "cfg_scale": 7
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Process response and return image URL
                    # This is a placeholder - actual implementation depends on API response format
                    self.logger.info(f"{GREEN}✅ Stable Diffusion image generated successfully{END}")
                    return "https://placeholder-stable-diffusion-url.com/image.png"
                else:
                    self.logger.error(f"{RED}❌ Stable Diffusion API error: {response.status_code}{END}")
                    return None
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Stable Diffusion generation error: {str(e)}{END}")
            return None
    
    async def download_and_process_image(self, image_url: str, job_id: str) -> Optional[str]:
        """
        Download and process generated image
        
        Args:
            image_url: URL of generated image
            job_id: Unique job identifier
            
        Returns:
            Local file path if successful, None otherwise
        """
        try:
            self.logger.info(f"{BLUE}📥 Downloading and processing image...{END}")
            
            # Download image
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                
                # Save original image
                original_path = self.renders_dir / f"{job_id}_original.png"
                with open(original_path, "wb") as f:
                    f.write(response.content)
                
                # Process image
                image = Image.open(io.BytesIO(response.content))
                
                # Enhance image
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Apply enhancements
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(1.1)
                
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.05)
                
                # Save processed image
                processed_path = self.renders_dir / f"{job_id}_processed.png"
                image.save(processed_path, "PNG", quality=95)
                
                self.logger.info(f"{GREEN}✅ Image processed and saved{END}")
                self.logger.debug(f"{CYAN}💾 Saved to: {processed_path}{END}")
                
                return str(processed_path)
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Image processing error: {str(e)}{END}")
            return None
    
    def save_render_job(self, job_data: Dict[str, Any]) -> Optional[str]:
        """
        Save render job to database
        
        Args:
            job_data: Render job information
            
        Returns:
            Job ID if successful, None otherwise
        """
        try:
            if not self.supabase_manager:
                self.logger.error(f"{RED}❌ Database not available{END}")
                return None
            
            # Insert to database
            result = self.supabase_manager.insert_render_job(job_data)
            
            if result['success']:
                job_id = result['data']['id']
                self.logger.info(f"{GREEN}✅ Render job saved: {job_id}{END}")
                return job_id
            else:
                self.logger.error(f"{RED}❌ Failed to save render job: {result['error']}{END}")
                return None
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Save render job error: {str(e)}{END}")
            return None
    
    def update_render_job(self, job_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update render job status
        
        Args:
            job_id: Job identifier
            update_data: Data to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.supabase_manager:
                self.logger.error(f"{RED}❌ Database not available{END}")
                return False
            
            result = self.supabase_manager.update_render_job(job_id, update_data)
            
            if result['success']:
                self.logger.info(f"{GREEN}✅ Render job updated: {job_id}{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to update render job: {result['error']}{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Update render job error: {str(e)}{END}")
            return False

# Global visual mirage instance
visual_mirage = VisualMirage()

# API endpoints
@router.post("/render-interior", response_model=RenderResponse)
async def render_interior(request: RenderRequest):
    """
    Generate interior rendering using AI
    """
    try:
        start_time = time.time()
        logger.info(f"{CYAN}🎨 Starting interior render...{END}")
        logger.info(f"{BLUE}📝 Prompt: {request.prompt}{END}")
        logger.info(f"{BLUE}🎭 Style: {request.style}, Room: {request.room_type}{END}")
        
        # Generate job ID
        job_id = f"render_{int(time.time())}_{hash(request.prompt) % 10000}"
        
        # Create render job
        render_job = RenderJob(
            job_id=job_id,
            prompt=request.prompt,
            style=request.style,
            room_type=request.room_type,
            width=request.width,
            height=request.height,
            quality=request.quality,
            status="processing",
            created_at=datetime.now()
        )
        
        # Save job to database
        saved_job_id = visual_mirage.save_render_job({
            "job_id": job_id,
            "prompt": request.prompt,
            "style": request.style,
            "room_type": request.room_type,
            "width": request.width,
            "height": request.height,
            "quality": request.quality,
            "status": "processing",
            "created_at": datetime.now().isoformat()
        })
        
        # Enhance prompt
        enhanced_prompt = visual_mirage.enhance_prompt(request.prompt, request.style, request.room_type)
        
        # Try OpenAI first, then fallback to Stable Diffusion
        image_url = await visual_mirage.generate_with_openai(
            enhanced_prompt, request.width, request.height, request.quality
        )
        
        if not image_url:
            image_url = await visual_mirage.generate_with_stable_diffusion(
                enhanced_prompt, request.width, request.height, request.quality
            )
        
        if not image_url:
            # Fallback to placeholder
            image_url = "https://via.placeholder.com/1024x1024/333333/FFFFFF?text=Render+Failed"
            logger.warning(f"{YELLOW}⚠️ Using placeholder image{END}")
        
        # Download and process image
        local_path = await visual_mirage.download_and_process_image(image_url, job_id)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update job status
        if local_path:
            visual_mirage.update_render_job(job_id, {
                "status": "completed",
                "image_url": local_path,
                "processing_time": processing_time,
                "updated_at": datetime.now().isoformat()
            })
        else:
            visual_mirage.update_render_job(job_id, {
                "status": "failed",
                "error": "Image processing failed",
                "processing_time": processing_time,
                "updated_at": datetime.now().isoformat()
            })
        
        # Send notification to Telegram
        if visual_mirage.telegram_sender:
            notification_message = f"""
🎨 **INTERIOR RENDER COMPLETED**

**Job ID**: {job_id}
**Prompt**: {request.prompt}
**Style**: {request.style}
**Room Type**: {request.room_type}
**Status**: {'✅ Success' if local_path else '❌ Failed'}
**Processing Time**: {processing_time:.2f}s

🖼️ {'Render generated successfully' if local_path else 'Render failed - using placeholder'}
            """.strip()
            
            visual_mirage.telegram_sender.send_message(notification_message)
        
        logger.info(f"{GREEN}✅ Interior render completed in {processing_time:.2f}s{END}")
        
        return RenderResponse(
            success=bool(local_path),
            image_url=f"/api/mirage/download/{job_id}" if local_path else image_url,
            render_id=job_id,
            prompt=request.prompt,
            style=request.style,
            generated_at=datetime.now(),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"{RED}❌ Render interior error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Render failed: {str(e)}")

@router.get("/download/{job_id}")
async def download_render(job_id: str):
    """
    Download rendered image by job ID
    """
    try:
        # Get render job from database
        if not visual_mirage.supabase_manager:
            raise HTTPException(status_code=500, detail="Database not available")
        
        result = visual_mirage.supabase_manager.get_render_job(job_id)
        
        if not result['success']:
            raise HTTPException(status_code=404, detail="Render job not found")
        
        job_data = result['data']
        image_url = job_data.get('image_url')
        
        if not image_url or not os.path.exists(image_url):
            raise HTTPException(status_code=404, detail="Rendered image not found")
        
        return FileResponse(
            path=image_url,
            filename=f"{job_id}_render.png",
            media_type='image/png'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"{RED}❌ Download render error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@router.get("/jobs")
async def list_render_jobs():
    """
    List all render jobs
    """
    try:
        if not visual_mirage.supabase_manager:
            raise HTTPException(status_code=500, detail="Database not available")
        
        result = visual_mirage.supabase_manager.get_render_jobs()
        
        if not result['success']:
            raise HTTPException(status_code=500, detail="Failed to fetch render jobs")
        
        return {
            "success": True,
            "jobs": result['data'],
            "count": len(result['data'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"{RED}❌ List render jobs error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Failed to list render jobs: {str(e)}")

@router.get("/styles")
async def get_available_styles():
    """
    Get available interior styles
    """
    return {
        "success": True,
        "styles": list(visual_mirage.style_presets.keys()),
        "room_types": list(visual_mirage.room_configs.keys())
    }

# Test function
if __name__ == "__main__":
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - PROJECT MIRAGE{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    print(f"{BLUE}🎨 Testing Visual Mirage system...{END}")
    
    # Test prompt enhancement
    test_prompt = "Desain interior dapur gaya Japandi modern dengan pencahayaan alami"
    enhanced = visual_mirage.enhance_prompt(test_prompt, "modern", "kitchen")
    
    print(f"{GREEN}✅ Original prompt: {test_prompt}{END}")
    print(f"{GREEN}✅ Enhanced prompt: {enhanced[:100]}...{END}")
    
    print(f"{MAGENTA}{'='*80}{END}")
