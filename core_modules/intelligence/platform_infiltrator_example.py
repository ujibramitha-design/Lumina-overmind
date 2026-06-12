"""
Twin-Dragon Engine - Platform Infiltrator Example Usage
Demonstrates advanced platform-specific scraping with data enrichment
"""

import asyncio
import json
from datetime import datetime

# Import the platform infiltrator
from platform_infiltrator import platform_infiltrator, scrape_linkedin, scrape_facebook, scrape_government
from mass_scout import infiltrate_platforms

async def example_platform_infiltration():
    """Example of comprehensive platform infiltration"""
    
    print("🎭 Twin-Dragon Platform Infiltration Example")
    print("=" * 50)
    
    # Example project data
    project_data = {
        'id': 'project_123',
        'namaProyek': 'Grand Serang Residence',
        'tipeProyek': 'KOMERSIL',
        'namaWilayah': 'Serang',
        'latitude': -6.1256,
        'longitude': 106.1445,
        'radiusKm': 5
    }
    
    # Keywords for infiltration
    keywords = [
        'property manager',
        'real estate director',
        'investment analyst',
        'property developer'
    ]
    
    print(f"🔍 Target Project: {project_data['namaProyek']} ({project_data['tipeProyek']})")
    print(f"📍 Location: {project_data['namaWilayah']}")
    print(f"🔎 Keywords: {', '.join(keywords)}")
    print()
    
    # 1. LinkedIn Infiltration
    print("🔗 LinkedIn Infiltration")
    print("-" * 25)
    
    linkedin_contacts = await scrape_linkedin(
        search_query="property manager Serang",
        max_profiles=5
    )
    
    print(f"✅ LinkedIn: {len(linkedin_contacts)} contacts extracted")
    
    for i, contact in enumerate(linkedin_contacts[:2], 1):
        print(f"  {i}. {contact.get('nama', 'Unknown')}")
        print(f"     Position: {contact.get('jabatan', 'N/A')}")
        print(f"     Phone: {contact.get('nomor_hp', 'N/A')}")
        print(f"     Email: {contact.get('email', 'N/A')}")
        print(f"     Platform: {contact.get('platform_sumber', 'LinkedIn')}")
        print(f"     Confidence: {contact.get('confidence_score', 0):.2f}")
        print()
    
    # 2. Facebook Group Infiltration
    print("📘 Facebook Group Infiltration")
    print("-" * 30)
    
    facebook_contacts = await scrape_facebook(
        group_search="jual beli properti Serang",
        max_posts=10
    )
    
    print(f"✅ Facebook: {len(facebook_contacts)} contacts extracted")
    
    for i, contact in enumerate(facebook_contacts[:2], 1):
        print(f"  {i}. {contact.get('nama', 'Unknown')}")
        print(f"     Position: {contact.get('jabatan', 'Facebook Group Member')}")
        print(f"     Phone: {contact.get('nomor_hp', 'N/A')}")
        print(f"     Email: {contact.get('email', 'N/A')}")
        print(f"     Platform: {contact.get('platform_sumber', 'Facebook')}")
        print()
    
    # 3. Government Directory Infiltration
    print("🏛️ Government Directory Infiltration")
    print("-" * 35)
    
    gov_contacts = await scrape_government(
        institution_type='pemda',
        location='Serang',
        max_contacts=10
    )
    
    print(f"✅ Government: {len(gov_contacts)} contacts extracted")
    
    for i, contact in enumerate(gov_contacts[:2], 1):
        print(f"  {i}. {contact.get('nama', 'Unknown')}")
        print(f"     Position: {contact.get('jabatan', 'N/A')}")
        print(f"     Phone: {contact.get('nomor_hp', 'N/A')}")
        print(f"     Email: {contact.get('email', 'N/A')}")
        print(f"     Platform: {contact.get('platform_sumber', 'Government Directory')}")
        print()
    
    # 4. Integrated Platform Infiltration (Mass Scout Integration)
    print("🎭 Integrated Platform Infiltration")
    print("-" * 35)
    
    integrated_contacts = await infiltrate_platforms(
        keywords=keywords,
        platforms=['linkedin', 'facebook', 'government'],
        project_data=project_data
    )
    
    print(f"✅ Integrated: {len(integrated_contacts)} total contacts extracted")
    
    # 5. Rich JSON Data Format Example
    print("📊 Rich JSON Data Format")
    print("-" * 25)
    
    example_contact = {
        "nama": "John Doe",
        "nomor_hp": "+628123456789",
        "email": "john.doe@company.com",
        "jabatan": "Property Manager",
        "platform_sumber": "LinkedIn",
        "lokasi": "Serang",
        "perusahaan": "PT. Property Indonesia",
        "headline": "Property Manager at PT. Property Indonesia",
        "url": "https://linkedin.com/in/johndoe",
        "extracted_at": datetime.now().isoformat(),
        "confidence_score": 0.85,
        "project_id": project_data['id'],
        "project_name": project_data['namaProyek'],
        "project_type": project_data['tipeProyek'],
        "enriched_at": datetime.now().isoformat(),
        "data_quality_score": 0.9,
        "contact_priority": "HIGH"
    }
    
    print("Example Rich JSON Contact Data:")
    print(json.dumps(example_contact, indent=2))
    
    print("\n🎯 Platform Infiltration Summary:")
    print(f"   LinkedIn: {len(linkedin_contacts)} contacts")
    print(f"   Facebook: {len(facebook_contacts)} contacts")
    print(f"   Government: {len(gov_contacts)} contacts")
    print(f"   Integrated: {len(integrated_contacts)} contacts")
    print(f"   Total: {len(linkedin_contacts) + len(facebook_contacts) + len(gov_contacts)} contacts")
    
    print("\n✅ Platform infiltration example completed!")

async def main():
    """Main function to run the example"""
    await example_platform_infiltration()

if __name__ == "__main__":
    asyncio.run(main())
