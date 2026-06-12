"""
PDF Creator Module - Professional PDF Generation with Puppeteer/WeasyPrint
Enterprise PDF generation for Lumina OS Visual Engine
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import tempfile
import subprocess
import json
from jinja2 import Template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFCreator:
    """Professional PDF creation with Puppeteer and WeasyPrint"""
    
    def __init__(self):
        """Initialize PDF creator"""
        self.logger = logging.getLogger(__name__)
        self.templates_dir = Path(__file__).parent.parent / 'templates'
        self.output_dir = Path(__file__).parent.parent / 'output' / 'pdfs'
        
        # Ensure directories exist
        self.templates_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for Puppeteer
        self.puppeteer_available = self._check_puppeteer()
        self.weasyprint_available = self._check_weasyprint()
    
    def _check_puppeteer(self) -> bool:
        """Check if Puppeteer is available"""
        try:
            result = subprocess.run(['puppeteer', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info("✅ Puppeteer is available")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        logger.warning("⚠️ Puppeteer not found, will use WeasyPrint fallback")
        return False
    
    def _check_weasyprint(self) -> bool:
        """Check if WeasyPrint is available"""
        try:
            import weasyprint
            logger.info("✅ WeasyPrint is available")
            return True
        except ImportError:
            logger.warning("⚠️ WeasyPrint not found, attempting to install...")
            try:
                subprocess.run(['pip', 'install', 'weasyprint'], 
                              check=True, capture_output=True)
                import weasyprint
                logger.info("✅ WeasyPrint installed successfully")
                return True
            except subprocess.CalledProcessError:
                logger.error("❌ Failed to install WeasyPrint")
                return False
    
    async def create_brochure_pdf(
        self,
        template_data: Dict[str, Any],
        output_filename: str,
        template_name: str = 'davinci_brochure',
        use_puppeteer: bool = True,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create PDF brochure from template
        
        Args:
            template_data: Data for template rendering
            output_filename: Output PDF filename
            template_name: Template name (without extension)
            use_puppeteer: Whether to use Puppeteer (fallback to WeasyPrint)
            options: Additional PDF options
        
        Returns:
            Dictionary with creation results
        """
        try:
            # Prepare output path
            output_path = self.output_dir / output_filename
            
            # Render template
            html_content = await self._render_template(template_name, template_data)
            
            if use_puppeteer and self.puppeteer_available:
                result = await self._create_with_puppeteer(html_content, output_path, options)
            else:
                result = await self._create_with_weasyprint(html_content, output_path, options)
            
            if result['success']:
                logger.info(f"✅ PDF created: {output_path}")
                return {
                    'success': True,
                    'output_path': str(output_path),
                    'file_size': os.path.getsize(output_path),
                    'method': result['method']
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Error creating PDF: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """Render HTML template with data"""
        try:
            template_path = self.templates_dir / f"{template_name}.html"
            
            if not template_path.exists():
                # Create default template
                await self._create_default_template(template_name)
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            template = Template(template_content)
            rendered_html = template.render(**data)
            
            return rendered_html
            
        except Exception as e:
            logger.error(f"❌ Error rendering template: {e}")
            raise
    
    async def _create_default_template(self, template_name: str):
        """Create default HTML template"""
        try:
            if template_name == 'davinci_brochure':
                html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 20px;
        }
        
        .content {
            margin-bottom: 40px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        
        .property-details {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        .detail-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .detail-row:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .detail-label {
            font-weight: bold;
            color: #495057;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
        }
        
        .feature-item {
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .feature-item:last-child {
            border-bottom: none;
        }
        
        .feature-icon {
            color: #27ae60;
            margin-right: 10px;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .qr-code {
            width: 150px;
            height: 150px;
            background: white;
            border: 2px solid #3498db;
            border-radius: 8px;
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #7f8c8d;
        }
        
        @media print {
            body {
                background: white;
            }
            
            .container {
                box-shadow: none;
                border-radius: 0;
            }
            
            .qr-code {
                border: 1px solid #333;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{{ title }}</h1>
            <p class="subtitle">{{ subtitle }}</p>
        </div>
        
        <div class="content">
            {% if property_details %}
            <div class="section">
                <h2 class="section-title">Property Details</h2>
                <div class="property-details">
                    <div class="detail-row">
                        <span class="detail-label">Type:</span>
                        <span>{{ property_details.type }}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Size:</span>
                        <span>{{ property_details.size }}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Bedrooms:</span>
                        <span>{{ property_details.bedrooms }}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Bathrooms:</span>
                        <span>{{ property_details.bathrooms }}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span>{{ property_details.price }}</span>
                    </div>
                </div>
            </div>
            {% endif %}
            
            {% if features %}
            <div class="section">
                <h2 class="section-title">Features & Amenities</h2>
                <ul class="feature-list">
                    {% for feature in features %}
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        {{ feature }}
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            {% if description %}
            <div class="section">
                <h2 class="section-title">Description</h2>
                <p>{{ description }}</p>
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Generated by Lumina OS Enterprise</p>
            <p>{{ generation_date }}</p>
            {% if qr_code_url %}
            <div class="qr-code">
                <div>QR Code</div>
                <div>{{ qr_code_url }}</div>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
                """
            else:
                # Create generic template
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{template_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>{template_name}</h1>
    <div>{{ data | safe }}</div>
</body>
</html>
                """
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Created default template: {template_name}")
            
        except Exception as e:
            logger.error(f"❌ Error creating default template: {e}")
            raise
    
    async def _create_with_puppeteer(
        self, 
        html_content: str, 
        output_path: Path, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create PDF using Puppeteer"""
        try:
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_file:
                temp_file.write(html_content)
                temp_path = temp_file.name
            
            # Puppeteer command
            cmd = [
                'puppeteer',
                'print-to-pdf',
                '--no-sandbox',
                '--disable-web-security',
                '--format=A4',
                '--margin-top=20mm',
                '--margin-right=20mm',
                '--margin-bottom=20mm',
                '--margin-left=20mm',
                temp_path,
                str(output_path)
            ]
            
            # Add custom options
            if options:
                if options.get('landscape'):
                    cmd.insert(-1, '--landscape')
                if options.get('background'):
                    cmd.insert(-1, f'--background={options["background"]}')
            
            # Execute Puppeteer
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'method': 'puppeteer',
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'method': 'puppeteer',
                    'error': result.stderr
                }
                
        except Exception as e:
            logger.error(f"❌ Error creating PDF with Puppeteer: {e}")
            return {
                'success': False,
                'method': 'puppeteer',
                'error': str(e)
            }
    
    async def _create_with_weasyprint(
        self, 
        html_content: str, 
        output_path: Path, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create PDF using WeasyPrint"""
        try:
            import weasyprint
            
            # CSS for print optimization
            css = """
            @page {
                size: A4;
                margin: 2cm;
                @bottom-center;
                @top-center;
            }
            
            body {
                font-family: Georgia, serif;
                line-height: 1.6;
            }
            
            h1, h2, h3 {
                color: #2c3e50;
                page-break-after: avoid;
            }
            
            .no-print {
                display: none;
            }
            """
            
            # Convert HTML to PDF
            pdf = weasyprint.HTML(string=html_content, base_url='file:///')
            pdf.write_pdf(str(output_path), styles=[css])
            
            return {
                'success': True,
                'method': 'weasyprint',
                'file_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating PDF with WeasyPrint: {e}")
            return {
                'success': False,
                'method': 'weasyprint',
                'error': str(e)
            }
    
    async def create_multiple_pdfs(
        self,
        pdf_requests: List[Dict[str, Any]],
        concurrent: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create multiple PDFs concurrently
        
        Args:
            pdf_requests: List of PDF creation requests
            concurrent: Whether to process concurrently
        
        Returns:
            List of creation results
        """
        if concurrent:
            tasks = []
            for request in pdf_requests:
                task = self.create_brochure_pdf(
                    template_data=request['template_data'],
                    output_filename=request['output_filename'],
                    template_name=request.get('template_name', 'davinci_brochure'),
                    use_puppeteer=request.get('use_puppeteer', True),
                    options=request.get('options')
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        else:
            results = []
            for request in pdf_requests:
                result = await self.create_brochure_pdf(
                    template_data=request['template_data'],
                    output_filename=request['output_filename'],
                    template_name=request.get('template_name', 'davinci_brochure'),
                    use_puppeteer=request.get('use_puppeteer', True),
                    options=request.get('options')
                )
                results.append(result)
        
        return results
    
    async def get_pdf_info(self, pdf_path: str) -> Dict[str, Any]:
        """Get PDF file information"""
        try:
            path = Path(pdf_path)
            if not path.exists():
                return {
                    'exists': False,
                    'error': 'File not found'
                }
            
            stat = path.stat()
            return {
                'exists': True,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'path': str(path)
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting PDF info: {e}")
            return {
                'exists': False,
                'error': str(e)
            }
    
    def list_templates(self) -> List[str]:
        """List available PDF templates"""
        try:
            templates = []
            for file in self.templates_dir.glob('*.html'):
                templates.append(file.stem)
            return sorted(templates)
            
        except Exception as e:
            logger.error(f"❌ Error listing templates: {e}")
            return []
    
    def list_pdfs(self) -> List[str]:
        """List generated PDFs"""
        try:
            pdfs = []
            for file in self.output_dir.glob('*.pdf'):
                pdfs.append(file.name)
            return sorted(pdfs)
            
        except Exception as e:
            logger.error(f"❌ Error listing PDFs: {e}")
            return []

# Global PDF creator instance
pdf_creator = PDFCreator()

# Convenience functions
async def create_brochure(template_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
    """Convenience function to create brochure PDF"""
    return await pdf_creator.create_brochure_pdf(
        template_data=template_data,
        output_filename=filename,
        template_name='davinci_brochure'
    )

async def create_multiple_brochures(pdf_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convenience function to create multiple brochures"""
    return await pdf_creator.create_multiple_pdfs(pdf_requests)

if __name__ == "__main__":
    # Test PDF creation
    async def test_pdf_creation():
        # Sample data
        template_data = {
            'title': 'Luxury Villa - Serang',
            'subtitle': 'Modern Living with Premium Amenities',
            'property_details': {
                'type': 'Luxury Villa',
                'size': '500m²',
                'bedrooms': 4,
                'bathrooms': 3,
                'price': 'Rp 2.500.000.000'
            },
            'features': [
                'Swimming Pool',
                'Garden',
                'Garage for 2 Cars',
                'Smart Home System',
                '24/7 Security'
            ],
            'description': 'Experience luxury living in this stunning modern villa located in the heart of Serang. Features include a spacious swimming pool, beautiful garden, and state-of-the-art smart home technology.',
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'qr_code_url': 'https://example.com/qr/123456'
        }
        
        # Create PDF
        result = await create_brochure(template_data, 'test_brochure.pdf')
        print(f"PDF creation result: {result}")
        
        # List templates and PDFs
        print(f"Available templates: {pdf_creator.list_templates()}")
        print(f"Generated PDFs: {pdf_creator.list_pdfs()}")
    
    asyncio.run(test_pdf_creation())
