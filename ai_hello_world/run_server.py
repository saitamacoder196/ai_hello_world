#!/usr/bin/env python3
"""
Script để chạy Django development server với Swagger
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Set development settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'development_settings')
    
    print("🚀 Starting Django Development Server...")
    print("📄 API Documentation available at:")
    print("   - Swagger UI: http://localhost:8000/api/docs/")
    print("   - ReDoc: http://localhost:8000/api/redoc/")
    print("   - OpenAPI Schema: http://localhost:8000/api/schema/")
    print("\n📋 Available APIs:")
    print("   - GET /api/v1/status - API Status")
    print("   - POST /api/v1/auth/simple/login - Simple Login")
    print("   - GET /api/v1/idle-resources/simple - Resource List")
    print("   - GET /api/v1/idle-resources/simple/{id} - Resource Detail")
    print("   - GET /api/v1/master-data/simple - Master Data")
    print("\n🔧 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start server
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])