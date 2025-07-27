"""
Test Configuration and Settings for TDD/BDD Test Suite.

Provides test-specific settings, utilities, and configuration
for running comprehensive tests across all models and workflows.
"""

import os
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db import transaction


class BaseTestCase(TestCase):
    """
    Base test case with common setup for all tests.
    
    Provides:
    - Database isolation
    - Common fixtures
    - Test utilities
    - Performance tracking
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level test data."""
        super().setUpClass()
        cls._setup_test_environment()
    
    @classmethod
    def _setup_test_environment(cls):
        """Configure test environment settings."""
        # Disable migrations for faster tests
        settings.MIGRATION_MODULES = {
            'authentication': None,
            'resource_management': None,
            'config': None,
            'integration': None,
            'monitoring': None,
            'monitoring_alerts': None,
        }
        
        # Use in-memory database for speed
        if 'test' in settings.DATABASES['default']['NAME']:
            settings.DATABASES['default']['OPTIONS'] = {
                'timeout': 20,
            }
    
    def setUp(self):
        """Set up test case."""
        super().setUp()
        self.start_transaction()
    
    def tearDown(self):
        """Clean up test case."""
        self.rollback_transaction()
        super().tearDown()
    
    def start_transaction(self):
        """Start database transaction for test isolation."""
        self.transaction = transaction.atomic()
        self.transaction.__enter__()
    
    def rollback_transaction(self):
        """Rollback transaction to clean up test data."""
        if hasattr(self, 'transaction'):
            self.transaction.__exit__(None, None, None)


class TDDTestMixin:
    """
    Mixin for Test-Driven Development test cases.
    
    Provides:
    - Red-Green-Refactor cycle tracking
    - Test coverage utilities
    - Assertion helpers
    """
    
    def assert_model_validation_error(self, model_instance, field_name, error_message=None):
        """Assert that model validation raises expected error."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError) as context:
            model_instance.full_clean()
        
        if field_name:
            self.assertIn(field_name, context.exception.error_dict)
        
        if error_message:
            field_errors = context.exception.error_dict.get(field_name, [])
            error_messages = [str(error) for error in field_errors]
            self.assertTrue(
                any(error_message in msg for msg in error_messages),
                f"Expected error message '{error_message}' not found in {error_messages}"
            )
    
    def assert_dao_method_success(self, result, expected_keys=None):
        """Assert that DAO method returns successful result."""
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get('success', False), f"DAO method failed: {result}")
        
        if expected_keys:
            for key in expected_keys:
                self.assertIn(key, result, f"Expected key '{key}' not found in result")
    
    def assert_dao_method_failure(self, result, expected_error=None):
        """Assert that DAO method returns failure result."""
        self.assertIsInstance(result, dict)
        self.assertFalse(result.get('success', True), "DAO method should have failed")
        
        if expected_error:
            error_message = result.get('error', '')
            self.assertIn(expected_error, error_message)
    
    def assert_audit_trail_updated(self, model_instance, field_names=None):
        """Assert that audit trail fields are properly updated."""
        default_audit_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
        fields_to_check = field_names or default_audit_fields
        
        for field in fields_to_check:
            if hasattr(model_instance, field):
                value = getattr(model_instance, field)
                self.assertIsNotNone(value, f"Audit field '{field}' should not be None")


class BDDTestMixin:
    """
    Mixin for Behavior-Driven Development test cases.
    
    Provides:
    - Given-When-Then structure
    - Business scenario tracking
    - Workflow validation
    """
    
    def given(self, description):
        """Mark the Given step of BDD scenario."""
        self.scenario_step = f"GIVEN: {description}"
        return self
    
    def when(self, description):
        """Mark the When step of BDD scenario."""
        self.scenario_step = f"WHEN: {description}"
        return self
    
    def then(self, description):
        """Mark the Then step of BDD scenario."""
        self.scenario_step = f"THEN: {description}"
        return self
    
    def and_step(self, description):
        """Mark an And step in BDD scenario."""
        self.scenario_step = f"AND: {description}"
        return self
    
    def assert_business_rule_enforced(self, rule_description, validation_func):
        """Assert that business rule is properly enforced."""
        try:
            result = validation_func()
            if result is False:
                self.fail(f"Business rule violated: {rule_description}")
        except Exception as e:
            self.fail(f"Business rule validation failed: {rule_description}. Error: {str(e)}")
    
    def assert_workflow_completed(self, workflow_steps, validation_func):
        """Assert that complete workflow is executed successfully."""
        for step_name, step_func in workflow_steps.items():
            try:
                step_result = step_func()
                self.assertTrue(
                    step_result, 
                    f"Workflow step '{step_name}' failed"
                )
            except Exception as e:
                self.fail(f"Workflow step '{step_name}' failed with error: {str(e)}")
        
        # Final validation
        final_result = validation_func()
        self.assertTrue(final_result, "Workflow completion validation failed")


class TestDataBuilder:
    """
    Builder pattern for creating complex test data scenarios.
    
    Provides fluent interface for building related model instances
    with proper relationships and realistic data.
    """
    
    def __init__(self):
        """Initialize test data builder."""
        self.data = {}
        self.created_objects = []
    
    def with_department(self, name=None, **kwargs):
        """Add department to test scenario."""
        from tests.factories import DepartmentFactory
        
        department = DepartmentFactory(
            department_name=name or 'Test Department',
            **kwargs
        )
        self.data['department'] = department
        self.created_objects.append(department)
        return self
    
    def with_employee(self, department=None, **kwargs):
        """Add employee to test scenario."""
        from tests.factories import EmployeeFactory
        
        emp_department = department or self.data.get('department')
        employee = EmployeeFactory(
            department=emp_department,
            **kwargs
        )
        self.data['employee'] = employee
        self.created_objects.append(employee)
        return self
    
    def with_user(self, **kwargs):
        """Add user to test scenario."""
        from tests.factories import UserFactory
        
        user = UserFactory(**kwargs)
        self.data['user'] = user
        self.created_objects.append(user)
        return self
    
    def with_idle_resource(self, employee=None, **kwargs):
        """Add idle resource to test scenario."""
        from tests.factories import IdleResourceFactory
        
        resource_employee = employee or self.data.get('employee')
        resource = IdleResourceFactory(
            employee=resource_employee,
            **kwargs
        )
        self.data['idle_resource'] = resource
        self.created_objects.append(resource)
        return self
    
    def with_skills(self, skill_names=None, **kwargs):
        """Add skills to idle resource."""
        from tests.factories import ResourceSkillFactory
        
        resource = self.data.get('idle_resource')
        if not resource:
            raise ValueError("Must create idle_resource before adding skills")
        
        skills = []
        skill_names = skill_names or ['Python', 'Django', 'PostgreSQL']
        
        for skill_name in skill_names:
            skill = ResourceSkillFactory(
                resource=resource,
                skill_name=skill_name,
                **kwargs
            )
            skills.append(skill)
            self.created_objects.append(skill)
        
        self.data['skills'] = skills
        return self
    
    def with_availability(self, **kwargs):
        """Add availability periods to resource."""
        from tests.factories import ResourceAvailabilityFactory
        
        resource = self.data.get('idle_resource')
        if not resource:
            raise ValueError("Must create idle_resource before adding availability")
        
        availability = ResourceAvailabilityFactory(
            resource=resource,
            **kwargs
        )
        self.data['availability'] = availability
        self.created_objects.append(availability)
        return self
    
    def with_session(self, user=None, **kwargs):
        """Add user session to test scenario."""
        from tests.factories import UserSessionFactory
        
        session_user = user or self.data.get('user')
        session = UserSessionFactory(
            user=session_user,
            **kwargs
        )
        self.data['session'] = session
        self.created_objects.append(session)
        return self
    
    def build(self):
        """Return built test data."""
        return self.data
    
    def cleanup(self):
        """Clean up created test objects."""
        # Delete in reverse order to handle dependencies
        for obj in reversed(self.created_objects):
            try:
                obj.delete()
            except Exception:
                pass  # Ignore cleanup errors
        
        self.data.clear()
        self.created_objects.clear()


class PerformanceTestMixin:
    """
    Mixin for performance testing of DAO methods and business logic.
    
    Provides:
    - Query count tracking
    - Response time measurement
    - Memory usage monitoring
    """
    
    def assert_query_count(self, expected_count, tolerance=0):
        """Assert that query count is within expected range."""
        from django.test.utils import override_settings
        from django.db import connection
        
        def decorator(func):
            def wrapper(*args, **kwargs):
                with override_settings(DEBUG=True):
                    initial_queries = len(connection.queries)
                    result = func(*args, **kwargs)
                    final_queries = len(connection.queries)
                    
                    actual_count = final_queries - initial_queries
                    min_expected = expected_count - tolerance
                    max_expected = expected_count + tolerance
                    
                    self.assertGreaterEqual(
                        actual_count, min_expected,
                        f"Query count {actual_count} below expected minimum {min_expected}"
                    )
                    self.assertLessEqual(
                        actual_count, max_expected,
                        f"Query count {actual_count} above expected maximum {max_expected}"
                    )
                    
                    return result
            return wrapper
        return decorator
    
    def assert_response_time(self, max_seconds):
        """Assert that operation completes within time limit."""
        import time
        
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                elapsed = end_time - start_time
                self.assertLessEqual(
                    elapsed, max_seconds,
                    f"Operation took {elapsed:.3f}s, expected <= {max_seconds}s"
                )
                
                return result
            return wrapper
        return decorator


# Test Configuration Constants
TEST_CONFIG = {
    'PERFORMANCE_THRESHOLDS': {
        'DAO_METHOD_MAX_TIME': 0.1,  # 100ms
        'LIST_QUERY_MAX_TIME': 0.5,  # 500ms
        'BULK_OPERATION_MAX_TIME': 2.0,  # 2 seconds
    },
    'QUERY_COUNT_LIMITS': {
        'SIMPLE_CRUD': 3,
        'LIST_WITH_FILTERS': 5,
        'COMPLEX_WORKFLOW': 10,
    },
    'TEST_DATA_SIZES': {
        'SMALL_DATASET': 10,
        'MEDIUM_DATASET': 100,
        'LARGE_DATASET': 1000,
    }
}


def run_test_suite():
    """Run the complete test suite with proper configuration."""
    import django
    from django.test.utils import get_runner
    from django.conf import settings
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_hello_world.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)
    
    # Run specific test modules
    test_modules = [
        'tests.test_authentication_models',
        'tests.test_resource_management_models', 
        'tests.test_bdd_scenarios',
    ]
    
    failures = test_runner.run_tests(test_modules)
    return failures == 0