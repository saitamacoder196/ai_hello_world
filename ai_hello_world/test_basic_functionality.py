#!/usr/bin/env python3
"""
Basic functionality test without external dependencies.
Demonstrates core model and DAO method functionality.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_hello_world.settings')
django.setup()

from django.utils import timezone
from authentication.models import Department, Employee, User, UserSession
from resource_management.models import IdleResource

def test_basic_models():
    """Test basic model creation and validation."""
    print("🧪 Testing Basic Model Creation...")
    
    try:
        # Test Department model
        dept = Department.objects.create(
            department_name="Engineering Test",
            is_active=True
        )
        print(f"✅ Department created: {dept.department_name}")
        
        # Test User model
        user = User.objects.create(
            username="testuser123",
            email="test123@company.com",
            password_hash="dummy_hash_for_testing",
            is_active=True
        )
        print(f"✅ User created: {user.username}")
        
        # Test Employee model
        employee = Employee.objects.create(
            employee_number="EMP123",
            first_name="John",
            last_name="Doe",
            email="john.doe123@company.com",
            department=dept,
            position="Software Engineer",
            hire_date=timezone.now().date()
        )
        print(f"✅ Employee created: {employee.employee_number}")
        
        return dept, user, employee
        
    except Exception as e:
        print(f"❌ Model creation failed: {str(e)}")
        return None, None, None

def test_user_session_dao_methods(user):
    """Test UserSession DAO methods."""
    if not user:
        print("❌ Cannot test UserSession: No user available")
        return
    
    print("\n🔐 Testing UserSession DAO Methods...")
    
    try:
        # Test create_session
        session_result = UserSession.create_session(
            user=user,
            ip_address="192.168.1.100",
            user_agent="Test Browser",
            remember_me=False
        )
        
        if session_result:
            print("✅ create_session() - Session created successfully")
            print(f"   Session ID: {session_result['session_id']}")
            print(f"   Expires in: {session_result['expires_in']} seconds")
            
            # Test validate_session
            access_token = session_result['access_token']
            validation_result = UserSession.validate_session(access_token)
            
            if validation_result:
                print("✅ validate_session() - Session validated successfully")
                print(f"   User ID: {validation_result['user_id']}")
            else:
                print("❌ validate_session() - Validation failed")
            
            # Test get_active_sessions
            active_sessions = UserSession.get_active_sessions(user)
            print(f"✅ get_active_sessions() - Found {len(active_sessions)} active sessions")
            
            # Test session cleanup
            cleanup_result = UserSession.cleanup_expired_sessions(days_old=30)
            print(f"✅ cleanup_expired_sessions() - Cleaned up {cleanup_result['deleted_sessions']} sessions")
            
        else:
            print("❌ create_session() - Failed to create session")
            
    except Exception as e:
        print(f"❌ UserSession DAO methods failed: {str(e)}")

def test_idle_resource_dao_methods(employee):
    """Test IdleResource DAO methods."""
    if not employee:
        print("❌ Cannot test IdleResource: No employee available")
        return
    
    print("\n📊 Testing IdleResource DAO Methods...")
    
    try:
        # Test create_with_validation
        resource_data = {
            'employee_id': employee.employee_id,
            'resource_type': 'developer',
            'status': 'available',
            'availability_start': timezone.now(),
            'availability_end': timezone.now() + timedelta(days=30),
            'skills': ['Python', 'Django', 'Testing'],
            'experience_years': 5,
            'hourly_rate': 75.00
        }
        
        create_result = IdleResource.create_with_validation(
            resource_data,
            created_by='test_system'
        )
        
        if create_result['success']:
            print("✅ create_with_validation() - Resource created successfully")
            print(f"   Resource ID: {create_result['resource_id']}")
            print(f"   Warnings: {len(create_result['warnings'])}")
            
            resource = create_result['resource']
            
            # Test list_with_filters
            list_result = IdleResource.list_with_filters(
                filters={'status': 'available', 'resource_type': 'developer'},
                page=1,
                page_size=10
            )
            print(f"✅ list_with_filters() - Found {list_result['total_count']} resources")
            
            # Test check_availability
            start_date = timezone.now() + timedelta(days=5)
            end_date = timezone.now() + timedelta(days=15)
            
            availability_result = resource.check_availability(start_date, end_date)
            availability_status = "available" if availability_result['is_available'] else "not available"
            print(f"✅ check_availability() - Resource is {availability_status}")
            print(f"   Conflicts: {len(availability_result['conflicts'])}")
            
            # Test update_with_version_check
            update_data = {
                'experience_years': 6,
                'skills': ['Python', 'Django', 'Testing', 'React'],
                'version': resource.version
            }
            
            update_result = resource.update_with_version_check(
                update_data,
                updated_by='test_system'
            )
            
            if update_result['success']:
                print("✅ update_with_version_check() - Resource updated successfully")
                print(f"   Updated fields: {update_result['updated_fields']}")
                print(f"   New version: {update_result['new_version']}")
            else:
                print(f"❌ update_with_version_check() - Update failed: {update_result['error']}")
            
        else:
            print(f"❌ create_with_validation() - Failed: {create_result['errors']}")
            
    except Exception as e:
        print(f"❌ IdleResource DAO methods failed: {str(e)}")

def test_model_relationships():
    """Test model relationships and properties."""
    print("\n🔗 Testing Model Relationships...")
    
    try:
        # Get existing data
        dept = Department.objects.first()
        employee = Employee.objects.first()
        resource = IdleResource.objects.first()
        
        if dept and employee:
            print(f"✅ Department-Employee relationship: {dept.employees.count()} employees")
        
        if employee and resource:
            print(f"✅ Employee-Resource relationship: Resource type = {resource.resource_type}")
            print(f"✅ Resource department property: {resource.department.department_name if resource.department else 'None'}")
            print(f"✅ Resource availability status: {resource.is_available_now}")
        
        # Test to_dict method
        if resource:
            resource_dict = resource.to_dict()
            print(f"✅ Resource to_dict() method: {len(resource_dict)} fields")
            
    except Exception as e:
        print(f"❌ Relationship testing failed: {str(e)}")

def main():
    """Main test execution."""
    print("🚀 Basic Functionality Test Suite")
    print("=" * 50)
    print("Testing core models and DAO methods without external dependencies")
    print()
    
    # Clean up any existing test data
    try:
        Department.objects.filter(department_name__contains="Test").delete()
        User.objects.filter(username__contains="test").delete()
        Employee.objects.filter(employee_number__contains="123").delete()
    except:
        pass  # Ignore cleanup errors
    
    # Run tests
    dept, user, employee = test_basic_models()
    
    if user:
        test_user_session_dao_methods(user)
    
    if employee:
        test_idle_resource_dao_methods(employee)
    
    test_model_relationships()
    
    print("\n" + "=" * 50)
    print("🎉 Basic functionality test completed!")
    print()
    print("Next steps:")
    print("1. Install factory-boy: pip install factory-boy")
    print("2. Run full test suite: python run_tests.py")
    print("3. Run specific tests: python manage.py test tests/")

if __name__ == "__main__":
    main()