#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🏗️ SVG ARCHITECT - Smart Blueprint Manipulator
===============================================

Advanced SVG manipulation system for floorplan highlighting and customization.
Supports dynamic color changes, layer manipulation, and export to PNG/PDF.

Features:
- SVG parsing and manipulation using lxml
- Dynamic floorplan highlighting based on focus areas
- Layer-specific color customization
- Export to PNG/PDF for brochure integration
- Elderly/elderly-friendly area highlighting
- Room-specific customization options
"""

import os
import re
import logging
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime
import base64
import io

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False
    import xml.etree.ElementTree as ET

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cairosvg
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SVGArchitect:
    """Advanced SVG manipulation system for floorplan customization"""
    
    def __init__(self, output_dir: str = "data/blueprints"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Color schemes for different focus areas
        self.color_schemes = {
            'ELDERLY': {
                'primary': '#FFD700',      # Gold
                'secondary': '#FFA500',    # Orange
                'accent': '#FF6347',       # Tomato
                'neutral': '#F5F5DC'       # Beige
            },
            'FAMILY': {
                'primary': '#4169E1',      # Royal Blue
                'secondary': '#6495ED',    # Cornflower Blue
                'accent': '#87CEEB',       # Sky Blue
                'neutral': '#E6E6FA'       # Lavender
            },
            'INVESTOR': {
                'primary': '#2E8B57',      # Sea Green
                'secondary': '#3CB371',    # Medium Sea Green
                'accent': '#90EE90',       # Light Green
                'neutral': '#F0FFF0'       # Honeydew
            },
            'YOUNG': {
                'primary': '#FF69B4',      # Hot Pink
                'secondary': '#FFB6C1',    # Light Pink
                'accent': '#FFC0CB',       # Pink
                'neutral': '#FFE4E1'       # Misty Rose
            },
            'LUXURY': {
                'primary': '#8B008B',      # Dark Magenta
                'secondary': '#9932CC',    # Dark Orchid
                'accent': '#BA55D3',       # Medium Orchid
                'neutral': '#E6E6FA'       # Lavender
            }
        }
        
        # Room layer mappings
        self.room_mappings = {
            'ELDERLY': {
                'kamar_bawah': 'primary',
                'kamar_utama': 'primary',
                'kamar_mandia': 'secondary',
                'ruang_keluarga': 'accent',
                'dapur': 'accent',
                'toilet_utama': 'secondary',
                'teras': 'neutral'
            },
            'FAMILY': {
                'kamar_utama': 'primary',
                'kamar_anak_1': 'secondary',
                'kamar_anak_2': 'secondary',
                'ruang_keluarga': 'primary',
                'dapur': 'accent',
                'toilet': 'accent',
                'teras_belakang': 'neutral'
            },
            'INVESTOR': {
                'ruang_tamu': 'primary',
                'dapur': 'primary',
                'kamar_1': 'secondary',
                'kamar_2': 'secondary',
                'carport': 'accent',
                'taman': 'neutral'
            },
            'YOUNG': {
                'kamar_utama': 'primary',
                'work_space': 'secondary',
                'living_room': 'accent',
                'kitchen': 'accent',
                'balcony': 'neutral'
            },
            'LUXURY': {
                'master_suite': 'primary',
                'walk_in_closet': 'secondary',
                'private_lounge': 'accent',
                'private_terrace': 'accent',
                'ensuite_bathroom': 'secondary'
            }
        }
    
    def highlight_floorplan(
        self,
        base_svg_path: str,
        focus_area: str,
        custom_colors: Optional[Dict[str, str]] = None,
        output_format: str = "svg"
    ) -> str:
        """
        Highlight floorplan based on focus area
        
        Args:
            base_svg_path: Path to base SVG file
            focus_area: Target area (ELDERLY, FAMILY, INVESTOR, YOUNG, LUXURY)
            custom_colors: Custom color scheme override
            output_format: Output format (svg, png, pdf)
        
        Returns:
            Path to generated file
        """
        try:
            # Validate inputs
            if not Path(base_svg_path).exists():
                raise FileNotFoundError(f"Base SVG not found: {base_svg_path}")
            
            if focus_area not in self.color_schemes:
                raise ValueError(f"Invalid focus area: {focus_area}")
            
            # Load and parse SVG
            svg_content = self._load_svg(base_svg_path)
            
            # Apply highlighting
            highlighted_svg = self._apply_highlighting(svg_content, focus_area, custom_colors)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = Path(base_svg_path).stem
            output_filename = f"{base_name}_{focus_area}_{timestamp}.{output_format}"
            output_path = self.output_dir / output_filename
            
            # Save in requested format
            if output_format.lower() == "svg":
                self._save_svg(highlighted_svg, output_path)
            elif output_format.lower() == "png":
                self._convert_to_png(highlighted_svg, output_path)
            elif output_format.lower() == "pdf":
                self._convert_to_pdf(highlighted_svg, output_path)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            logger.info(f"✅ Floorplan highlighted: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Floorplan highlighting failed: {e}")
            raise
    
    def _load_svg(self, svg_path: str) -> str:
        """Load SVG content from file"""
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"❌ Failed to load SVG: {e}")
            raise
    
    def _apply_highlighting(
        self,
        svg_content: str,
        focus_area: str,
        custom_colors: Optional[Dict[str, str]] = None
    ) -> str:
        """Apply highlighting to SVG content"""
        try:
            # Use custom colors if provided, otherwise use scheme colors
            color_scheme = custom_colors or self.color_schemes[focus_area]
            room_mapping = self.room_mappings.get(focus_area, {})
            
            # Parse SVG
            if LXML_AVAILABLE:
                # Use lxml for better XML handling
                parser = etree.XMLParser(remove_blank_text=True)
                root = etree.fromstring(svg_content.encode('utf-8'), parser)
                
                # Apply highlighting to matching elements
                for room_name, color_type in room_mapping.items():
                    color = color_scheme.get(color_type, color_scheme.get('primary'))
                    self._highlight_elements_by_name(root, room_name, color)
                
                # Convert back to string
                highlighted_svg = etree.tostring(root, encoding='unicode', pretty_print=True)
            else:
                # Fallback to regex-based manipulation
                highlighted_svg = self._apply_regex_highlighting(svg_content, room_mapping, color_scheme)
            
            return highlighted_svg
            
        except Exception as e:
            logger.error(f"❌ SVG highlighting failed: {e}")
            raise
    
    def _highlight_elements_by_name(self, root, element_name: str, color: str):
        """Highlight SVG elements by name/ID/class"""
        try:
            # Look for elements with matching name, ID, or class
            xpath_conditions = [
                f"//*[@id='{element_name}']",
                f"//*[@name='{element_name}']",
                f"//*[contains(@class, '{element_name}')]",
                f"//*[@data-room='{element_name}']",
                f"//*[@data-layer='{element_name}']"
            ]
            
            for xpath in xpath_conditions:
                elements = root.xpath(xpath)
                for element in elements:
                    self._apply_color_to_element(element, color)
            
            # Also try partial matches for flexibility
            partial_xpath = f"//*[contains(@id, '{element_name}') or contains(@name, '{element_name}') or contains(@class, '{element_name}')]"
            elements = root.xpath(partial_xpath)
            for element in elements:
                self._apply_color_to_element(element, color)
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to highlight elements for {element_name}: {e}")
    
    def _apply_color_to_element(self, element, color: str):
        """Apply color to SVG element"""
        try:
            # Apply fill color
            if 'fill' in element.attrib:
                original_fill = element.attrib['fill']
                element.attrib['fill'] = color
                # Store original fill for potential restoration
                element.attrib['data-original-fill'] = original_fill
            else:
                element.attrib['fill'] = color
            
            # Apply stroke color for better visibility
            if 'stroke' in element.attrib:
                original_stroke = element.attrib['stroke']
                element.attrib['stroke'] = color
                element.attrib['data-original-stroke'] = original_stroke
            else:
                element.attrib['stroke'] = color
                element.attrib['stroke-width'] = '2'
            
            # Add highlighting class
            existing_class = element.attrib.get('class', '')
            element.attrib['class'] = f"{existing_class} highlighted-area".strip()
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to apply color to element: {e}")
    
    def _apply_regex_highlighting(
        self,
        svg_content: str,
        room_mapping: Dict[str, str],
        color_scheme: Dict[str, str]
    ) -> str:
        """Fallback regex-based highlighting"""
        try:
            highlighted_svg = svg_content
            
            for room_name, color_type in room_mapping.items():
                color = color_scheme.get(color_type, color_scheme.get('primary'))
                
                # Pattern to find SVG elements with room identifiers
                patterns = [
                    rf'(id="{room_name}")',
                    rf'(name="{room_name}")',
                    rf'(class="[^"]*{room_name}[^"]*")',
                    rf'(data-room="{room_name}")',
                    rf'(data-layer="{room_name}")'
                ]
                
                for pattern in patterns:
                    # Add fill attribute after the matching attribute
                    highlighted_svg = re.sub(
                        pattern,
                        f'\\1 fill="{color}" stroke="{color}" stroke-width="2" class="highlighted-area"',
                        highlighted_svg,
                        flags=re.IGNORECASE
                    )
            
            return highlighted_svg
            
        except Exception as e:
            logger.error(f"❌ Regex highlighting failed: {e}")
            raise
    
    def _save_svg(self, svg_content: str, output_path: Path):
        """Save SVG content to file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
        except Exception as e:
            logger.error(f"❌ Failed to save SVG: {e}")
            raise
    
    def _convert_to_png(self, svg_content: str, output_path: Path):
        """Convert SVG to PNG"""
        try:
            if CAIROSVG_AVAILABLE:
                # Use cairosvg for high-quality conversion
                cairosvg.svg2png(
                    bytestring=svg_content.encode('utf-8'),
                    write_to=str(output_path),
                    output_width=1200,
                    output_height=800,
                    scale=2
                )
            elif PIL_AVAILABLE:
                # Fallback to PIL (may not render SVG perfectly)
                # This is a simplified fallback - in production, use cairosvg
                logger.warning("⚠️ Using PIL fallback for SVG to PNG conversion")
                self._create_placeholder_png(output_path)
            else:
                raise ImportError("Neither cairosvg nor PIL available for PNG conversion")
                
        except Exception as e:
            logger.error(f"❌ PNG conversion failed: {e}")
            raise
    
    def _convert_to_pdf(self, svg_content: str, output_path: Path):
        """Convert SVG to PDF"""
        try:
            if CAIROSVG_AVAILABLE:
                # Use cairosvg for PDF conversion
                cairosvg.svg2pdf(
                    bytestring=svg_content.encode('utf-8'),
                    write_to=str(output_path)
                )
            else:
                # Fallback: create a simple PDF placeholder
                logger.warning("⚠️ Creating PDF placeholder - cairosvg not available")
                self._create_placeholder_pdf(output_path)
                
        except Exception as e:
            logger.error(f"❌ PDF conversion failed: {e}")
            raise
    
    def _create_placeholder_png(self, output_path: Path):
        """Create placeholder PNG when conversion libraries unavailable"""
        try:
            # Create a simple placeholder image
            img = Image.new('RGB', (1200, 800), color='#F0F0F0')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            text = "Floorplan Highlight\n(Conversion libraries not available)"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (1200 - text_width) // 2
            y = (800 - text_height) // 2
            
            draw.text((x, y), text, fill='#333333', font=font)
            img.save(output_path)
            
        except Exception as e:
            logger.error(f"❌ Placeholder PNG creation failed: {e}")
            raise
    
    def _create_placeholder_pdf(self, output_path: Path):
        """Create placeholder PDF when conversion libraries unavailable"""
        try:
            # Create a simple text-based PDF placeholder
            placeholder_text = f"""
Floorplan Highlight Placeholder
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Note: Advanced SVG to PDF conversion requires cairosvg library.
Install with: pip install cairosvg
"""
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(placeholder_text)
                
        except Exception as e:
            logger.error(f"❌ Placeholder PDF creation failed: {e}")
            raise
    
    def create_custom_highlight(
        self,
        base_svg_path: str,
        room_highlights: Dict[str, str],
        output_format: str = "svg"
    ) -> str:
        """
        Create custom highlighting with specific room-color mappings
        
        Args:
            base_svg_path: Path to base SVG file
            room_highlights: Dictionary mapping room names to colors
            output_format: Output format (svg, png, pdf)
        
        Returns:
            Path to generated file
        """
        try:
            # Load SVG
            svg_content = self._load_svg(base_svg_path)
            
            # Apply custom highlighting
            if LXML_AVAILABLE:
                parser = etree.XMLParser(remove_blank_text=True)
                root = etree.fromstring(svg_content.encode('utf-8'), parser)
                
                for room_name, color in room_highlights.items():
                    self._highlight_elements_by_name(root, room_name, color)
                
                highlighted_svg = etree.tostring(root, encoding='unicode', pretty_print=True)
            else:
                # Fallback to regex
                highlighted_svg = self._apply_regex_highlighting(svg_content, room_highlights, room_highlights)
            
            # Generate output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = Path(base_svg_path).stem
            output_filename = f"{base_name}_custom_{timestamp}.{output_format}"
            output_path = self.output_dir / output_filename
            
            if output_format.lower() == "svg":
                self._save_svg(highlighted_svg, output_path)
            elif output_format.lower() == "png":
                self._convert_to_png(highlighted_svg, output_path)
            elif output_format.lower() == "pdf":
                self._convert_to_pdf(highlighted_svg, output_path)
            
            logger.info(f"✅ Custom floorplan created: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Custom highlighting failed: {e}")
            raise
    
    def get_room_info(self, svg_path: str) -> Dict[str, Any]:
        """
        Extract room information from SVG
        
        Args:
            svg_path: Path to SVG file
        
        Returns:
            Dictionary with room information
        """
        try:
            svg_content = self._load_svg(svg_path)
            
            if LXML_AVAILABLE:
                parser = etree.XMLParser(remove_blank_text=True)
                root = etree.fromstring(svg_content.encode('utf-8'), parser)
                
                rooms = {}
                
                # Find all elements with room identifiers
                room_elements = root.xpath("//*[@id or @name or @data-room or contains(@class, 'room')]")
                
                for element in room_elements:
                    room_id = (
                        element.attrib.get('id') or
                        element.attrib.get('name') or
                        element.attrib.get('data-room') or
                        self._extract_room_from_class(element.attrib.get('class', ''))
                    )
                    
                    if room_id:
                        rooms[room_id] = {
                            'element': element.tag,
                            'fill': element.attrib.get('fill', 'none'),
                            'stroke': element.attrib.get('stroke', 'black'),
                            'stroke_width': element.attrib.get('stroke-width', '1'),
                            'class': element.attrib.get('class', ''),
                            'bounds': self._get_element_bounds(element)
                        }
                
                return rooms
            else:
                # Fallback to regex extraction
                return self._extract_rooms_regex(svg_content)
                
        except Exception as e:
            logger.error(f"❌ Room info extraction failed: {e}")
            return {}
    
    def _extract_room_from_class(self, class_attr: str) -> Optional[str]:
        """Extract room name from class attribute"""
        try:
            if not class_attr:
                return None
            
            classes = class_attr.split()
            for cls in classes:
                if 'room' in cls.lower() or 'kamar' in cls.lower():
                    return cls
            return None
        except:
            return None
    
    def _get_element_bounds(self, element) -> Dict[str, float]:
        """Get bounding box of SVG element"""
        try:
            bounds = {}
            
            # Try to extract from viewBox or coordinates
            if 'x' in element.attrib:
                bounds['x'] = float(element.attrib['x'])
            if 'y' in element.attrib:
                bounds['y'] = float(element.attrib['y'])
            if 'width' in element.attrib:
                bounds['width'] = float(element.attrib['width'])
            if 'height' in element.attrib:
                bounds['height'] = float(element.attrib['height'])
            
            return bounds
        except:
            return {}
    
    def _extract_rooms_regex(self, svg_content: str) -> Dict[str, Any]:
        """Fallback regex-based room extraction"""
        try:
            rooms = {}
            
            # Pattern to find room identifiers
            room_patterns = [
                r'id="([^"]*(?:room|kamar)[^"]*)"',
                r'name="([^"]*(?:room|kamar)[^"]*)"',
                r'data-room="([^"]*)"',
                r'class="[^"]*([^"]*(?:room|kamar)[^"]*)[^"]*"'
            ]
            
            for pattern in room_patterns:
                matches = re.findall(pattern, svg_content, re.IGNORECASE)
                for match in matches:
                    rooms[match] = {
                        'source': 'regex',
                        'pattern': pattern
                    }
            
            return rooms
        except Exception as e:
            logger.error(f"❌ Regex room extraction failed: {e}")
            return {}

# Convenience function for easy usage
def highlight_floorplan(
    base_svg_path: str,
    focus_area: str,
    custom_colors: Optional[Dict[str, str]] = None,
    output_format: str = "svg"
) -> str:
    """
    Highlight floorplan based on focus area
    
    Args:
        base_svg_path: Path to base SVG file
        focus_area: Target area (ELDERLY, FAMILY, INVESTOR, YOUNG, LUXURY)
        custom_colors: Custom color scheme override
        output_format: Output format (svg, png, pdf)
    
    Returns:
        Path to generated file
    """
    architect = SVGArchitect()
    return architect.highlight_floorplan(base_svg_path, focus_area, custom_colors, output_format)

# Example usage and testing
if __name__ == "__main__":
    def test_svg_architect():
        """Test SVG Architect functionality"""
        
        # Create a sample SVG for testing
        sample_svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
    <rect id="kamar_utama" x="50" y="50" width="200" height="150" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="kamar_anak" x="300" y="50" width="150" height="120" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="ruang_keluarga" x="50" y="250" width="400" height="200" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="dapur" x="500" y="250" width="150" height="100" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <text x="150" y="125" text-anchor="middle" font-family="Arial" font-size="14">Kamar Utama</text>
    <text x="375" y="110" text-anchor="middle" font-family="Arial" font-size="14">Kamar Anak</text>
    <text x="250" y="350" text-anchor="middle" font-family="Arial" font-size="14">Ruang Keluarga</text>
    <text x="575" y="300" text-anchor="middle" font-family="Arial" font-size="14">Dapur</text>
</svg>"""
        
        # Save sample SVG
        sample_path = "data/blueprints/sample_floorplan.svg"
        Path("data/blueprints").mkdir(parents=True, exist_ok=True)
        with open(sample_path, 'w') as f:
            f.write(sample_svg)
        
        try:
            # Test highlighting
            architect = SVGArchitect()
            
            # Test ELDERLY focus area
            highlighted_svg = architect.highlight_floorplan(
                base_svg_path=sample_path,
                focus_area="ELDERLY",
                output_format="svg"
            )
            print(f"✅ ELDERLY floorplan highlighted: {highlighted_svg}")
            
            # Test FAMILY focus area
            family_svg = architect.highlight_floorplan(
                base_svg_path=sample_path,
                focus_area="FAMILY",
                output_format="svg"
            )
            print(f"✅ FAMILY floorplan highlighted: {family_svg}")
            
            # Test custom highlighting
            custom_colors = {
                'kamar_utama': '#FF0000',
                'ruang_keluarga': '#00FF00'
            }
            custom_svg = architect.create_custom_highlight(
                base_svg_path=sample_path,
                room_highlights=custom_colors,
                output_format="svg"
            )
            print(f"✅ Custom floorplan created: {custom_svg}")
            
            # Test room info extraction
            room_info = architect.get_room_info(sample_path)
            print(f"✅ Room info extracted: {list(room_info.keys())}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Run test
    test_svg_architect()
