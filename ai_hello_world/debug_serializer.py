#!/usr/bin/env python3

import os
import django
import uuid
from django.utils import timezone
from datetime import timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

from authentication.serializers import LoginResponseSerializer

def test_serializer():
    """Test the LoginResponseSerializer with mock data"""
    
    # Mock response data - exactly what's in the view
    mock_response_data = {
        'success': True,
        'message': 'Login successful',
        'is_valid': True,
        'user_id': str(uuid.uuid4()),
        'user_profile': {
            'user_id': str(uuid.uuid4()),
            'username': 'test_user',
            'email': 'test_user@company.com',
            'first_name': 'Test',
            'last_name': 'User',
            'language': 'en',
            'phone': '+84901234567',
            'avatar_url': 'https://example.com/avatar.jpg',
            'timezone': 'Asia/Ho_Chi_Minh',
            'date_format': 'DD/MM/YYYY',
            'is_active': True,
            'is_verified': True
        },
        'role_info': {
            'roles': [
                {
                    'role_id': str(uuid.uuid4()),
                    'role_name': 'RA_DEPT',
                    'role_description': 'Department Resource Administrator',
                    'is_active': True
                }
            ],
            'permissions': [
                {
                    'permission_id': str(uuid.uuid4()),
                    'permission_name': 'resource_read',
                    'permission_description': 'Read resource data',
                    'resource_type': 'idle_resource',
                    'action': 'read'
                },
                {
                    'permission_id': str(uuid.uuid4()),
                    'permission_name': 'resource_create',
                    'permission_description': 'Create resource data',
                    'resource_type': 'idle_resource',
                    'action': 'create'
                }
            ],
            'department': {
                'department_id': str(uuid.uuid4()),
                'department_name': 'Development Department',
                'parent_department_id': None,
                'is_active': True
            },
            'primary_role': 'RA_DEPT'
        },
        'session_id': str(uuid.uuid4()),
        'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_access_token',
        'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_refresh_token',
        'expires_in': 3600,  # 1 hour
        'last_login_time': None,  # Set to None to test null handling
        'login_time': timezone.now().isoformat(),
        'authentication_method': 'password'
    }
    
    print("Testing LoginResponseSerializer...")
    print(f"Input data keys: {list(mock_response_data.keys())}")
    
    # Create serializer
    serializer = LoginResponseSerializer(data=mock_response_data)
    
    print(f"Is valid: {serializer.is_valid()}")
    
    if not serializer.is_valid():
        print(f"Validation errors: {serializer.errors}")
        return False
    
    print(f"Validated data keys: {list(serializer.validated_data.keys())}")
    print(f"Serializer data keys: {list(serializer.data.keys())}")
    
    # Print only keys that have data
    print("\nActual serializer output:")
    for key, value in serializer.data.items():
        if value is not None:
            print(f"  {key}: {type(value).__name__} - {str(value)[:100]}...")
        else:
            print(f"  {key}: None")
    
    return True

if __name__ == "__main__":
    test_serializer()