#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for brochure generation system
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add root directory to Python path
root_dir = os.path.dirname(__file__)
sys.path.append(root_dir)

async def test_brochure_generation():
    """Test brochure generation with sample data"""
    
    try:
        # Import the modules
        sys.path.append(os.path.join(root_dir, 'core_modules', 'visual'))
        from pixel_perfect_renderer import generate_premium_brochure
        from agency_api_adapter import generate_agency_brochure
        
        print("✅ Successfully imported brochure modules")
        
        # Sample data for testing
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
            "TANGGAL_GENERASI": datetime.now().strftime("%d %B %Y"),
            "SALES_CONTACT": "+62 811-2233-4455"
        }
        
        print("✅ Sample data prepared")
        
        # Test local renderer
        print("\n🎨 Testing local renderer...")
        try:
            pdf_path = await generate_premium_brochure(
                template_name="luxury_property",
                context_data=sample_data,
                output_format="pdf"
            )
            print(f"✅ Local PDF generated: {pdf_path}")
            
            # Check if file exists
            if Path(pdf_path).exists():
                file_size = Path(pdf_path).stat().st_size
                print(f"📄 File size: {file_size} bytes")
            else:
                print("❌ PDF file not found")
                
        except Exception as e:
            print(f"❌ Local renderer failed: {e}")
        
        # Test agency adapter (fallback to local)
        print("\n🎨 Testing agency adapter...")
        try:
            agency_pdf_path = await generate_agency_brochure(
                template_name="luxury_property",
                context_data=sample_data,
                output_format="pdf",
                service="local"  # Force local to avoid API key issues
            )
            print(f"✅ Agency PDF generated: {agency_pdf_path}")
            
            # Check if file exists
            if Path(agency_pdf_path).exists():
                file_size = Path(agency_pdf_path).stat().st_size
                print(f"📄 File size: {file_size} bytes")
            else:
                print("❌ Agency PDF file not found")
                
        except Exception as e:
            print(f"❌ Agency adapter failed: {e}")
        
        # Test JPG generation
        print("\n🎨 Testing JPG generation...")
        try:
            jpg_path = await generate_premium_brochure(
                template_name="modern_apartment",
                context_data=sample_data,
                output_format="jpg"
            )
            print(f"✅ JPG generated: {jpg_path}")
            
            # Check if file exists
            if Path(jpg_path).exists():
                file_size = Path(jpg_path).stat().st_size
                print(f"🖼️ File size: {file_size} bytes")
            else:
                print("❌ JPG file not found")
                
        except Exception as e:
            print(f"❌ JPG generation failed: {e}")
        
        print("\n✅ Brochure generation test completed!")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install playwright")
        print("  python -m playwright install chromium")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_brochure_generation())
