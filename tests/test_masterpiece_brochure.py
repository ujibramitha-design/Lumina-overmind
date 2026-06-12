#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for Masterpiece Brochure Assembly System
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add root directory to Python path
root_dir = os.path.dirname(__file__)
sys.path.append(root_dir)

async def test_masterpiece_brochure():
    """Test complete brochure assembly pipeline"""
    
    try:
        # Import the modules
        from core_modules.visual.svg_architect import SVGArchitect, highlight_floorplan
        from core_modules.finance.kpr_engine import KPREngine, ProspectProfile, ProspectType
        from core_modules.visual.brochure_orchestrator import BrochureOrchestrator, assemble_masterpiece
        
        print("✅ Successfully imported all brochure modules")
        
        # Create sample SVG floorplan
        sample_svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
    <rect id="kamar_utama" x="50" y="50" width="200" height="150" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="kamar_anak" x="300" y="50" width="150" height="120" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="kamar_bawah" x="500" y="50" width="120" height="100" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="ruang_keluarga" x="50" y="250" width="400" height="200" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="dapur" x="500" y="250" width="150" height="100" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="toilet_utama" x="50" y="500" width="80" height="80" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <rect id="garasi" x="200" y="500" width="200" height="80" fill="#E0E0E0" stroke="#333" stroke-width="2"/>
    <text x="150" y="125" text-anchor="middle" font-family="Arial" font-size="14">Kamar Utama</text>
    <text x="375" y="110" text-anchor="middle" font-family="Arial" font-size="14">Kamar Anak</text>
    <text x="560" y="100" text-anchor="middle" font-family="Arial" font-size="14">Kamar Bawah</text>
    <text x="250" y="350" text-anchor="middle" font-family="Arial" font-size="14">Ruang Keluarga</text>
    <text x="575" y="300" text-anchor="middle" font-family="Arial" font-size="14">Dapur</text>
    <text x="90" y="540" text-anchor="middle" font-family="Arial" font-size="12">Toilet</text>
    <text x="300" y="540" text-anchor="middle" font-family="Arial" font-size="14">Garasi</text>
</svg>"""
        
        # Save sample SVG
        svg_path = "data/blueprints/sample_floorplan.svg"
        Path("data/blueprints").mkdir(parents=True, exist_ok=True)
        with open(svg_path, 'w') as f:
            f.write(sample_svg)
        
        print("✅ Sample SVG floorplan created")
        
        # Test SVG Architect
        print("\n🏗️ Testing SVG Architect...")
        architect = SVGArchitect()
        
        # Test ELDERLY focus area
        highlighted_svg = architect.highlight_floorplan(
            base_svg_path=svg_path,
            focus_area="ELDERLY",
            output_format="svg"
        )
        print(f"✅ ELDERLY floorplan highlighted: {highlighted_svg}")
        
        # Test KPR Engine
        print("\n💰 Testing KPR Engine...")
        kpr_engine = KPREngine()
        
        prospect_profile = ProspectProfile(
            age=35,
            monthly_income=15000000,  # Rp 15 juta
            employment_type="permanent",
            credit_score=750,
            existing_loans=2000000,   # Rp 2 juta
            family_size=4,
            prospect_type=ProspectType.UPGRADER
        )
        
        property_price = 800000000  # Rp 800 juta
        kpr_options = kpr_engine.generate_personalized_pricelist(property_price, prospect_profile)
        
        print(f"✅ Generated {len(kpr_options['options'])} KPR options")
        if kpr_options['options']:
            best_option = kpr_options['options'][0]
            print(f"🏆 Best option: {best_option['bank']}")
            print(f"💳 Monthly payment: Rp {best_option['best_option']['monthly_payment']:,.0f}")
        
        # Test Brochure Orchestrator
        print("\n🎭 Testing Brochure Orchestrator...")
        
        # Sample lead data
        sample_lead = {
            'id': 'lead_12345',
            'name': 'Ahmad Wijaya',
            'age': 35,
            'family_size': 4,
            'property_name': 'The Royal Residence',
            'property_price': 800000000,
            'property_image': 'https://via.placeholder.com/800x600/333333/ffffff?text=Luxury+Property',
            'floorplan_svg': svg_path,
            'prospect_profile': {
                'age': 35,
                'monthly_income': 15000000,
                'employment_type': 'permanent',
                'credit_score': 750,
                'existing_loans': 2000000,
                'family_size': 4,
                'prospect_type': 'upgrader'
            },
            'land_area': 200,
            'building_area': 150,
            'bedrooms': 3,
            'bathrooms': 2,
            'garage': 2,
            'electricity': 2200
        }
        
        # Test different campaign modes
        campaign_modes = ['luxury', 'modern', 'family']
        
        for mode in campaign_modes:
            try:
                print(f"\n🎨 Testing {mode} campaign mode...")
                
                brochure_path = await assemble_masterpiece(
                    lead_data=sample_lead,
                    campaign_mode=mode,
                    output_format="pdf"
                )
                
                print(f"✅ {mode.title()} brochure generated: {brochure_path}")
                
                # Check if file exists and get size
                if Path(brochure_path).exists():
                    file_size = Path(brochure_path).stat().st_size
                    print(f"📄 File size: {file_size} bytes")
                else:
                    print("❌ Brochure file not found")
                
            except Exception as e:
                print(f"❌ {mode.title()} brochure failed: {e}")
        
        # Test comparison table
        print("\n📊 Testing KPR comparison table...")
        comparison = kpr_engine.create_comparison_table(kpr_options['options'])
        print("Comparison Table:")
        print(comparison)
        
        print("\n✅ Masterpiece brochure system test completed!")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install playwright lxml cairosvg qrcode[pil] pillow")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_masterpiece_brochure())
