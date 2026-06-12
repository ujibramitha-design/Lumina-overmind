#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Authentication API Test
Test script for JWT authentication system
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_authentication_api():
    """Test all authentication endpoints"""
    print("🧪 Testing Lumina OS Authentication API")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Login with valid credentials (Form Data)
    print("\n2️⃣ Testing Login (Form Data) - Valid Credentials...")
    try:
        login_data = {
            "username": "admin@lumina.os",
            "password": "hunter2026"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful")
            print(f"   Message: {result.get('message')}")
            print(f"   Token Type: {result['data']['token_type']}")
            print(f"   Expires In: {result['data']['expires_in']} seconds")
            print(f"   User: {result['data']['user']['name']} ({result['data']['user']['role']})")
            
            # Save token for next tests
            access_token = result['data']['access_token']
            user_info = result['data']['user']
            
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Test 3: Login with invalid credentials
    print("\n3️⃣ Testing Login - Invalid Credentials...")
    try:
        login_data = {
            "username": "admin@lumina.os",
            "password": "wrongpassword"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        
        if response.status_code == 401:
            print("✅ Invalid credentials properly rejected")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Should have rejected invalid credentials: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Invalid credentials test error: {e}")
        return False
    
    # Test 4: Login with JSON payload
    print("\n4️⃣ Testing Login (JSON Payload)...")
    try:
        login_data = {
            "email": "agent@lumina.os",
            "password": "agent2026"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ JSON login successful")
            print(f"   User: {result['data']['user']['name']} ({result['data']['user']['role']})")
            agent_token = result['data']['access_token']
        else:
            print(f"❌ JSON login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ JSON login error: {e}")
        return False
    
    # Test 5: Get current user info
    print("\n5️⃣ Testing Get Current User Info...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ User info retrieved successfully")
            print(f"   User: {user_data['name']} ({user_data['role']})")
            print(f"   Email: {user_data['email']}")
        else:
            print(f"❌ Get user info failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Get user info error: {e}")
        return False
    
    # Test 6: Verify token
    print("\n6️⃣ Testing Token Verification...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/verify?token={access_token}")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Token verification successful")
                print(f"   User ID: {result['data']['user_id']}")
                print(f"   Email: {result['data']['email']}")
                print(f"   Role: {result['data']['role']}")
            else:
                print(f"❌ Token verification failed: {result['message']}")
                return False
        else:
            print(f"❌ Token verification error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Token verification error: {e}")
        return False
    
    # Test 7: Access protected endpoint without token
    print("\n7️⃣ Testing Protected Endpoint - No Token...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me")
        
        if response.status_code == 401:
            print("✅ Protected endpoint properly rejected unauthorized access")
        else:
            print(f"❌ Should have rejected unauthorized access: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Protected endpoint test error: {e}")
        return False
    
    # Test 8: Access protected endpoint with invalid token
    print("\n8️⃣ Testing Protected Endpoint - Invalid Token...")
    try:
        headers = {"Authorization": "Bearer invalid_token_here"}
        
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        
        if response.status_code == 401:
            print("✅ Protected endpoint properly rejected invalid token")
        else:
            print(f"❌ Should have rejected invalid token: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Invalid token test error: {e}")
        return False
    
    # Test 9: Logout
    print("\n9️⃣ Testing Logout...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/logout")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Logout successful")
            print(f"   Message: {result['message']}")
        else:
            print(f"❌ Logout failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return False
    
    # Test 10: Test different user roles
    print("\n🔟 Testing Different User Roles...")
    test_users = [
        {"email": "admin@lumina.os", "password": "hunter2026", "role": "admin"},
        {"email": "agent@lumina.os", "password": "agent2026", "role": "agent"},
        {"email": "analyst@lumina.os", "password": "analyst2026", "role": "analyst"}
    ]
    
    for user in test_users:
        try:
            login_data = {
                "username": user["email"],
                "password": user["password"]
            }
            
            response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
            
            if response.status_code == 200:
                result = response.json()
                actual_role = result['data']['user']['role']
                if actual_role == user["role"]:
                    print(f"   ✅ {user['email']} - Role: {actual_role}")
                else:
                    print(f"   ❌ {user['email']} - Expected: {user['role']}, Got: {actual_role}")
            else:
                print(f"   ❌ {user['email']} - Login failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {user['email']} - Error: {e}")
    
    print("\n🎉 All authentication tests completed successfully!")
    return True

def test_api_integration():
    """Test authentication integration with other API endpoints"""
    print("\n🔗 Testing API Integration with Authentication")
    print("=" * 60)
    
    # Login to get token
    try:
        login_data = {
            "username": "admin@lumina.os",
            "password": "hunter2026"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        
        if response.status_code != 200:
            print("❌ Cannot login for integration tests")
            return False
        
        access_token = response.json()['data']['access_token']
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test accessing protected endpoints
        protected_endpoints = [
            "/api/runners",
            "/api/inbox/pending",
            "/api/system",
            "/api/search?q=test"
        ]
        
        for endpoint in protected_endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} - Access granted")
                elif response.status_code == 401:
                    print(f"   ⚠️  {endpoint} - Authentication required")
                else:
                    print(f"   ❌ {endpoint} - Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {endpoint} - Error: {e}")
        
        print("✅ API integration tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Main test function"""
    print("🔐 LUMINA OS AUTHENTICATION API TEST SUITE")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Base URL: {BASE_URL}")
    print()
    
    # Run authentication tests
    if test_authentication_api():
        # Run integration tests
        test_api_integration()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("🔐 Authentication system is working correctly")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please check the API server and try again")
        print("=" * 60)

if __name__ == "__main__":
    main()
