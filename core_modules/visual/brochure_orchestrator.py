#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎭 BROCHURE ORCHESTRATOR - Modular Assembly System
=================================================

Advanced brochure assembly system combining visual architect, KPR engine, and React-based templates.
Creates multi-page brochures with personalized content and dynamic layouts.

Features:
- Modular 5-page brochure assembly
- React-based HTML templates with TailwindCSS
- SVG floorplan highlighting integration
- Personalized KPR calculations
- QR code generation for tracking
- Playwright rendering for print-ready output
- Dynamic content injection based on lead data
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import base64
import io

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    import qrcode
    from qrcode.image.pil import PilImage
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# Import our custom modules
try:
    from .svg_architect import SVGArchitect, highlight_floorplan
    from ..finance.kpr_engine import KPREngine, ProspectProfile, ProspectType, generate_personalized_pricelist
    CUSTOM_MODULES_AVAILABLE = True
except ImportError:
    CUSTOM_MODULES_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrochureOrchestrator:
    """Advanced modular brochure assembly system"""
    
    def __init__(self, output_dir: str = "data/brochures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize sub-modules
        if CUSTOM_MODULES_AVAILABLE:
            self.svg_architect = SVGArchitect()
            self.kpr_engine = KPREngine()
        else:
            self.svg_architect = None
            self.kpr_engine = None
        
        # QR code settings
        self.base_url = os.getenv('BROCHURE_BASE_URL', 'https://virtualtour.example.com')
        
        # Template configurations
        self.template_configs = {
            'luxury': {
                'theme': 'gold',
                'font_family': 'Playfair Display',
                'primary_color': '#D4AF37',
                'secondary_color': '#1a1a1a',
                'accent_color': '#8B4513'
            },
            'modern': {
                'theme': 'purple',
                'font_family': 'Inter',
                'primary_color': '#667eea',
                'secondary_color': '#764ba2',
                'accent_color': '#f093fb'
            },
            'minimalist': {
                'theme': 'gray',
                'font_family': 'Source Sans Pro',
                'primary_color': '#4a5568',
                'secondary_color': '#718096',
                'accent_color': '#a0aec0'
            },
            'family': {
                'theme': 'blue',
                'font_family': 'Poppins',
                'primary_color': '#3182ce',
                'secondary_color': '#2c5282',
                'accent_color': '#63b3ed'
            }
        }
        
        # Page templates
        self.page_templates = {
            'cover': self._get_cover_template(),
            'hook': self._get_hook_template(),
            'blueprint': self._get_blueprint_template(),
            'investment': self._get_investment_template(),
            'cta': self._get_cta_template()
        }
    
    async def assemble_masterpiece(
        self,
        lead_data: Dict[str, Any],
        campaign_mode: str = "luxury",
        output_format: str = "pdf"
    ) -> str:
        """
        Assemble complete 5-page masterpiece brochure
        
        Args:
            lead_data: Lead information and preferences
            campaign_mode: Campaign theme (luxury, modern, minimalist, family)
            output_format: Output format (pdf, png)
        
        Returns:
            Path to generated brochure
        """
        try:
            logger.info(f"🎭 Assembling masterpiece brochure for {lead_data.get('name', 'Unknown')}")
            logger.info(f"🎨 Campaign mode: {campaign_mode}")
            
            # Validate dependencies
            if not PLAYWRIGHT_AVAILABLE:
                raise ImportError("Playwright not available. Install with: pip install playwright")
            
            # Get template configuration
            template_config = self.template_configs.get(campaign_mode, self.template_configs['luxury'])
            
            # Prepare content for each page
            page_contents = await self._prepare_page_contents(lead_data, campaign_mode, template_config)
            
            # Generate complete HTML
            complete_html = self._assemble_complete_html(page_contents, template_config)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            lead_name = lead_data.get('name', 'unknown').replace(' ', '_').lower()
            filename = f"masterpiece_{lead_name}_{campaign_mode}_{timestamp}.{output_format}"
            output_path = self.output_dir / filename
            
            # Render to PDF/PNG using Playwright
            await self._render_brochure(complete_html, output_path, output_format)
            
            logger.info(f"✅ Masterpiece brochure assembled: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Brochure assembly failed: {e}")
            raise
    
    async def _prepare_page_contents(
        self,
        lead_data: Dict[str, Any],
        campaign_mode: str,
        template_config: Dict[str, Any]
    ) -> Dict[str, str]:
        """Prepare content for each page"""
        try:
            page_contents = {}
            
            # Page 1: Cover
            page_contents['cover'] = await self._prepare_cover_content(lead_data, template_config)
            
            # Page 2: Hook (Marketing copy)
            page_contents['hook'] = await self._prepare_hook_content(lead_data, campaign_mode, template_config)
            
            # Page 3: Blueprint (Floorplan)
            page_contents['blueprint'] = await self._prepare_blueprint_content(lead_data, campaign_mode, template_config)
            
            # Page 4: Investment (KPR calculations)
            page_contents['investment'] = await self._prepare_investment_content(lead_data, template_config)
            
            # Page 5: Call to Action (QR code)
            page_contents['cta'] = await self._prepare_cta_content(lead_data, template_config)
            
            return page_contents
            
        except Exception as e:
            logger.error(f"❌ Page content preparation failed: {e}")
            raise
    
    async def _prepare_cover_content(self, lead_data: Dict[str, Any], template_config: Dict[str, Any]) -> str:
        """Prepare cover page content"""
        try:
            client_name = lead_data.get('name', 'Calon Pembeli')
            property_name = lead_data.get('property_name', 'Properti Eksklusif')
            property_image = lead_data.get('property_image', 'https://via.placeholder.com/800x600')
            
            cover_html = f"""
            <div class="cover-page" style="background: linear-gradient(135deg, {template_config['primary_color']}22 0%, {template_config['secondary_color']}22 100%); min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px; position: relative;">
                <div class="cover-content" style="text-align: center; max-width: 800px;">
                    <div class="property-image" style="margin-bottom: 40px;">
                        <img src="{property_image}" alt="{property_name}" style="width: 100%; max-width: 600px; height: 300px; object-fit: cover; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
                    </div>
                    <h1 class="property-name" style="font-family: '{template_config['font_family']}', serif; font-size: 3.5rem; font-weight: 700; color: {template_config['primary_color']}; margin-bottom: 20px; line-height: 1.2;">
                        {property_name}
                    </h1>
                    <div class="client-name" style="font-size: 1.8rem; color: {template_config['secondary_color']}; margin-bottom: 10px; font-weight: 300;">
                        Khusus Untuk
                    </div>
                    <div class="client-highlight" style="font-size: 2.5rem; font-weight: 600; color: {template_config['primary_color']}; margin-bottom: 40px;">
                        {client_name}
                    </div>
                    <div class="tagline" style="font-size: 1.2rem; color: {template_config['accent_color']}; font-style: italic;">
                        {self._get_tagline_for_client(lead_data)}
                    </div>
                </div>
                <div class="cover-footer" style="position: absolute; bottom: 40px; left: 0; right: 0; text-align: center; color: {template_config['secondary_color']}; font-size: 0.9rem;">
                    <div>Generated: {datetime.now().strftime('%d %B %Y')}</div>
                </div>
            </div>
            """
            
            return cover_html
            
        except Exception as e:
            logger.error(f"❌ Cover content preparation failed: {e}")
            raise
    
    async def _prepare_hook_content(self, lead_data: Dict[str, Any], campaign_mode: str, template_config: Dict[str, Any]) -> str:
        """Prepare hook page content (marketing copy)"""
        try:
            # Get marketing copy based on campaign mode
            marketing_copy = self._get_marketing_copy(campaign_mode, lead_data)
            
            hook_html = f"""
            <div class="hook-page" style="min-height: 100vh; padding: 80px 60px; background: white; display: flex; flex-direction: column; justify-content: center;">
                <div class="hook-content" style="max-width: 800px; margin: 0 auto;">
                    <h2 class="hook-title" style="font-family: '{template_config['font_family']}', serif; font-size: 2.5rem; font-weight: 700; color: {template_config['primary_color']}; margin-bottom: 40px; text-align: center;">
                        Mengapa Ini Pilihan Tepat Untuk Anda?
                    </h2>
                    <div class="marketing-copy" style="font-size: 1.2rem; line-height: 1.8; color: {template_config['secondary_color']}; text-align: justify; margin-bottom: 40px;">
                        {marketing_copy}
                    </div>
                    <div class="key-benefits" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 30px; margin-bottom: 40px;">
                        {self._generate_benefit_cards(lead_data, template_config)}
                    </div>
                    <div class="testimonial" style="background: {template_config['primary_color']}11; padding: 30px; border-radius: 12px; border-left: 4px solid {template_config['primary_color']}; font-style: italic;">
                        "{self._generate_testimonial(lead_data)}"
                    </div>
                </div>
            </div>
            """
            
            return hook_html
            
        except Exception as e:
            logger.error(f"❌ Hook content preparation failed: {e}")
            raise
    
    async def _prepare_blueprint_content(self, lead_data: Dict[str, Any], campaign_mode: str, template_config: Dict[str, Any]) -> str:
        """Prepare blueprint page content (floorplan)"""
        try:
            # Generate highlighted floorplan if SVG architect is available
            floorplan_image = None
            if self.svg_architect and lead_data.get('floorplan_svg'):
                try:
                    focus_area = self._determine_focus_area(lead_data)
                    floorplan_path = self.svg_architect.highlight_floorplan(
                        base_svg_path=lead_data['floorplan_svg'],
                        focus_area=focus_area,
                        output_format="png"
                    )
                    floorplan_image = floorplan_path
                except Exception as e:
                    logger.warning(f"⚠️ Floorplan highlighting failed: {e}")
            
            # Generate floorplan HTML
            blueprint_html = f"""
            <div class="blueprint-page" style="min-height: 100vh; padding: 80px 60px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); display: flex; flex-direction: column; justify-content: center;">
                <div class="blueprint-content" style="max-width: 900px; margin: 0 auto;">
                    <h2 class="blueprint-title" style="font-family: '{template_config['font_family']}', serif; font-size: 2.5rem; font-weight: 700; color: {template_config['primary_color']}; margin-bottom: 40px; text-align: center;">
                        Denah Ideal Untuk {self._get_focus_area_display(lead_data)}
                    </h2>
                    <div class="floorplan-container" style="text-align: center; margin-bottom: 40px;">
                        {self._generate_floorplan_display(floorplan_image, template_config)}
                    </div>
                    <div class="specifications" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        {self._generate_specification_cards(lead_data, template_config)}
                    </div>
                </div>
            </div>
            """
            
            return blueprint_html
            
        except Exception as e:
            logger.error(f"❌ Blueprint content preparation failed: {e}")
            raise
    
    async def _prepare_investment_content(self, lead_data: Dict[str, Any], template_config: Dict[str, Any]) -> str:
        """Prepare investment page content (KPR calculations)"""
        try:
            # Generate KPR calculations if KPR engine is available
            kpr_data = None
            if self.kpr_engine and lead_data.get('property_price') and lead_data.get('prospect_profile'):
                try:
                    prospect_profile = self._create_prospect_profile(lead_data['prospect_profile'])
                    kpr_data = generate_personalized_pricelist(
                        property_price=lead_data['property_price'],
                        prospect_profile=prospect_profile
                    )
                except Exception as e:
                    logger.warning(f"⚠️ KPR calculation failed: {e}")
            
            # Generate investment HTML
            investment_html = f"""
            <div class="investment-page" style="min-height: 100vh; padding: 80px 60px; background: white; display: flex; flex-direction: column; justify-content: center;">
                <div class="investment-content" style="max-width: 900px; margin: 0 auto;">
                    <h2 class="investment-title" style="font-family: '{template_config['font_family']}', serif; font-size: 2.5rem; font-weight: 700; color: {template_config['primary_color']}; margin-bottom: 40px; text-align: center;">
                        Investasi Paling Cermat Untuk Masa Depan
                    </h2>
                    <div class="kpr-calculations" style="margin-bottom: 40px;">
                        {self._generate_kpr_display(kpr_data, template_config)}
                    </div>
                    <div class="investment-highlights" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                        {self._generate_investment_cards(lead_data, template_config)}
                    </div>
                </div>
            </div>
            """
            
            return investment_html
            
        except Exception as e:
            logger.error(f"❌ Investment content preparation failed: {e}")
            raise
    
    async def _prepare_cta_content(self, lead_data: Dict[str, Any], template_config: Dict[str, Any]) -> str:
        """Prepare call-to-action page content (QR code)"""
        try:
            # Generate QR code if available
            qr_code_data = None
            if QR_AVAILABLE:
                try:
                    qr_code_data = self._generate_qr_code(lead_data)
                except Exception as e:
                    logger.warning(f"⚠️ QR code generation failed: {e}")
            
            # Generate CTA HTML
            cta_html = f"""
            <div class="cta-page" style="min-height: 100vh; padding: 80px 60px; background: linear-gradient(135deg, {template_config['primary_color']}22 0%, {template_config['secondary_color']}22 100%); display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div class="cta-content" style="text-align: center; max-width: 600px;">
                    <h2 class="cta-title" style="font-family: '{template_config['font_family']}', serif; font-size: 2.5rem; font-weight: 700; color: {template_config['primary_color']}; margin-bottom: 40px;">
                        Langkah Selanjutnya
                    </h2>
                    <div class="qr-container" style="margin-bottom: 40px;">
                        {self._generate_qr_display(qr_code_data, template_config)}
                    </div>
                    <div class="cta-instructions" style="font-size: 1.2rem; line-height: 1.6; color: {template_config['secondary_color']}; margin-bottom: 30px;">
                        <p>Scan QR code untuk memulai Virtual Tour 360°</p>
                        <p style="font-size: 1rem; margin-top: 20px;">Atau hubungi kami langsung:</p>
                    </div>
                    <div class="contact-info" style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                        <div class="phone" style="font-size: 1.5rem; font-weight: 600; color: {template_config['primary_color']}; margin-bottom: 10px;">
                            📞 {os.getenv('SALES_CONTACT', '+62 812-3456-7890')}
                        </div>
                        <div class="email" style="font-size: 1.1rem; color: {template_config['secondary_color']};">
                            📧 {os.getenv('SALES_EMAIL', 'sales@property.com')}
                        </div>
                    </div>
                </div>
            </div>
            """
            
            return cta_html
            
        except Exception as e:
            logger.error(f"❌ CTA content preparation failed: {e}")
            raise
    
    def _assemble_complete_html(self, page_contents: Dict[str, str], template_config: Dict[str, Any]) -> str:
        """Assemble complete HTML with all pages"""
        try:
            html_template = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Masterpiece Brochure</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family={template_config['font_family'].replace(' ', '+')}:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: '{template_config['font_family']}', sans-serif;
            margin: 0;
            padding: 0;
            color: {template_config['secondary_color']};
        }}
        .page {{
            width: 210mm;
            height: 297mm;
            page-break-after: always;
            position: relative;
            overflow: hidden;
        }}
        @media print {{
            .page {{
                page-break-after: always;
            }}
        }}
        .highlight-area {{
            color: {template_config['primary_color']};
            font-weight: 600;
        }}
        .accent-text {{
            color: {template_config['accent_color']};
        }}
    </style>
</head>
<body>
    <div class="page">
        {page_contents.get('cover', '')}
    </div>
    <div class="page">
        {page_contents.get('hook', '')}
    </div>
    <div class="page">
        {page_contents.get('blueprint', '')}
    </div>
    <div class="page">
        {page_contents.get('investment', '')}
    </div>
    <div class="page">
        {page_contents.get('cta', '')}
    </div>
</body>
</html>
            """
            
            return html_template
            
        except Exception as e:
            logger.error(f"❌ HTML assembly failed: {e}")
            raise
    
    async def _render_brochure(self, html_content: str, output_path: Path, output_format: str):
        """Render brochure to PDF/PNG using Playwright"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1200, 'height': 1600},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()
                
                # Set content and wait for loading
                await page.set_content(html_content, wait_until='networkidle')
                
                # Generate output
                if output_format.lower() == 'pdf':
                    await page.pdf(
                        path=str(output_path),
                        format='A4',
                        print_background=True,
                        margin={'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
                        scale=1.0,
                        prefer_css_page_size=True
                    )
                elif output_format.lower() in ['jpg', 'jpeg', 'png']:
                    await page.screenshot(
                        path=str(output_path),
                        full_page=True,
                        type='png'
                    )
                
                await context.close()
                await browser.close()
                
        except Exception as e:
            logger.error(f"❌ Brochure rendering failed: {e}")
            raise
    
    def _generate_qr_code(self, lead_data: Dict[str, Any]) -> Optional[str]:
        """Generate QR code for virtual tour"""
        try:
            if not QR_AVAILABLE:
                return None
            
            # Create unique URL with lead ID
            lead_id = lead_data.get('id', 'unknown')
            virtual_tour_url = f"{self.base_url}/tour/{lead_id}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(virtual_tour_url)
            qr.make(fit=True)
            
            # Convert to base64 for HTML embedding
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error(f"❌ QR code generation failed: {e}")
            return None
    
    def _determine_focus_area(self, lead_data: Dict[str, Any]) -> str:
        """Determine focus area for floorplan highlighting"""
        age = lead_data.get('age', 35)
        family_size = lead_data.get('family_size', 4)
        prospect_type = lead_data.get('prospect_type', 'upgrader')
        
        if age >= 60:
            return 'ELDERLY'
        elif family_size >= 4:
            return 'FAMILY'
        elif prospect_type == 'investor':
            return 'INVESTOR'
        elif age <= 35:
            return 'YOUNG'
        else:
            return 'FAMILY'
    
    def _get_tagline_for_client(self, lead_data: Dict[str, Any]) -> str:
        """Get personalized tagline for client"""
        age = lead_data.get('age', 35)
        family_size = lead_data.get('family_size', 4)
        
        if age >= 60:
            return "Kenyamanan dan Ketentraman di Masa Pensiun"
        elif family_size >= 4:
            return "Rumah Impian untuk Keluarga Bahagia"
        elif age <= 35:
            return "Investasi Cerdas untuk Masa Depan Gemilang"
        else:
            return "Elevasi Gaya Hidup Anda ke Level Berikutnya"
    
    def _get_marketing_copy(self, campaign_mode: str, lead_data: Dict[str, Any]) -> str:
        """Get marketing copy based on campaign mode"""
        client_name = lead_data.get('name', 'Anda')
        
        marketing_copies = {
            'luxury': f"""
            <p>Hai {client_name}, kami memahami bahwa Anda mencari lebih dari sekadar rumah - Anda mencari simbol status dan kebanggaan. Properti eksklusif ini dirancang untuk memberikan pengalaman hidup yang tak tertandingi dengan fasilitas kelas dunia dan lokasi premium.</p>
            <p>Dengan arsitektur yang memukau dan finishing yang sempurna, setiap detail dirancang untuk memenuhi standar tertinggi Anda. Ini bukan hanya tentang memiliki properti, tapi tentang memiliki warisan yang akan dihargai dari generasi ke generasi.</p>
            """,
            'modern': f"""
            <p>Hai {client_name}, di era modern ini, Anda membutuhkan rumah yang tidak hanya nyaman tapi juga cerdas. Properti ini menggabungkan teknologi terkini dengan desain minimalis yang fungsional, menciptakan ruang hidup yang inspiratif dan efisien.</p>
            <p>Dilengkapi dengan smart home system, area kerja yang produktif, dan fasilitas rekreasi yang modern, rumah ini dirancang untuk mendukung gaya hidup dinamis Anda. Ini adalah investasi untuk masa depan digital Anda.</p>
            """,
            'family': f"""
            <p>Hai {client_name}, keluarga adalah segalanya. Kami merancang rumah ini dengan pemahaman mendalam tentang kebutuhan keluarga modern - ruang yang aman untuk anak-anak bermain, area berkumpul yang nyaman, dan privasi untuk orang tua.</p>
            <p>Lokasi strategis dekat sekolah berkualitas, taman bermain, dan fasilitas kesehatan membuat rumah ini menjadi pilihan sempurna untuk pertumbuhan keluarga Anda. Ini adalah tempat kenangan indah akan dibuat.</p>
            """,
            'minimalist': f"""
            <p>Hai {client_name}, dalam kesederhanaan terdapat keindahan. Rumah ini menawarkan desain minimalis yang elegan dengan fokus pada fungsi dan kenyamanan. Setiap ruang dioptimalkan untuk memberikan maksimal kegunaan tanpa mengorbankan estetika.</p>
            <p>Dengan material berkualitas dan tata letak yang cerdas, rumah ini menjadi tempat perlindungan sempurna dari hiruk pikuk dunia luar. Ini adalah oasis ketenangan di tengah kesibukan urban.</p>
            """
        }
        
        return marketing_copies.get(campaign_mode, marketing_copies['luxury'])
    
    def _generate_benefit_cards(self, lead_data: Dict[str, Any], template_config: Dict[str, Any]) -> str:
        """Generate benefit cards for hook page"""
        benefits = [
            ("Lokasi Premium", "Strategis di pusat kota dengan akses mudah ke fasilitas utama"),
            ("Investasi Cerdas", "Nilai properti yang terus meningkat dengan potensi capital gain tinggi"),
            ("Fasilitas Lengkap", "Kolam renang, gym, dan area rekreasi untuk kenyamanan maksimal"),
            ("Keamanan 24/7", "Sistem keamanan modern dengan CCTV dan petugas keamanan berpengalaman")
        ]
        
        cards_html = ""
        for title, description in benefits:
            cards_html += f"""
            <div class="benefit-card" style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 3px solid {template_config['primary_color']};">
                <h3 class="benefit-title" style="font-size: 1.2rem; font-weight: 600; color: {template_config['primary_color']}; margin-bottom: 10px;">
                    {title}
                </h3>
                <p class="benefit-description" style="font-size: 0.95rem; color: {template_config['secondary_color']}; line-height: 1.5;">
                    {description}
                </p>
            </div>
            """
        
        return cards_html
    
    def _generate_testimonial(self, lead_data: Dict[str, Any]) -> str:
        """Generate personalized testimonial"""
        client_name = lead_data.get('name', 'Pembeli')
        
        testimonials = [
            f"Ini adalah keputusan terbaik yang pernah saya buat. Rumah ini melampaui semua ekspektasi saya dan memberikan kualitas hidup yang jauh lebih baik. - {client_name}",
            f"Saya sangat puas dengan investasi ini. Lokasinya sempurna dan fasilitasnya luar biasa. Direkomendasikan untuk siapa pun yang mencari properti berkualitas. - {client_name}",
            f"Dari awal saya tahu ini adalah rumah yang tepat untuk saya. Proses pembelian lancar dan tim sangat membantu. - {client_name}"
        ]
        
        import random
        return random.choice(testimonials)
    
    def _generate_floorplan_display(self, floorplan_image: Optional[str], template_config: Dict[str, Any]) -> str:
        """Generate floorplan display HTML"""
        if floorplan_image and Path(floorplan_image).exists():
            return f'<img src="{floorplan_image}" alt="Floorplan" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">'
        else:
            return f'<div style="background: {template_config["primary_color"]}22; padding: 60px; border-radius: 12px; text-align: center; color: {template_config["secondary_color"]};">Floorplan akan ditampilkan di sini</div>'
    
    def _generate_specification_cards(self, lead_data: Dict[str, Any], template_config: Dict[str, Any]) -> str:
        """Generate specification cards"""
        specifications = [
            ("Luas Tanah", f"{lead_data.get('land_area', '200')} m²"),
            ("Luas Bangunan", f"{lead_data.get('building_area', '150')} m²"),
            ("Kamar Tidur", f"{lead_data.get('bedrooms', '3')} + 1"),
            ("Kamar Mandi", f"{lead_data.get('bathrooms', '2')}"),
            ("Garasi", f"{lead_data.get('garage', '2')} Mobil"),
            ("Listrik", f"{lead_data.get('electricity', '2200')} Watt")
        ]
        
        cards_html = ""
        for label, value in specifications:
            cards_html += f"""
            <div class="spec-card" style="background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                <div class="spec-label" style="font-size: 0.9rem; color: {template_config['accent_color']}; margin-bottom: 5px;">
                    {label}
                </div>
                <div class="spec-value" style="font-size: 1.3rem; font-weight: 600; color: {template_config['primary_color']};">
                    {value}
                </div>
            </div>
            """
        
        return cards_html
    
    def _get_focus_area_display(self, lead_data: Dict[str, Any]) -> str:
        """Get focus area display name"""
        focus_area = self._determine_focus_area(lead_data)
        displays = {
            'ELDERLY': 'Lansia',
            'FAMILY': 'Keluarga',
            'INVESTOR': 'Investor',
            'YOUNG': 'Profesional Muda'
        }
        return displays.get(focus_area, 'Keluarga')
    
    def _generate_kpr_display(self, kpr_data: Optional[Dict[str, Any]], template_config: Dict[str, Any]) -> str:
        """Generate KPR calculation display"""
        if not kpr_data or not kpr_data.get('options'):
            return '<div style="text-align: center; padding: 40px;">Kalkulasi KPR akan ditampilkan di sini</div>'
        
        best_option = kpr_data['options'][0]
        best_payment = best_option['best_option']
        
        return f"""
        <div class="kpr-summary" style="background: {template_config['primary_color']}11; padding: 30px; border-radius: 12px; margin-bottom: 30px;">
            <h3 style="font-size: 1.5rem; font-weight: 600; color: {template_config['primary_color']}; margin-bottom: 20px; text-align: center;">
                Opsi KPR Terbaik: {best_option['bank']}
            </h3>
            <div class="kpr-details" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; text-align: center;">
                <div>
                    <div class="detail-label" style="font-size: 0.9rem; color: {template_config['accent_color']}; margin-bottom: 5px;">DP</div>
                    <div class="detail-value" style="font-size: 1.2rem; font-weight: 600; color: {template_config['primary_color']};">Rp {best_option['down_payment_amount']:,.0f}</div>
                </div>
                <div>
                    <div class="detail-label" style="font-size: 0.9rem; color: {template_config['accent_color']}; margin-bottom: 5px;">Cicilan/Bulan</div>
                    <div class="detail-value" style="font-size: 1.2rem; font-weight: 600; color: {template_config['primary_color']};">Rp {best_payment['monthly_payment']:,.0f}</div>
                </div>
                <div>
                    <div class="detail-label" style="font-size: 0.9rem; color: {template_config['accent_color']}; margin-bottom: 5px;">Tenor</div>
                    <div class="detail-value" style="font-size: 1.2rem; font-weight: 600; color: {template_config['primary_color']};">{best_option['loan_term_years']} Tahun</div>
                </div>
                <div>
                    <div class="detail-label" style="font-size: 0.9rem; color: {template_config['accent_color']}; margin-bottom: 5px;">Skor Terjangkau</div>
                    <div class="detail-value" style="font-size: 1.2rem; font-weight: 600; color: {template_config['primary_color']};">{best_option['affordability_score']:.0f}/100</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_investment_cards(self, lead_data: Dict[str, Any], template_config: Dict[str, Any]) -> str:
        """Generate investment highlight cards"""
        investments = [
            ("Potensi Kenaikan", "8-12% per tahun berdasarkan lokasi strategis"),
            ("Rental Yield", "4-6% per tahun untuk passive income"),
            ("Capital Gain", "Potensi keuntungan 20% dalam 3 tahun"),
            ("Liquidity", "Mudah dijual kembali dengan harga kompetitif")
        ]
        
        cards_html = ""
        for title, description in investments:
            cards_html += f"""
            <div class="investment-card" style="background: linear-gradient(135deg, {template_config['primary_color']}22 0%, {template_config['secondary_color']}22 100%); padding: 25px; border-radius: 12px; text-align: center;">
                <h3 class="investment-title" style="font-size: 1.1rem; font-weight: 600; color: {template_config['primary_color']}; margin-bottom: 10px;">
                    {title}
                </h3>
                <p class="investment-description" style="font-size: 0.9rem; color: {template_config['secondary_color']}; line-height: 1.4;">
                    {description}
                </p>
            </div>
            """
        
        return cards_html
    
    def _generate_qr_display(self, qr_code_data: Optional[str], template_config: Dict[str, Any]) -> str:
        """Generate QR code display"""
        if qr_code_data:
            return f'<img src="{qr_code_data}" alt="Virtual Tour QR" style="width: 200px; height: 200px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">'
        else:
            return f'<div style="background: {template_config["primary_color"]}22; padding: 100px; border-radius: 12px; text-align: center; color: {template_config["secondary_color"]};">QR Code akan ditampilkan di sini</div>'
    
    def _create_prospect_profile(self, profile_data: Dict[str, Any]) -> ProspectProfile:
        """Create prospect profile from data"""
        return ProspectProfile(
            age=profile_data.get('age', 35),
            monthly_income=profile_data.get('monthly_income', 15000000),
            employment_type=profile_data.get('employment_type', 'permanent'),
            credit_score=profile_data.get('credit_score', 750),
            existing_loans=profile_data.get('existing_loans', 0),
            family_size=profile_data.get('family_size', 4),
            prospect_type=ProspectType(profile_data.get('prospect_type', 'upgrader'))
        )
    
    # Template methods (simplified for brevity)
    def _get_cover_template(self) -> str:
        return "Cover template"
    
    def _get_hook_template(self) -> str:
        return "Hook template"
    
    def _get_blueprint_template(self) -> str:
        return "Blueprint template"
    
    def _get_investment_template(self) -> str:
        return "Investment template"
    
    def _get_cta_template(self) -> str:
        return "CTA template"

# Convenience function for easy usage
async def assemble_masterpiece(
    lead_data: Dict[str, Any],
    campaign_mode: str = "luxury",
    output_format: str = "pdf"
) -> str:
    """
    Assemble complete masterpiece brochure
    
    Args:
        lead_data: Lead information and preferences
        campaign_mode: Campaign theme (luxury, modern, minimalist, family)
        output_format: Output format (pdf, png)
    
    Returns:
        Path to generated brochure
    """
    orchestrator = BrochureOrchestrator()
    return await orchestrator.assemble_masterpiece(lead_data, campaign_mode, output_format)

# Example usage and testing
if __name__ == "__main__":
    async def test_brochure_orchestrator():
        """Test brochure orchestrator functionality"""
        
        # Sample lead data
        sample_lead = {
            'id': 'lead_12345',
            'name': 'Ahmad Wijaya',
            'age': 35,
            'family_size': 4,
            'property_name': 'The Royal Residence',
            'property_price': 800000000,
            'property_image': 'https://via.placeholder.com/800x600/333333/ffffff?text=Luxury+Property',
            'floorplan_svg': None,  # Would be path to SVG file
            'prospect_profile': {
                'age': 35,
                'monthly_income': 15000000,
                'employment_type': 'permanent',
                'credit_score': 750,
                'existing_loans': 2000000,
                'family_size': 4,
                'prospect_type': 'upgrader'
            }
        }
        
        try:
            # Test brochure assembly
            brochure_path = await assemble_masterpiece(
                lead_data=sample_lead,
                campaign_mode="luxury",
                output_format="pdf"
            )
            
            print(f"✅ Masterpiece brochure assembled: {brochure_path}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Run test
    asyncio.run(test_brochure_orchestrator())
