#!/usr/bin/env python3

import requests
import json
import datetime

# Base URL for the remote API
BASE_URL = "https://7v38qrq1-8000.asse.devtunnels.ms"

def test_api_endpoint(test_name: str, method: str, endpoint: str, payload=None, params=None):
    """Test an API endpoint with comprehensive logging"""
    
    headers = {
        'User-Agent': 'API-Test-Client/1.0',
        'Accept': 'application/json'
    }
    
    print(f"Testing {test_name}...")
    print(f"  Method: {method}")
    print(f"  Endpoint: {endpoint}")
    if payload:
        print(f"  Payload: {json.dumps(payload, indent=2)}")
    if params:
        print(f"  Params: {params}")
    
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
        
        print(f"  Status Code: {response.status_code}")
        
        # Try to parse JSON response
        try:
            response_body = response.json()
            print(f"  Response: {json.dumps(response_body, indent=2)}")
        except:
            print(f"  Response: {response.text}")
        
        print(f"  Result: {'✅ PASS' if 200 <= response.status_code < 300 else '❌ FAIL'}")
        print("-" * 60)
        
        return 200 <= response.status_code < 300
        
    except Exception as e:
        print(f"  Error: {e}")
        print(f"  Result: ❌ FAIL")
        print("-" * 60)
        return False

def run_updated_api_tests():
    """Test all updated API endpoints with the new request/response formats"""
    
    print("=" * 80)
    print("TESTING UPDATED API ENDPOINTS")
    print("=" * 80)
    
    test_results = []
    
    # Test 1: Get Idle Resource List with new parameters
    print("\n1. Testing Get Idle Resource List with new parameters...")
    params = {
        'page': 1,
        'pageSize': 5,
        'sortBy': 'idleFrom',
        'sortOrder': 'desc',
        'departmentId': 'DEPT001',
        'urgentOnly': False
    }
    test_results.append(test_api_endpoint(
        "Get Idle Resource List (New Format)", 
        "GET", 
        "/api/v1/idle-resources", 
        params=params
    ))
    
    # Test 2: Create Idle Resource with exact specification format
    print("\n2. Testing Create Idle Resource with specification format...")
    create_payload = {
        "employeeName": "Nguyen Van A",
        "employeeId": "EMP001", 
        "departmentId": "DEPT001",
        "childDepartmentId": "CHILD001",
        "jobRank": "Senior",
        "currentLocation": "Hanoi",
        "expectedWorkingPlaces": ["Hanoi", "HCMC"],
        "idleType": "Bench",
        "idleFromDate": "2025-01-01",
        "idleToDate": "2025-12-31",
        "japaneseLevel": "N2",
        "englishLevel": "Intermediate",
        "sourceType": "FJPer",
        "salesPrice": 500000,
        "specialAction": "Training",
        "changeDeptLending": "Not Yet Open",
        "skillsExperience": "Java, Spring Boot, React",
        "progressNotes": "Ready for new project",
        "pic": "Manager Name"
    }
    test_results.append(test_api_endpoint(
        "Create Idle Resource (New Format)", 
        "POST", 
        "/api/v1/idle-resources", 
        payload=create_payload
    ))
    
    # Test 3: Export Idle Resources
    print("\n3. Testing Export Idle Resources...")
    export_payload = {
        "format": "excel",
        "filters": {
            "departmentId": "DEPT001",
            "dateFrom": "2025-01-01",
            "dateTo": "2025-07-27",
            "idleType": "Bench"
        },
        "columns": ["employeeName", "employeeId", "idleFromDate", "specialAction"],
        "sortBy": "idleFromDate",
        "sortOrder": "desc",
        "fileName": "idle_resources_export",
        "includeMetadata": True,
        "asyncMode": False
    }
    test_results.append(test_api_endpoint(
        "Export Idle Resources", 
        "POST", 
        "/api/v1/idle-resources/export", 
        payload=export_payload
    ))
    
    # Test 4: Advanced Search
    print("\n4. Testing Advanced Search...")
    search_payload = {
        "query": "Java developer",
        "filters": {
            "departmentId": "DEPT001",
            "idleType": ["Bench", "Training"],
            "dateRange": {
                "from": "2025-01-01",
                "to": "2025-07-27"
            }
        },
        "facets": ["departmentId", "idleType", "jobRank"],
        "sortBy": "updatedAt",
        "sortOrder": "desc",
        "page": 1,
        "pageSize": 20,
        "includeCount": True,
        "includeAggregations": True,
        "searchMode": "standard"
    }
    test_results.append(test_api_endpoint(
        "Advanced Search", 
        "POST", 
        "/api/v1/idle-resources/search", 
        payload=search_payload
    ))
    
    # Test 5: Validate Data
    print("\n5. Testing Data Validation...")
    validate_payload = {
        "data": {
            "employeeName": "Test Employee",
            "employeeId": "EMP001",
            "departmentId": "DEPT001",
            "idleFromDate": "2025-01-01",
            "idleToDate": "2024-12-31"  # Invalid: end before start
        },
        "validationType": "full",
        "context": "create",
        "strictMode": False,
        "includeWarnings": True,
        "checkDuplicates": True,
        "businessRules": []
    }
    test_results.append(test_api_endpoint(
        "Data Validation", 
        "POST", 
        "/api/v1/idle-resources/validate", 
        payload=validate_payload
    ))
    
    # Test 6: Bulk Update
    print("\n6. Testing Bulk Update...")
    bulk_payload = {
        "updates": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "specialAction": "Training",
                    "progressNotes": "Updated note"
                },
                "version": 1
            }
        ],
        "rollbackOnError": True,
        "validateAll": True,
        "operationId": "bulk-op-001"
    }
    test_results.append(test_api_endpoint(
        "Bulk Update", 
        "PATCH", 
        "/api/v1/idle-resources/bulk", 
        payload=bulk_payload
    ))
    
    # Test 7: Master Data with new format
    print("\n7. Testing Master Data with new format...")
    params = {
        'dataTypes': 'departments,jobRanks,locations',
        'userRole': 'RA_DEPT',
        'departmentScope': 'DEPT001'
    }
    test_results.append(test_api_endpoint(
        "Master Data (New Format)", 
        "GET", 
        "/api/v1/master-data", 
        params=params
    ))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("🎉 All updated API endpoints are working correctly!")
    elif passed > total // 2:
        print("⚠️ Most API endpoints are working with the new format.")
    else:
        print("❌ Several API endpoints need attention.")
    
    return test_results

if __name__ == "__main__":
    run_updated_api_tests()