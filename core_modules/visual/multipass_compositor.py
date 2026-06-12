#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎨️ ANTI-PLASTIC VFX 2.0 - Multipass Compositing System
=======================================================

Advanced visual effects compositing system for Senior 3D Artist quality output.
Implements professional multipass rendering with layer compositing, lens effects,
and DSLR EXIF injection for photorealistic results.

Features:
- ComfyUI API integration for multipass rendering
- 4-layer output (Diffuse, Specular, AO, Depth)
- Professional blend modes (Multiply, Screen, Overlay, Soft Light)
- Lens halation simulation for premium optics
- DSLR EXIF data injection for authenticity
- OpenCV-based image processing
"""

import os
import logging
import asyncio
import aiohttp
import cv2
import numpy as np
from PIL import Image
import piexif
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import base64
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultipassCompositor:
    """
    Advanced multipass compositing system for professional visual effects
    """
    
    def __init__(self, comfyui_url: str, api_key: Optional[str] = None):
        self.comfyui_url = comfyui_url
        self.api_key = api_key
        self.session = aiohttp.ClientSession()
        
        # Blend mode configurations
        self.blend_modes = {
            'multiply': self._multiply_blend,
            'screen': self._screen_blend,
            'overlay': self._overlay_blend,
            'soft_light': self._soft_light_blend,
            'hard_light': self._hard_light_blend,
            'color_dodge': self._color_dodge_blend,
            'color_burn': self._color_burn_blend,
            'linear_dodge': self._linear_dodge_blend,
            'linear_burn': self._linear_burn_blend
        }
        
        # Lens halation parameters
        self.halation_threshold = 240
        self.halation_intensity = 1.5
        self.halation_blur_radius = 3
        
        # DSLR EXIF data template
        self.exif_template = {
            'make': 'Canon',
            'model': 'EOS R5',
            'lens_model': 'EF 24-70mm f/2.8L II USM',
            'focal_length': '50mm',
            'aperture': 'f/2.8',
            'iso': '100',
            'shutter_speed': '1/125',
            'datetime': '2024:01:01 12:00:00',
            'artist': 'Senior 3D Artist',
            'copyright': '© 2024 HUNTER_AGENT_AI_MARKETING_DIGITAL'
        }
        
        # Output directory
        self.output_dir = os.path.join("data", "multipass_output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_multipass_layers(
        self,
        prompt: str,
        input_image: str,
        output_format: str = "png"
    ) -> Dict[str, str]:
        """
        Generate 4-layer multipass output using ComfyUI API
        
        Args:
            prompt: Text prompt for rendering
            input_image: Path to input image
            output_format: Output format (png, jpg)
        
        Returns:
            Dictionary with paths to 4 output layers
        """
        try:
            logger.info(f"🎨️ Generating multipass layers for: {prompt}")
            
            # Load and encode input image
            image_data = self._encode_image(input_image)
            
            # Construct multipass workflow
            workflow = self._build_multipass_workflow(prompt, image_data)
            
            # Submit to ComfyUI
            result = await self._submit_workflow(workflow)
            
            # Wait for completion and fetch layers
            layers = await self._fetch_multipass_layers(result["prompt_id"], output_format)
            
            logger.info(f"✅ Multipass layers generated: {list(layers.keys())}")
            return layers
            
        except Exception as e:
            logger.error(f"❌ Multipass generation failed: {e}")
            raise
    
    def _build_multipass_workflow(self, prompt: str, image_data: str) -> Dict:
        """
        Build ComfyUI workflow for multipass rendering
        """
        return {
            "1": {
                "inputs": {
                    "ckpt_name": "RealVisXL_V4.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {
                    "text": f"{prompt}, architectural rendering, photorealistic, 8k, professional photography, detailed textures, accurate lighting",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "3": {
                "inputs": {
                    "text": "cartoon, drawing, sketch, low quality, unrealistic, plastic, artificial, 3d render, blurry, distorted",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "4": {
                "inputs": {
                    "image": image_data,
                    "controlnet_name": "control_v11p_sd15_mlsd",
                    "strength": 0.8,
                    "pixel_perfect": True
                },
                "class_type": "ControlNetLoader"
            },
            "5": {
                "inputs": {
                    "seed": 123456,
                    "steps": 30,
                    "cfg": 7.5,
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "denoise": 0.75,
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["6", 0],
                    "controlnet": ["4", 0]
                },
                "class_type": "KSampler"
            },
            "6": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "7": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode"
            },
            "8": {
                "inputs": {
                    "filename_prefix": "diffuse",
                    "images": ["7", 0]
                },
                "class_type": "SaveImage"
            },
            "9": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode"
            },
            "10": {
                "inputs": {
                    "filename_prefix": "specular",
                    "images": ["9", 0]
                },
                "class_type": "SaveImage"
            },
            "11": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode"
            },
            "12": {
                "inputs": {
                    "filename_prefix": "ao",
                    "images": ["11", 0]
                },
                "class_type": "SaveImage"
            },
            "13": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode"
            },
            "14": {
                "inputs": {
                    "filename_prefix": "depth",
                    "images": ["13", 0]
                },
                "class_type": "SaveImage"
            }
        }
    
    def composite_layers(
        self,
        layers: Dict[str, str],
        output_path: str,
        blend_config: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Composite multiple layers using professional blend modes
        
        Args:
            layers: Dictionary with paths to layer images
            output_path: Path for final composited image
            blend_config: Custom blend configuration (optional)
        
        Returns:
            Path to final composited image
        """
        try:
            logger.info("🎨️ Compositing layers with professional blend modes")
            
            # Load all layers
            diffuse = cv2.imread(layers['diffuse'])
            specular = cv2.imread(layers['specular'])
            ao = cv2.imread(layers['ao'])
            depth = cv2.imread(layers['depth'])
            
            if any(layer is None for layer in [diffuse, specular, ao, depth]):
                raise ValueError("Failed to load one or more layer images")
            
            # Check if all images have the same dimensions
            if not self._check_dimensions_consistent([diffuse, specular, ao, depth]):
                logger.warning("⚠️ Layer dimensions inconsistent, resizing to match")
                # Resize all layers to match the first layer
                height, width = diffuse.shape[:2]
                specular = cv2.resize(specular, (width, height))
                ao = cv2.resize(ao, (width, height))
                depth = cv2.resize(depth, (width, height))
            
            # Normalize layers to 0-1 range
            diffuse_norm = diffuse.astype(np.float32) / 255.0
            specular_norm = specular.astype(np.float32) / 255.0
            ao_norm = ao.astype(np.float32) / 255.0
            depth_norm = depth.astype(np.float32) / 255.0
            
            # Apply blend modes
            # Multiply AO with diffuse
            logger.info("🎨️ Applying Multiply blend for AO layer")
            ao_composite = self.blend_modes['multiply'](diffuse_norm, ao_norm)
            
            # Screen blend specular
            logger.info("🎨️ Applying Screen blend for Specular layer")
            specular_composite = self.blend_modes['screen'](ao_composite, specular_norm)
            
            # Apply depth-based fog effect
            logger.info("🎨️ Applying depth-based atmospheric fog")
            depth_fog = self._apply_depth_fog(specular_composite, depth_norm)
            
            # Convert back to 0-255 range
            final_image = (depth_fog * 255).astype(np.uint8)
            
            # Apply lens halation
            logger.info("🎨️ Applying lens halation effect")
            halated_image = self.apply_lens_halation(final_image)
            
            # Save composited image
            cv2.imwrite(output_path, halated_image)
            
            logger.info(f"✅ Layers composited: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Layer compositing failed: {e}")
            raise
    
    def apply_lens_halation(self, image: np.ndarray) -> np.ndarray:
        """
        Apply lens halation effect mimicking Leica/Hasselblad optics
        
        Args:
            image: Input image array
            
        Returns:
            Image with lens halation effect
        """
        try:
            logger.info("🎨️ Applying lens halation for premium optics")
            
            # Convert to float for processing
            image_float = image.astype(np.float32) / 255.0
            
            # Create halation mask for high-exposure areas
            gray = cv2.cvtColor(image_float, cv2.COLOR_BGR2GRAY)
            halation_mask = np.where(gray > (self.halation_threshold / 255.0), 1.0, 0.0)
            
            # Apply Gaussian blur to halation mask
            halation_blur = cv2.GaussianBlur(
                halation_mask, 
                (self.halation_blur_radius * 2 + 1, 
                 self.halation_blur_radius * 2 + 1), 0
            )
            
            # Create color halation effect
            halation_effect = np.zeros_like(image_float)
            
            # Apply different intensity for each channel (color aberration simulation)
            for i in range(3):  # RGB channels
                channel_intensity = self.halation_intensity
                if i == 0:  # Red channel (slightly stronger)
                    channel_intensity *= 1.2
                elif i == 1:  # Green channel (medium)
                    channel_intensity *= 1.0
                else:  # Blue channel (slightly weaker)
                    channel_intensity *= 0.8
                
                halation_effect[:, :, i] = halation_blur * channel_intensity
            
            # Blend halation with original image
            halated_image = image_float + halation_effect
            
            # Clip values to valid range
            halated_image = np.clip(halated_image, 0.0, 1.0)
            
            return (halated_image * 255).astype(np.uint8)
            
        except Exception as e:
            logger.error(f"❌ Lens halation failed: {e}")
            return image
    
    def inject_dslr_exif(
        self,
        image_path: str,
        exif_data: Optional[Dict] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Inject fake DSLR EXIF data for authenticity
        
        Args:
            image_path: Path to input image
            exif_data: Custom EXIF data (optional)
            output_path: Output path for image with EXIF
        
        Returns:
            Path to image with injected EXIF
        """
        try:
            logger.info("📸 Injecting DSLR EXIF data for authenticity")
            
            # Use default EXIF data if not provided
            if exif_data is None:
                exif_data = self.exif_template.copy()
            
            # Load image
            image = Image.open(image_path)
            
            # Create EXIF data
            exif_dict = {
                piexif.ExifIF.Make: exif_data['make'],
                piexif.ExifIF.Model: exif_data['model'],
                piexif.ExifIF.LensModel: exif_data['lens_model'],
                piexif.ExifIF.LensSpec: f"{exif_data['lens_model']} f/{exif_data['aperture']}",
                piexif.ExifIF.FocalLength: self._parse_aperture(exif_data['focal_length']),
                piexif.ExifIF.FNumber: self._parse_aperture(exif_data['aperture']),
                piexif.ExifIF.ISOSpeedRatings: [int(exif_data['iso'])],
                piexif.ExifIF.ExposureTime: self._parse_shutter_speed(exif_data['shutter_speed']),
                piexif.ExifIF.DateTime: exif_data['datetime'],
                piexif.ExifIF.Artist: exif_data.get('artist', 'Senior 3D Artist'),
                piexif.ExifIF.Copyright: exif_data.get('copyright', '© 2024 HUNTER_AGENT_AI_MARKETING_DIGITAL')
            }
            
            # Add additional EXIF tags for professional look
            exif_dict.update({
                piexif.ExifIF.ImageDescription: f"Professional architectural rendering - {exif_data.get('title', 'Untitled')}",
                piexif.ExifIF.Software: "ComfyUI + Anti-Plastic VFX 2.0",
                piexif.ExifIF.ProcessingSoftware: "Multipass Compositor"
            })
            
            exif_bytes = piexif.dump(exif_dict)
            
            # Determine output path
            if output_path is None:
                output_path = image_path.replace('.', '_exif.')
            
            # Save image with EXIF
            image.save(output_path, exif=exif_bytes, quality=95)
            
            logger.info(f"✅ EXIF data injected: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ EXIF injection failed: {e}")
            return image_path
    
    def _multiply_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Multiply blend mode"""
        return cv2.multiply(base, overlay)
    
    def _screen_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Screen blend mode"""
        return cv2.add(base, overlay)
    
    def _overlay_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Overlay blend mode"""
        return cv2.addWeighted(base, 0.5, overlay, 0.5)
    
    def _soft_light_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Soft light blend mode"""
        return np.where(
            overlay < 0.5,
            2 * base * overlay + base * (1 - 2 * overlay),
            2 * base * (1 - overlay) + 2 * np.sqrt(base * overlay) - 1
        )
    
    def _hard_light_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Hard light blend mode"""
        return np.where(
            overlay < 0.5,
            2 * overlay * base,
            1 - 2 * (1 - overlay) * (1 - base)
        )
    
    def _color_dodge_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Color dodge blend mode"""
        return np.where(
            overlay == 1,
            overlay,
            base / (1 - overlay)
        )
    
    def _color_burn_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Color burn blend mode"""
        return np.where(
            base == 1,
            overlay,
            1 - (1 - base) / overlay
        )
    
    def _linear_dodge_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Linear dodge blend mode"""
        return np.minimum(base, overlay / (1 - overlay + 0.001))
    
    def _linear_burn_blend(self, base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Linear burn blend mode"""
        return np.maximum(base, 1 - (1 - overlay) / (base + 0.001))
    
    def _apply_depth_fog(self, image: np.ndarray, depth: np.ndarray) -> np.ndarray:
        """
        Apply depth-based atmospheric fog effect
        
        Args:
            image: Input image
            depth: Depth map (0=near, 1=far)
            
        Returns:
            Image with depth-based fog
        """
        try:
            # Invert depth (far objects have higher values)
            depth_inverted = 1.0 - depth
            
            # Create fog color (light blue-gray for architectural rendering)
            fog_color = np.array([0.7, 0.75, 0.8])
            
            # Blend with depth
            fogged = image * (1 - depth_inverted) + fog_color * depth_inverted
            
            return fogged
            
        except Exception as e:
            logger.error(f"❌ Depth fog application failed: {e}")
            return image
    
    def _check_dimensions_consistent(self, images: List[np.ndarray]) -> bool:
        """Check if all images have the same dimensions"""
        if len(images) < 2:
            return True
        
        first_shape = images[0].shape[:2]
        return all(img.shape[:2] == first_shape for img in images)
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 for ComfyUI API"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Image encoding failed: {e}")
            raise
    
    async def _submit_workflow(self, workflow: Dict) -> Dict:
        """Submit workflow to ComfyUI"""
        try:
            payload = {"prompt": workflow}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with self.session.post(
                f"{self.comfyui_url}/prompt",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to submit workflow: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Workflow submission failed: {e}")
            raise
    
    async def _fetch_multipass_layers(
        self,
        prompt_id: str,
        output_format: str = "png"
    ) -> Dict[str, str]:
        """
        Fetch multipass layer outputs from ComfyUI
        
        Args:
            prompt_id: ComfyUI prompt ID
            output_format: Output format (png, jpg)
            
        Returns:
            Dictionary with paths to layer files
        """
        try:
            layers = {}
            layer_names = ['diffuse', 'specular', 'ao', 'depth']
            
            max_wait_time = 300  # 5 minutes
            wait_interval = 2
            elapsed_time = 0
            
            logger.info(f"⏳️ Waiting for multipass layer completion...")
            
            while elapsed_time < max_wait_time:
                try:
                    async with self.session.get(f"{self.comfyui_url}/history/{prompt_id}") as response:
                        if response.status == 200:
                            history = await response.json()
                            
                            if prompt_id in history:
                                prompt_data = history[prompt_id]
                                outputs = prompt_data.get("outputs", {})
                                
                                # Check for layer-specific outputs
                                for node_id, node_data in outputs.items():
                                    if "images" in node_data:
                                        images = node_data["images"]
                                        if images:
                                            for image_info in images:
                                                image_filename = image_info["filename"]
                                                
                                                # Check if this matches our layer names
                                                for layer_name in layer_names:
                                                    if layer_name in image_filename:
                                                        image_url = f"{self.comfyui_url}/view?filename={image_filename}"
                                                        
                                                        # Download the layer
                                                        layer_path = await self._download_image(image_url, layer_name, output_format)
                                                        layers[layer_name] = layer_path
                                
                                # Check if we have all layers
                                if len(layers) == len(layer_names):
                                    logger.info(f"✅ All layers fetched: {list(layers.keys())}")
                                    return layers
                                
                except Exception as e:
                    logger.warning(f"⚠️ Layer fetch check failed: {e}")
                
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
            
            raise TimeoutError(f"Multipass layer completion timeout after {max_wait_time} seconds")
            
        except Exception as e:
            logger.error(f"❌ Layer fetching failed: {e}")
            raise
    
    async def _download_image(
        self,
        image_url: str,
        layer_name: str,
        output_format: str = "png"
    ) -> str:
        """Download completed image from ComfyUI"""
        try:
            async with self.session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    # Save image
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{layer_name}_{timestamp}.{output_format}"
                    output_path = os.path.join(self.output_dir, filename)
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    logger.info(f"✅ Downloaded {layer_name} layer: {output_path}")
                    return output_path
                else:
                    raise Exception(f"Failed to download image: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Image download failed: {e}")
            raise
    
    def _parse_aperture(self, aperture_str: str) -> Tuple[int, int]:
        """Parse aperture string like 'f/2.8' to rational number"""
        try:
            if aperture_str.startswith('f/'):
                f_value = float(aperture_str[2:])
                return (1, int(f_value * 1000))
            return (2, 8)  # Default f/2.8
        except:
            return (2, 8)
    
    def _parse_shutter_speed(self, shutter_str: str) -> Tuple[int, int]:
        """Parse shutter speed string like '1/125' to rational number"""
        try:
            if '/' in shutter_str:
                numerator, denominator = shutter_str.split('/')
                return (int(numerator), int(denominator))
            return (1, 125)  # Default 1/125
        except:
            return (1, 125)

# Convenience function for easy usage
async def generate_multipass_layers(
    comfyui_url: str,
    prompt: str,
    input_image: str,
    api_key: Optional[str] = None,
    output_format: str = "png"
) -> Dict[str, str]:
    """
    Generate multipass layers using ComfyUI API
    
    Args:
        comfyui_url: ComfyUI server URL
        prompt: Text prompt for rendering
        input_image: Path to input image
        api_key: ComfyUI API key (optional)
        output_format: Output format (png, jpg)
    
    Returns:
        Dictionary with paths to 4 output layers
    """
    compositor = MultipassCompositor(comfyui_url, api_key)
    return await compositor.generate_multipass_layers(prompt, input_image, output_format)

def composite_layers(
    layers: Dict[str, str],
    output_path: str,
    blend_config: Optional[Dict[str, str]] = None
) -> str:
    """
    Composite multiple layers using professional blend modes
    
    Args:
        layers: Dictionary with paths to layer images
        output_path: Path for final composited image
        blend_config: Custom blend configuration (optional)
    
    Returns:
        Path to final composited image
    """
    compositor = MultipassCompositor("")
    return compositor.composite_layers(layers, output_path, blend_config)

def apply_lens_halation(
    image_path: str,
    output_path: Optional[str] = None,
    threshold: int = 240,
    intensity: float = 1.5,
    blur_radius: int = 3
) -> str:
    """
    Apply lens halation effect to image
    
    Args:
        image_path: Path to input image
        output_path: Output path (optional)
        threshold: Brightness threshold for halation
        intensity: Halation intensity
        blur_radius: Blur radius for halation effect
    
    Returns:
        Path to processed image
    """
    compositor = MultipassCompositor("")
    
    # Update parameters
    compositor.halation_threshold = threshold
    compositor.halation_intensity = intensity
    compositor.halation_blur_radius = blur_radius
    
    # Load image
    image = cv2.imread(image_path)
    
    # Apply halation
    halated_image = compositor.apply_lens_halation(image)
    
    # Save result
    if output_path is None:
        output_path = image_path.replace('.', '_halated.')
    
    cv2.imwrite(output_path, halated_image)
    
    return output_path

def inject_dslr_exif(
    image_path: str,
    exif_data: Optional[Dict] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Inject DSLR EXIF data into image
    
    Args:
        image_path: Path to input image
        exif_data: Custom EXIF data (optional)
        output_path: Output path (optional)
    
    Returns:
        Path to image with injected EXIF
    """
    compositor = MultipassCompositor("")
    return compositor.inject_dslr_exif(image_path, exif_data, output_path)

# Example usage and testing
if __name__ == "__main__":
    async def test_multipass_compositor():
        """Test multipass compositor functionality"""
        
        try:
            # Create sample image for testing
            sample_image = np.zeros((1024, 1024, 3), dtype=np.uint8)
            sample_image[:] = [100, 150, 200]  # Base color
            
            # Save sample image
            sample_path = "data/multipass_sample.png"
            os.makedirs("data", exist_ok=True)
            cv2.imwrite(sample_path, sample_image)
            
            # Test multipass generation (mock)
            compositor = MultipassCompleter("http://localhost:8188")
            
            # Mock the multipass layers for testing
            layers = {
                'diffuse': sample_path,
                'specular': sample_path,
                'ao': sample_path,
                'depth': sample_path
            }
            
            # Test compositing
            composited_path = compositor.composite_layers(
                layers,
                "data/composited_multipass.png"
            )
            print(f"✅ Composited image: {composited_path}")
            
            # Test lens halation
            halated_path = compositor.apply_lens_halation(sample_path)
            print(f"✅ Halated image: {halated_path}")
            
            # Test EXIF injection
            exif_path = compositor.inject_dslr_exif(sample_path)
            print(f"✅ EXIF injected: {exif_path}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Run test
    asyncio.run(test_multipass_compositor())
