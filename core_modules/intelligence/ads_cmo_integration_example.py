"""
Twin-Dragon Engine - AI CMO Trigger & Context-Aware Prompting Example Usage
Demonstrates AI Chief Marketing Officer with context-aware proposal generation
"""

import asyncio
import json
from datetime import datetime

# Import ads manager functions
from ads_manager import generate_ad_proposals

async def example_ai_cmo_integration():
    """Example of AI CMO with context-aware prompting"""
    
    print("🤖 Twin-Dragon AI CMO Context-Aware Example")
    print("=" * 50)
    
    # Example comprehensive project data with full context
    project_data = {
        'id': 'project_123',
        'namaProyek': 'Grand Serang Residence',
        'tipeProyek': 'KOMERSIL',
        'lokasi': 'Serang, Banten',
        'latitude': -6.1256,
        'longitude': 106.1445,
        'radiusKm': 5,
        'namaWilayah': 'Serang Kota',
        'hargaStart': 500000000,
        'targetMarket': 'Middle to Upper Class Professionals',
        
        # Performance data
        'leadsCount': 45,
        'hotLeadsCount': 12,
        'conversionRate': 6.7,
        
        # Configuration
        'tipeInputLokasi': 'KOORDINAT',
        'dorkingTargets': ['property investment', 'real estate', 'commercial property'],
        'scoutMode': 'HYBRID',
        'aiPromptStyle': 'Professional & Data-Driven',
        'isActive': True,
        
        # Existing leads context for AI analysis
        'existingLeads': {
            'total': 45,
            'recent': [
                {
                    'business_name': 'PT. Maju Jaya',
                    'contact': '08123456789',
                    'status': 'INTERESTED',
                    'priority': 'HIGH',
                    'createdAt': '2026-01-01T10:30:00.000Z'
                },
                {
                    'business_name': 'CV. Sejahtera',
                    'contact': '08223456789',
                    'status': 'CONTACTED',
                    'priority': 'MEDIUM',
                    'createdAt': '2026-01-01T09:15:00.000Z'
                },
                {
                    'business_name': 'PT. Berkah Jaya',
                    'contact': '0833456789',
                    'status': 'SCOUTED',
                    'priority': 'LOW',
                    'createdAt': '2026-01-01T08:00:00.000Z'
                }
            ],
            'statusDistribution': {
                'SCOUTED': 15,
                'CONTACTED': 12,
                'INTERESTED': 10,
                'CONVERTED': 8
            }
        },
        
        'createdAt': '2024-01-01T00:00:00.000Z',
        'updatedAt': '2024-01-01T12:00:00.000Z'
    }
    
    print(f"🏢 Target Project: {project_data['namaProyek']}")
    print(f"📍 Type: {project_data['tipeProyek']}")
    print(f"📍 Location: {project_data['lokasi']}")
    print(f"💰 Price: Rp {project_data['hargaStart']:,}")
    print(f"🎯 Performance: {project_data['leadsCount']} leads, {project_data['hotLeadsCount']} hot, {project_data['conversionRate']:.1f}% conversion")
    print()
    
    # Test context-aware AI CMO generation
    print("🤖 Context-Aware AI CMO Generation:")
    print("-" * 40)
    
    print("📊 AI CMO is analyzing project context...")
    print("   - Project data: Name, type, location, price")
    print("   - Performance data: Leads, conversion rate, hot leads")
    print("   - Existing leads: Status distribution and recent leads")
    print("   - Configuration: Scout mode, dorking targets, AI style")
    print()
    
    # Generate context-aware proposals
    proposals = await generate_ad_proposals(project_data)
    
    print(f"✅ Generated {len(proposals)} Context-Aware Ad Proposals:")
    print()
    
    for i, proposal in enumerate(proposals, 1):
        print(f"\n{i}. {proposal.opsi_strategi}")
        print(f"   Target: {proposal.target_audience}")
        print(f"   Budget: Rp {proposal.estimasi_budget:,}")
        print(f"   Copy: {proposal.copywriting}")
        print(f"   Channels: {', '.join(proposal.channel_rekomendasi)}")
        print(f"   KPI: {', '.join(proposal.kpi_utama)}")
        print(f"   Duration: {proposal.durasi_kampanye}")
    
    # Test API endpoint simulation
    print(f"\n🌐 API Endpoint Simulation:")
    print("-" * 40)
    
    # Simulate POST /api/ads/generate/{project_id}
    api_endpoint = f"POST /api/ads/generate/{project_data['id']}"
    print(f"📡 {api_endpoint}")
    print(f"   Method: POST")
    print(f"   Headers: Content-Type: application/json")
    print(f"   Body: None (automatic context extraction)")
    print()
    
    # Simulate API response
    mock_response = {
        "status": "success",
        "message": f"AI CMO generated {len(proposals)} ad proposals for {project_data['namaProyek']}",
        "project_id": project_data['id'],
        "project_name": project_data['namaProyek'],
        "proposals_generated": len(proposals),
        "proposals": [
            {
                "opsiStrategi": proposal.opsi_strategi,
                "targetAudience": proposal.target_audience,
                "copywriting": proposal.copywriting,
                "estimasiBudget": proposal.estimasi_budget,
                "channelRekomendasi": proposal.channel_rekomendasi,
                "kpiUtama": proposal.kpi_utama,
                "durasiKampanye": proposal.durasi_kampanye
            }
            for proposal in proposals
        ],
        "context_used": {
            "project_data": {
                "name": project_data['namaProyek'],
                "type": project_data['tipeProyek'],
                "location": project_data['lokasi'],
                "price": project_data['hargaStart'],
                "leads_count": project_data['leadsCount']
            },
            "existing_leads": project_data['existingLeads']['total'],
            "generation_timestamp": datetime.now().isoformat()
        }
    }
    
    print(f"   Response: {json.dumps(mock_response, indent=2)}")
    
    # Context analysis demonstration
    print(f"\n🔍 Context Analysis Demonstration:")
    print("-" * 40)
    
    print("📊 AI CMO Context Processing:")
    print(f"   📍 Project Name: {project_data['namaProyek']}")
    print(f"   📍 Project Type: {project_data['tipeProyek']} (affects copywriting style)")
    print(f"   📍 Location: {project_data['lokasi']} (affects targeting)")
    print(f"   📍 Price Point: Rp {project_data['hargaStart':,} (affects budget calculation)")
    print(f"   📍 Market Performance: {project_data['conversionRate']:.1f}% conversion rate")
    print(f"   📍 Lead Volume: {project_data['leadsCount']} existing leads")
    print(f"   📍 Hot Leads: {project_data['hotLeadsCount]} high-intent prospects")
    print(f"   📍 Scout Mode: {project_data['scoutMode']} (affects data sources)")
    print(f"   📍 Dorking Targets: {', '.join(project_data['dorking_targets')} (affects keyword strategy)")
    print()
    
    # Strategy adaptation based on context
    print("🎯 Strategy Adaptation Based on Context:")
    print("-" * 40)
    
    if project_data['conversionRate'] > 5:
        print(f"   ✅ High Conversion Rate ({project_data['conversionRate:.1f}%):")
        print(f"      → Focus on conversion optimization and retargeting")
        print(f"      → Emphasize success stories and testimonials")
    elif project_data['conversionRate'] > 2:
        print(f"   ⚠️ Moderate Conversion Rate ({project_data['conversionRate']:.1f}%):")
        print(f"      → Balance between awareness and conversion")
        print(f"      → Include both educational and conversion-focused copy")
    else:
        print(f"   🔴 Low Conversion Rate ({project_data['conversion_rate:.1f}%):")
        print(f"      → Focus on awareness and lead generation")
        print(f"      → Emphasize problem-solution and benefits")
    
    if project_data['tipeProyek'] == 'KOMERSIL':
        print(f"   💼 Commercial Project Strategy:")
        print(f"      → Target: High-income professionals and investors")
        print(f"      → Focus: Investment returns and business opportunities")
        print(f"      → Tone: Professional, authoritative, results-oriented")
    else:
        print(f   🏠️ Subsidi Project Strategy:")
        print(f"      → Target: First-time homebuyers and families")
        print(f"      → Focus: Affordability and government programs")
        print(f"      → Tone: Friendly, helpful, family-oriented")
    
    print(f"   📍 Budget Strategy Based on Price Point:")
    base_budget = int(project_data['hargaStart'] * 0.01)
    print(f"      → Base Budget: Rp {base_budget:,}")
    print(f"      → Agresif: Rp {base_budget * 1.5:,} (High-intent targeting)")
    print(f"      → Seimbang: Rp {base_budget:,} (Balanced approach)")
    print(f"      → Hemat: Rp {base_budget * 0.7:,} (Budget-conscious)")
    
    print(f"   📍 Channel Strategy Based on Location:")
    print(f"      → Area: {project_data['lokasi']} with {project_data['leadsCount']} leads")
    print(f"      → Performance: {project_data['conversion_rate']:.1f}% conversion rate")
    print(f"      → Recommended: Digital channels for {project_data['tipeProyek']} projects")
    print()
    
    # Lead analysis impact
    print("📊 Lead Analysis Impact on AI Decisions:")
    print("-" * 40)
    
    if project_data['existingLeads']['statusDistribution']['CONVERTED'] > 5:
        print(f"   ✅ Strong Conversion History ({project_data['existingLeads']['statusDistribution']['CONVERTED']} converted leads):")
        print(f"      → Include success stories and testimonials")
        print(f"      → Leverage social proof and trust signals")
    
    if project_data['existingLeads']['statusDistribution']['INTERESTED'] > 10:
        print(f"   🔥 High Interest Volume ({project_data['existingLeads']['statusDistribution']['INTERESTED']} interested leads):")
        print(f"      → Focus on urgency and limited-time offers")
        print(f"      → Create scarcity and FOMO elements")
    
    print(f"   📊 AI CMO Generated Proposals Analysis:")
    for i, proposal in enumerate(proposals, 1):
        print(f"   {i}. {proposal.opsi_strategi}")
        print(f"      - Context Used: {project_data['namaProyek']} in {project_data['lokasi']}")
        print(f"      - Budget: Rp {proposal.estimasi_budget:,} (based on Rp {project_data['hargaStart':,})")
        print(f"      - Copy mentions: {'✅' if project_data['namaProyek'].lower() in proposal.copywriting.lower() else '❌'}")
        print(f"      - Location mentions: {'✅' if project_data['lokasi'].lower() in proposal.copywriting.lower() else '❌'}")
        print(f"      - Conversion-aware: {'✅' if 'conversion' in proposal.copywriting.lower() else '❌'}")
    
    print(f"\n✅ AI CMO Context-Aware Integration Completed!")
    print(f"\n🎯 Key Features Demonstrated:")
    print(f"  ✅ Context-aware AI prompting with full project data")
    print(f"  ✅ Performance data integration (leads, conversion, hot leads)")
    print(f"  ✅ Existing leads analysis for targeting refinement")
    print(f"  ✅ Location and price-based budget optimization")
    print(f"  ✅ Project type adaptation (KOMERSIL vs SUBSIDI)")
    print(f"  ✅ Single LLM call for all 3 strategies (efficient)")
    print(f"  ✅ Comprehensive context injection in AI prompts")
    print(f"  ✅ Database integration with full context storage")
    
    print(f"\n🚀 Business Impact:")
    print(f"  - Hyper-personalized ad proposals based on actual project data")
    print(f"  - Data-driven budget optimization")
    print(f"  - Performance-aware targeting strategies")
    print(f"  - Contextual copywriting that mentions project specifics")
    print(f"  - Efficient AI processing (single LLM call for all strategies)")
    print(f"  - Seamless integration with existing project data")
    
    print(f"\n🔗 Next Steps:")
    print(f"  1. Review generated proposals in project detail page")
    print(f"  2. Approve high-performing proposals")
    print(f"  3. Launch campaigns with optimized targeting")
    print(f"  4. Monitor performance and iterate based on results")

async def main():
    """Main function to run all examples"""
    await example_ai_cmo_integration()

if __name__ == "__main__":
    asyncio.run(main())
