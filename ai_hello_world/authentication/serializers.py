"""
Authentication API Serializers

Defines request/response serializers for authentication endpoints
with fixed payload structures as specified.
"""

from rest_framework import serializers
from typing import Dict, Any


class LoginRequestSerializer(serializers.Serializer):
    """
    Login request payload serializer
    """
    username = serializers.CharField(
        max_length=100, 
        required=True,
        help_text="Username or email address"
    )
    password = serializers.CharField(
        max_length=255, 
        required=True, 
        write_only=True,
        help_text="User password"
    )
    language = serializers.ChoiceField(
        choices=['en', 'vi', 'ja', 'ko'],
        default='en',
        required=False,
        help_text="Preferred language for the session"
    )
    remember_me = serializers.BooleanField(
        default=False,
        required=False,
        help_text="Keep session active for extended period"
    )


class UserProfileSerializer(serializers.Serializer):
    """
    User profile information in login response
    """
    user_id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    language = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True, allow_null=True)
    avatar_url = serializers.URLField(read_only=True, allow_null=True)
    timezone = serializers.CharField(read_only=True)
    date_format = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)


class RoleSerializer(serializers.Serializer):
    """
    User role information
    """
    role_id = serializers.UUIDField(read_only=True)
    role_name = serializers.CharField(read_only=True)
    role_description = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class PermissionSerializer(serializers.Serializer):
    """
    User permission information
    """
    permission_id = serializers.UUIDField(read_only=True)
    permission_name = serializers.CharField(read_only=True)
    permission_description = serializers.CharField(read_only=True)
    resource_type = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)


class DepartmentSerializer(serializers.Serializer):
    """
    Department information
    """
    department_id = serializers.UUIDField(read_only=True)
    department_name = serializers.CharField(read_only=True)
    parent_department_id = serializers.UUIDField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)


class RoleInfoSerializer(serializers.Serializer):
    """
    Complete role and permission information
    """
    roles = RoleSerializer(many=True, read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True)
    department = DepartmentSerializer(read_only=True, allow_null=True)
    primary_role = serializers.CharField(read_only=True, allow_null=True)


class LoginResponseSerializer(serializers.Serializer):
    """
    Login response payload serializer
    """
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    
    # Authentication result
    is_valid = serializers.BooleanField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    
    # User information
    user_profile = UserProfileSerializer(read_only=True)
    role_info = RoleInfoSerializer(read_only=True)
    
    # Session information
    session_id = serializers.UUIDField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)
    
    # Metadata
    last_login_time = serializers.DateTimeField(read_only=True, allow_null=True)
    login_time = serializers.DateTimeField(read_only=True)
    authentication_method = serializers.CharField(read_only=True)


class LoginErrorResponseSerializer(serializers.Serializer):
    """
    Login error response payload serializer
    """
    success = serializers.BooleanField(read_only=True, default=False)
    message = serializers.CharField(read_only=True)
    errors = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )
    error_code = serializers.CharField(read_only=True)
    
    # Security information for failed attempts
    remaining_attempts = serializers.IntegerField(read_only=True, allow_null=True)
    lockout_time = serializers.IntegerField(read_only=True, allow_null=True)
    retry_after = serializers.IntegerField(read_only=True, allow_null=True)


class LogoutRequestSerializer(serializers.Serializer):
    """
    Logout request payload serializer
    """
    session_id = serializers.UUIDField(required=True)
    access_token = serializers.CharField(required=True)


class LogoutResponseSerializer(serializers.Serializer):
    """
    Logout response payload serializer
    """
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    logged_out_at = serializers.DateTimeField(read_only=True)


class ValidateSessionRequestSerializer(serializers.Serializer):
    """
    Session validation request payload serializer
    """
    access_token = serializers.CharField(required=True)


class ValidateSessionResponseSerializer(serializers.Serializer):
    """
    Session validation response payload serializer
    """
    success = serializers.BooleanField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    
    # Session information if valid
    user_id = serializers.UUIDField(read_only=True, allow_null=True)
    session_id = serializers.UUIDField(read_only=True, allow_null=True)
    expires_in = serializers.IntegerField(read_only=True, allow_null=True)
    user_profile = UserProfileSerializer(read_only=True, allow_null=True)


class RefreshTokenRequestSerializer(serializers.Serializer):
    """
    Token refresh request payload serializer
    """
    refresh_token = serializers.CharField(required=True)


class RefreshTokenResponseSerializer(serializers.Serializer):
    """
    Token refresh response payload serializer
    """
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    
    # New tokens
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)
    
    # Session information
    session_id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)