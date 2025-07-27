"""
TDD Test Suite for Resource Management Models.

Following Test-Driven Development principles with comprehensive coverage
of all resource management models and their DAO methods.

Based on:
- Database Design: DD/database_v0.1.md
- DAO Specifications: DD/MDE-03/04-dao/
- Business Rules: Resource management module requirements
"""

import uuid
from datetime import datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import IntegrityError
from decimal import Decimal

from authentication.models import Employee, Department
from resource_management.models import (
    IdleResource, ImportSession, ExportSession,
    ResourceSkill, ResourceAvailability
)
from tests.factories import (
    DepartmentFactory, EmployeeFactory, IdleResourceFactory,
    ImportSessionFactory, ExportSessionFactory, ResourceSkillFactory,
    ResourceAvailabilityFactory, create_employee_with_department,
    create_idle_resource_with_skills
)


class IdleResourceModelTest(TestCase):
    """
    TDD Test Cases for IdleResource Model and DAO Methods.
    
    Tests based on DAO specifications:
    - Resource CRUD operations with validation
    - Business rule enforcement
    - Availability checking
    - Dynamic filtering and pagination
    """
    
    def setUp(self):
        """Set up test data."""
        self.employee, self.department = create_employee_with_department('Engineering')
        self.resource_data = {
            'employee': self.employee,
            'resource_type': 'developer',
            'status': 'available',
            'availability_start': timezone.now(),
            'availability_end': timezone.now() + timedelta(days=30),
            'skills': ['Python', 'Django', 'PostgreSQL'],
            'experience_years': 5,
            'hourly_rate': Decimal('75.00')
        }
    
    def test_create_idle_resource_with_valid_data(self):
        """Test creating idle resource with valid data."""
        # Given: Valid resource data
        resource = IdleResource.objects.create(**self.resource_data)
        
        # When: Resource is created
        saved_resource = IdleResource.objects.get(id=resource.id)
        
        # Then: Resource should be saved correctly
        self.assertEqual(saved_resource.employee, self.employee)
        self.assertEqual(saved_resource.resource_type, 'developer')
        self.assertEqual(saved_resource.status, 'available')
        self.assertEqual(saved_resource.skills, ['Python', 'Django', 'PostgreSQL'])
        self.assertEqual(saved_resource.experience_years, 5)
        self.assertEqual(saved_resource.hourly_rate, Decimal('75.00'))
    
    def test_resource_type_choices_validation(self):
        """Test resource type must be from valid choices."""
        # Given: Invalid resource type
        self.resource_data['resource_type'] = 'invalid_type'
        
        # When: Creating resource with invalid type
        resource = IdleResource(**self.resource_data)
        
        # Then: Should raise ValidationError on full_clean
        with self.assertRaises(ValidationError):
            resource.full_clean()
    
    def test_status_choices_validation(self):
        """Test status must be from valid choices."""
        # Given: Invalid status
        self.resource_data['status'] = 'invalid_status'
        
        # When: Creating resource with invalid status
        resource = IdleResource(**self.resource_data)
        
        # Then: Should raise ValidationError on full_clean
        with self.assertRaises(ValidationError):
            resource.full_clean()
    
    def test_availability_date_range_validation(self):
        """Test availability start must be before end date."""
        # Given: Invalid date range
        self.resource_data['availability_start'] = timezone.now() + timedelta(days=30)
        self.resource_data['availability_end'] = timezone.now()
        
        # When: Creating resource with invalid dates
        resource = IdleResource(**self.resource_data)
        
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            resource.clean()
    
    def test_negative_hourly_rate_validation(self):
        """Test hourly rate cannot be negative."""
        # Given: Negative hourly rate
        self.resource_data['hourly_rate'] = Decimal('-10.00')
        
        # When: Creating resource with negative rate
        resource = IdleResource(**self.resource_data)
        
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            resource.clean()
    
    def test_negative_experience_years_validation(self):
        """Test experience years cannot be negative."""
        # Given: Negative experience years
        self.resource_data['experience_years'] = -1
        
        # When: Creating resource with negative experience
        resource = IdleResource(**self.resource_data)
        
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            resource.clean()
    
    def test_is_available_now_property(self):
        """Test is_available_now property logic."""
        # Given: Available resource within date range
        resource = IdleResourceFactory(
            status='available',
            availability_start=timezone.now() - timedelta(days=1),
            availability_end=timezone.now() + timedelta(days=1)
        )
        
        # When: Checking availability
        # Then: Should be available
        self.assertTrue(resource.is_available_now)
        
        # Given: Resource with non-available status
        resource.status = 'allocated'
        
        # When: Checking availability
        # Then: Should not be available
        self.assertFalse(resource.is_available_now)
    
    def test_department_property(self):
        """Test department property through employee relationship."""
        # Given: Resource with employee in department
        resource = IdleResourceFactory(employee=self.employee)
        
        # When: Accessing department
        # Then: Should return employee's department
        self.assertEqual(resource.department, self.department)
    
    def test_to_dict_method(self):
        """Test to_dict method for API responses."""
        # Given: Resource
        resource = IdleResourceFactory(employee=self.employee)
        
        # When: Converting to dictionary
        result = resource.to_dict()
        
        # Then: Should contain all required fields
        self.assertIn('id', result)
        self.assertIn('employee_name', result)
        self.assertIn('employee_id', result)
        self.assertIn('department_id', result)
        self.assertIn('resource_type', result)
        self.assertIn('status', result)
        self.assertIn('skills', result)
        self.assertIn('version', result)
        
        # And: Should format data correctly
        self.assertEqual(result['id'], str(resource.id))
        self.assertIsInstance(result['skills'], list)


class IdleResourceDAOMethodsTest(TestCase):
    """
    TDD Test Cases for IdleResource DAO Methods.
    
    Tests based on DAO specifications:
    - DAO-MDE-03-01-01: Create with Validation
    - DAO-MDE-03-01-02: Update with Version Check
    - DAO-MDE-03-01-03: List with Filters
    - DAO-MDE-03-01-04: Check Availability
    """
    
    def setUp(self):
        """Set up test data."""
        self.employee, self.department = create_employee_with_department('Engineering')
    
    def test_create_with_validation_dao_method(self):
        """Test DAO-MDE-03-01-01: Create with Validation method."""
        # Given: Valid resource data
        resource_data = {
            'employee_id': self.employee.employee_id,
            'resource_type': 'developer',
            'status': 'available',
            'availability_start': timezone.now(),
            'availability_end': timezone.now() + timedelta(days=30),
            'skills': ['Python', 'Django'],
            'experience_years': 3,
            'hourly_rate': Decimal('65.00')
        }
        
        # When: Creating resource with validation
        result = IdleResource.create_with_validation(resource_data, created_by='test_user')
        
        # Then: Should create resource successfully
        self.assertTrue(result['success'])
        self.assertIn('resource', result)
        self.assertIn('resource_id', result)
        self.assertEqual(result['warnings'], [])
        
        # And: Resource should be saved in database
        resource = IdleResource.objects.get(id=result['resource_id'])
        self.assertEqual(resource.employee, self.employee)
        self.assertEqual(resource.resource_type, 'developer')
        self.assertEqual(resource.created_by, 'test_user')
    
    def test_create_with_validation_employee_not_found(self):
        """Test create with validation when employee doesn't exist."""
        # Given: Invalid employee ID
        resource_data = {
            'employee_id': uuid.uuid4(),  # Non-existent employee
            'resource_type': 'developer'
        }
        
        # When: Creating resource with invalid employee
        result = IdleResource.create_with_validation(resource_data)
        
        # Then: Should return error
        self.assertFalse(result['success'])
        self.assertIn('errors', result)
        self.assertTrue(any('not found' in error for error in result['errors']))
    
    def test_create_with_validation_duplicate_employee(self):
        """Test create with validation when employee already has active resource."""
        # Given: Employee with existing active resource
        IdleResourceFactory(employee=self.employee, status='available')
        
        resource_data = {
            'employee_id': self.employee.employee_id,
            'resource_type': 'tester'
        }
        
        # When: Creating another resource for same employee
        result = IdleResource.create_with_validation(resource_data)
        
        # Then: Should create but include warning
        self.assertTrue(result['success'])
        self.assertTrue(any('already has an active resource' in warning for warning in result['warnings']))
    
    def test_create_with_validation_invalid_date_range(self):
        """Test create with validation for invalid date range."""
        # Given: Invalid date range
        resource_data = {
            'employee_id': self.employee.employee_id,
            'availability_start': timezone.now() + timedelta(days=30),
            'availability_end': timezone.now()  # End before start
        }
        
        # When: Creating resource with invalid dates
        result = IdleResource.create_with_validation(resource_data)
        
        # Then: Should return error
        self.assertFalse(result['success'])
        self.assertTrue(any('start must be before end' in error for error in result['errors']))
    
    def test_create_with_validation_invalid_skills_format(self):
        """Test create with validation for invalid skills format."""
        # Given: Invalid skills format
        resource_data = {
            'employee_id': self.employee.employee_id,
            'skills': 'not_a_list'  # Should be list
        }
        
        # When: Creating resource with invalid skills
        result = IdleResource.create_with_validation(resource_data)
        
        # Then: Should return error
        self.assertFalse(result['success'])
        self.assertTrue(any('must be a list' in error for error in result['errors']))
    
    def test_update_with_version_check_dao_method(self):
        """Test DAO-MDE-03-01-02: Update with Version Check method."""
        # Given: Existing resource
        resource = IdleResourceFactory(employee=self.employee)
        original_version = resource.version
        
        update_data = {
            'resource_type': 'analyst',
            'experience_years': 7,
            'version': original_version
        }
        
        # When: Updating resource with version check
        result = resource.update_with_version_check(update_data, updated_by='test_user')
        
        # Then: Should update successfully
        self.assertTrue(result['success'])
        self.assertIn('updated_fields', result)
        self.assertIn('new_version', result)
        self.assertGreater(result['new_version'], original_version)
        
        # And: Resource should be updated in database
        resource.refresh_from_db()
        self.assertEqual(resource.resource_type, 'analyst')
        self.assertEqual(resource.experience_years, 7)
        self.assertEqual(resource.updated_by, 'test_user')
    
    def test_update_with_version_check_stale_version(self):
        """Test update with version check for stale version."""
        # Given: Resource with specific version
        resource = IdleResourceFactory(employee=self.employee)
        
        update_data = {
            'resource_type': 'analyst',
            'version': resource.version - 1  # Stale version
        }
        
        # When: Updating with stale version
        result = resource.update_with_version_check(update_data)
        
        # Then: Should return version conflict error
        self.assertFalse(result['success'])
        self.assertIn('modified by another user', result['error'])
        self.assertIn('current_version', result)
        self.assertIn('provided_version', result)
    
    def test_update_with_version_check_validation_error(self):
        """Test update with version check when validation fails."""
        # Given: Resource
        resource = IdleResourceFactory(employee=self.employee)
        
        update_data = {
            'experience_years': -5,  # Invalid negative value
            'version': resource.version
        }
        
        # When: Updating with invalid data
        result = resource.update_with_version_check(update_data)
        
        # Then: Should return validation error
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('validation_errors', result)
    
    def test_list_with_filters_dao_method(self):
        """Test DAO-MDE-03-01-03: List with Filters method."""
        # Given: Multiple resources with different attributes
        resource1 = IdleResourceFactory(
            resource_type='developer',
            status='available',
            experience_years=3,
            skills=['Python', 'Django']
        )
        resource2 = IdleResourceFactory(
            resource_type='tester',
            status='allocated',
            experience_years=5,
            skills=['Selenium', 'Java']
        )
        
        # When: Listing resources without filters
        result = IdleResource.list_with_filters()
        
        # Then: Should return all resources
        self.assertGreaterEqual(result['total_count'], 2)
        self.assertIn('records', result)
        self.assertIn('page_info', result)
        
        # When: Filtering by resource type
        result = IdleResource.list_with_filters(filters={'resource_type': 'developer'})
        
        # Then: Should return only developers
        self.assertEqual(result['total_count'], 1)
        self.assertEqual(result['records'][0]['resource_type'], 'developer')
    
    def test_list_with_filters_status_filter(self):
        """Test list with filters for status filtering."""
        # Given: Resources with different statuses
        IdleResourceFactory(status='available')
        IdleResourceFactory(status='allocated')
        
        # When: Filtering by available status
        result = IdleResource.list_with_filters(filters={'status': 'available'})
        
        # Then: Should return only available resources
        available_count = len([r for r in result['records'] if r['status'] == 'available'])
        self.assertEqual(available_count, result['total_count'])
    
    def test_list_with_filters_skills_filter(self):
        """Test list with filters for skills filtering."""
        # Given: Resources with different skills
        IdleResourceFactory(skills=['Python', 'Django'])
        IdleResourceFactory(skills=['Java', 'Spring'])
        
        # When: Filtering by Python skill
        result = IdleResource.list_with_filters(filters={'skills': 'Python'})
        
        # Then: Should return resources with Python skill
        self.assertGreater(result['total_count'], 0)
        python_resources = [r for r in result['records'] if 'Python' in r.get('skills', [])]
        self.assertEqual(len(python_resources), result['total_count'])
    
    def test_list_with_filters_experience_filter(self):
        """Test list with filters for minimum experience."""
        # Given: Resources with different experience levels
        IdleResourceFactory(experience_years=2)
        IdleResourceFactory(experience_years=6)
        
        # When: Filtering by minimum experience
        result = IdleResource.list_with_filters(filters={'min_experience': 5})
        
        # Then: Should return only experienced resources
        experienced_count = len([r for r in result['records'] if r['experience_years'] >= 5])
        self.assertEqual(experienced_count, result['total_count'])
    
    def test_list_with_filters_pagination(self):
        """Test list with filters pagination."""
        # Given: Multiple resources
        for i in range(15):
            IdleResourceFactory()
        
        # When: Requesting first page with page size 5
        result = IdleResource.list_with_filters(page=1, page_size=5)
        
        # Then: Should return paginated results
        self.assertEqual(len(result['records']), 5)
        self.assertEqual(result['page_info']['current_page'], 1)
        self.assertEqual(result['page_info']['page_size'], 5)
        self.assertGreaterEqual(result['page_info']['total_pages'], 3)
    
    def test_list_with_filters_sorting(self):
        """Test list with filters sorting."""
        # Given: Resources with different creation times
        old_resource = IdleResourceFactory()
        new_resource = IdleResourceFactory()
        
        # When: Sorting by creation date ascending
        result = IdleResource.list_with_filters(
            sort_by='created_at',
            sort_order='asc'
        )
        
        # Then: Should return resources in ascending order
        first_record = result['records'][0]
        self.assertEqual(first_record['id'], str(old_resource.id))
    
    def test_check_availability_dao_method(self):
        """Test DAO-MDE-03-01-04: Check Availability method."""
        # Given: Available resource
        resource = IdleResourceFactory(
            status='available',
            availability_start=timezone.now() - timedelta(days=1),
            availability_end=timezone.now() + timedelta(days=30)
        )
        
        start_date = timezone.now() + timedelta(days=5)
        end_date = timezone.now() + timedelta(days=10)
        
        # When: Checking availability
        result = resource.check_availability(start_date, end_date)
        
        # Then: Should be available
        self.assertTrue(result['is_available'])
        self.assertEqual(len(result['conflicts']), 0)
        self.assertIn('availability_window', result)
    
    def test_check_availability_with_unavailable_status(self):
        """Test check availability for resource with unavailable status."""
        # Given: Unavailable resource
        resource = IdleResourceFactory(status='allocated')
        
        start_date = timezone.now()
        end_date = timezone.now() + timedelta(days=5)
        
        # When: Checking availability
        result = resource.check_availability(start_date, end_date)
        
        # Then: Should not be available
        self.assertFalse(result['is_available'])
        self.assertIn('Resource status is allocated', result['reason'])
    
    def test_check_availability_outside_window(self):
        """Test check availability outside availability window."""
        # Given: Resource with specific availability window
        resource = IdleResourceFactory(
            status='available',
            availability_start=timezone.now() + timedelta(days=10),
            availability_end=timezone.now() + timedelta(days=20)
        )
        
        # When: Checking availability before window
        start_date = timezone.now()
        end_date = timezone.now() + timedelta(days=5)
        
        result = resource.check_availability(start_date, end_date)
        
        # Then: Should have conflicts
        self.assertFalse(result['is_available'])
        self.assertGreater(len(result['conflicts']), 0)
        self.assertTrue(any('not available before' in conflict['message'] for conflict in result['conflicts']))
    
    def test_check_availability_with_allocation_conflicts(self):
        """Test check availability with existing allocations."""
        # Given: Resource with allocated period
        resource = IdleResourceFactory(status='available')
        
        # Allocated period
        ResourceAvailabilityFactory(
            resource=resource,
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=10),
            is_allocated=True,
            allocation_reference='PROJECT-123'
        )
        
        # When: Checking availability during allocated period
        start_date = timezone.now() + timedelta(days=7)
        end_date = timezone.now() + timedelta(days=12)
        
        result = resource.check_availability(start_date, end_date)
        
        # Then: Should have allocation conflicts
        self.assertFalse(result['is_available'])
        conflict_found = any(
            'allocation_conflict' in conflict['type'] and 
            'PROJECT-123' in conflict.get('allocation_reference', '')
            for conflict in result['conflicts']
        )
        self.assertTrue(conflict_found)


class ImportSessionModelTest(TestCase):
    """
    TDD Test Cases for ImportSession Model.
    
    Tests based on import/export requirements:
    - Session tracking for import operations
    - Status management and error handling
    - File processing statistics
    """
    
    def test_create_import_session(self):
        """Test creating import session with valid data."""
        # Given: Import session data
        session = ImportSession.objects.create(
            session_name='Test Import',
            file_name='resources.csv',
            file_path='/uploads/resources.csv',
            status='pending',
            total_records=100
        )
        
        # When: Session is created
        saved_session = ImportSession.objects.get(id=session.id)
        
        # Then: Session should be saved correctly
        self.assertEqual(saved_session.session_name, 'Test Import')
        self.assertEqual(saved_session.file_name, 'resources.csv')
        self.assertEqual(saved_session.status, 'pending')
        self.assertEqual(saved_session.total_records, 100)
        self.assertEqual(saved_session.processed_records, 0)
        self.assertEqual(saved_session.failed_records, 0)
    
    def test_import_session_status_choices(self):
        """Test import session status validation."""
        # Given: Invalid status
        session = ImportSession(
            session_name='Test',
            file_name='test.csv',
            status='invalid_status'
        )
        
        # When: Validating session
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            session.full_clean()
    
    def test_import_session_progress_tracking(self):
        """Test import session progress tracking."""
        # Given: Import session
        session = ImportSessionFactory(
            total_records=100,
            processed_records=75,
            failed_records=5
        )
        
        # When: Calculating progress
        processed_percentage = (session.processed_records / session.total_records) * 100
        
        # Then: Should track progress correctly
        self.assertEqual(processed_percentage, 75.0)
        self.assertEqual(session.failed_records, 5)


class ExportSessionModelTest(TestCase):
    """
    TDD Test Cases for ExportSession Model.
    
    Tests based on export requirements:
    - Session tracking for export operations
    - Format validation
    - File generation statistics
    """
    
    def test_create_export_session(self):
        """Test creating export session with valid data."""
        # Given: Export session data
        session = ExportSession.objects.create(
            session_name='Resource Export',
            export_format='csv',
            filters={'status': 'available'},
            status='pending'
        )
        
        # When: Session is created
        saved_session = ExportSession.objects.get(id=session.id)
        
        # Then: Session should be saved correctly
        self.assertEqual(saved_session.session_name, 'Resource Export')
        self.assertEqual(saved_session.export_format, 'csv')
        self.assertEqual(saved_session.filters, {'status': 'available'})
        self.assertEqual(saved_session.status, 'pending')
    
    def test_export_format_choices(self):
        """Test export format validation."""
        # Given: Invalid format
        session = ExportSession(
            session_name='Test',
            export_format='invalid_format'
        )
        
        # When: Validating session
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            session.full_clean()


class ResourceSkillModelTest(TestCase):
    """
    TDD Test Cases for ResourceSkill Model.
    
    Tests based on skill management requirements:
    - Skill categorization and proficiency tracking
    - Certification management
    - Skill verification process
    """
    
    def setUp(self):
        """Set up test data."""
        self.resource = IdleResourceFactory()
    
    def test_create_resource_skill(self):
        """Test creating resource skill with valid data."""
        # Given: Skill data
        skill = ResourceSkill.objects.create(
            resource=self.resource,
            skill_name='Python',
            skill_category='programming',
            proficiency_level='advanced',
            years_experience=5,
            certification_name='Python Institute PCAP',
            is_verified=True
        )
        
        # When: Skill is created
        saved_skill = ResourceSkill.objects.get(id=skill.id)
        
        # Then: Skill should be saved correctly
        self.assertEqual(saved_skill.resource, self.resource)
        self.assertEqual(saved_skill.skill_name, 'Python')
        self.assertEqual(saved_skill.skill_category, 'programming')
        self.assertEqual(saved_skill.proficiency_level, 'advanced')
        self.assertEqual(saved_skill.years_experience, 5)
        self.assertTrue(saved_skill.is_verified)
    
    def test_resource_skill_unique_constraint(self):
        """Test resource-skill combination uniqueness."""
        # Given: Existing skill
        ResourceSkillFactory(resource=self.resource, skill_name='Python')
        
        # When: Creating duplicate skill
        # Then: Should raise IntegrityError
        with self.assertRaises(IntegrityError):
            ResourceSkillFactory(resource=self.resource, skill_name='Python')
    
    def test_skill_category_choices(self):
        """Test skill category validation."""
        # Given: Invalid category
        skill = ResourceSkill(
            resource=self.resource,
            skill_name='Test',
            skill_category='invalid_category'
        )
        
        # When: Validating skill
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            skill.full_clean()
    
    def test_proficiency_level_choices(self):
        """Test proficiency level validation."""
        # Given: Invalid proficiency level
        skill = ResourceSkill(
            resource=self.resource,
            skill_name='Test',
            proficiency_level='invalid_level'
        )
        
        # When: Validating skill
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            skill.full_clean()


class ResourceAvailabilityModelTest(TestCase):
    """
    TDD Test Cases for ResourceAvailability Model.
    
    Tests based on availability management requirements:
    - Availability period tracking
    - Capacity and commitment management
    - Allocation tracking
    """
    
    def setUp(self):
        """Set up test data."""
        self.resource = IdleResourceFactory()
    
    def test_create_resource_availability(self):
        """Test creating resource availability with valid data."""
        # Given: Availability data
        start_date = timezone.now()
        end_date = timezone.now() + timedelta(days=14)
        
        availability = ResourceAvailability.objects.create(
            resource=self.resource,
            start_date=start_date,
            end_date=end_date,
            availability_type='full_time',
            capacity_percentage=100,
            hourly_commitment=40,
            location_constraints='remote'
        )
        
        # When: Availability is created
        saved_availability = ResourceAvailability.objects.get(id=availability.id)
        
        # Then: Availability should be saved correctly
        self.assertEqual(saved_availability.resource, self.resource)
        self.assertEqual(saved_availability.availability_type, 'full_time')
        self.assertEqual(saved_availability.capacity_percentage, 100)
        self.assertEqual(saved_availability.hourly_commitment, 40)
        self.assertEqual(saved_availability.location_constraints, 'remote')
    
    def test_availability_date_validation(self):
        """Test availability date range validation."""
        # Given: Invalid date range
        availability = ResourceAvailability(
            resource=self.resource,
            start_date=timezone.now() + timedelta(days=10),
            end_date=timezone.now(),  # End before start
            availability_type='full_time'
        )
        
        # When: Validating availability
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            availability.clean()
    
    def test_capacity_percentage_validation(self):
        """Test capacity percentage bounds validation."""
        # Given: Invalid capacity percentage
        availability = ResourceAvailability(
            resource=self.resource,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            capacity_percentage=150  # Over 100%
        )
        
        # When: Validating availability
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            availability.clean()
    
    def test_hourly_commitment_validation(self):
        """Test hourly commitment validation."""
        # Given: Invalid hourly commitment
        availability = ResourceAvailability(
            resource=self.resource,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            hourly_commitment=200  # Over 168 hours per week
        )
        
        # When: Validating availability
        # Then: Should raise ValidationError
        with self.assertRaises(ValidationError):
            availability.clean()
    
    def test_allocation_tracking(self):
        """Test allocation tracking functionality."""
        # Given: Available period
        availability = ResourceAvailabilityFactory(
            resource=self.resource,
            is_allocated=False,
            allocation_reference=''
        )
        
        # When: Allocating period
        availability.is_allocated = True
        availability.allocation_reference = 'PROJECT-456'
        availability.save()
        
        # Then: Allocation should be tracked
        availability.refresh_from_db()
        self.assertTrue(availability.is_allocated)
        self.assertEqual(availability.allocation_reference, 'PROJECT-456')
    
    def test_recurring_availability_pattern(self):
        """Test recurring availability pattern storage."""
        # Given: Recurring availability
        recurrence_pattern = {
            'type': 'weekly',
            'days': ['monday', 'tuesday', 'wednesday'],
            'repeat_count': 4
        }
        
        availability = ResourceAvailabilityFactory(
            resource=self.resource,
            is_recurring=True,
            recurrence_pattern=recurrence_pattern
        )
        
        # When: Accessing pattern
        # Then: Pattern should be stored correctly
        self.assertTrue(availability.is_recurring)
        self.assertEqual(availability.recurrence_pattern['type'], 'weekly')
        self.assertEqual(len(availability.recurrence_pattern['days']), 3)