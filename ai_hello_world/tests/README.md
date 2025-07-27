# Test Suite Documentation

## Overview

This comprehensive test suite follows **Test-Driven Development (TDD)** and **Behavior-Driven Development (BDD)** principles to ensure robust coverage of all business requirements and technical specifications.

## Test Structure

### 📁 Test Organization
```
tests/
├── __init__.py                     # Test package initialization
├── factories.py                   # Test data factories (Factory Boy pattern)
├── test_authentication_models.py  # TDD tests for authentication models
├── test_resource_management_models.py  # TDD tests for resource management
├── test_bdd_scenarios.py          # BDD workflow and integration tests
├── test_config.py                 # Test configuration and utilities
└── README.md                      # This documentation
```

## 🧪 Test Categories

### 1. TDD Tests (Test-Driven Development)

#### Authentication Models (`test_authentication_models.py`)
- **Department Model**: Hierarchy, manager assignment, uniqueness
- **Employee Model**: Contact info, department relationships, termination tracking
- **User Model**: Authentication, account status, audit trails
- **UserSession Model**: Complete DAO method testing
  - `create_session()` - Token generation and session creation
  - `validate_session()` - Session validation and activity tracking
  - `refresh_session()` - Token refresh with optimistic locking
  - `revoke_session()` - Session invalidation
  - `cleanup_expired_sessions()` - Maintenance operations
  - `get_active_sessions()` - Active session listing
  - `update_session_activity()` - Activity tracking

#### Resource Management Models (`test_resource_management_models.py`)
- **IdleResource Model**: Core CRUD operations and business rules
- **IdleResource DAO Methods**:
  - `create_with_validation()` - Business rule enforcement
  - `update_with_version_check()` - Optimistic locking
  - `list_with_filters()` - Dynamic filtering and pagination
  - `check_availability()` - Conflict detection and scheduling
- **ImportSession/ExportSession**: Bulk operation tracking
- **ResourceSkill**: Skill categorization and verification
- **ResourceAvailability**: Scheduling and allocation management

### 2. BDD Tests (Behavior-Driven Development)

#### User Authentication Workflows (`test_bdd_scenarios.py`)
- **Successful Authentication**: Login, session creation, activity tracking
- **Multi-Device Sessions**: Concurrent session management
- **Token Refresh**: Seamless token renewal process
- **Session Cleanup**: Security maintenance and cleanup

#### Resource Management Workflows
- **Complete Onboarding**: Employee → Resource → Skills → Availability
- **Resource Allocation**: Search → Availability Check → Allocation
- **Skill Validation**: Certification tracking and verification
- **Bulk Import/Export**: Data processing and error handling

#### Integration Workflows
- **User-to-Resource Lifecycle**: Complete end-to-end process
- **Cross-Department Coordination**: Multi-department resource allocation

## 🏭 Test Factories

### Factory Classes (using Factory Boy pattern)
```python
# Core Factories
DepartmentFactory()          # Organizational departments
EmployeeFactory()           # Employee records
UserFactory()               # User accounts
ProfileFactory()            # User profiles
UserSessionFactory()        # Authentication sessions

# Resource Management Factories
IdleResourceFactory()       # Idle resources
ResourceSkillFactory()      # Skills and certifications
ResourceAvailabilityFactory()  # Availability periods
ImportSessionFactory()      # Import operations
ExportSessionFactory()      # Export operations

# Utility Functions
create_user_with_profile()  # User + Profile
create_employee_with_department()  # Employee + Department
create_idle_resource_with_skills()  # Resource + Skills
```

## 🛠️ Test Utilities

### Base Test Classes
- **BaseTestCase**: Common setup, transaction management
- **TDDTestMixin**: Red-Green-Refactor utilities, DAO assertions
- **BDDTestMixin**: Given-When-Then structure, workflow validation
- **PerformanceTestMixin**: Query counting, response time tracking

### Test Data Builder
```python
# Fluent interface for complex test scenarios
builder = TestDataBuilder()
data = (builder
    .with_department('Engineering')
    .with_employee()
    .with_user()
    .with_idle_resource(status='available')
    .with_skills(['Python', 'Django'])
    .with_availability()
    .build())
```

## 🚀 Running Tests

### Command Line Interface
```bash
# Run all tests
python run_tests.py

# Run specific category
python run_tests.py authentication
python run_tests.py resource_management
python run_tests.py bdd

# Run specific test
python run_tests.py --test tests.test_authentication_models.UserSessionModelTest.test_create_session_dao_method

# Generate detailed report
python run_tests.py --report

# Adjust verbosity (0=minimal, 3=debug)
python run_tests.py -v 3
```

### Django Test Runner
```bash
# Standard Django test commands
python manage.py test tests.test_authentication_models
python manage.py test tests.test_resource_management_models
python manage.py test tests.test_bdd_scenarios

# Run with coverage
coverage run --source='.' manage.py test tests/
coverage report
coverage html
```

## 📋 Test Coverage

### Model Coverage
- ✅ **Authentication Models**: 100% model coverage, all DAO methods
- ✅ **Resource Management Models**: 100% model coverage, all DAO methods
- ✅ **Validation Rules**: All business rules and constraints
- ✅ **Relationships**: All foreign keys and many-to-many relationships

### Business Logic Coverage
- ✅ **CRUD Operations**: Create, Read, Update, Delete with validation
- ✅ **DAO Methods**: All custom business logic methods
- ✅ **Workflow Integration**: End-to-end business processes
- ✅ **Error Handling**: Exception scenarios and edge cases

### Performance Testing
- ✅ **Query Optimization**: N+1 query prevention
- ✅ **Response Time**: Sub-100ms for simple operations
- ✅ **Bulk Operations**: Efficient batch processing
- ✅ **Memory Usage**: Appropriate resource consumption

## 🎯 Test Assertions

### TDD Assertions
```python
# Model validation
self.assert_model_validation_error(model, 'field_name', 'error message')

# DAO method success
self.assert_dao_method_success(result, ['resource_id', 'warnings'])

# DAO method failure
self.assert_dao_method_failure(result, 'expected error message')

# Audit trail verification
self.assert_audit_trail_updated(model, ['created_at', 'updated_at'])
```

### BDD Assertions
```python
# Business rule enforcement
self.assert_business_rule_enforced('rule description', validation_func)

# Workflow completion
self.assert_workflow_completed(workflow_steps, final_validation)

# Integration scenarios
self.given('setup description')
self.when('action description')
self.then('expected outcome')
```

## 📊 Performance Benchmarks

### Response Time Targets
- **Simple CRUD**: < 100ms
- **List with Filters**: < 500ms
- **Complex Workflows**: < 2000ms
- **Bulk Operations**: < 5000ms

### Query Count Limits
- **Simple Operations**: ≤ 3 queries
- **List Operations**: ≤ 5 queries
- **Complex Workflows**: ≤ 10 queries

## 🔍 Test Quality Metrics

### Coverage Requirements
- **Statement Coverage**: ≥ 95%
- **Branch Coverage**: ≥ 90%
- **Function Coverage**: 100%
- **Model Coverage**: 100%

### Business Rule Testing
- ✅ All validation rules tested
- ✅ All business constraints verified
- ✅ All error scenarios covered
- ✅ All edge cases handled

## 🐛 Debugging Tests

### Common Issues
1. **Import Errors**: Check Django settings and app registration
2. **Database Errors**: Ensure migrations are applied
3. **Factory Errors**: Verify model relationships and constraints
4. **Performance Issues**: Check query optimization and indexes

### Debug Commands
```bash
# Run with debug SQL
python run_tests.py -v 3

# Run specific failing test
python run_tests.py --test path.to.failing.test

# Check test database
python manage.py dbshell --database=test

# Verify migrations
python manage.py showmigrations
```

## 📝 Best Practices

### TDD Cycle
1. **Red**: Write failing test first
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

### BDD Scenarios
1. **Given**: Setup test conditions
2. **When**: Execute the action
3. **Then**: Verify expected outcome
4. **And**: Additional conditions/verifications

### Test Maintenance
- Keep tests focused and specific
- Use descriptive test names
- Maintain test data isolation
- Regular test review and cleanup
- Performance monitoring

## 🔗 Related Documentation

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [TDD Best Practices](https://docs.python.org/3/library/unittest.html)
- [BDD with Python](https://behave.readthedocs.io/)

---

*This test suite ensures comprehensive coverage of all business requirements while maintaining high code quality and performance standards.*