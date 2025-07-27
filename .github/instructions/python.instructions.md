---
applyTo: "**/*.py"
---

# Python Development Standards & Best Practices

## Language Standards

### Python Version & Features
- Use Python 3.9+ for all projects
- Apply modern Python features: type hints, dataclasses, pattern matching (3.10+)
- Follow PEP 8 style guide with Black formatter (line length: 88)
- Use f-strings for string formatting
- Apply walrus operator (:=) where appropriate

### Code Style & Formatting
```python
# Good: Modern Python with type hints
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class UserConfig:
    """User configuration with validation."""
    name: str
    email: str
    age: int
    preferences: Dict[str, Union[str, bool]] = None
    
    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if self.age < 0:
            raise ValueError("Age must be positive")
        if self.preferences is None:
            self.preferences = {}

def process_users(users: List[Dict[str, str]]) -> List[UserConfig]:
    """Process user data with proper type annotations."""
    return [
        UserConfig(
            name=user['name'],
            email=user['email'], 
            age=int(user['age'])
        )
        for user in users
        if user.get('email')  # Only process users with email
    ]
```

## Code Organization & Structure

### Project Layout
```
project_root/
├── src/                    # Source code (src-layout)
│   ├── package_name/
│   │   ├── __init__.py
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utility functions
│   │   └── exceptions.py   # Custom exceptions
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── requirements/           # Dependencies
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── pyproject.toml         # Project configuration
├── README.md
└── .env.example
```

### Import Organization
```python
# Standard library imports
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
import requests
from pydantic import BaseModel, validator
from sqlalchemy import create_engine

# Local imports
from .models import User
from .services.user_service import UserService
from .utils.validation import validate_email
```

## Type Annotations & Documentation

### Type Hints Best Practices
```python
from typing import List, Dict, Optional, Union, TypeVar, Protocol
from collections.abc import Callable, Iterable

T = TypeVar('T')

class Processable(Protocol):
    """Protocol for objects that can be processed."""
    def process(self) -> str: ...

def process_items(
    items: Iterable[Processable],
    processor: Callable[[Processable], T],
    filter_func: Optional[Callable[[Processable], bool]] = None
) -> List[T]:
    """Process items with optional filtering.
    
    Args:
        items: Iterable of processable items
        processor: Function to process each item
        filter_func: Optional function to filter items
        
    Returns:
        List of processed items
        
    Example:
        >>> items = [User(name="John"), User(name="Jane")]
        >>> result = process_items(items, lambda u: u.name.upper())
        >>> print(result)
        ['JOHN', 'JANE']
    """
    filtered_items = filter(filter_func, items) if filter_func else items
    return [processor(item) for item in filtered_items]
```

### Docstring Standards (Google Style)
```python
def calculate_user_score(
    user_data: Dict[str, Union[str, int, float]], 
    weights: Optional[Dict[str, float]] = None
) -> float:
    """Calculate user score based on various metrics.
    
    This function computes a weighted score based on user activity,
    engagement, and other factors defined in the weights dictionary.
    
    Args:
        user_data: Dictionary containing user metrics including:
            - activity_score: User activity rating (0-100)
            - engagement_score: User engagement rating (0-100)
            - completion_rate: Task completion percentage (0-1)
        weights: Optional custom weights for score calculation.
            Defaults to {'activity': 0.4, 'engagement': 0.4, 'completion': 0.2}
            
    Returns:
        Calculated composite score as float between 0.0 and 100.0
        
    Raises:
        ValueError: If user_data is missing required fields
        TypeError: If weights contain non-numeric values
        
    Example:
        Basic usage:
        >>> user = {
        ...     'activity_score': 85,
        ...     'engagement_score': 92,
        ...     'completion_rate': 0.88
        ... }
        >>> score = calculate_user_score(user)
        >>> print(f"User score: {score:.1f}")
        User score: 87.6
        
        With custom weights:
        >>> weights = {'activity': 0.5, 'engagement': 0.3, 'completion': 0.2}
        >>> score = calculate_user_score(user, weights)
        >>> print(f"Weighted score: {score:.1f}")
        Weighted score: 86.9
        
    Note:
        This function uses a linear combination of scores. For more
        complex scoring algorithms, consider using the ScoreCalculator class.
    """
    # Implementation here
    pass
```

## Error Handling & Exceptions

### Custom Exception Hierarchy
```python
class ApplicationError(Exception):
    """Base exception for application-specific errors."""
    
    def __init__(self, message: str, error_code: str = None) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__

class ValidationError(ApplicationError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: str = None) -> None:
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field

class UserNotFoundError(ApplicationError):
    """Raised when requested user cannot be found."""
    
    def __init__(self, user_id: str) -> None:
        message = f"User with ID {user_id} not found"
        super().__init__(message, "USER_NOT_FOUND")
        self.user_id = user_id
```

### Error Handling Patterns
```python
import logging
from contextlib import contextmanager
from typing import Iterator, Optional

logger = logging.getLogger(__name__)

def safe_api_call(url: str, timeout: int = 30) -> Optional[Dict]:
    """Make API call with proper error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        logger.error(f"API call timed out: {url}")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed for {url}: {e}")
        return None
        
    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {e}")
        return None

@contextmanager
def database_transaction() -> Iterator[None]:
    """Context manager for database transactions."""
    transaction = None
    try:
        transaction = db.begin()
        yield
        transaction.commit()
        
    except Exception as e:
        if transaction:
            transaction.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
        
    finally:
        if transaction:
            transaction.close()
```

## Performance & Memory Optimization

### Memory-Efficient Patterns
```python
from typing import Iterator, Generator
import itertools

def read_large_file(filename: str) -> Generator[str, None, None]:
    """Read large file line by line to avoid memory issues."""
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

def process_in_batches(
    items: Iterator[T], 
    batch_size: int = 1000
) -> Iterator[List[T]]:
    """Process items in batches to control memory usage."""
    iterator = iter(items)
    while batch := list(itertools.islice(iterator, batch_size)):
        yield batch

# Memory-efficient data processing
def process_large_dataset(filename: str) -> Dict[str, int]:
    """Process large dataset with minimal memory footprint."""
    result = {}
    
    for batch in process_in_batches(read_large_file(filename)):
        for line in batch:
            # Process each line
            key = extract_key(line)
            result[key] = result.get(key, 0) + 1
            
    return result
```

### Performance Optimization
```python
from functools import lru_cache, wraps
import time
from typing import Callable, Any

def retry_with_backoff(
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> Callable:
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    wait_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s")
                    time.sleep(wait_time)
                    
        return wrapper
    return decorator

@lru_cache(maxsize=128)
def expensive_calculation(value: int) -> int:
    """Cached expensive calculation."""
    # Simulate expensive operation
    time.sleep(0.1)
    return value ** 2

class DataProcessor:
    """Optimized data processor with caching."""
    
    def __init__(self, cache_size: int = 1000):
        self._cache = {}
        self._cache_size = cache_size
    
    def process_with_cache(self, data: str) -> str:
        """Process data with LRU cache."""
        if data in self._cache:
            return self._cache[data]
            
        result = self._expensive_process(data)
        
        # Simple LRU implementation
        if len(self._cache) >= self._cache_size:
            # Remove oldest item
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            
        self._cache[data] = result
        return result
```

## Testing Best Practices

### Unit Testing Patterns
```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Generator

class TestUserService:
    """Test suite for UserService class."""
    
    @pytest.fixture
    def mock_database(self) -> Mock:
        """Mock database for testing."""
        return Mock()
    
    @pytest.fixture
    def user_service(self, mock_database: Mock) -> UserService:
        """UserService instance with mocked dependencies."""
        return UserService(database=mock_database)
    
    @pytest.fixture
    def sample_user(self) -> Dict[str, Any]:
        """Sample user data for testing."""
        return {
            'id': '123',
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 30
        }
    
    def test_get_user_success(self, user_service: UserService, mock_database: Mock, sample_user: Dict):
        """Test successful user retrieval."""
        # Arrange
        mock_database.get_user.return_value = sample_user
        
        # Act
        result = user_service.get_user('123')
        
        # Assert
        assert result == sample_user
        mock_database.get_user.assert_called_once_with('123')
    
    def test_get_user_not_found(self, user_service: UserService, mock_database: Mock):
        """Test user not found scenario."""
        # Arrange
        mock_database.get_user.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User with ID 123 not found"):
            user_service.get_user('123')
    
    @pytest.mark.parametrize("user_data,expected_valid", [
        ({'name': 'John', 'email': 'john@example.com', 'age': 25}, True),
        ({'name': '', 'email': 'john@example.com', 'age': 25}, False),
        ({'name': 'John', 'email': 'invalid-email', 'age': 25}, False),
        ({'name': 'John', 'email': 'john@example.com', 'age': -5}, False),
    ])
    def test_validate_user_data(self, user_service: UserService, user_data: Dict, expected_valid: bool):
        """Test user data validation with various inputs."""
        if expected_valid:
            # Should not raise exception
            user_service.validate_user_data(user_data)
        else:
            with pytest.raises(ValidationError):
                user_service.validate_user_data(user_data)

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_user_operation()
    assert result is not None
```

## Configuration & Environment

### Environment Configuration
```python
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration from environment variables."""
    
    # Database
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    database_pool_size: int = int(os.getenv('DATABASE_POOL_SIZE', '10'))
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    jwt_secret: str = os.getenv('JWT_SECRET', 'jwt-secret-change-in-production')
    
    # Application
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    environment: str = os.getenv('ENVIRONMENT', 'development')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # External Services
    redis_url: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    api_base_url: str = os.getenv('API_BASE_URL', 'http://localhost:8000')
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.environment == 'production':
            if self.secret_key.startswith('dev-'):
                raise ValueError("SECRET_KEY must be set in production")
            if self.debug:
                raise ValueError("DEBUG must be False in production")

# Global configuration instance
config = AppConfig()

def get_config() -> AppConfig:
    """Get application configuration."""
    return config
```

### Logging Configuration
```python
import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = 'INFO', log_file: Optional[Path] = None) -> None:
    """Configure application logging."""
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Configure third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
```

## Security Best Practices

### Input Validation & Sanitization
```python
import re
import html
from typing import Any, Dict

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) and len(email) <= 254

def sanitize_input(user_input: str, max_length: int = 1000) -> str:
    """Sanitize user input to prevent XSS and injection attacks."""
    if not user_input:
        return ""
    
    # HTML escape
    sanitized = html.escape(user_input)
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';\\]', '', sanitized)
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    # Remove excessive whitespace
    sanitized = ' '.join(sanitized.split())
    
    return sanitized.strip()

def validate_user_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize user input data."""
    validated = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            validated[key] = sanitize_input(value)
        elif isinstance(value, (int, float, bool)):
            validated[key] = value
        elif isinstance(value, dict):
            validated[key] = validate_user_input(value)
        else:
            # Skip unknown types
            continue
            
    return validated
```

## Dependency Management

### Requirements Management
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "my-django-api"
version = "1.0.0"
description = "Django REST Framework API"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"

dependencies = [
    "Django>=4.2,<5.0",
    "djangorestframework>=3.14.0",
    "django-cors-headers>=4.0.0",
    "djangorestframework-simplejwt>=5.2.0",
    "django-filter>=22.1",
    "drf-yasg>=1.21.0",
    "psycopg2-binary>=2.9.0",
    "redis>=4.5.0",
    "celery>=5.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-django>=4.5.0",
    "pytest-cov>=4.0.0",
    "factory-boy>=3.2.0",
    "black>=22.0.0",
    "isort>=5.10.0",
    "flake8>=5.0.0",
    "mypy>=0.991",
]

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_django = "django"
sections = ["FUTURE", "STDLIB", "DJANGO", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]

[tool.mypy]
python_version = "3.9"
check_untyped_defs = true
ignore_missing_imports = true
warn_unused_ignores = true
warn_redundant_casts = true
warn_unused_configs = true
```

When writing Python code:
- Use type hints for all function signatures and complex variables
- Follow PEP 8 with Black formatting
- Write comprehensive docstrings using Google style
- Implement proper error handling with custom exceptions
- Use context managers for resource management
- Apply modern Python features appropriately
- Optimize for performance and memory usage
- Write tests for all functionality
- Use environment variables for configuration
- Implement proper logging and monitoring
- Validate and sanitize all user inputs
- Keep dependencies updated and secure