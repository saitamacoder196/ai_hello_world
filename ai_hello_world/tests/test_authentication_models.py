"""
TDD Test Suite for Authentication Models.

Following Test-Driven Development principles with comprehensive coverage
of all authentication models and their DAO methods.

Based on:
- Database Design: DD/database_v0.1.md
- DAO Specifications: DD/MDE-01/04-dao/
- Business Rules: Authentication module requirements
"""

import uuid
from datetime import datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import IntegrityError
import hashlib

from authentication.models import (
    Department, Employee, User, Profile, Role, Permission,
    UserRole, RolePermission, UserSession, SecurityPolicy,
    LoginAttempt, PasswordResetToken
)
from tests.factories import (
    DepartmentFactory, EmployeeFactory, UserFactory, ProfileFactory,
    RoleFactory, PermissionFactory, UserSessionFactory, SecurityPolicyFactory,
    create_user_with_profile, create_employee_with_department
)


class DepartmentModelTest(TestCase):
    """
    TDD Test Cases for Department Model.
    
    Tests based on database design requirements:
    - Unique department names
    - Hierarchical structure support
    - Manager assignment capability
    - Audit trail fields
    """
    
    def setUp(self):
        """Set up test data."""
        self.department_data = {
            'department_name': 'Engineering',
            'is_active': True
        }
    
    def test_create_department_with_valid_data(self):
        """Test creating department with valid data."""
        # Given: Valid department data
        department = Department.objects.create(**self.department_data)
        
        # When: Department is created
        saved_department = Department.objects.get(department_id=department.department_id)
        
        # Then: Department should be saved correctly
        self.assertEqual(saved_department.department_name, 'Engineering')
        self.assertTrue(saved_department.is_active)
        self.assertIsNotNone(saved_department.created_at)
        self.assertIsNotNone(saved_department.updated_at)
        self.assertIsInstance(saved_department.department_id, uuid.UUID)
    
    def test_department_name_uniqueness_constraint(self):
        """Test that department names must be unique."""
        # Given: Existing department
        Department.objects.create(**self.department_data)
        
        # When: Creating department with same name
        # Then: Should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Department.objects.create(**self.department_data)
    
    def test_hierarchical_department_structure(self):
        """Test parent-child department relationships."""
        # Given: Parent department
        parent = DepartmentFactory(department_name='Engineering')
        
        # When: Creating child department
        child = DepartmentFactory(
            department_name='Backend Engineering',
            parent_department=parent
        )
        
        # Then: Relationships should be established
        self.assertEqual(child.parent_department, parent)
        self.assertIn(child, parent.child_departments.all())
    
    def test_department_manager_assignment(self):
        """Test manager assignment to department."""
        # Given: User and department
        user = UserFactory()
        department = DepartmentFactory()
        
        # When: Assigning manager
        department.manager = user
        department.save()
        
        # Then: Manager should be assigned
        self.assertEqual(department.manager, user)
        self.assertIn(department, user.managed_departments.all())
    
    def test_department_string_representation(self):
        """Test __str__ method returns department name."""
        # Given: Department
        department = DepartmentFactory(department_name='HR Department')
        
        # When: Converting to string
        # Then: Should return department name
        self.assertEqual(str(department), 'HR Department')


class EmployeeModelTest(TestCase):
    """
    TDD Test Cases for Employee Model.
    
    Tests based on DAO specifications:
    - Unique employee numbers
    - Department relationships
    - Contact information validation
    - Employment status tracking
    """
    
    def setUp(self):
        """Set up test data."""
        self.department = DepartmentFactory()
        self.employee_data = {
            'employee_number': 'EMP001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@company.com',
            'phone': '+1234567890',
            'department': self.department,
            'position': 'Software Developer',
            'hire_date': timezone.now().date(),
            'is_active': True
        }
    
    def test_create_employee_with_valid_data(self):
        """Test creating employee with valid data."""
        # Given: Valid employee data
        employee = Employee.objects.create(**self.employee_data)
        
        # When: Employee is created
        saved_employee = Employee.objects.get(employee_id=employee.employee_id)
        
        # Then: Employee should be saved correctly
        self.assertEqual(saved_employee.employee_number, 'EMP001')
        self.assertEqual(saved_employee.first_name, 'John')
        self.assertEqual(saved_employee.last_name, 'Doe')
        self.assertEqual(saved_employee.email, 'john.doe@company.com')
        self.assertEqual(saved_employee.department, self.department)
        self.assertTrue(saved_employee.is_active)
    
    def test_employee_number_uniqueness_constraint(self):
        """Test that employee numbers must be unique."""
        # Given: Existing employee
        Employee.objects.create(**self.employee_data)
        
        # When: Creating employee with same number
        duplicate_data = self.employee_data.copy()
        duplicate_data['email'] = 'different.email@company.com'
        
        # Then: Should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Employee.objects.create(**duplicate_data)
    
    def test_employee_email_uniqueness_constraint(self):
        """Test that employee emails must be unique."""
        # Given: Existing employee
        Employee.objects.create(**self.employee_data)
        
        # When: Creating employee with same email
        duplicate_data = self.employee_data.copy()
        duplicate_data['employee_number'] = 'EMP002'
        
        # Then: Should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Employee.objects.create(**duplicate_data)
    
    def test_employee_department_relationship(self):
        """Test employee-department relationship."""
        # Given: Employee with department
        employee = EmployeeFactory(department=self.department)
        
        # When: Accessing department
        # Then: Relationship should work both ways
        self.assertEqual(employee.department, self.department)
        self.assertIn(employee, self.department.employees.all())
    
    def test_employee_termination_tracking(self):
        """Test employee termination date tracking."""
        # Given: Active employee
        employee = EmployeeFactory(is_active=True, termination_date=None)
        
        # When: Terminating employee
        termination_date = timezone.now().date()
        employee.termination_date = termination_date
        employee.is_active = False
        employee.save()
        
        # Then: Termination should be tracked
        self.assertFalse(employee.is_active)
        self.assertEqual(employee.termination_date, termination_date)


class UserModelTest(TestCase):
    """
    TDD Test Cases for User Model.
    
    Tests based on DAO specifications:
    - User authentication methods
    - Password security requirements
    - Account status management
    - Audit trail tracking
    """
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@company.com',
            'password_hash': '$2b$12$dummy.hash.for.testing',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
            'is_superuser': False,
            'is_staff': False
        }
    
    def test_create_user_with_valid_data(self):
        """Test creating user with valid data."""
        # Given: Valid user data
        user = User.objects.create(**self.user_data)
        
        # When: User is created
        saved_user = User.objects.get(user_id=user.user_id)
        
        # Then: User should be saved correctly
        self.assertEqual(saved_user.username, 'testuser')
        self.assertEqual(saved_user.email, 'test@company.com')
        self.assertTrue(saved_user.is_active)
        self.assertIsNotNone(saved_user.created_at)
        self.assertIsInstance(saved_user.user_id, uuid.UUID)
    
    def test_username_uniqueness_constraint(self):
        """Test that usernames must be unique."""
        # Given: Existing user
        User.objects.create(**self.user_data)
        
        # When: Creating user with same username
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'different@company.com'
        
        # Then: Should raise IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create(**duplicate_data)
    
    def test_email_uniqueness_constraint(self):
        """Test that emails must be unique."""
        # Given: Existing user
        User.objects.create(**self.user_data)
        
        # When: Creating user with same email
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'differentuser'
        
        # Then: Should raise IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create(**duplicate_data)
    
    def test_user_profile_relationship(self):
        """Test one-to-one user-profile relationship."""
        # Given: User with profile
        user, profile = create_user_with_profile()
        
        # When: Accessing profile
        # Then: Relationship should work both ways
        self.assertEqual(user.profile, profile)
        self.assertEqual(profile.user, user)


class UserSessionModelTest(TestCase):
    """
    TDD Test Cases for UserSession Model and DAO Methods.
    
    Tests based on DAO specifications:
    - Session creation with tokens
    - Session validation
    - Token refresh mechanism
    - Session cleanup operations
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = UserFactory()
        self.session_data = {
            'user': self.user,
            'access_token_hash': 'dummy_hash',
            'refresh_token_hash': 'dummy_refresh_hash',
            'is_valid': True,
            'expires_in': 3600,
            'ip_address': '192.168.1.1',
            'user_agent': 'Test Browser',
            'remember_me': False
        }
    
    def test_create_session_dao_method(self):
        """Test DAO-MDE-01-02-01: Create Session method."""
        # Given: User and session parameters
        session_data = {'test': 'data'}
        
        # When: Creating session using DAO method
        result = UserSession.create_session(
            user=self.user,
            session_data=session_data,
            remember_me=False,
            ip_address='192.168.1.1',
            user_agent='Test Browser'
        )
        
        # Then: Session should be created with tokens
        self.assertIn('session_id', result)
        self.assertIn('access_token', result)
        self.assertIn('refresh_token', result)
        self.assertIn('expires_in', result)
        self.assertEqual(result['user_id'], str(self.user.user_id))
        self.assertFalse(result['remember_me'])
        
        # And: Session should be saved in database
        session = UserSession.objects.get(session_id=result['session_id'])
        self.assertEqual(session.user, self.user)
        self.assertTrue(session.is_valid)
        self.assertEqual(session.session_data, session_data)
    
    def test_create_session_with_remember_me(self):
        """Test session creation with extended expiration."""
        # Given: Remember me option
        # When: Creating session with remember_me=True
        result = UserSession.create_session(
            user=self.user,
            remember_me=True
        )
        
        # Then: Session should have extended expiration
        self.assertTrue(result['remember_me'])
        self.assertEqual(result['expires_in'], 7 * 24 * 3600)  # 7 days
    
    def test_validate_session_dao_method(self):
        """Test DAO-MDE-01-02-02: Validate Session method."""
        # Given: Created session with tokens
        create_result = UserSession.create_session(user=self.user)
        access_token = create_result['access_token']
        
        # When: Validating session
        result = UserSession.validate_session(access_token)
        
        # Then: Session should be validated
        self.assertIsNotNone(result)
        self.assertEqual(result['user_id'], str(self.user.user_id))
        self.assertIn('expires_at', result)
        self.assertIn('last_activity', result)
        
        # And: Session last_activity should be updated
        session = UserSession.objects.get(session_id=result['session_id'])
        self.assertIsNotNone(session.last_activity)
    
    def test_validate_session_with_invalid_token(self):
        """Test session validation with invalid token."""
        # Given: Invalid token
        invalid_token = 'invalid_token'
        
        # When: Validating invalid token
        result = UserSession.validate_session(invalid_token)
        
        # Then: Should return None
        self.assertIsNone(result)
    
    def test_validate_expired_session(self):
        """Test validation of expired session."""
        # Given: Expired session
        session = UserSessionFactory(
            user=self.user,
            expires_in=1,  # 1 second
            created_time=timezone.now() - timedelta(seconds=2)
        )
        
        # When: Validating expired session
        token_hash = hashlib.sha256('test_token'.encode()).hexdigest()
        session.access_token_hash = token_hash
        session.save()
        
        result = UserSession.validate_session('test_token')
        
        # Then: Should return None and mark session invalid
        self.assertIsNone(result)
        session.refresh_from_db()
        self.assertFalse(session.is_valid)
    
    def test_refresh_session_dao_method(self):
        """Test DAO-MDE-01-02-03: Refresh Session method."""
        # Given: Valid session with tokens
        create_result = UserSession.create_session(user=self.user)
        session = UserSession.objects.get(session_id=create_result['session_id'])
        refresh_token = create_result['refresh_token']
        
        # When: Refreshing session
        result = session.refresh_session(refresh_token)
        
        # Then: Should return new access token
        self.assertIsNotNone(result)
        self.assertIn('access_token', result)
        self.assertNotEqual(result['access_token'], create_result['access_token'])
        self.assertEqual(result['refresh_token'], refresh_token)  # Same refresh token
    
    def test_refresh_session_with_invalid_token(self):
        """Test refresh with invalid refresh token."""
        # Given: Session
        session = UserSessionFactory(user=self.user)
        
        # When: Refreshing with invalid token
        result = session.refresh_session('invalid_refresh_token')
        
        # Then: Should return None
        self.assertIsNone(result)
    
    def test_revoke_session_dao_method(self):
        """Test DAO-MDE-01-02-04: Revoke Session method."""
        # Given: Valid session
        session = UserSessionFactory(user=self.user, is_valid=True)
        
        # When: Revoking session
        session.revoke_session()
        
        # Then: Session should be invalidated
        session.refresh_from_db()
        self.assertFalse(session.is_valid)
        self.assertEqual(session.access_token_hash, '')
        self.assertEqual(session.refresh_token_hash, '')
    
    def test_cleanup_expired_sessions_dao_method(self):
        """Test DAO-MDE-01-02-05: Cleanup Expired Sessions method."""
        # Given: Mix of valid and expired sessions
        old_date = timezone.now() - timedelta(days=35)
        
        # Old expired session (should be deleted)
        old_session = UserSessionFactory(
            user=self.user,
            is_valid=False,
            created_time=old_date
        )
        
        # Recent session (should be kept)
        recent_session = UserSessionFactory(
            user=self.user,
            is_valid=True
        )
        
        # When: Cleaning up expired sessions
        result = UserSession.cleanup_expired_sessions(days_old=30)
        
        # Then: Old sessions should be deleted
        self.assertGreaterEqual(result['deleted_sessions'], 1)
        self.assertIn('cleanup_date', result)
        
        # And: Old session should be deleted
        with self.assertRaises(UserSession.DoesNotExist):
            UserSession.objects.get(session_id=old_session.session_id)
        
        # And: Recent session should still exist
        UserSession.objects.get(session_id=recent_session.session_id)
    
    def test_get_active_sessions_dao_method(self):
        """Test DAO-MDE-01-02-06: Get Active Sessions method."""
        # Given: Multiple sessions for user
        valid_session = UserSessionFactory(user=self.user, is_valid=True)
        invalid_session = UserSessionFactory(user=self.user, is_valid=False)
        
        # When: Getting active sessions
        result = UserSession.get_active_sessions(self.user)
        
        # Then: Should return only valid sessions
        self.assertEqual(len(result), 1)
        session_data = result[0]
        self.assertEqual(session_data['session_id'], str(valid_session.session_id))
        self.assertIn('created_time', session_data)
        self.assertIn('expires_at', session_data)
        self.assertIn('ip_address', session_data)
    
    def test_update_session_activity_dao_method(self):
        """Test DAO-MDE-01-02-07: Update Session Activity method."""
        # Given: Session
        session = UserSessionFactory(user=self.user)
        original_activity = session.last_activity
        activity_data = {'page': 'dashboard', 'action': 'view'}
        
        # When: Updating session activity
        session.update_session_activity(activity_data)
        
        # Then: Last activity should be updated
        session.refresh_from_db()
        self.assertGreater(session.last_activity, original_activity)
        self.assertIn('last_activity_data', session.session_data)
        self.assertEqual(session.session_data['last_activity_data'], activity_data)
        self.assertEqual(session.session_data['activity_count'], 1)
    
    def test_session_expiration_property(self):
        """Test session expiration calculation."""
        # Given: Session with specific expiration
        session = UserSessionFactory(
            expires_in=3600,
            created_time=timezone.now() - timedelta(seconds=1800)  # 30 minutes ago
        )
        
        # When: Checking expiration
        # Then: Should not be expired yet
        self.assertFalse(session.is_expired)
        
        # Given: Expired session
        expired_session = UserSessionFactory(
            expires_in=1800,  # 30 minutes
            created_time=timezone.now() - timedelta(seconds=3600)  # 1 hour ago
        )
        
        # When: Checking expiration
        # Then: Should be expired
        self.assertTrue(expired_session.is_expired)


class SecurityPolicyModelTest(TestCase):
    """
    TDD Test Cases for SecurityPolicy Model.
    
    Tests based on security requirements:
    - Policy configuration validation
    - Policy activation/deactivation
    - Password complexity rules
    - Login attempt policies
    """
    
    def setUp(self):
        """Set up test data."""
        self.policy_config = {
            'password_min_length': 8,
            'password_require_uppercase': True,
            'password_require_numbers': True,
            'max_login_attempts': 3,
            'lockout_duration': 300
        }
    
    def test_create_security_policy(self):
        """Test creating security policy with configuration."""
        # Given: Policy configuration
        policy = SecurityPolicy.objects.create(
            policy_name='Default Security Policy',
            policy_config=self.policy_config,
            is_active=True
        )
        
        # When: Policy is created
        saved_policy = SecurityPolicy.objects.get(policy_id=policy.policy_id)
        
        # Then: Policy should be saved with configuration
        self.assertEqual(saved_policy.policy_name, 'Default Security Policy')
        self.assertEqual(saved_policy.policy_config, self.policy_config)
        self.assertTrue(saved_policy.is_active)
    
    def test_policy_configuration_validation(self):
        """Test policy configuration contains required fields."""
        # Given: Policy with configuration
        policy = SecurityPolicyFactory(policy_config=self.policy_config)
        
        # When: Accessing configuration
        config = policy.policy_config
        
        # Then: Should contain all required fields
        self.assertIn('password_min_length', config)
        self.assertIn('max_login_attempts', config)
        self.assertIn('lockout_duration', config)
        self.assertEqual(config['password_min_length'], 8)
        self.assertEqual(config['max_login_attempts'], 3)