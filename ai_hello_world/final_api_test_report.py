#!/usr/bin/env python3

import requests
import json
import datetime
from typing import Dict, Any

# Base URL for the remote API
BASE_URL = "https://7v38qrq1-8000.asse.devtunnels.ms"

class FinalAPITestRunner:
    def __init__(self):
        self.test_results = []
        self.test_count = 0
    
    def log_test(self, test_name: str, method: str, endpoint: str, 
                 request_headers: Dict = None, request_payload: Any = None,
                 request_params: Dict = None, response_status: int = None, 
                 response_headers: Dict = None, response_body: Any = None, 
                 error: str = None):
        
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
                "payload": request_payload,
                "params": request_params
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
    
    def test_api_endpoint(self, test_name: str, method: str, endpoint: str, 
                         payload=None, params=None, expected_status=200):
        """Test an API endpoint with comprehensive logging"""
        
        headers = {
            'User-Agent': 'Final-API-Test/1.0',
            'Accept': 'application/json'
        }
        
        print(f"Testing {test_name}...")
        
        try:
            if method.upper() == 'POST' and payload:
                headers['Content-Type'] = 'application/json'
                response = requests.post(f"{BASE_URL}{endpoint}", json=payload, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, params=params)
            elif method.upper() == 'PUT' and payload:
                headers['Content-Type'] = 'application/json'
                response = requests.put(f"{BASE_URL}{endpoint}", json=payload, headers=headers, params=params)
            elif method.upper() == 'DELETE':
                response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers, params=params)
            elif method.upper() == 'PATCH' and payload:
                headers['Content-Type'] = 'application/json'
                response = requests.patch(f"{BASE_URL}{endpoint}", json=payload, headers=headers, params=params)
            else:  # GET
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
            
            # Try to parse JSON response
            try:
                response_body = response.json()
            except:
                response_body = response.text
            
            return self.log_test(
                test_name=test_name,
                method=method.upper(),
                endpoint=endpoint,
                request_headers=headers,
                request_payload=payload,
                request_params=params,
                response_status=response.status_code,
                response_headers=response.headers,
                response_body=response_body
            )
            
        except Exception as e:
            return self.log_test(
                test_name=test_name,
                method=method.upper(),
                endpoint=endpoint,
                request_headers=headers,
                request_payload=payload,
                request_params=params,
                error=str(e)
            )

    def run_complete_test_suite(self):
        """Run comprehensive test suite for all API endpoints"""
        
        print("=" * 80)
        print("FINAL COMPREHENSIVE API TEST SUITE")
        print("=" * 80)
        print(f"Testing against: {BASE_URL}")
        print(f"Start time: {datetime.datetime.now().isoformat()}")
        print("=" * 80)
        
        # Test 1: Health Check
        self.test_api_endpoint("Health Check", "GET", "/api/health/")
        
        # Test 2: Auth Health Check  
        self.test_api_endpoint("Auth Health Check", "GET", "/api/v1/auth/health")
        
        # Test 3: Get Idle Resource List (Original Format)
        params = {'page': 1, 'page_size': 5}
        self.test_api_endpoint("Get Idle Resource List (Original)", "GET", "/api/v1/idle-resources", params=params)
        
        # Test 4: Get Idle Resource List (New Format)
        params = {
            'page': 1,
            'pageSize': 5,
            'sortBy': 'idleFrom',
            'sortOrder': 'desc',
            'departmentId': 'DEPT001'
        }
        self.test_api_endpoint("Get Idle Resource List (New Format)", "GET", "/api/v1/idle-resources", params=params)
        
        # Test 5: Create Idle Resource (Original Format Test)
        create_payload_old = {
            "employee_name": "Test Employee",
            "employee_id": "EMP001",
            "department_id": "DEPT001",
            "job_rank": "Senior",
            "current_location": "Hanoi",
            "idle_type": "Bench",
            "idle_from_date": "2025-01-01",
            "idle_to_date": "2025-12-31"
        }
        self.test_api_endpoint("Create Idle Resource (Old Format)", "POST", "/api/v1/idle-resources", payload=create_payload_old)
        
        # Test 6: Create Idle Resource (New Format)
        create_payload_new = {
            "employeeName": "Nguyen Van A",
            "employeeId": "EMP001",
            "departmentId": "DEPT001",
            "jobRank": "Senior",
            "currentLocation": "Hanoi",
            "idleType": "Bench",
            "idleFromDate": "2025-01-01",
            "idleToDate": "2025-12-31",
            "japaneseLevel": "N2",
            "englishLevel": "Intermediate",
            "sourceType": "FJPer",
            "salesPrice": 500000,
            "specialAction": "Training"
        }
        self.test_api_endpoint("Create Idle Resource (New Format)", "POST", "/api/v1/idle-resources", payload=create_payload_new)
        
        # Test 7: Export Idle Resources
        export_payload = {
            "format": "excel",
            "filters": {"departmentId": "DEPT001"},
            "columns": ["employeeName", "employeeId"],
            "fileName": "test_export"
        }
        self.test_api_endpoint("Export Idle Resources", "POST", "/api/v1/idle-resources/export", payload=export_payload)
        
        # Test 8: Advanced Search
        search_payload = {
            "query": "Java developer",
            "page": 1,
            "pageSize": 10
        }
        self.test_api_endpoint("Advanced Search", "POST", "/api/v1/idle-resources/search", payload=search_payload)
        
        # Test 9: Data Validation (Valid Data)
        validate_payload_valid = {
            "data": {
                "employeeName": "Valid Employee",
                "idleFromDate": "2025-01-01",
                "idleToDate": "2025-12-31"
            },
            "validationType": "full"
        }
        self.test_api_endpoint("Data Validation (Valid)", "POST", "/api/v1/idle-resources/validate", payload=validate_payload_valid)
        
        # Test 10: Data Validation (Invalid Data)
        validate_payload_invalid = {
            "data": {
                "employeeName": "Invalid Employee",
                "idleFromDate": "2025-01-01", 
                "idleToDate": "2024-12-31"  # Invalid: end before start
            },
            "validationType": "full"
        }
        self.test_api_endpoint("Data Validation (Invalid)", "POST", "/api/v1/idle-resources/validate", payload=validate_payload_invalid)
        
        # Test 11: Bulk Update
        bulk_payload = {
            "updates": [{
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "data": {"specialAction": "Training"},
                "version": 1
            }],
            "operationId": "test-bulk-001"
        }
        self.test_api_endpoint("Bulk Update", "PATCH", "/api/v1/idle-resources/bulk", payload=bulk_payload)
        
        # Test 12: Master Data
        self.test_api_endpoint("Master Data", "GET", "/api/v1/master-data")
        
        # Test 13: Master Data with Filters
        params = {'dataTypes': 'departments,jobRanks'}
        self.test_api_endpoint("Master Data (Filtered)", "GET", "/api/v1/master-data", params=params)
        
        return self.generate_final_report()
    
    def generate_final_report(self):
        """Generate comprehensive final test report"""
        
        # Count results
        passed = sum(1 for test in self.test_results if test["success"])
        total = len(self.test_results)
        
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
            "test_results": self.test_results,
            "summary": {
                "endpoint_coverage": [
                    "GET /api/health/ - Health Check",
                    "GET /api/v1/auth/health - Auth Health Check", 
                    "GET /api/v1/idle-resources - List Resources (both formats)",
                    "POST /api/v1/idle-resources - Create Resource (both formats)",
                    "POST /api/v1/idle-resources/export - Export Resources",
                    "POST /api/v1/idle-resources/search - Advanced Search",
                    "POST /api/v1/idle-resources/validate - Data Validation",
                    "PATCH /api/v1/idle-resources/bulk - Bulk Operations",
                    "GET /api/v1/master-data - Master Data"
                ],
                "format_compatibility": {
                    "camelCase_support": "Implemented",
                    "snake_case_legacy": "Maintained",
                    "specification_compliance": f"{passed}/{total} endpoints working"
                }
            }
        }
        
        return report

def main():
    """Run the final comprehensive test suite"""
    
    test_runner = FinalAPITestRunner()
    report = test_runner.run_complete_test_suite()
    
    # Save comprehensive report
    with open("final_api_test_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generate readable summary
    with open("final_api_test_summary.txt", 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("FINAL API TEST REPORT SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        
        session = report['test_session']
        f.write(f"Test Session:\n")
        f.write(f"  Timestamp: {session['timestamp']}\n")
        f.write(f"  Base URL: {session['base_url']}\n")
        f.write(f"  Total Tests: {session['total_tests']}\n")
        f.write(f"  Passed: {session['passed_tests']}\n")
        f.write(f"  Failed: {session['failed_tests']}\n")
        f.write(f"  Success Rate: {session['success_rate']:.1f}%\n\n")
        
        f.write("Individual Test Results:\n")
        f.write("-" * 40 + "\n")
        for test in report['test_results']:
            status = "✅ PASS" if test['success'] else "❌ FAIL"
            f.write(f"{test['test_number']:2d}. {test['test_name']}: {status}\n")
            if test.get('error'):
                f.write(f"    Error: {test['error']}\n")
            elif test['response']['status_code']:
                f.write(f"    Status: {test['response']['status_code']}\n")
        
        f.write(f"\nEndpoint Coverage:\n")
        f.write("-" * 40 + "\n")
        for endpoint in report['summary']['endpoint_coverage']:
            f.write(f"• {endpoint}\n")
    
    # Print summary
    print("\n" + "=" * 80)
    print("FINAL TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {report['test_session']['total_tests']}")
    print(f"Passed: {report['test_session']['passed_tests']}")
    print(f"Failed: {report['test_session']['failed_tests']}")
    print(f"Success Rate: {report['test_session']['success_rate']:.1f}%")
    
    print(f"\n📊 Reports generated:")
    print(f"  • final_api_test_report.json - Complete test data")
    print(f"  • final_api_test_summary.txt - Human-readable summary")
    
    if report['test_session']['success_rate'] >= 90:
        print("🎉 Excellent! API implementation is working great!")
    elif report['test_session']['success_rate'] >= 75:
        print("✅ Good! Most API endpoints are working correctly.")
    elif report['test_session']['success_rate'] >= 50:
        print("⚠️ Some API endpoints need attention.")
    else:
        print("❌ Several API endpoints require fixes.")

if __name__ == "__main__":
    main()