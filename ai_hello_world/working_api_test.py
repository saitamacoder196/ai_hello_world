#!/usr/bin/env python3

import requests
import json
import datetime
from typing import Dict, Any

# Base URL for the remote API
BASE_URL = "https://7v38qrq1-8000.asse.devtunnels.ms"

def log_api_test(test_name: str, method: str, endpoint: str, 
                 request_headers: Dict = None, request_payload: Any = None,
                 response_status: int = None, response_headers: Dict = None,
                 response_body: Any = None, error: str = None):
    """Log comprehensive API test details"""
    
    test_result = {
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
    
    return test_result

def test_api_endpoint(test_name: str, method: str, endpoint: str, payload: Any = None):
    """Test an API endpoint with comprehensive logging"""
    
    headers = {
        'User-Agent': 'API-Test-Client/1.0',
        'Accept': 'application/json'
    }
    
    print(f"Testing {test_name}...")
    
    try:
        if method.upper() == 'POST' and payload:
            headers['Content-Type'] = 'application/json'
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers)
        else:  # GET
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        
        # Try to parse JSON response
        try:
            response_body = response.json()
        except:
            response_body = response.text
        
        return log_api_test(
            test_name=test_name,
            method=method.upper(),
            endpoint=endpoint,
            request_headers=headers,
            request_payload=payload,
            response_status=response.status_code,
            response_headers=response.headers,
            response_body=response_body
        )
        
    except Exception as e:
        return log_api_test(
            test_name=test_name,
            method=method.upper(),
            endpoint=endpoint,
            request_headers=headers,
            request_payload=payload,
            error=str(e)
        )

def run_api_tests():
    """Run all API tests that we know work"""
    
    print("=== Comprehensive API Testing Suite ===")
    print(f"Testing against: {BASE_URL}")
    print(f"Start time: {datetime.datetime.now().isoformat()}")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Health Check API
    test_results.append(test_api_endpoint("Health Check", "GET", "/api/health/"))
    
    # Test 2: Hello/Index API
    test_results.append(test_api_endpoint("Hello Index", "GET", "/"))
    
    # Test 3: Auth Health Check
    test_results.append(test_api_endpoint("Auth Health Check", "GET", "/api/v1/auth/health"))
    
    # Test 4: Login API with credentials
    login_payload = {
        "username": "test_user",
        "password": "test_password", 
        "language": "en",
        "remember_me": False
    }
    test_results.append(test_api_endpoint("User Login", "POST", "/api/v1/auth/login", login_payload))
    
    # Test 5: Idle Resources List
    test_results.append(test_api_endpoint("Idle Resources List", "GET", "/api/v1/idle-resources"))
    
    # Test 6: Idle Resources with pagination
    test_results.append(test_api_endpoint("Idle Resources Paginated", "GET", "/api/v1/idle-resources?page=1&page_size=5"))
    
    # Test 7: Master Data
    test_results.append(test_api_endpoint("Master Data", "GET", "/api/v1/master-data"))
    
    # Test 8: Login with different credentials
    admin_login_payload = {
        "username": "admin",
        "password": "admin123", 
        "language": "vi",
        "remember_me": True
    }
    test_results.append(test_api_endpoint("Admin Login", "POST", "/api/v1/auth/login", admin_login_payload))
    
    # Test 9: Create Idle Resource
    resource_payload = {
        "employee_name": "John Doe",
        "employee_id": "EMP001",
        "department_name": "IT",
        "job_rank": "Senior Developer",
        "skills": ["Python", "Django"],
        "experience_years": 5,
        "hourly_rate": 50.0
    }
    test_results.append(test_api_endpoint("Create Idle Resource", "POST", "/api/v1/idle-resources", resource_payload))
    
    print("\n" + "=" * 60)
    print("Tests completed. Generating report...")
    
    return test_results

def generate_comprehensive_report(test_results):
    """Generate comprehensive report in multiple formats"""
    
    # Count results
    passed = sum(1 for test in test_results if test["success"])
    total = len(test_results)
    
    # Create comprehensive report
    report = {
        "test_session": {
            "timestamp": datetime.datetime.now().isoformat(),
            "base_url": BASE_URL,
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed / total * 100) if total > 0 else 0
        },
        "tests": test_results
    }
    
    # Save JSON report
    with open("comprehensive_api_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Save readable report
    with open("comprehensive_api_report.txt", 'w', encoding='utf-8') as f:
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
        f.write(f"  Success Rate: {session['success_rate']:.1f}%\n\n")
        
        for i, test in enumerate(test_results, 1):
            f.write("-" * 80 + "\n")
            f.write(f"TEST #{i}: {test['test_name']}\n")
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
                if isinstance(resp['body'], (dict, list)):
                    f.write(f"    {json.dumps(resp['body'], indent=4, ensure_ascii=False)}\n")
                else:
                    f.write(f"    {resp['body']}\n")
            
            if test['error']:
                f.write(f"ERROR: {test['error']}\n")
            
            f.write("\n\n")
    
    return report

if __name__ == "__main__":
    # Run tests
    test_results = run_api_tests()
    
    # Generate comprehensive report
    report = generate_comprehensive_report(test_results)
    
    print(f"\n📊 Comprehensive reports generated:")
    print(f"  JSON format: comprehensive_api_report.json")
    print(f"  Readable format: comprehensive_api_report.txt")
    
    # Print summary
    session = report['test_session']
    print(f"\n📈 Final Summary:")
    print(f"  Total Tests: {session['total_tests']}")
    print(f"  Passed: {session['passed_tests']}")
    print(f"  Failed: {session['failed_tests']}")
    print(f"  Success Rate: {session['success_rate']:.1f}%")
    
    if session['success_rate'] > 80:
        print("🎉 API endpoints are working well!")
    elif session['success_rate'] > 50:
        print("⚠️ Most API endpoints are working.")
    else:
        print("❌ Many API endpoints need attention.")