"""
Twin-Dragon Engine - AI Ads Manager Integration Example Usage
Demonstrates AI Chief Marketing Officer, proposal generation, and approval workflow
"""

import asyncio
import json
from datetime import datetime

# Import ads manager functions
from ads_manager import generate_ad_proposals, revise_proposal

async def example_ads_integration():
    """Example of comprehensive ads integration"""
    
    print("📢 Twin-Dragon AI Ads Manager Example")
    print("=" * 50)
    
    # Example project data
    project_data = {
        'id': 'project_123',
        'namaProyek': 'Grand Serang Residence',
        'tipeProyek': 'KOMERSIL',
        'lokasi': 'Serang',
        'hargaStart': 500000000,
        'targetMarket': 'Middle to Upper Class'
    }
    
    print(f"🏢 Target Project: {project_data['namaProyek']}")
    print(f"📍 Type: {project_data['tipeProyek']}")
    print(f"🌍 Location: {project_data['lokasi']}")
    print(f"💰 Price: Rp {project_data['hargaStart']:,}")
    print()
    
    # Test 1: Generate AI Ad Proposals
    print("🤖 AI Chief Marketing Officer - Proposal Generation:")
    print("-" * 50)
    
    proposals = await generate_ad_proposals(project_data)
    
    print(f"📊 Generated {len(proposals)} Ad Proposals:")
    for i, proposal in enumerate(proposals, 1):
        print(f"\n{i}. {proposal.opsi_strategi}")
        print(f"   Target: {proposal.target_audience}")
        print(f"   Budget: Rp {proposal.estimasi_budget:,}")
        print(f"   Copy: {proposal.copywriting}")
        print(f"   Channels: {', '.join(proposal.channel_rekomendasi)}")
        print(f"   KPI: {', '.join(proposal.kpi_utama)}")
        print(f"   Duration: {proposal.durasi_kampanye}")
    
    # Test 2: Simulate Approval Workflow
    print(f"\n🔄 Approval Workflow Simulation:")
    print("-" * 40)
    
    # Simulate API calls for approval workflow
    approval_steps = [
        {
            'action': 'GET /api/ads/proposals?status=PENDING',
            'description': 'Fetch pending proposals',
            'response': {'data': proposals, 'total': len(proposals), 'pending': len(proposals)}
        },
        {
            'action': 'POST /api/ads/proposals/proposal_1/approve',
            'description': 'Approve first proposal',
            'response': {'status': 'success', 'message': 'Proposal approved and launched successfully'}
        },
        {
            'action': 'POST /api/ads/proposals/proposal_2/reject',
            'description': 'Reject second proposal',
            'response': {'status': 'success', 'message': 'Proposal rejected successfully'}
        },
        {
            'action': 'POST /api/ads/proposals/proposal_3/revise',
            'description': 'Request revision for third proposal',
            'request': {'revisionInstructions': 'Make the copy more aggressive and increase budget by 20%'},
            'response': {'status': 'success', 'message': 'Proposal revision request submitted successfully'}
        }
    ]
    
    for step in approval_steps:
        print(f"\n  📡 {step['action']}")
        print(f"     {step['description']}")
        if 'request' in step:
            print(f"     Request: {json.dumps(step['request'], indent=6)}")
        print(f"     Response: {json.dumps(step['response'], indent=6)}")
    
    # Test 3: Revise Proposal
    print(f"\n✏️ AI Proposal Revision:")
    print("-" * 30)
    
    if proposals:
        proposal_id = "proposal_3"  # Simulate ID
        revision_instructions = "Make the copy more aggressive and increase budget by 20%"
        
        print(f"  Proposal ID: {proposal_id}")
        print(f"  Revision Instructions: {revision_instructions}")
        
        # Simulate revision (would call actual API in real implementation)
        revised_proposal = await revise_proposal(proposal_id, revision_instructions)
        
        if revised_proposal:
            print(f"  ✅ Revision Successful:")
            print(f"     New Strategy: {revised_proposal.opsi_strategi}")
            print(f"     New Budget: Rp {revised_proposal.estimasi_budget:,}")
            print(f"     New Copy: {revised_proposal.copywriting}")
        else:
            print(f"  ❌ Revision Failed")
    
    # Test 4: Strategy Analysis
    print(f"\n📈 Strategy Analysis:")
    print("-" * 25)
    
    strategy_comparison = {
        'Agresif': {
            'budget_multiplier': 1.5,
            'target_audience': 'High-intent buyers with strong purchasing power',
            'tone': 'Bold, urgent, and compelling',
            'channels': ['Google Ads', 'Facebook Ads', 'Instagram Ads'],
            'campaign_duration': '2-4 weeks intensive'
        },
        'Seimbang': {
            'budget_multiplier': 1.0,
            'target_audience': 'General property seekers with moderate interest',
            'tone': 'Professional, informative, and trustworthy',
            'channels': ['Google Ads', 'Facebook Ads', 'Content Marketing'],
            'campaign_duration': '4-6 weeks sustained'
        },
        'Hemat': {
            'budget_multiplier': 0.7,
            'target_audience': 'Budget-conscious first-time homebuyers',
            'tone': 'Friendly, helpful, and value-focused',
            'channels': ['Facebook Ads', 'Instagram Ads', 'WhatsApp Marketing'],
            'campaign_duration': '6-8 weeks nurturing'
        }
    }
    
    for strategy, details in strategy_comparison.items():
        print(f"\n  🎯 {strategy} Strategy:")
        print(f"     Budget Multiplier: {details['budget_multiplier']}x")
        print(f"     Target: {details['target_audience']}")
        print(f"     Tone: {details['tone']}")
        print(f"     Channels: {', '.join(details['channels'])}")
        print(f"     Duration: {details['campaign_duration']}")
    
    # Test 5: Project Type Adaptation
    print(f"\n🏗️ Project Type Adaptation:")
    print("-" * 30)
    
    project_type_adaptation = {
        'KOMERSIL': {
            'focus': ['Investment', 'Prestige', 'Luxury', 'Business Opportunity'],
            'keywords': ['properti komersial', 'investasi properti', 'usaha', 'bisnis'],
            'call_to_action': ['Hubungi Kami Sekarang', 'Dapatkan Penawaran Terbaik', 'Investasi Cerdas']
        },
        'SUBSIDI': {
            'focus': ['Affordable', 'Family', 'Comfort', 'Government Support'],
            'keywords': ['rumah subsidi', 'KPR FLPP', 'cicilan ringan', 'keluarga'],
            'call_to_action': ['Dapatkan Rumah Impian', 'Cicilan Ringan', 'Promo Pemerintah']
        }
    }
    
    for project_type, adaptation in project_type_adaptation.items():
        print(f"\n  🏠 {project_type} Projects:")
        print(f"     Focus: {', '.join(adaptation['focus'])}")
        print(f"     Keywords: {', '.join(adaptation['keywords'])}")
        print(f"     CTA: {', '.join(adaptation['call_to_action'])}")
    
    # Test 6: Budget Calculation
    print(f"\n💰 Budget Calculation Examples:")
    print("-" * 35)
    
    base_price = project_data['hargaStart']
    budget_examples = [
        {'strategy': 'Agresif', 'multiplier': 1.5},
        {'strategy': 'Seimbang', 'multiplier': 1.0},
        {'strategy': 'Hemat', 'multiplier': 0.7}
    ]
    
    for example in budget_examples:
        budget = int(base_price * 0.01 * example['multiplier'])
        min_budget = max(budget, 10000000)
        
        print(f"  📊 {example['strategy']} Strategy:")
        print(f"     Base Price: Rp {base_price:,}")
        print(f"     Budget Multiplier: {example['multiplier']}x")
        print(f"     Calculated Budget: Rp {budget:,}")
        print(f"     Final Budget: Rp {min_budget:,} (min 10M)")
    
    print(f"\n✅ AI Ads Manager Integration Examples Completed!")
    print(f"\n🎯 Key Features Demonstrated:")
    print(f"  ✅ AI Chief Marketing Officer proposal generation")
    print(f"  ✅ Multi-strategy ad proposals (Agresif/Seimbang/Hemat)")
    print(f"  ✅ Project type adaptation (KOMERSIL/SUBSIDI)")
    print(f"  ✅ Budget calculation and optimization")
    print(f"  ✅ Approval workflow simulation")
    print(f"  ✅ Proposal revision with AI assistance")
    print(f"  ✅ Strategy analysis and comparison")
    
    print(f"\n🚀 Business Impact:")
    print(f"  - Automated ad proposal generation saves time")
    print(f"  - AI-powered copywriting increases effectiveness")
    print(f"  - Multi-strategy approach optimizes budget allocation")
    print(f"  - Human-in-the-loop approval ensures quality control")
    print(f"  - Revision capability allows continuous improvement")
    print(f"  - Project type adaptation ensures relevance")

async def main():
    """Main function to run all examples"""
    await example_ads_integration()

if __name__ == "__main__":
    asyncio.run(main())
