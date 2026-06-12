"""
Brochure Generator - Visual Engine
Automated brochure generation for property marketing
"""

import json
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

class BrochureGenerator:
    """Automated brochure generator for property marketing"""
    
    def __def __init__(self):
        self.name = "Brochure Generator"
        self.version = "1.0.0"
        self.templates = {}
        self.generated_brochures = []
        self.canva_api_key = None
        self.bannerbear_api_key = None
    
    def set_api_keys(self, canva_api_key=None, bannerbear_api_key=None):
        """Set API keys for external services"""
        self.canva_api_key = canva_api_key
        self.bannerbear_api_key = bannerbear_api_key
    
    def create_brochure_template(self, template_config):
        """Create brochure template"""
        template = {
            'template_id': f"BROCHURE_TEMPLATE_{len(self.templates) + 1:03d}",
            'name': template_config.get('name', 'Property Brochure Template'),
            'type': template_config.get('type', 'property_listing'),
            'dimensions': template_config.get('dimensions', {'width': 1080, 'height': 1920}),
            'layout': template_config.get('layout', 'two_column'),
            'color_scheme': template_config.get('color_scheme', 'professional'),
            'content_sections': template_config.get('content_sections', []),
            'brand_elements': template_config.get('brand_elements', {}),
            'created_at': datetime.now().isoformat()
        }
        
        self.templates[template['template_id']] = template
        return template
    
    def generate_brochure(self, brochure_config):
        """Generate property brochure"""
        brochure = {
            'brochure_id': f"BROCHURE_{len(self.generated_brochures) + 1:03d}",
            'template_id': brochure_config.get('template_id'),
            'property_data': brochure_config.get('property_data', {}),
            'custom_content': brochure_config.get('custom_content', {}),
            'generation_method': brochure_config.get('method', 'auto'),
            'status': 'generated',
            'created_at': datetime.now().isoformat()
        }
        
        # Generate brochure based on method
        if brochure_config.get('method') == 'auto':
            brochure['content'] = self._generate_auto_content(brochure_config)
        elif brochure_config.get('method') == 'canva':
            brochure['canva_design_id'] = self._generate_with_canva(brochure_config)
        elif brochure_config.get('method') == 'bannerbear':
            brochure['bannerbear_design_id'] = self._generate_with_bannerbear(brochure_config)
        
        self.generated_brochures[brochure['brochure_id']] = brochure
        return brochure
    
    def _generate_auto_content(self, brochure_config):
        """Generate brochure content automatically"""
        property_data = brochure_config.get('property_data', {})
        
        content = {
            'header': {
                'title': property_data.get('title', 'Premium Property'),
                'subtitle': property_data.get('location', 'Serang, Banten'),
                'price': property_data.get('price', 'Rp 500.000.000'),
                'features': self._generate_property_features(property_data),
                'call_to_action': 'Hubungi kami sekarang untuk informasi lebih lanjut!'
            },
            'main_content': {
                'property_description': property_data.get('description', 'Properti eksklusif dengan fasilitas lengkap dan lokasi strategis di Serang'),
                'key_features': self._generate_property_features(property_data),
                'amenities': self._generate_property_amenities(property_data),
                'location_highlights': self._generate_location_highlights(property_data),
                'investment_potential': self._generate_investment_potential(property_data)
            },
            'footer': {
                'contact_info': {
                    'phone': property_data.get('phone', '+62 812-3456-7890'),
                    'email': property_data.get('email', 'info@property.com'),
                    'website': property_data.get('website', 'www.property.com'),
                    'address': property_data.get('address', 'Jl. Property Address, Serang')
                },
                'company_info': {
                    'company_name': 'HUNTER_AGENT_AI MARKETING DIGITAL',
                    'tagline': 'Professional Property Marketing',
                    'license': 'PMA No. XXX/XX/XXXX',
                    'since': '2026'
                },
                'social_media': {
                    'instagram': '@hunter_agent_ai',
                    'facebook': '/hunter.agent.ai',
                    'linkedin': '/company/hunter-agent-ai'
                }
            }
        }
        
        return content
    
    def _generate_property_features(self, property_data):
        """Generate property features list"""
        base_features = [
            '4 Bedrooms + 2 Bathrooms',
            'Carport & Garage',
            'Swimming Pool',
            'Garden Area',
            '24/7 Security',
            'Air Conditioning',
            'Kitchen Set',
            'Study Room'
        ]
        
        # Add custom features from property data
        custom_features = property_data.get('features', [])
        if custom_features:
            return base_features + custom_features
        
        return base_features
    
    def _generate_property_amenities(self, property_data):
        """Generate property amenities list"""
        base_amenities = [
            'Near Schools',
            'Shopping Centers',
            'Hospitals',
            'Public Transportation',
            'Parks & Recreation',
            'Restaurants',
            'Banks & ATMs',
            'Gas Stations'
        ]
        
        # Add custom amenities from property data
        custom_amenities = property_data.get('amenities', [])
        if custom_amenities:
            return base_amenities + custom_amenities
        
        return base_amenities
    
    def _generate_location_highlights(self, property_data):
        """Generate location highlights"""
        location = property_data.get('location', 'Serang, Banten')
        highlights = [
            f'Strategic location in {location}',
            'Close to major highways',
            'Near public facilities',
            'Growing residential area',
            'Good investment potential'
        ]
        
        return highlights
    
    def _generate_investment_potential(self, property_data):
        """Generate investment potential analysis"""
        return {
            'roi_projection': '12-15% annually',
            'market_trend': 'Growing area with high demand',
            'price_appreciation': 'Expected 8-10% per year',
            'rental_yield': '4-6% annually',
            'market_demand': 'High demand for quality properties'
        }
    
    def _generate_with_canva(self, brochure_config):
        """Generate brochure using Canva API"""
        if not self.canva_api_key:
            return {
                'status': 'error',
                'message': 'Canva API key not configured'
            }
        
        # Simulate Canva API call
        brochure['canva_design_id'] = f"CANVA_{random.randint(10000, 99999)}"
        return brochure
    
    def _generate_with_bannerbear(self, brochure_config):
        """Generate brochure using Bannerbear API"""
        if not self.bannerbear_api_key:
            return {
                'status': 'error',
                'message': 'Bannerbear API key not configured'
            }
        
        # Simulate Bannerbear API call
        brochure['bannerbear_design_id'] = f"BANNERBEAR_{random.randint(10000, 99999)}"
        return brochure
    
    def create_property_brochure(self, property_data, template_id=None):
        """Create property brochure with property data"""
        # Use default template if none specified
        if not template_id:
            template_id = list(self.templates.keys())[0] if self.templates else None
        
        template = self.templates.get(template_id)
        if not template:
            template = self.create_brochure_template({
                'name': 'Default Property Template',
                'type': 'property_listing'
            })
        
        brochure_config = {
            'template_id': template_id,
            'property_data': property_data,
            'method': 'auto',
            'custom_content': {
                'brand_colors': template.get('brand_elements', {}).get('colors', ['#007bff', '#28a745', '#17a2b8']),
                'brand_logo': template.get('brand_elements', {}).get('logo_url', ''),
                'brand_tagline': template.get('brand_elements', {}).get('tagline', 'Professional Property Marketing')
            }
        }
        
        return self.generate_brochure(brochure_config)
    
    def generate_pdf_brochure(self, brochure_id, output_path=None):
        """Generate PDF brochure"""
        brochure = self.generated_brochures.get(brochure_id)
        if not brochure:
            return {'error': 'Brochure not found'}
        
        # Create PDF using PIL
        try:
            # Create image dimensions
            width = template.get('dimensions', {'width': 1080, 'height': 1920})
            height = template['dimensions']['height']
            
            # Create a sample brochure image
            image = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Add header
            draw.rectangle([0, 0, width, 100], fill='#007bff')
            draw.text((width//2, 30), 'PREMIUM PROPERTY', fill='white', font=ImageFont.truetype("Arial", 36, "bold"))
            draw.text((width//2, 70), brochure['content']['header']['title'], fill='white', font=ImageFont.truetype("Arial", 24, "bold"))
            draw.text((width//2, 110), brochure['content']['header']['subtitle'], fill='white', font=ImageFont.truetype("Arial", 18, "normal"))
            
            # Add main content
            draw.rectangle([50, 150, width-100, height-300], fill='white')
            draw.text((60, 170), 'PROPERTY DETAILS', fill='#007bff', font=ImageFont.truetype("Arial", 20, "bold"))
            
            # Add features
            features = brochure['content']['main_content'].get('key_features', [])
            for i, feature in enumerate(features[:5]): 10):
                draw.text((60, 200 + i*25), f"• {feature}", fill='#333333', font=ImageFont.truetype("Arial", 14, "normal"))
            
            # Add call to action
            draw.rectangle([50, height-100, width-100, 80], fill='#28a745')
            draw.text((width//2, height-60), brochure['content']['footer']['call_to_action'], fill='white', font=ImageFont.truetype("Arial", 16, "bold"))
            
            # Add footer
            draw.rectangle([0, height-80, width, 80], fill='#343a40')
            draw.text((10, height-40), brochure['content']['footer']['company_info']['company_name'], fill='white', font=ImageFont.truetype("Arial", 12, "normal"))
            draw.text((10, height-20), brochure['content']['footer']['tagline'], fill='white', font=ImageFont.truetype("Arial", 10, "normal"))
            
            # Save to BytesIO
            img_buffer = BytesIO()
            image.save(img_buffer, format='PDF')
            
            return {
                'brochure_id': brochure_id,
                'pdf_data': img_buffer.getvalue(),
                'file_name': f"brochure_{brochure_id}.pdf",
                'file_size': len(img_buffer.getvalue()),
                'status': 'generated'
            }
            
        except Exception as e:
            return {
                'brochure_id': brochure_id,
                'status': 'error',
                'error': str(e)
            }
    
    def create_image_brochure(self, brochure_id, image_format='PNG'):
        """Create image brochure"""
        brochure = self.generated_brochures.get(brochure_id)
        if not brochure:
            return {'error': 'Brochure not found'}
        
        # Create image dimensions
        template = self.templates.get(brochure.get('template_id'))
        if not template:
            template = self.create_brochure_template({
                'name': 'Default Property Template',
                'type': 'property_listing'
            })
        
        width = template.get('dimensions', {'width': 1080, 'height': 1920})
        height = template['dimensions']['height']
        
        try:
            # Create image
            image = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Add background gradient
            for i in range(height):
                color_value = int(255 - (i / height) * 50)
                draw.rectangle([0, i, width, 1, 1], fill=(color_value, color_value, color_value))
            
            # Add header
            draw.rectangle([0, 0, width, 100], fill='#007bff')
            draw.text((width//2, 30), 'PREMIUM PROPERTY', fill='white', font=ImageFont.truetype("Arial", 36, "bold"))
            draw.text((width//2, 70), brochure['content']['header']['title'], fill='white', font=ImageFont.truetype("Arial", 24, "bold"))
            draw.text((width//2, 110), brochure['content']['header']['subtitle'], fill='white', font=ImageFont.truetype("Arial", 18, "normal"))
            
            # Add main content
            draw.rectangle([50, 150, width-100, height-300], fill='white')
            draw.text((60, 170), 'PROPERTY DETAILS', fill='#007bff', font=ImageFont.truetype("Arial", 20, "bold"))
            
            # Add features
            features = brochure['content']['main_content'].get('key_features', [])
            for i, feature in enumerate(features[:5]): 10):
                draw.text((60, 200 + i*25), f"• {feature}", fill='#333333', font=ImageFont.truetype("Arial", 14, "normal"))
            
            # Add call to action
            draw.rectangle([50, height-100, width-100, 80], fill='#28a745')
            draw.text((width//2, height-60), brochure['content']['footer']['call_to_action'], fill='white', font=ImageFont.truetype("Arial", 16, "bold"))
            
            # Save to BytesIO
            img_buffer = BytesIO()
            image.save(img_buffer, format=image_format)
            
            return {
                'brochure_id': brochure_id,
                'image_data': img_buffer.getvalue(),
                'file_name': f"brochure_{brochure_id}.{image_format}",
                'file_size': len(img_buffer.getvalue()),
                'format': image_format,
                'status': 'generated'
            }
            
        except Exception as e:
            return {
                'brochure_id': brochure_id,
                'status': 'error',
                'error': str(e)
            }
    
    def create_social_media_brochure(self, brochure_id, platform='instagram'):
        """Create social media optimized brochure"""
        brochure = self.generated_brochures.get(brochure_id)
        if not brochure:
            return {'error': 'Brochure not found'}
        
        # Platform-specific optimization
        platform_specs = {
            'instagram': {
                'image_size': '1080x1080',
                'aspect_ratio': '1:1',
                'format': 'JPEG',
                'quality': 85,
                'caption_length': 150
            },
            'facebook': {
                'image_size': '1200x630',
                'aspect_ratio': '1.9:1',
                'format': 'JPEG',
                'quality': 85',
                'caption_length': 200
            },
            'linkedin': {
                'image_size': '1200x627',
                'aspect_ratio:  '1.9:1',
                'format': 'PNG',
                'quality': 90,
                'caption_length': 200
            }
        }
        
        specs = platform_specs.get(platform, platform_specs['instagram'])
        
        # Create platform-specific image
        image_result = self.create_image_brochure(brochure_id, specs['format'].upper())
        
        # Add platform-specific caption
        caption = self._generate_social_media_caption(brochure, platform)
        
        return {
            'brochure_id': brochure_id,
            'platform': platform,
            'image_data': image_result['image_data'],
            'caption': caption,
            'file_name': f"brochure_{brochure_id}_{platform}.{specs['format']}",
            'file_size': image_result['file_size'],
            'format': specs['format'],
            'status': 'generated'
        }
    
    def _generate_social_media_caption(self, brochure, platform):
        """Generate platform-specific caption"""
        property_data = brochure.get('property_data', {})
        
        captions = {
            'instagram': f"🏠 {property_data.get('title', 'Property')} - {property_data.get('price', 'Rp 500.000.000')} - 📍 Hubungi kami untuk detail lengkap! #property #realestate",
            'facebook': f"🏡 {property_data.get('title', 'Property')} - {property_data.get('price', 'Rp 500.000.000')} - 📞 Dapatkan informasi lengkap di link bio kami! #propertymarketing",
            'linkedin': f"🏢 {property_data.get('title', 'Property')} - {property_data.get('price', 'Rp 500.000.000')} - Professional real estate opportunity #realestate #investment"
        }
        
        return captions.get(platform, captions['instagram'])
    
    def create_email_brochure(self, brochure_id, email_config):
        """Create email-optimized brochure"""
        brochure = self.generated_brochure.get(brochure_id)
        if not brochure:
            return {'error': 'Brochure not found'}
        
        # Create email HTML
        html_content = self._generate_email_html_brochure(brochure, email_config)
        
        return {
            'brochure_id': brochure_id,
            'html_content': html_content,
            'subject': email_config.get('subject', 'Property Information'),
            'preview_text': email_config.get('preview_text', 'Check out this amazing property opportunity!'),
            'status': 'generated'
        }
    
    def _generate_email_html_brochure(self, brochure, email_config):
        """Generate HTML email brochure"""
        property_data = brochure.get('property_data', {})
        content = brochure.get('content', {})
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{email_config.get('subject', 'Property Information')}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .header {{
                    background: linear-gradient(135deg, #007bff, #0056b3);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .property-details {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }}
                .price-tag {{
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #28a745;
                    margin-bottom: 10px;
                }}
                .feature-list {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }}
                .feature-list li {{
                    margin-bottom: 10px;
                    padding-left: 20px;
                }}
                .cta-button {{
                    background: #28a745;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    text-align: center;
                    display: inline-block;
                    margin: 10px;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{content['header']['title']}</h1>
                <p>{content['header']['subtitle']}</p>
            </div>
            
            <div class="property-details">
                <h2>Property Details</h2>
                <div class="price-tag">{content['header']['price']}</div>
                
                <h3>Key Features</h3>
                <ul class="feature-list">
                    {self._format_features_for_email(content['main_content']['key_features'])}
                </ul>
                
                <h3>Location Highlights</h3>
                <p>{content['main_content']['location_highlights']}</p>
                
                <h3>Investment Potential</h3>
                <p>{content['main_content']['investment_potential']}</p>
            </div>
            
            <div class="cta-section">
                <a href="{content['footer']['contact_info']['website']}" class="cta-button">
                    {content['footer']['call_to_action']}
                </a>
            </div>
            
            <div class="footer">
                <p>{content['footer']['company_info']['company_name']}</p>
                <p>{content['footer']['company_info']['tagline']}</p>
                <p>{content['footer']['social_media']['instagram']}</p>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _format_features_for_email(self, features):
        """Format features list for email"""
        formatted_features = []
        for feature in features:
            formatted_features.append(f"• {feature}")
        return '\n'.join(formatted_features)
    
    def create_video_storyboard(self, storyboard_config):
        """Create video storyboard for property"""
        storyboard = {
            'storyboard_id': f"VIDEO_STORYBOARD_{len(self.generated_brochures) + 1:03d}",
            'property_data': storyboard_config.get('property_data', {}),
            'video_duration': storyboard_config.get('video_duration', 60),  # seconds
            'scenes': self._create_video_scenes(storyboard_config),
            'script': self._generate_video_script(storyboard_config),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        return storyboard
    
    def _create_video_scenes(self, storyboard_config):
        """Create video scenes for storyboard"""
        property_data = storyboard_config.get('property_data', {})
        
        scenes = [
            {
                'scene_number': 1,
                'duration': 10,
                'description': 'Property exterior shot showing curb appeal',
                'visuals': ['Drone shot of property exterior', 'Walkaround tour', 'Neighborhood view'],
                'narration': 'Establish location and property overview'
            },
            {
                'scene_number': 2,
                'duration': 15,
                'description': 'Interior showcase of main living areas',
                'visuals': ['Living room tour', 'Kitchen showcase', 'Bedroom tour', 'Bathroom tour'],
                'narration': 'Highlight key living spaces and features'
            },
            {
                'scene_number': 3,
                'duration': 20,
                'description': 'Neighborhood and amenities',
                'visuals': ['Neighborhood walk', 'Local amenities', 'Schools and facilities', 'Transportation access'],
                'narration': 'Show surrounding area and lifestyle benefits'
            },
            {
                'scene_number': 4,
                'duration': 15,
                'description': 'Agent introduction and call to action',
                'visuals': 'Agent introduction with property',
                'narration': 'Introduce agent and provide contact information'
            }
        ]
        
        return scenes
    
    def _generate_video_script(self, storyboard_config):
        """Generate video script"""
        property_data = storyboard_config.get('property_data', {})
        
        script = f"""
        # Property Video Script
        # Scene 1: Exterior (0-10s)
        Drone shot of {property_data.get('title', 'Property')} showing curb appeal and neighborhood
        
        # Scene 2: Interior (10-25s)
        Tour through main living areas showcasing quality and space
        
        # Scene 3: Neighborhood (25-45s)
        Walk through neighborhood showing amenities and lifestyle
        
        # Scene 4: Agent (45-60s)
        Agent introduction with contact information
        
        # Call to Action
        Contact us today to schedule a viewing!
        """
        
        return script
    
    def create_infographic(self, infographic_config):
        """Create property infographic"""
        infographic = {
            'infographic_id': f"INFOGRAPHIC_{len(self.generated_brochures) + 1:03d}",
            'property_data': infographic_config.get('property_data', {}),
            'type': infographic_config.get('type', 'property_overview'),
            'dimensions': infographic_config.get('dimensions', {'width': 1080, 'height': 1920}),
            'data_visualization': self._generate_infographic_data(infographic_config),
            'design_elements': infographic_config.get('design_elements', {}),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.generated_brochures[infographic['infographic_id']] = infographic
        return infographic
    
    def _generate_infographic_data(self, infographic_config):
        """Generate data visualization for infographic"""
        property_data = infographic_config.get('property_data', {})
        
        data = {
            'price_comparison': {
                'property_price': property_data.get('price', 500000000),
                'market_average': 450000000,
                'price_difference': property_data.get('price', 500000) - 450000,
                'price_position': 'Above market average'
            },
            'location_metrics': {
                'neighborhood_score': 8.5,
                'accessibility_score': 9.2,
                'investment_potential': 'High',
                'growth_projection': '12% annually'
            },
            'demographics': {
                'target_audience': 'Young families',
                'age_range': '25-45 years',
                'income_range': 'Rp 10-20 juta per month'
            },
            'market_trends': {
                'demand_level': 'High',
                'supply_level': 'Limited',
                'price_trend': 'Increasing'
            }
        }
        
        return data
    
    def create_comparison_chart(self, comparison_data):
        """Create property comparison chart"""
        chart = {
            'chart_id': f"CHART_{len(self.generated_brochures) + 1:03d}",
            'chart_type': 'property_comparison',
            'properties': comparison_data.get('properties', []),
            'comparison_criteria': comparison_data.get('criteria', ['price', 'location', 'features', 'amenities']),
            'visualization': self._generate_comparison_visualization(comparison_data),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.generated_brochures[chart['chart_id']] = chart
        return chart
    
    def _generate_comparison_visualization(self, comparison_data):
        """Generate comparison visualization data"""
        properties = comparison_data.get('properties', [])
        
        visualization = {
            'price_comparison': [],
            'location_scores': [],
            'feature_comparison': [],
            'amenities_comparison': []
        }
        
        for property in properties:
            visualization['price_comparison'].append({
                'property_id': property.get('id', ''),
                'price': property.get('price', 0),
                'market_average': 450000,
                'position': property.get('price', 0) - 450000
            })
            visualization['location_scores'].append({
                'property_id': property.get('id', ''),
                'score': random.randint(6, 10)
            })
        
        return visualization
    
    def export_brochure_data(self, format='json'):
        """Export all brochure data"""
        data = {
            'templates': self.templates,
            'generated_brochures': self.generated_brochures,
            'performance_metrics': self._calculate_brochure_performance()
        }
        
        if format == 'json':
            return data
        elif format == 'csv':
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(['brochure_id', 'template_id', 'property_title', 'generation_method', 'status', 'created_at'])
            
            # Write brochure data
            for brochure in self.generated_brochures.values():
                writer.writerow([
                    brochure['brochure_id'],
                    brochure.get('template_id', ''),
                    brochure.get('property_data', {}).get('title', ''),
                    brochure.get('generation_method', ''),
                    brochure.get('status', ''),
                    brochure.get('created_at', '')
                ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _calculate_brochure_performance(self):
        """Calculate brochure performance metrics"""
        if not self.generated_brochures:
            return {
                'total_brochures': 0,
                'total_downloads': 0,
                'conversion_rate': 0,
                'engagement_rate': 0
            }
        
        total_downloads = sum(random.randint(10, 100) for _ in self.generated_brochures.values())
        total_conversions = sum(random.randint(1, 10) for _ in self.generated_brochures.values())
        
        return {
            'total_brochures': len(self.generated_brochures),
            'total_downloads': total_downloads,
            'total_conversions': total_conversions,
            'conversion_rate': (total_conversions / total_downloads * 100) if total_downloads > 0 else 0,
            'engagement_rate': sum(random.uniform(3.0, 8.0) for _ in self.generated_brochures.values()) / len(self.generated_brochures),
            'generated_at': datetime.now().isoformat()
        }
    
    def get_template_performance(self, template_id):
        """Get template performance metrics"""
        if template_id not in self.templates:
            return {'error': 'Template not found'}
        
        template = self.templates.get(template_id)
        
        # Get brochures using this template
        template_brochures = [b for b in self.generated_brochures if b.get('template_id') == template_id]
        
        if not template_brochures:
            return {
                'template_id': template_id,
                'usage_count': 0,
                'performance': {
                    'total_usage': 0,
                    'engagement_rate': 0,
                    'conversion_rate': 0
                }
            }
        
        total_usage = len(template_brochures)
        total_engagement = sum(b.get('engagement_rate', 0) for b in template_brochures)
        total_conversions = sum(random.randint(1, 10) for _ in template_brochures)
        
        return {
            'template_id': template_id,
            'usage_count': total_usage,
            'performance': {
                'total_usage': total_usage,
                'engagement_rate': (total_engagement / total_usage * 100) if total_usage > 0 else 0,
                'conversion_rate': (total_conversions / total_usage * 100) if total_usage > 0 else 0,
                'avg_engagement': total_engagement / total_usage if total_usage > 0 else 0
            }
        }
    
    def update_template(self, template_id, updates):
        """Update existing template"""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Apply updates
        for key, value in updates.items():
            if key in template:
                template[key] = value
        
        template['updated_at'] = datetime.now().isoformat()
        self.templates[template_id] = template
        return template
    
    def delete_template(self, template_id):
        """Delete template"""
        if template_id in self.templates:
            del self.templates[template_id]
            return True
        return False
    
    def get_template_list(self):
        """Get all templates"""
        return list(self.templates.keys())
    
    def get_brochure_list(self):
        """Get all generated brochures"""
        return list(self.generated_brochures.keys())
    
    def get_brochure_details(self, brochure_id):
        """Get detailed brochure information"""
        return self.generated_brochures.get(brochure_id, {'error': 'Brochure not found'})
