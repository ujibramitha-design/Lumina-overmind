# 🚀 Lumina OS Background Services - Documentation

## Overview
Advanced background service modules for continuous data collection and market intelligence, designed for 24/7 operation within the Lumina OS ecosystem.

## 🔧 Service Architecture

### Service Components
- **Banten Government Intelligence**: PNS & P3K data extraction
- **Property Market Scraper**: Competitive price analysis
- **Continuous Operation**: Infinite loop with 10-second intervals
- **Database Integration**: SQLite storage for analytics
- **Hacker Aesthetic**: Terminal styling with colored output

## 🏛️ Banten Government Intelligence Service

### File: `scripts/run_banten_government_intelligence.py`

#### **Purpose**
Simulates extraction of PNS & P3K employee data from Banten Provincial Government systems for lead generation.

#### **Core Features**
- **Data Simulation**: Realistic PNS profile generation
- **Intent Analysis**: Purchase intent scoring algorithm
- **Database Storage**: Automatic lead insertion to leads.db
- **Continuous Scanning**: 10-second interval cycles
- **Hacker Terminal**: Blue/cyan colored output

#### **Data Flow**
```
Banten Gov Systems → Data Extraction → Intent Analysis → Lead Generation → Database Storage
```

#### **Key Functions**

##### `simulate_banten_gov_scan()`
```python
def simulate_banten_gov_scan() -> List[Dict[str, Any]]:
    """Simulate scanning Banten Government systems for PNS & P3K data"""
    print_hacker("🌐 Targeting Banten Gov Server...", 'blue')
    print_hacker("🔓 Bypassing security protocols...", 'yellow')
    print_hacker("📊 Accessing PNS & P3K database...", 'blue')
    
    # Generate 8-15 PNS profiles
    num_profiles = random.randint(8, 15)
    print_hacker(f"🎯 Found {num_profiles} high-intent PNS profiles...", 'cyan')
```

##### `analyze_pns_intent()`
```python
def analyze_pns_intent(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze PNS profile for property purchase intent"""
    intent_score = 0
    
    # High income indicates purchasing power
    if profile['pendapatan'] > 10000000:
        intent_score += 30
        intent_factors.append('High income (>10M/month)')
    
    # Higher golongan indicates stability
    if profile['golongan'] in ['IV/a', 'IV/b']:
        intent_score += 25
        intent_factors.append('Senior golongan (IV)')
```

##### `save_to_leads_db()`
```python
def save_to_leads_db(profiles: List[Dict[str, Any]]):
    """Save PNS profiles to leads database"""
    for profile in profiles:
        intent_analysis = analyze_pns_intent(profile)
        
        # Generate AI follow-up notes
        catatan_followup = {
            'message': f"High-value government employee detected...",
            'metadata': {
                'source': 'Banten_Gov_Intel',
                'pekerjaan': 'PNS Pemprov Banten',
                'intent_score': intent_analysis['intent_score']
            }
        }
```

#### **Generated Data Structure**
```python
profile = {
    'nama': 'Ahmad Santoso',
    'nip': '1985123456789012',
    'golongan': 'IV/a',
    'unit_kerja': 'Dinas Pendidikan',
    'lokasi': 'Serang',
    'pendapatan': 12000000,
    'status_kepegawaian': 'PNS'
}
```

#### **Intent Scoring Algorithm**
- **High Income (>10M/month)**: +30 points
- **Senior Golongan (IV)**: +25 points
- **Permanent PNS Status**: +20 points
- **High-Value Unit**: +15 points
- **Prime Location**: +10 points
- **Total Score**: 0-100 (High: ≥70, Medium: ≥40, Low: <40)

#### **Terminal Output Example**
```
[14:23:45] ► 🔍 Initiating Banten Government Intelligence Scan...
[14:23:46] ► 🌐 Targeting Banten Gov Server...
[14:23:47] ► 🔓 Bypassing security protocols...
[14:23:48] ► 📊 Accessing PNS & P3K database...
[14:23:50] ► 🎯 Found 12 high-intent PNS profiles...
[14:23:51] ► 💾 Saved PNS profile: Ahmad Santoso (Dinas Pendidikan)
[14:23:52] ► ✅ Successfully saved 12 PNS profiles to database
```

## 🏠 Property Market Scraper Service

### File: `scripts/run_property_market_scraper.py`

#### **Purpose**
Simulates competitive property price analysis from major property portals for market intelligence.

#### **Core Features**
- **Portal Simulation**: Rumah123, 99.co, Lamudi, UrbanIndo
- **Price Analysis**: Market gap detection and trend analysis
- **Database Storage**: Analytics.db with market_data and price_analysis tables
- **Continuous Monitoring**: 10-second interval cycles
- **Hacker Terminal**: Yellow/orange colored output

#### **Data Flow**
```
Property Portals → Data Extraction → Price Analysis → Market Intelligence → Database Storage
```

#### **Key Functions**

##### `simulate_property_scrape()`
```python
def simulate_property_scrape() -> List[Dict[str, Any]]:
    """Simulate scraping property data from major portals"""
    locations = ['Serang', 'Cilegon', 'Tangerang', 'Pandeglang', 'Lebak']
    target_location = random.choice(locations)
    
    print_hacker(f"🌐 Scanning competitor pricing in {target_location}...", 'yellow')
    
    portals = ['Rumah123', '99.co', 'Lamudi', 'UrbanIndo']
    target_portal = random.choice(portals)
    
    print_hacker(f"🔓 Accessing {target_portal} database...", 'blue')
```

##### `analyze_market_data()`
```python
def analyze_market_data(listings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze scraped market data and identify opportunities"""
    
    # Calculate market gap (compared to our target price)
    our_target_price = get_base_price(location, property_type)
    market_gap_percent = ((our_target_price - price_avg) / price_avg) * 100
    
    # Determine trend
    if market_gap_percent > 10:
        trend = 'Undervalued'
    elif market_gap_percent < -10:
        trend = 'Overvalued'
    else:
        trend = 'Stable'
```

##### `save_to_analytics_db()`
```python
def save_to_analytics_db(analysis_data: Dict[str, Any]):
    """Save market analysis data to analytics database"""
    
    # Insert into market_data table
    cursor.execute('''
        INSERT INTO market_data (
            property_type, location, price_min, price_max, price_avg,
            competitor, listing_count, price_per_meter, scan_timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''')
    
    # Insert into price_analysis table
    cursor.execute('''
        INSERT INTO price_analysis (
            location, property_type, avg_price, price_trend,
            market_gap_percent, competitor_count, analysis_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''')
```

#### **Generated Data Structure**
```python
listing = {
    'property_type': 'Rumah',
    'location': 'Serang',
    'price': 550000000,
    'area': 120,
    'price_per_meter': 4583333,
    'portal': 'Rumah123',
    'title': 'Modern Rumah Full Furnished di Serang',
    'facilities': ['AC', 'Water Heater', 'Carport', 'Garden']
}
```

#### **Price Analysis Algorithm**
- **Base Price Calculation**: Location and property type specific
- **Market Gap**: ((target_price - avg_price) / avg_price) * 100
- **Trend Detection**: Undervalued (>+10%), Overvalued (<-10%), Stable
- **Competitor Analysis**: Portal distribution and listing counts

#### **Terminal Output Example**
```
[14:23:45] ► 🔍 Initiating Property Market Intelligence Scan...
[14:23:46] ► 🌐 Scanning competitor pricing in Serang...
[14:23:48] ► 🔓 Accessing Rumah123 database...
[14:23:50] ► 📊 Extracting property listings...
[14:23:52] ► 🎯 Found 25 active listings in Serang
[14:23:53] ► ⚠️  Price gap detected: 15% below market average for Rumah in Serang
[14:23:54] ► 💾 Saved market data: Rumah in Serang
```

## 🗄️ Database Schema

### Leads Database (`data/leads.db`)
```sql
CREATE TABLE leads (
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
);
```

### Analytics Database (`data/analytics.db`)
```sql
CREATE TABLE market_data (
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
);

CREATE TABLE price_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    property_type TEXT NOT NULL,
    avg_price REAL NOT NULL,
    price_trend TEXT,
    market_gap_percent REAL,
    competitor_count INTEGER,
    analysis_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 Terminal Aesthetic

### Color Scheme
```python
class Colors:
    GREEN = '\033[92m'      # Success messages
    BLUE = '\033[94m'       # Info messages
    CYAN = '\033[96m'       # Primary accent
    YELLOW = '\033[93m'     # Warnings
    ORANGE = '\033[38;5;208m' # Property scraper
    RED = '\033[91m'        # Errors
    MAGENTA = '\033[95m'    # Headers
    BOLD = '\033[1m'        # Bold text
    DIM = '\033[2m'         # Dim text
    END = '\033[0m'         # Reset formatting
```

### Message Format
```python
def print_hacker(message, color='cyan'):
    timestamp = datetime.now().strftime('%H:%M:%S')
    prefix = f"{Colors.DIM}[{timestamp}]{Colors.END}"
    color_code = getattr(Colors, color.upper(), Colors.CYAN)
    print(f"{prefix} {color_code}►{Colors.END} {color_code}{message}{Colors.END}")
```

### Visual Indicators
- **🔍** - Scanning/Analysis
- **🌐** - Network/Server access
- **🔓** - Security bypass
- **📊** - Data extraction
- **🎯** - Target found
- **💾** - Data saved
- **✅** - Success
- **⚠️** - Warning/Alert
- **❌** - Error

## 🚀 Deployment & Operation

### Standalone Execution
```bash
# Banten Government Intelligence
python scripts/run_banten_government_intelligence.py

# Property Market Scraper
python scripts/run_property_market_scraper.py
```

### Background Service Mode
Both services run in infinite loops with 10-second intervals:
```python
while True:
    # Perform scan/analysis
    scan_data = perform_scan()
    
    # Save to database
    save_to_database(scan_data)
    
    # Display results
    display_report(scan_data)
    
    # Wait for next cycle
    time.sleep(10)
```

### Integration with Next.js Orchestrator
```javascript
// In orchestrator service
const { spawn } = require('child_process');

// Start Banten Government Intelligence
const bantenService = spawn('python', ['scripts/run_banten_government_intelligence.py']);

// Start Property Market Scraper
const propertyService = spawn('python', ['scripts/run_property_market_scraper.py']);

// Handle service output
bantenService.stdout.on('data', (data) => {
    console.log(`Banten Intel: ${data}`);
});

propertyService.stdout.on('data', (data) => {
    console.log(`Property Scraper: ${data}`);
});
```

## 📊 Monitoring & Analytics

### Service Health Monitoring
```python
# Service status indicators
print_hacker("🚀 Banten Government Intelligence Service: Active", 'green')
print_hacker("🔄 Continuous monitoring mode: Enabled", 'blue')
print_hacker("📊 Scan cycles completed: 42", 'cyan')
```

### Database Statistics
```python
# Query database for statistics
cursor.execute("SELECT COUNT(*) FROM leads WHERE source = 'Banten_Gov_Intel'")
pns_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM market_data")
market_data_count = cursor.fetchone()[0]
```

### Performance Metrics
- **Scan Frequency**: Every 10 seconds
- **Data Volume**: 8-15 PNS profiles, 15-35 property listings per cycle
- **Database Growth**: Continuous storage of intelligence data
- **Processing Time**: 5-10 seconds per cycle

## 🔧 Configuration

### Environment Setup
```python
# Database paths
LEADS_DB_PATH = '../data/leads.db'
ANALYTICS_DB_PATH = '../data/analytics.db'

# Scan intervals
SCAN_INTERVAL_SECONDS = 10

# Data generation ranges
PNS_PROFILES_MIN = 8
PNS_PROFILES_MAX = 15
PROPERTY_LISTINGS_MIN = 15
PROPERTY_LISTINGS_MAX = 35
```

### Customization Options
```python
# Modify target locations
BANTEN_LOCATIONS = ['Serang', 'Cilegon', 'Tangerang', 'Pandeglang', 'Lebak']

# Modify property portals
PROPERTY_PORTALS = ['Rumah123', '99.co', 'Lamudi', 'UrbanIndo']

# Modify intent scoring weights
INTENT_WEIGHTS = {
    'high_income': 30,
    'senior_golongan': 25,
    'permanent_status': 20,
    'high_value_unit': 15,
    'prime_location': 10
}
```

## 🔮 Advanced Features

### Intent Analysis Enhancement
```python
def enhanced_intent_analysis(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced intent analysis with ML-like scoring"""
    
    # Multi-factor analysis
    income_score = calculate_income_score(profile['pendapatan'])
    stability_score = calculate_stability_score(profile['golongan'], profile['status_kepegawaian'])
    location_score = calculate_location_score(profile['lokasi'])
    unit_score = calculate_unit_score(profile['unit_kerja'])
    
    # Weighted combination
    final_score = (
        income_score * 0.35 +
        stability_score * 0.30 +
        location_score * 0.20 +
        unit_score * 0.15
    )
    
    return {
        'intent_score': final_score,
        'confidence': calculate_confidence(profile),
        'recommendations': generate_recommendations(final_score)
    }
```

### Market Prediction
```python
def predict_market_trends(historical_data: List[Dict]) -> Dict[str, Any]:
    """Predict future market trends based on historical data"""
    
    # Simple trend analysis
    price_changes = calculate_price_changes(historical_data)
    trend_direction = analyze_trend_direction(price_changes)
    
    return {
        'predicted_trend': trend_direction,
        'confidence_level': calculate_confidence_level(price_changes),
        'next_period_forecast': generate_forecast(price_changes)
    }
```

### Real-time Alerts
```python
def check_market_alerts(analysis_data: Dict[str, Any]) -> List[str]:
    """Check for market conditions that require attention"""
    alerts = []
    
    for result in analysis_data['analysis_results']:
        # Price gap alert
        if abs(result['market_gap_percent']) > 20:
            alerts.append(f"Significant price gap: {result['market_gap_percent']:.1f}% for {result['property_type']} in {result['location']}")
        
        # Low competition alert
        if result['competitor_count'] < 3:
            alerts.append(f"Low competition detected: {result['competitor_count']} competitors for {result['property_type']} in {result['location']}")
        
        # High demand alert
        if result['listing_count'] > 30:
            alerts.append(f"High demand area: {result['listing_count']} listings for {result['property_type']} in {result['location']}")
    
    return alerts
```

## 🚨 Error Handling & Recovery

### Database Connection Errors
```python
try:
    conn = get_db_connection(db_path)
    # Perform operations
except sqlite3.Error as e:
    print_error(f"Database connection error: {e}")
    # Wait and retry
    time.sleep(5)
    continue
finally:
    if 'conn' in locals():
        conn.close()
```

### Network Simulation Errors
```python
def simulate_network_operation():
    """Simulate network operation with potential failures"""
    if random.random() < 0.05:  # 5% failure rate
        print_warning("Network timeout detected, retrying...")
        time.sleep(2)
        return simulate_network_operation()
    return True
```

### Graceful Shutdown
```python
try:
    while True:
        perform_scan_cycle()
        time.sleep(10)
except KeyboardInterrupt:
    print_hacker("⚠️  Service interrupted by user", 'yellow')
    print_hacker("🔚 Service stopped gracefully", 'magenta')
    sys.exit(130)
except Exception as e:
    print_error(f"Critical error: {e}")
    sys.exit(1)
```

## 📈 Performance Optimization

### Database Optimization
```python
# Use transactions for bulk operations
conn.execute("BEGIN TRANSACTION")
for data in bulk_data:
    conn.execute(insert_query, data)
conn.commit()

# Create indexes for faster queries
conn.execute("CREATE INDEX IF NOT EXISTS idx_leads_source ON leads(source)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_market_data_location ON market_data(location)")
```

### Memory Management
```python
# Process data in batches to avoid memory issues
def process_large_dataset(data, batch_size=100):
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        process_batch(batch)
        
        # Clear memory
        del batch
        gc.collect()
```

### Concurrent Operations
```python
import threading
from concurrent.futures import ThreadPoolExecutor

def parallel_scan():
    """Run multiple scans in parallel"""
    with ThreadPoolExecutor(max_workers=2) as executor:
        banten_future = executor.submit(banten_gov_scan)
        property_future = executor.submit(property_scan)
        
        banten_results = banten_future.result()
        property_results = property_future.result()
        
    return banten_results, property_results
```

## 🔒 Security Considerations

### Data Protection
```python
# Encrypt sensitive data
def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive PNS data"""
    # Use encryption library
    encrypted = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()

# Anonymize data for storage
def anonymize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Remove or mask sensitive information"""
    anonymized = profile.copy()
    anonymized['nip'] = mask_nip(profile['nip'])
    return anonymized
```

### Access Control
```python
# Add access logging
def log_access(operation: str, user: str = 'system'):
    """Log all data access operations"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'operation': operation,
        'user': user,
        'ip_address': get_client_ip()
    }
    write_access_log(log_entry)
```

## 📱 Integration Examples

### API Integration
```python
# Add REST API endpoints for real-time data access
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/banten-intelligence/latest')
def get_latest_banten_data():
    """Get latest Banten intelligence data"""
    conn = get_db_connection('../data/leads.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM leads 
        WHERE source = 'Banten_Gov_Intel' 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'success': True, 'data': results})
```

### WebSocket Integration
```python
# Real-time data streaming
import asyncio
import websockets

async def stream_intelligence():
    """Stream intelligence data in real-time"""
    while True:
        data = get_latest_intelligence()
        await websocket.send(json.dumps(data))
        await asyncio.sleep(10)
```

---

## 🎯 Key Features Summary

### Banten Government Intelligence
- **Data Source**: Simulated Banten Government systems
- **Target Profile**: PNS & P3K employees
- **Analysis**: Purchase intent scoring (0-100)
- **Storage**: leads.db with AI follow-up notes
- **Frequency**: Every 10 seconds
- **Output**: Blue/cyan hacker terminal

### Property Market Scraper
- **Data Source**: Major property portals (Rumah123, 99.co, etc.)
- **Target Data**: Property prices and market trends
- **Analysis**: Market gap detection and trend analysis
- **Storage**: analytics.db with market_data and price_analysis tables
- **Frequency**: Every 10 seconds
- **Output**: Yellow/orange hacker terminal

### Technical Features
- **Background Service**: Infinite loop operation
- **Database Integration**: SQLite with proper schema
- **Error Handling**: Comprehensive exception management
- **Terminal Aesthetic**: Hacker-style colored output
- **Modular Design**: Standalone execution capability
- **Performance**: Optimized for continuous operation

---

*Last updated: May 30, 2026*
