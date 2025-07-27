#!/bin/bash

echo "🔧 Setting up Django CORS configuration..."

# Install django-cors-headers
echo "📦 Installing django-cors-headers..."
pip install django-cors-headers==4.3.1

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ django-cors-headers installed successfully"
else
    echo "❌ Failed to install django-cors-headers"
    exit 1
fi

echo "🚀 Starting Django server with CORS support..."
echo "Server will be available at: http://127.0.0.1:8000"
echo "API endpoints will be accessible from any origin in development mode"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Django development server
python manage.py runserver 0.0.0.0:8000
