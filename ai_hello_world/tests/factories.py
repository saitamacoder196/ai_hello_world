"""
Test factories for creating model instances in tests.

Following Factory Boy pattern for consistent test data generation.
Based on DAO specifications and database design requirements.
"""

import uuid
from datetime import datetime, timedelta
from django.utils import timezone as django_timezone
import factory
from factory.django import DjangoModelFactory
from authentication.models import (
    Department, Employee, User, Profile, Role, Permission, 
    UserRole, RolePermission, UserSession, SecurityPolicy, 
    LoginAttempt, PasswordResetToken
)
from resource_management.models import (
    IdleResource, ImportSession, ExportSession, 
    ResourceSkill, ResourceAvailability
)


# Authentication Model Factories
class DepartmentFactory(DjangoModelFactory):
    """
    Factory for Department model.
    Creates organizational department data for testing.
    """
    class Meta:
        model = Department
    
    department_id = factory.LazyFunction(uuid.uuid4)
    department_name = factory.Sequence(lambda n: f"Department {n}")
    is_active = True
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


class EmployeeFactory(DjangoModelFactory):
    """
    Factory for Employee model.
    Creates employee data following business rules.
    """
    class Meta:
        model = Employee
    
    employee_id = factory.LazyFunction(uuid.uuid4)
    employee_number = factory.Sequence(lambda n: f"EMP{n:04d}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@company.com")
    phone = factory.Faker('phone_number')
    department = factory.SubFactory(DepartmentFactory)
    position = factory.Faker('job')
    hire_date = factory.LazyFunction(lambda: django_timezone.now().date() - timedelta(days=365))
    is_active = True
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


class UserFactory(DjangoModelFactory):
    """
    Factory for User model.
    Creates user accounts for authentication testing.
    """
    class Meta:
        model = User
    
    user_id = factory.LazyFunction(uuid.uuid4)
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@company.com")
    password_hash = factory.LazyFunction(lambda: "$2b$12$dummy.hash.for.testing.purposes")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_superuser = False
    is_staff = False
    last_login = None
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


class ProfileFactory(DjangoModelFactory):
    """
    Factory for Profile model.
    Creates user profile data linked to users.
    """
    class Meta:
        model = Profile
    
    profile_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    display_name = factory.LazyAttribute(lambda obj: f"{obj.user.first_name} {obj.user.last_name}")
    bio = factory.Faker('text', max_nb_chars=200)
    avatar_url = factory.Faker('image_url')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    timezone = 'UTC'
    language = 'en'
    theme = 'light'
    created_at = factory.LazyFunction(lambda: django_timezone.now())
    updated_at = factory.LazyFunction(lambda: django_timezone.now())


class RoleFactory(DjangoModelFactory):
    """
    Factory for Role model.
    Creates roles for RBAC testing.
    """
    class Meta:
        model = Role
    
    role_id = factory.LazyFunction(uuid.uuid4)
    role_name = factory.Sequence(lambda n: f"Role {n}")
    role_description = factory.Faker('text', max_nb_chars=100)
    is_active = True
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


class PermissionFactory(DjangoModelFactory):
    """
    Factory for Permission model.
    Creates permissions for RBAC testing.
    """
    class Meta:
        model = Permission
    
    permission_id = factory.LazyFunction(uuid.uuid4)
    permission_name = factory.Sequence(lambda n: f"permission_{n}")
    permission_description = factory.Faker('text', max_nb_chars=100)
    resource_type = factory.Faker('word')
    action = factory.Iterator(['create', 'read', 'update', 'delete'])
    is_active = True
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


class UserSessionFactory(DjangoModelFactory):
    """
    Factory for UserSession model.
    Creates user sessions for authentication testing.
    """
    class Meta:
        model = UserSession
    
    session_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    access_token_hash = factory.LazyFunction(lambda: "dummy_access_token_hash_for_testing")
    refresh_token_hash = factory.LazyFunction(lambda: "dummy_refresh_token_hash_for_testing")
    is_valid = True
    expires_in = 3600  # 1 hour
    created_time = factory.LazyFunction(django_timezone.now)
    last_activity = factory.LazyFunction(django_timezone.now)
    ip_address = factory.Faker('ipv4')
    user_agent = factory.Faker('user_agent')
    remember_me = False
    session_data = factory.Dict({})


class SecurityPolicyFactory(DjangoModelFactory):
    """
    Factory for SecurityPolicy model.
    Creates security policies for testing.
    """
    class Meta:
        model = SecurityPolicy
    
    policy_id = factory.LazyFunction(uuid.uuid4)
    policy_name = factory.Sequence(lambda n: f"Security Policy {n}")
    policy_config = factory.Dict({
        'password_min_length': 8,
        'password_require_uppercase': True,
        'password_require_numbers': True,
        'max_login_attempts': 3,
        'lockout_duration': 300
    })
    is_active = True
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


# Resource Management Model Factories
class IdleResourceFactory(DjangoModelFactory):
    """
    Factory for IdleResource model.
    Creates idle resource data for testing.
    """
    class Meta:
        model = IdleResource
    
    employee = factory.SubFactory(EmployeeFactory)
    resource_type = factory.Iterator(['developer', 'tester', 'analyst', 'designer'])
    status = factory.Iterator(['available', 'allocated', 'unavailable'])
    availability_start = factory.LazyFunction(django_timezone.now)
    availability_end = factory.LazyFunction(lambda: django_timezone.now() + timedelta(days=30))
    skills = factory.List(['Python', 'Django', 'PostgreSQL'])
    experience_years = factory.Faker('random_int', min=1, max=10)
    hourly_rate = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    created_by = 'test_user'
    created_at = factory.LazyFunction(django_timezone.now)
    updated_at = factory.LazyFunction(django_timezone.now)


class ImportSessionFactory(DjangoModelFactory):
    """
    Factory for ImportSession model.
    Creates import session data for testing.
    """
    class Meta:
        model = ImportSession
    
    session_name = factory.Sequence(lambda n: f"Import Session {n}")
    file_name = factory.LazyAttribute(lambda obj: f"{obj.session_name.lower().replace(' ', '_')}.csv")
    file_path = factory.LazyAttribute(lambda obj: f"/uploads/{obj.file_name}")
    status = factory.Iterator(['pending', 'processing', 'completed', 'failed'])
    total_records = factory.Faker('random_int', min=10, max=1000)
    processed_records = 0
    failed_records = 0
    errors = factory.List([])
    metadata = factory.Dict({'source': 'test'})
    created_by = 'test_user'
    created_at = factory.LazyFunction(django_timezone.now)


class ExportSessionFactory(DjangoModelFactory):
    """
    Factory for ExportSession model.
    Creates export session data for testing.
    """
    class Meta:
        model = ExportSession
    
    session_name = factory.Sequence(lambda n: f"Export Session {n}")
    export_format = factory.Iterator(['csv', 'excel', 'json', 'pdf'])
    filters = factory.Dict({'status': 'available'})
    status = factory.Iterator(['pending', 'processing', 'completed', 'failed'])
    file_path = factory.LazyAttribute(lambda obj: f"/exports/{obj.session_name.lower().replace(' ', '_')}.{obj.export_format}")
    total_records = factory.Faker('random_int', min=1, max=500)
    file_size = factory.Faker('random_int', min=1024, max=1048576)  # 1KB to 1MB
    metadata = factory.Dict({'generated_by': 'test'})
    created_by = 'test_user'
    created_at = factory.LazyFunction(django_timezone.now)


class ResourceSkillFactory(DjangoModelFactory):
    """
    Factory for ResourceSkill model.
    Creates resource skill data for testing.
    """
    class Meta:
        model = ResourceSkill
    
    resource = factory.SubFactory(IdleResourceFactory)
    skill_name = factory.Iterator(['Python', 'Java', 'JavaScript', 'React', 'Django', 'PostgreSQL'])
    skill_category = factory.Iterator(['programming', 'framework', 'database', 'tool'])
    proficiency_level = factory.Iterator(['beginner', 'intermediate', 'advanced', 'expert'])
    years_experience = factory.Faker('random_int', min=1, max=8)
    certification_name = factory.Maybe(
        'is_verified',
        yes_declaration=factory.Faker('word'),
        no_declaration=''
    )
    is_verified = factory.Faker('boolean', chance_of_getting_true=30)
    notes = factory.Faker('text', max_nb_chars=100)
    created_by = 'test_user'
    created_at = factory.LazyFunction(django_timezone.now)


class ResourceAvailabilityFactory(DjangoModelFactory):
    """
    Factory for ResourceAvailability model.
    Creates resource availability data for testing.
    """
    class Meta:
        model = ResourceAvailability
    
    resource = factory.SubFactory(IdleResourceFactory)
    start_date = factory.LazyFunction(django_timezone.now)
    end_date = factory.LazyFunction(lambda: django_timezone.now() + timedelta(days=14))
    availability_type = factory.Iterator(['full_time', 'part_time', 'on_call', 'consulting'])
    capacity_percentage = factory.Faker('random_int', min=25, max=100)
    hourly_commitment = factory.Maybe(
        'availability_type',
        yes_declaration=factory.Faker('random_int', min=20, max=40),
        no_declaration=None
    )
    location_constraints = factory.Iterator(['remote', 'onsite', 'hybrid', 'flexible'])
    is_recurring = factory.Faker('boolean', chance_of_getting_true=20)
    recurrence_pattern = factory.Dict({})
    notes = factory.Faker('text', max_nb_chars=50)
    is_allocated = False
    allocation_reference = ''
    created_by = 'test_user'
    created_at = factory.LazyFunction(django_timezone.now)


# Utility Factory Functions
def create_user_with_profile(username=None, **kwargs):
    """
    Create a user with associated profile.
    Utility function for tests requiring complete user setup.
    """
    user = UserFactory(username=username, **kwargs)
    profile = ProfileFactory(user=user)
    return user, profile


def create_employee_with_department(department_name=None, **kwargs):
    """
    Create an employee with department.
    Utility function for tests requiring organizational structure.
    """
    department = DepartmentFactory(department_name=department_name)
    employee = EmployeeFactory(department=department, **kwargs)
    return employee, department


def create_idle_resource_with_skills(skill_count=3, **kwargs):
    """
    Create an idle resource with multiple skills.
    Utility function for tests requiring skill validation.
    """
    resource = IdleResourceFactory(**kwargs)
    skills = []
    for _ in range(skill_count):
        skill = ResourceSkillFactory(resource=resource)
        skills.append(skill)
    return resource, skills


def create_user_session_with_tokens():
    """
    Create a user session with realistic token data.
    Utility function for authentication tests.
    """
    session = UserSessionFactory()
    # Simulate real token creation
    tokens = {
        'access_token': f"access_token_{session.session_id}",
        'refresh_token': f"refresh_token_{session.session_id}"
    }
    return session, tokens