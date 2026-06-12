"""
Twin-Dragon Engine - Scout Mode Example Usage
Demonstrates API_OFFICIAL, DIRECT_SCRAPE, and HYBRID integration
"""

import asyncio
import json
from datetime import datetime

# Import scout mode functions
from mass_scout import (
    run_official_api_scout, 
    run_direct_scrape, 
    run_hybrid_scout, 
    execute_scout_mode
)

async def example_scout_mode_operations():
    """Example of comprehensive scout mode operations"""
    
    print("🎯 Twin-Dragon Scout Mode Example")
    print("=" * 50)
    
    # Example project data
    project_data = {
        'id': 'project_123',
        'namaProyek': 'Grand Serang Residence',
        'tipeProyek': 'KOMERSIL',
        'namaWilayah': 'Serang',
        'latitude': -6.1256,
        'longitude': 106.1445,
        'radiusKm': 5,
        'scout_mode': 'HYBRID'
    }
    
    # Keywords for scouting
    keywords = [
        'property manager Serang',
        'real estate director',
        'investment analyst',
        'property developer'
    ]
    
    print(f"🎯 Target Project: {project_data['namaProyek']} ({project_data['tipeProyek']})")
    print(f"📍 Location: {project_data['namaWilayah']}")
    print(f"🔎 Keywords: {', '.join(keywords)}")
    print()
    
    # Test 1: API_OFFICIAL mode
    print("🔌 Testing API_OFFICIAL Mode:")
    print("-" * 30)
    
    api_results = await run_official_api_scout(keywords, project_data)
    print(f"  Status: {api_results.get('status', 'unknown')}")
    print(f"  Method: {api_results.get('method', 'N/A')}")
    print(f"  Leads Found: {api_results.get('leads_found', 0)}")
    print(f"  Message: {api_results.get('message', 'N/A')}")
    print()
    
    # Test 2: DIRECT_SCRAPE mode
    print("🕷️ Testing DIRECT_SCRAPE Mode:")
    print("-" * 30)
    
    scrape_results = await run_direct_scrape(keywords, project_data)
    print(f"  Status: {scrape_results.get('status', 'unknown')}")
    print(f"  Method: {scrape_results.get('method', 'N/A')}")
    print(f"  Leads Found: {scrape_results.get('leads_found', 0)}")
    print(f"  Targets Count: {len(scrape_results.get('targets', []))}")
    
    if scrape_results.get('targets'):
        print(f"  Sample Target: {scrape_results['targets'][0].get('business_name', 'Unknown')}")
    print()
    
    # Test 3: HYBRID mode
    print("🔀 Testing HYBRID Mode:")
    print("-" * 30)
    
    hybrid_results = await run_hybrid_scout(keywords, project_data)
    print(f"  Status: {hybrid_results.get('status', 'unknown')}")
    print(f"  Method: {hybrid_results.get('method', 'N/A')}")
    print(f"  Total API Leads: {hybrid_results.get('total_api_leads', 0)}")
    print(f"  Total Scraped Leads: {hybrid_results.get('total_scraped_leads', 0)}")
    print(f"  Deduplicated Leads: {hybrid_results.get('leads_found', 0)}")
    print(f"  Message: {hybrid_results.get('message', 'N/A')}")
    print()
    
    # Test 4: Execute scout mode by mode string
    print("🎯 Testing execute_scout_mode Function:")
    print("-" * 40)
    
    modes = ['API_OFFICIAL', 'DIRECT_SCRAPE', 'HYBRID']
    
    for mode in modes:
        print(f"\n  Executing {mode}:")
        results = await execute_scout_mode(keywords, mode, project_data)
        print(f"    Status: {results.get('status', 'unknown')}")
        print(f"    Leads Found: {results.get('leads_found', 0)}")
        
        if results.get('status') == 'failed':
            print(f"    Error: {results.get('error', 'Unknown error')}")
    
    print("\n📊 Scout Mode Comparison Summary:")
    print("-" * 40)
    
    # Compare results
    all_results = {
        'API_OFFICIAL': api_results,
        'DIRECT_SCRAPE': scrape_results,
        'HYBRID': hybrid_results
    }
    
    for mode, results in all_results.items():
        leads = results.get('leads_found', 0)
        status = results.get('status', 'unknown')
        status_icon = '✅' if status == 'completed' else '❌'
        
        print(f"  {mode}: {status_icon} {leads} leads")

async def main():
    """Main function to run all examples"""
    await example_scout_mode_operations()
    
    print("\n✅ All scout mode examples completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("  ✅ API_OFFICIAL: Official API integration (placeholder)")
    print("  ✅ DIRECT_SCRAPE: Web scraping with existing mass_scout")
    print("  ✅ HYBRID: Combined API + scraping with deduplication")
    print("  ✅ execute_scout_mode: Dynamic mode selection")
    print("  ✅ Project-aware logging to database")
    print("  ✅ Comprehensive error handling")
    print("  ✅ Detailed result reporting")

if __name__ == "__main__":
    asyncio.run(main())
