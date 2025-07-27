"""
Authentication Service implementing SVE-MDE-01-01-01

This service handles user credential validation and authentication logic
according to the service design specification.

Source: DD/MDE-01/03-service/SVE-MDE-01-01_v0.1.md
Business Logic: User authentication with credential validation and security enforcement
"""

from typing import Dict, Optional
from django.utils import timezone
from ..base import BaseService, ServiceResponse
from ..exceptions import AuthenticationException, ValidationException
from ...authentication.models import User, LoginAttempt


class AuthenticationService(BaseService):
    """
    Authentication Service implementing SVE-MDE-01-01-01
    Handles user credential validation and authentication logic.
    """
    
    def authenticate_user(self, username: str, password: str, language: str = 'en') -> ServiceResponse:
        """
        Authenticate user credentials and establish session.
        
        Maps to Service SVE-MDE-01-01-01: Authentication Service
        Implements Steps 1-6 from service design document.
        
        Args:
            username: Username or email address
            password: User password for verification
            language: User language preference
            
        Returns:
            ServiceResponse with authentication result including user profile and roles
        """
        return self.execute_with_audit(
            'authenticate_user',
            self._authenticate_user_impl,
            username=username,
            password=password,
            language=language
        )
    
    def _authenticate_user_impl(self, username: str, password: str, language: str) -> ServiceResponse:
        """Internal authentication implementation following service design steps."""
        
        # Step 1: Validate input parameters and prepare authentication request
        validation_errors = self._validate_authentication_inputs(username, password, language)
        if validation_errors:
            return ServiceResponse.validation_response(validation_errors)
        
        try:
            # Step 2: Retrieve user credentials and profile information
            user_data = self._get_user_credentials_and_profile(username)
            if not user_data['user_exists']:
                self._log_failed_attempt(username, 'user_not_found')
                return ServiceResponse.error_response("Invalid credentials")
            
            if not user_data['is_active']:
                self._log_failed_attempt(username, 'account_inactive')
                return ServiceResponse.error_response("Account is inactive")
            
            user = user_data['user']
            
            # Step 3: Verify provided password against stored hash
            if not self._verify_password(username, password):
                self._log_failed_attempt(username, 'invalid_password')
                return ServiceResponse.error_response("Invalid credentials")
            
            # Step 4: Retrieve user roles and permissions for session establishment
            roles_and_permissions = self._get_user_roles_and_permissions(user.user_id)
            
            # Step 5: Update last login time and authentication audit trail
            previous_login = user.last_login
            self._update_last_login(user.user_id)
            
            # Step 6: Return comprehensive authentication result
            return self._compile_authentication_result(
                user=user,
                user_profile=user_data['user_profile'],
                roles_data=roles_and_permissions['roles'],
                permissions_data=roles_and_permissions['permissions'],
                department_data=roles_and_permissions['department'],
                previous_login=previous_login,
                language=language
            )
            
        except Exception as e:
            self._log_failed_attempt(username, 'system_error')
            return ServiceResponse.error_response(f"Authentication failed: {str(e)}")
    
    def _validate_authentication_inputs(self, username: str, password: str, language: str) -> list:
        """Step 1: Validate input parameters."""
        errors = []
        
        if not username or not username.strip():
            errors.append("Username is required")
        elif len(username) > 100:
            errors.append("Username cannot exceed 100 characters")
        
        if not password or not password.strip():
            errors.append("Password is required")
        elif len(password) > 255:
            errors.append("Password cannot exceed 255 characters")
        
        # Validate language enum values
        valid_languages = ['en', 'vi', 'ja', 'ko']
        if language and language not in valid_languages:
            errors.append(f"Language must be one of: {', '.join(valid_languages)}")
        
        return errors
    
    def _get_user_credentials_and_profile(self, username: str) -> Dict:
        """Step 2: Retrieve user credentials and profile information using DAO."""
        try:
            # Use the DAO method we implemented in the User model
            user_data = User.get_user_with_roles(username)
            return user_data
            
        except Exception as e:
            return {
                'user_exists': False,
                'is_active': False,
                'user': None,
                'user_profile': None,
                'error': str(e)
            }
    
    def _verify_password(self, username: str, password: str) -> bool:
        """Step 3: Verify provided password against stored hash."""
        try:
            # Use the DAO method we implemented in the User model
            return User.authenticate_user(username, password)
        except Exception:
            return False
    
    def _get_user_roles_and_permissions(self, user_id: str) -> Dict:
        """Step 4: Retrieve user roles and permissions."""
        try:
            # Get user with all related data
            user = User.objects.select_related('profile', 'profile__department').prefetch_related(
                'user_roles__role__role_permissions__permission'
            ).get(user_id=user_id)
            
            # Extract roles
            roles = []
            permissions = []
            
            for user_role in user.user_roles.all():
                role = user_role.role
                roles.append({
                    'role_id': str(role.role_id),
                    'role_name': role.role_name,
                    'role_description': role.role_description,
                    'is_active': role.is_active
                })
                
                # Extract permissions for this role
                for role_permission in role.role_permissions.all():
                    permission = role_permission.permission
                    if permission.is_active:
                        permissions.append({
                            'permission_id': str(permission.permission_id),
                            'permission_name': permission.permission_name,
                            'permission_description': permission.permission_description,
                            'resource_type': permission.resource_type,
                            'action': permission.action
                        })
            
            # Remove duplicate permissions
            unique_permissions = []
            seen_permissions = set()
            for perm in permissions:
                perm_key = (perm['permission_name'], perm['resource_type'], perm['action'])
                if perm_key not in seen_permissions:
                    seen_permissions.add(perm_key)
                    unique_permissions.append(perm)
            
            # Extract department information
            department_data = None
            if user.profile and user.profile.department:
                dept = user.profile.department
                department_data = {
                    'department_id': str(dept.department_id),
                    'department_name': dept.department_name,
                    'parent_department_id': str(dept.parent_department_id) if dept.parent_department_id else None,
                    'is_active': dept.is_active
                }
            
            return {
                'roles': roles,
                'permissions': unique_permissions,
                'department': department_data
            }
            
        except Exception as e:
            return {
                'roles': [],
                'permissions': [],
                'department': None,
                'error': str(e)
            }
    
    def _update_last_login(self, user_id: str) -> Optional[timezone.datetime]:
        """Step 5: Update last login time."""
        try:
            user = User.objects.get(user_id=user_id)
            previous_login = user.last_login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return previous_login
        except Exception:
            return None
    
    def _compile_authentication_result(self, user, user_profile: Dict, roles_data: list, 
                                     permissions_data: list, department_data: Dict, 
                                     previous_login: timezone.datetime, language: str) -> ServiceResponse:
        """Step 6: Compile comprehensive authentication result."""
        
        # Build user profile information
        profile_info = {
            'user_id': str(user.user_id),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language': language,
            'is_active': user.is_active,
            'is_verified': user.is_verified
        }
        
        # Add profile details if available
        if user_profile:
            profile_info.update({
                'phone': user_profile.get('phone'),
                'avatar_url': user_profile.get('avatar_url'),
                'timezone': user_profile.get('timezone', 'UTC'),
                'date_format': user_profile.get('date_format', 'YYYY-MM-DD')
            })
        
        # Build role information
        role_info = {
            'roles': roles_data,
            'permissions': permissions_data,
            'department': department_data,
            'primary_role': roles_data[0]['role_name'] if roles_data else None
        }
        
        # Build response data
        response_data = {
            'isValid': True,
            'userId': str(user.user_id),
            'userProfile': profile_info,
            'roleInfo': role_info,
            'message': 'Authentication successful',
            'lastLoginTime': previous_login.isoformat() if previous_login else None
        }
        
        # Build metadata
        metadata = {
            'login_time': timezone.now().isoformat(),
            'session_required': True,
            'authentication_method': 'password',
            'ip_address': self.user_context.get('ip_address'),
            'user_agent': self.user_context.get('user_agent')
        }
        
        return ServiceResponse.success_response(data=response_data, metadata=metadata)
    
    def _log_failed_attempt(self, username: str, failure_reason: str):
        """Log failed authentication attempt."""
        try:
            LoginAttempt.log_security_event(
                username=username,
                event_type='failed_login',
                ip_address=self.user_context.get('ip_address'),
                user_agent=self.user_context.get('user_agent'),
                details={'failure_reason': failure_reason}
            )
        except Exception:
            # Don't let audit logging failures affect authentication
            pass
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Validate authentication operations."""
        # Authentication operations don't require pre-existing authentication
        return True


class UserProfileService(BaseService):
    """Service for user profile operations."""
    
    def get_user_profile(self, user_id: str) -> ServiceResponse:
        """Get comprehensive user profile information."""
        try:
            user = User.objects.select_related('profile', 'profile__department').get(user_id=user_id)
            
            profile_data = {
                'user_id': str(user.user_id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'date_joined': user.date_joined.isoformat(),
            }
            
            if user.profile:
                profile = user.profile
                profile_data.update({
                    'phone': profile.phone,
                    'avatar_url': profile.avatar_url,
                    'bio': profile.bio,
                    'timezone': profile.timezone,
                    'language': profile.language,
                    'date_format': profile.date_format,
                    'department': {
                        'department_id': str(profile.department.department_id),
                        'department_name': profile.department.department_name
                    } if profile.department else None
                })
            
            return ServiceResponse.success_response(data=profile_data)
            
        except User.DoesNotExist:
            return ServiceResponse.error_response("User not found")
        except Exception as e:
            return ServiceResponse.error_response(f"Failed to retrieve user profile: {str(e)}")
    
    def validate_operation_context(self, operation: str, **kwargs) -> bool:
        """Profile operations require authenticated user."""
        return self.user_context.get('user_id') is not None