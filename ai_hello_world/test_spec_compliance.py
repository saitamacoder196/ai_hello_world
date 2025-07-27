#!/usr/bin/env python3
"""
Test API Spec Compliance
Kiểm tra các endpoints có đúng theo API specification không
"""

import os
import django
import json
from django.test import Client

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'development_settings')
django.setup()

def test_api_spec_compliance():
    """Test API endpoints compliance with specification"""
    client = Client()
    
    print("🧪 Testing API Specification Compliance")
    print("=" * 60)
    
    test_results = []
    
    # Test cases theo đúng API specification
    test_cases = [
        {
            "name": "API-MDE-03-01: Get Idle Resource List",
            "method": "GET",
            "url": "/api/v1/idle-resources?page=1&pageSize=10&sortBy=idleFrom",
            "expected_fields": ["records", "totalCount", "pageInfo", "aggregations", "executionTime"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-02: Get Idle Resource Detail",
            "method": "GET", 
            "url": "/api/v1/idle-resources/550e8400-e29b-41d4-a716-446655440000?includeAudit=true",
            "expected_fields": ["id", "employeeName", "employeeId", "departmentId", "version"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-03: Create Idle Resource",
            "method": "POST",
            "url": "/api/v1/idle-resources",
            "data": {
                "employeeName": "Test Employee",
                "employeeId": "TEST001",
                "departmentId": "DEPT001",
                "idleFromDate": "2025-01-01",
                "idleToDate": "2025-12-31",
                "idleType": "Bench"
            },
            "expected_fields": ["id", "createdRecord", "auditTrailId", "businessRuleResults"],
            "expected_status": 201
        },
        {
            "name": "API-MDE-03-04: Update Idle Resource",
            "method": "PUT",
            "url": "/api/v1/idle-resources/550e8400-e29b-41d4-a716-446655440000",
            "data": {
                "employeeName": "Updated Name",
                "version": 1
            },
            "expected_fields": ["updatedRecord", "auditTrailId", "changedFields"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-05: Delete Idle Resource",
            "method": "DELETE",
            "url": "/api/v1/idle-resources/550e8400-e29b-41d4-a716-446655440000?deleteType=soft",
            "expected_fields": ["deleted", "deletedRecord", "auditTrailId", "deletionType"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-06: Bulk Update",
            "method": "PATCH",
            "url": "/api/v1/idle-resources/bulk",
            "data": {
                "updates": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "data": {"specialAction": "Training"},
                        "version": 1
                    }
                ],
                "operationId": "bulk-test-001"
            },
            "expected_fields": ["operationId", "totalRequested", "successCount", "results"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-07: Export Resources",
            "method": "POST",
            "url": "/api/v1/idle-resources/export",
            "data": {
                "format": "excel",
                "filters": {"departmentId": "DEPT001"}
            },
            "expected_fields": ["exportId", "fileUrl", "fileName", "status"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-08: Import Resources",
            "method": "POST",
            "url": "/api/v1/idle-resources/import",
            "data": {"importMode": "validate"},
            "expected_fields": ["importId", "totalRows", "validRows", "importSummary"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-09: Advanced Search",
            "method": "POST",
            "url": "/api/v1/idle-resources/search",
            "data": {
                "query": "Java developer",
                "filters": {"departmentId": "DEPT001"},
                "page": 1,
                "pageSize": 10
            },
            "expected_fields": ["results", "totalCount", "facets", "searchMetadata"],
            "expected_status": 200
        },
        {
            "name": "API-MDE-03-13: Validate Data",
            "method": "POST",
            "url": "/api/v1/idle-resources/validate",
            "data": {
                "data": {
                    "employeeName": "Test",
                    "idleFromDate": "2025-01-01",
                    "idleToDate": "2024-12-31"  # Invalid: before start date
                },
                "validationType": "full"
            },
            "expected_fields": ["isValid", "validationResults", "errorCount", "validationSummary"],
            "expected_status": 200
        },
        {
            "name": "Master Data API",
            "method": "GET",
            "url": "/api/v1/master-data?dataTypes=departments,jobRanks",
            "expected_fields": ["departments", "jobRanks"],
            "expected_status": 200
        }
    ]
    
    # Run tests
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        
        try:
            # Make request
            if test_case['method'] == 'GET':
                response = client.get(test_case['url'])
            elif test_case['method'] == 'POST':
                response = client.post(test_case['url'], 
                                     data=json.dumps(test_case.get('data', {})),
                                     content_type='application/json')
            elif test_case['method'] == 'PUT':
                response = client.put(test_case['url'],
                                    data=json.dumps(test_case.get('data', {})),
                                    content_type='application/json')
            elif test_case['method'] == 'DELETE':
                response = client.delete(test_case['url'])
            elif test_case['method'] == 'PATCH':
                response = client.patch(test_case['url'],
                                      data=json.dumps(test_case.get('data', {})),
                                      content_type='application/json')
            
            # Check status code
            status_ok = response.status_code == test_case['expected_status']
            print(f"   Status Code: {response.status_code} {'✅' if status_ok else '❌'}")
            
            # Check response format
            if status_ok:
                try:
                    response_data = response.json()
                    
                    # Check expected fields
                    missing_fields = []
                    for field in test_case['expected_fields']:
                        if field not in response_data:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"   Missing Fields: {missing_fields} ❌")
                        field_check = False
                    else:
                        print(f"   Response Fields: ✅ All required fields present")
                        field_check = True
                    
                    # Check field naming convention (camelCase)
                    camel_case_fields = [k for k in response_data.keys() 
                                       if k[0].islower() and '_' not in k]
                    snake_case_fields = [k for k in response_data.keys() if '_' in k]
                    
                    if snake_case_fields:
                        print(f"   ⚠️  Snake case fields found: {snake_case_fields}")
                    else:
                        print(f"   Naming Convention: ✅ CamelCase")
                    
                    # Overall result
                    test_passed = status_ok and field_check
                    test_results.append({
                        'name': test_case['name'],
                        'passed': test_passed,
                        'status_code': response.status_code,
                        'missing_fields': missing_fields
                    })
                    
                    print(f"   Result: {'✅ PASS' if test_passed else '❌ FAIL'}")
                    
                except Exception as e:
                    print(f"   JSON Parse Error: {str(e)} ❌")
                    test_results.append({
                        'name': test_case['name'],
                        'passed': False,
                        'error': str(e)
                    })
            else:
                test_results.append({
                    'name': test_case['name'],
                    'passed': False,
                    'status_code': response.status_code
                })
                
        except Exception as e:
            print(f"   Request Error: {str(e)} ❌")
            test_results.append({
                'name': test_case['name'],
                'passed': False,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 API Specification Compliance Summary")
    print("=" * 60)
    
    passed_tests = [t for t in test_results if t['passed']]
    failed_tests = [t for t in test_results if not t['passed']]
    
    print(f"✅ Passed: {len(passed_tests)}/{len(test_results)}")
    print(f"❌ Failed: {len(failed_tests)}/{len(test_results)}")
    
    if failed_tests:
        print("\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test['name']}")
            if 'missing_fields' in test and test['missing_fields']:
                print(f"     Missing: {test['missing_fields']}")
    
    if len(passed_tests) == len(test_results):
        print("\n🎉 All APIs are compliant with specification!")
    else:
        print(f"\n⚠️  {len(failed_tests)} APIs need attention")
    
    return test_results

if __name__ == "__main__":
    test_api_spec_compliance()