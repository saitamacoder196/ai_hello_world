#!/usr/bin/env python3

import requests
import json

# Base URL for the remote API
BASE_URL = "https://7v38qrq1-8000.asse.devtunnels.ms"

def test_health_api():
    """Test the health check API"""
    print("Testing Health Check API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_hello_api():
    """Test the hello/index API"""
    print("\nTesting Hello/Index API...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            if response.headers.get('content-type', '').startswith('application/json'):
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Response: {response.text}")
        else:
            print(f"Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login_api():
    """Test the login API endpoint"""
    print("\nTesting Login API...")
    
    # Test data
    login_data = {
        "username": "test_user",
        "password": "test_password", 
        "language": "en",
        "remember_me": False
    }
    
    print(f"Request: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 400, 401, 403]:
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_auth_health_api():
    """Test the auth health check API"""
    print("\nTesting Auth Health Check API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/health")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_idle_resources_api():
    """Test the idle resources API"""
    print("\nTesting Idle Resources API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/idle-resources?page=1&page_size=5")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 404]:
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_master_data_api():
    """Test the master data API"""
    print("\nTesting Master Data API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/master-data")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 404]:
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Remote API Testing Suite ===")
    print(f"Testing against: {BASE_URL}")
    print("=" * 50)
    
    results = []
    results.append(("Health API", test_health_api()))
    results.append(("Hello/Index API", test_hello_api()))
    results.append(("Auth Health API", test_auth_health_api()))
    results.append(("Login API", test_login_api()))
    results.append(("Idle Resources API", test_idle_resources_api()))
    results.append(("Master Data API", test_master_data_api()))
    
    print("\n" + "=" * 50)
    print("=== Test Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nSummary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API endpoints are working correctly!")
    elif passed > 0:
        print("⚠️ Some API endpoints are working, others need attention.")
    else:
        print("❌ No API endpoints are responding correctly.")