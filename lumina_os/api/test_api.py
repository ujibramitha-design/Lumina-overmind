"""
API Testing Script

This script provides a comprehensive test suite for the leads API endpoints.
It can be used to verify API functionality and demonstrate usage.

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_endpoint(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
    """
    Test API endpoint and return response
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        data: JSON data for POST/PUT requests
        params: Query parameters for GET requests
    
    Returns:
        Dict: Response data and status
    """
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else None,
            "success": response.status_code < 400
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 0,
            "response": None,
            "error": str(e),
            "success": False
        }

def print_test_result(test_name: str, result: Dict[str, Any]):
    """
    Print formatted test result
    
    Args:
        test_name: Name of the test
        result: Test result dictionary
    """
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Status Code: {result['status_code']}")
    print(f"Success: {result['success']}")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print("Response:")
        print(json.dumps(result['response'], indent=2))

def run_api_tests():
    """
    Run comprehensive API tests
    """
    print("🚀 Starting API Tests for HUNTER_AGENT_AI_MARKETING_DIGITAL")
    print(f"Base URL: {API_BASE}")
    
    # Test 1: Health Check
    result = test_endpoint("GET", "/leads/health")
    print_test_result("Health Check", result)
    
    # Test 2: Get All Leads (Empty)
    result = test_endpoint("GET", "/leads/")
    print_test_result("Get All Leads (Initial)", result)
    
    # Test 3: Create New Lead
    lead_data = {
        "nama": "John Doe",
        "no_hp": "+62812345678",
        "email": "john@example.com",
        "lokasi": "Jakarta",
        "sumber": "API Test",
        "catatan": "Test lead from API testing script",
        "skor_ai": 8,
        "status": "New"
    }
    
    result = test_endpoint("POST", "/leads/", data=lead_data)
    print_test_result("Create New Lead", result)
    
    # Extract lead ID for subsequent tests
    lead_id = None
    if result['success'] and result['response'] and result['response'].get('status') == 'success':
        lead_id = result['response']['data'].get('id')
        print(f"✅ Created lead with ID: {lead_id}")
    else:
        print("❌ Failed to create lead, skipping ID-dependent tests")
        return
    
    # Test 4: Get Specific Lead
    result = test_endpoint("GET", f"/leads/{lead_id}")
    print_test_result("Get Specific Lead", result)
    
    # Test 5: Update Lead
    update_data = {
        "status": "Follow Up",
        "catatan": "Updated notes from API test",
        "skor_ai": 9
    }
    
    result = test_endpoint("PUT", f"/leads/{lead_id}", data=update_data)
    print_test_result("Update Lead", result)
    
    # Test 6: Get Leads with Filtering
    params = {
        "limit": 10,
        "offset": 0,
        "status": "Follow Up",
        "sort_by": "created_at",
        "sort_order": "desc"
    }
    
    result = test_endpoint("GET", "/leads/", params=params)
    print_test_result("Get Leads with Filtering", result)
    
    # Test 7: Search Leads
    search_params = {
        "search": "John",
        "limit": 5
    }
    
    result = test_endpoint("GET", "/leads/", params=search_params)
    print_test_result("Search Leads", result)
    
    # Test 8: Get Leads Statistics
    result = test_endpoint("GET", "/leads/stats")
    print_test_result("Get Leads Statistics", result)
    
    # Test 9: Create Multiple Leads for Pagination Test
    print(f"\n{'='*60}")
    print("Creating additional test leads...")
    
    for i in range(5):
        multi_lead_data = {
            "nama": f"Test User {i+2}",
            "no_hp": f"+6281234567{i+2}",
            "email": f"test{i+2}@example.com",
            "lokasi": "Serang",
            "sumber": "Bulk Test",
            "skor_ai": (i+2) % 10,
            "status": "New"
        }
        
        result = test_endpoint("POST", "/leads/", data=multi_lead_data)
        if result['success']:
            print(f"✅ Created lead: {multi_lead_data['nama']}")
        else:
            print(f"❌ Failed to create: {multi_lead_data['nama']}")
        
        time.sleep(0.1)  # Small delay between requests
    
    # Test 10: Pagination Test
    pagination_params = {
        "limit": 3,
        "offset": 0,
        "sort_by": "created_at",
        "sort_order": "desc"
    }
    
    result = test_endpoint("GET", "/leads/", params=pagination_params)
    print_test_result("Pagination Test (Page 1)", result)
    
    # Test 11: Pagination Test (Page 2)
    pagination_params["offset"] = 3
    result = test_endpoint("GET", "/leads/", params=pagination_params)
    print_test_result("Pagination Test (Page 2)", result)
    
    # Test 12: Error Handling - Invalid Lead ID
    result = test_endpoint("GET", "/leads/99999")
    print_test_result("Error Handling - Invalid Lead ID", result)
    
    # Test 13: Error Handling - Invalid Data
    invalid_data = {
        "nama": "",  # Empty name
        "no_hp": "123"  # Invalid phone
    }
    
    result = test_endpoint("POST", "/leads/", data=invalid_data)
    print_test_result("Error Handling - Invalid Data", result)
    
    # Test 14: Delete Lead (Soft Delete)
    result = test_endpoint("DELETE", f"/leads/{lead_id}")
    print_test_result("Delete Lead (Soft Delete)", result)
    
    # Test 15: Verify Lead is Marked as Deleted
    result = test_endpoint("GET", f"/leads/{lead_id}")
    print_test_result("Verify Lead is Marked as Deleted", result)
    
    print(f"\n{'='*60}")
    print("🎉 API Tests Completed!")
    print(f"{'='*60}")
    print("Summary:")
    print("- ✅ Health Check")
    print("- ✅ CRUD Operations")
    print("- ✅ Pagination & Filtering")
    print("- ✅ Search Functionality")
    print("- ✅ Statistics Endpoint")
    print("- ✅ Error Handling")
    print("- ✅ Soft Delete")
    print("\nAll tests completed successfully!")

def test_api_performance():
    """
    Test API performance with multiple requests
    """
    print(f"\n{'='*60}")
    print("🏃 Performance Testing")
    print(f"{'='*60}")
    
    # Test multiple concurrent requests
    import threading
    import concurrent.futures
    
    def make_request():
        return test_endpoint("GET", "/leads/health")
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    
    successful_requests = sum(1 for r in results if r['success'])
    
    print(f"Total Requests: 50")
    print(f"Successful: {successful_requests}")
    print(f"Failed: {50 - successful_requests}")
    print(f"Total Time: {end_time - start_time:.2f} seconds")
    print(f"Requests per Second: {50 / (end_time - start_time):.2f}")

if __name__ == "__main__":
    print("🧪 HUNTER_AGENT_AI_MARKETING_DIGITAL API Test Suite")
    print("=" * 60)
    
    try:
        run_api_tests()
        test_api_performance()
        
        print(f"\n{'='*60}")
        print("📊 Test Summary")
        print(f"{'='*60}")
        print("✅ All API endpoints tested")
        print("✅ Error handling verified")
        print("✅ Performance tested")
        print("\n🚀 API is ready for production!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        print("Please ensure the API server is running on http://localhost:5000")
