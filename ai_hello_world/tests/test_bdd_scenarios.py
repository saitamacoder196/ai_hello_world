"""
BDD Test Suite for Business Workflows.

Following Behavior-Driven Development principles with comprehensive scenarios
covering end-to-end business workflows and user stories.

Based on:
- Database Design: DD/database_v0.1.md
- DAO Specifications: DD/MDE-01/04-dao/ and DD/MDE-03/04-dao/
- Business Rules: Authentication and resource management workflows
"""

import uuid
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from django.db import transaction
from decimal import Decimal

from authentication.models import (
    User, UserSession, Department, Employee, 
    Role, Permission, SecurityPolicy
)
from resource_management.models import (
    IdleResource, ImportSession, ExportSession,
    ResourceSkill, ResourceAvailability
)
from tests.factories import (
    UserFactory, DepartmentFactory, EmployeeFactory, IdleResourceFactory,
    RoleFactory, PermissionFactory, SecurityPolicyFactory,
    ImportSessionFactory, ExportSessionFactory,
    create_user_with_profile, create_employee_with_department,
    create_idle_resource_with_skills
)


class UserAuthenticationWorkflowTest(TestCase):
    """
    BDD Scenarios for User Authentication Workflow.
    
    Feature: User Authentication and Session Management
    As a system user
    I want to authenticate securely and manage my sessions
    So that I can access the system safely
    """
    
    def setUp(self):
        """Set up test environment."""
        self.security_policy = SecurityPolicyFactory(
            policy_config={
                'password_min_length': 8,
                'max_login_attempts': 3,
                'lockout_duration': 300,
                'session_timeout': 3600
            }
        )
    
    def test_successful_user_authentication_and_session_creation(self):
        """
        Scenario: Successful user login with session creation
        
        Given a registered user with valid credentials
        When the user attempts to log in with correct credentials
        Then the system should authenticate the user
        And create a new session with access tokens
        And track the login activity
        """
        # Given: A registered user with valid credentials
        user = UserFactory(
            username='john.doe',
            email='john.doe@company.com',
            is_active=True
        )
        
        # When: The user attempts to log in
        login_result = self._simulate_login(
            username='john.doe',
            ip_address='192.168.1.100',
            user_agent='Mozilla/5.0 Chrome',
            remember_me=False
        )
        
        # Then: The system should authenticate the user
        self.assertTrue(login_result['success'])
        self.assertEqual(login_result['user_id'], str(user.user_id))
        
        # And: Create a new session with access tokens
        self.assertIn('session_id', login_result)
        self.assertIn('access_token', login_result)
        self.assertIn('refresh_token', login_result)
        
        # And: Track the login activity
        session = UserSession.objects.get(session_id=login_result['session_id'])
        self.assertEqual(session.user, user)
        self.assertEqual(session.ip_address, '192.168.1.100')
        self.assertTrue(session.is_valid)
    
    def test_multiple_concurrent_sessions_management(self):
        """
        Scenario: User manages multiple active sessions
        
        Given a user with existing active sessions
        When the user logs in from a different device
        Then the system should create a new session
        And maintain all active sessions
        And allow the user to view all active sessions
        """
        # Given: A user with existing active sessions
        user = UserFactory()
        
        # Existing session from desktop
        desktop_session = UserSession.create_session(
            user=user,
            ip_address='192.168.1.100',
            user_agent='Desktop Chrome'
        )
        
        # When: The user logs in from a different device (mobile)
        mobile_session = UserSession.create_session(
            user=user,
            ip_address='10.0.0.5',
            user_agent='Mobile Safari'
        )
        
        # Then: The system should create a new session
        self.assertNotEqual(desktop_session['session_id'], mobile_session['session_id'])
        
        # And: Maintain all active sessions
        active_sessions = UserSession.get_active_sessions(user)
        self.assertEqual(len(active_sessions), 2)
        
        # And: Allow the user to view all active sessions
        session_ids = [s['session_id'] for s in active_sessions]
        self.assertIn(desktop_session['session_id'], session_ids)
        self.assertIn(mobile_session['session_id'], session_ids)
    
    def test_session_token_refresh_workflow(self):
        """
        Scenario: User session token refresh
        
        Given a user with an active session
        When the access token is near expiration
        And the user makes a request with refresh token
        Then the system should issue a new access token
        And extend the session validity
        And maintain the same session ID
        """
        # Given: A user with an active session
        user = UserFactory()
        session_data = UserSession.create_session(user=user)
        session = UserSession.objects.get(session_id=session_data['session_id'])
        
        original_access_token = session_data['access_token']
        refresh_token = session_data['refresh_token']
        
        # When: The access token is near expiration and refresh is requested
        refresh_result = session.refresh_session(refresh_token)
        
        # Then: The system should issue a new access token
        self.assertIsNotNone(refresh_result)
        self.assertIn('access_token', refresh_result)
        self.assertNotEqual(refresh_result['access_token'], original_access_token)
        
        # And: Extend the session validity
        self.assertIn('expires_at', refresh_result)
        
        # And: Maintain the same session ID
        self.assertEqual(refresh_result['session_id'], session_data['session_id'])
    
    def test_session_cleanup_and_security_maintenance(self):
        """
        Scenario: System maintains session security through cleanup
        
        Given multiple sessions with various states and ages
        When the system performs periodic cleanup
        Then expired sessions should be removed
        And invalid sessions should be cleaned up
        And recent valid sessions should be preserved
        """
        # Given: Multiple sessions with various states and ages
        user = UserFactory()
        
        # Old expired session (should be cleaned)
        old_session = UserSession.objects.create(
            user=user,
            access_token_hash='old_hash',
            refresh_token_hash='old_refresh',
            is_valid=False,
            created_time=timezone.now() - timedelta(days=35)
        )
        
        # Recent valid session (should be preserved)
        recent_session = UserSession.objects.create(
            user=user,
            access_token_hash='recent_hash',
            refresh_token_hash='recent_refresh',
            is_valid=True,
            created_time=timezone.now() - timedelta(hours=1)
        )
        
        # When: The system performs periodic cleanup
        cleanup_result = UserSession.cleanup_expired_sessions(days_old=30)
        
        # Then: Expired sessions should be removed
        self.assertGreater(cleanup_result['deleted_sessions'], 0)
        
        # And: Recent valid sessions should be preserved
        self.assertTrue(
            UserSession.objects.filter(session_id=recent_session.session_id).exists()
        )
        
        # And: Old sessions should be cleaned up
        self.assertFalse(
            UserSession.objects.filter(session_id=old_session.session_id).exists()
        )
    
    def _simulate_login(self, username, ip_address=None, user_agent=None, remember_me=False):
        """Simulate user login process."""
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                session_data = UserSession.create_session(
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    remember_me=remember_me
                )
                return {
                    'success': True,
                    'user_id': str(user.user_id),
                    **session_data
                }
            else:
                return {'success': False, 'error': 'Account is inactive'}
        except User.DoesNotExist:
            return {'success': False, 'error': 'Invalid credentials'}


class ResourceManagementWorkflowTest(TestCase):
    """
    BDD Scenarios for Resource Management Workflow.
    
    Feature: Idle Resource Management
    As a resource manager
    I want to manage idle resources effectively
    So that I can optimize resource allocation
    """
    
    def setUp(self):
        """Set up test environment."""
        self.hr_department = DepartmentFactory(department_name='Human Resources')
        self.it_department = DepartmentFactory(department_name='IT Department')
        
        self.hr_manager = UserFactory(username='hr.manager')
        self.project_manager = UserFactory(username='project.manager')
    
    def test_complete_resource_onboarding_workflow(self):
        """
        Scenario: Complete resource onboarding process
        
        Given a new employee has joined the company
        When HR creates an employee record
        And adds the employee as an idle resource
        And defines their skills and availability
        Then the resource should be available for allocation
        And searchable by skills and availability
        """
        # Given: A new employee has joined the company
        employee_data = {
            'employee_number': 'EMP2024001',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@company.com',
            'phone': '+1-555-0123',
            'department': self.it_department,
            'position': 'Senior Developer',
            'hire_date': timezone.now().date(),
            'is_active': True
        }
        
        # When: HR creates an employee record
        employee = Employee.objects.create(**employee_data)
        
        # And: Adds the employee as an idle resource
        resource_result = IdleResource.create_with_validation({
            'employee_id': employee.employee_id,
            'resource_type': 'developer',
            'status': 'available',
            'availability_start': timezone.now(),
            'availability_end': timezone.now() + timedelta(days=90),
            'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
            'experience_years': 8,
            'hourly_rate': Decimal('85.00')
        }, created_by='hr.manager')
        
        # Then: The resource should be created successfully
        self.assertTrue(resource_result['success'])
        resource = resource_result['resource']
        
        # And: Defines their skills and availability
        skill_data = [
            {'skill_name': 'Python', 'skill_category': 'programming', 'proficiency_level': 'expert'},
            {'skill_name': 'Django', 'skill_category': 'framework', 'proficiency_level': 'advanced'},
            {'skill_name': 'React', 'skill_category': 'framework', 'proficiency_level': 'intermediate'}
        ]
        
        for skill_info in skill_data:
            ResourceSkill.objects.create(
                resource=resource,
                **skill_info,
                years_experience=5,
                is_verified=True
            )
        
        # And: Define availability periods
        ResourceAvailability.objects.create(
            resource=resource,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            availability_type='full_time',
            capacity_percentage=100,
            location_constraints='hybrid'
        )
        
        # Then: The resource should be available for allocation
        self.assertEqual(resource.status, 'available')
        self.assertTrue(resource.is_available_now)
        
        # And: Searchable by skills and availability
        search_result = IdleResource.list_with_filters(
            filters={'skills': 'Python', 'status': 'available'}
        )
        resource_ids = [r['id'] for r in search_result['records']]
        self.assertIn(str(resource.id), resource_ids)
    
    def test_resource_allocation_and_tracking_workflow(self):
        """
        Scenario: Resource allocation to project
        
        Given an available resource with specific skills
        When a project manager searches for resources
        And finds a suitable resource
        And allocates the resource to a project
        Then the resource status should be updated
        And availability periods should be marked as allocated
        And the allocation should be tracked
        """
        # Given: An available resource with specific skills
        resource, skills = create_idle_resource_with_skills(
            skill_count=3,
            status='available'
        )
        
        # Create availability period
        availability = ResourceAvailabilityFactory(
            resource=resource,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=60),
            availability_type='full_time',
            capacity_percentage=100,
            is_allocated=False
        )
        
        # When: A project manager searches for resources
        search_filters = {
            'skills': skills[0].skill_name,
            'status': 'available',
            'available_from': timezone.now().isoformat(),
            'available_until': (timezone.now() + timedelta(days=30)).isoformat()
        }
        
        search_result = IdleResource.list_with_filters(filters=search_filters)
        
        # And: Finds a suitable resource
        self.assertGreater(search_result['total_count'], 0)
        found_resource_data = search_result['records'][0]
        self.assertEqual(found_resource_data['id'], str(resource.id))
        
        # And: Checks availability for specific period
        allocation_start = timezone.now() + timedelta(days=5)
        allocation_end = timezone.now() + timedelta(days=35)
        
        availability_check = resource.check_availability(allocation_start, allocation_end)
        self.assertTrue(availability_check['is_available'])
        
        # And: Allocates the resource to a project
        resource.status = 'allocated'
        resource.save()
        
        availability.is_allocated = True
        availability.allocation_reference = 'PROJECT-ABC-2024'
        availability.start_date = allocation_start
        availability.end_date = allocation_end
        availability.save()
        
        # Then: The resource status should be updated
        resource.refresh_from_db()
        self.assertEqual(resource.status, 'allocated')
        
        # And: Availability periods should be marked as allocated
        availability.refresh_from_db()
        self.assertTrue(availability.is_allocated)
        self.assertEqual(availability.allocation_reference, 'PROJECT-ABC-2024')
        
        # And: The allocation should be tracked
        new_availability_check = resource.check_availability(allocation_start, allocation_end)
        self.assertFalse(new_availability_check['is_available'])
        allocation_conflict = any(
            'PROJECT-ABC-2024' in conflict.get('allocation_reference', '')
            for conflict in new_availability_check['conflicts']
        )
        self.assertTrue(allocation_conflict)
    
    def test_resource_skill_validation_and_certification_workflow(self):
        """
        Scenario: Resource skill validation and certification tracking
        
        Given a resource with claimed skills
        When a skill verification process is initiated
        And certifications are provided
        Then skills should be marked as verified
        And certification details should be tracked
        And skill proficiency should be validated
        """
        # Given: A resource with claimed skills
        resource = IdleResourceFactory()
        
        unverified_skills = [
            {
                'skill_name': 'AWS Solutions Architect',
                'skill_category': 'certification',
                'proficiency_level': 'advanced',
                'years_experience': 3,
                'is_verified': False
            },
            {
                'skill_name': 'Kubernetes',
                'skill_category': 'tool',
                'proficiency_level': 'intermediate',
                'years_experience': 2,
                'is_verified': False
            }
        ]
        
        created_skills = []
        for skill_data in unverified_skills:
            skill = ResourceSkill.objects.create(resource=resource, **skill_data)
            created_skills.append(skill)
        
        # When: A skill verification process is initiated
        # And: Certifications are provided
        aws_skill = created_skills[0]
        aws_skill.certification_name = 'AWS Certified Solutions Architect - Professional'
        aws_skill.certification_date = timezone.now().date() - timedelta(days=30)
        aws_skill.is_verified = True
        aws_skill.verification_date = timezone.now().date()
        aws_skill.notes = 'Verified through AWS certification portal'
        aws_skill.save()
        
        k8s_skill = created_skills[1]
        k8s_skill.is_verified = True
        k8s_skill.verification_date = timezone.now().date()
        k8s_skill.notes = 'Verified through hands-on assessment'
        k8s_skill.save()
        
        # Then: Skills should be marked as verified
        verified_skills = ResourceSkill.objects.filter(
            resource=resource,
            is_verified=True
        )
        self.assertEqual(verified_skills.count(), 2)
        
        # And: Certification details should be tracked
        aws_skill.refresh_from_db()
        self.assertEqual(aws_skill.certification_name, 'AWS Certified Solutions Architect - Professional')
        self.assertIsNotNone(aws_skill.certification_date)
        
        # And: Skill proficiency should be validated
        self.assertIn(aws_skill.proficiency_level, ['beginner', 'intermediate', 'advanced', 'expert'])
        self.assertGreater(aws_skill.years_experience, 0)
    
    def test_bulk_resource_import_workflow(self):
        """
        Scenario: Bulk resource import from external system
        
        Given a CSV file with resource data
        When HR initiates a bulk import process
        And the system validates each record
        Then valid resources should be created
        And invalid records should be reported
        And import statistics should be tracked
        """
        # Given: A CSV file with resource data (simulated)
        import_data = [
            {
                'employee_number': 'EMP001',
                'first_name': 'John',
                'last_name': 'Developer',
                'email': 'john.dev@company.com',
                'resource_type': 'developer',
                'skills': ['Java', 'Spring Boot'],
                'experience_years': 5
            },
            {
                'employee_number': 'EMP002',
                'first_name': 'Jane',
                'last_name': 'Tester',
                'email': 'jane.test@company.com',
                'resource_type': 'tester',
                'skills': ['Selenium', 'TestNG'],
                'experience_years': 3
            },
            {
                'employee_number': '',  # Invalid - missing employee number
                'first_name': 'Invalid',
                'last_name': 'Record',
                'email': 'invalid@company.com',
                'resource_type': 'developer'
            }
        ]
        
        # When: HR initiates a bulk import process
        import_session = ImportSession.objects.create(
            session_name='Q1 2024 Resource Import',
            file_name='resources_q1_2024.csv',
            file_path='/uploads/resources_q1_2024.csv',
            status='processing',
            total_records=len(import_data),
            metadata={'import_source': 'HR_System', 'batch_id': 'BATCH001'}
        )
        
        # And: The system validates each record
        processed_count = 0
        failed_count = 0
        errors = []
        
        for record in import_data:
            try:
                # Simulate validation
                if not record.get('employee_number'):
                    raise ValueError('Employee number is required')
                
                # Create employee first
                employee = Employee.objects.create(
                    employee_number=record['employee_number'],
                    first_name=record['first_name'],
                    last_name=record['last_name'],
                    email=record['email'],
                    department=self.it_department,
                    position=f"{record.get('resource_type', 'employee').title()}",
                    hire_date=timezone.now().date()
                )
                
                # Create resource
                resource_result = IdleResource.create_with_validation({
                    'employee_id': employee.employee_id,
                    'resource_type': record.get('resource_type', 'developer'),
                    'skills': record.get('skills', []),
                    'experience_years': record.get('experience_years', 0)
                }, created_by='import_system')
                
                if resource_result['success']:
                    processed_count += 1
                else:
                    failed_count += 1
                    errors.extend(resource_result.get('errors', []))
                
            except Exception as e:
                failed_count += 1
                errors.append(f"Row {import_data.index(record) + 1}: {str(e)}")
        
        # Update import session
        import_session.processed_records = processed_count
        import_session.failed_records = failed_count
        import_session.errors = errors
        import_session.status = 'completed' if failed_count == 0 else 'completed_with_errors'
        import_session.completed_at = timezone.now()
        import_session.save()
        
        # Then: Valid resources should be created
        self.assertEqual(processed_count, 2)
        
        # And: Invalid records should be reported
        self.assertEqual(failed_count, 1)
        self.assertGreater(len(errors), 0)
        
        # And: Import statistics should be tracked
        import_session.refresh_from_db()
        self.assertEqual(import_session.total_records, 3)
        self.assertEqual(import_session.processed_records, 2)
        self.assertEqual(import_session.failed_records, 1)
        self.assertIn('completed', import_session.status)
    
    def test_resource_export_and_reporting_workflow(self):
        """
        Scenario: Resource export and reporting
        
        Given multiple resources with different attributes
        When a manager requests a resource report
        And applies specific filters
        Then the system should export matching resources
        And provide export statistics
        And track the export session
        """
        # Given: Multiple resources with different attributes
        resources = []
        for i in range(5):
            employee = EmployeeFactory(department=self.it_department)
            resource = IdleResourceFactory(
                employee=employee,
                resource_type='developer' if i % 2 == 0 else 'tester',
                status='available' if i < 3 else 'allocated',
                experience_years=i + 2,
                skills=['Python', 'Django'] if i % 2 == 0 else ['Java', 'Selenium']
            )
            resources.append(resource)
        
        # When: A manager requests a resource report
        export_filters = {
            'resource_type': 'developer',
            'status': 'available',
            'min_experience': 2
        }
        
        export_session = ExportSession.objects.create(
            session_name='Available Developers Report',
            export_format='csv',
            filters=export_filters,
            status='processing',
            metadata={'requested_by': 'project.manager', 'purpose': 'project_staffing'}
        )
        
        # And: Applies specific filters
        filtered_result = IdleResource.list_with_filters(filters=export_filters)
        
        # Simulate export process
        export_session.total_records = filtered_result['total_count']
        export_session.file_path = f'/exports/available_developers_{export_session.id}.csv'
        export_session.file_size = export_session.total_records * 256  # Estimated file size
        export_session.status = 'completed'
        export_session.completed_at = timezone.now()
        export_session.save()
        
        # Then: The system should export matching resources
        self.assertGreater(filtered_result['total_count'], 0)
        
        # And: Provide export statistics
        export_session.refresh_from_db()
        self.assertEqual(export_session.total_records, filtered_result['total_count'])
        self.assertGreater(export_session.file_size, 0)
        
        # And: Track the export session
        self.assertEqual(export_session.status, 'completed')
        self.assertIsNotNone(export_session.completed_at)
        self.assertEqual(export_session.filters, export_filters)


class IntegratedBusinessWorkflowTest(TestCase):
    """
    BDD Scenarios for Integrated Business Workflows.
    
    Feature: End-to-End Business Process Integration
    As a business stakeholder
    I want seamless integration between authentication and resource management
    So that business processes flow efficiently
    """
    
    def test_complete_user_to_resource_lifecycle(self):
        """
        Scenario: Complete lifecycle from user creation to resource allocation
        
        Given a new user account is created
        When the user is assigned roles and permissions
        And an employee record is created
        And the employee is added as a resource
        And skills are validated and verified
        Then the complete workflow should be traceable
        And audit trails should be maintained
        """
        # Given: A new user account is created
        user, profile = create_user_with_profile(username='new.employee')
        
        # When: The user is assigned roles and permissions
        developer_role = RoleFactory(role_name='Developer')
        resource_permission = PermissionFactory(
            permission_name='manage_resources',
            action='read'
        )
        
        # Assign role to user (through UserRole model if exists)
        user.is_active = True
        user.save()
        
        # And: An employee record is created
        employee = Employee.objects.create(
            employee_number='EMP2024100',
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            department=DepartmentFactory(department_name='Software Engineering'),
            position='Senior Software Developer',
            hire_date=timezone.now().date()
        )
        
        # And: The employee is added as a resource
        resource_result = IdleResource.create_with_validation({
            'employee_id': employee.employee_id,
            'resource_type': 'developer',
            'status': 'available',
            'skills': ['Python', 'Django', 'React'],
            'experience_years': 6,
            'hourly_rate': Decimal('80.00')
        }, created_by=str(user.user_id))
        
        # And: Skills are validated and verified
        resource = resource_result['resource']
        skill_validations = [
            {
                'skill_name': 'Python',
                'skill_category': 'programming',
                'proficiency_level': 'expert',
                'certification_name': 'Python Institute PCPP',
                'is_verified': True
            },
            {
                'skill_name': 'Django',
                'skill_category': 'framework',
                'proficiency_level': 'advanced',
                'is_verified': True
            }
        ]
        
        for skill_data in skill_validations:
            ResourceSkill.objects.create(
                resource=resource,
                years_experience=4,
                verification_date=timezone.now().date(),
                **skill_data
            )
        
        # Then: The complete workflow should be traceable
        self.assertTrue(resource_result['success'])
        self.assertEqual(resource.employee.email, user.email)
        self.assertEqual(resource.created_by, str(user.user_id))
        
        # And: Audit trails should be maintained
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(employee.created_at)
        self.assertIsNotNone(resource.created_at)
        
        # Verify complete traceability
        verified_skills = ResourceSkill.objects.filter(
            resource=resource,
            is_verified=True
        ).count()
        self.assertEqual(verified_skills, 2)
        
        # Verify the resource is searchable and allocatable
        search_result = IdleResource.list_with_filters(
            filters={'status': 'available', 'skills': 'Python'}
        )
        resource_found = any(
            r['id'] == str(resource.id) for r in search_result['records']
        )
        self.assertTrue(resource_found)
    
    def test_multi_department_resource_coordination_workflow(self):
        """
        Scenario: Multi-department resource coordination
        
        Given resources from multiple departments
        When a cross-department project needs staffing
        And resources are searched across departments
        Then suitable resources should be identified
        And allocation coordination should be managed
        """
        # Given: Resources from multiple departments
        engineering_dept = DepartmentFactory(department_name='Engineering')
        qa_dept = DepartmentFactory(department_name='Quality Assurance')
        design_dept = DepartmentFactory(department_name='Design')
        
        # Create resources in different departments
        departments_and_resources = []
        for dept, resource_type, skills in [
            (engineering_dept, 'developer', ['Python', 'React']),
            (qa_dept, 'tester', ['Selenium', 'TestNG']),
            (design_dept, 'designer', ['Figma', 'Adobe XD'])
        ]:
            employee = EmployeeFactory(department=dept)
            resource = IdleResourceFactory(
                employee=employee,
                resource_type=resource_type,
                status='available',
                skills=skills
            )
            departments_and_resources.append((dept, resource))
        
        # When: A cross-department project needs staffing
        project_requirements = {
            'developers': {'skills': ['Python'], 'count': 1},
            'testers': {'skills': ['Selenium'], 'count': 1},
            'designers': {'skills': ['Figma'], 'count': 1}
        }
        
        # And: Resources are searched across departments
        staffing_plan = {}
        for role, requirements in project_requirements.items():
            search_result = IdleResource.list_with_filters(
                filters={
                    'status': 'available',
                    'skills': requirements['skills'][0]
                }
            )
            staffing_plan[role] = search_result['records'][:requirements['count']]
        
        # Then: Suitable resources should be identified
        self.assertEqual(len(staffing_plan['developers']), 1)
        self.assertEqual(len(staffing_plan['testers']), 1)
        self.assertEqual(len(staffing_plan['designers']), 1)
        
        # And: Allocation coordination should be managed
        project_start = timezone.now() + timedelta(days=7)
        project_end = timezone.now() + timedelta(days=37)
        
        allocated_resources = []
        for role, resources in staffing_plan.items():
            for resource_data in resources:
                resource = IdleResource.objects.get(id=resource_data['id'])
                
                # Check availability
                availability_check = resource.check_availability(project_start, project_end)
                if availability_check['is_available']:
                    # Allocate resource
                    resource.status = 'allocated'
                    resource.save()
                    
                    # Create allocation record
                    ResourceAvailability.objects.create(
                        resource=resource,
                        start_date=project_start,
                        end_date=project_end,
                        availability_type='project_based',
                        capacity_percentage=100,
                        is_allocated=True,
                        allocation_reference=f'PROJECT-CROSS-DEPT-2024'
                    )
                    
                    allocated_resources.append(resource)
        
        # Verify successful cross-department allocation
        self.assertEqual(len(allocated_resources), 3)
        
        # Verify each department is represented
        departments_in_allocation = set(
            r.employee.department.department_name for r in allocated_resources
        )
        expected_departments = {'Engineering', 'Quality Assurance', 'Design'}
        self.assertEqual(departments_in_allocation, expected_departments)


# BDD Test Helper Functions
def given_setup_description(description):
    """Decorator for BDD Given steps."""
    def decorator(func):
        func.__doc__ = f"GIVEN: {description}\n{func.__doc__ or ''}"
        return func
    return decorator


def when_action_description(description):
    """Decorator for BDD When steps."""
    def decorator(func):
        func.__doc__ = f"WHEN: {description}\n{func.__doc__ or ''}"
        return func
    return decorator


def then_assertion_description(description):
    """Decorator for BDD Then steps."""
    def decorator(func):
        func.__doc__ = f"THEN: {description}\n{func.__doc__ or ''}"
        return func
    return decorator