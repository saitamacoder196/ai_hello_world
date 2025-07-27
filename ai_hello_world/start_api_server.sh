#!/bin/bash

# API Server Startup Script with CORS Fix
# Khởi động Django server với đầy đủ cấu hình cho frontend

echo "🚀 Starting AI Hello World API Server"
echo "====================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check Django configuration
echo "🔍 Checking Django configuration..."
DJANGO_SETTINGS_MODULE=development_settings python manage.py check

if [ $? -eq 0 ]; then
    echo "✅ Django configuration OK"
else
    echo "❌ Django configuration errors found"
    exit 1
fi

# Test CORS configuration
echo "🧪 Testing CORS configuration..."
python test_cors_django.py

echo ""
echo "🌐 Starting Django development server..."
echo "📄 API Documentation will be available at:"
echo "   - Swagger UI: http://localhost:8000/api/docs/"
echo "   - ReDoc: http://localhost:8000/api/redoc/"
echo "   - OpenAPI Schema: http://localhost:8000/api/schema/"
echo ""
echo "📋 Available APIs:"
echo "   - GET /api/v1/status - API Status"
echo "   - POST /api/v1/auth/simple/login - Simple Login"
echo "   - GET /api/v1/idle-resources/simple - Resource List"
echo "   - GET /api/v1/idle-resources/simple/{id} - Resource Detail"
echo "   - GET /api/v1/master-data/simple - Master Data"
echo ""
echo "✅ CORS is enabled for frontend development"
echo "🔧 Press Ctrl+C to stop the server"
echo "====================================="

# Start Django server with development settings
DJANGO_SETTINGS_MODULE=development_settings python manage.py runserver 0.0.0.0:8000