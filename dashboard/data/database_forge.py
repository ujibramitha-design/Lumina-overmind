#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Database Forge
Creates and initializes core databases with sample data
"""

import os
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

# ANSI Color Codes for Terminal Output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message: str):
    """Print success message in green"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message: str):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_header(message: str):
    """Print header message in bold cyan"""
    print(f"{Colors.BOLD}{Colors.CYAN}🔧 {message}{Colors.END}")

class DatabaseForge:
    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.databases = {
            'leads': 'leads.db (SQLite - removed),
            'analytics': 'analytics.db (SQLite - removed), 
            'competitors': 'competitors.db (SQLite - removed),
            'campaigns': 'campaigns.db (SQLite - removed),
            'users': 'users.db (SQLite - removed),
            'notifications': 'notifications.db (SQLite - removed),
            'settings': 'settings.db (SQLite - removed),
            'logs': 'logs.db (SQLite - removed)
        }
        
    def create_database_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print_success("Created data directory")
    
    def create_leads_database(self):
        """Create leads database with comprehensive schema"""
        db_path = os.path.join(self.data_dir, self.databases['leads'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # Create leads table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_name TEXT NOT NULL,
                    contact TEXT,
                    phone TEXT,
                    email TEXT,
                    url TEXT,
                    keywords TEXT,
                    source TEXT DEFAULT 'web_scraping',
                    score REAL DEFAULT 0.0,
                    location TEXT,
                    city TEXT,
                    status TEXT DEFAULT 'new',
                    priority TEXT DEFAULT 'medium',
                    date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_contacted DATETIME,
                    notes TEXT,
                    property_type TEXT,
                    price_range TEXT,
                    bedrooms INTEGER,
                    bathrooms INTEGER,
                    land_size REAL,
                    building_size REAL,
                    year_built INTEGER,
                    description TEXT,
                    images TEXT, -- JSON array of image URLs
                    documents TEXT, -- JSON array of document URLs
                    metadata TEXT, -- JSON for additional data
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for performance
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_leads_location ON leads(location)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_leads_date_found ON leads(date_found)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_leads_source ON leads(source)')
            
            # conn.commit() removed
            print_success("Created leads database with comprehensive schema")
    
    def create_analytics_database(self):
        """Create analytics database with system stats and logs"""
        db_path = os.path.join(self.data_dir, self.databases['analytics'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # System stats table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS system_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # Scoring log table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS scoring_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER,
                    previous_score REAL,
                    new_score REAL,
                    scoring_method TEXT,
                    reason TEXT,
                    scored_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # Market data table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    property_type TEXT,
                    avg_price REAL,
                    price_trend TEXT, -- up, down, stable
                    market_sentiment TEXT, -- hot, warm, cold
                    inventory_count INTEGER,
                    days_on_market INTEGER,
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # User activity table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS user_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    resource_type TEXT,
                    resource_id INTEGER,
                    details TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Performance metrics table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    execution_time_ms REAL,
                    success BOOLEAN DEFAULT 1,
                    error_message TEXT,
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # conn.commit() removed
            print_success("Created analytics database with comprehensive tracking")
    
    def create_competitors_database(self):
        """Create competitors database for market intelligence"""
        db_path = os.path.join(self.data_dir, self.databases['competitors'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # Competitors table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS competitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    website TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    city TEXT,
                    province TEXT,
                    company_type TEXT, -- developer, agent, individual
                    specialization TEXT, -- residential, commercial, industrial
                    established_year INTEGER,
                    reputation_score REAL DEFAULT 0.0,
                    market_share REAL DEFAULT 0.0,
                    avg_price_point REAL,
                    total_listings INTEGER DEFAULT 0,
                    active_listings INTEGER DEFAULT 0,
                    sold_properties INTEGER DEFAULT 0,
                    last_scraped DATETIME,
                    notes TEXT,
                    metadata TEXT, -- JSON for additional data
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Competitor listings table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS competitor_listings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    competitor_id INTEGER,
                    property_title TEXT NOT NULL,
                    property_type TEXT,
                    location TEXT,
                    price REAL,
                    bedrooms INTEGER,
                    bathrooms INTEGER,
                    land_size REAL,
                    building_size REAL,
                    description TEXT,
                    listing_url TEXT,
                    status TEXT DEFAULT 'active', -- active, sold, withdrawn
                    listed_date DATETIME,
                    sold_date DATETIME,
                    days_on_market INTEGER,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (competitor_id) REFERENCES competitors (id)
                )
            ''')
            
            # Price history table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    competitor_id INTEGER,
                    listing_id INTEGER,
                    price REAL NOT NULL,
                    price_change REAL,
                    change_type TEXT, -- increase, decrease, same
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (competitor_id) REFERENCES competitors (id)
                )
            ''')
            
            # conn.commit() removed
            print_success("Created competitors database with market intelligence")
    
    def create_campaigns_database(self):
        """Create campaigns database for marketing management"""
        db_path = os.path.join(self.data_dir, self.databases['campaigns'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # Campaigns table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    campaign_type TEXT, -- email, social, ads, direct
                    status TEXT DEFAULT 'draft', -- draft, active, paused, completed
                    target_audience TEXT,
                    budget REAL,
                    spent REAL DEFAULT 0.0,
                    start_date DATETIME,
                    end_date DATETIME,
                    objectives TEXT,
                    metrics TEXT, -- JSON for campaign metrics
                    creative_assets TEXT, -- JSON for asset URLs
                    created_by TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Campaign performance table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS campaign_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER,
                    date DATE NOT NULL,
                    impressions INTEGER DEFAULT 0,
                    clicks INTEGER DEFAULT 0,
                    conversions INTEGER DEFAULT 0,
                    cost REAL DEFAULT 0.0,
                    revenue REAL DEFAULT 0.0,
                    ctr REAL, -- click-through rate
                    cpc REAL, -- cost per click
                    cpa REAL, -- cost per acquisition
                    roi REAL, -- return on investment
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
                )
            ''')
            
            # conn.commit() removed
            print_success("Created campaigns database for marketing management")
    
    def create_users_database(self):
        """Create users database for user management"""
        db_path = os.path.join(self.data_dir, self.databases['users'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # Users table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    phone TEXT,
                    role TEXT DEFAULT 'user', -- admin, manager, user
                    department TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    last_login DATETIME,
                    login_count INTEGER DEFAULT 0,
                    preferences TEXT, -- JSON for user preferences
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User sessions table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    expires_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # conn.commit() removed
            print_success("Created users database for user management")
    
    def create_notifications_database(self):
        """Create notifications database"""
        db_path = os.path.join(self.data_dir, self.databases['notifications'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # Notifications table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    type TEXT DEFAULT 'info', -- info, success, warning, error
                    priority TEXT DEFAULT 'medium', -- low, medium, high, urgent
                    is_read BOOLEAN DEFAULT 0,
                    action_url TEXT,
                    action_text TEXT,
                    metadata TEXT, -- JSON for additional data
                    expires_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    read_at DATETIME
                )
            ''')
            
            # conn.commit() removed
            print_success("Created notifications database")
    
    def create_settings_database(self):
        """Create settings database for configuration"""
        db_path = os.path.join(self.data_dir, self.databases['settings'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # Settings table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    description TEXT,
                    data_type TEXT DEFAULT 'string', -- string, integer, boolean, json
                    is_system BOOLEAN DEFAULT 0,
                    updated_by TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # conn.commit() removed
            print_success("Created settings database")
    
    def create_logs_database(self):
        """Create logs database for system logging"""
        db_path = os.path.join(self.data_dir, self.databases['logs'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # System logs table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL, -- DEBUG, INFO, WARNING, ERROR, CRITICAL
                    logger_name TEXT,
                    message TEXT NOT NULL,
                    module TEXT,
                    function_name TEXT,
                    line_number INTEGER,
                    exception_text TEXT,
                    stack_trace TEXT,
                    user_id TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    request_id TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Audit logs table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    resource_type TEXT,
                    resource_id INTEGER,
                    old_values TEXT, -- JSON
                    new_values TEXT, -- JSON
                    ip_address TEXT,
                    user_agent TEXT,
                    session_id TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # conn.commit() removed
            print_success("Created logs database for system logging")
    
    def seed_initial_data(self):
        """Seed databases with high-quality sample data"""
        print_header("Seeding Initial Data...")
        
        # Seed leads database
        self._seed_leads_data()
        
        # Seed analytics database
        self._seed_analytics_data()
        
        # Seed competitors database
        self._seed_competitors_data()
        
        # Seed campaigns database
        self._seed_campaigns_data()
        
        # Seed settings database
        self._seed_settings_data()
        
        print_success("Initial data seeding completed")
    
    def _seed_leads_data(self):
        """Seed leads database with high-quality prospects"""
        db_path = os.path.join(self.data_dir, self.databases['leads'])
        
        sample_leads = [
            {
                'business_name': 'PT. Maju Bersama Properti',
                'contact': 'Budi Santoso',
                'phone': '+62812345678',
                'email': 'budi@majubersama.co.id',
                'url': 'https://majubersama-properti.com',
                'keywords': 'investasi properti, rumah mewah, apartemen premium',
                'source': 'website_inquiry',
                'score': 9.2,
                'location': 'Jakarta Selatan',
                'city': 'Jakarta',
                'status': 'hot_lead',
                'priority': 'high',
                'property_type': 'apartment',
                'price_range': '2M-5M',
                'bedrooms': 3,
                'bathrooms': 2,
                'description': 'Looking for premium investment properties in South Jakarta area'
            },
            {
                'business_name': 'Citra Home Development',
                'contact': 'Siti Nurhaliza',
                'phone': '+62823456789',
                'email': 'siti@citrahome.com',
                'url': 'https://citrahome-development.com',
                'keywords': 'rumah keluarga, cluster, developer terpercaya',
                'source': 'property_portal',
                'score': 8.5,
                'location': 'Tangerang',
                'city': 'Tangerang',
                'status': 'qualified',
                'priority': 'high',
                'property_type': 'house',
                'price_range': '800M-1.5M',
                'bedrooms': 4,
                'bathrooms': 3,
                'land_size': 120,
                'building_size': 150,
                'description': 'Family looking for house in Tangerang with good school access'
            },
            {
                'business_name': 'Investasi Cerdas Indonesia',
                'contact': 'Ahmad Fauzi',
                'phone': '+62834567890',
                'email': 'ahmad@investasicerdas.id',
                'url': 'https://investasicerdas-indonesia.com',
                'keywords': 'properti komersial, ruko, gudang, investasi',
                'source': 'referral',
                'score': 8.8,
                'location': 'Bekasi',
                'city': 'Bekasi',
                'status': 'hot_lead',
                'priority': 'high',
                'property_type': 'commercial',
                'price_range': '1.5M-3M',
                'bedrooms': 0,
                'bathrooms': 0,
                'description': 'Commercial property investment for business expansion'
            },
            {
                'business_name': 'Rumah Idaman Keluarga',
                'contact': 'Dewi Lestari',
                'phone': '+62845678901',
                'email': 'dewi@rumahidaman.com',
                'url': 'https://rumahidaman-keluarga.com',
                'keywords': 'rumah subsidi, KPR, first home buyer',
                'source': 'social_media',
                'score': 7.8,
                'location': 'Depok',
                'city': 'Depok',
                'status': 'new',
                'priority': 'medium',
                'property_type': 'house',
                'price_range': '400M-800M',
                'bedrooms': 2,
                'bathrooms': 1,
                'description': 'First time home buyer looking for affordable housing'
            },
            {
                'business_name': 'Golden Land Corporation',
                'contact': 'Rizki Pratama',
                'phone': '+62856789012',
                'email': 'rizki@goldenland.co.id',
                'url': 'https://goldenland-corporation.com',
                'keywords': 'tanah kavling, investasi tanah, development',
                'source': 'cold_call',
                'score': 8.2,
                'location': 'Bogor',
                'city': 'Bogor',
                'status': 'qualified',
                'priority': 'medium',
                'property_type': 'land',
                'price_range': '500M-1M',
                'bedrooms': 0,
                'bathrooms': 0,
                'land_size': 500,
                'description': 'Land investment for future development project'
            },
            {
                'business_name': 'Mega Property Group',
                'contact': 'Indah Permata',
                'phone': '+62867890123',
                'email': 'indah@megaproperty.id',
                'url': 'https://megaproperty-group.com',
                'keywords': 'apartment mewah, fasilitas lengkap, lokasi strategis',
                'source': 'property_expo',
                'score': 9.0,
                'location': 'Jakarta Pusat',
                'city': 'Jakarta',
                'status': 'hot_lead',
                'priority': 'high',
                'property_type': 'apartment',
                'price_range': '3M-7M',
                'bedrooms': 2,
                'bathrooms': 2,
                'description': 'Luxury apartment in central Jakarta with full facilities'
            },
            {
                'business_name': 'Harapan Baru Realty',
                'contact': 'Faisal Rahman',
                'phone': '+62878901234',
                'email': 'faisal@harapanbaru.com',
                'url': 'https://harapanbaru-realty.com',
                'keywords': 'rumah second hand, renovasi, good condition',
                'source': 'online_marketplace',
                'score': 7.5,
                'location': 'Cibubur',
                'city': 'Bogor',
                'status': 'new',
                'priority': 'medium',
                'property_type': 'house',
                'price_range': '600M-900M',
                'bedrooms': 3,
                'bathrooms': 2,
                'building_size': 120,
                'year_built': 2015,
                'description': 'Looking for well-maintained second home in Cibubur area'
            },
            {
                'business_name': 'Tropical Paradise Homes',
                'contact': 'Maya Sari',
                'phone': '+62889012345',
                'email': 'maya@tropicalparadise.com',
                'url': 'https://tropicalparadise-homes.com',
                'keywords': 'villa, resort, investasi liburan',
                'source': 'referral',
                'score': 8.6,
                'location': 'Bali',
                'city': 'Denpasar',
                'status': 'qualified',
                'priority': 'high',
                'property_type': 'villa',
                'price_range': '2M-4M',
                'bedrooms': 4,
                'bathrooms': 3,
                'land_size': 300,
                'building_size': 200,
                'description': 'Vacation villa investment in Bali tourist area'
            },
            {
                'business_name': 'Smart Living Solutions',
                'contact': 'Thomas Wijaya',
                'phone': '+62890123456',
                'email': 'thomas@smartliving.id',
                'url': 'https://smartliving-solutions.com',
                'keywords': 'smart home, teknologi, modern living',
                'source': 'website_inquiry',
                'score': 8.3,
                'location': 'Bandung',
                'city': 'Bandung',
                'status': 'qualified',
                'priority': 'medium',
                'property_type': 'apartment',
                'price_range': '1.2M-2.5M',
                'bedrooms': 2,
                'bathrooms': 2,
                'description': 'Tech-savvy professional looking for smart home apartment'
            },
            {
                'business_name': 'Cozy Living Spaces',
                'contact': 'Sarah Johnson',
                'phone': '+62891234567',
                'email': 'sarah@cozyliving.com',
                'url': 'https://cozyliving-spaces.com',
                'keywords': 'studio apartment, minimalist, young professional',
                'source': 'social_media',
                'score': 7.9,
                'location': 'Surabaya',
                'city': 'Surabaya',
                'status': 'new',
                'priority': 'medium',
                'property_type': 'apartment',
                'price_range': '300M-600M',
                'bedrooms': 1,
                'bathrooms': 1,
                'building_size': 35,
                'description': 'Young professional seeking minimalist studio apartment'
            }
        ]
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            for lead in sample_leads:
                # cursor.execute() removed'''
                    INSERT OR REPLACE INTO leads (
                        business_name, contact, phone, email, url, keywords, source, 
                        score, location, city, status, priority, property_type, 
                        price_range, bedrooms, bathrooms, land_size, building_size, 
                        year_built, description, date_found
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    lead['business_name'], lead['contact'], lead['phone'], lead['email'],
                    lead['url'], lead['keywords'], lead['source'], lead['score'],
                    lead['location'], lead['city'], lead['status'], lead['priority'],
                    lead['property_type'], lead['price_range'], lead['bedrooms'],
                    lead['bathrooms'], lead.get('land_size'), lead.get('building_size'),
                    lead.get('year_built'), lead['description'],
                    datetime.now() - timedelta(days=random.randint(1, 30))
                ))
            
            # conn.commit() removed
            print_success(f"Seeded {len(sample_leads)} high-quality leads")
    
    def _seed_analytics_data(self):
        """Seed analytics database with sample data"""
        db_path = os.path.join(self.data_dir, self.databases['analytics'])
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            # System stats
            system_stats = [
                ('total_leads', 156, 'count'),
                ('active_campaigns', 8, 'count'),
                ('conversion_rate', 12.5, 'percentage'),
                ('avg_response_time', 2.4, 'hours'),
                ('monthly_revenue', 45000000, 'IDR'),
                ('user_satisfaction', 4.6, 'score')
            ]
            
            for metric_name, metric_value, metric_unit in system_stats:
                # cursor.execute() removed'''
                    INSERT INTO system_stats (metric_name, metric_value, metric_unit)
                    VALUES (?, ?, ?)
                ''', (metric_name, metric_value, metric_unit))
            
            # Market data
            market_data = [
                ('Jakarta Selatan', 'apartment', 3500000000, 'up', 'hot', 245, 45),
                ('Tangerang', 'house', 1200000000, 'stable', 'warm', 189, 67),
                ('Bekasi', 'house', 950000000, 'down', 'cold', 156, 89),
                ('Depok', 'apartment', 850000000, 'up', 'warm', 134, 34),
                ('Bogor', 'land', 750000000, 'stable', 'cold', 98, 123)
            ]
            
            for location, prop_type, avg_price, trend, sentiment, inventory, days_on_market in market_data:
                # cursor.execute() removed'''
                    INSERT INTO market_data (
                        location, property_type, avg_price, price_trend, 
                        market_sentiment, inventory_count, days_on_market
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (location, prop_type, avg_price, trend, sentiment, inventory, days_on_market))
            
            # conn.commit() removed
            print_success("Seeded analytics data")
    
    def _seed_competitors_data(self):
        """Seed competitors database with sample data"""
        db_path = os.path.join(self.data_dir, self.databases['competitors'])
        
        competitors = [
            ('Properti Maju Bersama', 'https://propertimaju.com', '+6221500001', 'info@propertimaju.com',
             'Jakarta Selatan', 'Jakarta', 'developer', 'residential', 2010, 4.2, 8.5, 2800000000, 45, 38, 156, 0),
            ('Citra Home Developer', 'https://citrahome.id', '+6221500002', 'contact@citrahome.id',
             'Tangerang', 'Banten', 'developer', 'residential', 2008, 4.0, 6.8, 1500000000, 32, 28, 98, 0),
            ('Golden Land Corp', 'https://goldenland.co.id', '+6221500003', 'sales@goldenland.co.id',
             'Jakarta Pusat', 'Jakarta', 'agent', 'commercial', 2012, 3.8, 4.2, 4500000000, 18, 15, 67, 0)
        ]
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            for competitor in competitors:
                # cursor.execute() removed'''
                    INSERT INTO competitors (
                        name, website, phone, email, address, city, province, 
                        company_type, specialization, established_year, reputation_score,
                        market_share, avg_price_point, total_listings, active_listings,
                        sold_properties
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', competitor)
            
            # conn.commit() removed
            print_success("Seeded competitors data")
    
    def _seed_campaigns_data(self):
        """Seed campaigns database with sample data"""
        db_path = os.path.join(self.data_dir, self.databases['campaigns'])
        
        campaigns = [
            ('Summer Property Expo 2024', 'Digital campaign for summer property exhibition', 'social', 'active',
             'first_home_buyers, investors', 50000000, 25000000, '2024-06-01', '2024-06-30',
             'Generate 100+ qualified leads', '{}', '{}', 'admin'),
            ('Luxury Living Campaign', 'Premium property marketing campaign', 'ads', 'active',
             'high_net_worth_individuals', 75000000, 45000000, '2024-05-15', '2024-07-15',
             'Sell 10 luxury properties', '{}', '{}', 'marketing_manager')
        ]
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            for campaign in campaigns:
                # cursor.execute() removed'''
                    INSERT INTO campaigns (
                        name, description, campaign_type, status, target_audience, 
                        budget, spent, start_date, end_date, objectives, 
                        metrics, creative_assets, created_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', campaign)
            
            # conn.commit() removed
            print_success("Seeded campaigns data")
    
    def _seed_settings_data(self):
        """Seed settings database with default configuration"""
        db_path = os.path.join(self.data_dir, self.databases['settings'])
        
        settings = [
            ('app_name', 'HUNTER AGENT AI MARKETING DIGITAL', 'Application name', 'string', 1, 'system'),
            ('app_version', '1.0.0', 'Application version', 'string', 1, 'system'),
            ('default_currency', 'IDR', 'Default currency for pricing', 'string', 1, 'system'),
            ('timezone', 'Asia/Jakarta', 'Default timezone', 'string', 1, 'system'),
            ('max_upload_size', '10485760', 'Maximum file upload size in bytes', 'integer', 1, 'system'),
            ('enable_notifications', 'true', 'Enable push notifications', 'boolean', 0, 'user'),
            ('auto_backup_enabled', 'true', 'Enable automatic database backup', 'boolean', 1, 'system'),
            ('session_timeout', '3600', 'Session timeout in seconds', 'integer', 1, 'system')
        ]
        
        with # SQLite connection removed as conn:
            cursor = conn.cursor()
            
            for key, value, description, data_type, is_system, updated_by in settings:
                # cursor.execute() removed'''
                    INSERT OR REPLACE INTO settings (
                        key, value, description, data_type, is_system, updated_by
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (key, value, description, data_type, is_system, updated_by))
            
            # conn.commit() removed
            print_success("Seeded default settings")
    
    def forge_all_databases(self):
        """Create all databases and seed initial data"""
        print_header("🔧 HUNTER AGENT AI MARKETING DIGITAL - Database Forge")
        print(f"{Colors.CYAN}Creating databases in: {self.data_dir}{Colors.END}")
        print("=" * 60)
        
        try:
            # Create directory
            self.create_database_directory()
            
            # Create all databases
            self.create_leads_database()
            self.create_analytics_database()
            self.create_competitors_database()
            self.create_campaigns_database()
            self.create_users_database()
            self.create_notifications_database()
            self.create_settings_database()
            self.create_logs_database()
            
            print()
            print_header("🎯 Database Creation Summary")
            print(f"{Colors.GREEN}✅ Leads Database: {self.databases['leads']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Analytics Database: {self.databases['analytics']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Competitors Database: {self.databases['competitors']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Campaigns Database: {self.databases['campaigns']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Users Database: {self.databases['users']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Notifications Database: {self.databases['notifications']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Settings Database: {self.databases['settings']}{Colors.END}")
            print(f"{Colors.GREEN}✅ Logs Database: {self.databases['logs']}{Colors.END}")
            
            # Seed initial data
            self.seed_initial_data()
            
            print()
            print_header("🚀 Database Forge Complete!")
            print(f"{Colors.GREEN}🎉 All 8 core databases created successfully!{Colors.END}")
            print(f"{Colors.BLUE}📊 Total sample leads: 10 high-quality prospects{Colors.END}")
            print(f"{Colors.BLUE}⚙️ Default settings and configurations applied{Colors.END}")
            print(f"{Colors.YELLOW}💡 Your UI is now ready with sample data!{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error during database creation: {str(e)}{Colors.END}")
            raise

def main():
    """Main execution function"""
    forge = DatabaseForge()
    forge.forge_all_databases()

if __name__ == "__main__":
    main()
