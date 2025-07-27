"""
Base service classes and utilities for the service layer.

This module provides the foundation for all service layer operations,
including standardized response formats, audit logging, and access control.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .exceptions import ServiceException, AuthorizationException


@dataclass
class ServiceResponse:
    """Standardized service response format."""
    success: bool
    data: Any = None
    errors: List[str] = None
    warnings: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def success_response(cls, data: Any = None, metadata: Dict = None):
        """Create a successful response."""
        return cls(success=True, data=data, metadata=metadata or {})
    
    @classmethod
    def error_response(cls, errors: Union[str, List[str]], data: Any = None):
        """Create an error response."""
        if isinstance(errors, str):
            errors = [errors]
        return cls(success=False, data=data, errors=errors)
    
    @classmethod
    def validation_response(cls, errors: List[str], warnings: List[str] = None, data: Any = None):
        """Create a validation response."""
        return cls(
            success=len(errors) == 0,
            data=data,
            errors=errors,
            warnings=warnings or []
        )


class BaseService(ABC):
    """Base service class providing common functionality for all services."""
    
    def __init__(self, user_context: Optional[Dict] = None):
        self.user_context = user_context or {}
        self._audit_enabled = True
    
    def execute_with_audit(self, operation_name: str, operation_func, *args, **kwargs):
        """Execute operation with audit trail logging."""
        try:
            with transaction.atomic():
                result = operation_func(*args, **kwargs)
                
                if self._audit_enabled:
                    self._log_audit_success(operation_name, result, args, kwargs)
                
                return result
        except Exception as e:
            if self._audit_enabled:
                self._log_audit_error(operation_name, str(e), args, kwargs)
            raise
    
    def _log_audit_success(self, operation: str, result: Any, args: tuple, kwargs: dict):
        """Log successful operation for audit trail."""
        # Import here to avoid circular imports
        try:
            from .common.audit_service import AuditService
            AuditService.log_operation(
                operation=operation,
                user_context=self.user_context,
                result=result,
                args=args,
                kwargs=kwargs
            )
        except ImportError:
            # Audit service not yet implemented, skip logging
            pass
    
    def _log_audit_error(self, operation: str, error: str, args: tuple, kwargs: dict):
        """Log failed operation for audit trail."""
        try:
            from .common.audit_service import AuditService
            AuditService.log_error(
                operation=operation,
                user_context=self.user_context,
                error=error,
                args=args,
                kwargs=kwargs
            )
        except ImportError:
            # Audit service not yet implemented, skip logging
            pass
    
    def validate_user_permissions(self, required_permissions: List[str]) -> bool:
        """Validate user has required permissions."""
        if not self.user_context.get('user_id'):
            raise AuthorizationException("User context required")
        
        user_permissions = self.user_context.get('permissions', [])
        missing_permissions = [perm for perm in required_permissions if perm not in user_permissions]
        
        if missing_permissions:
            raise AuthorizationException(
                f"Missing required permissions: {', '.join(missing_permissions)}",
                required_permissions=required_permissions
            )
        
        return True
    
    def get_user_department_scope(self) -> List[str]:
        """Get user's department access scope."""
        user_role = self.user_context.get('role')
        user_dept = self.user_context.get('department_id')
        
        if user_role == 'admin':
            return []  # Admin sees all departments
        elif user_role == 'manager':
            # Manager sees own department and children
            return self._get_department_hierarchy(user_dept)
        else:
            # Regular user sees only own department
            return [user_dept] if user_dept else []
    
    def _get_department_hierarchy(self, department_id: str) -> List[str]:
        """Get department and all its child departments."""
        # This would typically query a department hierarchy table
        # For now, return just the department itself
        # In a real implementation, this would recursively find child departments
        return [department_id] if department_id else []
    
    def get_current_timestamp(self):
        """Get current timestamp for operations."""
        return timezone.now()
    
    def validate_required_fields(self, data: Dict, required_fields: List[str]) -> List[str]:
        """Validate that required fields are present in data."""
        errors = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                errors.append(f"Field '{field}' is required")
        return errors
    
    def validate_field_formats(self, data: Dict, field_formats: Dict[str, str]) -> List[str]:
        """Validate field formats using basic validation rules."""
        errors = []
        
        for field, format_type in field_formats.items():
            if field in data and data[field] is not None:
                value = data[field]
                
                if format_type == 'email':
                    if not self._is_valid_email(value):
                        errors.append(f"Field '{field}' must be a valid email address")
                elif format_type == 'uuid':
                    if not self._is_valid_uuid(value):
                        errors.append(f"Field '{field}' must be a valid UUID")
                elif format_type == 'phone':
                    if not self._is_valid_phone(value):
                        errors.append(f"Field '{field}' must be a valid phone number")
                elif format_type == 'date':
                    if not self._is_valid_date(value):
                        errors.append(f"Field '{field}' must be a valid date")
        
        return errors
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _is_valid_uuid(self, uuid_str: str) -> bool:
        """Basic UUID validation."""
        import re
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return re.match(pattern, str(uuid_str).lower()) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Basic phone number validation."""
        import re
        # Allow various phone number formats
        pattern = r'^[\+]?[1-9][\d]{0,15}$'
        return re.match(pattern, phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) is not None
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Basic date validation."""
        try:
            from datetime import datetime
            datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return True
        except (ValueError, AttributeError):
            return False
    
    def paginate_results(self, queryset, pagination: Dict) -> Dict:
        """Apply pagination to queryset and return paginated results with metadata."""
        page = pagination.get('page', 1)
        page_size = min(pagination.get('page_size', 20), 100)  # Limit max page size
        offset = (page - 1) * page_size
        
        total_count = queryset.count()
        results = list(queryset[offset:offset + page_size])
        
        return {
            'results': results,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size,
                'has_next': offset + page_size < total_count,
                'has_previous': page > 1
            }
        }
    
    def apply_sorting(self, queryset, sorting: Dict):
        """Apply sorting to queryset."""
        if not sorting:
            return queryset
        
        sort_field = sorting.get('field')
        sort_order = sorting.get('order', 'asc')
        
        if sort_field:
            if sort_order.lower() == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
        
        return queryset
    
    @abstractmethod
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate operation can be performed in current context."""
        pass


class ReadOnlyService(BaseService):
    """Base class for read-only services that don't modify data."""
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Read-only services typically require authenticated user."""
        return self.user_context.get('user_id') is not None


class WriteService(BaseService):
    """Base class for services that modify data."""
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Write services require authenticated user and proper permissions."""
        if not self.user_context.get('user_id'):
            return False
        
        # Additional validation can be added here based on operation
        return True
    
    def validate_write_permissions(self, resource_type: str, operation: str) -> bool:
        """Validate user has write permissions for specific resource and operation."""
        required_permission = f"{resource_type}_{operation}"
        try:
            self.validate_user_permissions([required_permission])
            return True
        except AuthorizationException:
            return False