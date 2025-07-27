---
applyTo: "test/**/*.py,tests/**/*.py,**/test_*.py"
---

# Python Testing Standards for Django REST Framework

## Testing Framework & Configuration

### Primary Testing Tools
- **Framework**: pytest-django for Django integration
- **Data Generation**: factory-boy for test data creation
- **Mocking**: unittest.mock for external dependencies
- **Coverage**: pytest-cov for code coverage tracking
- **API Testing**: Django REST Framework's APIClient

### Test Configuration
```python
# pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = config.settings.testing
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --reuse-db
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (database, external services)
    api: API endpoint tests
    slow: Slow running tests
    django_db: Tests requiring database access
```

## Test Case Naming Convention

### Format: `[AREA]-[TYPE]-[NUMBER]`

**Django/DRF Area Prefixes:**
- `MODEL` - Django model tests
- `VIEW` - Django view/viewset tests  
- `SERIALIZER` - DRF serializer tests
- `API` - REST API endpoint tests
- `PERMISSION` - Permission class tests
- `MIDDLEWARE` - Django middleware tests
- `SIGNAL` - Django signal tests
- `MANAGER` - Custom model manager tests
- `FORM` - Django form tests
- `COMMAND` - Management command tests
- `UTIL` - Utility function tests
- `SERVICE` - Service layer tests
- `AUTH` - Authentication tests

**Type Suffixes:**
- `UNIT` - Unit tests (isolated component)
- `INT` - Integration tests (component interaction)
- `E2E` - End-to-end tests (full workflow)

**Examples:**
- `MODEL-UNIT-001` - First unit test for model
- `API-INT-001` - First integration test for API
- `SERIALIZER-UNIT-001` - First serializer unit test

## Test Structure & Organization

### Test Directory Structure
```
tests/
├── conftest.py              # Global fixtures and configuration
├── factories/               # Factory Boy factories
│   ├── __init__.py
│   ├── user_factory.py
│   └── order_factory.py
├── unit/                    # Unit tests
│   ├── test_models.py
│   ├── test_serializers.py
│   ├── test_views.py
│   └── test_utils.py
├── integration/             # Integration tests
│   ├── test_api_workflows.py
│   ├── test_database.py
│   └── test_services.py
├── e2e/                     # End-to-end tests
│   ├── test_user_journey.py
│   └── test_api_flows.py
└── fixtures/                # Test data fixtures
    ├── users.json
    └── sample_data.json
```

## Fixtures & Test Data

### Global Fixtures (conftest.py)
```python
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    """DRF API client for testing."""
    return APIClient()

@pytest.fixture
def django_client():
    """Django test client."""
    return Client()

@pytest.fixture
@pytest.mark.django_db
def user():
    """Create a test user."""
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
@pytest.mark.django_db
def admin_user():
    """Create admin user."""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='adminpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    """API client with authenticated user."""
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def jwt_token(user):
    """JWT token for user."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def auth_headers(jwt_token):
    """Authorization headers with JWT token."""
    return {'HTTP_AUTHORIZATION': f'Bearer {jwt_token}'}
```

### Factory Boy Factories
```python
# tests/factories/user_factory.py
import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
        django_get_or_create = ('email',)
    
    email = factory.LazyFunction(lambda: fake.email())
    username = factory.LazyAttribute(lambda obj: obj.email.split('@')[0])
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    is_active = True
    is_staff = False
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after creation."""
        if not create:
            return
        
        password = extracted or 'defaultpass123'
        self.set_password(password)
        self.save()

class AdminUserFactory(UserFactory):
    """Factory for admin users."""
    is_staff = True
    is_superuser = True
    username = 'admin'
    email = 'admin@example.com'
```

## Unit Testing Patterns

### Model Testing
```python
# tests/unit/test_models.py
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.users.models import User
from tests.factories import UserFactory

@pytest.mark.django_db
class TestUserModel:
    """MODEL-UNIT-001: Test User model functionality."""
    
    def test_user_creation_success(self):
        """Test successful user creation with valid data."""
        user = UserFactory()
        
        assert user.pk is not None
        assert user.email
        assert user.is_active is True
        assert str(user) == f"{user.email}"
    
    def test_user_email_uniqueness(self):
        """Test email uniqueness constraint."""
        user1 = UserFactory(email='test@example.com')
        
        with pytest.raises(IntegrityError):
            UserFactory(email='test@example.com')
    
    @pytest.mark.parametrize("email,is_valid", [
        ('valid@example.com', True),
        ('invalid-email', False),
        ('', False),
        ('test@', False),
    ])
    def test_email_validation(self, email, is_valid):
        """Test email format validation."""
        user = User(email=email, username='test')
        
        if is_valid:
            user.full_clean()  # Should not raise
        else:
            with pytest.raises(ValidationError):
                user.full_clean()
    
    def test_user_soft_delete(self):
        """Test soft delete functionality."""
        user = UserFactory()
        user.soft_delete()
        
        assert user.is_active is False
        assert User.objects.filter(pk=user.pk).exists()
    
    def test_user_manager_active_users(self):
        """Test custom manager for active users."""
        active_user = UserFactory(is_active=True)
        inactive_user = UserFactory(is_active=False)
        
        active_users = User.active_objects.all()
        
        assert active_user in active_users
        assert inactive_user not in active_users
```

### Serializer Testing
```python
# tests/unit/test_serializers.py
import pytest
from apps.users.serializers import UserSerializer, UserCreateSerializer
from tests.factories import UserFactory

class TestUserSerializer:
    """SERIALIZER-UNIT-001: Test User serializer functionality."""
    
    @pytest.mark.django_db
    def test_serializer_valid_data(self):
        """Test serializer with valid data."""
        user = UserFactory()
        serializer = UserSerializer(user)
        
        assert 'id' in serializer.data
        assert 'email' in serializer.data
        assert 'password' not in serializer.data  # Should be write-only
    
    def test_serializer_validation_success(self):
        """Test successful validation of input data."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'securepass123'
        }
        
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid()
    
    @pytest.mark.parametrize("invalid_data,expected_error", [
        ({'email': 'invalid'}, 'email'),
        ({'email': ''}, 'email'),
        ({'password': '123'}, 'password'),  # Too short
    ])
    def test_serializer_validation_errors(self, invalid_data, expected_error):
        """Test serializer validation with invalid data."""
        base_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'securepass123'
        }
        base_data.update(invalid_data)
        
        serializer = UserCreateSerializer(data=base_data)
        assert not serializer.is_valid()
        assert expected_error in serializer.errors
    
    @pytest.mark.django_db
    def test_serializer_create_user(self):
        """Test user creation through serializer."""
        data = {
            'email': 'new@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.email == data['email']
        assert user.check_password(data['password'])
```

### View/ViewSet Testing
```python
# tests/unit/test_views.py
import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import UserFactory

@pytest.mark.django_db
class TestUserViewSet:
    """VIEW-UNIT-001: Test User ViewSet functionality."""
    
    def test_list_users_unauthenticated(self, api_client):
        """Test listing users requires authentication."""
        url = reverse('user-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_users_authenticated(self, authenticated_client):
        """Test authenticated user can list users."""
        UserFactory.create_batch(3)
        
        url = reverse('user-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 4  # 3 created + 1 authenticated user
    
    def test_create_user_success(self, api_client):
        """Test successful user creation."""
        data = {
            'email': 'new@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == data['email']
        assert 'password' not in response.data
    
    def test_retrieve_user_success(self, authenticated_client, user):
        """Test retrieving specific user."""
        url = reverse('user-detail', kwargs={'pk': user.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.pk
    
    def test_update_user_own_profile(self, authenticated_client, user):
        """Test user can update own profile."""
        data = {'first_name': 'Updated'}
        
        url = reverse('user-detail', kwargs={'pk': user.pk})
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
    
    def test_delete_user_permission_denied(self, authenticated_client, user):
        """Test regular user cannot delete other users."""
        other_user = UserFactory()
        
        url = reverse('user-detail', kwargs={'pk': other_user.pk})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
```

## Integration Testing

### API Integration Tests
```python
# tests/integration/test_api_workflows.py
import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import UserFactory

@pytest.mark.django_db
class TestUserAPIWorkflow:
    """API-INT-001: Test complete user API workflows."""
    
    def test_user_registration_and_login_flow(self, api_client):
        """Test complete user registration and login workflow."""
        # Step 1: Register new user
        registration_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'securepass123'
        }
        
        register_url = reverse('user-list')
        register_response = api_client.post(register_url, registration_data, format='json')
        
        assert register_response.status_code == status.HTTP_201_CREATED
        user_id = register_response.data['id']
        
        # Step 2: Login with new credentials
        login_data = {
            'email': registration_data['email'],
            'password': registration_data['password']
        }
        
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(login_url, login_data, format='json')
        
        assert login_response.status_code == status.HTTP_200_OK
        assert 'access' in login_response.data
        assert 'refresh' in login_response.data
        
        # Step 3: Access protected endpoint with token
        token = login_response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        profile_url = reverse('user-detail', kwargs={'pk': user_id})
        profile_response = api_client.get(profile_url)
        
        assert profile_response.status_code == status.HTTP_200_OK
        assert profile_response.data['email'] == registration_data['email']
    
    def test_user_crud_operations(self, authenticated_client, user):
        """Test complete CRUD operations for user."""
        # Create
        create_data = {
            'email': 'crud@example.com',
            'username': 'cruduser',
            'password': 'crudpass123'
        }
        
        create_url = reverse('user-list')
        create_response = authenticated_client.post(create_url, create_data, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED
        created_user_id = create_response.data['id']
        
        # Read
        read_url = reverse('user-detail', kwargs={'pk': created_user_id})
        read_response = authenticated_client.get(read_url)
        assert read_response.status_code == status.HTTP_200_OK
        
        # Update
        update_data = {'first_name': 'Updated Name'}
        update_response = authenticated_client.patch(read_url, update_data, format='json')
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data['first_name'] == 'Updated Name'
        
        # Delete (if permitted)
        delete_response = authenticated_client.delete(read_url)
        # Result depends on permissions - test appropriate response
```

### Database Integration Tests
```python
# tests/integration/test_database.py
import pytest
from django.db import transaction
from django.test import TransactionTestCase
from tests.factories import UserFactory

class TestDatabaseOperations(TransactionTestCase):
    """DB-INT-001: Test database operations and transactions."""
    
    def test_bulk_user_creation(self):
        """Test bulk creation of users."""
        users_data = [
            {'email': f'user{i}@example.com', 'username': f'user{i}'}
            for i in range(100)
        ]
        
        users = [User(**data) for data in users_data]
        created_users = User.objects.bulk_create(users)
        
        assert len(created_users) == 100
        assert User.objects.count() == 100
    
    def test_transaction_rollback(self):
        """Test transaction rollback on error."""
        initial_count = User.objects.count()
        
        try:
            with transaction.atomic():
                UserFactory()
                # Force an error to trigger rollback
                raise Exception("Simulated error")
        except Exception:
            pass
        
        assert User.objects.count() == initial_count
    
    def test_select_related_optimization(self):
        """Test query optimization with select_related."""
        user = UserFactory()
        
        with self.assertNumQueries(1):
            # Should use select_related to fetch profile in single query
            users = User.objects.select_related('profile').all()
            for user in users:
                _ = user.profile  # Should not trigger additional query

## Mocking & External Dependencies

### Mock External Services
```python
# tests/unit/test_services.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import RequestException
from apps.services.email_service import EmailService
from apps.services.api_client import ExternalAPIClient

class TestEmailService:
    """SERVICE-UNIT-001: Test email service with mocking."""
    
    @patch('apps.services.email_service.send_mail')
    def test_send_email_success(self, mock_send_mail):
        """Test successful email sending."""
        mock_send_mail.return_value = True
        
        service = EmailService()
        result = service.send_welcome_email('test@example.com', 'John')
        
        assert result is True
        mock_send_mail.assert_called_once_with(
            subject='Welcome John!',
            message=mock_send_mail.call_args[1]['message'],
            from_email='noreply@example.com',
            recipient_list=['test@example.com']
        )
    
    @patch('apps.services.email_service.send_mail')
    def test_send_email_failure(self, mock_send_mail):
        """Test email sending failure handling."""
        mock_send_mail.side_effect = Exception("SMTP Error")
        
        service = EmailService()
        result = service.send_welcome_email('test@example.com', 'John')
        
        assert result is False

class TestExternalAPIClient:
    """SERVICE-UNIT-002: Test external API client with mocking."""
    
    @patch('requests.get')
    def test_api_call_success(self, mock_get):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'success'}
        mock_get.return_value = mock_response
        
        client = ExternalAPIClient()
        result = client.fetch_user_data('123')
        
        assert result == {'data': 'success'}
        mock_get.assert_called_once_with(
            'https://api.example.com/users/123',
            headers={'Authorization': 'Bearer fake-token'},
            timeout=30
        )
    
    @patch('requests.get')
    def test_api_call_timeout(self, mock_get):
        """Test API call timeout handling."""
        mock_get.side_effect = RequestException("Timeout")
        
        client = ExternalAPIClient()
        result = client.fetch_user_data('123')
        
        assert result is None

### Context Managers & Resources
```python
# tests/unit/test_resources.py
import pytest
from unittest.mock import mock_open, patch, MagicMock
from apps.utils.file_processor import FileProcessor

class TestFileProcessor:
    """UTIL-UNIT-001: Test file processing with mocked file operations."""
    
    @patch('builtins.open', new_callable=mock_open, read_data='line1\nline2\nline3')
    def test_process_file_success(self, mock_file):
        """Test successful file processing."""
        processor = FileProcessor()
        result = processor.process_text_file('test.txt')
        
        assert result == ['line1', 'line2', 'line3']
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')
    
    @patch('builtins.open')
    def test_process_file_not_found(self, mock_open):
        """Test file not found error handling."""
        mock_open.side_effect = FileNotFoundError("File not found")
        
        processor = FileProcessor()
        result = processor.process_text_file('nonexistent.txt')
        
        assert result == []
    
    @patch('apps.utils.file_processor.os.path.exists')
    @patch('apps.utils.file_processor.shutil.copy2')
    def test_backup_file(self, mock_copy, mock_exists):
        """Test file backup functionality."""
        mock_exists.return_value = True
        
        processor = FileProcessor()
        result = processor.backup_file('source.txt', 'backup.txt')
        
        assert result is True
        mock_copy.assert_called_once_with('source.txt', 'backup.txt')
```

## Performance & Load Testing

### Performance Testing with pytest-benchmark
```python
# tests/performance/test_performance.py
import pytest
from tests.factories import UserFactory
from apps.services.user_service import UserService

class TestUserServicePerformance:
    """Test user service performance benchmarks."""
    
    @pytest.mark.django_db
    def test_user_creation_performance(self, benchmark):
        """Benchmark user creation performance."""
        service = UserService()
        user_data = {
            'email': 'perf@example.com',
            'username': 'perfuser',
            'password': 'perfpass123'
        }
        
        result = benchmark(service.create_user, user_data)
        assert result.email == user_data['email']
    
    @pytest.mark.django_db
    def test_user_search_performance(self, benchmark):
        """Benchmark user search performance."""
        # Create test data
        UserFactory.create_batch(100)
        
        service = UserService()
        result = benchmark(service.search_users, query='user', limit=10)
        
        assert len(result) <= 10
    
    @pytest.mark.parametrize("batch_size", [10, 50, 100])
    @pytest.mark.django_db
    def test_bulk_operations_performance(self, benchmark, batch_size):
        """Test performance with different batch sizes."""
        users_data = [
            {'email': f'bulk{i}@example.com', 'username': f'bulk{i}'}
            for i in range(batch_size)
        ]
        
        service = UserService()
        result = benchmark(service.bulk_create_users, users_data)
        
        assert len(result) == batch_size

### Memory Usage Testing
```python
# tests/performance/test_memory.py
import pytest
import gc
import tracemalloc
from tests.factories import UserFactory

@pytest.mark.slow
class TestMemoryUsage:
    """Test memory usage patterns."""
    
    @pytest.mark.django_db
    def test_memory_usage_bulk_creation(self):
        """Test memory usage during bulk operations."""
        tracemalloc.start()
        
        # Baseline memory
        gc.collect()
        snapshot1 = tracemalloc.take_snapshot()
        
        # Create many users
        UserFactory.create_batch(1000)
        
        # Measure memory after creation
        gc.collect()
        snapshot2 = tracemalloc.take_snapshot()
        
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        # Assert memory usage is reasonable (this is example - adjust as needed)
        total_size = sum(stat.size for stat in top_stats[:10])
        assert total_size < 50 * 1024 * 1024  # Less than 50MB for 1000 users
        
        tracemalloc.stop()
```

## End-to-End Testing

### Complete User Journey Tests
```python
# tests/e2e/test_user_journey.py
import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import UserFactory

@pytest.mark.django_db
@pytest.mark.e2e
class TestCompleteUserJourney:
    """E2E-001: Test complete user journey workflows."""
    
    def test_new_user_complete_workflow(self, api_client):
        """Test complete new user workflow from registration to profile update."""
        
        # Step 1: User registration
        registration_data = {
            'email': 'journey@example.com',
            'username': 'journeyuser',
            'password': 'journeypass123',
            'first_name': 'Journey',
            'last_name': 'User'
        }
        
        register_url = reverse('user-list')
        register_response = api_client.post(register_url, registration_data, format='json')
        
        assert register_response.status_code == status.HTTP_201_CREATED
        user_id = register_response.data['id']
        
        # Step 2: Email verification (simulated)
        verify_url = reverse('user-verify-email', kwargs={'pk': user_id})
        verify_response = api_client.post(verify_url, {'token': 'mock-token'})
        assert verify_response.status_code == status.HTTP_200_OK
        
        # Step 3: Login
        login_data = {
            'email': registration_data['email'],
            'password': registration_data['password']
        }
        
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(login_url, login_data, format='json')
        
        assert login_response.status_code == status.HTTP_200_OK
        access_token = login_response.data['access']
        
        # Step 4: Access user profile
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        profile_url = reverse('user-detail', kwargs={'pk': user_id})
        profile_response = api_client.get(profile_url)
        
        assert profile_response.status_code == status.HTTP_200_OK
        assert profile_response.data['email'] == registration_data['email']
        
        # Step 5: Update profile
        update_data = {
            'first_name': 'Updated Journey',
            'bio': 'This is my updated bio'
        }
        
        update_response = api_client.patch(profile_url, update_data, format='json')
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data['first_name'] == 'Updated Journey'
        
        # Step 6: Change password
        change_password_url = reverse('user-change-password', kwargs={'pk': user_id})
        password_data = {
            'old_password': 'journeypass123',
            'new_password': 'newjourneypass123'
        }
        
        password_response = api_client.post(change_password_url, password_data, format='json')
        assert password_response.status_code == status.HTTP_200_OK
        
        # Step 7: Login with new password
        api_client.credentials()  # Clear credentials
        
        new_login_data = {
            'email': registration_data['email'],
            'password': 'newjourneypass123'
        }
        
        new_login_response = api_client.post(login_url, new_login_data, format='json')
        assert new_login_response.status_code == status.HTTP_200_OK
    
    def test_admin_user_management_workflow(self, api_client):
        """Test admin user management workflow."""
        
        # Create admin user
        admin_user = UserFactory(is_staff=True, is_superuser=True)
        api_client.force_authenticate(user=admin_user)
        
        # Create regular users
        users = UserFactory.create_batch(5)
        
        # Admin lists all users
        list_url = reverse('user-list')
        list_response = api_client.get(list_url)
        
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data['results']) == 6  # 5 + admin
        
        # Admin updates user status
        user_to_deactivate = users[0]
        deactivate_url = reverse('user-detail', kwargs={'pk': user_to_deactivate.pk})
        deactivate_response = api_client.patch(
            deactivate_url, 
            {'is_active': False}, 
            format='json'
        )
        
        assert deactivate_response.status_code == status.HTTP_200_OK
        assert deactivate_response.data['is_active'] is False
        
        # Verify user is deactivated
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is False
```

## Security Testing

### Authentication & Authorization Tests
```python
# tests/security/test_security.py
import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import UserFactory

@pytest.mark.django_db
class TestSecurityFeatures:
    """AUTH-E2E-001: Test security features and vulnerabilities."""
    
    def test_unauthenticated_access_denied(self, api_client):
        """Test that protected endpoints deny unauthenticated access."""
        protected_urls = [
            reverse('user-list'),
            reverse('user-detail', kwargs={'pk': 1}),
        ]
        
        for url in protected_urls:
            response = api_client.get(url)
            assert response.status_code in [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
    
    def test_unauthorized_user_modification(self, api_client):
        """Test users cannot modify other users' data."""
        user1 = UserFactory()
        user2 = UserFactory()
        
        api_client.force_authenticate(user=user1)
        
        # Try to update user2's data
        update_url = reverse('user-detail', kwargs={'pk': user2.pk})
        update_data = {'first_name': 'Hacked'}
        
        response = api_client.patch(update_url, update_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_sql_injection_prevention(self, authenticated_client):
        """Test SQL injection prevention in search."""
        malicious_query = "'; DROP TABLE users; --"
        
        search_url = reverse('user-list')
        response = authenticated_client.get(search_url, {'search': malicious_query})
        
        # Should return safely without executing SQL injection
        assert response.status_code == status.HTTP_200_OK
        
        # Verify users table still exists by making another query
        verify_response = authenticated_client.get(search_url)
        assert verify_response.status_code == status.HTTP_200_OK
    
    def test_xss_prevention(self, authenticated_client):
        """Test XSS prevention in user input."""
        xss_payload = '<script>alert("XSS")</script>'
        
        user_data = {
            'first_name': xss_payload,
            'bio': f'Normal text {xss_payload} more text'
        }
        
        create_url = reverse('user-list')
        response = authenticated_client.post(create_url, user_data, format='json')
        
        if response.status_code == status.HTTP_201_CREATED:
            # Verify XSS payload is properly escaped/sanitized
            assert '<script>' not in response.data.get('first_name', '')
            assert '<script>' not in response.data.get('bio', '')
    
    def test_rate_limiting(self, api_client):
        """Test API rate limiting (if implemented)."""
        login_url = reverse('token_obtain_pair')
        login_data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        
        # Make many failed login attempts
        for _ in range(10):
            response = api_client.post(login_url, login_data, format='json')
            # First few should return 401, later ones might be rate limited
            assert response.status_code in [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_429_TOO_MANY_REQUESTS
            ]

## Testing Utilities & Helpers

### Custom Assertions
```python
# tests/utils.py
import json
from typing import Dict, Any
from rest_framework.response import Response

def assert_api_response_structure(response: Response, expected_keys: list):
    """Assert API response has expected structure."""
    assert response.status_code == 200
    data = response.data
    
    for key in expected_keys:
        assert key in data, f"Expected key '{key}' not found in response"

def assert_validation_error(response: Response, field: str, error_message: str = None):
    """Assert response contains validation error for specific field."""
    assert response.status_code == 400
    assert field in response.data
    
    if error_message:
        field_errors = response.data[field]
        assert any(error_message in str(error) for error in field_errors)

def assert_database_state(model_class, expected_count: int, **filters):
    """Assert database contains expected number of objects."""
    actual_count = model_class.objects.filter(**filters).count()
    assert actual_count == expected_count, \
        f"Expected {expected_count} {model_class.__name__} objects, found {actual_count}"

class APITestMixin:
    """Mixin providing common API testing utilities."""
    
    def assert_paginated_response(self, response, expected_count=None):
        """Assert response is properly paginated."""
        assert 'results' in response.data
        assert 'count' in response.data
        assert 'next' in response.data
        assert 'previous' in response.data
        
        if expected_count is not None:
            assert response.data['count'] == expected_count
    
    def assert_serializer_fields(self, response_data, expected_fields):
        """Assert response contains expected serializer fields."""
        for field in expected_fields:
            assert field in response_data
    
    def create_authenticated_user(self, **kwargs):
        """Create and authenticate user for testing."""
        user = UserFactory(**kwargs)
        self.client.force_authenticate(user=user)
        return user
```

## Test Documentation & Reporting

### Test Reporting Configuration
```python
# pytest.ini (additional configuration)
[tool:pytest]
# ... other configuration ...
addopts = 
    --strict-markers
    --strict-config
    --tb=short
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml:coverage.xml
    --junit-xml=test-results/junit.xml
    --html=test-results/report.html
    --self-contained-html

markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    api: marks tests as API tests
    security: marks tests as security tests
    performance: marks tests as performance tests
```

## Best Practices Summary

### Test Writing Guidelines
1. **Naming**: Use descriptive test names that explain what is being tested
2. **Structure**: Follow Arrange-Act-Assert pattern consistently
3. **Isolation**: Each test should be independent and not rely on other tests
4. **Data**: Use factories for test data creation, not hard-coded values
5. **Mocking**: Mock external dependencies, not the code under test
6. **Coverage**: Aim for >80% code coverage, 100% for critical paths
7. **Performance**: Keep tests fast, mark slow tests appropriately
8. **Documentation**: Document complex test scenarios and edge cases

### Django-Specific Testing Best Practices
1. Use `@pytest.mark.django_db` for tests that need database access
2. Use `TransactionTestCase` for tests requiring transaction testing
3. Mock external services (email, APIs, file systems)
4. Test both success and failure scenarios
5. Validate serializer behavior thoroughly
6. Test permission classes and authentication
7. Use `assertNumQueries` to test query optimization
8. Test custom model managers and methods
9. Verify soft deletion and audit trail functionality
10. Test API pagination, filtering, and searching features

When writing tests:
- Follow the test naming convention consistently
- Use appropriate fixtures and factories
- Mock external dependencies properly
- Test both positive and negative scenarios
- Maintain high test coverage (>80%)
- Keep tests fast and isolated
- Document complex test scenarios
- Use parametrized tests for multiple similar cases
- Test security and authorization thoroughly
- Include performance tests for critical operations