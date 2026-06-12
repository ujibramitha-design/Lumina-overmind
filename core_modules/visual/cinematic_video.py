#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎬️ CINEMATIC AI VIDEO GENERATOR
======================================

Advanced video generation system for cinematic architectural visualization.
Integrates with Runway Gen-3 and Luma Dream Machine APIs for professional video output.

Features:
- Runway Gen-3 API integration
- Luma Dream Machine API integration
- Cinematic drone panning effects
- Slow motion architectural visualization
- 4K hyperrealistic output
- Background autoplay for VR integration
"""

import os
import logging
import asyncio
import aiohttp
import base64
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CinematicVideoGenerator:
    """
    Advanced cinematic video generator for architectural visualization
    """
    
    def __init__(self, api_key: str, service: str = "runway"):
        self.api_key = api_key
        self.service = service
        self.session = aiohttp.ClientSession()
        
        # API endpoints
        self.endpoints = {
            'runway': 'https://api.runwayml.com/v1',
            'luma': 'https://api.lumalabs.ai/api/v0'
        }
        
        # Cinematic prompts for different video types
        self.cinematic_prompts = {
            'drone_panning': (
                'Slow cinematic drone panning, architectural photography, 4k, hyperrealistic, '
                'slow motion, professional cinematography, smooth camera movement, '
                'aerial view, architectural showcase, premium quality, cinematic lighting'
            ),
            'interior_walkthrough': (
                'Cinematic interior walkthrough, smooth camera movement, architectural visualization, '
                '4k, professional lighting, natural light, detailed textures, '
                'realistic materials, professional filming'
            ),
            'exterior_flythrough': (
                'Aerial exterior flythrough, architectural showcase, smooth camera movement, '
                '4k, cinematic quality, drone footage, architectural photography, '
                'professional cinematography, high-end rendering'
            ),
            'lifestyle_shot': (
                'Lifestyle architectural photography, natural lighting, cinematic composition, '
                '4k, professional photography, warm atmosphere, detailed textures, '
                'premium quality, cinematic framing'
            ),
            'sunset_shot': (
                'Golden hour architectural photography, dramatic lighting, cinematic composition, '
                '4k, professional photography, warm colors, long shadows, '
                'sunset lighting, architectural showcase'
            ),
            'dawn_shot': (
                'Early morning architectural photography, soft lighting, cinematic composition, '
                '4k, professional photography, cool tones, misty atmosphere, '
                'dawn lighting, architectural showcase'
            )
        }
        
        # Output directory
        self.output_dir = Path("data/cinematic_videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_cinematic_video(
        self,
        input_image: str,
        video_type: str = "drone_panning",
        duration: int = 4,
        output_format: str = "mp4",
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Generate cinematic video from image
        
        Args:
            input_image: Path to input image
            video_type: Type of cinematic video
            duration: Video duration in seconds
            output_format: Output video format
            custom_prompt: Custom prompt (optional)
        
        Returns:
            Path to generated video
        """
        try:
            logger.info(f"🎬️ Generating cinematic video: {video_type}")
            logger.info(f"📸 Duration: {duration}s")
            
            # Validate input
            if not Path(input_image).exists():
                raise FileNotFoundError(f"Input image not found: {input_image}")
            
            # Validate service
            if self.service not in self.endpoints:
                raise ValueError(f"Unsupported service: {self.service}")
            
            # Get or use custom prompt
            prompt = custom_prompt or self.cinematic_prompts.get(video_type, self.cinematic_prompts['drone_panning'])
            
            logger.info(f"🎬️ Using prompt: {prompt}")
            
            # Generate video based on service
            if self.service == "runway":
                return await self._generate_with_runway(input_image, prompt, duration, output_format)
            elif self.service == "luma":
                return await self._generate_with_luma(input_image, prompt, duration, output_format)
            else:
                raise ValueError(f"Unsupported service: {self.service}")
                
        except Exception as e:
            logger.error(f"❌ Video generation failed: {e}")
            raise
    
    async def _generate_with_runway(
        self,
        input_image: str,
        prompt: str,
        duration: int,
        output_format: str
    ) -> str:
        """
        Generate video using Runway Gen-3
        
        Args:
            input_image: Path to input image
            prompt: Text prompt for video generation
            duration: Video duration in seconds
            output_format: Output video format
        
        Returns:
            Path to generated video
        """
        try:
            logger.info("🎬️ Using Runway Gen-3 for video generation")
            
            # Load and encode input image
            image_data = self._encode_image(input_image)
            
            # Create generation request
            payload = {
                "image": image_data,
                "prompt": prompt,
                "duration": duration,
                "model": "gen3a_turbo",
                "watermark": False,
                "ratio": "16:9",
                "loop": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info("🎬️ Submitting generation request to Runway...")
            
            # Submit generation request
            async with self.session.post(
                f"{self.endpoints['runway']}/video/generations",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 201:
                    result = await response.json()
                    task_id = result.get('id')
                    
                    logger.info(f"✅ Runway task created: {task_id}")
                    
                    # Wait for completion
                    video_url = await self._wait_for_runway_completion(task_id)
                    
                    # Download video
                    return await self._download_video(video_url, "runway", output_format)
                else:
                    error_data = await response.text()
                    raise Exception(f"Runway API error: {response.status} - {error_data}")
                    
        except Exception as e:
            logger.error(f"❌ Runway generation failed: {e}")
            raise
    
    async def _generate_with_luma(
        self,
        input_image: str,
        prompt: str,
        duration: int,
        output_format: str
    ) -> str:
        """
        Generate video using Luma Dream Machine
        
        Args:
            input_image: Path to input image
            prompt: Text prompt for video generation
            duration: Video duration in seconds
            output_format: Output video format
        
        Returns:
            Path to generated video
        """
        try:
            logger.info("🎬️ Using Luma Dream Machine for video generation")
            
            # Load and encode input image
            image_data = self._encode_image(input_image)
            
            # Create generation request
            payload = {
                "source": image_data,
                "prompt": prompt,
                "duration": duration,
                "aspect_ratio": "16:9",
                "loop": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info("🎬️ Submitting generation request to Luma...")
            
            # Submit generation request
            async with self.session.post(
                f"{self.endpoints['luma']}/dream-machine",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    task_id = result.get('id')
                    
                    logger.info(f"✅ Luma task created: {task_id}")
                    
                    # Wait for completion
                    video_url = await self._wait_for_luma_completion(task_id)
                    
                    # Download video
                    return await self._download_video(video_url, "luma", output_format)
                else:
                    error_data = await response.text()
                    raise Exception(f"Luma API error: {response.status} - {error_data}")
                    
        except Exception as e:
            logger.error(f"❌ Luma generation failed: {e}")
            raise
    
    async def _wait_for_runway_completion(
        self,
        task_id: str,
        max_wait_time: int = 300
    ) -> str:
        """
        Wait for Runway video completion
        
        Args:
            task_id: Runway task ID
            max_wait_time: Maximum wait time in seconds
        
        Returns:
            URL of completed video
        """
        try:
            wait_interval = 5
            elapsed_time = 0
            
            logger.info(f"⏳️ Waiting for Runway completion (max {max_wait_time}s)...")
            
            while elapsed_time < max_wait_time:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                
                async with self.session.get(
                    f"{self.endpoints['runway']}/video/generations/{task_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        status = result.get('status')
                        
                        logger.info(f"🎬️ Runway status: {status}")
                        
                        if status == 'succeeded':
                            return result.get('output', {}).get('url')
                        elif status == 'failed':
                            failure = result.get('failure')
                            raise Exception(f"Runway generation failed: {failure}")
                        elif status == 'queued':
                            logger.info(f"🎬️ Still queued, waiting...")
                        elif status == 'running':
                            logger.info(f"🎬️ Still running, processing...")
                        else:
                            logger.warning(f"⚠️ Unknown status: {status}")
                    else:
                        raise Exception(f"Runway API error: {response.status}")
                
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
            
            raise TimeoutError(f"Runway video completion timeout after {max_wait_time} seconds")
            
        except Exception as e:
            logger.error(f"❌ Runway completion check failed: {e}")
            raise
    
    async def _wait_for_luma_completion(
        self,
        task_id: str,
        max_wait_time: int = 300
    ) -> str:
        """
        Wait for Luma video completion
        
        Args:
            task_id: Luma task ID
            max_wait_time: Maximum wait time in seconds
        
        Returns:
            URL of completed video
        """
        try:
            wait_interval = 5
            elapsed_time = 0
            
            logger.info(f"⏳️ Waiting for Luma completion (max {max_wait_time}s)...")
            
            while elapsed_time < max_wait_time:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                
                async with self.session.get(
                    f"{self.endpoints['luma']}/dream-machine/{task_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        status = result.get('state')
                        
                        logger.info(f"🎬️ Luma status: {status}")
                        
                        if status == 'completed':
                            return result.get('video_url')
                        elif status == 'failed':
                            failure = result.get('error')
                            raise Exception(f"Luma generation failed: {failure}")
                        elif status == 'queued':
                            logger.info(f"🎬️ Still queued, waiting...")
                        elif status == 'running':
                            logger.info(f"🎬️ Still running, processing...")
                        else:
                            logger.warning(f"⚠️ Unknown status: {status}")
                    else:
                        raise Exception(f"Luma API error: {response.status}")
                
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
            
            raise TimeoutError(f"Luma video completion timeout after {max_wait_time} seconds")
            
        except Exception as e:
            logger.error(f"❌ Luma completion check failed: {e}")
            raise
    
    async def _download_video(
        self,
        video_url: str,
        service: str,
        output_format: str = "mp4"
    ) -> str:
        """
        Download generated video
        
        Args:
            video_url: URL of completed video
            service: Service name (runway/luma)
            output_format: Output video format
        
        Returns:
            Path to downloaded video
        """
        try:
            logger.info(f"🎬️ Downloading video from {service}")
            
            async with self.session.get(video_url) as response:
                if response.status == 200:
                    video_data = await response.read()
                    
                    # Create filename with timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"cinematic_{service}_{timestamp}.{output_format}"
                    output_path = self.output_dir / filename
                    
                    # Save video
                    with open(output_path, 'wb') as f:
                        f.write(video_data)
                    
                    logger.info(f"✅ Video downloaded: {output_path}")
                    return str(output_path)
                else:
                    error_data = await response.text()
                    raise Exception(f"Failed to download video: {response.status} - {error_data}")
                    
        except Exception as e:
            logger.error(f"❌ Video download failed: {e}")
            raise
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API submission"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Image encoding failed: {e}")
            raise
    
    def get_available_video_types(self) -> List[str]:
        """Get list of available video types"""
        return list(self.cinematic_prompts.keys())
    
    def get_cinematic_prompt(self, video_type: str) -> str:
        """Get cinematic prompt for video type"""
        return self.cinematic_prompts.get(video_type, self.cinematic_prompts['drone_panning'])
    
    def add_custom_video_type(
        self,
        video_type: str,
        prompt: str
    ):
        """
        Add custom video type with custom prompt
        
        Args:
            video_type: Name of video type
            prompt: Cinematic prompt for video type
        """
        self.cinematic_prompts[video_type] = prompt
        logger.info(f"✅ Added custom video type: {video_type}")

# Convenience function for easy usage
async def generate_cinematic_video(
    api_key: str,
    input_image: str,
    video_type: str = "drone_panning",
    duration: int = 4,
    output_format: str = "mp4",
    service: str = "runway",
    custom_prompt: Optional[str] = None
) -> str:
    """
    Generate cinematic video using AI service
    
    Args:
        api_key: API key for video service
        input_image: Path to input image
        video_type: Type of cinematic video
        duration: Video duration in seconds
        output_format: Output video format
        service: Video service to use (runway/luma)
        custom_prompt: Custom prompt (optional)
    
    Returns:
        Path to generated video
    """
    generator = CinematicVideoGenerator(api_key, service)
    return await generator.generate_cinematic_video(
        input_image=input_image,
        video_type=video_type,
        duration=duration,
        output_format=output_format,
        custom_prompt=custom_prompt
    )

# Example usage and testing
if __name__ == "__main__":
    async def test_cinematic_video():
        """Test cinematic video generation"""
        
        try:
            # Create sample image for testing
            from PIL import Image
            import numpy as np
            
            # Create a sample image
            sample_image = np.zeros((1024, 1024, 3), dtype=np.uint8)
            sample_image[:] = [100, 150, 200]  # Base color
            sample_image[400:600, 400:600] = [50, 100, 150]  # Center area
            
            # Save sample image
            sample_path = "data/cinematic_sample.png"
            os.makedirs("data", exist_ok=True)
            Image.fromarray(sample_image).save(sample_path)
            
            # Test video generation (mock)
            generator = CinematicVideoGenerator("test_api_key", "runway")
            
            # Test with mock data since we don't have real API keys
            print("✅ Cinematic Video Generator initialized")
            print(f"🎬️ Available video types: {generator.get_available_video_types()}")
            print(f"🎬️ Default prompt for drone_panning: {generator.get_cinematic_prompt('drone_panning')}")
            
            print("✅ Test completed (no actual API calls made)")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Run test
    asyncio.run(test_cinematic_video())
