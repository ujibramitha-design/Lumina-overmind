"""
Test Suite for API Endpoints Security and Functionality
Comprehensive testing of all API endpoints with security validation
"""

import pytest
import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, List, Any
import random
import string

class TestAPIEndpoints:
    """Comprehensive API endpoint testing"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_data = {}
        self.auth_token = None
        
    def setup_test_data(self):
        """Setup test data for API testing"""
        self.test_data = {
            'projects': [
                {
                    'namaProyek': 'Test Project KOMERSIL',
                    'tipeProyek': 'KOMERSIL',
                    'lokasi': 'Test Location',
                    'hargaStart': 500000000,
                    'targetMarket': 'Test Market'
                },
                {
                    'namaProyek': 'Test Project SUBSIDI',
                    'tipeProyek': 'SUBSIDI',
                    'lokasi': 'Test Location 2',
                    'hargaStart': 150000000,
                    'targetMarket': 'Test Market 2'
                }
            ],
            'leads': [
                {
                    'business_name': 'Test Lead 1',
                    'contact': '+62812345678',
                    'project_id': 'test_project_1',
                    'score': 8,
                    'source': 'test'
                },
                {
                    'business_name': 'Test Lead 2',
                    'contact': '+62887654321',
                    'project_id': 'test_project_2',
                    'score': 6,
                    'source': 'test'
                }
            ]
        }
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("🧪 Testing Health Endpoint...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'passed',
                    'response_time': response.elapsed.total_seconds(),
                    'data': data
                }
            else:
                return {
                    'status': 'failed',
                    'status_code': response.status_code,
                    'response': response.text
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def test_projects_endpoint(self):
        """Test projects CRUD operations"""
        print("🧪 Testing Projects Endpoint...")
        
        results = {}
        
        # Test GET projects
        try:
            response = requests.get(f"{self.base_url}/api/projects", timeout=10)
            results['get_projects'] = {
                'status': 'passed' if response.status_code == 200 else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            results['get_projects'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test POST project
        try:
            project_data = self.test_data['projects'][0]
            response = requests.post(
                f"{self.base_url}/api/projects",
                json=project_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            results['create_project'] = {
                'status': 'passed' if response.status_code in [200, 201] else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            if response.status_code in [200, 201]:
                created_project = response.json()
                project_id = created_project.get('id')
                
                # Test PUT project
                update_data = {'namaProyek': 'Updated Test Project'}
                response = requests.put(
                    f"{self.base_url}/api/projects/{project_id}",
                    json=update_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                results['update_project'] = {
                    'status': 'passed' if response.status_code == 200 else 'failed',
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds()
                }
                
                # Test DELETE project
                response = requests.delete(
                    f"{self.base_url}/api/projects/{project_id}",
                    timeout=10
                )
                results['delete_project'] = {
                    'status': 'passed' if response.status_code == 200 else 'failed',
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds()
                }
                
        except Exception as e:
            results['create_project'] = {
                'status': 'error',
                'error': str(e)
            }
        
        return results
    
    def test_leads_endpoint(self):
        """Test leads CRUD operations with project isolation"""
        print("🧪 Testing Leads Endpoint...")
        
        results = {}
        
        # Test GET leads
        try:
            response = requests.get(f"{self.base_url}/api/leads", timeout=10)
            results['get_leads'] = {
                'status': 'passed' if response.status_code == 200 else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            results['get_leads'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test POST lead with project isolation
        try:
            lead_data = self.test_data['leads'][0]
            response = requests.post(
                f"{self.base_url}/api/leads",
                json=lead_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            results['create_lead'] = {
                'status': 'passed' if response.status_code in [200, 201] else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            if response.status_code in [200, 201]:
                created_lead = response.json()
                lead_id = created_lead.get('id')
                
                # Test duplicate prevention
                response = requests.post(
                    f"{self.base_url}/api/leads",
                    json=lead_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                results['duplicate_prevention'] = {
                    'status': 'passed' if response.status_code == 409 else 'failed',
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'message': 'Duplicate prevention working' if response.status_code == 409 else 'Duplicate prevention failed'
                }
                
                # Test GET lead by project
                response = requests.get(
                    f"{self.base_url}/api/leads?project_id={lead_data['project_id']}",
                    timeout=10
                )
                results['get_leads_by_project'] = {
                    'status': 'passed' if response.status_code == 200 else 'failed',
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds()
                }
                
        except Exception as e:
            results['create_lead'] = {
                'status': 'error',
                'error': str(e)
            }
        
        return results
    
    def test_jarvis_endpoint(self):
        """Test J.A.R.V.I.S. AI assistant endpoint"""
        print("🧪 Testing J.A.R.V.I.S. Endpoint...")
        
        results = {}
        
        # Test GET jarvis status
        try:
            response = requests.get(f"{self.base_url}/api/jarvis/status", timeout=10)
            results['get_status'] = {
                'status': 'passed' if response.status_code == 200 else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            results['get_status'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test POST jarvis chat
        try:
            chat_data = {
                'message': 'Hello J.A.R.V.I.S., what can you do?',
                'user_id': 'test_user'
            }
            response = requests.post(
                f"{self.base_url}/api/jarvis/chat",
                json=chat_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            results['chat'] = {
                'status': 'passed' if response.status_code == 200 else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            results['chat'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test POST jarvis toggle
        try:
            response = requests.post(
                f"{self.base_url}/api/jarvis/toggle",
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            results['toggle'] = {
                'status': 'passed' if response.status_code == 200 else 'failed',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            results['toggle'] = {
                'status': 'error',
                'error': str(e)
            }
        
        return results
    
    def test_security_headers(self):
        """Test security headers on all endpoints"""
        print("🧪 Testing Security Headers...")
        
        endpoints_to_test = [
            '/health',
            '/api/projects',
            '/api/leads',
            '/api/jarvis/status'
        ]
        
        results = {}
        
        for endpoint in endpoints_to_test:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                
                security_headers = {
                    'x_content_type_options': response.headers.get('X-Content-Type-Options'),
                    'x_frame_options': response.headers.get('X-Frame-Options'),
                    'x_xss_protection': response.headers.get('X-XSS-Protection'),
                    'strict_transport_security': response.headers.get('Strict-Transport-Security'),
                    'content_security_policy': response.headers.get('Content-Security-Policy')
                }
                
                results[endpoint] = {
                    'status': 'passed' if response.status_code == 200 else 'failed',
                    'status_code': response.status_code,
                    'security_headers': security_headers,
                    'has_cors': 'Access-Control-Allow-Origin' in response.headers
                }
                
            except Exception as e:
                results[endpoint] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def test_rate_limiting(self):
        """Test rate limiting on API endpoints"""
        print("🧪 Testing Rate Limiting...")
        
        results = {}
        
        # Test rapid requests to /health endpoint
        rapid_requests = []
        start_time = datetime.now()
        
        for i in range(50):  # 50 rapid requests
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                rapid_requests.append({
                    'request_id': i,
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds()
                })
            except Exception as e:
                rapid_requests.append({
                    'request_id': i,
                    'error': str(e)
                })
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Analyze results
        successful_requests = [r for r in rapid_requests if r.get('status_code') == 200]
        rate_limited_requests = [r for r in rapid_requests if r.get('status_code') == 429]
        
        results['rate_limiting_test'] = {
            'total_requests': len(rapid_requests),
            'successful_requests': len(successful_requests),
            'rate_limited_requests': len(rate_limited_requests),
            'total_time': total_time,
            'requests_per_second': len(rapid_requests) / total_time,
            'rate_limiting_active': len(rate_limited_requests) > 0
        }
        
        return results
    
    def test_input_validation(self):
        """Test input validation and sanitization"""
        print("🧪 Testing Input Validation...")
        
        results = {}
        
        # Test malicious input on leads endpoint
        malicious_inputs = [
            {"business_name": "<script>alert('xss')</script>", "contact": "+62812345678", "project_id": "test", "source": "test"},
            {"business_name": "'; DROP TABLE leads; --", "contact": "+62812345678", "project_id": "test", "source": "test"},
            {"business_name": "A" * 10000, "contact": "+62812345678", "project_id": "test", "source": "test"},  # Very long input
            {"business_name": "Test", "contact": "invalid_phone", "project_id": "test", "source": "test"},  # Invalid phone
        ]
        
        for i, malicious_input in enumerate(malicious_inputs):
            try:
                response = requests.post(
                    f"{self.base_url}/api/leads",
                    json=malicious_input,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                results[f'malicious_input_{i}'] = {
                    'status': 'passed' if response.status_code == 422 else 'failed',
                    'status_code': response.status_code,
                    'should_be_rejected': True,
                    'actually_rejected': response.status_code == 422,
                    'validation_working': response.status_code == 422
                }
                
            except Exception as e:
                results[f'malicious_input_{i}'] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def test_error_handling(self):
        """Test error handling and graceful failures"""
        print("🧪 Testing Error Handling...")
        
        results = {}
        
        # Test 404 errors
        try:
            response = requests.get(f"{self.base_url}/api/nonexistent", timeout=10)
            results['404_error'] = {
                'status': 'passed' if response.status_code == 404 else 'failed',
                'status_code': response.status_code,
                'has_error_response': 'error' in response.text.lower()
            }
        except Exception as e:
            results['404_error'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test 405 method not allowed
        try:
            response = requests.delete(f"{self.base_url}/api/projects", timeout=10)
            results['405_error'] = {
                'status': 'passed' if response.status_code == 405 else 'failed',
                'status_code': response.status_code,
                'has_error_response': 'error' in response.text.lower()
            }
        except Exception as e:
            results['405_error'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test 422 validation error
        try:
            response = requests.post(
                f"{self.base_url}/api/leads",
                json={},  # Empty data should fail validation
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            results['422_error'] = {
                'status': 'passed' if response.status_code == 422 else 'failed',
                'status_code': response.status_code,
                'has_validation_error': 'validation' in response.text.lower()
            }
        except Exception as e:
            results['422_error'] = {
                'status': 'error',
                'error': str(e)
            }
        
        return results
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Endpoint Test Suite...\n")
        
        # Setup test data
        self.setup_test_data()
        
        # Run tests
        test_results = {}
        
        try:
            test_results['health'] = self.test_health_endpoint()
            test_results['projects'] = self.test_projects_endpoint()
            test_results['leads'] = self.test_leads_endpoint()
            test_results['jarvis'] = self.test_jarvis_endpoint()
            test_results['security_headers'] = self.test_security_headers()
            test_results['rate_limiting'] = self.test_rate_limiting()
            test_results['input_validation'] = self.test_input_validation()
            test_results['error_handling'] = self.test_error_handling()
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
        
        # Generate report
        self._generate_test_report(test_results)
        
        return test_results
    
    def _generate_test_report(self, test_results: Dict[str, Any]):
        """Generate comprehensive test report"""
        report = f"""
# 🧪 API ENDPOINT TEST REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 TEST RESULTS SUMMARY

### 1. Health Endpoint
- **Status**: {test_results.get('health', {}).get('status', 'NOT_TESTED').upper()}
- **Response Time**: {test_results.get('health', {}).get('response_time', 'N/A')}s

### 2. Projects Endpoint
- **GET Projects**: {test_results.get('projects', {}).get('get_projects', {}).get('status', 'NOT_TESTED').upper()}
- **Create Project**: {test_results.get('projects', {}).get('create_project', {}).get('status', 'NOT_TESTED').upper()}
- **Update Project**: {test_results.get('projects', {}).get('update_project', {}).get('status', 'NOT_TESTED').upper()}
- **Delete Project**: {test_results.get('projects', {}).get('delete_project', {}).get('status', 'NOT_TESTED').upper()}

### 3. Leads Endpoint
- **GET Leads**: {test_results.get('leads', {}).get('get_leads', {}).get('status', 'NOT_TESTED').upper()}
- **Create Lead**: {test_results.get('leads', {}).get('create_lead', {}).get('status', 'NOT_TESTED').upper()}
- **Duplicate Prevention**: {test_results.get('leads', {}).get('duplicate_prevention', {}).get('status', 'NOT_TESTED').upper()}
- **Get Leads by Project**: {test_results.get('leads', {}).get('get_leads_by_project', {}).get('status', 'NOT_TESTED').upper()}

### 4. J.A.R.V.I.S. Endpoint
- **GET Status**: {test_results.get('jarvis', {}).get('get_status', {}).get('status', 'NOT_TESTED').upper()}
- **Chat**: {test_results.get('jarvis', {}).get('chat', {}).get('status', 'NOT_TESTED').upper()}
- **Toggle**: {test_results.get('jarvis', {}).get('toggle', {}).get('status', 'NOT_TESTED').upper()}

### 5. Security Headers
- **Endpoints Tested**: {len(test_results.get('security_headers', {}))}
- **CORS Enabled**: {len([e for e in test_results.get('security_headers', {}).values() if e.get('has_cors')])}
- **Security Headers Present**: {len([e for e in test_results.get('security_headers', {}).values() if any(e.get('security_headers', {}).values())])}

### 6. Rate Limiting
- **Total Requests**: {test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('total_requests', 0)}
- **Successful**: {test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('successful_requests', 0)}
- **Rate Limited**: {test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('rate_limited_requests', 0)}
- **Rate Limiting Active**: {test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('rate_limiting_active', False)}

### 7. Input Validation
- **Malicious Inputs Tested**: {len(test_results.get('input_validation', {}))}
- **Validation Working**: {len([v for v in test_results.get('input_validation', {}).values() if v.get('validation_working')])}
- **All Rejected**: {len([v for v in test_results.get('input_validation', {}).values() if v.get('actually_rejected')])}

### 8. Error Handling
- **404 Error**: {test_results.get('error_handling', {}).get('404_error', {}).get('status', 'NOT_TESTED').upper()}
- **405 Error**: {test_results.get('error_handling', {}).get('405_error', {}).get('status', 'NOT_TESTED').upper()}
- **422 Error**: {test_results.get('error_handling', {}).get('422_error', {}).get('status', 'NOT_TESTED').upper()}

## 🔍 SECURITY ASSESSMENT

### Security Score
{self._calculate_security_score(test_results)}/10

### Critical Issues
{self._identify_critical_issues(test_results)}

### Recommendations
{self._generate_recommendations(test_results)}
"""
        
        # Save report
        with open('test_api_endpoints_report.md', 'w') as f:
            f.write(report)
        
        print(report)
        print(f"\n📄 Detailed report saved to: test_api_endpoints_report.md")
    
    def _calculate_security_score(self, test_results: Dict[str, Any]) -> int:
        """Calculate security score (0-10)"""
        score = 10
        
        # Deduct points for security issues
        if not test_results.get('input_validation', {}).get('validation_working', True):
            score -= 3
        
        if not test_results.get('error_handling', {}).get('404_error', {}).get('status') == 'passed':
            score -= 2
        
        if not test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('rate_limiting_active', False):
            score -= 2
        
        # Check security headers
        security_headers = test_results.get('security_headers', {})
        if not any(h.get('has_cors') for h in security_headers.values()):
            score -= 1
        
        return max(0, score)
    
    def _identify_critical_issues(self, test_results: Dict[str, Any]) -> str:
        """Identify critical security issues"""
        issues = []
        
        if not test_results.get('input_validation', {}).get('validation_working', True):
            issues.append("❌ Input validation not working - XSS/SQL injection possible")
        
        if not test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('rate_limiting_active', False):
            issues.append("❌ No rate limiting - DoS attack possible")
        
        if not test_results.get('error_handling', {}).get('404_error', {}).get('status') == 'passed':
            issues.append("❌ 404 error handling not working")
        
        if not test_results.get('leads', {}).get('duplicate_prevention', {}).get('status') == 'passed':
            issues.append("❌ Duplicate prevention not working")
        
        return '\n'.join(issues) if issues else "✅ No critical issues found"
    
    def _generate_recommendations(self, test_results: Dict[str, Any]) -> str:
        """Generate security recommendations"""
        recommendations = []
        
        if not test_results.get('input_validation', {}).get('validation_working', True):
            recommendations.append("• Implement proper input validation and sanitization")
        
        if not test_results.get('rate_limiting', {}).get('rate_limiting_test', {}).get('rate_limiting_active', False):
            recommendations.append("• Implement rate limiting on all API endpoints")
        
        if not any(h.get('has_cors') for h in test_results.get('security_headers', {}).values()):
            recommendations.append("• Configure CORS headers properly")
        
        if not test_results.get('error_handling', {}).get('422_error', {}).get('status') == 'passed':
            recommendations.append("• Implement proper validation error responses")
        
        return '\n'.join(recommendations) if recommendations else "✅ All security measures are properly implemented"

# Run tests if executed directly
if __name__ == "__main__":
    test_suite = TestAPIEndpoints()
    results = test_suite.run_all_tests()
    
    # Calculate overall score
    security_score = test_suite._calculate_security_score(results)
    
    print(f"\n🎯 Overall Security Score: {security_score}/10")
    exit(0 if security_score >= 7 else 1)
