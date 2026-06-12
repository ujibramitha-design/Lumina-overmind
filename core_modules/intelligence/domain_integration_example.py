"""
Twin-Dragon Engine - Domain Integration Example Usage
Demonstrates public landing page, webhook, green-zone dorking, and AI prompt injection
"""

import asyncio
import json
from datetime import datetime

# Import domain integration functions
from mass_scout import green_zone_dorking

async def example_domain_integration():
    """Example of comprehensive domain integration"""
    
    print("🌐 Twin-Dragon Domain Integration Example")
    print("=" * 50)
    
    # Test 1: Green-Zone Dorking for KOMERSIL
    print("\n🌱 Testing Green-Zone Dorking - KOMERSIL:")
    print("-" * 40)
    
    komersil_results = await green_zone_dorking(
        project_type='KOMERSIL',
        area='Jakarta Selatan',
        max_results=10
    )
    
    print(f"  Status: {komersil_results.get('status', 'unknown')}")
    print(f"  Method: {komersil_results.get('method', 'N/A')}")
    print(f"  Total Queries: {komersil_results.get('total_queries', 0)}")
    print(f"  Success Rate: {komersil_results.get('success_rate', 0):.2%}")
    print(f"  Contacts Found: {komersil_results.get('deduplicated_results', 0)}")
    
    if komersil_results.get('contacts'):
        print(f"  Sample Contact: {komersil_results['contacts'][0].get('nama', 'Unknown')}")
        print(f"  Phone: {komersil_results['contacts'][0].get('nomor_hp', 'N/A')}")
    
    # Test 2: Green-Zone Dorking for SUBSIDI
    print("\n🌱 Testing Green-Zone Dorking - SUBSIDI:")
    print("-" * 40)
    
    subsidi_results = await green_zone_dorking(
        project_type='SUBSIDI',
        area='Bandung',
        max_results=10
    )
    
    print(f"  Status: {subsidi_results.get('status', 'unknown')}")
    print(f"  Method: {subsidi_results.get('method', 'N/A')}")
    print(f"  Total Queries: {subsidi_results.get('total_queries', 0)}")
    print(f"  Success Rate: {subsidi_results.get('success_rate', 0):.2%}")
    print(f"  Contacts Found: {subsidi_results.get('deduplicated_results', 0)}")
    
    if subsidi_results.get('contacts'):
        print(f"  Sample Contact: {subsidi_results['contacts'][0].get('nama', 'Unknown')}")
        print(f"  Email: {subsidi_results['contacts'][0].get('email', 'N/A')}")
    
    # Test 3: Simulate Public Landing Page Submission
    print("\n🌐 Simulating Public Landing Page Submission:")
    print("-" * 40)
    
    # Simulate form data
    landing_page_data = {
        'nama': 'John Doe',
        'nomor_hp': '08123456789',
        'project_id': 'project_123',
        'project_type': 'KOMERSIL',
        'source': 'landing_page_public'
    }
    
    print(f"  Name: {landing_page_data['nama']}")
    print(f"  Phone: {landing_page_data['nomor_hp']}")
    print(f"  Project Type: {landing_page_data['project_type']}")
    print(f"  Source: {landing_page_data['source']}")
    
    # Simulate webhook call
    print("\n📡 Simulating Webhook Call to /api/leads/public-submit:")
    print("-" * 40)
    
    webhook_payload = {
        'nama': landing_page_data['nama'],
        'nomor_hp': landing_page_data['nomor_hp'],
        'project_id': landing_page_data['project_id'],
        'project_type': landing_page_data['project_type'],
        'source': landing_page_data['source']
    }
    
    print(f"  Endpoint: POST /api/leads/public-submit")
    print(f"  Payload: {json.dumps(webhook_payload, indent=2)}")
    
    # Simulate webhook response
    webhook_response = {
        "status": "success",
        "message": "Lead submitted successfully",
        "lead_id": "lead_123",
        "data": {
            "id": "lead_123",
            "nama": "John Doe",
            "nomor_hp": "08123456789",
            "project_id": "project_123",
            "project_type": "KOMERSIL",
            "status": "NEW",
            "created_at": datetime.now().isoformat()
        }
    }
    
    print(f"  Response: {json.dumps(webhook_response, indent=2)}")
    
    # Test 4: AI Prompt Injection Simulation
    print("\n🤖 AI Prompt Injection Simulation:")
    print("-" * 40)
    
    # Simulate AI greeting with domain injection
    ai_greetings = {
        'KOMERSIL': [
            "Selamat pagi Bapak/Ibu, terima kasih sudah menghubungi kami. Untuk melihat e-brosur lengkap dan simulasi KPR, kunjungi: https://domain-anda.com/komersil",
            "Halo Bapak/Ibu, saya siap membantu Anda. Untuk info lengkap dan simulasi cicilan, akses: https://domain-anda.com/komersil"
        ],
        'SUBSIDI': [
            "Selamat pagi Kakak/Mas/Mbak, senang bisa membantu Anda. Untuk melihat e-brosur lengkap dan simulasi cicilan, kunjungi: https://domain-anda.com/subsidi",
            "Halo Kakak, saya siap membantu menemukan rumah impian Anda. Untuk info lengkap dan simulasi cicilan, akses: https://domain-anda.com/subsidi"
        ]
    }
    
    for project_type, greetings in ai_greetings.items():
        print(f"\n  {project_type} Greeting Examples:")
        for i, greeting in enumerate(greetings, 1):
            print(f"    {i}. {greeting}")
    
    print(f"\n  Domain Marketing Rules:")
    print(f"    - WAJIB menyisipkan link domain dalam setiap pesan pertama")
    print(f"    - Selalu arahkan prospek untuk mengklik link domain")
    print(f"    - Prioritaskan domain link dalam setiap response greeting")
    
    # Test 5: Integration Flow Demonstration
    print("\n🔄 Integration Flow Demonstration:")
    print("-" * 40)
    
    print(f"  Step 1: Public Landing Page → Form Submission")
    print(f"  Step 2: Webhook /api/leads/public-submit → Database Storage")
    print(f"  Step 3: AI Response with Domain Injection → Prospect Engagement")
    print(f"  Step 4: Green-Zone Dorking → Lead Generation")
    print(f"  Step 5: Multi-channel Marketing → Conversion")
    
    print(f"\n📊 Integration Summary:")
    print(f"  Public Landing Page: ✅ Available")
    print(f"  Public Webhook: ✅ Available")
    print(f"  Green-Zone Dorking: ✅ Available")
    print(f"  AI Prompt Injection: ✅ Available")
    print(f"  Domain Marketing: ✅ Available")
    
    print(f"\n🎯 Business Impact:")
    print(f"  - Public lead capture without login requirement")
    print(f"  - Real-time lead storage and processing")
    print(f"  - Advanced dorking for targeted lead generation")
    print(f"  - AI-powered domain marketing automation")
    print(f"  - Complete integration pipeline")

async def main():
    """Main function to run all examples"""
    await example_domain_integration()
    
    print("\n✅ All domain integration examples completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("  ✅ Public Landing Page with lead capture form")
    print("  ✅ Public webhook endpoint for lead submission")
    print("  ✅ Green-zone dorking with strict parameters")
    print("  ✅ AI prompt injection for domain marketing")
    print("  ✅ Complete integration pipeline")
    print("  ✅ Multi-channel lead generation")

if __name__ == "__main__":
    asyncio.run(main())
