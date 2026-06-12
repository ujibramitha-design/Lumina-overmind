#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎨 AGENCY API ADAPTER - External Design Services Integration
===========================================================

Professional design service integration for premium brochure generation.
Supports Bannerbear, Adobe PDF Services, and other design APIs.

Features:
- REST API integration with external design services
- Template-based design generation
- Image and text layer manipulation
- High-quality output from professional design tools
- Fallback to local rendering if external services unavailable
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import asyncio
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgencyAPIAdapter:
    """Adapter for external design service APIs"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.output_dir = Path("data/brochures")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # API configurations
        self.bannerbear_config = {
            'api_key': self.config.get('bannerbear_api_key', os.getenv('BANNERBEAR_API_KEY')),
            'base_url': 'https://api.bannerbear.com/v2',
            'templates': {
                'luxury_property': 'template_luxury_property_id',
                'modern_apartment': 'template_modern_apartment_id',
                'commercial_space': 'template_commercial_space_id',
                'minimalist_home': 'template_minimalist_home_id'
            }
        }
        
        self.adobe_config = {
            'api_key': self.config.get('adobe_api_key', os.getenv('ADOBE_API_KEY')),
            'client_secret': self.config.get('adobe_client_secret', os.getenv('ADOBE_CLIENT_SECRET')),
            'base_url': 'https://pdf-services.adobe.io',
            'templates': {
                'luxury_property': 'adobe_luxury_template_id',
                'modern_apartment': 'adobe_modern_template_id',
                'commercial_space': 'adobe_commercial_template_id',
                'minimalist_home': 'adobe_minimalist_template_id'
            }
        }
        
        # Request timeout settings
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_with_bannerbear(
        self,
        template_name: str,
        context_data: Dict[str, Any],
        output_format: str = "pdf"
    ) -> str:
        """
        Generate brochure using Bannerbear API
        
        Args:
            template_name: Template to use
            context_data: Dynamic data for template
            output_format: 'pdf' or 'jpg'
        
        Returns:
            Path to generated file
        """
        try:
            if not self.bannerbear_config['api_key']:
                raise ValueError("Bannerbear API key not configured")
            
            # Get template ID
            template_id = self.bannerbear_config['templates'].get(template_name)
            if not template_id:
                raise ValueError(f"Template '{template_name}' not found in Bannerbear configuration")
            
            # Prepare image modifications
            modifications = self._prepare_bannerbear_modifications(context_data)
            
            # Create image generation request
            payload = {
                'template': template_id,
                'modifications': modifications,
                'format': output_format,
                'quality': 95
            }
            
            # Make API request
            headers = {
                'Authorization': f"Bearer {self.bannerbear_config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.bannerbear_config['base_url']}/images",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Bannerbear API error: {response.status_code} - {response.text}")
            
            result = response.json()
            image_uid = result.get('image_uid')
            
            if not image_uid:
                raise ValueError("No image UID returned from Bannerbear")
            
            # Wait for image to be processed
            image_url = await self._wait_for_bannerbear_image(image_uid)
            
            # Download the generated image
            filename = f"bannerbear_{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
            output_path = self.output_dir / filename
            
            # Download image
            image_response = requests.get(image_url, timeout=self.timeout)
            image_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(image_response.content)
            
            logger.info(f"✅ Bannerbear brochure generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Bannerbear generation failed: {e}")
            raise
    
    async def generate_with_adobe_pdf_services(
        self,
        template_name: str,
        context_data: Dict[str, Any],
        output_format: str = "pdf"
    ) -> str:
        """
        Generate brochure using Adobe PDF Services API
        
        Args:
            template_name: Template to use
            context_data: Dynamic data for template
            output_format: 'pdf' or 'jpg'
        
        Returns:
            Path to generated file
        """
        try:
            if not self.adobe_config['api_key'] or not self.adobe_config['client_secret']:
                raise ValueError("Adobe PDF Services API credentials not configured")
            
            # Get template ID
            template_id = self.adobe_config['templates'].get(template_name)
            if not template_id:
                raise ValueError(f"Template '{template_name}' not found in Adobe configuration")
            
            # Prepare document generation request
            document_data = self._prepare_adobe_document_data(context_data)
            
            # Create document generation job
            job_payload = {
                'templateId': template_id,
                'outputFormat': output_format,
                'data': document_data,
                'options': {
                    'pdfA': True,
                    'linearize': True,
                    'compress': True
                }
            }
            
            # Get access token
            access_token = await self._get_adobe_access_token()
            
            # Submit job
            headers = {
                'Authorization': f"Bearer {access_token}",
                'Content-Type': 'application/json',
                'x-api-key': self.adobe_config['api_key']
            }
            
            response = requests.post(
                f"{self.adobe_config['base_url']}/documentGenerationJobs",
                json=job_payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code != 201:
                raise Exception(f"Adobe PDF Services error: {response.status_code} - {response.text}")
            
            job_result = response.json()
            job_id = job_result.get('id')
            
            if not job_id:
                raise ValueError("No job ID returned from Adobe PDF Services")
            
            # Wait for job completion
            download_url = await self._wait_for_adobe_job(job_id, access_token)
            
            # Download the generated document
            filename = f"adobe_{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
            output_path = self.output_dir / filename
            
            # Download document
            document_response = requests.get(download_url, timeout=self.timeout)
            document_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(document_response.content)
            
            logger.info(f"✅ Adobe PDF Services brochure generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Adobe PDF Services generation failed: {e}")
            raise
    
    def _prepare_bannerbear_modifications(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare Bannerbear modifications from context data"""
        modifications = []
        
        # Text modifications
        text_fields = [
            'NAMA_PROPERTI', 'LOKASI_PREMIUM', 'LUAS_TANAH', 'LUAS_BANGUNAN',
            'JUMLAH_KAMAR', 'HARGA_DINAMIS', 'NAMA_KLIEN', 'KONTAK_KLIEN',
            'TAGLINE_MODERN', 'DESKRIPSI_LOKASI', 'SALES_CONTACT'
        ]
        
        for field in text_fields:
            if field in context_data:
                modifications.append({
                    'name': field.lower(),
                    'text': str(context_data[field]),
                    'color': '#000000',
                    'size': 24
                })
        
        # Image modifications
        if 'GAMBAR_AI' in context_data:
            modifications.append({
                'name': 'gambar_ai',
                'image_url': context_data['GAMBAR_AI']
            })
        
        return modifications
    
    def _prepare_adobe_document_data(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare Adobe PDF Services document data"""
        document_data = {}
        
        # Map context data to Adobe template fields
        field_mapping = {
            'NAMA_PROPERTI': 'property_name',
            'LOKASI_PREMIUM': 'location',
            'LUAS_TANAH': 'land_area',
            'LUAS_BANGUNAN': 'building_area',
            'JUMLAH_KAMAR': 'bedrooms',
            'HARGA_DINAMIS': 'price',
            'NAMA_KLIEN': 'client_name',
            'KONTAK_KLIEN': 'client_contact',
            'GAMBAR_AI': 'hero_image',
            'DESKRIPSI_LOKASI': 'location_description'
        }
        
        for context_key, adobe_key in field_mapping.items():
            if context_key in context_data:
                document_data[adobe_key] = context_data[context_key]
        
        return document_data
    
    async def _wait_for_bannerbear_image(self, image_uid: str) -> str:
        """Wait for Bannerbear image processing to complete"""
        max_wait_time = 120  # 2 minutes
        wait_interval = 5
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                headers = {
                    'Authorization': f"Bearer {self.bannerbear_config['api_key']}",
                    'Content-Type': 'application/json'
                }
                
                response = requests.get(
                    f"{self.bannerbear_config['base_url']}/images/{image_uid}",
                    headers=headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'completed':
                        return result.get('image_url')
                    elif status == 'failed':
                        raise Exception(f"Bannerbear image processing failed: {result.get('error', 'Unknown error')}")
                
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
                
            except Exception as e:
                logger.warning(f"Bannerbear status check failed: {e}")
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
        
        raise TimeoutError(f"Bannerbear image processing timeout after {max_wait_time} seconds")
    
    async def _wait_for_adobe_job(self, job_id: str, access_token: str) -> str:
        """Wait for Adobe PDF Services job to complete"""
        max_wait_time = 180  # 3 minutes
        wait_interval = 10
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                headers = {
                    'Authorization': f"Bearer {access_token}",
                    'Content-Type': 'application/json',
                    'x-api-key': self.adobe_config['api_key']
                }
                
                response = requests.get(
                    f"{self.adobe_config['base_url']}/documentGenerationJobs/{job_id}",
                    headers=headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'done':
                        return result.get('output', {}).get('content', {}).get('downloadUrl')
                    elif status == 'failed':
                        raise Exception(f"Adobe PDF Services job failed: {result.get('error', 'Unknown error')}")
                
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
                
            except Exception as e:
                logger.warning(f"Adobe job status check failed: {e}")
                await asyncio.sleep(wait_interval)
                elapsed_time += wait_interval
        
        raise TimeoutError(f"Adobe PDF Services job timeout after {max_wait_time} seconds")
    
    async def _get_adobe_access_token(self) -> str:
        """Get Adobe PDF Services access token"""
        try:
            payload = {
                'client_id': self.adobe_config['api_key'],
                'client_secret': self.adobe_config['client_secret'],
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(
                'https://ims-na1.adobelogin.com/ims/oauth2/token',
                data=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Adobe authentication failed: {response.status_code} - {response.text}")
            
            result = response.json()
            return result.get('access_token')
            
        except Exception as e:
            logger.error(f"❌ Adobe authentication failed: {e}")
            raise
    
    async def generate_brochure(
        self,
        template_name: str,
        context_data: Dict[str, Any],
        output_format: str = "pdf",
        service: str = "auto"
    ) -> str:
        """
        Generate brochure using available services
        
        Args:
            template_name: Template to use
            context_data: Dynamic data for template
            output_format: 'pdf' or 'jpg'
            service: 'bannerbear', 'adobe', 'auto', or 'local'
        
        Returns:
            Path to generated file
        """
        services_to_try = []
        
        if service == "auto":
            # Try services in order of preference
            if self.bannerbear_config['api_key']:
                services_to_try.append("bannerbear")
            if self.adobe_config['api_key'] and self.adobe_config['client_secret']:
                services_to_try.append("adobe")
            services_to_try.append("local")
        elif service == "bannerbear":
            services_to_try.append("bannerbear")
        elif service == "adobe":
            services_to_try.append("adobe")
        elif service == "local":
            services_to_try.append("local")
        else:
            raise ValueError(f"Unknown service: {service}")
        
        last_error = None
        
        for service_name in services_to_try:
            try:
                if service_name == "bannerbear":
                    return await self.generate_with_bannerbear(template_name, context_data, output_format)
                elif service_name == "adobe":
                    return await self.generate_with_adobe_pdf_services(template_name, context_data, output_format)
                elif service_name == "local":
                    # Fallback to local renderer
                    from .pixel_perfect_renderer import generate_premium_brochure
                    return await generate_premium_brochure(template_name, context_data, output_format)
                    
            except Exception as e:
                logger.warning(f"❌ {service_name} failed: {e}")
                last_error = e
                continue
        
        # All services failed
        raise Exception(f"All brochure generation services failed. Last error: {last_error}")

# Convenience function for easy usage
async def generate_agency_brochure(
    template_name: str,
    context_data: Dict[str, Any],
    output_format: str = "pdf",
    service: str = "auto",
    config: Dict[str, Any] = None
) -> str:
    """
    Generate brochure using agency design services
    
    Args:
        template_name: Template to use
        context_data: Dynamic data for template
        output_format: 'pdf' or 'jpg'
        service: 'bannerbear', 'adobe', 'auto', or 'local'
        config: Service configuration
    
    Returns:
        Path to generated file
    """
    adapter = AgencyAPIAdapter(config)
    return await adapter.generate_brochure(
        template_name=template_name,
        context_data=context_data,
        output_format=output_format,
        service=service
    )

# Example usage and testing
if __name__ == "__main__":
    async def test_agency_services():
        """Test agency service integration"""
        
        # Sample data
        sample_data = {
            "NAMA_PROPERTI": "The Executive Suite",
            "LOKASI_PREMIUM": "Jakarta CBD",
            "LUAS_TANAH": "300",
            "LUAS_BANGUNAN": "450",
            "JUMLAH_KAMAR": "3",
            "GAMBAR_AI": "https://via.placeholder.com/1200x800/333333/ffffff?text=Executive+Suite",
            "HARGA_DINAMIS": "8.500.000.000",
            "NAMA_KLIEN": "Budi Santoso",
            "KONTAK_KLIEN": "+62 811-2233-4455",
            "DESKRIPSI_LOKASI": "Prime location in Jakarta Central Business District"
        }
        
        try:
            # Test with auto service selection
            brochure_path = await generate_agency_brochure(
                template_name="luxury_property",
                context_data=sample_data,
                output_format="pdf",
                service="auto"
            )
            print(f"✅ Agency brochure generated: {brochure_path}")
            
        except Exception as e:
            print(f"❌ Agency generation failed: {e}")
    
    # Run test
    asyncio.run(test_agency_services())
