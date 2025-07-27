# Testing Setup Guide

## Quick Start

### Option 1: Install Dependencies
```bash
# Install factory-boy for test data generation
pip install factory-boy

# Run all tests
python run_tests.py
```

### Option 2: Use Django's Built-in Test Runner
```bash
# Run tests directly with Django (works without factory-boy)
python manage.py test tests.test_authentication_models.DepartmentModelTest.test_create_department_with_valid_data

# Run specific test modules
python manage.py test tests.test_authentication_models
```

### Option 3: Manual Dependency Installation
If you're having trouble with pip, try these alternatives:

```bash
# Using pip with user flag
pip install --user factory-boy

# Using conda (if available)
conda install factory-boy

# Using system package manager (Ubuntu/Debian)
sudo apt-get install python3-factory-boy

# Using system package manager (macOS with Homebrew)
brew install python-factory-boy
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'factory'

**Solution 1**: Install factory-boy
```bash
pip install factory-boy==3.3.1
```

**Solution 2**: Skip factory-based tests and run simple model tests
```bash
# Run individual tests that don't require factories
python manage.py test authentication.tests
python manage.py test resource_management.tests
```

**Solution 3**: Use virtual environment
```bash
# Create virtual environment
python -m venv test_env

# Activate virtual environment
# On Windows:
test_env\Scripts\activate
# On Linux/Mac:
source test_env/bin/activate

# Install dependencies
pip install factory-boy django

# Run tests
python run_tests.py
```

### Issue: Build Dependencies Failed

If you see Rust/maturin errors, try:

```bash
# Install only essential packages
pip install factory-boy --no-deps
pip install faker

# Or skip optional dependencies
pip install factory-boy --ignore-installed
```

## Minimal Test Execution

If you can't install factory-boy, you can still test core functionality:

### Test Database Models
```bash
# Test model creation and validation
python manage.py shell
>>> from authentication.models import Department
>>> dept = Department.objects.create(department_name="Test Dept")
>>> print(dept)
```

### Test DAO Methods
```bash
# Test DAO methods manually
python manage.py shell
>>> from authentication.models import User, UserSession
>>> user = User.objects.create(username="test", email="test@example.com")
>>> session_data = UserSession.create_session(user=user)
>>> print(session_data)
```

### Run Specific Model Tests
```bash
# Run tests for specific models without factories
python -c "
import django
django.setup()
from authentication.models import Department
dept = Department(department_name='Test')
dept.full_clean()
print('✅ Department model validation passed')
"
```

## Environment Check

Run this script to check your environment:

```python
# check_env.py
import sys
print(f"Python version: {sys.version}")

try:
    import django
    print(f"✅ Django {django.VERSION} available")
except ImportError:
    print("❌ Django not installed")

try:
    import factory
    print(f"✅ Factory Boy available")
except ImportError:
    print("❌ Factory Boy not installed - install with: pip install factory-boy")

try:
    from authentication.models import User
    print("✅ Authentication models available")
except ImportError as e:
    print(f"❌ Model import failed: {e}")
```

## Alternative Test Approaches

### 1. Direct Model Testing
```python
# Simple model tests without factories
from django.test import TestCase
from authentication.models import Department

class SimpleModelTest(TestCase):
    def test_department_creation(self):
        dept = Department.objects.create(
            department_name="Engineering"
        )
        self.assertEqual(dept.department_name, "Engineering")
```

### 2. Manual Data Creation
```python
# Create test data manually
def create_test_data():
    from authentication.models import Department, Employee, User
    
    dept = Department.objects.create(department_name="IT")
    user = User.objects.create(
        username="testuser",
        email="test@company.com",
        first_name="Test",
        last_name="User"
    )
    employee = Employee.objects.create(
        employee_number="EMP001",
        first_name="Test",
        last_name="Employee",
        email="employee@company.com",
        department=dept,
        position="Developer",
        hire_date="2024-01-01"
    )
    return dept, user, employee
```

### 3. DAO Method Testing
```python
# Test DAO methods directly
def test_dao_methods():
    user, _ = create_test_data()
    
    # Test session creation
    session_result = UserSession.create_session(user=user)
    assert session_result['success']
    
    # Test session validation
    access_token = session_result['access_token']
    validation_result = UserSession.validate_session(access_token)
    assert validation_result is not None
    
    print("✅ DAO methods working correctly")
```

## Success Verification

Once dependencies are installed, verify with:

```bash
# Quick test
python -c "
import django
django.setup()
from tests.factories import UserFactory
user = UserFactory()
print(f'✅ Test user created: {user.username}')
"

# Full test suite
python run_tests.py --verbosity 1

# Specific test category
python run_tests.py authentication
```

## Getting Help

If you're still having issues:

1. **Check Python version**: `python --version` (should be 3.8+)
2. **Check Django installation**: `python -c "import django; print(django.VERSION)"`
3. **Check current directory**: Make sure you're in the project root
4. **Check virtual environment**: Consider using a fresh virtual environment
5. **Check permissions**: On some systems, use `sudo` or `--user` flag with pip

For persistent issues, you can run individual tests without the full test suite:

```bash
python manage.py test authentication.models.test_user_creation
```