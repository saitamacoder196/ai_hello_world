"""
MANDATORY DOCSTRING - User model for authentication and credential management.

Source Information (REQUIRED):
- Database Table: users
- Database Design: DD/database_v0.1.md - Section: users
- DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
- Business Module: authentication

Business Rules (REQUIRED):
    - Unique username and email required for lookup and login
    - Password hash must be stored securely
    - Account status (is_active, is_deleted) controls authentication
    - Audit fields for login and update tracking

Relationships (REQUIRED):
    - Related to Profile via one-to-one (profile)
    - Related to Department via foreign key (department)
    - Related to Role via many-to-many (roles through UserRole)

Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
"""
import uuid
from django.db import models

class Department(models.Model):
    """
    MANDATORY DOCSTRING - Department model for organizational units.
    Source Information:
    - Database Table: departments
    - Database Design: DD/database_v0.1.md - Section: departments
    - DAO Specification: (future)
    - Business Module: authentication
    Business Rules:
        - Department name must be unique
        - Can have parent department (hierarchy)
        - Can have manager (FK to User)
    Relationships:
        - Related to User via department FK
        - Related to itself via parent_department FK
    Verification Source: DD/database_v0.1.md
    """
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=100)
    parent_department = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_departments')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.department_name
    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

class User(models.Model):
    """
    MANDATORY DOCSTRING - User model for authentication and credential management.
    Source Information:
    - Database Table: users
    - Database Design: DD/database_v0.1.md - Section: users
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    Business Rules:
        - Unique username and email required for lookup and login
        - Password hash must be stored securely
        - Account status (is_active, is_deleted) controls authentication
        - Audit fields for login and update tracking
    Relationships:
        - Related to Profile via one-to-one (profile)
        - Related to Department via foreign key (department)
        - Related to Role via many-to-many (roles through UserRole)
    Verification Source: This information can be verified by checking
        the referenced DAO specification and database design documents.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    last_login_time = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    login_count = models.PositiveIntegerField(default=0)
    password_updated_time = models.DateTimeField(null=True, blank=True)
    language_preference = models.CharField(max_length=20, default='en')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def update_last_login(self, login_time):
        """
        Update last login timestamp and increment login count.
        Based on: DAO-MDE-01-01_v0.1.md - Step 3: Update Last Login Operation
        """
        self.last_login_time = login_time
        self.login_count += 1
        self.save()
    def update_password(self, password_hash):
        """
        Update password hash and password_updated_time.
        Based on: DAO-MDE-01-01_v0.1.md - Step 4: Update Password Operation
        """
        self.password_hash = password_hash
        self.password_updated_time = timezone.now()
        self.save()

class Profile(models.Model):
    """
    MANDATORY DOCSTRING - Profile model for extended user information.
    Source Information:
    - Database Table: profiles
    - Database Design: DD/database_v0.1.md - Section: profiles
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    Business Rules:
        - Each user has one profile
        - Profile contains first name, last name, phone number
    Relationships:
        - Related to User via one-to-one (user)
    Verification Source: DD/database_v0.1.md, DAO-MDE-01-01_v0.1.md
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Role(models.Model):
    """
    MANDATORY DOCSTRING - Role model for user authorization.
    Source Information:
    - Database Table: roles
    - Database Design: DD/database_v0.1.md - Section: roles
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    Business Rules:
        - Role name must be unique
        - Role can have multiple permissions
    Relationships:
        - Related to User via UserRole
        - Related to Permission via RolePermission
    Verification Source: DD/database_v0.1.md, DAO-MDE-01-01_v0.1.md
    """
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=100, unique=True)
    role_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.role_name
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

class Permission(models.Model):
    """
    MANDATORY DOCSTRING - Permission model for access control.
    Source Information:
    - Database Table: permissions
    - Database Design: DD/database_v0.1.md - Section: permissions
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    Business Rules:
        - Permission name must be unique
    Relationships:
        - Related to Role via RolePermission
    Verification Source: DD/database_v0.1.md, DAO-MDE-01-01_v0.1.md
    """
    permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.permission_name
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

class UserRole(models.Model):
    """
    MANDATORY DOCSTRING - UserRole model for role assignment to users.
    Source Information:
    - Database Table: user_roles
    - Database Design: DD/database_v0.1.md - Section: user_roles
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    Business Rules:
        - Each user can have multiple roles
        - Each role can be assigned to multiple users
        - Assignment date and status tracked
    Relationships:
        - Related to User via FK
        - Related to Role via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-01-01_v0.1.md
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'

    """
    MANDATORY DOCSTRING - RolePermission model for permission assignment to roles.
    Source Information:
    - Database Table: role_permissions
    - Database Design: DD/database_v0.1.md - Section: role_permissions
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    Business Rules:
        - Each role can have multiple permissions
        - Each permission can be assigned to multiple roles
    Relationships:
        - Related to Role via FK
        - Related to Permission via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-01-01_v0.1.md
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    class Meta:
        db_table = 'role_permissions'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'

# --- SESSION MANAGEMENT ---
class UserSession(models.Model):
    """
    MANDATORY DOCSTRING - UserSession model for session management and tracking.
    
    Source Information (REQUIRED):
    - Database Table: user_sessions
    - Database Design: DD/database_v0.1.md - Section: user_sessions
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-02_v0.1.md
    - Business Module: authentication
    
    Business Rules (REQUIRED):
        - Each session must be linked to a user
        - Access/refresh tokens must be stored securely
        - Session validity, expiration, and audit tracked
        - Support for remember_me, IP, user_agent, and activity
    
    Relationships (REQUIRED):
        - Related to User via user FK
    
    Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
    """
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    access_token_hash = models.CharField(max_length=256)
    refresh_token_hash = models.CharField(max_length=256)
    is_valid = models.BooleanField(default=True)
    expires_in = models.IntegerField(default=3600, help_text="Session expiration time in seconds")
    created_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=256, blank=True)
    remember_me = models.BooleanField(default=False)
    session_data = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return f"Session {self.session_id} for user {self.user_id}"
    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'

# --- SECURITY POLICY ---
class SecurityPolicy(models.Model):
    """
    MANDATORY DOCSTRING - SecurityPolicy model for storing security policies and configuration.
    
    Source Information (REQUIRED):
    - Database Table: security_policy
    - Database Design: DD/database_v0.1.md - Section: security_policy
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-03_v0.1.md
    - Business Module: authentication
    
    Business Rules (REQUIRED):
        - Store security policy name, config, status, audit
        - Track creation and update times
    
    Relationships (REQUIRED):
        - Can be referenced by LoginAttempt for policy enforcement
    
    Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
    """
    policy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy_name = models.CharField(max_length=100, unique=True)
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.policy_name
    class Meta:
        db_table = 'security_policy'
        verbose_name = 'Security Policy'
        verbose_name_plural = 'Security Policies'

class LoginAttempt(models.Model):
    """
    MANDATORY DOCSTRING - LoginAttempt model for tracking login attempts and enforcement.
    
    Source Information (REQUIRED):
    - Database Table: login_attempts
    - Database Design: DD/database_v0.1.md - Section: login_attempts
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-03_v0.1.md
    - Business Module: authentication
    
    Business Rules (REQUIRED):
        - Track user, IP, user agent, status, failed attempts, lockout
        - Link to security policy for enforcement
    
    Relationships (REQUIRED):
        - Related to User via FK
        - Related to SecurityPolicy via FK
    
    Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
    """
    attempt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts')
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=256, blank=True)
    status = models.CharField(max_length=20, default='pending')
    failed_attempts = models.IntegerField(default=0)
    lockout_expiry = models.DateTimeField(null=True, blank=True)
    policy = models.ForeignKey(SecurityPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"LoginAttempt {self.attempt_id} for user {self.user_id}"
    class Meta:
        db_table = 'login_attempts'
        verbose_name = 'Login Attempt'
        verbose_name_plural = 'Login Attempts'

class PasswordResetToken(models.Model):
    """
    MANDATORY DOCSTRING - PasswordResetToken model for managing password reset tokens.
    
    Source Information (REQUIRED):
    - Database Table: password_reset_tokens
    - Database Design: DD/database_v0.1.md - Section: password_reset_tokens
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-03_v0.1.md
    - Business Module: authentication
    
    Business Rules (REQUIRED):
        - Track user, token, expiration, usage status
    
    Relationships (REQUIRED):
        - Related to User via FK
    
    Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
    """
    token_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=128, unique=True)
    expires_in = models.IntegerField(default=3600)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"PasswordResetToken {self.token_id} for user {self.user_id}"
    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
