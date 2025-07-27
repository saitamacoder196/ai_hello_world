#!/usr/bin/env python3

import os
import django
import uuid
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

from authentication.serializers import LoginResponseSerializer

def test_correct_serializer_usage():
    """Test the correct way to use serializers for output"""
    
    # Create a simple object-like class to hold the data
    class MockData:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    # Mock response data
    mock_data = MockData(
        success=True,
        message='Login successful',
        is_valid=True,
        user_id=str(uuid.uuid4()),
        user_profile=MockData(
            user_id=str(uuid.uuid4()),
            username='test_user',
            email='test_user@company.com',
            first_name='Test',
            last_name='User',
            language='en',
            phone='+84901234567',
            avatar_url='https://example.com/avatar.jpg',
            timezone='Asia/Ho_Chi_Minh',
            date_format='DD/MM/YYYY',
            is_active=True,
            is_verified=True
        ),
        role_info=MockData(
            roles=[
                MockData(
                    role_id=str(uuid.uuid4()),
                    role_name='RA_DEPT',
                    role_description='Department Resource Administrator',
                    is_active=True
                )
            ],
            permissions=[
                MockData(
                    permission_id=str(uuid.uuid4()),
                    permission_name='resource_read',
                    permission_description='Read resource data',
                    resource_type='idle_resource',
                    action='read'
                )
            ],
            department=MockData(
                department_id=str(uuid.uuid4()),
                department_name='Development Department',
                parent_department_id=None,
                is_active=True
            ),
            primary_role='RA_DEPT'
        ),
        session_id=str(uuid.uuid4()),
        access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_access_token',
        refresh_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_refresh_token',
        expires_in=3600,
        last_login_time=None,
        login_time=timezone.now(),
        authentication_method='password'
    )
    
    print("Testing correct serializer usage (passing object instance)...")
    
    # Use serializer correctly - pass object instance, not data dict
    serializer = LoginResponseSerializer(mock_data)
    
    print(f"Serializer data keys: {list(serializer.data.keys())}")
    print(f"Number of keys in output: {len(serializer.data)}")
    
    return serializer.data

def test_dict_serialization():
    """Test using dictionary directly"""
    
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
        'expires_in': 3600,
        'last_login_time': None,
        'login_time': timezone.now().isoformat(),
        'authentication_method': 'password'
    }
    
    print("\nTesting direct dictionary return (no serializer validation)...")
    print(f"Dictionary keys: {list(mock_response_data.keys())}")
    print(f"Number of keys in output: {len(mock_response_data)}")
    
    return mock_response_data

if __name__ == "__main__":
    print("=== Debugging Serializer Issues ===")
    
    result1 = test_correct_serializer_usage()
    result2 = test_dict_serialization()
    
    print(f"\nObject serialization result length: {len(result1)}")
    print(f"Dictionary result length: {len(result2)}")
    
    # The solution is to return the dictionary directly since it's mock data
    print("\n✅ Solution: Return dictionary directly for mock responses")