"""
Custom exceptions for service layer operations.

These exceptions provide specific error types for different service layer scenarios,
enabling better error handling and user feedback.
"""


class ServiceException(Exception):
    """Base exception for all service layer errors."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code or 'SERVICE_ERROR'
        self.details = details or {}
        super().__init__(self.message)


class BusinessRuleException(ServiceException):
    """Exception raised when business rules are violated."""
    
    def __init__(self, message: str, rule_name: str = None, details: dict = None):
        self.rule_name = rule_name
        super().__init__(message, 'BUSINESS_RULE_VIOLATION', details)


class ValidationException(ServiceException):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str, field_errors: dict = None, details: dict = None):
        self.field_errors = field_errors or {}
        super().__init__(message, 'VALIDATION_ERROR', details)


class AuthenticationException(ServiceException):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, 'AUTHENTICATION_ERROR', details)


class AuthorizationException(ServiceException):
    """Exception raised when authorization/permission check fails."""
    
    def __init__(self, message: str, required_permissions: list = None, details: dict = None):
        self.required_permissions = required_permissions or []
        super().__init__(message, 'AUTHORIZATION_ERROR', details)


class DataNotFoundException(ServiceException):
    """Exception raised when requested data is not found."""
    
    def __init__(self, message: str, resource_type: str = None, resource_id: str = None, details: dict = None):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(message, 'DATA_NOT_FOUND', details)


class DataConflictException(ServiceException):
    """Exception raised when data conflicts occur (e.g., version conflicts, duplicates)."""
    
    def __init__(self, message: str, conflict_type: str = None, details: dict = None):
        self.conflict_type = conflict_type
        super().__init__(message, 'DATA_CONFLICT', details)


class ExternalServiceException(ServiceException):
    """Exception raised when external service calls fail."""
    
    def __init__(self, message: str, service_name: str = None, details: dict = None):
        self.service_name = service_name
        super().__init__(message, 'EXTERNAL_SERVICE_ERROR', details)


class RateLimitException(ServiceException):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message: str, limit_type: str = None, retry_after: int = None, details: dict = None):
        self.limit_type = limit_type
        self.retry_after = retry_after
        super().__init__(message, 'RATE_LIMIT_EXCEEDED', details)