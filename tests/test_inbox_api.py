#!/usr/bin/env python3
"""
Test Script for Omni-Channel Inbox API Endpoints
Tests the new inbox endpoints with SQLite database integration
"""

import requests
import json
import os
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "pending": f"{BASE_URL}/api/inbox/pending",
    "approve": f"{BASE_URL}/api/inbox/approve/",
    "stats": f"{BASE_URL}/api/inbox/stats"
}

# Colors for console output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log(message, color='reset'):
    print(f"{getattr(Colors, color.upper(), '')}{message}{Colors.END}")

def log_success(message):
    log(f"✅ {message}", 'green')

def log_error(message):
    log(f"❌ {message}", 'red')

def log_info(message):
    log(f"ℹ️  {message}", 'blue')

def log_header(message):
    log(f"🔧 {message}", 'bold cyan')

def setup_test_database():
    """Create test database with sample data"""
    db_path = os.path.join('data', 'leads.db (SQLite - removed))
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Create leads table
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
        
        # Clear existing test data
        # cursor.execute() removed"DELETE FROM leads WHERE business_name LIKE 'Test Lead%'")
        
        # Insert test data
        test_leads = [
            {
                'business_name': 'Test Lead 1 - Follow Up with Notes',
                'contact': 'Interested in property investment',
                'url': 'https://example.com/1',
                'keywords': 'investasi,properti',
                'source': 'web',
                'score': 85.0,
                'status': 'Follow Up',
                'location': 'Jakarta',
                'catatan_followup': json.dumps({
                    'message': 'Lead is interested in investment properties, follow up required',
                    'metadata': {
                        'priority': 'high',
                        'contact_method': 'phone',
                        'last_contact': '2026-05-29'
                    }
                })
            },
            {
                'business_name': 'Test Lead 2 - Follow Up with Complex Notes',
                'contact': 'Looking for family home in suburban area',
                'url': 'https://example.com/2',
                'keywords': 'rumah,keluarga',
                'source': 'social',
                'score': 75.0,
                'status': 'Follow Up',
                'location': 'Tangerang',
                'catatan_followup': json.dumps({
                    'message': 'Family looking for 3BR house, budget 500M, prefers quiet area',
                    'metadata': {
                        'budget': '500M',
                        'requirements': ['3BR', 'quiet_area', 'near_school'],
                        'family_size': 4,
                        'timeline': '2_months'
                    }
                })
            },
            {
                'business_name': 'Test Lead 3 - Invalid JSON Notes',
                'contact': 'Contact information available',
                'url': 'https://example.com/3',
                'keywords': 'kontak',
                'source': 'email',
                'score': 60.0,
                'status': 'Follow Up',
                'location': 'Bogor',
                'catatan_followup': 'Invalid JSON string {broken'
            },
            {
                'business_name': 'Test Lead 4 - No Follow Up Notes',
                'contact': 'General inquiry',
                'url': 'https://example.com/4',
                'keywords': 'info',
                'source': 'web',
                'score': 45.0,
                'status': 'Follow Up',
                'location': 'Depok',
                'catatan_followup': None
            },
            {
                'business_name': 'Test Lead 5 - Already Contacted',
                'contact': 'Already processed',
                'url': 'https://example.com/5',
                'keywords': 'processed',
                'source': 'phone',
                'score': 90.0,
                'status': 'Contacted',
                'location': 'Bandung',
                'catatan_followup': json.dumps({
                    'message': 'Already contacted and processed',
                    'metadata': {'status': 'completed'}
                })
            },
            {
                'business_name': 'Test Lead 6 - New Lead',
                'contact': 'New inquiry received',
                'url': 'https://example.com/6',
                'keywords': 'baru',
                'source': 'web',
                'score': 70.0,
                'status': 'New',
                'location': 'Surabaya',
                'catatan_followup': None
            }
        ]
        
        for lead in test_leads:
            # cursor.execute() removed'''
                INSERT INTO leads (
                    business_name, contact, url, keywords, source, score, status, 
                    location, catatan_followup
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead['business_name'],
                lead['contact'],
                lead['url'],
                lead['keywords'],
                lead['source'],
                lead['score'],
                lead['status'],
                lead['location'],
                lead['catatan_followup']
            ))
        
        # conn.commit() removed
        # conn.close() removed
        
        log_success("Test database setup completed")
        log_info(f"Created {len(test_leads)} test leads")
        return True
        
    except Exception as e:
        log_error(f"Database setup failed: {e}")
        return False

def test_health_check():
    """Test API health check"""
    log_header("Testing API Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            log_success("API is healthy")
            return True
        else:
            log_error(f"API health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"API connection failed: {e}")
        return False

def test_get_pending_leads():
    """Test GET /api/inbox/pending endpoint"""
    log_header("Testing GET /api/inbox/pending")
    
    try:
        response = requests.get(API_ENDPOINTS["pending"], timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                leads = data.get("data", {}).get("leads", [])
                total = data.get("data", {}).get("total", 0)
                
                log_success(f"Retrieved {total} pending leads")
                
                # Validate response structure
                for lead in leads:
                    required_fields = ["id", "business_name", "status", "catatan_followup"]
                    for field in required_fields:
                        if field not in lead:
                            log_error(f"Missing required field: {field}")
                            return False
                
                # Check catatan_followup parsing
                for lead in leads:
                    followup = lead.get("catatan_followup")
                    if followup:
                        if isinstance(followup, dict):
                            if "message" in followup or "parse_error" in followup:
                                log_success(f"Lead {lead['id']}: Follow-up parsed correctly")
                            else:
                                log_error(f"Lead {lead['id']}: Invalid follow-up structure")
                                return False
                        else:
                            log_error(f"Lead {lead['id']}: Follow-up not parsed as dict")
                            return False
                
                log_success("Pending leads endpoint validation passed")
                return True
            else:
                log_error(f"API returned error: {data}")
                return False
        else:
            log_error(f"HTTP error: {response.status_code}")
            log_error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"JSON decode error: {e}")
        return False

def test_approve_lead():
    """Test POST /api/inbox/approve/{lead_id} endpoint"""
    log_header("Testing POST /api/inbox/approve/{lead_id}")
    
    try:
        # First get a pending lead to approve
        response = requests.get(API_ENDPOINTS["pending"], timeout=10)
        
        if response.status_code != 200:
            log_error("Failed to get pending leads for approval test")
            return False
        
        data = response.json()
        leads = data.get("data", {}).get("leads", [])
        
        if not leads:
            log_error("No pending leads available for approval test")
            return False
        
        # Get first pending lead
        test_lead = leads[0]
        lead_id = test_lead["id"]
        old_status = test_lead["status"]
        
        log_info(f"Testing approval for lead {lead_id} (current status: {old_status})")
        
        # Approve the lead
        approve_response = requests.post(f"{API_ENDPOINTS['approve']}{lead_id}", timeout=10)
        
        if approve_response.status_code == 200:
            approve_data = approve_response.json()
            
            if approve_data.get("success"):
                new_status = approve_data.get("data", {}).get("new_status")
                
                if new_status == "Contacted":
                    log_success(f"Lead {lead_id} approved successfully")
                    log_info(f"Status changed from '{old_status}' to '{new_status}'")
                    return True
                else:
                    log_error(f"Unexpected status change: {old_status} -> {new_status}")
                    return False
            else:
                log_error(f"Approval API returned error: {approve_data}")
                return False
        else:
            log_error(f"Approval HTTP error: {approve_response.status_code}")
            log_error(f"Response: {approve_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Approval request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"Approval JSON decode error: {e}")
        return False

def test_invalid_approve():
    """Test approval with invalid lead ID"""
    log_header("Testing POST /api/inbox/approve with invalid ID")
    
    try:
        # Test with non-existent ID
        response = requests.post(f"{API_ENDPOINTS['approve']}99999", timeout=10)
        
        if response.status_code == 404:
            log_success("Correctly returned 404 for non-existent lead")
        else:
            log_error(f"Expected 404, got {response.status_code}")
            return False
        
        # Test with invalid ID type
        response = requests.post(f"{API_ENDPOINTS['approve']}invalid", timeout=10)
        
        if response.status_code == 404 or response.status_code == 422:
            log_success("Correctly handled invalid ID type")
        else:
            log_error(f"Expected 404/422, got {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        log_error(f"Invalid approval test failed: {e}")
        return False

def test_inbox_stats():
    """Test GET /api/inbox/stats endpoint"""
    log_header("Testing GET /api/inbox/stats")
    
    try:
        response = requests.get(API_ENDPOINTS["stats"], timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                stats = data.get("data", {})
                
                # Validate required fields
                required_fields = ["total_leads", "pending_leads", "status_breakdown", "pending_breakdown"]
                for field in required_fields:
                    if field not in stats:
                        log_error(f"Missing required field: {field}")
                        return False
                
                log_success(f"Stats retrieved successfully")
                log_info(f"Total leads: {stats.get('total_leads')}")
                log_info(f"Pending leads: {stats.get('pending_leads')}")
                log_info(f"Status breakdown: {stats.get('status_breakdown')}")
                
                return True
            else:
                log_error(f"Stats API returned error: {data}")
                return False
        else:
            log_error(f"Stats HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Stats request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"Stats JSON decode error: {e}")
        return False

def test_database_integrity():
    """Test database integrity after API operations"""
    log_header("Testing Database Integrity")
    
    try:
        db_path = os.path.join('data', 'leads.db (SQLite - removed))
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Count total leads
        # cursor.execute() removed"SELECT COUNT(*) FROM leads WHERE business_name LIKE 'Test Lead%'")
        total_test_leads = cursor.fetchone()[0]
        
        # Count by status
        # cursor.execute() removed"""
            SELECT status, COUNT(*) 
            FROM leads 
            WHERE business_name LIKE 'Test Lead%'
            GROUP BY status
        """)
        status_counts = dict(cursor.fetchall())
        
        # Count pending leads with notes
        # cursor.execute() removed"""
            SELECT COUNT(*) 
            FROM leads 
            WHERE business_name LIKE 'Test Lead%' 
            AND status = 'Follow Up' 
            AND catatan_followup IS NOT NULL 
            AND catatan_followup != ''
        """)
        pending_with_notes = cursor.fetchone()[0]
        
        # conn.close() removed
        
        log_info(f"Total test leads: {total_test_leads}")
        log_info(f"Status breakdown: {status_counts}")
        log_info(f"Pending with notes: {pending_with_notes}")
        
        # Validate expected counts
        expected_total = 6
        if total_test_leads != expected_total:
            log_error(f"Expected {expected_total} test leads, found {total_test_leads}")
            return False
        
        expected_pending = 3  # Leads 1, 2, 3 should have notes
        if pending_with_notes < expected_pending:
            log_error(f"Expected at least {expected_pending} pending leads with notes, found {pending_with_notes}")
            return False
        
        log_success("Database integrity check passed")
        return True
        
    except Exception as e:
        log_error(f"Database integrity check failed: {e}")
        return False

def main():
    """Run all tests"""
    log_header("🚀 Omni-Channel Inbox API Test Suite")
    log("Testing new inbox endpoints with SQLite database integration")
    log("=" * 80)
    
    # Setup test database
    if not setup_test_database():
        log_error("Database setup failed, aborting tests")
        return 1
    
    # Check API health
    if not test_health_check():
        log_error("API health check failed, aborting tests")
        return 1
    
    log("", 'reset')
    
    # Run tests
    tests = [
        ("Get Pending Leads", test_get_pending_leads),
        ("Approve Lead", test_approve_lead),
        ("Invalid Approval", test_invalid_approve),
        ("Inbox Stats", test_inbox_stats),
        ("Database Integrity", test_database_integrity)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        log(f"Running: {test_name}", 'reset')
        if test_func():
            passed += 1
        log("", 'reset')
    
    # Results
    log_header("🎯 Test Results")
    log("=" * 60)
    log(f"Passed: {passed}/{total}", 'reset')
    
    if passed == total:
        log_success("🎉 All tests passed! Inbox API is working correctly.")
        log("", 'reset')
        log("📱 API Endpoints Tested:", 'reset')
        log("✅ GET /api/inbox/pending - Retrieve pending leads with parsed follow-up notes", 'reset')
        log("✅ POST /api/inbox/approve/{id} - Approve lead and update status", 'reset')
        log("✅ GET /api/inbox/stats - Get inbox statistics", 'reset')
        log("✅ Error handling for invalid requests", 'reset')
        log("✅ JSON parsing for catatan_followup field", 'reset')
        log("✅ Database connection and query handling", 'reset')
        return 0
    else:
        log_error(f"❌ {total - passed} tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
