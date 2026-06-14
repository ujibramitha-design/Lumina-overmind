#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Lead Simulation Script
Simulates incoming webhook leads with hacker aesthetic terminal output
"""

import requests
import json
import time
import random
import sys
from datetime import datetime

# ANSI Color Codes for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    END = '\033[0m'

def print_hacker(message, color='cyan'):
    """Print message with hacker aesthetic"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    prefix = f"{Colors.DIM}[{timestamp}]{Colors.END}"
    color_code = getattr(Colors, color.upper(), Colors.CYAN)
    print(f"{prefix} {color_code}►{Colors.END} {color_code}{message}{Colors.END}")

def print_success(message):
    print_hacker(f"✅ {message}", 'green')

def print_error(message):
    print_hacker(f"❌ {message}", 'red')

def print_warning(message):
    print_hacker(f"⚠️  {message}", 'yellow')

def print_info(message):
    print_hacker(f"ℹ️  {message}", 'blue')

def print_header(message):
    print_hacker(f"🔧 {message}", 'magenta')

def print_separator(char='═', length=80):
    print(f"{Colors.CYAN}{char * length}{Colors.END}")

def typewriter_effect(text, delay=0.03):
    """Create typewriter effect for text"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def create_payloads():
    """Create dummy lead payloads according to Fase 3 specifications"""
    
    # Lead 1 (Hot): Budi Santoso, PNS, Serang, Facebook Ads
    lead_1 = {
        "nama": "Budi Santoso",
        "no_hp": "08123456789",
        "email": "budi.santoso@gmail.com",
        "sumber": "Facebook Ads",
        "campaign": "PNS_Property_Promo_2026",
        "catatan": "Sangat tertarik dengan rumah subsidi PNS, lokasi strategis dekat kantor, butuh KPR dengan bunga rendah, siap bayar DP 20%",
        "lokasi": "Serang",
        "pekerjaan": "PNS"
    }
    
    # Lead 2 (Warm): Sarah Putri, Wirausaha, TikTok Ads
    lead_2 = {
        "nama": "Sarah Putri",
        "no_hp": "08234567890",
        "email": "sarah.putri@yahoo.com",
        "sumber": "TikTok Ads",
        "campaign": "Entrepreneur_Home_Series",
        "catatan": "Mencari rumah untuk investasi, lokasi di area Jabodetabek, budget 500-800 juta, prefer cluster dengan fasilitas lengkap, butuh cicilan ringan",
        "lokasi": "Jakarta",
        "pekerjaan": "Wirausaha"
    }
    
    # Lead 3 (Cold): Rudi, Organic Web (data minim)
    lead_3 = {
        "nama": "Rudi",
        "no_hp": "08345678901",
        "email": None,
        "sumber": "Organic Web",
        "campaign": None,
        "catatan": None,
        "lokasi": None,
        "pekerjaan": None
    }
    
    return [lead_1, lead_2, lead_3]

def simulate_network_delay():
    """Simulate realistic network delay"""
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)

def send_lead_to_webhook(payload, headers, url):
    """Send lead to webhook endpoint with detailed logging"""
    
    # Print lead info
    print_hacker(f"📦 Preparing payload: {payload['nama']}", 'yellow')
    print_hacker(f"   Source: {payload['sumber']}", 'dim')
    print_hacker(f"   Phone: {payload['no_hp']}", 'dim')
    
    if payload.get('pekerjaan'):
        print_hacker(f"   Occupation: {payload['pekerjaan']}", 'dim')
    if payload.get('lokasi'):
        print_hacker(f"   Location: {payload['lokasi']}", 'dim')
    if payload.get('campaign'):
        print_hacker(f"   Campaign: {payload['campaign']}", 'dim')
    
    print_hacker("🚀 Mengirim data lead...", 'cyan')
    print_hacker(f"   Target: {url}", 'dim')
    print_hacker(f"   Headers: {headers}", 'dim')
    
    try:
        # Simulate network delay
        simulate_network_delay()
        
        # Send request
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # Print response status
        if response.status_code == 201:
            print_success(f"Status: {response.status_code} Created")
        elif response.status_code == 200:
            print_success(f"Status: {response.status_code} OK")
        elif response.status_code == 401:
            print_error(f"Status: {response.status_code} Unauthorized")
            print_error("   Token validation failed!")
            return None
        elif response.status_code == 422:
            print_error(f"Status: {response.status_code} Unprocessable Entity")
            print_error("   Payload validation failed!")
            return None
        else:
            print_warning(f"Status: {response.status_code}")
        
        # Parse and display response
        try:
            response_data = response.json()
            
            if response_data.get("success"):
                data = response_data.get("data", {})
                
                # Display lead processing results
                print_hacker("📊 Processing Results:", 'green')
                print_hacker(f"   Lead ID: {data.get('lead_id', 'N/A')}", 'dim')
                print_hacker(f"   Name: {data.get('nama', 'N/A')}", 'dim')
                print_hacker(f"   Score: {data.get('score', 'N/A')}", 'dim')
                
                # Color code based on score
                score = data.get('score', 0)
                status = data.get('status', 'Unknown')
                
                if score >= 80:
                    status_color = 'green'
                    status_icon = '🔥'
                elif score >= 60:
                    status_color = 'yellow'
                    status_icon = '⚡'
                else:
                    status_color = 'blue'
                    status_icon = '❄️'
                
                print_hacker(f"   Status: {status_icon} {status}", status_color)
                
                # Display keywords found
                keywords = data.get('keywords_found', [])
                if keywords:
                    print_hacker("   Keywords Found:", 'dim')
                    for keyword in keywords:
                        print_hacker(f"     • {keyword}", 'dim')
                
                # Display processing time
                processed_at = data.get('processed_at')
                if processed_at:
                    print_hacker(f"   Processed: {processed_at}", 'dim')
                
                print_success("Lead processing completed successfully!")
                
            else:
                print_error("Lead processing failed!")
                error_detail = response_data.get("detail", "Unknown error")
                print_hacker(f"   Error: {error_detail}", 'dim')
                
        except json.JSONDecodeError:
            print_error("Failed to parse JSON response")
            print_hacker(f"   Raw response: {response.text[:200]}...", 'dim')
        
        print_separator()
        return response_data
        
    except requests.exceptions.Timeout:
        print_error("Request timeout!")
        print_hacker("   Connection timed out after 10 seconds", 'dim')
        return None
        
    except requests.exceptions.ConnectionError:
        print_error("Connection error!")
        print_hacker("   Failed to connect to webhook server", 'dim')
        print_hacker("   Make sure the API server is running", 'dim')
        return None
        
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return None

def main():
    """Main simulation function"""
    
    # Print header with typewriter effect
    print_separator('═')
    print()
    typewriter_effect("🔐 HUNTER AGENT AI MARKETING DIGITAL - LEAD SIMULATION SYSTEM", 0.02)
    typewriter_effect("🚀 FASE 3: THE INTAKE ENGINE - WEBHOOK SIMULATOR", 0.02)
    print_separator('═')
    print()
    
    # Configuration
    print_hacker("🔧 System Configuration:", 'magenta')
    url = "http://localhost:8000/api/webhook/incoming-lead"
    headers = {
        'Content-Type': 'application/json',
        'X-Lumina-Token': 'DUMMY-TOKEN-123'
    }
    
    print_hacker(f"   Target URL: {url}", 'dim')
    print_hacker(f"   Auth Token: {headers['X-Lumina-Token']}", 'dim')
    print_hacker(f"   Content-Type: {headers['Content-Type']}", 'dim')
    print()
    
    # Create payloads
    print_hacker("📦 Loading Lead Payloads:", 'magenta')
    payloads = create_payloads()
    
    lead_descriptions = [
        "🔥 HOT LEAD - Budi Santoso (PNS, Serang, Facebook Ads)",
        "⚡ WARM LEAD - Sarah Putri (Wirausaha, TikTok Ads)",
        "❄️ COLD LEAD - Rudi (Organic Web, Minimal Data)"
    ]
    
    for i, (payload, description) in enumerate(zip(payloads, lead_descriptions), 1):
        print_hacker(f"   Lead {i}: {description}", 'dim')
    
    print()
    print_separator('─')
    print()
    
    # Check API health first
    print_hacker("🔍 Checking API Health...", 'blue')
    try:
        health_response = requests.get("http://localhost:8000/api/webhook/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print_success("API Health Check Passed")
            print_hacker(f"   Service: {health_data.get('service', 'Unknown')}", 'dim')
            print_hacker(f"   Version: {health_data.get('version', 'Unknown')}", 'dim')
        else:
            print_warning(f"Health check returned: {health_response.status_code}")
    except:
        print_error("API Health Check Failed")
        print_hacker("   Make sure the API server is running on port 8000", 'dim')
        print_hacker("   Run: python api/main.py", 'dim')
        print()
        return 1
    
    print()
    print_separator('─')
    print()
    
    # Send leads
    print_hacker("🚀 Starting Lead Transmission Sequence...", 'cyan')
    print()
    
    successful_leads = 0
    failed_leads = 0
    
    for i, (payload, description) in enumerate(zip(payloads, lead_descriptions), 1):
        print_hacker(f"📡 TRANSMISSION {i}/3: {description}", 'cyan')
        print_separator('─')
        
        result = send_lead_to_webhook(payload, headers, url)
        
        if result and result.get("success"):
            successful_leads += 1
        else:
            failed_leads += 1
        
        # Add delay between transmissions
        if i < len(payloads):
            delay = random.uniform(1.0, 3.0)
            print_hacker(f"⏳ Waiting {delay:.1f} seconds before next transmission...", 'yellow')
            time.sleep(delay)
            print()
    
    # Final summary
    print_separator('═')
    print()
    print_hacker("🎯 TRANSMISSION SUMMARY", 'magenta')
    print_separator('─')
    print_hacker(f"📊 Total Leads Processed: {len(payloads)}", 'dim')
    print_success(f"✅ Successful: {successful_leads}")
    
    if failed_leads > 0:
        print_error(f"❌ Failed: {failed_leads}")
    else:
        print_hacker("❌ Failed: 0", 'dim')
    
    print_hacker(f"📈 Success Rate: {(successful_leads/len(payloads)*100):.1f}%", 'dim')
    
    if successful_leads == len(payloads):
        print_success("🎉 All leads transmitted successfully!")
        print_hacker("🔥 Lead Intake Engine is fully operational!", 'green')
    else:
        print_warning("⚠️  Some leads failed to transmit")
        print_hacker("🔧 Check API server logs for details", 'yellow')
    
    print()
    print_separator('═')
    print_hacker("🔚 SIMULATION COMPLETE", 'magenta')
    print_separator('═')
    print()
    
    return 0 if failed_leads == 0 else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print()
        print_hacker("⚠️  Simulation interrupted by user", 'yellow')
        print_separator('═')
        sys.exit(130)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        print_separator('═')
        sys.exit(1)
