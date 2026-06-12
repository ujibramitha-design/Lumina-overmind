# 🚀 Lead Simulation Script - Documentation

## Overview
Advanced lead simulation script for testing the Lumina Webhook Intake Engine with hacker aesthetic terminal output and realistic payload generation.

## 🎯 Purpose
- Test webhook endpoints with realistic lead data
- Validate token authentication
- Verify lead scoring integration
- Monitor API response handling
- Provide visual feedback with terminal styling

## 🔧 Technical Implementation

### Dependencies
```python
import requests      # HTTP requests
import json          # JSON handling
import time          # Delays and timing
import random        # Random delays
import sys           # System operations
from datetime import datetime  # Timestamps
```

### ANSI Color System
```python
class Colors:
    GREEN = '\033[92m'      # Success messages
    BLUE = '\033[94m'       # Info messages
    YELLOW = '\033[93m'     # Warnings
    RED = '\033[91m'        # Errors
    CYAN = '\033[96m'       # Primary accent
    MAGENTA = '\033[95m'    # Headers
    WHITE = '\033[97m'      # Bright text
    BOLD = '\033[1m'        # Bold text
    DIM = '\033[2m'         # Dim text
    UNDERLINE = '\033[4m'    # Underlined text
    BLINK = '\033[5m'       # Blinking text
    REVERSE = '\033[7m'     # Reverse video
    END = '\033[0m'         # Reset formatting
```

## 📦 Lead Payloads

### Lead 1 (Hot) - Budi Santoso
```python
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
```

**Expected Score:** 85-95 (Hot)
**Hot Keywords:** "jual", "subsidi", "kpr", "dp", "strategis"

### Lead 2 (Warm) - Sarah Putri
```python
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
```

**Expected Score:** 70-85 (Warm)
**Warm Keywords:** "investasi", "rumah", "cluster", "fasilitas"

### Lead 3 (Cold) - Rudi
```python
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
```

**Expected Score:** 40-50 (Cold)
**Keywords:** None (minimal data)

## 🎨 Terminal Output Features

### Typewriter Effect
```python
def typewriter_effect(text, delay=0.03):
    """Create typewriter effect for text"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
```

### Hacker-Style Logging
```python
def print_hacker(message, color='cyan'):
    """Print message with hacker aesthetic"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    prefix = f"{Colors.DIM}[{timestamp}]{Colors.END}"
    color_code = getattr(Colors, color.upper(), Colors.CYAN)
    print(f"{prefix} {color_code}►{Colors.END} {color_code}{message}{Colors.END}")
```

### Visual Indicators
- **🔧** - Configuration/System info
- **🚀** - Action/Transmission
- **✅** - Success
- **❌** - Error
- **⚠️** - Warning
- **📦** - Data/Payload
- **📡** - Network transmission
- **📊** - Results/Statistics
- **🔍** - Health check
- **⏳** - Waiting/Delay

## 🔄 Execution Flow

### 1. Initialization
```python
# Print header with typewriter effect
typewriter_effect("🔐 HUNTER AGENT AI MARKETING DIGITAL - LEAD SIMULATION SYSTEM", 0.02)
typewriter_effect("🚀 FASE 3: THE INTAKE ENGINE - WEBHOOK SIMULATOR", 0.02)
```

### 2. Configuration Display
```python
print_hacker("🔧 System Configuration:", 'magenta')
url = "http://localhost:8000/api/webhook/incoming-lead"
headers = {
    'Content-Type': 'application/json',
    'X-Lumina-Token': 'DUMMY-TOKEN-123'
}
```

### 3. Health Check
```python
print_hacker("🔍 Checking API Health...", 'blue')
try:
    health_response = requests.get("http://localhost:8000/api/webhook/health", timeout=5)
    if health_response.status_code == 200:
        print_success("API Health Check Passed")
    else:
        print_warning(f"Health check returned: {health_response.status_code}")
except:
    print_error("API Health Check Failed")
```

### 4. Lead Transmission
```python
for i, (payload, description) in enumerate(zip(payloads, lead_descriptions), 1):
    print_hacker(f"📡 TRANSMISSION {i}/3: {description}", 'cyan')
    result = send_lead_to_webhook(payload, headers, url)
    
    # Add delay between transmissions
    if i < len(payloads):
        delay = random.uniform(1.0, 3.0)
        print_hacker(f"⏳ Waiting {delay:.1f} seconds...", 'yellow')
        time.sleep(delay)
```

### 5. Response Processing
```python
if response.status_code == 201:
    print_success(f"Status: {response.status_code} Created")
    
    # Parse response
    response_data = response.json()
    data = response_data.get("data", {})
    
    # Display results
    print_hacker("📊 Processing Results:", 'green')
    print_hacker(f"   Lead ID: {data.get('lead_id', 'N/A')}", 'dim')
    print_hacker(f"   Score: {data.get('score', 'N/A')}", 'dim')
    
    # Color code based on score
    score = data.get('score', 0)
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
```

### 6. Summary Report
```python
print_hacker("🎯 TRANSMISSION SUMMARY", 'magenta')
print_hacker(f"📊 Total Leads Processed: {len(payloads)}", 'dim')
print_success(f"✅ Successful: {successful_leads}")
print_error(f"❌ Failed: {failed_leads}")
print_hacker(f"📈 Success Rate: {(successful_leads/len(payloads)*100):.1f}%", 'dim')
```

## 🚨 Error Handling

### Network Errors
```python
except requests.exceptions.Timeout:
    print_error("Request timeout!")
    print_hacker("   Connection timed out after 10 seconds", 'dim')
    
except requests.exceptions.ConnectionError:
    print_error("Connection error!")
    print_hacker("   Failed to connect to webhook server", 'dim')
    
except requests.exceptions.RequestException as e:
    print_error(f"Request failed: {e}")
```

### HTTP Status Codes
```python
if response.status_code == 201:
    print_success(f"Status: {response.status_code} Created")
elif response.status_code == 401:
    print_error(f"Status: {response.status_code} Unauthorized")
    print_error("   Token validation failed!")
elif response.status_code == 422:
    print_error(f"Status: {response.status_code} Unprocessable Entity")
    print_error("   Payload validation failed!")
```

### JSON Parsing
```python
try:
    response_data = response.json()
    if response_data.get("success"):
        # Process successful response
        pass
    else:
        print_error("Lead processing failed!")
        error_detail = response_data.get("detail", "Unknown error")
        print_hacker(f"   Error: {error_detail}", 'dim')
except json.JSONDecodeError:
    print_error("Failed to parse JSON response")
    print_hacker(f"   Raw response: {response.text[:200]}...", 'dim')
```

## 🎮 Usage Instructions

### 1. Start API Server
```bash
cd dashboard
python api/main.py
```

### 2. Run Simulation
```bash
cd dashboard
python scripts/simulate_incoming_leads.py
```

### 3. Expected Output
```
════════════════════════════════════════════════════════════════════════════════

🔐 HUNTER AGENT AI MARKETING DIGITAL - LEAD SIMULATION SYSTEM
🚀 FASE 3: THE INTAKE ENGINE - WEBHOOK SIMULATOR
════════════════════════════════════════════════════════════════════════════════

[01:47:55] ► 🔧 System Configuration:
[01:47:55] ►    Target URL: http://localhost:8000/api/webhook/incoming-lead
[01:47:55] ►    Auth Token: DUMMY-TOKEN-123
[01:47:55] ►    Content-Type: application/json

[01:47:55] ► 📦 Loading Lead Payloads:
[01:47:55] ►    Lead 1: 🔥 HOT LEAD - Budi Santoso (PNS, Serang, Facebook Ads)
[01:47:55] ►    Lead 2: ⚡ WARM LEAD - Sarah Putri (Wirausaha, TikTok Ads)
[01:47:55] ►    Lead 3: ❄️ COLD LEAD - Rudi (Organic Web, Minimal Data)

────────────────────────────────────────────────────────────────────────────────

[01:47:55] ► 🔍 Checking API Health...
[01:47:56] ► ✅ API Health Check Passed
[01:47:56] ►    Service: Lumina Webhook Intake Engine
[01:47:56] ►    Version: 1.0.0

────────────────────────────────────────────────────────────────────────────────

[01:47:56] ► 🚀 Starting Lead Transmission Sequence...

[01:47:56] ► 📡 TRANSMISSION 1/3: 🔥 HOT LEAD - Budi Santoso (PNS, Serang, Facebook Ads)
────────────────────────────────────────────────────────────────────────────────
[01:47:56] ► 📦 Preparing payload: Budi Santoso
[01:47:56] ►    Source: Facebook Ads
[01:47:56] ►    Phone: 08123456789
[01:47:56] ►    Occupation: PNS
[01:47:56] ►    Location: Serang
[01:47:56] ►    Campaign: PNS_Property_Promo_2026
[01:47:57] ► 🚀 Mengirim data lead...
[01:47:58] ► ✅ Status: 201 Created
[01:47:58] ► 📊 Processing Results:
[01:47:58] ►    Lead ID: 123
[01:47:58] ►    Name: Budi Santoso
[01:47:58] ►    Score: 92
[01:47:58] ►    Status: 🔥 Hot
[01:47:58] ►    Keywords Found:
[01:47:58] ►      • jual
[01:47:58] ►      • subsidi
[01:47:58] ►      • kpr
[01:47:58] ►      • dp
[01:47:58] ►    Processed: 2026-05-30T01:47:58.000Z
[01:47:58] ► ✅ Lead processing completed successfully!

════════════════════════════════════════════════════════════════════════════════

[01:48:01] ► 🎯 TRANSMISSION SUMMARY
────────────────────────────────────────────────────────────────────────────────
[01:48:01] ► 📊 Total Leads Processed: 3
[01:48:01] ► ✅ Successful: 3
[01:48:01] ► ❌ Failed: 0
[01:48:01] ► 📈 Success Rate: 100.0%
[01:48:01] ► 🎉 All leads transmitted successfully!
[01:48:01] ► 🔥 Lead Intake Engine is fully operational!

════════════════════════════════════════════════════════════════════════════════

[01:48:01] ► 🔚 SIMULATION COMPLETE
════════════════════════════════════════════════════════════════════════════════
```

## 🔧 Customization

### Adding New Leads
```python
# Add to create_payloads() function
lead_4 = {
    "nama": "New Lead Name",
    "no_hp": "08123456789",
    "email": "email@example.com",
    "sumber": "New Source",
    "campaign": "New Campaign",
    "catatan": "Additional notes",
    "lokasi": "New Location",
    "pekerjaan": "New Occupation"
}
```

### Modifying Delays
```python
# Change network delay range
delay = random.uniform(0.5, 5.0)  # Increase max delay

# Change transmission delay
delay = random.uniform(2.0, 5.0)  # Longer between transmissions
```

### Custom Colors
```python
# Add new color codes
PURPLE = '\033[95m'
ORANGE = '\033[93m'

# Use in print functions
print_hacker("Custom message", 'purple')
```

## 📊 Monitoring & Debugging

### Network Monitoring
```python
# Add timing measurements
start_time = time.time()
response = requests.post(url, json=payload, headers=headers, timeout=10)
end_time = time.time()

print_hacker(f"   Response Time: {(end_time - start_time):.2f}s", 'dim')
```

### Request Logging
```python
# Log full request details
print_hacker("📋 Request Details:", 'yellow')
print_hacker(f"   URL: {url}", 'dim')
print_hacker(f"   Method: POST", 'dim')
print_hacker(f"   Headers: {headers}", 'dim')
print_hacker(f"   Payload Size: {len(json.dumps(payload))} bytes", 'dim')
```

### Response Analysis
```python
# Analyze response headers
print_hacker("📋 Response Headers:", 'yellow')
for key, value in response.headers.items():
    print_hacker(f"   {key}: {value}", 'dim')
```

## 🔮 Advanced Features

### Batch Processing
```python
def send_batch_leads(payloads, headers, url):
    """Send multiple leads in parallel"""
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(send_lead_to_webhook, payload, headers, url)
            for payload in payloads
        ]
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            # Process results
```

### Configurable Simulation
```python
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Lead Simulation Script')
    parser.add_argument('--url', default='http://localhost:8000/api/webhook/incoming-lead')
    parser.add_argument('--token', default='DUMMY-TOKEN-123')
    parser.add_argument('--count', type=int, default=3)
    parser.add_argument('--delay', type=float, default=1.0)
    return parser.parse_args()
```

### Real-time Monitoring
```python
def monitor_database():
    """Monitor database changes in real-time"""
    import sqlite3
    import time
    
    while True:
        conn = sqlite3.connect('data/leads.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM leads WHERE created_at > ?", (datetime.now() - timedelta(minutes=1),))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print_hacker(f"📊 New leads in last minute: {count}", 'green')
        
        conn.close()
        time.sleep(10)
```

## 🚀 Production Deployment

### Environment Configuration
```python
# Use environment variables
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'http://localhost:8000/api/webhook/incoming-lead')
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN', 'DUMMY-TOKEN-123')
```

### Logging Integration
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lead_simulation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Error Reporting
```python
def report_error(error, context):
    """Report errors to monitoring system"""
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error': str(error),
        'context': context,
        'script_version': '1.0.0'
    }
    
    # Send to monitoring system
    requests.post('https://monitoring.example.com/errors', json=error_data)
```

## 📁 File Structure
```
dashboard/
├── scripts/
│   └── simulate_incoming_leads.py    # Main simulation script
├── api/
│   └── main.py                      # Webhook endpoints
├── data/
│   └── leads.db                    # SQLite database
└── LEAD_SIMULATION_DOCUMENTATION.md   # This documentation
```

## 🔧 Troubleshooting

### Common Issues

#### Connection Refused
```bash
# Check if API server is running
curl http://localhost:8000/api/webhook/health

# Start server
python api/main.py
```

#### Token Authentication Error
```bash
# Verify token
grep -n "DUMMY-TOKEN-123" api/main.py

# Check headers in script
grep -A 5 "headers =" scripts/simulate_incoming_leads.py
```

#### Payload Validation Error
```bash
# Test with minimal payload
curl -X POST http://localhost:8000/api/webhook/incoming-lead \
  -H "Content-Type: application/json" \
  -H "X-Lumina-Token: DUMMY-TOKEN-123" \
  -d '{"nama": "Test", "no_hp": "08123456789", "sumber": "test"}'
```

#### Database Errors
```bash
# Check database file
ls -la data/leads.db

# Test database connection
python -c "
import sqlite3
conn = sqlite3.connect('data/leads.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM leads')
print(f'Total leads: {cursor.fetchone()[0]}')
conn.close()
"
```

---

## 🎯 Key Features Summary

### Visual Design
- **Hacker Aesthetic**: Terminal styling with ANSI colors
- **Typewriter Effect**: Animated text display
- **Visual Indicators**: Emoji and symbol-based status
- **Structured Output**: Organized logging and reporting

### Functional Features
- **Realistic Payloads**: Three lead types (Hot/Warm/Cold)
- **Network Simulation**: Random delays and timing
- **Health Checking**: API availability validation
- **Error Handling**: Comprehensive exception management
- **Response Analysis**: Detailed result processing

### Technical Features
- **Token Authentication**: Proper header validation
- **JSON Processing**: Request/response handling
- **Scoring Integration**: AI lead scoring validation
- **Database Testing**: Lead storage verification
- **Summary Reporting**: Success rate statistics

---

*Last updated: May 30, 2026*
