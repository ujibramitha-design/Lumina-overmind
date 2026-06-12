#!/usr/bin/env python3
"""
Lumina OS - Incoming Leads Simulation Script
Simulates webhook calls from different marketing platforms

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any

# Configuration
WEBHOOK_URL = "http://localhost:5000/api/webhook/incoming-lead"
WEBHOOK_TOKEN = "DUMMY-TOKEN-123"
API_TIMEOUT = 30  # seconds

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message: str, color: str = Colors.END):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def print_header():
    """Print simulation header"""
    print_colored("=" * 80, Colors.BOLD)
    print_colored("🚀 LUMINA OS - INCOMING LEADS SIMULATION", Colors.BOLD)
    print_colored("   Intake Engine - Webhook Simulation", Colors.BLUE)
    print_colored("=" * 80, Colors.BOLD)
    print()

def print_lead_header(lead_number: int, source: str, expected_category: str):
    """Print lead simulation header"""
    print_colored(f"📊 LEAD #{lead_number}: {source}", Colors.YELLOW)
    print_colored(f"   Expected Category: {expected_category}", Colors.BLUE)
    print("-" * 50)

def create_test_leads() -> list[Dict[str, Any]]:
    """
    Create test lead data for different marketing platforms
    
    Returns:
        list: List of test lead dictionaries
    """
    test_leads = [
        {
            # Lead 1: Facebook Ads - High quality (Hot)
            "nama": "Budi Santoso, S.T.",
            "no_hp": "08123456789",
            "email": "budi.santoso@engineering.co.id",
            "sumber": "Facebook Ads",
            "campaign": "Summer Property Promo 2024",
            "catatan": "Saya tertarik dengan tipe 36/72, sudah siap DP 30%. Pekerjaan sebagai PNS di Kementerian PU, penghasilan stabil. Lokasi di Serang dekat kantor.",
            "lokasi": "Serang",
            "pekerjaan": "PNS",
            "expected_category": "Hot",
            "description": "Data sangat lengkap, pekerjaan PNS, lokasi jelas, siap DP"
        },
        {
            # Lead 2: TikTok Ads - Medium quality (Warm)
            "nama": "Sarah Putri",
            "no_hp": "08234567890",
            "email": "sarah.putri@gmail.com",
            "sumber": "TikTok Ads",
            "campaign": "Gen Z Property Hunt",
            "catatan": "Cari rumah untuk keluarga muda, budget 300-400 juta. Lokasi preferensi Serang atau sekitarnya.",
            "lokasi": "Serang",
            "pekerjaan": "Wirausaha",
            "expected_category": "Warm",
            "description": "Data standar, ada email dan catatan jelas, budget spesifik"
        },
        {
            # Lead 3: Organic Web - Low quality (Cold)
            "nama": "Rudi",
            "no_hp": "08345678901",
            "email": "",
            "sumber": "Organic Web",
            "campaign": "",
            "catatan": "",
            "lokasi": "",
            "pekerjaan": "",
            "expected_category": "Cold",
            "description": "Data minim, hanya nama dan telepon, tidak ada email atau catatan"
        }
    ]
    
    return test_leads

def send_webhook_request(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send webhook request to Lumina OS
    
    Args:
        lead_data: Dictionary containing lead information
        
    Returns:
        Dict: Response from webhook
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Lumina-Token': WEBHOOK_TOKEN
    }
    
    try:
        print_colored(f"📤 Sending webhook request...", Colors.BLUE)
        print_colored(f"   URL: {WEBHOOK_URL}", Colors.BLUE)
        print_colored(f"   Token: {WEBHOOK_TOKEN}", Colors.BLUE)
        print()
        
        # Print lead data
        print_colored("📋 Lead Data:", Colors.YELLOW)
        for key, value in lead_data.items():
            if key != 'expected_category' and key != 'description':
                print_colored(f"   {key}: {value}", Colors.END)
        print()
        
        # Send request
        response = requests.post(
            WEBHOOK_URL,
            json=lead_data,
            headers=headers,
            timeout=API_TIMEOUT
        )
        
        return {
            'success': True,
            'status_code': response.status_code,
            'response_data': response.json() if response.content else None,
            'response_headers': dict(response.headers)
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout',
            'status_code': None
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Connection error - Is Lumina OS running?',
            'status_code': None
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e),
            'status_code': None
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'JSON decode error: {str(e)}',
            'status_code': None
        }

def process_webhook_response(response: Dict[str, Any], lead_data: Dict[str, Any]):
    """
    Process and display webhook response
    
    Args:
        response: Webhook response dictionary
        lead_data: Original lead data
    """
    if not response['success']:
        print_colored(f"❌ WEBHOOK FAILED: {response['error']}", Colors.RED)
        if response['status_code']:
            print_colored(f"   Status Code: {response['status_code']}", Colors.RED)
        print()
        return False
    
    # Success case
    print_colored(f"✅ WEBHOOK SUCCESS!", Colors.GREEN)
    print_colored(f"   Status Code: {response['status_code']}", Colors.GREEN)
    
    if response['response_data']:
        data = response['response_data']
        print_colored(f"   Lead ID: {data.get('data', {}).get('lead_id', 'N/A')}", Colors.GREEN)
        print_colored(f"   Name: {data.get('data', {}).get('nama', 'N/A')}", Colors.GREEN)
        print_colored(f"   Score: {data.get('data', {}).get('skor_akhir', 'N/A')}", Colors.GREEN)
        print_colored(f"   Category: {data.get('data', {}).get('kategori', 'N/A')}", Colors.GREEN)
        print_colored(f"   Processed: {data.get('data', {}).get('waktu_proses', 'N/A')}", Colors.GREEN)
        
        # Compare expected vs actual category
        expected = lead_data.get('expected_category', 'Unknown')
        actual = data.get('data', {}).get('kategori', 'Unknown')
        
        if expected.lower() == actual.lower():
            print_colored(f"   🎯 Category Match: Expected '{expected}' = Actual '{actual}' ✅", Colors.GREEN)
        else:
            print_colored(f"   ⚠️  Category Mismatch: Expected '{expected}' ≠ Actual '{actual}'", Colors.YELLOW)
    
    print()
    return True

def run_simulation():
    """Run the complete lead simulation"""
    print_header()
    
    # Check if Lumina OS is running
    print_colored("🔍 Checking Lumina OS connection...", Colors.BLUE)
    try:
        response = requests.get(f"{WEBHOOK_URL.replace('/incoming-lead', '/health')}", timeout=5)
        if response.status_code == 200:
            print_colored("✅ Lumina OS is running and healthy!", Colors.GREEN)
        else:
            print_colored(f"⚠️  Lumina OS responded with status {response.status_code}", Colors.YELLOW)
    except:
        print_colored("❌ Cannot connect to Lumina OS. Make sure it's running on http://localhost:5000", Colors.RED)
        print_colored("   Run: python lumina_os/api/__init__.py", Colors.YELLOW)
        return
    
    print()
    
    # Get test leads
    test_leads = create_test_leads()
    
    # Statistics
    total_leads = len(test_leads)
    successful_leads = 0
    failed_leads = 0
    
    print_colored(f"🚀 Starting simulation with {total_leads} test leads...", Colors.BOLD)
    print()
    
    # Process each lead
    for i, lead in enumerate(test_leads, 1):
        print_lead_header(i, lead['sumber'], lead['expected_category'])
        print_colored(f"📝 Description: {lead['description']}", Colors.BLUE)
        print()
        
        # Send webhook request
        response = send_webhook_request(lead)
        
        # Process response
        if process_webhook_response(response, lead):
            successful_leads += 1
        else:
            failed_leads += 1
        
        # Add delay between requests (except last one)
        if i < total_leads:
            print_colored("⏳ Waiting 2 seconds before next lead...", Colors.YELLOW)
            time.sleep(2)
            print()
    
    # Print summary
    print_colored("=" * 80, Colors.BOLD)
    print_colored("📊 SIMULATION SUMMARY", Colors.BOLD)
    print_colored("=" * 80, Colors.BOLD)
    print_colored(f"Total Leads Processed: {total_leads}", Colors.END)
    print_colored(f"✅ Successful: {successful_leads}", Colors.GREEN)
    print_colored(f"❌ Failed: {failed_leads}", Colors.RED)
    print_colored(f"📈 Success Rate: {(successful_leads/total_leads)*100:.1f}%", Colors.BLUE)
    print_colored(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.END)
    print_colored("=" * 80, Colors.BOLD)
    
    if failed_leads > 0:
        print_colored("\n⚠️  Some leads failed to process. Check Lumina OS logs for details.", Colors.YELLOW)
        print_colored("   Logs location: logs/api.log", Colors.YELLOW)
    else:
        print_colored("\n🎉 All leads processed successfully! Check Lumina OS dashboard to see the results.", Colors.GREEN)

def main():
    """Main function"""
    try:
        run_simulation()
    except KeyboardInterrupt:
        print_colored("\n\n⏹️  Simulation interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n💥 Unexpected error: {str(e)}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
