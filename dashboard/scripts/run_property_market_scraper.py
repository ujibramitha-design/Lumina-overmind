#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Property Market Scraper Module
Simulates competitive property price analysis from major property portals
Designed for continuous background service operation
"""

import time
import random
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# ANSI Color Codes for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'
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

def ensure_analytics_table(conn: sqlite3.Connection):
    """Ensure analytics database and market_data table exist"""
    try:
        cursor = conn.cursor()
        
        # Create market_data table
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_type TEXT NOT NULL,
                location TEXT NOT NULL,
                price_min REAL,
                price_max REAL,
                price_avg REAL,
                competitor TEXT NOT NULL,
                listing_count INTEGER DEFAULT 1,
                price_per_meter REAL,
                area_range TEXT,
                facilities TEXT,
                scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create price_analysis table for trend tracking
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS price_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                property_type TEXT NOT NULL,
                avg_price REAL NOT NULL,
                price_trend TEXT,
                market_gap_percent REAL,
                competitor_count INTEGER,
                analysis_date DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # conn.commit() removed
        print_success("Analytics tables verified/created")
    except sqlite3.Error as e:
        print_error(f"Table creation error: {e}")
        raise

def simulate_property_scrape() -> List[Dict[str, Any]]:
    """Simulate scraping property data from major portals"""
    print_hacker("🔍 Initiating Property Market Intelligence Scan...", 'orange')
    
    # Simulate network delay
    time.sleep(random.uniform(1.0, 2.5))
    
    # Target locations in Banten area
    locations = ['Serang', 'Cilegon', 'Tangerang', 'Pandeglang', 'Lebak']
    target_location = random.choice(locations)
    
    print_hacker(f"🌐 Scanning competitor pricing in {target_location}...", 'yellow')
    time.sleep(random.uniform(0.8, 2.0))
    
    # Simulate accessing different portals
    portals = ['Rumah123', '99.co', 'Lamudi', 'UrbanIndo']
    target_portal = random.choice(portals)
    
    print_hacker(f"🔓 Accessing {target_portal} database...", 'blue')
    time.sleep(random.uniform(1.0, 2.5))
    
    print_hacker("📊 Extracting property listings...", 'orange')
    time.sleep(random.uniform(1.5, 3.0))
    
    # Generate fake property data
    property_listings = []
    num_listings = random.randint(15, 35)
    
    print_hacker(f"🎯 Found {num_listings} active listings in {target_location}", 'cyan')
    
    for i in range(num_listings):
        listing = generate_property_listing(target_location, target_portal)
        property_listings.append(listing)
    
    print_success(f"Successfully extracted {len(property_listings)} property listings")
    return property_listings

def generate_property_listing(location: str, portal: str) -> Dict[str, Any]:
    """Generate realistic property listing data"""
    property_types = ['Rumah', 'Apartemen', 'Ruko', 'Tanah', 'Villa']
    property_type = random.choice(property_types)
    
    # Generate price based on location and property type
    base_price = get_base_price(location, property_type)
    price_variation = random.uniform(0.8, 1.3)
    price = base_price * price_variation
    
    # Generate area
    if property_type in ['Rumah', 'Villa']:
        area = random.randint(60, 300)
    elif property_type == 'Apartemen':
        area = random.randint(25, 120)
    elif property_type == 'Ruko':
        area = random.randint(60, 200)
    else:  # Tanah
        area = random.randint(100, 1000)
    
    # Generate facilities
    facilities = generate_facilities(property_type)
    
    return {
        'property_type': property_type,
        'location': location,
        'price': price,
        'area': area,
        'price_per_meter': price / area if area > 0 else 0,
        'portal': portal,
        'title': generate_property_title(property_type, location),
        'description': generate_property_description(property_type, location, area),
        'facilities': facilities,
        'listing_date': datetime.now() - timedelta(days=random.randint(1, 90))
    }

def get_base_price(location: str, property_type: str) -> float:
    """Get base price based on location and property type"""
    base_prices = {
        'Serang': {
            'Rumah': 500000000,
            'Apartemen': 350000000,
            'Ruko': 800000000,
            'Tanah': 2000000,
            'Villa': 1200000000
        },
        'Cilegon': {
            'Rumah': 450000000,
            'Apartemen': 300000000,
            'Ruko': 700000000,
            'Tanah': 1800000,
            'Villa': 1000000000
        },
        'Tangerang': {
            'Rumah': 800000000,
            'Apartemen': 600000000,
            'Ruko': 1200000000,
            'Tanah': 3500000,
            'Villa': 2000000000
        },
        'Pandeglang': {
            'Rumah': 350000000,
            'Apartemen': 250000000,
            'Ruko': 500000000,
            'Tanah': 1200000,
            'Villa': 800000000
        },
        'Lebak': {
            'Rumah': 300000000,
            'Apartemen': 200000000,
            'Ruko': 400000000,
            'Tanah': 1000000,
            'Villa': 600000000
        }
    }
    
    return base_prices.get(location, {}).get(property_type, 400000000)

def generate_property_title(property_type: str, location: str) -> str:
    """Generate realistic property title"""
    adjectives = ['Modern', 'Minimalis', 'Mewah', 'Strategis', 'Nyaman', 'Asri', 'Eksklusif']
    features = ['Full Furnished', 'Semi Furnished', 'Siap Huni', 'Baru', 'Renovasi']
    
    adj = random.choice(adjectives)
    feature = random.choice(features)
    
    return f"{adj} {property_type} {feature} di {location}"

def generate_property_description(property_type: str, location: str, area: int) -> str:
    """Generate realistic property description"""
    descriptions = {
        'Rumah': f"Dijual {property_type} dengan luas {area}m² di lokasi strategis {location}. Dekat dengan fasilitas umum, akses mudah, lingkungan aman dan nyaman.",
        'Apartemen': f"Unit {property_type} modern {area}m² di {location}. Fasilitas lengkap, security 24 jam, dekat dengan pusat bisnis dan transportasi publik.",
        'Ruko': f"{property_type} komersial {area}m² di {location}. Cocok untuk usaha, lokasi strategis, traffic tinggi, parking luas.",
        'Tanah': f"Tanah kosong {area}m² di {location}. Sertifikat Hak Milik, lokasi bagus untuk investasi, siap bangun.",
        'Villa': f"Villa mewah {area}m² di {location}. Pemandangan indah, privasi terjamin, cocok untuk liburan keluarga."
    }
    
    return descriptions.get(property_type, f"Properti {property_type} {area}m² di {location}")

def generate_facilities(property_type: str) -> List[str]:
    """Generate realistic facility list"""
    all_facilities = [
        'AC', 'Water Heater', 'Carport', 'Garden', 'Kitchen Set',
        'Swimming Pool', 'Security 24 Jam', 'Playground', 'Gym', 'Sauna',
        'Basketball Court', 'Tennis Court', 'Jogging Track', 'BBQ Area',
        'CCTV', 'Electricity', 'PDAM', 'Telephone Line', 'Internet'
    ]
    
    if property_type == 'Rumah':
        return random.sample(all_facilities[:10], random.randint(3, 6))
    elif property_type == 'Apartemen':
        return random.sample(all_facilities[5:15], random.randint(4, 7))
    elif property_type == 'Ruko':
        return random.sample(['Carport', 'Security 24 Jam', 'CCTV', 'Electricity', 'Telephone Line', 'Internet'], random.randint(2, 4))
    elif property_type == 'Villa':
        return random.sample(all_facilities[:8], random.randint(5, 8))
    else:  # Tanah
        return ['Electricity', 'PDAM']

def analyze_market_data(listings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze scraped market data and identify opportunities"""
    if not listings:
        return {}
    
    # Group by location and property type
    market_segments = {}
    for listing in listings:
        key = f"{listing['location']}_{listing['property_type']}"
        if key not in market_segments:
            market_segments[key] = []
        market_segments[key].append(listing)
    
    analysis_results = []
    
    for segment_key, segment_listings in market_segments.items():
        location, property_type = segment_key.split('_', 1)
        
        prices = [l['price'] for l in segment_listings]
        areas = [l['area'] for l in segment_listings]
        prices_per_meter = [l['price_per_meter'] for l in segment_listings]
        
        # Calculate statistics
        price_min = min(prices)
        price_max = max(prices)
        price_avg = sum(prices) / len(prices)
        area_avg = sum(areas) / len(areas)
        price_per_meter_avg = sum(prices_per_meter) / len(prices_per_meter)
        
        # Calculate market gap (compared to our target price)
        our_target_price = get_base_price(location, property_type)
        market_gap_percent = ((our_target_price - price_avg) / price_avg) * 100
        
        # Determine trend
        trend = 'Stable'
        if market_gap_percent > 10:
            trend = 'Undervalued'
        elif market_gap_percent < -10:
            trend = 'Overvalued'
        
        # Get competitor info
        competitors = list(set(l['portal'] for l in segment_listings))
        
        # Get common facilities
        all_facilities = []
        for listing in segment_listings:
            all_facilities.extend(listing['facilities'])
        
        facility_counts = {}
        for facility in all_facilities:
            facility_counts[facility] = facility_counts.get(facility, 0) + 1
        
        common_facilities = [f for f, count in facility_counts.items() if count >= len(segment_listings) * 0.3]
        
        # Check for price gap alert
        price_gap_alert = None
        if abs(market_gap_percent) > 15:
            if market_gap_percent > 0:
                price_gap_alert = f"Price gap detected: {abs(market_gap_percent):.1f}% below market average"
            else:
                price_gap_alert = f"Price gap detected: {abs(market_gap_percent):.1f}% above market average"
        
        analysis_result = {
            'location': location,
            'property_type': property_type,
            'price_min': price_min,
            'price_max': price_max,
            'price_avg': price_avg,
            'price_per_meter_avg': price_per_meter_avg,
            'area_avg': area_avg,
            'listing_count': len(segment_listings),
            'competitors': competitors,
            'competitor_count': len(competitors),
            'common_facilities': common_facilities,
            'market_gap_percent': market_gap_percent,
            'price_trend': trend,
            'price_gap_alert': price_gap_alert,
            'scan_timestamp': datetime.now().isoformat()
        }
        
        analysis_results.append(analysis_result)
        
        # Print alerts
        if price_gap_alert:
            print_hacker(f"⚠️  {price_gap_alert} for {property_type} in {location}", 'yellow')
    
    return {
        'total_listings': len(listings),
        'segments_analyzed': len(analysis_results),
        'analysis_results': analysis_results
    }

def save_to_analytics_db(analysis_data: Dict[str, Any]):
    """Save market analysis data to analytics database"""
    db_path = os.path.join('..', 'data', 'analytics.db (SQLite - removed))
    conn = get_db_connection(db_path)
    
    try:
        ensure_analytics_table(conn)
        cursor = conn.cursor()
        
        saved_count = 0
        
        for result in analysis_data['analysis_results']:
            # Insert into market_data table
            # cursor.execute() removed'''
                INSERT INTO market_data (
                    property_type, location, price_min, price_max, price_avg,
                    competitor, listing_count, price_per_meter, area_range,
                    facilities, scan_timestamp, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['property_type'],
                result['location'],
                result['price_min'],
                result['price_max'],
                result['price_avg'],
                ','.join(result['competitors']),
                result['listing_count'],
                result['price_per_meter_avg'],
                f"{int(result['area_avg'] * 0.8)}-{int(result['area_avg'] * 1.2)}m²",
                ','.join(result['common_facilities']),
                result['scan_timestamp'],
                datetime.now().isoformat()
            ))
            
            # Insert into price_analysis table
            # cursor.execute() removed'''
                INSERT INTO price_analysis (
                    location, property_type, avg_price, price_trend,
                    market_gap_percent, competitor_count, analysis_date, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['location'],
                result['property_type'],
                result['price_avg'],
                result['price_trend'],
                result['market_gap_percent'],
                result['competitor_count'],
                datetime.now().date(),
                datetime.now().isoformat()
            ))
            
            saved_count += 1
            print_hacker(f"💾 Saved market data: {result['property_type']} in {result['location']}", 'green')
        
        # conn.commit() removed
        print_success(f"Successfully saved {saved_count} market segments to database")
        
    except sqlite3.Error as e:
        print_error(f"Database save error: {e}")
        conn.rollback()
        raise
    finally:
        # conn.close() removed

def display_market_report(analysis_data: Dict[str, Any]):
    """Display formatted market analysis report"""
    print_header("📊 PROPERTY MARKET INTELLIGENCE REPORT")
    print_separator('─')
    
    print_hacker(f"📈 Total Listings Analyzed: {analysis_data['total_listings']}", 'orange')
    print_hacker(f"🎯 Market Segments: {analysis_data['segments_analyzed']}", 'cyan')
    
    print()
    print_hacker("📍 MARKET SEGMENT ANALYSIS:", 'magenta')
    print_separator('─')
    
    for result in analysis_data['analysis_results']:
        print_hacker(f"🏠 {result['property_type']} - {result['location']}", 'yellow')
        print_hacker(f"   💰 Price Range: Rp{result['price_min']:,.0f} - Rp{result['price_max']:,.0f}", 'dim')
        print_hacker(f"   📊 Average Price: Rp{result['price_avg']:,.0f}", 'dim')
        print_hacker(f"   📏 Avg Price/m²: Rp{result['price_per_meter_avg']:,.0f}", 'dim')
        print_hacker(f"   📈 Trend: {result['price_trend']}", 'dim')
        print_hacker(f"   🏪 Competitors: {', '.join(result['competitors'])} ({result['competitor_count']})", 'dim')
        print_hacker(f"   📋 Listings: {result['listing_count']}", 'dim')
        
        if result['price_gap_alert']:
            print_hacker(f"   ⚠️  {result['price_gap_alert']}", 'yellow')
        
        print()
    
    print_separator('═')

def print_separator(char='═', length=80):
    print(f"{Colors.ORANGE}{char * length}{Colors.END}")

def main():
    """Main function for continuous background service"""
    print_separator('═')
    print()
    typewriter_effect("🔐 HUNTER AGENT AI MARKETING DIGITAL - PROPERTY MARKET SCRAPER", 0.02)
    typewriter_effect("🏠 COMPETITIVE PRICE INTELLIGENCE MODULE", 0.02)
    print_separator('═')
    print()
    
    print_hacker("🚀 Initializing Property Market Intelligence Service...", 'orange')
    print_hacker("🔄 Starting continuous market monitoring mode...", 'blue')
    print()
    
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            print_header(f"🔍 MARKET SCAN CYCLE #{scan_count}")
            print_separator('─')
            
            # Simulate property scraping
            listings = simulate_property_scrape()
            
            if listings:
                # Analyze market data
                analysis_data = analyze_market_data(listings)
                
                # Save to database
                save_to_analytics_db(analysis_data)
                
                # Display report
                display_market_report(analysis_data)
                
                print_hacker("✨ Market intelligence processed and stored", 'green')
                print_hacker("🎯 Ready for next market analysis cycle", 'blue')
            else:
                print_warning("No property listings found in this scan cycle")
            
            print()
            print_hacker("⏳ Waiting 10 seconds before next scan...", 'yellow')
            print_separator('═')
            print()
            
            # Delay for next cycle
            time.sleep(10)
            
    except KeyboardInterrupt:
        print()
        print_hacker("⚠️  Market intelligence service interrupted by user", 'yellow')
        print_hacker(f"📊 Total scans completed: {scan_count}", 'orange')
        print_separator('═')
        print_hacker("🔚 PROPERTY MARKET INTELLIGENCE SERVICE STOPPED", 'magenta')
        print_separator('═')
        print()
        sys.exit(130)
        
    except Exception as e:
        print()
        print_error(f"Critical error in market intelligence service: {e}")
        print_hacker(f"📊 Scans completed before error: {scan_count}", 'orange')
        print_separator('═')
        sys.exit(1)

if __name__ == "__main__":
    main()
