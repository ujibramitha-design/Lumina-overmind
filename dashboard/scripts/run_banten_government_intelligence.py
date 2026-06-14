#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Banten Government Intelligence Module
Simulates PNS & P3K data extraction from Banten Provincial Government systems
Designed for continuous background service operation
"""

import time
import random
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# ANSI Color Codes for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
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

def typewriter_effect(text, delay=0.02):
    """Create typewriter effect for text"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Get database connection with proper error handling"""
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = # SQLite connection removed
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print_error(f"Database connection error: {e}")
        raise

def ensure_leads_table(conn: sqlite3.Connection):
    """Ensure leads table exists with proper schema"""
    try:
        cursor = conn.cursor()
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                contact TEXT,
                url TEXT,
                keywords TEXT,
                source TEXT DEFAULT 'web_scraping',
                score REAL DEFAULT 0.0,
                status TEXT DEFAULT 'new',
                location TEXT,
                date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                catatan_followup TEXT
            )
        ''')
        # conn.commit() removed
        print_success("Leads table verified/created")
    except sqlite3.Error as e:
        print_error(f"Table creation error: {e}")
        raise

def simulate_banten_gov_scan() -> List[Dict[str, Any]]:
    """Simulate scanning Banten Government systems for PNS & P3K data"""
    print_hacker("🔍 Initiating Banten Government Intelligence Scan...", 'cyan')
    
    # Simulate network delay
    time.sleep(random.uniform(1.0, 3.0))
    
    print_hacker("🌐 Targeting Banten Gov Server...", 'blue')
    time.sleep(random.uniform(0.5, 1.5))
    
    print_hacker("🔓 Bypassing security protocols...", 'yellow')
    time.sleep(random.uniform(0.8, 2.0))
    
    print_hacker("📊 Accessing PNS & P3K database...", 'blue')
    time.sleep(random.uniform(1.0, 2.5))
    
    # Generate fake PNS data
    pns_profiles = []
    num_profiles = random.randint(8, 15)
    
    print_hacker(f"🎯 Found {num_profiles} high-intent PNS profiles...", 'cyan')
    
    for i in range(num_profiles):
        profile = {
            'nama': generate_pns_name(),
            'nip': generate_nip(),
            'golongan': random.choice(['III/a', 'III/b', 'III/c', 'III/d', 'IV/a', 'IV/b']),
            'unit_kerja': generate_unit_kerja(),
            'lokasi': random.choice(['Serang', 'Cilegon', 'Tangerang', 'Pandeglang', 'Lebak']),
            'pendapatan': random.randint(5000000, 15000000),
            'status_kepegawaian': random.choice(['PNS', 'P3K'])
        }
        pns_profiles.append(profile)
    
    print_success(f"Successfully extracted {len(pns_profiles)} PNS profiles")
    return pns_profiles

def generate_pns_name() -> str:
    """Generate realistic Indonesian PNS name"""
    first_names = ['Ahmad', 'Budi', 'Dewi', 'Rina', 'Siti', 'Hendra', 'Maya', 'Rudi', 'Sarah', 'Fajar']
    last_names = ['Santoso', 'Wijaya', 'Putri', 'Hidayat', 'Susanto', 'Kusuma', 'Pratiwi', 'Fauzi', 'Nurmalasari', 'Saputra']
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_nip() -> str:
    """Generate realistic NIP (Nomor Induk Pegawai)"""
    return f"19{random.randint(70, 99):02d}{random.randint(100000000, 999999999)}"

def generate_unit_kerja() -> str:
    """Generate realistic government unit names"""
    units = [
        'Dinas Pendidikan',
        'Dinas Kesehatan',
        'Dinas Pekerjaan Umum',
        'Dinas Perhubungan',
        'Bappeda',
        'Inspektorat',
        'Dinas Sosial',
        'Dinas Pertanian',
        'Dinas Perindustrian',
        'Satpol PP'
    ]
    return random.choice(units)

def analyze_pns_intent(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze PNS profile for property purchase intent"""
    intent_score = 0
    intent_factors = []
    
    # High income indicates purchasing power
    if profile['pendapatan'] > 10000000:
        intent_score += 30
        intent_factors.append('High income (>10M/month)')
    
    # Higher golongan indicates stability
    if profile['golongan'] in ['IV/a', 'IV/b']:
        intent_score += 25
        intent_factors.append('Senior golongan (IV)')
    
    # PNS status indicates permanent employment
    if profile['status_kepegawaian'] == 'PNS':
        intent_score += 20
        intent_factors.append('Permanent PNS status')
    
    # Certain units indicate higher likelihood
    high_intent_units = ['Dinas Pendidikan', 'Dinas Kesehatan', 'Bappeda']
    if profile['unit_kerja'] in high_intent_units:
        intent_score += 15
        intent_factors.append(f'High-value unit: {profile["unit_kerja"]}')
    
    # Location analysis
    prime_locations = ['Serang', 'Tangerang']
    if profile['lokasi'] in prime_locations:
        intent_score += 10
        intent_factors.append(f'Prime location: {profile["lokasi"]}')
    
    return {
        'intent_score': intent_score,
        'intent_level': 'High' if intent_score >= 70 else 'Medium' if intent_score >= 40 else 'Low',
        'intent_factors': intent_factors
    }

def save_to_leads_db(profiles: List[Dict[str, Any]]):
    """Save PNS profiles to leads database"""
    db_path = os.path.join('..', 'data', 'leads.db (SQLite - removed))
    conn = get_db_connection(db_path)
    
    try:
        ensure_leads_table(conn)
        cursor = conn.cursor()
        
        saved_count = 0
        
        for profile in profiles:
            # Analyze intent
            intent_analysis = analyze_pns_intent(profile)
            
            # Prepare lead data
            business_name = profile['nama']
            contact = f"NIP: {profile['nip']}, Golongan: {profile['golongan']}, Unit: {profile['unit_kerja']}, Status: {profile['status_kepegawaian']}, Pendapatan: Rp{profile['pendapatan']:,}"
            url = f"banten_gov_intel_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{profile['nip']}"
            keywords = f"pns,p3k,banten,gov,{profile['unit_kerja'].lower().replace(' ', '_')},{profile['lokasi'].lower()},{profile['status_kepegawaian'].lower()}"
            
            # Generate AI follow-up notes
            catatan_followup = {
                'message': f"High-value government employee detected. {profile['nama']} is a {profile['status_kepegawaian']} with {profile['golongan']} at {profile['unit_kerja']} in {profile['lokasi']}. Monthly income: Rp{profile['pendapatan']:,}. Intent analysis: {intent_analysis['intent_level']} ({intent_analysis['intent_score']} points). Key factors: {', '.join(intent_analysis['intent_factors'])}. Recommended approach: Focus on family housing, KPR facilities, and location convenience near government offices.",
                'metadata': {
                    'source': 'Banten_Gov_Intel',
                    'nip': profile['nip'],
                    'golongan': profile['golongan'],
                    'unit_kerja': profile['unit_kerja'],
                    'pendapatan': profile['pendapatan'],
                    'intent_score': intent_analysis['intent_score'],
                    'intent_level': intent_analysis['intent_level'],
                    'pekerjaan': 'PNS Pemprov Banten',
                    'scan_timestamp': datetime.now().isoformat()
                }
            }
            
            # Insert into database
            # cursor.execute() removed'''
                INSERT INTO leads (
                    business_name, contact, url, keywords, source, score, status, 
                    location, date_found, created_at, updated_at, catatan_followup
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                business_name,
                contact,
                url,
                keywords,
                'Banten_Gov_Intel',
                intent_analysis['intent_score'],
                'Follow Up',
                profile['lokasi'],
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                json.dumps(catatan_followup)
            ))
            
            saved_count += 1
            print_hacker(f"💾 Saved PNS profile: {profile['nama']} ({profile['unit_kerja']})", 'green')
        
        # conn.commit() removed
        print_success(f"Successfully saved {saved_count} PNS profiles to database")
        
    except sqlite3.Error as e:
        print_error(f"Database save error: {e}")
        conn.rollback()
        raise
    finally:
        # conn.close() removed

def generate_scan_report(profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comprehensive scan report"""
    total_profiles = len(profiles)
    pns_count = sum(1 for p in profiles if p['status_kepegawaian'] == 'PNS')
    p3k_count = total_profiles - pns_count
    
    # Calculate average income
    avg_income = sum(p['pendapatan'] for p in profiles) / total_profiles if total_profiles > 0 else 0
    
    # Location distribution
    location_dist = {}
    for profile in profiles:
        location = profile['lokasi']
        location_dist[location] = location_dist.get(location, 0) + 1
    
    # Unit distribution
    unit_dist = {}
    for profile in profiles:
        unit = profile['unit_kerja']
        unit_dist[unit] = unit_dist.get(unit, 0) + 1
    
    # Intent analysis
    high_intent = 0
    medium_intent = 0
    low_intent = 0
    
    for profile in profiles:
        intent = analyze_pns_intent(profile)
        if intent['intent_level'] == 'High':
            high_intent += 1
        elif intent['intent_level'] == 'Medium':
            medium_intent += 1
        else:
            low_intent += 1
    
    return {
        'scan_timestamp': datetime.now().isoformat(),
        'total_profiles': total_profiles,
        'pns_count': pns_count,
        'p3k_count': p3k_count,
        'average_income': avg_income,
        'location_distribution': location_dist,
        'unit_distribution': unit_dist,
        'intent_distribution': {
            'high': high_intent,
            'medium': medium_intent,
            'low': low_intent
        }
    }

def display_scan_report(report: Dict[str, Any]):
    """Display formatted scan report"""
    print_header("📊 BANTEN GOVERNMENT INTELLIGENCE REPORT")
    print_separator('─')
    
    print_hacker(f"📈 Total Profiles Scanned: {report['total_profiles']}", 'cyan')
    print_hacker(f"👥 PNS Employees: {report['pns_count']}", 'blue')
    print_hacker(f"🔄 P3K Employees: {report['p3k_count']}", 'yellow')
    print_hacker(f"💰 Average Monthly Income: Rp{report['average_income']:,.0f}", 'green')
    
    print()
    print_hacker("📍 Location Distribution:", 'magenta')
    for location, count in report['location_distribution'].items():
        print_hacker(f"   • {location}: {count} profiles", 'dim')
    
    print()
    print_hacker("🏢 Unit Distribution:", 'magenta')
    for unit, count in report['unit_distribution'].items():
        print_hacker(f"   • {unit}: {count} profiles", 'dim')
    
    print()
    print_hacker("🎯 Purchase Intent Analysis:", 'magenta')
    print_hacker(f"   • High Intent: {report['intent_distribution']['high']} profiles", 'green')
    print_hacker(f"   • Medium Intent: {report['intent_distribution']['medium']} profiles", 'yellow')
    print_hacker(f"   • Low Intent: {report['intent_distribution']['low']} profiles", 'red')
    
    print_separator('═')

def print_separator(char='═', length=80):
    print(f"{Colors.CYAN}{char * length}{Colors.END}")

def main():
    """Main function for continuous background service"""
    print_separator('═')
    print()
    typewriter_effect("🔐 HUNTER AGENT AI MARKETING DIGITAL - BANTEN GOVERNMENT INTELLIGENCE", 0.02)
    typewriter_effect("🏛️  PNS & P3K DATA EXTRACTION MODULE", 0.02)
    print_separator('═')
    print()
    
    print_hacker("🚀 Initializing Banten Government Intelligence Service...", 'cyan')
    print_hacker("🔄 Starting continuous monitoring mode...", 'blue')
    print()
    
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            print_header(f"🔍 SCAN CYCLE #{scan_count}")
            print_separator('─')
            
            # Simulate Banten Government scan
            profiles = simulate_banten_gov_scan()
            
            if profiles:
                # Save to database
                save_to_leads_db(profiles)
                
                # Generate and display report
                report = generate_scan_report(profiles)
                display_scan_report(report)
                
                print_hacker("✨ High-value leads identified and processed", 'green')
                print_hacker("🎯 Ready for next intelligence cycle", 'blue')
            else:
                print_warning("No profiles found in this scan cycle")
            
            print()
            print_hacker("⏳ Waiting 10 seconds before next scan...", 'yellow')
            print_separator('═')
            print()
            
            # Delay for next cycle
            time.sleep(10)
            
    except KeyboardInterrupt:
        print()
        print_hacker("⚠️  Intelligence service interrupted by user", 'yellow')
        print_hacker(f"📊 Total scans completed: {scan_count}", 'cyan')
        print_separator('═')
        print_hacker("🔚 BANTEN GOVERNMENT INTELLIGENCE SERVICE STOPPED", 'magenta')
        print_separator('═')
        print()
        sys.exit(130)
        
    except Exception as e:
        print()
        print_error(f"Critical error in intelligence service: {e}")
        print_hacker(f"📊 Scans completed before error: {scan_count}", 'cyan')
        print_separator('═')
        sys.exit(1)

if __name__ == "__main__":
    # Import json for catatan_followup
    import json
    
    main()
