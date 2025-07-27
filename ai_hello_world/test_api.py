#!/usr/bin/env python3

import os
import sys
import django
import json
from django.test import Client
from django.conf import settings

# Setup Django environment with test settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

def test_login_api():
    """Test the login API endpoint"""
    client = Client()
    
    # Test data
    login_data = {
        "username": "test_user",
        "password": "test_password", 
        "language": "en",
        "remember_me": False
    }
    
    print("Testing Login API...")
    print(f"Request: {json.dumps(login_data, indent=2)}")
    
    # Make API call
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_health_api():
    """Test the health check API"""
    client = Client()
    
    print("\nTesting Health Check API...")
    
    response = client.get('/api/v1/auth/health')
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_idle_resources_api():
    """Test the idle resources API"""
    client = Client()
    
    print("\nTesting Idle Resources API...")
    
    response = client.get('/api/v1/idle-resources?page=1&page_size=5')
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

if __name__ == "__main__":
    print("=== API Testing Suite ===")
    
    results = []
    results.append(("Login API", test_login_api()))
    results.append(("Health API", test_health_api()))
    results.append(("Idle Resources API", test_idle_resources_api()))
    
    print("\n=== Test Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nSummary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API endpoints are working correctly!")
    else:
        print("⚠️ Some API endpoints need attention.")