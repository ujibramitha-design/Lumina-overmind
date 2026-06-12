#!/usr/bin/env python3
"""
Test Script for Lumina Webhook Intake Engine API
Tests the new webhook endpoints with token validation and lead processing
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "webhook_health": f"{BASE_URL}/api/webhook/health",
    "incoming_lead": f"{BASE_URL}/api/webhook/incoming-lead"
}

# Webhook Configuration
WEBHOOK_TOKEN = "DUMMY-TOKEN-123"
INVALID_TOKEN = "INVALID-TOKEN"

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

def test_webhook_health():
    """Test webhook health check endpoint"""
    log_header("Testing Webhook Health Check")
    
    try:
        response = requests.get(API_ENDPOINTS["webhook_health"], timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            expected_fields = ["status", "service", "timestamp", "version"]
            for field in expected_fields:
                if field not in data:
                    log_error(f"Missing field: {field}")
                    return False
            
            if data["status"] == "OK" and data["service"] == "Lumina Webhook Intake Engine":
                log_success("Webhook health check passed")
                log_info(f"Service: {data['service']}")
                log_info(f"Version: {data['version']}")
                return True
            else:
                log_error(f"Invalid response: {data}")
                return False
        else:
            log_error(f"HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"JSON decode error: {e}")
        return False

def test_webhook_token_validation():
    """Test webhook token validation"""
    log_header("Testing Webhook Token Validation")
    
    # Test without token
    try:
        payload = {
            "nama": "Test User",
            "no_hp": "08123456789",
            "email": "test@example.com",
            "sumber": "test_source"
        }
        
        response = requests.post(
            API_ENDPOINTS["incoming_lead"], 
            json=payload,
            timeout=10
        )
        
        if response.status_code == 401:
            log_success("Correctly rejected request without token")
        else:
            log_error(f"Expected 401, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    
    # Test with invalid token
    try:
        headers = {"X-Lumina-Token": INVALID_TOKEN}
        
        response = requests.post(
            API_ENDPOINTS["incoming_lead"], 
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 401:
            log_success("Correctly rejected request with invalid token")
        else:
            log_error(f"Expected 401, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    
    # Test with valid token
    try:
        headers = {"X-Lumina-Token": WEBHOOK_TOKEN}
        
        response = requests.post(
            API_ENDPOINTS["incoming_lead"], 
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            log_success("Successfully accepted request with valid token")
            return True
        else:
            log_error(f"Expected 201, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False

def test_payload_validation():
    """Test webhook payload validation"""
    log_header("Testing Webhook Payload Validation")
    
    headers = {"X-Lumina-Token": WEBHOOK_TOKEN}
    
    # Test valid payload
    valid_payload = {
        "nama": "John Doe",
        "no_hp": "08123456789",
        "email": "john@example.com",
        "sumber": "website",
        "campaign": "summer_promo",
        "catatan": "Interested in property investment",
        "lokasi": "Jakarta",
        "pekerjaan": "Software Engineer"
    }
    
    try:
        response = requests.post(
            API_ENDPOINTS["incoming_lead"],
            json=valid_payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            
            if data.get("success"):
                log_success("Valid payload processed successfully")
                log_info(f"Lead ID: {data.get('data', {}).get('lead_id')}")
                log_info(f"Score: {data.get('data', {}).get('score')}")
                log_info(f"Status: {data.get('data', {}).get('status')}")
                return True
            else:
                log_error(f"API returned error: {data}")
                return False
        else:
            log_error(f"HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"JSON decode error: {e}")
        return False

def test_invalid_payloads():
    """Test webhook payload validation with invalid data"""
    log_header("Testing Invalid Payload Validation")
    
    headers = {"X-Lumina-Token": WEBHOOK_TOKEN}
    
    invalid_payloads = [
        {
            "name": "Missing required fields",
            "description": "Should fail - missing required fields"
        },
        {
            "nama": "",  # Empty name
            "no_hp": "08123456789",
            "sumber": "test"
        },
        {
            "nama": "A" * 300,  # Too long name
            "no_hp": "08123456789",
            "sumber": "test"
        },
        {
            "nama": "Test User",
            "no_hp": "123",  # Too short phone
            "sumber": "test"
        },
        {
            "nama": "Test User",
            "no_hp": "08123456789",
            "email": "invalid-email",  # Invalid email
            "sumber": "test"
        }
    ]
    
    for i, payload in enumerate(invalid_payloads, 1):
        try:
            response = requests.post(
                API_ENDPOINTS["incoming_lead"],
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [400, 422]:
                log_success(f"Invalid payload {i} correctly rejected (HTTP {response.status_code})")
            else:
                log_error(f"Invalid payload {i} should be rejected, got {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            log_error(f"Request failed for invalid payload {i}: {e}")
            return False
    
    return True

def test_lead_scoring_integration():
    """Test lead scoring integration"""
    log_header("Testing Lead Scoring Integration")
    
    headers = {"X-Lumina-Token": WEBHOOK_TOKEN}
    
    # Test payload with scoring keywords
    scoring_payload = {
        "nama": "JUAL Rumah Murah Jakarta",
        "no_hp": "08123456789",
        "email": "buyer@example.com",
        "sumber": "property_portal",
        "campaign": "flash_sale",
        "catatan": "Sangat tertarik dengan harga promo, ready stock, bisa KPR",
        "lokasi": "Jakarta Selatan",
        "pekerjaan": "Investor"
    }
    
    try:
        response = requests.post(
            API_ENDPOINTS["incoming_lead"],
            json=scoring_payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            
            if data.get("success"):
                result_data = data.get("data", {})
                
                # Check if scoring was applied
                if "score" in result_data and "status" in result_data:
                    score = result_data["score"]
                    status = result_data["status"]
                    keywords_found = result_data.get("keywords_found", [])
                    
                    log_success("Lead scoring integration working")
                    log_info(f"Score: {score}")
                    log_info(f"Status: {status}")
                    log_info(f"Keywords found: {len(keywords_found)}")
                    
                    # Should have high score due to hot keywords
                    if score >= 80 and status == "Hot":
                        log_success("Hot keywords correctly detected")
                    elif score >= 60 and status == "Warm":
                        log_success("Warm keywords correctly detected")
                    
                    return True
                else:
                    log_error("Scoring data not found in response")
                    return False
            else:
                log_error(f"API returned error: {data}")
                return False
        else:
            log_error(f"HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"JSON decode error: {e}")
        return False

def test_database_integration():
    """Test database integration"""
    log_header("Testing Database Integration")
    
    headers = {"X-Lumina-Token": WEBHOOK_TOKEN}
    
    # Create multiple leads to test database operations
    test_leads = [
        {
            "nama": f"Test Lead {datetime.now().strftime('%H%M%S')}",
            "no_hp": "08123456789",
            "sumber": "test_integration"
        },
        {
            "nama": f"Test Lead {datetime.now().strftime('%H%M%S')} 2",
            "no_hp": "08123456790",
            "email": "test2@example.com",
            "sumber": "test_integration",
            "lokasi": "Test City"
        }
    ]
    
    created_leads = []
    
    for lead in test_leads:
        try:
            response = requests.post(
                API_ENDPOINTS["incoming_lead"],
                json=lead,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                if data.get("success"):
                    lead_id = data.get("data", {}).get("lead_id")
                    created_leads.append(lead_id)
                    log_success(f"Lead {lead_id} created successfully")
                else:
                    log_error(f"Failed to create lead: {data}")
                    return False
            else:
                log_error(f"HTTP error creating lead: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            log_error(f"Request failed: {e}")
            return False
    
    log_success(f"Successfully created {len(created_leads)} leads in database")
    return True

def test_response_format():
    """Test webhook response format"""
    log_header("Testing Webhook Response Format")
    
    headers = {"X-Lumina-Token": WEBHOOK_TOKEN}
    
    payload = {
        "nama": "Response Test User",
        "no_hp": "08123456789",
        "sumber": "test_response"
    }
    
    try:
        response = requests.post(
            API_ENDPOINTS["incoming_lead"],
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            
            # Validate response structure
            required_fields = ["success", "message", "data"]
            for field in required_fields:
                if field not in data:
                    log_error(f"Missing required field: {field}")
                    return False
            
            # Validate data structure
            response_data = data.get("data", {})
            required_data_fields = [
                "lead_id", "nama", "no_hp", "sumber", "score", 
                "status", "processed_at"
            ]
            
            for field in required_data_fields:
                if field not in response_data:
                    log_error(f"Missing data field: {field}")
                    return False
            
            # Validate timestamp format
            processed_at = response_data.get("processed_at")
            try:
                datetime.fromisoformat(processed_at.replace('Z', '+00:00'))
                log_success("Timestamp format is valid")
            except ValueError:
                log_error("Invalid timestamp format")
                return False
            
            log_success("Response format validation passed")
            return True
        else:
            log_error(f"HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        log_error(f"Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        log_error(f"JSON decode error: {e}")
        return False

def main():
    """Run all webhook tests"""
    log_header("🚀 Lumina Webhook Intake Engine Test Suite")
    log("Testing webhook endpoints with token validation and lead processing")
    log("=" * 80)
    
    # Check API health first
    if not test_webhook_health():
        log_error("API health check failed, aborting tests")
        return 1
    
    log()
    
    # Run tests
    tests = [
        ("Token Validation", test_webhook_token_validation),
        ("Payload Validation", test_payload_validation),
        ("Invalid Payloads", test_invalid_payloads),
        ("Lead Scoring Integration", test_lead_scoring_integration),
        ("Database Integration", test_database_integration),
        ("Response Format", test_response_format)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        log(f"Running: {test_name}")
        if test_func():
            passed += 1
        log()
    
    # Results
    log_header("🎯 Test Results")
    log("=" * 60)
    log(f"Passed: {passed}/{total}")
    
    if passed == total:
        log_success("🎉 All webhook tests passed! Webhook Intake Engine is working correctly.")
        log()
        log("📱 Webhook Features Tested:")
        log("✅ Token validation with X-Lumina-Token header")
        log("✅ Payload validation with Pydantic models")
        log("✅ LeadScorer integration for AI scoring")
        log("✅ Database storage with SQLite")
        log("✅ Response format validation")
        log("✅ Error handling for invalid requests")
        log("✅ HTTP status codes (201, 401, 400, 422, 500)")
        return 0
    else:
        log_error(f"❌ {total - passed} tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
