#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎨 PIXEL PERFECT RENDERER - Headless Design Engine
===============================================

Advanced brochure generation system using Playwright for premium PDF/JPG output.
Replaces fpdf and Pillow with professional-grade web rendering.

Features:
- Playwright-based headless browser rendering
- Premium HTML/CSS templates with TailwindCSS
- Print-ready PDF generation (A4/A5, high resolution)
- Dynamic data injection and template customization
- Agency-quality design output
"""

import asyncio
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    from playwright._impl._api_types import PageError
except ImportError:
    print("❌ Playwright not found. Install with: pip install playwright && python -m playwright install")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PixelPerfectRenderer:
    """Advanced brochure renderer using Playwright"""
    
    def __init__(self, output_dir: str = "data/brochures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir = Path("core_modules/visual/templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Browser configuration
        self.browser_config = {
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-gpu'
            ]
        }
        
        # PDF export settings
        self.pdf_config = {
            'format': 'A4',
            'print_background': True,
            'margin': {
                'top': '0mm',
                'right': '0mm',
                'bottom': '0mm',
                'left': '0mm'
            },
            'scale': 1.0,
            'prefer_css_page_size': True
        }
        
        # Image export settings
        self.image_config = {
            'type': 'png',
            'quality': 100,
            'full_page': True,
            'clip': None
        }
    
    async def _initialize_browser(self) -> tuple[Browser, BrowserContext]:
        """Initialize Playwright browser with optimal settings"""
        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(**self.browser_config)
            context = await browser.new_context(
                viewport={'width': 1200, 'height': 1600},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            return browser, context
        except Exception as e:
            logger.error(f"❌ Browser initialization failed: {e}")
            raise
    
    def _get_template_html(self, template_name: str) -> str:
        """Load HTML template with TailwindCSS styling"""
        templates = {
            'luxury_property': self._get_luxury_property_template(),
            'modern_apartment': self._get_modern_apartment_template(),
            'commercial_space': self._get_commercial_space_template(),
            'minimalist_home': self._get_minimalist_home_template()
        }
        
        if template_name not in templates:
            raise ValueError(f"Template '{template_name}' not found. Available: {list(templates.keys())}")
        
        return templates[template_name]
    
    def _inject_data_into_template(self, html_template: str, context_data: Dict[str, Any]) -> str:
        """Inject dynamic data into HTML template"""
        html = html_template
        
        # Replace placeholders with actual data
        for key, value in context_data.items():
            placeholder = f"{{{{{key.upper()}}}}}"
            if isinstance(value, (dict, list)):
                # Handle complex data structures
                value = json.dumps(value, ensure_ascii=False)
            elif value is None:
                value = ""
            else:
                value = str(value)
            
            html = html.replace(placeholder, value)
        
        return html
    
    async def generate_premium_brochure(
        self,
        template_name: str,
        context_data: Dict[str, Any],
        output_format: str = "pdf",
        filename: Optional[str] = None
    ) -> str:
        """
        Generate premium brochure with Playwright rendering
        
        Args:
            template_name: Template to use ('luxury_property', 'modern_apartment', etc.)
            context_data: Dynamic data to inject into template
            output_format: 'pdf' or 'jpg'
            filename: Custom filename (auto-generated if None)
        
        Returns:
            Path to generated file
        """
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"brochure_{template_name}_{timestamp}.{output_format}"
            
            output_path = self.output_dir / filename
            
            # Initialize browser
            browser, context = await self._initialize_browser()
            page = await context.new_page()
            
            # Get and prepare template
            html_template = self._get_template_html(template_name)
            html_content = self._inject_data_into_template(html_template, context_data)
            
            # Set page content
            await page.set_content(html_content, wait_until='networkidle')
            
            # Wait for all images to load
            await page.wait_for_load_state('networkidle')
            
            # Generate output
            if output_format.lower() == 'pdf':
                await page.pdf(path=str(output_path), **self.pdf_config)
            elif output_format.lower() in ['jpg', 'jpeg', 'png']:
                await page.screenshot(path=str(output_path), **self.image_config)
            else:
                raise ValueError(f"Unsupported format: {output_format}")
            
            # Cleanup
            await context.close()
            await browser.close()
            
            logger.info(f"✅ Brochure generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Brochure generation failed: {e}")
            raise
    
    def _get_luxury_property_template(self) -> str:
        """Premium luxury property brochure template"""
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luxury Property Brochure</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-serif { font-family: 'Playfair Display', serif; }
        .gradient-overlay {
            background: linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 100%);
        }
        .gold-accent { color: #D4AF37; }
        .gold-border { border-color: #D4AF37; }
        .luxury-gradient {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- A4 Size Container -->
    <div class="w-[210mm] h-[297mm] bg-white overflow-hidden">
        
        <!-- Hero Section with Background -->
        <div class="relative h-[45%] bg-cover bg-center" style="background-image: url('{{GAMBAR_AI}}');">
            <div class="gradient-overlay absolute inset-0 flex items-center justify-center">
                <div class="text-center text-white px-8">
                    <h1 class="font-serif text-5xl font-bold mb-2">{{NAMA_PROPERTI}}</h1>
                    <p class="text-xl font-light tracking-wide">{{LOKASI_PREMIUM}}</p>
                    <div class="mt-4 flex justify-center space-x-8">
                        <div class="text-center">
                            <p class="text-3xl font-bold gold-accent">{{LUAS_TANAH}}m²</p>
                            <p class="text-sm">Tanah</p>
                        </div>
                        <div class="text-center">
                            <p class="text-3xl font-bold gold-accent">{{LUAS_BANGUNAN}}m²</p>
                            <p class="text-sm">Bangunan</p>
                        </div>
                        <div class="text-center">
                            <p class="text-3xl font-bold gold-accent">{{JUMLAH_KAMAR}}</p>
                            <p class="text-sm">Kamar</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Content Section -->
        <div class="h-[55%] p-12">
            <!-- Header -->
            <div class="text-center mb-8">
                <h2 class="font-serif text-3xl font-bold text-gray-800 mb-2">Eksklusifitas Tanpa Kompromi</h2>
                <div class="w-24 h-1 gold-border border-t-2 mx-auto"></div>
            </div>
            
            <!-- Main Content Grid -->
            <div class="grid grid-cols-2 gap-8 mb-8">
                <!-- Left Column -->
                <div>
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">Fitur Unggulan</h3>
                    <ul class="space-y-2 text-gray-600">
                        <li class="flex items-start">
                            <span class="gold-accent mr-2">✓</span>
                            <span>{{FITUR_1}}</span>
                        </li>
                        <li class="flex items-start">
                            <span class="gold-accent mr-2">✓</span>
                            <span>{{FITUR_2}}</span>
                        </li>
                        <li class="flex items-start">
                            <span class="gold-accent mr-2">✓</span>
                            <span>{{FITUR_3}}</span>
                        </li>
                        <li class="flex items-start">
                            <span class="gold-accent mr-2">✓</span>
                            <span>{{FITUR_4}}</span>
                        </li>
                    </ul>
                </div>
                
                <!-- Right Column -->
                <div>
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">Lokasi Strategis</h3>
                    <p class="text-gray-600 mb-4">{{DESKRIPSI_LOKASI}}</p>
                    <div class="luxury-gradient rounded-lg p-4 text-white">
                        <p class="text-sm mb-1">Akses Mudah Menuju:</p>
                        <p class="text-xs">{{AKSES_LOKASI}}</p>
                    </div>
                </div>
            </div>
            
            <!-- Price Section -->
            <div class="border-t-2 gold-border pt-6">
                <div class="flex justify-between items-end">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Investasi Premium</p>
                        <p class="text-3xl font-bold text-gray-800">Rp {{HARGA_DINAMIS}}</p>
                        <p class="text-sm text-gray-500">{{HARGA_PER_METER}} per m²</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm text-gray-600 mb-2">Khusus Untuk</p>
                        <p class="text-xl font-semibold text-gray-800">{{NAMA_KLIEN}}</p>
                        <p class="text-sm text-gray-500">{{KONTAK_KLIEN}}</p>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="mt-8 pt-4 border-t border-gray-200">
                <div class="flex justify-between items-center text-xs text-gray-500">
                    <p>© 2026 Luxury Properties</p>
                    <p>Generated: {{TANGGAL_GENERASI}}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def _get_modern_apartment_template(self) -> str:
        """Modern apartment brochure template"""
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Apartment Brochure</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; }
        .font-montserrat { font-family: 'Montserrat', sans-serif; }
        .modern-gradient {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .accent-purple { color: #667eea; }
        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="bg-gray-100">
    <!-- A4 Size Container -->
    <div class="w-[210mm] h-[297mm] bg-white overflow-hidden">
        
        <!-- Hero Section -->
        <div class="relative h-[40%] modern-gradient">
            <div class="absolute inset-0 bg-cover bg-center opacity-30" style="background-image: url('{{GAMBAR_AI}}');"></div>
            <div class="relative h-full flex items-center justify-center">
                <div class="text-center text-white px-8">
                    <h1 class="font-montserrat text-4xl font-bold mb-2">{{NAMA_PROPERTI}}</h1>
                    <p class="text-lg font-light mb-4">{{TAGLINE_MODERN}}</p>
                    <div class="glass-effect rounded-lg px-6 py-3 inline-block">
                        <p class="text-2xl font-bold">Rp {{HARGA_DINAMIS}}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Content Section -->
        <div class="h-[60%] p-10">
            <!-- Stats Bar -->
            <div class="grid grid-cols-4 gap-4 mb-8">
                <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <p class="text-2xl font-bold accent-purple">{{LUAS_BANGUNAN}}m²</p>
                    <p class="text-xs text-gray-600">Luas Unit</p>
                </div>
                <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <p class="text-2xl font-bold accent-purple">{{JUMLAH_KAMAR}}</p>
                    <p class="text-xs text-gray-600">Kamar Tidur</p>
                </div>
                <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <p class="text-2xl font-bold accent-purple">{{LANTAI_UNIT}}</p>
                    <p class="text-xs text-gray-600">Lantai</p>
                </div>
                <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <p class="text-2xl font-bold accent-purple">{{TIPE_UNIT}}</p>
                    <p class="text-xs text-gray-600">Tipe</p>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="grid grid-cols-3 gap-6 mb-8">
                <!-- Features -->
                <div class="col-span-2">
                    <h3 class="font-montserrat text-xl font-semibold text-gray-800 mb-4">Fasilitas Premium</h3>
                    <div class="grid grid-cols-2 gap-3">
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 accent-purple bg-purple-600 rounded-full"></div>
                            <span class="text-sm text-gray-700">{{FASILITAS_1}}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 accent-purple bg-purple-600 rounded-full"></div>
                            <span class="text-sm text-gray-700">{{FASILITAS_2}}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 accent-purple bg-purple-600 rounded-full"></div>
                            <span class="text-sm text-gray-700">{{FASILITAS_3}}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 accent-purple bg-purple-600 rounded-full"></div>
                            <span class="text-sm text-gray-700">{{FASILITAS_4}}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 accent-purple bg-purple-600 rounded-full"></div>
                            <span class="text-sm text-gray-700">{{FASILITAS_5}}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 accent-purple bg-purple-600 rounded-full"></div>
                            <span class="text-sm text-gray-700">{{FASILITAS_6}}</span>
                        </div>
                    </div>
                </div>
                
                <!-- Location Info -->
                <div>
                    <h3 class="font-montserrat text-xl font-semibold text-gray-800 mb-4">Lokasi</h3>
                    <div class="bg-purple-50 rounded-lg p-4">
                        <p class="text-sm text-gray-700 mb-2">{{ALAMAT_LENGKAP}}</p>
                        <div class="space-y-1">
                            <p class="text-xs text-gray-600">📍 {{DISTRIK_UTAMA}}</p>
                            <p class="text-xs text-gray-600">🚇 {{STASIUN_TERDEKAT}}</p>
                            <p class="text-xs text-gray-600">🛍️ {{MALL_TERDEKAT}}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Client Info & CTA -->
            <div class="modern-gradient rounded-lg p-6 text-white">
                <div class="flex justify-between items-center">
                    <div>
                        <p class="text-sm opacity-90 mb-1">Penawaran Khusus Untuk</p>
                        <p class="text-xl font-semibold">{{NAMA_KLIEN}}</p>
                        <p class="text-sm opacity-75">{{KONTAK_KLIEN}}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm opacity-90 mb-2">Hubungi Sekarang</p>
                        <p class="text-lg font-semibold">{{SALES_CONTACT}}</p>
                        <p class="text-sm opacity-75">{{TANGGAL_GENERASI}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def _get_commercial_space_template(self) -> str:
        """Commercial space brochure template"""
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commercial Space Brochure</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Oswald:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Roboto', sans-serif; }
        .font-oswald { font-family: 'Oswald', sans-serif; }
        .business-gradient {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        }
        .accent-blue { color: #2a5298; }
        .professional-border { border-color: #2a5298; }
    </style>
</head>
<body class="bg-gray-50">
    <!-- A4 Size Container -->
    <div class="w-[210mm] h-[297mm] bg-white overflow-hidden">
        
        <!-- Header -->
        <div class="business-gradient h-[25%] flex items-center justify-center">
            <div class="text-center text-white px-8">
                <h1 class="font-oswald text-3xl font-bold mb-2">{{NAMA_PROPERTI}}</h1>
                <p class="text-lg">{{TAGLINE_KOMERSIAL}}</p>
            </div>
        </div>
        
        <!-- Hero Image -->
        <div class="h-[25%] bg-cover bg-center" style="background-image: url('{{GAMBAR_AI}}');">
            <div class="h-full bg-black bg-opacity-40 flex items-end">
                <div class="bg-white p-4 m-4 rounded-lg">
                    <p class="text-2xl font-bold accent-blue">Rp {{HARGA_DINAMIS}}</p>
                    <p class="text-sm text-gray-600">{{HARGA_PER_METER}} per m²</p>
                </div>
            </div>
        </div>
        
        <!-- Content -->
        <div class="h-[50%] p-8">
            <!-- Key Metrics -->
            <div class="grid grid-cols-4 gap-4 mb-6">
                <div class="text-center p-3 border professional-border rounded">
                    <p class="text-xl font-bold accent-blue">{{LUAS_TANAH}}m²</p>
                    <p class="text-xs text-gray-600">Luas Tanah</p>
                </div>
                <div class="text-center p-3 border professional-border rounded">
                    <p class="text-xl font-bold accent-blue">{{LUAS_BANGUNAN}}m²</p>
                    <p class="text-xs text-gray-600">Luas Bangunan</p>
                </div>
                <div class="text-center p-3 border professional-border rounded">
                    <p class="text-xl font-bold accent-blue">{{JUMLAH_LANTAI}}</p>
                    <p class="text-xs text-gray-600">Jumlah Lantai</p>
                </div>
                <div class="text-center p-3 border professional-border rounded">
                    <p class="text-xl font-bold accent-blue">{{PARKIR_KAPASITAS}}</p>
                    <p class="text-xs text-gray-600">Kapasitas Parkir</p>
                </div>
            </div>
            
            <!-- Business Details -->
            <div class="grid grid-cols-2 gap-6 mb-6">
                <div>
                    <h3 class="font-oswald text-lg font-semibold text-gray-800 mb-3">Keunggulan Lokasi</h3>
                    <ul class="space-y-2 text-sm text-gray-700">
                        <li class="flex items-start">
                            <span class="accent-blue mr-2">•</span>
                            <span>{{KEUNGGULAN_1}}</span>
                        </li>
                        <li class="flex items-start">
                            <span class="accent-blue mr-2">•</span>
                            <span>{{KEUNGGULAN_2}}</span>
                        </li>
                        <li class="flex items-start">
                            <span class="accent-blue mr-2">•</span>
                            <span>{{KEUNGGULAN_3}}</span>
                        </li>
                        <li class="flex items-start">
                            <span class="accent-blue mr-2">•</span>
                            <span>{{KEUNGGULAN_4}}</span>
                        </li>
                    </ul>
                </div>
                
                <div>
                    <h3 class="font-oswald text-lg font-semibold text-gray-800 mb-3">Spesifikasi</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Sertifikat:</span>
                            <span class="font-medium">{{SERTIFIKAT_JENIS}}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Daya Listrik:</span>
                            <span class="font-medium">{{DAYA_LISTRIK}}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Air:</span>
                            <span class="font-medium">{{SUMBER_AIR}}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Akses:</span>
                            <span class="font-medium">{{AKSES_JALAN}}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Client Information -->
            <div class="border-t-2 professional-border pt-4">
                <div class="flex justify-between items-center">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Informasi Penawaran</p>
                        <p class="text-lg font-semibold text-gray-800">{{NAMA_KLIEN}}</p>
                        <p class="text-sm text-gray-500">{{KONTAK_KLIEN}}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm text-gray-600 mb-1">Konsultasi Bisnis</p>
                        <p class="text-lg font-semibold accent-blue">{{SALES_CONTACT}}</p>
                        <p class="text-xs text-gray-500">{{TANGGAL_GENERASI}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def _get_minimalist_home_template(self) -> str:
        """Minimalist home brochure template"""
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimalist Home Brochure</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&family=Raleway:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Source Sans Pro', sans-serif; }
        .font-raleway { font-family: 'Raleway', sans-serif; }
        .minimal-gradient {
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
        }
        .accent-gray { color: #666666; }
        .clean-border { border-color: #e0e0e0; }
    </style>
</head>
<body class="bg-white">
    <!-- A4 Size Container -->
    <div class="w-[210mm] h-[297mm] overflow-hidden">
        
        <!-- Header Section -->
        <div class="h-[20%] minimal-gradient flex items-center justify-center">
            <div class="text-center px-8">
                <h1 class="font-raleway text-2xl font-light text-gray-800 mb-2">{{NAMA_PROPERTI}}</h1>
                <p class="text-sm text-gray-600">{{TAGLINE_MINIMALIS}}</p>
            </div>
        </div>
        
        <!-- Hero Image -->
        <div class="h-[35%] bg-cover bg-center bg-gray-100" style="background-image: url('{{GAMBAR_AI}}');">
        </div>
        
        <!-- Content Section -->
        <div class="h-[45%] p-10">
            <!-- Key Information -->
            <div class="grid grid-cols-3 gap-6 mb-8">
                <div class="text-center">
                    <p class="text-2xl font-light text-gray-800">{{LUAS_BANGUNAN}}m²</p>
                    <p class="text-xs text-gray-500">Luas Bangunan</p>
                </div>
                <div class="text-center">
                    <p class="text-2xl font-light text-gray-800">{{JUMLAH_KAMAR}}</p>
                    <p class="text-xs text-gray-500">Kamar Tidur</p>
                </div>
                <div class="text-center">
                    <p class="text-2xl font-light text-gray-800">Rp {{HARGA_DINAMIS}}</p>
                    <p class="text-xs text-gray-500">Harga</p>
                </div>
            </div>
            
            <!-- Description -->
            <div class="mb-8">
                <h3 class="font-raleway text-lg font-semibold text-gray-800 mb-3">Desain Minimalis</h3>
                <p class="text-sm text-gray-600 leading-relaxed">{{DESKRIPSI_MINIMALIS}}</p>
            </div>
            
            <!-- Features Grid -->
            <div class="grid grid-cols-2 gap-4 mb-8">
                <div class="border clean-border rounded p-4">
                    <h4 class="font-medium text-gray-800 mb-2">Interior</h4>
                    <ul class="space-y-1 text-xs text-gray-600">
                        <li>• {{INTERIOR_1}}</li>
                        <li>• {{INTERIOR_2}}</li>
                        <li>• {{INTERIOR_3}}</li>
                    </ul>
                </div>
                <div class="border clean-border rounded p-4">
                    <h4 class="font-medium text-gray-800 mb-2">Eksterior</h4>
                    <ul class="space-y-1 text-xs text-gray-600">
                        <li>• {{EKSTERIOR_1}}</li>
                        <li>• {{EKSTERIOR_2}}</li>
                        <li>• {{EKSTERIOR_3}}</li>
                    </ul>
                </div>
            </div>
            
            <!-- Contact Information -->
            <div class="border-t clean-border pt-4">
                <div class="flex justify-between items-center text-sm">
                    <div>
                        <p class="text-gray-600">Untuk</p>
                        <p class="font-medium text-gray-800">{{NAMA_KLIEN}}</p>
                        <p class="text-xs text-gray-500">{{KONTAK_KLIEN}}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-gray-600">Hubungi</p>
                        <p class="font-medium accent-gray">{{SALES_CONTACT}}</p>
                        <p class="text-xs text-gray-500">{{TANGGAL_GENERASI}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """

# Convenience function for easy usage
async def generate_premium_brochure(
    template_name: str,
    context_data: Dict[str, Any],
    output_format: str = "pdf",
    filename: Optional[str] = None
) -> str:
    """
    Generate premium brochure with Playwright rendering
    
    Args:
        template_name: Template to use
        context_data: Dynamic data for template
        output_format: 'pdf' or 'jpg'
        filename: Custom filename
    
    Returns:
        Path to generated file
    """
    renderer = PixelPerfectRenderer()
    return await renderer.generate_premium_brochure(
        template_name=template_name,
        context_data=context_data,
        output_format=output_format,
        filename=filename
    )

# Example usage and testing
if __name__ == "__main__":
    async def test_brochure_generation():
        """Test brochure generation with sample data"""
        
        # Sample data for luxury property template
        sample_data = {
            "NAMA_PROPERTI": "The Royal Residence",
            "LOKASI_PREMIUM": "Jakarta Selatan",
            "LUAS_TANAH": "500",
            "LUAS_BANGUNAN": "750",
            "JUMLAH_KAMAR": "5",
            "GAMBAR_AI": "https://via.placeholder.com/1200x800/1a1a1a/ffffff?text=Luxury+Property",
            "FITUR_1": "Private Swimming Pool",
            "FITUR_2": "Smart Home System",
            "FITUR_3": "24/7 Security",
            "FITUR_4": "Rooftop Garden",
            "DESKRIPSI_LOKASI": "Strategis di pusat bisnis Jakarta Selatan dengan akses mudah ke fasilitas premium",
            "AKSES_LOKASI": "Toll Road, MRT Station, International School, Hospital, Shopping Center",
            "HARGA_DINAMIS": "15.000.000.000",
            "HARGA_PER_METER": "20.000.000",
            "NAMA_KLIEN": "Bapak Ahmad Wijaya",
            "KONTAK_KLIEN": "+62 812-3456-7890",
            "TANGGAL_GENERASI": datetime.now().strftime("%d %B %Y")
        }
        
        try:
            # Generate PDF brochure
            pdf_path = await generate_premium_brochure(
                template_name="luxury_property",
                context_data=sample_data,
                output_format="pdf"
            )
            print(f"✅ PDF Generated: {pdf_path}")
            
            # Generate JPG brochure
            jpg_path = await generate_premium_brochure(
                template_name="luxury_property",
                context_data=sample_data,
                output_format="jpg"
            )
            print(f"✅ JPG Generated: {jpg_path}")
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
    
    # Run test
    asyncio.run(test_brochure_generation())
