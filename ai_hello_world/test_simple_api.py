#!/usr/bin/env python3

import os
import sys
import django
import json
from django.test import Client

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

def test_simple_apis():
    """Test các API đơn giản cho màn hình list"""
    client = Client()
    
    print("=== Testing Simple APIs for List Screens ===\n")
    
    # 1. Test API Status
    print("1. Testing API Status...")
    response = client.get('/api/v1/status')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {data['status']}")
        print(f"   Available APIs: {len(data['apis_available'])}")
        print("   ✅ API Status - OK")
    else:
        print("   ❌ API Status - FAILED")
    print()
    
    # 2. Test Simple Login
    print("2. Testing Simple Login...")
    login_data = {"username": "test_user", "password": "any_password"}
    response = client.post('/api/v1/auth/simple/login', 
                          data=json.dumps(login_data), 
                          content_type='application/json')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Success: {data['success']}")
        print(f"   Username: {data['username']}")
        print(f"   Token: {data['access_token'][:30]}...")
        print("   ✅ Simple Login - OK")
    else:
        print("   ❌ Simple Login - FAILED")
    print()
    
    # 3. Test Idle Resources List
    print("3. Testing Idle Resources List...")
    response = client.get('/api/v1/idle-resources/simple?page=1&page_size=5')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total Records: {data['total_count']}")
        print(f"   Records in Page: {len(data['records'])}")
        print(f"   First Employee: {data['records'][0]['employee_name']}")
        print(f"   Departments: {list(data['aggregations']['by_department'].keys())}")
        print("   ✅ Idle Resources List - OK")
    else:
        print("   ❌ Idle Resources List - FAILED")
    print()
    
    # 4. Test Resource Detail
    print("4. Testing Resource Detail...")
    test_id = "test-resource-123"
    response = client.get(f'/api/v1/idle-resources/simple/{test_id}')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Resource ID: {data['id']}")
        print(f"   Employee Name: {data['employee_name']}")
        print(f"   Department: {data['department_name']}")
        print(f"   Skills: {data['skills_experience']}")
        print("   ✅ Resource Detail - OK")
    else:
        print("   ❌ Resource Detail - FAILED")
    print()
    
    # 5. Test Master Data
    print("5. Testing Master Data...")
    response = client.get('/api/v1/master-data/simple')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Departments: {len(data['departments'])}")
        print(f"   Job Ranks: {len(data['job_ranks'])}")
        print(f"   Locations: {len(data['locations'])}")
        print(f"   Idle Types: {len(data['idle_types'])}")
        print("   ✅ Master Data - OK")
    else:
        print("   ❌ Master Data - FAILED")
    print()
    
    print("=== Test Complete ===")
    print("Tất cả APIs đã sẵn sàng cho việc phát triển frontend!")
    print("\nCác APIs có thể sử dụng:")
    print("- GET /api/v1/status")
    print("- POST /api/v1/auth/simple/login")
    print("- GET /api/v1/idle-resources/simple")
    print("- GET /api/v1/idle-resources/simple/{id}")
    print("- GET /api/v1/master-data/simple")

if __name__ == "__main__":
    test_simple_apis()