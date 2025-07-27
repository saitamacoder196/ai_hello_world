#!/usr/bin/env python3

import requests
import json
from datetime import datetime

# Base URL for the remote API
BASE_URL = "https://7v38qrq1-8000.asse.devtunnels.ms"

def test_get_idle_resources_format():
    """Test GET /api/v1/idle-resources response format"""
    
    print("=" * 80)
    print("TESTING FIXED API RESPONSE FORMATS")
    print("=" * 80)
    print(f"Testing against: {BASE_URL}")
    print(f"Test time: {datetime.now().isoformat()}")
    print("=" * 80)
    
    # Test GET idle resources with expected format
    print("\n1. Testing GET /api/v1/idle-resources response format...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/idle-resources?page=1&pageSize=3")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response JSON: {json.dumps(data, indent=2)}")
                
                # Check if response has correct format
                expected_fields = ['records', 'totalCount', 'pageInfo', 'aggregations', 'executionTime']
                has_all_fields = all(field in data for field in expected_fields)
                
                if has_all_fields:
                    print("✅ CORRECT FORMAT: Response contains all expected fields")
                    
                    # Check records structure
                    if 'records' in data and isinstance(data['records'], list) and len(data['records']) > 0:
                        first_record = data['records'][0]
                        record_fields = ['id', 'employeeName', 'employeeId', 'departmentId', 'jobRank', 
                                       'currentLocation', 'idleType', 'idleFromDate', 'idleToDate', 
                                       'idleMM', 'salesPrice', 'specialAction', 'pic']
                        
                        record_has_fields = all(field in first_record for field in record_fields[:6])  # Check key fields
                        
                        if record_has_fields:
                            print("✅ RECORD FORMAT: Records have correct camelCase fields")
                        else:
                            print("❌ RECORD FORMAT: Records missing expected fields")
                            print(f"First record fields: {list(first_record.keys())}")
                    else:
                        print("⚠️ No records in response to validate structure")
                    
                    # Check pageInfo structure
                    if 'pageInfo' in data:
                        page_info = data['pageInfo']
                        page_fields = ['currentPage', 'totalPages', 'hasNextPage', 'hasPreviousPage']
                        page_has_fields = all(field in page_info for field in page_fields)
                        
                        if page_has_fields:
                            print("✅ PAGINATION FORMAT: pageInfo has correct structure")
                        else:
                            print("❌ PAGINATION FORMAT: pageInfo missing expected fields")
                            print(f"pageInfo fields: {list(page_info.keys())}")
                
                else:
                    print("❌ INCORRECT FORMAT: Response missing expected fields")
                    print(f"Expected: {expected_fields}")
                    print(f"Actual: {list(data.keys())}")
                    
                    # Check if it's the old format
                    if len(data) == 1 and 'aggregations' in data:
                        print("🔄 SERVER CACHE: This appears to be cached old response")
                        print("   Recommendation: Restart Django server to load new code")
                
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                print(f"Raw response: {response.text}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    print("\n" + "=" * 80)
    
    # Test POST create endpoint format
    print("\n2. Testing POST /api/v1/idle-resources (Create) format...")
    
    create_payload = {
        "employeeName": "Test Employee",
        "employeeId": "TEST001",
        "departmentId": "DEPT001", 
        "jobRank": "Senior",
        "currentLocation": "Hanoi",
        "idleType": "Bench",
        "idleFromDate": "2025-01-01",
        "idleToDate": "2025-12-31"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/idle-resources", 
            json=create_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            try:
                data = response.json()
                print(f"Response JSON: {json.dumps(data, indent=2)}")
                
                # Check if response has correct format for create
                expected_create_fields = ['id', 'createdRecord', 'auditTrailId', 'validationWarnings', 
                                        'businessRuleResults', 'createdAt']
                has_create_fields = all(field in data for field in expected_create_fields[:3])  # Check key fields
                
                if has_create_fields:
                    print("✅ CREATE FORMAT: Response contains expected create fields")
                else:
                    print("❌ CREATE FORMAT: Response missing expected create fields")
                    print(f"Expected: {expected_create_fields}")
                    print(f"Actual: {list(data.keys())}")
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                print(f"Raw response: {response.text}")
        elif response.status_code == 400:
            try:
                error_data = response.json()
                print(f"Validation Error: {json.dumps(error_data, indent=2)}")
                print("🔄 This might be due to server not loading updated serializers")
            except:
                print(f"Error response: {response.text}")
        elif response.status_code == 405:
            print("❌ Method Not Allowed - Server may not have loaded new endpoint configuration")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("If you see 'SERVER CACHE' or old response formats:")
    print("1. The code changes are correct in the repository")
    print("2. The server needs to restart to load the new code")
    print("3. Django development server auto-reload may not have triggered")
    print("\nExpected Response Format for GET /api/v1/idle-resources:")
    print("""{
  "records": [
    {
      "id": "uuid",
      "employeeName": "string",
      "employeeId": "string", 
      "departmentId": "string",
      "jobRank": "string",
      "currentLocation": "string",
      "idleType": "string",
      "idleFromDate": "2025-01-01",
      "idleToDate": "2025-12-31",
      "idleMM": 12,
      "salesPrice": 500000,
      "specialAction": "string",
      "pic": "string"
    }
  ],
  "totalCount": 100,
  "pageInfo": {
    "currentPage": 1,
    "totalPages": 4,
    "hasNextPage": true,
    "hasPreviousPage": false
  },
  "aggregations": {},
  "executionTime": 150
}""")

if __name__ == "__main__":
    test_get_idle_resources_format()