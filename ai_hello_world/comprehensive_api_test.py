#!/usr/bin/env python3

import requests
import json
import datetime
from typing import Dict, Any, Optional

# Base URL for the remote API
BASE_URL = "https://7v38qrq1-8000.asse.devtunnels.ms"

class APITestLogger:
    def __init__(self):
        self.test_results = []
        self.test_count = 0
    
    def log_test(self, test_name: str, method: str, endpoint: str, 
                 request_headers: Dict = None, request_payload: Any = None,
                 response_status: int = None, response_headers: Dict = None,
                 response_body: Any = None, error: str = None):
        
        self.test_count += 1
        
        test_result = {
            "test_number": self.test_count,
            "test_name": test_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "request": {
                "method": method,
                "endpoint": endpoint,
                "full_url": f"{BASE_URL}{endpoint}",
                "headers": request_headers or {},
                "payload": request_payload
            },
            "response": {
                "status_code": response_status,
                "headers": dict(response_headers) if response_headers else {},
                "body": response_body
            },
            "error": error,
            "success": error is None and response_status and 200 <= response_status < 300
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def generate_report(self):
        report = {
            "test_session": {
                "timestamp": datetime.datetime.now().isoformat(),
                "base_url": BASE_URL,
                "total_tests": self.test_count,
                "passed_tests": sum(1 for test in self.test_results if test["success"]),
                "failed_tests": sum(1 for test in self.test_results if not test["success"])
            },
            "tests": self.test_results
        }
        return report

def make_request(logger: APITestLogger, test_name: str, method: str, endpoint: str, 
                 headers: Dict = None, payload: Any = None):
    """Make HTTP request and log all details"""
    
    default_headers = {
        'User-Agent': 'API-Test-Client/1.0',
        'Accept': 'application/json'
    }
    
    if headers:
        default_headers.update(headers)
    
    full_url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(full_url, headers=default_headers, timeout=10)
        elif method.upper() == 'POST':
            if payload:
                default_headers['Content-Type'] = 'application/json'
                response = requests.post(full_url, json=payload, headers=default_headers, timeout=10)
            else:
                response = requests.post(full_url, headers=default_headers, timeout=10)
        elif method.upper() == 'PUT':
            if payload:
                default_headers['Content-Type'] = 'application/json'
                response = requests.put(full_url, json=payload, headers=default_headers, timeout=10)
            else:
                response = requests.put(full_url, headers=default_headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(full_url, headers=default_headers, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Try to parse JSON response
        try:
            response_body = response.json()
        except:
            response_body = response.text
        
        return logger.log_test(
            test_name=test_name,
            method=method.upper(),
            endpoint=endpoint,
            request_headers=default_headers,
            request_payload=payload,
            response_status=response.status_code,
            response_headers=response.headers,
            response_body=response_body
        )
        
    except Exception as e:
        return logger.log_test(
            test_name=test_name,
            method=method.upper(),
            endpoint=endpoint,
            request_headers=default_headers,
            request_payload=payload,
            error=str(e)
        )

def run_comprehensive_tests():
    """Run all API tests with comprehensive logging"""
    
    logger = APITestLogger()
    
    print("=== Comprehensive API Testing Suite ===")
    print(f"Testing against: {BASE_URL}")
    print(f"Start time: {datetime.datetime.now().isoformat()}")
    print("=" * 60)
    
    # Test 1: Health Check API
    print("1. Testing Health Check API...")
    make_request(logger, "Health Check", "GET", "/api/health/")
    
    # Test 2: Hello/Index API
    print("2. Testing Hello/Index API...")
    make_request(logger, "Hello Index", "GET", "/")
    
    # Test 3: Auth Health Check
    print("3. Testing Auth Health Check API...")
    make_request(logger, "Auth Health Check", "GET", "/api/v1/auth/health")
    
    # Test 4: Login API with credentials
    print("4. Testing Login API...")
    login_payload = {
        "username": "test_user",
        "password": "test_password", 
        "language": "en",
        "remember_me": False
    }
    make_request(logger, "User Login", "POST", "/api/v1/auth/login", payload=login_payload)
    
    # Test 5: Login API with different credentials
    print("5. Testing Login API with admin credentials...")
    admin_login_payload = {
        "username": "admin",
        "password": "admin123", 
        "language": "vi",
        "remember_me": True
    }
    make_request(logger, "Admin Login", "POST", "/api/v1/auth/login", payload=admin_login_payload)
    
    # Test 6: Session Validation (without token)
    print("6. Testing Session Validation...")
    make_request(logger, "Session Validation", "GET", "/api/v1/auth/validate")
    
    # Test 7: Token Refresh (without token)
    print("7. Testing Token Refresh...")
    refresh_payload = {"refresh_token": "dummy_refresh_token"}
    make_request(logger, "Token Refresh", "POST", "/api/v1/auth/refresh", payload=refresh_payload)
    
    # Test 8: Logout
    print("8. Testing Logout...")
    logout_payload = {"session_id": "dummy_session"}
    make_request(logger, "User Logout", "POST", "/api/v1/auth/logout", payload=logout_payload)
    
    # Test 9: Idle Resources List
    print("9. Testing Idle Resources List...")
    make_request(logger, "Idle Resources List", "GET", "/api/v1/idle-resources")
    
    # Test 10: Idle Resources with pagination
    print("10. Testing Idle Resources with Pagination...")
    make_request(logger, "Idle Resources Paginated", "GET", "/api/v1/idle-resources?page=1&page_size=5")
    
    # Test 11: Create Idle Resource
    print("11. Testing Create Idle Resource...")
    resource_payload = {
        "employee_name": "John Doe",
        "employee_id": "EMP001",
        "department_name": "IT",
        "department_id": "DEPT001",
        "job_rank": "Senior Developer",
        "skills": ["Python", "Django", "React"],
        "experience_years": 5,
        "idle_from": "2025-07-27",
        "idle_to": "2025-08-27",
        "idle_type": "Between Projects",
        "hourly_rate": 50.0,
        "availability_status": "Available"
    }
    make_request(logger, "Create Idle Resource", "POST", "/api/v1/idle-resources", payload=resource_payload)
    
    # Test 12: Master Data
    print("12. Testing Master Data...")
    make_request(logger, "Master Data", "GET", "/api/v1/master-data")
    
    # Test 13: Master Data with filters
    print("13. Testing Master Data with Filters...")
    make_request(logger, "Master Data Filtered", "GET", "/api/v1/master-data?include_inactive=true")
    
    # Test 14: Resource Detail (with dummy ID)
    print("14. Testing Resource Detail...")
    make_request(logger, "Resource Detail", "GET", "/api/v1/idle-resources/123e4567-e89b-12d3-a456-426614174000")
    
    # Test 15: Update Resource (with dummy ID)
    print("15. Testing Update Resource...")
    update_payload = {
        "employee_name": "Jane Doe Updated",
        "availability_status": "Busy"
    }
    make_request(logger, "Update Resource", "PUT", "/api/v1/idle-resources/123e4567-e89b-12d3-a456-426614174000", payload=update_payload)
    
    # Test 16: Delete Resource (with dummy ID)
    print("16. Testing Delete Resource...")
    make_request(logger, "Delete Resource", "DELETE", "/api/v1/idle-resources/123e4567-e89b-12d3-a456-426614174000")
    
    print("\n" + "=" * 60)
    print("Tests completed. Generating report...")
    
    return logger.generate_report()

def save_report_to_file(report: Dict[str, Any], filename: str = "api_test_report.json"):
    """Save the test report to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Also create a human-readable version
    readable_filename = filename.replace('.json', '_readable.txt')
    with open(readable_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("COMPREHENSIVE API TEST REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        session = report['test_session']
        f.write(f"Test Session Information:\n")
        f.write(f"  Timestamp: {session['timestamp']}\n")
        f.write(f"  Base URL: {session['base_url']}\n")
        f.write(f"  Total Tests: {session['total_tests']}\n")
        f.write(f"  Passed: {session['passed_tests']}\n")
        f.write(f"  Failed: {session['failed_tests']}\n")
        f.write(f"  Success Rate: {(session['passed_tests']/session['total_tests']*100):.1f}%\n\n")
        
        for test in report['tests']:
            f.write("-" * 80 + "\n")
            f.write(f"TEST #{test['test_number']}: {test['test_name']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Timestamp: {test['timestamp']}\n")
            f.write(f"Status: {'✅ PASS' if test['success'] else '❌ FAIL'}\n\n")
            
            # Request details
            req = test['request']
            f.write("REQUEST:\n")
            f.write(f"  Method: {req['method']}\n")
            f.write(f"  Endpoint: {req['endpoint']}\n")
            f.write(f"  Full URL: {req['full_url']}\n")
            f.write(f"  Headers:\n")
            for header, value in req['headers'].items():
                f.write(f"    {header}: {value}\n")
            if req['payload']:
                f.write(f"  Payload:\n")
                f.write(f"    {json.dumps(req['payload'], indent=4)}\n")
            f.write("\n")
            
            # Response details
            resp = test['response']
            f.write("RESPONSE:\n")
            if resp['status_code']:
                f.write(f"  Status Code: {resp['status_code']}\n")
                f.write(f"  Headers:\n")
                for header, value in resp['headers'].items():
                    f.write(f"    {header}: {value}\n")
                f.write(f"  Body:\n")
                if isinstance(resp['body'], dict) or isinstance(resp['body'], list):
                    f.write(f"    {json.dumps(resp['body'], indent=4, ensure_ascii=False)}\n")
                else:
                    f.write(f"    {resp['body']}\n")
            
            if test['error']:
                f.write(f"ERROR: {test['error']}\n")
            
            f.write("\n\n")
    
    return filename, readable_filename

if __name__ == "__main__":
    # Run comprehensive tests
    report = run_comprehensive_tests()
    
    # Save reports
    json_file, readable_file = save_report_to_file(report)
    
    print(f"\n📊 Test report saved to:")
    print(f"  JSON format: {json_file}")
    print(f"  Readable format: {readable_file}")
    
    # Print summary
    session = report['test_session']
    print(f"\n📈 Summary:")
    print(f"  Total Tests: {session['total_tests']}")
    print(f"  Passed: {session['passed_tests']}")
    print(f"  Failed: {session['failed_tests']}")
    print(f"  Success Rate: {(session['passed_tests']/session['total_tests']*100):.1f}%")