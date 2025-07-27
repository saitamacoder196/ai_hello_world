#!/usr/bin/env python3
"""
Test CORS and API endpoints
"""

import os
import requests
import json

def test_cors_and_apis():
    """Test CORS headers and API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing CORS and API Endpoints")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        ("GET", "/api/v1/status", None),
        ("POST", "/api/v1/auth/simple/login", {"username": "test", "password": "test"}),
        ("GET", "/api/v1/idle-resources/simple", None),
        ("GET", "/api/v1/master-data/simple", None),
        ("GET", "/api/docs/", None),  # Swagger UI
        ("GET", "/api/schema/", None),  # OpenAPI schema
    ]
    
    for method, endpoint, data in endpoints:
        print(f"\n📍 Testing {method} {endpoint}")
        
        try:
            # Add CORS headers to simulate browser request
            headers = {
                'Origin': 'http://localhost:3000',  # Simulate frontend origin
                'Content-Type': 'application/json',
                'Access-Control-Request-Method': method,
                'Access-Control-Request-Headers': 'Content-Type',
            }
            
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", headers=headers)
            else:
                response = requests.post(f"{base_url}{endpoint}", 
                                       json=data, 
                                       headers=headers)
            
            print(f"   Status: {response.status_code}")
            
            # Check CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            }
            
            print(f"   CORS Headers:")
            for header, value in cors_headers.items():
                if value:
                    print(f"     ✅ {header}: {value}")
                else:
                    print(f"     ⚠️  {header}: Not set")
            
            # Check response content for non-HTML endpoints
            if endpoint not in ["/api/docs/", "/api/schema/"]:
                try:
                    response_data = response.json()
                    print(f"   Response: {type(response_data).__name__} with {len(response_data)} keys")
                except:
                    print(f"   Response: {response.headers.get('content-type', 'unknown type')}")
            else:
                print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code < 400:
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error - Server not running?")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Testing Summary:")
    print("- If CORS headers are present, Swagger UI should work")
    print("- If APIs return data, frontend integration is ready")
    print("- Access Swagger UI at: http://localhost:8000/api/docs/")

if __name__ == "__main__":
    test_cors_and_apis()