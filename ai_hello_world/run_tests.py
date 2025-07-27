#!/usr/bin/env python
"""
Comprehensive Test Runner for AI Hello World Project.

Runs TDD and BDD test suites with detailed reporting and coverage analysis.
Supports different test categories and output formats.
"""

import os
import sys
import argparse
import time
from datetime import datetime
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import call_command


def setup_django():
    """Setup Django for test execution."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_hello_world.settings')
    django.setup()


def run_migrations():
    """Ensure database is properly migrated for tests."""
    print("🔄 Setting up test database...")
    try:
        call_command('migrate', verbosity=0, interactive=False)
        print("✅ Database migrations completed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    return True


def run_test_category(category, verbosity=2):
    """Run specific test category."""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=False,
        keepdb=True,  # Keep database between test runs for speed
        debug_sql=verbosity > 2
    )
    
    test_modules = {
        'authentication': ['tests.test_authentication_models'],
        'resource_management': ['tests.test_resource_management_models'],
        'bdd': ['tests.test_bdd_scenarios'],
        'all': [
            'tests.test_authentication_models',
            'tests.test_resource_management_models',
            'tests.test_bdd_scenarios'
        ]
    }
    
    modules_to_run = test_modules.get(category, test_modules['all'])
    
    print(f"🧪 Running {category} tests...")
    print(f"📋 Test modules: {', '.join(modules_to_run)}")
    
    start_time = time.time()
    failures = test_runner.run_tests(modules_to_run)
    end_time = time.time()
    
    duration = end_time - start_time
    
    if failures == 0:
        print(f"✅ All {category} tests passed! ({duration:.2f}s)")
        return True
    else:
        print(f"❌ {failures} test(s) failed in {category} category ({duration:.2f}s)")
        return False


def run_specific_test(test_path, verbosity=2):
    """Run a specific test method or class."""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=False,
        keepdb=True
    )
    
    print(f"🎯 Running specific test: {test_path}")
    
    start_time = time.time()
    failures = test_runner.run_tests([test_path])
    end_time = time.time()
    
    duration = end_time - start_time
    
    if failures == 0:
        print(f"✅ Test passed! ({duration:.2f}s)")
        return True
    else:
        print(f"❌ Test failed ({duration:.2f}s)")
        return False


def generate_test_report():
    """Generate comprehensive test report."""
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
# Test Execution Report
Generated: {report_time}

## Test Coverage Summary

### TDD Tests (Test-Driven Development)
- **Authentication Models**: Core user, session, and security tests
- **Resource Management Models**: Resource CRUD and DAO method tests
- **Model Validation**: Business rule and constraint validation
- **Database Integrity**: Foreign key and unique constraint tests

### BDD Tests (Behavior-Driven Development)  
- **User Authentication Workflow**: Login, session management, cleanup
- **Resource Management Workflow**: Onboarding, allocation, skill validation
- **Import/Export Workflows**: Bulk operations and data validation
- **Cross-Department Coordination**: Multi-department resource allocation

### DAO Method Testing
- **Create with Validation**: Business rule enforcement
- **Update with Version Check**: Optimistic locking
- **List with Filters**: Dynamic filtering and pagination
- **Availability Checking**: Conflict detection and scheduling

## Test Categories

### 🔐 Authentication Tests
- User account management
- Session creation and validation
- Token refresh mechanisms
- Security policy enforcement
- Audit trail verification

### 📊 Resource Management Tests
- Resource CRUD operations
- Skill management and validation
- Availability scheduling
- Import/export processing
- Business workflow integration

### 🔄 Integration Tests
- End-to-end workflows
- Cross-module interactions
- Data consistency validation
- Performance benchmarks

## Test Data Factories
- Comprehensive factory classes for all models
- Realistic test data generation
- Relationship management
- Utility functions for complex scenarios

## Quality Assurance
- Model validation testing
- Business rule enforcement
- Database constraint verification
- Performance benchmarking
- Error handling validation

---
*This test suite follows TDD and BDD best practices to ensure comprehensive coverage of all business requirements and technical specifications.*
"""
    
    return report


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run AI Hello World test suite')
    parser.add_argument(
        'category',
        nargs='?',
        default='all',
        choices=['all', 'authentication', 'resource_management', 'bdd'],
        help='Test category to run (default: all)'
    )
    parser.add_argument(
        '--test',
        help='Run specific test (e.g., tests.test_authentication_models.UserModelTest.test_create_user)'
    )
    parser.add_argument(
        '--verbosity', '-v',
        type=int,
        default=2,
        choices=[0, 1, 2, 3],
        help='Verbosity level (0=minimal, 3=debug)'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate test report'
    )
    parser.add_argument(
        '--no-migrations',
        action='store_true',
        help='Skip running migrations'
    )
    
    args = parser.parse_args()
    
    print("🚀 AI Hello World Test Suite")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Run migrations unless skipped
    if not args.no_migrations:
        if not run_migrations():
            return 1
    
    success = True
    
    if args.test:
        # Run specific test
        success = run_specific_test(args.test, args.verbosity)
    else:
        # Run test category
        success = run_test_category(args.category, args.verbosity)
    
    if args.report:
        print("\n📄 Generating test report...")
        report = generate_test_report()
        
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"📝 Test report saved to: {report_file}")
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Test execution completed successfully!")
        return 0
    else:
        print("💥 Test execution completed with failures!")
        return 1


if __name__ == '__main__':
    sys.exit(main())