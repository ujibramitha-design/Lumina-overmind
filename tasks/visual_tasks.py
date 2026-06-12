"""
LUMINA OS - VISUAL TASKS
==========================

Async visual processing tasks for ComfyUI, video generation,
PDF creation, and image processing.

Features:
- ComfyUI image generation with ControlNet, IC-Light, SUPIR
- Video processing with Runway Gen-3 and Luma Dream Machine
- PDF creation with Puppeteer/Playwright
- Image post-processing with OpenCV
- Multipass compositing and VFX
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Import Celery app
from tasks.celery_app import celery_app, visual_task
from core_modules.visual.multipass_compositor import MultipassCompositor
from core_modules.visual.cinematic_video import CinematicVideoGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@visual_task
def generate_comfyui_image(
    self,
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    steps: int = 20,
    cfg_scale: float = 7.0,
    seed: Optional[int] = None,
    controlnet_image: Optional[str] = None,
    controlnet_type: str = "mlsd",
    ic_light_image: Optional[str] = None,
    supir_upscale: bool = False,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate image using ComfyUI with advanced features
    
    Args:
        prompt: Main prompt for image generation
        negative_prompt: Negative prompt
        width: Image width
        height: Image height
        steps: Number of inference steps
        cfg_scale: CFG scale
        seed: Random seed
        controlnet_image: Base64 encoded ControlNet input image
        controlnet_type: Type of ControlNet (mlsd, canny, depth, etc.)
        ic_light_image: Base64 encoded IC-Light relighting image
        supir_upscale: Whether to use SUPIR upscaling
        output_path: Path to save generated image
    
    Returns:
        Dictionary containing generation results
    """
    
    try:
        logger.info(f"Starting ComfyUI image generation: {prompt[:100]}...")
        
        # Initialize ComfyUI orchestrator
        from core_modules.visual.comfyui_orchestrator import ComfyUIOrchestrator
        orchestrator = ComfyUIOrchestrator()
        
        # Build workflow payload
        workflow = orchestrator.build_workflow(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            cfg_scale=cfg_scale,
            seed=seed,
            controlnet_image=controlnet_image,
            controlnet_type=controlnet_type,
            ic_light_image=ic_light_image,
            supir_upscale=supir_upscale
        )
        
        # Submit workflow to ComfyUI
        result = orchestrator.submit_workflow(workflow)
        
        if result['success']:
            # Save image if output path provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Decode base64 image
                image_data = base64.b64decode(result['image'])
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                result['output_path'] = output_path
                logger.info(f"Image saved to: {output_path}")
            
            logger.info(f"ComfyUI generation completed successfully")
            return result
        else:
            raise Exception(f"ComfyUI generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"ComfyUI image generation failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@visual_task
def process_multipass_compositing(
    self,
    base_image_path: str,
    output_path: str,
    apply_halation: bool = True,
    inject_exif: bool = True,
    custom_blend_modes: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Process multipass compositing with VFX effects
    
    Args:
        base_image_path: Path to base image
        output_path: Output path for composited image
        apply_halation: Whether to apply lens halation effect
        inject_exif: Whether to inject DSLR EXIF data
        custom_blend_modes: Custom blend modes for layers
    
    Returns:
        Dictionary containing compositing results
    """
    
    try:
        logger.info(f"Starting multipass compositing for: {base_image_path}")
        
        # Initialize multipass compositor
        compositor = MultipassCompositor()
        
        # Generate multipass layers
        layers = compositor.generate_multipass_layers(base_image_path)
        
        if not layers['success']:
            raise Exception(f"Failed to generate multipass layers: {layers.get('error', 'Unknown error')}")
        
        # Composite layers
        composited_path = compositor.composite_layers(
            layers['layers'],
            output_path,
            custom_blend_modes
        )
        
        # Apply lens halation if requested
        if apply_halation:
            composited_path = compositor.apply_lens_halation(composited_path)
        
        # Inject EXIF data if requested
        if inject_exif:
            composited_path = compositor.inject_dslr_exif(composited_path)
        
        logger.info(f"Multipass compositing completed: {composited_path}")
        
        return {
            'success': True,
            'output_path': composited_path,
            'layers_used': list(layers['layers'].keys()),
            'halation_applied': apply_halation,
            'exif_injected': inject_exif,
            'processing_time': layers.get('processing_time', 0)
        }
        
    except Exception as e:
        logger.error(f"Multipass compositing failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@visual_task
def generate_cinematic_video(
    self,
    input_image_path: str,
    video_type: str = "drone_panning",
    output_path: Optional[str] = None,
    duration: float = 4.0,
    quality: str = "4K",
    service: str = "runway"
) -> Dict[str, Any]:
    """
    Generate cinematic video using AI services
    
    Args:
        input_image_path: Path to input image
        video_type: Type of cinematic video
        output_path: Output path for generated video
        duration: Video duration in seconds
        quality: Video quality (4K, 1080p, 720p)
        service: AI service to use (runway, luma)
    
    Returns:
        Dictionary containing video generation results
    """
    
    try:
        logger.info(f"Starting cinematic video generation: {video_type}")
        
        # Initialize cinematic video generator
        video_generator = CinematicVideoGenerator(
            api_key=os.getenv('RUNWAY_API_KEY') if service == 'runway' else os.getenv('LUMA_API_KEY'),
            service=service
        )
        
        # Generate video
        result = video_generator.generate_cinematic_video(
            input_image_path=input_image_path,
            video_type=video_type,
            output_path=output_path,
            duration=duration,
            quality=quality
        )
        
        if result['success']:
            logger.info(f"Cinematic video generation completed: {result['video_path']}")
            return result
        else:
            raise Exception(f"Video generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Cinematic video generation failed: {e}")
        raise self.retry(exc=e, countdown=120, max_retries=2)

@visual_task
def create_pdf_brochure(
    self,
    template_data: Dict[str, Any],
    output_path: str,
    template_type: str = "davinci",
    include_qr_code: bool = True,
    custom_css: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create PDF brochure using React templates
    
    Args:
        template_data: Data for template rendering
        output_path: Output path for PDF
        template_type: Type of template (davinci, modern, classic)
        include_qr_code: Whether to include QR code
        custom_css: Custom CSS for styling
    
    Returns:
        Dictionary containing PDF creation results
    """
    
    try:
        logger.info(f"Starting PDF brochure creation: {template_type}")
        
        # Initialize PDF creator
        from core_modules.visual.pdf_creator import PDFCreator
        pdf_creator = PDFCreator()
        
        # Create PDF
        result = pdf_creator.create_brochure_pdf(
            template_data=template_data,
            output_filename=os.path.basename(output_path),
            template_name=template_type,
            use_puppeteer=True,
            options={
                'landscape': False,
                'background': True
            }
        )
        
        if result['success']:
            logger.info(f"PDF brochure created: {result['pdf_path']}")
            return result
        else:
            raise Exception(f"PDF creation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"PDF brochure creation failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@visual_task
def process_image_post_processing(
    self,
    image_path: str,
    output_path: str,
    operations: List[Dict[str, Any]],
    preserve_metadata: bool = True
) -> Dict[str, Any]:
    """
    Process image with post-processing operations
    
    Args:
        image_path: Path to input image
        output_path: Output path for processed image
        operations: List of operations to apply
        preserve_metadata: Whether to preserve image metadata
    
    Returns:
        Dictionary containing processing results
    """
    
    try:
        logger.info(f"Starting image post-processing: {len(operations)} operations")
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"Failed to load image: {image_path}")
        
        original_shape = image.shape
        
        # Apply operations
        for operation in operations:
            op_type = operation.get('type')
            params = operation.get('params', {})
            
            if op_type == 'resize':
                image = cv2.resize(image, params.get('size', (image.shape[1], image.shape[0])))
            elif op_type == 'blur':
                kernel_size = params.get('kernel_size', 5)
                image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            elif op_type == 'sharpen':
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                image = cv2.filter2D(image, -1, kernel)
            elif op_type == 'brightness_contrast':
                alpha = params.get('alpha', 1.0)  # Contrast
                beta = params.get('beta', 0)      # Brightness
                image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
            elif op_type == 'color_correction':
                # Simple color balance
                image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(image)
                l = cv2.add(l, params.get('l_offset', 0))
                a = cv2.add(a, params.get('a_offset', 0))
                b = cv2.add(b, params.get('b_offset', 0))
                image = cv2.merge([l, a, b])
                image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
            elif op_type == 'noise_reduction':
                image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
            elif op_type == 'edge_enhancement':
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                image = cv2.addWeighted(image, 0.8, edges, 0.2, 0)
        
        # Save processed image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)
        
        # Preserve metadata if requested
        if preserve_metadata:
            try:
                from PIL import Image as PILImage
                from PIL.ExifTags import TAGS
                
                # Load original image with PIL
                original_image = PILImage.open(image_path)
                exif_data = original_image.info.get('exif')
                
                if exif_data:
                    # Save with metadata
                    processed_image = PILImage.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    processed_image.save(output_path, exif=exif_data)
                    logger.info("Image metadata preserved")
            except Exception as e:
                logger.warning(f"Failed to preserve metadata: {e}")
        
        logger.info(f"Image post-processing completed: {output_path}")
        
        return {
            'success': True,
            'output_path': output_path,
            'original_shape': original_shape,
            'final_shape': image.shape,
            'operations_applied': len(operations),
            'metadata_preserved': preserve_metadata
        }
        
    except Exception as e:
        logger.error(f"Image post-processing failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@visual_task
def batch_process_images(
    self,
    image_paths: List[str],
    output_dir: str,
    operations: List[Dict[str, Any]],
    max_concurrent: int = 5
) -> Dict[str, Any]:
    """
    Batch process multiple images
    
    Args:
        image_paths: List of input image paths
        output_dir: Output directory for processed images
        operations: List of operations to apply to each image
        max_concurrent: Maximum concurrent processes
    
    Returns:
        Dictionary containing batch processing results
    """
    
    try:
        logger.info(f"Starting batch image processing: {len(image_paths)} images")
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        failed_images = []
        
        # Process images in batches
        batch_size = max_concurrent
        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i + batch_size]
            
            # Process batch concurrently
            tasks = []
            for image_path in batch:
                output_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}")
                task = process_image_post_processing.s(
                    image_path=image_path,
                    output_path=output_path,
                    operations=operations
                )
                tasks.append(task)
            
            # Wait for batch completion
            batch_results = [task.get() for task in tasks]
            
            # Collect results
            for j, result in enumerate(batch_results):
                if result.get('success', False):
                    results.append(result)
                else:
                    failed_images.append({
                        'image_path': batch[j],
                        'error': result.get('error', 'Unknown error')
                    })
        
        logger.info(f"Batch processing completed: {len(results)} successful, {len(failed_images)} failed")
        
        return {
            'success': True,
            'processed_count': len(results),
            'failed_count': len(failed_images),
            'total_count': len(image_paths),
            'results': results,
            'failed_images': failed_images
        }
        
    except Exception as e:
        logger.error(f"Batch image processing failed: {e}")
        raise self.retry(exc=e, countdown=120, max_retries=2)

@visual_task
def optimize_image_for_web(
    self,
    image_path: str,
    output_path: str,
    quality: int = 85,
    max_width: int = 1920,
    max_height: int = 1080,
    format: str = 'jpeg'
) -> Dict[str, Any]:
    """
    Optimize image for web usage
    
    Args:
        image_path: Path to input image
        output_path: Output path for optimized image
        quality: Image quality (1-100)
        max_width: Maximum width
        max_height: Maximum height
        format: Output format (jpeg, png, webp)
    
    Returns:
        Dictionary containing optimization results
    """
    
    try:
        logger.info(f"Starting image optimization for web: {image_path}")
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"Failed to load image: {image_path}")
        
        original_size = os.path.getsize(image_path)
        original_shape = image.shape
        
        # Resize if necessary
        height, width = image.shape[:2]
        if width > max_width or height > max_height:
            # Calculate new dimensions maintaining aspect ratio
            aspect_ratio = width / height
            if width > height:
                new_width = min(width, max_width)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min(height, max_height)
                new_width = int(new_height * aspect_ratio)
            
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Convert to PIL for format conversion
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        
        # Save optimized image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if format.lower() == 'webp':
            pil_image.save(output_path, 'WEBP', quality=quality, optimize=True)
        elif format.lower() == 'png':
            pil_image.save(output_path, 'PNG', optimize=True)
        else:  # jpeg
            pil_image.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Calculate compression ratio
        optimized_size = os.path.getsize(output_path)
        compression_ratio = (original_size - optimized_size) / original_size * 100
        
        logger.info(f"Image optimization completed: {output_path} ({compression_ratio:.1f}% reduction)")
        
        return {
            'success': True,
            'output_path': output_path,
            'original_size': original_size,
            'optimized_size': optimized_size,
            'compression_ratio': compression_ratio,
            'original_shape': original_shape,
            'final_shape': image.shape,
            'format': format
        }
        
    except Exception as e:
        logger.error(f"Image optimization failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
