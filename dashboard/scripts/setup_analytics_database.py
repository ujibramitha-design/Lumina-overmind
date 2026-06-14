#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Analytics Database Setup
Initializes analytics database with proper schema for background services
"""

import os
from datetime import datetime

# ANSI Color Codes
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
    timestamp = datetime.now().strftime('%H:%M:%S')
    prefix = f"{Colors.DIM}[{timestamp}]{Colors.END}"
    color_code = getattr(Colors, color.upper(), Colors.CYAN)
    print(f"{prefix} {color_code}►{Colors.END} {color_code}{message}{Colors.END}")

def print_success(message):
    print_hacker(f"✅ {message}", 'green')

def print_error(message):
    print_hacker(f"❌ {message}", 'red')

def print_header(message):
    print_hacker(f"🔧 {message}", 'magenta')

def setup_analytics_database():
    """Setup analytics database with required tables"""
    db_path = os.path.join('..', 'data', 'analytics.db (SQLite - removed))
    
    try:
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to database
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        print_hacker("🔗 Connecting to analytics database...", 'blue')
        
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
        
        print_success("market_data table created/verified")
        
        # Create price_analysis table
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
        
        print_success("price_analysis table created/verified")
        
        # Create indexes for performance
        # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_market_data_location ON market_data(location)')
        # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_market_data_property_type ON market_data(property_type)')
        # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_market_data_created_at ON market_data(created_at)')
        
        # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_price_analysis_location ON price_analysis(location)')
        # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_price_analysis_property_type ON price_analysis(property_type)')
        # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_price_analysis_created_at ON price_analysis(created_at)')
        
        print_success("Database indexes created")
        
        # Drop existing view and create new one
        # cursor.execute() removed'DROP VIEW IF EXISTS market_summary')
        
        # cursor.execute() removed'''
            CREATE VIEW market_summary AS
            SELECT 
                location,
                property_type,
                COUNT(*) as total_listings,
                AVG(price_avg) as avg_price,
                AVG(price_per_meter) as avg_price_per_meter,
                MAX(created_at) as last_scan
            FROM market_data
            GROUP BY location, property_type
        ''')
        
        print_success("market_summary view created")
        
        # conn.commit() removed
        # conn.close() removed
        
        print_success("Analytics database setup completed successfully!")
        return True
        
    except sqlite3.Error as e:
        print_error(f"Database setup error: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🔐 HUNTER AGENT AI MARKETING DIGITAL - Analytics Database Setup")
    print("=" * 60)
    print()
    
    print_hacker("🚀 Initializing analytics database setup...", 'cyan')
    print()
    
    if setup_analytics_database():
        print()
        print_success("🎉 Analytics database is ready for background services!")
        print_hacker("📊 Market intelligence services can now store data", 'green')
        print_hacker("🔄 Background services will automatically use this database", 'blue')
        print()
        print_hacker("📁 Database location: ../data/analytics.db (SQLite - removed), 'dim')
        print_hacker("📋 Tables created: market_data, price_analysis", 'dim')
        print_hacker("👀 Views created: market_summary", 'dim')
        print_hacker("🔍 Indexes created for performance optimization", 'dim')
    else:
        print()
        print_error("❌ Analytics database setup failed!")
        print_hacker("🔧 Please check database permissions and try again", 'yellow')
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
