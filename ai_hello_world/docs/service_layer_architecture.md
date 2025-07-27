# Django REST Framework Service Layer Architecture

## 📋 Overview

This document outlines the implementation of service layer in Django REST Framework based on the service design documents. The service layer acts as an intermediary between Django REST Framework views and Django models, implementing complex business logic, validation, and data access patterns.

## 🏗️ Architecture Design

### Layer Structure
```
┌─────────────────────────────────────┐
│           API Layer (Views)         │
│  - ViewSets                         │
│  - Serializers                      │
│  - URL Routing                      │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Service Layer               │
│  - Authentication Services          │
│  - Resource Management Services     │
│  - Validation Services              │
│  - Business Logic                   │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Model Layer (DAO)           │
│  - Django Models                    │
│  - Custom Model Methods             │
│  - Database Access                  │
└─────────────────────────────────────┘
```

## 📁 Service Layer Directory Structure

```
ai_hello_world/
├── services/
│   ├── __init__.py
│   ├── base.py                    # Base service classes and utilities
│   ├── exceptions.py              # Custom service exceptions
│   └── authentication/
│       ├── __init__.py
│       ├── auth_service.py        # Authentication logic
│       ├── session_service.py     # Session management
│       └── security_service.py    # Security policies
│   └── resource_management/
│       ├── __init__.py
│       ├── crud_service.py        # CRUD operations
│       ├── search_service.py      # Search and filtering
│       ├── validation_service.py  # Validation logic
│       └── import_export_service.py
│   └── common/
│       ├── __init__.py
│       ├── audit_service.py       # Audit trail service
│       ├── notification_service.py
│       └── cache_service.py
```

## 🎯 Service Design Patterns

### 1. Base Service Pattern
All services inherit from a base service class providing common functionality:

```python
# services/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from django.db import transaction
from django.core.exceptions import ValidationError
from .exceptions import ServiceException, BusinessRuleException

class BaseService(ABC):
    """Base service class providing common functionality for all services."""
    
    def __init__(self, user_context: Optional[Dict] = None):
        self.user_context = user_context or {}
        self._audit_enabled = True
    
    def execute_with_audit(self, operation_name: str, operation_func, *args, **kwargs):
        """Execute operation with audit trail logging."""
        from .common.audit_service import AuditService
        
        try:
            with transaction.atomic():
                result = operation_func(*args, **kwargs)
                
                if self._audit_enabled:
                    AuditService.log_operation(
                        operation=operation_name,
                        user_context=self.user_context,
                        result=result,
                        args=args,
                        kwargs=kwargs
                    )
                
                return result
        except Exception as e:
            if self._audit_enabled:
                AuditService.log_error(
                    operation=operation_name,
                    user_context=self.user_context,
                    error=str(e),
                    args=args,
                    kwargs=kwargs
                )
            raise
    
    def validate_user_permissions(self, required_permissions: List[str]) -> bool:
        """Validate user has required permissions."""
        if not self.user_context.get('user_id'):
            raise ServiceException("User context required")
        
        user_permissions = self.user_context.get('permissions', [])
        return all(perm in user_permissions for perm in required_permissions)
    
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
    
    @abstractmethod
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate operation can be performed in current context."""
        pass
```

### 2. Service Response Pattern
Standardized response format for all service operations:

```python
# services/base.py
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

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
        return cls(success=True, data=data, metadata=metadata or {})
    
    @classmethod
    def error_response(cls, errors: Union[str, List[str]], data: Any = None):
        if isinstance(errors, str):
            errors = [errors]
        return cls(success=False, data=data, errors=errors)
    
    @classmethod
    def validation_response(cls, errors: List[str], warnings: List[str] = None):
        return cls(
            success=len(errors) == 0,
            errors=errors,
            warnings=warnings or []
        )
```

## 🔐 Authentication Services Implementation

### Authentication Service
Maps to SVE-MDE-01-01-01 from service design:

```python
# services/authentication/auth_service.py
from typing import Dict, Optional
from django.contrib.auth import authenticate
from django.utils import timezone
from ..base import BaseService, ServiceResponse
from ...authentication.models import User, UserSession, LoginAttempt

class AuthenticationService(BaseService):
    """
    Authentication Service implementing SVE-MDE-01-01-01
    Handles user credential validation and authentication logic.
    """
    
    def authenticate_user(self, username: str, password: str, language: str = 'en') -> ServiceResponse:
        """
        Authenticate user credentials and establish session.
        
        Maps to Service SVE-MDE-01-01-01: Authentication Service
        Steps 1-6 from service design document.
        """
        return self.execute_with_audit(
            'authenticate_user',
            self._authenticate_user_impl,
            username=username,
            password=password,
            language=language
        )
    
    def _authenticate_user_impl(self, username: str, password: str, language: str) -> ServiceResponse:
        """Internal authentication implementation."""
        
        # Step 1: Validate input parameters
        if not username or not password:
            return ServiceResponse.error_response("Username and password are required")
        
        # Step 2: Retrieve user credentials and profile
        try:
            user_data = User.get_user_with_roles(username)
            if not user_data['user_exists'] or not user_data['is_active']:
                return ServiceResponse.error_response("Invalid credentials or inactive account")
        except Exception as e:
            return ServiceResponse.error_response(f"Authentication failed: {str(e)}")
        
        # Step 3: Verify password
        user = user_data['user']
        if not User.authenticate_user(username, password):
            # Log failed attempt
            LoginAttempt.log_security_event(
                username=username,
                event_type='failed_login',
                ip_address=self.user_context.get('ip_address'),
                user_agent=self.user_context.get('user_agent')
            )
            return ServiceResponse.error_response("Invalid credentials")
        
        # Step 4: Retrieve user roles and permissions
        roles_data = user_data['roles']
        permissions_data = user_data['permissions']
        
        # Step 5: Update last login time
        try:
            previous_login = User.objects.filter(user_id=user.user_id).first().last_login
            user.last_login = timezone.now()
            user.save()
        except Exception:
            previous_login = None
        
        # Step 6: Compile authentication result
        return ServiceResponse.success_response(
            data={
                'isValid': True,
                'userId': str(user.user_id),
                'userProfile': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'language': language
                },
                'roleInfo': {
                    'roles': roles_data,
                    'permissions': permissions_data,
                    'department': user_data.get('department')
                },
                'message': 'Authentication successful',
                'lastLoginTime': previous_login.isoformat() if previous_login else None
            },
            metadata={
                'login_time': timezone.now().isoformat(),
                'session_required': True
            }
        )
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate authentication operations."""
        return True  # Authentication operations don't require pre-existing auth
```

### Session Management Service
Maps to SVE-MDE-01-02-01:

```python
# services/authentication/session_service.py
import jwt
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from ..base import BaseService, ServiceResponse
from ...authentication.models import UserSession

class SessionManagementService(BaseService):
    """
    Session Management Service implementing SVE-MDE-01-02-01
    Manages user sessions, JWT tokens, and session lifecycle.
    """
    
    def create_session(self, user_id: str, user_profile: Dict, remember_me: bool = False) -> ServiceResponse:
        """Create new user session with JWT tokens."""
        return self.execute_with_audit(
            'create_session',
            self._create_session_impl,
            user_id=user_id,
            user_profile=user_profile,
            remember_me=remember_me
        )
    
    def _create_session_impl(self, user_id: str, user_profile: Dict, remember_me: bool) -> ServiceResponse:
        """Internal session creation implementation."""
        
        try:
            # Create session using model method
            session_data = UserSession.create_session(
                user_id=user_id,
                ip_address=self.user_context.get('ip_address'),
                user_agent=self.user_context.get('user_agent'),
                remember_me=remember_me
            )
            
            # Generate JWT tokens
            access_token, refresh_token = self._generate_jwt_tokens(
                user_id=user_id,
                session_id=session_data['session_id'],
                user_profile=user_profile,
                remember_me=remember_me
            )
            
            return ServiceResponse.success_response(
                data={
                    'success': True,
                    'sessionId': session_data['session_id'],
                    'accessToken': access_token,
                    'refreshToken': refresh_token,
                    'expiresIn': session_data['expires_in'],
                    'sessionData': session_data,
                    'message': 'Session created successfully'
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Session creation failed: {str(e)}")
    
    def validate_session(self, access_token: str) -> ServiceResponse:
        """Validate existing session and access token."""
        return self.execute_with_audit(
            'validate_session',
            self._validate_session_impl,
            access_token=access_token
        )
    
    def _validate_session_impl(self, access_token: str) -> ServiceResponse:
        """Internal session validation implementation."""
        
        try:
            # Decode JWT token
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            session_id = payload.get('session_id')
            user_id = payload.get('user_id')
            
            # Validate session using model method
            validation_result = UserSession.validate_session(session_id, user_id)
            
            if validation_result['is_valid']:
                return ServiceResponse.success_response(
                    data={
                        'success': True,
                        'isValid': True,
                        'sessionData': validation_result['session_data'],
                        'userId': user_id,
                        'expiresIn': validation_result['expires_in']
                    }
                )
            else:
                return ServiceResponse.error_response("Invalid or expired session")
                
        except jwt.ExpiredSignatureError:
            return ServiceResponse.error_response("Token expired")
        except jwt.InvalidTokenError:
            return ServiceResponse.error_response("Invalid token")
        except Exception as e:
            return ServiceResponse.error_response(f"Session validation failed: {str(e)}")
    
    def refresh_session(self, refresh_token: str) -> ServiceResponse:
        """Generate new access token using refresh token."""
        return self.execute_with_audit(
            'refresh_session',
            self._refresh_session_impl,
            refresh_token=refresh_token
        )
    
    def _refresh_session_impl(self, refresh_token: str) -> ServiceResponse:
        """Internal session refresh implementation."""
        
        try:
            # Decode refresh token
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            session_id = payload.get('session_id')
            user_id = payload.get('user_id')
            
            # Refresh session using model method
            refresh_result = UserSession.refresh_session(session_id, user_id)
            
            if refresh_result['is_valid']:
                # Generate new tokens
                new_access_token, new_refresh_token = self._generate_jwt_tokens(
                    user_id=user_id,
                    session_id=session_id,
                    user_profile=refresh_result['user_profile']
                )
                
                return ServiceResponse.success_response(
                    data={
                        'success': True,
                        'isValid': True,
                        'sessionData': refresh_result['session_data'],
                        'newTokens': {
                            'accessToken': new_access_token,
                            'refreshToken': new_refresh_token
                        },
                        'expiresIn': refresh_result['expires_in']
                    }
                )
            else:
                return ServiceResponse.error_response("Invalid refresh token")
                
        except jwt.ExpiredSignatureError:
            return ServiceResponse.error_response("Refresh token expired")
        except jwt.InvalidTokenError:
            return ServiceResponse.error_response("Invalid refresh token")
        except Exception as e:
            return ServiceResponse.error_response(f"Session refresh failed: {str(e)}")
    
    def terminate_session(self, session_id: str, access_token: str) -> ServiceResponse:
        """Invalidate session and all associated tokens."""
        return self.execute_with_audit(
            'terminate_session',
            self._terminate_session_impl,
            session_id=session_id,
            access_token=access_token
        )
    
    def _terminate_session_impl(self, session_id: str, access_token: str) -> ServiceResponse:
        """Internal session termination implementation."""
        
        try:
            # Revoke session using model method
            revoke_result = UserSession.revoke_session(session_id)
            
            return ServiceResponse.success_response(
                data={
                    'success': revoke_result['success'],
                    'message': 'Session terminated successfully'
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Session termination failed: {str(e)}")
    
    def _generate_jwt_tokens(self, user_id: str, session_id: str, user_profile: Dict, remember_me: bool = False):
        """Generate JWT access and refresh tokens."""
        
        now = timezone.now()
        access_expiry = now + timedelta(hours=1)  # 1 hour for access token
        refresh_expiry = now + timedelta(days=30 if remember_me else 7)  # 30 days if remember_me, else 7 days
        
        access_payload = {
            'user_id': user_id,
            'session_id': session_id,
            'user_profile': user_profile,
            'exp': access_expiry,
            'iat': now,
            'type': 'access'
        }
        
        refresh_payload = {
            'user_id': user_id,
            'session_id': session_id,
            'exp': refresh_expiry,
            'iat': now,
            'type': 'refresh'
        }
        
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
        
        return access_token, refresh_token
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate session management operations."""
        if operation in ['create_session']:
            return True  # Session creation doesn't require existing session
        return self.user_context.get('user_id') is not None
```

## 🔍 Resource Management Services

### CRUD Service
Maps to SVE-MDE-03-01-01 through SVE-MDE-03-01-05:

```python
# services/resource_management/crud_service.py
from typing import Dict, List, Any, Optional
from django.db import transaction
from ..base import BaseService, ServiceResponse
from ...resource_management.models import IdleResource
from ..common.audit_service import AuditService

class ResourceCRUDService(BaseService):
    """
    Resource CRUD Service implementing SVE-MDE-03-01 operations
    Handles Create, Read, Update, Delete operations for idle resources.
    """
    
    def create_resource(self, record_data: Dict, validation_level: str = 'full') -> ServiceResponse:
        """
        Create new idle resource record.
        
        Maps to Service SVE-MDE-03-01-01: Create Idle Resource
        """
        if not self.validate_user_permissions(['resource_create']):
            return ServiceResponse.error_response("Insufficient permissions for resource creation")
        
        return self.execute_with_audit(
            'create_resource',
            self._create_resource_impl,
            record_data=record_data,
            validation_level=validation_level
        )
    
    def _create_resource_impl(self, record_data: Dict, validation_level: str) -> ServiceResponse:
        """Internal resource creation implementation."""
        
        try:
            # Step 1: Data Validation (using validation service)
            from .validation_service import ResourceValidationService
            validator = ResourceValidationService(self.user_context)
            
            validation_result = validator.validate_create_data(record_data, validation_level)
            if not validation_result.success:
                return validation_result
            
            # Step 2 & 3: Create record using model method
            created_record = IdleResource.create_with_validation(
                record_data=record_data,
                user_context=self.user_context
            )
            
            return ServiceResponse.success_response(
                data={
                    'createdRecord': created_record.to_dict(),
                    'recordId': str(created_record.resource_id),
                    'auditTrailId': created_record.audit_trail_id,
                    'validationResults': validation_result.data
                },
                metadata={
                    'created_at': created_record.created_at.isoformat(),
                    'created_by': str(created_record.created_by_id)
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Resource creation failed: {str(e)}")
    
    def read_resource(self, record_id: str, include_metadata: bool = False) -> ServiceResponse:
        """
        Retrieve idle resource record.
        
        Maps to Service SVE-MDE-03-01-02: Read Idle Resource
        """
        return self.execute_with_audit(
            'read_resource',
            self._read_resource_impl,
            record_id=record_id,
            include_metadata=include_metadata
        )
    
    def _read_resource_impl(self, record_id: str, include_metadata: bool) -> ServiceResponse:
        """Internal resource reading implementation."""
        
        try:
            # Step 1: Access Control Check
            department_scope = self.get_user_department_scope()
            
            # Step 2: Retrieve Record
            try:
                resource = IdleResource.objects.get(resource_id=record_id)
                
                # Check department access
                if department_scope and str(resource.department_id) not in department_scope:
                    return ServiceResponse.error_response("Access denied to this resource", None)
                
            except IdleResource.DoesNotExist:
                return ServiceResponse.error_response("Resource not found")
            
            # Step 3: Apply Data Filtering based on user role
            filtered_data = self._apply_data_filtering(resource.to_dict())
            
            response_data = {
                'record': filtered_data,
                'accessLevel': self._get_access_level(resource)
            }
            
            if include_metadata:
                response_data['metadata'] = {
                    'created_at': resource.created_at.isoformat(),
                    'updated_at': resource.updated_at.isoformat(),
                    'version': resource.version,
                    'created_by': str(resource.created_by_id)
                }
            
            return ServiceResponse.success_response(data=response_data)
            
        except Exception as e:
            return ServiceResponse.error_response(f"Resource reading failed: {str(e)}")
    
    def update_resource(self, record_id: str, update_data: Dict, version: int) -> ServiceResponse:
        """
        Update existing idle resource record.
        
        Maps to Service SVE-MDE-03-01-03: Update Idle Resource
        """
        if not self.validate_user_permissions(['resource_update']):
            return ServiceResponse.error_response("Insufficient permissions for resource update")
        
        return self.execute_with_audit(
            'update_resource',
            self._update_resource_impl,
            record_id=record_id,
            update_data=update_data,
            version=version
        )
    
    def _update_resource_impl(self, record_id: str, update_data: Dict, version: int) -> ServiceResponse:
        """Internal resource update implementation."""
        
        try:
            # Step 1: Access Control and Validation
            department_scope = self.get_user_department_scope()
            
            # Step 2: Retrieve Current Record
            try:
                current_resource = IdleResource.objects.get(resource_id=record_id)
                
                # Check department access
                if department_scope and str(current_resource.department_id) not in department_scope:
                    return ServiceResponse.error_response("Access denied to this resource")
                
                # Check version for optimistic locking
                if current_resource.version != version:
                    return ServiceResponse.error_response("Version conflict - record was modified by another user")
                
            except IdleResource.DoesNotExist:
                return ServiceResponse.error_response("Resource not found")
            
            # Step 3: Update Record
            updated_resource = IdleResource.update_with_version_check(
                resource_id=record_id,
                update_data=update_data,
                current_version=version,
                user_context=self.user_context
            )
            
            # Step 4: Calculate changed fields
            changed_fields = self._calculate_changed_fields(current_resource.to_dict(), updated_resource.to_dict())
            
            return ServiceResponse.success_response(
                data={
                    'updatedRecord': updated_resource.to_dict(),
                    'auditTrailId': updated_resource.audit_trail_id,
                    'changedFields': changed_fields,
                    'newVersion': updated_resource.version
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Resource update failed: {str(e)}")
    
    def delete_resource(self, record_id: str, delete_type: str = 'soft', reason: str = None) -> ServiceResponse:
        """
        Delete idle resource record.
        
        Maps to Service SVE-MDE-03-01-04: Delete Idle Resource
        """
        if not self.validate_user_permissions(['resource_delete']):
            return ServiceResponse.error_response("Insufficient permissions for resource deletion")
        
        return self.execute_with_audit(
            'delete_resource',
            self._delete_resource_impl,
            record_id=record_id,
            delete_type=delete_type,
            reason=reason
        )
    
    def _delete_resource_impl(self, record_id: str, delete_type: str, reason: str) -> ServiceResponse:
        """Internal resource deletion implementation."""
        
        try:
            # Step 1: Access Control and Validation
            department_scope = self.get_user_department_scope()
            
            # Step 2: Retrieve Record for Deletion
            try:
                resource_to_delete = IdleResource.objects.get(resource_id=record_id)
                
                # Check department access
                if department_scope and str(resource_to_delete.department_id) not in department_scope:
                    return ServiceResponse.error_response("Access denied to this resource")
                
            except IdleResource.DoesNotExist:
                return ServiceResponse.error_response("Resource not found")
            
            # Step 3: Perform Deletion
            deleted_data = resource_to_delete.to_dict()  # Save data before deletion
            
            if delete_type == 'soft':
                resource_to_delete.soft_delete(
                    user_id=self.user_context.get('user_id'),
                    reason=reason
                )
                final_delete_type = 'soft'
            else:
                # Hard delete - check dependencies first
                if self._check_delete_dependencies(record_id):
                    return ServiceResponse.error_response("Cannot delete - record has dependencies")
                
                resource_to_delete.delete()
                final_delete_type = 'hard'
            
            return ServiceResponse.success_response(
                data={
                    'deleted': True,
                    'deletedRecord': deleted_data,
                    'auditTrailId': getattr(resource_to_delete, 'audit_trail_id', None),
                    'deletionType': final_delete_type
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Resource deletion failed: {str(e)}")
    
    def list_resources(self, filters: Dict = None, pagination: Dict = None, sorting: Dict = None) -> ServiceResponse:
        """
        Retrieve paginated list of idle resources.
        
        Maps to Service SVE-MDE-03-01-05: List Idle Resources
        """
        return self.execute_with_audit(
            'list_resources',
            self._list_resources_impl,
            filters=filters or {},
            pagination=pagination or {},
            sorting=sorting or {}
        )
    
    def _list_resources_impl(self, filters: Dict, pagination: Dict, sorting: Dict) -> ServiceResponse:
        """Internal resource listing implementation."""
        
        try:
            # Step 1: Apply Access Control Filters
            department_scope = self.get_user_department_scope()
            access_filters = {}
            
            if department_scope:
                access_filters['department_id__in'] = department_scope
            
            # Step 2: Retrieve Record List
            queryset = IdleResource.list_with_filters(
                filters={**filters, **access_filters},
                user_context=self.user_context
            )
            
            # Apply sorting
            if sorting:
                sort_field = sorting.get('field', 'created_at')
                sort_order = 'desc' if sorting.get('order') == 'desc' else 'asc'
                if sort_order == 'desc':
                    sort_field = f'-{sort_field}'
                queryset = queryset.order_by(sort_field)
            
            # Apply pagination
            page = pagination.get('page', 1)
            page_size = pagination.get('page_size', 20)
            offset = (page - 1) * page_size
            
            total_count = queryset.count()
            records = list(queryset[offset:offset + page_size])
            
            # Step 3: Apply Data Filtering
            filtered_records = [self._apply_data_filtering(record.to_dict()) for record in records]
            
            return ServiceResponse.success_response(
                data={
                    'records': filtered_records,
                    'totalCount': total_count,
                    'pageInfo': {
                        'page': page,
                        'pageSize': page_size,
                        'totalPages': (total_count + page_size - 1) // page_size,
                        'hasNext': offset + page_size < total_count,
                        'hasPrevious': page > 1
                    },
                    'appliedFilters': {**filters, **access_filters}
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Resource listing failed: {str(e)}")
    
    def _apply_data_filtering(self, record_data: Dict) -> Dict:
        """Apply role-based field filtering to record data."""
        user_role = self.user_context.get('role', 'user')
        
        # Define field access by role
        if user_role == 'admin':
            return record_data  # Admin sees all fields
        elif user_role == 'manager':
            # Manager doesn't see sensitive personal data
            filtered_data = record_data.copy()
            filtered_data.pop('personal_phone', None)
            filtered_data.pop('personal_email', None)
            return filtered_data
        else:
            # Regular user sees limited fields
            allowed_fields = ['resource_id', 'employee_name', 'job_rank', 'department_name', 'status']
            return {field: record_data.get(field) for field in allowed_fields if field in record_data}
    
    def _get_access_level(self, resource) -> str:
        """Determine user's access level to the resource."""
        user_role = self.user_context.get('role', 'user')
        user_dept = self.user_context.get('department_id')
        
        if user_role == 'admin':
            return 'full'
        elif user_role == 'manager' and str(resource.department_id) == str(user_dept):
            return 'write'
        elif str(resource.department_id) == str(user_dept):
            return 'read'
        else:
            return 'none'
    
    def _calculate_changed_fields(self, old_data: Dict, new_data: Dict) -> List[str]:
        """Calculate which fields were changed in the update."""
        changed_fields = []
        for field, new_value in new_data.items():
            if field in old_data and old_data[field] != new_value:
                changed_fields.append(field)
        return changed_fields
    
    def _check_delete_dependencies(self, record_id: str) -> bool:
        """Check if record has dependencies preventing deletion."""
        # Implementation would check for foreign key references
        # This is a placeholder - actual implementation would check related models
        return False
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate resource CRUD operations require authenticated user."""
        return self.user_context.get('user_id') is not None
```

## 🔍 Search and Validation Services

### Search Service
Maps to SVE-MDE-03-02 operations:

```python
# services/resource_management/search_service.py
from typing import Dict, List, Any, Optional
from ..base import BaseService, ServiceResponse
from ...resource_management.models import IdleResource

class ResourceSearchService(BaseService):
    """
    Resource Search Service implementing SVE-MDE-03-02 operations
    Handles advanced search, full-text search, and faceted search.
    """
    
    def advanced_search(self, search_criteria: Dict, filters: Dict = None, 
                       sort_options: Dict = None, pagination: Dict = None) -> ServiceResponse:
        """
        Perform complex multi-field search with filters and sorting.
        
        Maps to Service SVE-MDE-03-02-01: Advanced Search
        """
        return self.execute_with_audit(
            'advanced_search',
            self._advanced_search_impl,
            search_criteria=search_criteria,
            filters=filters or {},
            sort_options=sort_options or {},
            pagination=pagination or {}
        )
    
    def _advanced_search_impl(self, search_criteria: Dict, filters: Dict, 
                             sort_options: Dict, pagination: Dict) -> ServiceResponse:
        """Internal advanced search implementation."""
        
        try:
            # Step 1: Validate Search Criteria
            validation_errors = self._validate_search_criteria(search_criteria)
            if validation_errors:
                return ServiceResponse.error_response(validation_errors)
            
            # Step 2: Apply Department Access Control
            department_scope = self.get_user_department_scope()
            if department_scope:
                filters['department_id__in'] = department_scope
            
            # Step 3: Execute Advanced Search
            queryset = IdleResource.objects.all()
            
            # Apply search criteria
            for field, criteria in search_criteria.items():
                if criteria.get('value'):
                    operator = criteria.get('operator', 'exact')
                    value = criteria['value']
                    
                    if operator == 'contains':
                        queryset = queryset.filter(**{f"{field}__icontains": value})
                    elif operator == 'exact':
                        queryset = queryset.filter(**{field: value})
                    elif operator == 'range':
                        if criteria.get('min_value'):
                            queryset = queryset.filter(**{f"{field}__gte": criteria['min_value']})
                        if criteria.get('max_value'):
                            queryset = queryset.filter(**{f"{field}__lte": criteria['max_value']})
                    elif operator == 'in':
                        queryset = queryset.filter(**{f"{field}__in": value})
            
            # Apply additional filters
            for field, value in filters.items():
                queryset = queryset.filter(**{field: value})
            
            # Apply sorting
            if sort_options.get('field'):
                sort_field = sort_options['field']
                if sort_options.get('order') == 'desc':
                    sort_field = f'-{sort_field}'
                queryset = queryset.order_by(sort_field)
            
            # Get total count before pagination
            total_count = queryset.count()
            
            # Apply pagination
            page = pagination.get('page', 1)
            page_size = pagination.get('page_size', 20)
            offset = (page - 1) * page_size
            
            search_results = list(queryset[offset:offset + page_size])
            
            # Step 4: Generate Faceted Results
            facets = self._generate_facets(queryset)
            
            # Step 5: Generate Search Suggestions
            suggestions = self._generate_search_suggestions(search_criteria, total_count)
            
            return ServiceResponse.success_response(
                data={
                    'searchResults': [result.to_dict() for result in search_results],
                    'totalCount': total_count,
                    'facets': facets,
                    'queryMetadata': {
                        'execution_time': '50ms',  # Would be calculated
                        'query_complexity': 'medium'
                    },
                    'suggestions': suggestions
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Advanced search failed: {str(e)}")
    
    def full_text_search(self, search_query: str, search_mode: str = 'standard',
                        filters: Dict = None, pagination: Dict = None) -> ServiceResponse:
        """
        Execute full-text search across searchable fields.
        
        Maps to Service SVE-MDE-03-02-02: Full Text Search
        """
        return self.execute_with_audit(
            'full_text_search',
            self._full_text_search_impl,
            search_query=search_query,
            search_mode=search_mode,
            filters=filters or {},
            pagination=pagination or {}
        )
    
    def _full_text_search_impl(self, search_query: str, search_mode: str,
                              filters: Dict, pagination: Dict) -> ServiceResponse:
        """Internal full-text search implementation."""
        
        try:
            # Step 1: Parse and Validate Query
            if not search_query.strip():
                return ServiceResponse.error_response("Search query cannot be empty")
            
            # Step 2: Apply Access Control
            department_scope = self.get_user_department_scope()
            if department_scope:
                filters['department_id__in'] = department_scope
            
            # Step 3: Execute Full Text Search
            searchable_fields = ['employee_name', 'job_rank', 'skills', 'work_location']
            queryset = IdleResource.objects.none()
            
            for field in searchable_fields:
                if search_mode == 'fuzzy':
                    # Implement fuzzy search logic
                    field_queryset = IdleResource.objects.filter(**{f"{field}__icontains": search_query})
                elif search_mode == 'exact':
                    field_queryset = IdleResource.objects.filter(**{f"{field}__iexact": search_query})
                else:  # standard
                    field_queryset = IdleResource.objects.filter(**{f"{field}__icontains": search_query})
                
                queryset = queryset.union(field_queryset)
            
            # Apply additional filters
            for field, value in filters.items():
                queryset = queryset.filter(**{field: value})
            
            # Order by relevance (simplified - would need proper text ranking)
            queryset = queryset.order_by('employee_name')
            
            # Get total count
            total_count = queryset.count()
            
            # Apply pagination
            page = pagination.get('page', 1)
            page_size = pagination.get('page_size', 20)
            offset = (page - 1) * page_size
            
            search_results = list(queryset[offset:offset + page_size])
            
            # Step 4: Generate Related Terms
            related_terms = self._generate_related_terms(search_query)
            
            return ServiceResponse.success_response(
                data={
                    'searchResults': [result.to_dict() for result in search_results],
                    'totalCount': total_count,
                    'searchHighlights': self._generate_highlights(search_results, search_query),
                    'relatedTerms': related_terms
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Full text search failed: {str(e)}")
    
    def faceted_search(self, base_criteria: Dict = None, facet_fields: List[str] = None,
                      selected_facets: Dict = None) -> ServiceResponse:
        """
        Provide faceted search results with aggregated counts.
        
        Maps to Service SVE-MDE-03-02-03: Faceted Search
        """
        return self.execute_with_audit(
            'faceted_search',
            self._faceted_search_impl,
            base_criteria=base_criteria or {},
            facet_fields=facet_fields or [],
            selected_facets=selected_facets or {}
        )
    
    def _faceted_search_impl(self, base_criteria: Dict, facet_fields: List[str],
                            selected_facets: Dict) -> ServiceResponse:
        """Internal faceted search implementation."""
        
        try:
            # Step 1: Validate Facet Configuration
            default_facets = ['department_name', 'job_rank', 'status', 'work_location']
            if not facet_fields:
                facet_fields = default_facets
            
            # Step 2: Apply Base Criteria and Access Control
            department_scope = self.get_user_department_scope()
            queryset = IdleResource.objects.all()
            
            if department_scope:
                queryset = queryset.filter(department_id__in=department_scope)
            
            # Apply base criteria
            for field, value in base_criteria.items():
                queryset = queryset.filter(**{field: value})
            
            # Apply selected facets
            for facet_field, facet_values in selected_facets.items():
                if isinstance(facet_values, list):
                    queryset = queryset.filter(**{f"{facet_field}__in": facet_values})
                else:
                    queryset = queryset.filter(**{facet_field: facet_values})
            
            # Step 3: Generate Faceted Aggregations
            facet_results = {}
            for facet_field in facet_fields:
                facet_counts = self._calculate_facet_counts(queryset, facet_field)
                facet_results[facet_field] = facet_counts
            
            filtered_count = queryset.count()
            
            # Step 4: Calculate Filter Impact
            available_filters = self._calculate_filter_impact(queryset, facet_fields)
            
            return ServiceResponse.success_response(
                data={
                    'facetResults': facet_results,
                    'filteredCount': filtered_count,
                    'availableFilters': available_filters,
                    'facetHierarchy': self._build_facet_hierarchy(facet_results)
                }
            )
            
        except Exception as e:
            return ServiceResponse.error_response(f"Faceted search failed: {str(e)}")
    
    def _validate_search_criteria(self, criteria: Dict) -> List[str]:
        """Validate search criteria format."""
        errors = []
        allowed_fields = ['employee_name', 'job_rank', 'department_name', 'status', 'work_location']
        
        for field, criteria_data in criteria.items():
            if field not in allowed_fields:
                errors.append(f"Search field '{field}' is not allowed")
            
            if not isinstance(criteria_data, dict):
                errors.append(f"Search criteria for '{field}' must be an object")
        
        return errors
    
    def _generate_facets(self, queryset) -> Dict:
        """Generate faceted aggregations from queryset."""
        facets = {}
        facet_fields = ['department_name', 'job_rank', 'status']
        
        for field in facet_fields:
            facets[field] = self._calculate_facet_counts(queryset, field)
        
        return facets
    
    def _calculate_facet_counts(self, queryset, facet_field: str) -> Dict:
        """Calculate counts for each facet value."""
        from django.db.models import Count
        
        counts = queryset.values(facet_field).annotate(count=Count('resource_id')).order_by('-count')
        return {item[facet_field]: item['count'] for item in counts}
    
    def _generate_search_suggestions(self, search_criteria: Dict, result_count: int) -> List[str]:
        """Generate search improvement suggestions."""
        suggestions = []
        
        if result_count == 0:
            suggestions.append("Try broadening your search criteria")
            suggestions.append("Check spelling of search terms")
        elif result_count > 1000:
            suggestions.append("Consider adding more specific filters")
            suggestions.append("Use advanced search for better precision")
        
        return suggestions
    
    def _generate_highlights(self, results: List, search_query: str) -> Dict:
        """Generate search term highlights in results."""
        highlights = {}
        search_terms = search_query.lower().split()
        
        for result in results:
            result_highlights = []
            result_dict = result.to_dict()
            
            for field, value in result_dict.items():
                if isinstance(value, str):
                    for term in search_terms:
                        if term in value.lower():
                            result_highlights.append(f"{field}: highlighted '{term}' in '{value}'")
            
            highlights[str(result.resource_id)] = result_highlights
        
        return highlights
    
    def _generate_related_terms(self, search_query: str) -> List[str]:
        """Generate related search terms."""
        # This would typically use a more sophisticated algorithm
        # For now, return some basic related terms
        related_terms = []
        
        if 'engineer' in search_query.lower():
            related_terms.extend(['developer', 'programmer', 'software engineer'])
        if 'manager' in search_query.lower():
            related_terms.extend(['supervisor', 'lead', 'director'])
        
        return related_terms[:5]  # Limit to 5 suggestions
    
    def _calculate_filter_impact(self, queryset, facet_fields: List[str]) -> List[Dict]:
        """Calculate the impact of applying each available filter."""
        available_filters = []
        
        for field in facet_fields:
            field_values = queryset.values_list(field, flat=True).distinct()
            for value in field_values:
                if value:  # Skip null values
                    impact_count = queryset.filter(**{field: value}).count()
                    available_filters.append({
                        'field': field,
                        'value': value,
                        'impact_count': impact_count
                    })
        
        return available_filters
    
    def _build_facet_hierarchy(self, facet_results: Dict) -> Dict:
        """Build hierarchical relationships between facets."""
        hierarchy = {}
        
        # Example: Department -> Job Rank hierarchy
        if 'department_name' in facet_results and 'job_rank' in facet_results:
            hierarchy['department_job_rank'] = {
                'parent': 'department_name',
                'child': 'job_rank',
                'relationship': 'contains'
            }
        
        return hierarchy
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate search operations require authenticated user."""
        return self.user_context.get('user_id') is not None
```

## 🔧 Integration with Django REST Framework

### ViewSet Integration
```python
# views.py (example for authentication app)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .services.authentication.auth_service import AuthenticationService
from .services.authentication.session_service import SessionManagementService

class AuthenticationViewSet(viewsets.ViewSet):
    """Authentication API ViewSet using service layer."""
    
    @action(detail=False, methods=['post'])
    def authenticate(self, request):
        """Authenticate user credentials."""
        
        # Extract request data
        username = request.data.get('username')
        password = request.data.get('password')
        language = request.data.get('language', 'en')
        
        # Prepare user context
        user_context = {
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        }
        
        # Call authentication service
        auth_service = AuthenticationService(user_context)
        result = auth_service.authenticate_user(username, password, language)
        
        if result.success:
            # Create session if authentication successful
            session_service = SessionManagementService(user_context)
            session_result = session_service.create_session(
                user_id=result.data['userId'],
                user_profile=result.data['userProfile'],
                remember_me=request.data.get('remember_me', False)
            )
            
            if session_result.success:
                # Combine authentication and session data
                response_data = {
                    **result.data,
                    **session_result.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(session_result.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def validate_session(self, request):
        """Validate user session."""
        
        access_token = request.data.get('access_token')
        if not access_token:
            return Response(['Access token required'], status=status.HTTP_400_BAD_REQUEST)
        
        session_service = SessionManagementService()
        result = session_service.validate_session(access_token)
        
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(result.errors, status=status.HTTP_401_UNAUTHORIZED)

class ResourceViewSet(viewsets.ViewSet):
    """Resource management API ViewSet using service layer."""
    
    def create(self, request):
        """Create new resource."""
        
        user_context = self._get_user_context(request)
        crud_service = ResourceCRUDService(user_context)
        
        result = crud_service.create_resource(
            record_data=request.data,
            validation_level=request.query_params.get('validation_level', 'full')
        )
        
        if result.success:
            return Response(result.data, status=status.HTTP_201_CREATED)
        else:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Retrieve resource by ID."""
        
        user_context = self._get_user_context(request)
        crud_service = ResourceCRUDService(user_context)
        
        result = crud_service.read_resource(
            record_id=pk,
            include_metadata=request.query_params.get('include_metadata', 'false') == 'true'
        )
        
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(result.errors, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Search resources."""
        
        user_context = self._get_user_context(request)
        search_service = ResourceSearchService(user_context)
        
        search_type = request.data.get('search_type', 'advanced')
        
        if search_type == 'full_text':
            result = search_service.full_text_search(
                search_query=request.data.get('query', ''),
                search_mode=request.data.get('mode', 'standard'),
                filters=request.data.get('filters', {}),
                pagination=request.data.get('pagination', {})
            )
        else:
            result = search_service.advanced_search(
                search_criteria=request.data.get('criteria', {}),
                filters=request.data.get('filters', {}),
                sort_options=request.data.get('sorting', {}),
                pagination=request.data.get('pagination', {})
            )
        
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_user_context(self, request) -> Dict:
        """Extract user context from request."""
        # This would typically extract from JWT token or session
        return {
            'user_id': getattr(request.user, 'user_id', None),
            'username': getattr(request.user, 'username', None),
            'role': getattr(request.user, 'role', 'user'),
            'department_id': getattr(request.user, 'department_id', None),
            'permissions': getattr(request.user, 'permissions', []),
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        }
```

## 📝 Implementation Summary

The service layer architecture provides:

1. **Clear Separation of Concerns**: Business logic is separated from API presentation and data access
2. **Standardized Responses**: All services return consistent ServiceResponse objects
3. **Comprehensive Audit Trail**: All operations are automatically logged for audit purposes
4. **Role-Based Access Control**: Fine-grained permissions and data filtering
5. **Error Handling**: Centralized exception handling and user-friendly error messages
6. **Validation Framework**: Multi-level validation with business rules
7. **Transaction Management**: Atomic operations with rollback capabilities
8. **Performance Optimization**: Efficient querying and pagination
9. **Security Integration**: Built-in security policy enforcement
10. **Extensibility**: Easy to add new services and extend existing functionality

This architecture maps directly to the service design documents while maintaining Django REST Framework best practices and providing a robust foundation for the application's business logic.