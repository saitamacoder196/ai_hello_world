#!/usr/bin/env python3

import os
import django
from django.test import Client
from django.test.utils import override_settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'development_settings')
django.setup()

def test_cors_headers():
    """Test CORS headers in Django responses"""
    client = Client()
    
    print("🧪 Testing CORS Headers with Django Test Client")
    print("=" * 55)
    
    # Test API endpoints with CORS headers
    endpoints = [
        "/api/v1/status",
        "/api/v1/idle-resources/simple",
        "/api/v1/master-data/simple",
    ]
    
    for endpoint in endpoints:
        print(f"\n📍 Testing {endpoint}")
        
        # Make request with Origin header (simulates CORS request)
        response = client.get(endpoint, HTTP_ORIGIN='http://localhost:3000')
        
        print(f"   Status Code: {response.status_code}")
        
        # Check CORS headers
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods', 
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials'
        ]
        
        for header in cors_headers:
            value = response.get(header)
            if value:
                print(f"   ✅ {header}: {value}")
            else:
                print(f"   ⚠️  {header}: Not set")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Response: {type(data).__name__} with {len(data)} fields")
            except:
                print(f"   📄 Response: {response['content-type']}")
        
        print(f"   {'✅ Success' if response.status_code == 200 else '❌ Failed'}")
    
    # Test OPTIONS request (preflight)
    print(f"\n📍 Testing OPTIONS /api/v1/status (CORS Preflight)")
    response = client.options('/api/v1/status', 
                             HTTP_ORIGIN='http://localhost:3000',
                             HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET')
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.get('Access-Control-Allow-Origin', 'Not set')}")
    print(f"   Access-Control-Allow-Methods: {response.get('Access-Control-Allow-Methods', 'Not set')}")
    
    print("\n" + "=" * 55)
    print("🎯 CORS Configuration Status:")
    
    # Check if CORS is properly configured
    test_response = client.get('/api/v1/status', HTTP_ORIGIN='http://localhost:3000')
    if test_response.get('Access-Control-Allow-Origin'):
        print("✅ CORS is properly configured")
        print("✅ Swagger UI should work without CORS errors")
        print("✅ Frontend can make API calls")
    else:
        print("❌ CORS headers not found")
        print("⚠️  Swagger UI may have CORS issues")

if __name__ == "__main__":
    test_cors_headers()