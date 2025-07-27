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
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

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
    department_name = models.CharField(max_length=100, unique=True)
    parent_department = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_departments')
    manager = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_departments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.department_name
    
    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Employee(models.Model):
    """
    MANDATORY DOCSTRING - Employee model for employee information and management.
    
    Source Information (REQUIRED):
    - Database Table: employees
    - Database Design: DD/database_v0.1.md - Section: employees
    - DAO Specification: DD/MDE-01/04-dao/DAO-MDE-01-01_v0.1.md
    - Business Module: authentication
    
    Business Rules (REQUIRED):
        - Employee number must be unique for identification
        - Link to department for organizational structure
        - Track hire date, position, and employment status
        - Support for contact information (email, phone)
        - Audit trail for employee record changes
    
    Relationships (REQUIRED):
        - Related to Department via department FK
        - Related to User via one-to-one (for system access)
        - Related to IdleResource via employee FK
    
    Verification Source: This information can be verified by checking
        the referenced database design and DAO specification documents.
    """
    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for employee")
    employee_number = models.CharField(max_length=20, unique=True, help_text="Unique employee number for identification")
    first_name = models.CharField(max_length=50, help_text="Employee's first name")
    last_name = models.CharField(max_length=50, help_text="Employee's last name")
    email = models.EmailField(max_length=100, unique=True, help_text="Employee's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Employee's phone number")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', help_text="Employee's assigned department")
    position = models.CharField(max_length=100, help_text="Employee's job position/title")
    hire_date = models.DateField(help_text="Date when employee was hired")
    termination_date = models.DateField(null=True, blank=True, help_text="Date when employee was terminated")
    is_active = models.BooleanField(default=True, help_text="Whether employee is currently active")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when record was last updated")
    created_by = models.CharField(max_length=36, help_text="ID of user who created this record")
    updated_by = models.CharField(max_length=36, null=True, blank=True, help_text="ID of user who last updated this record")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_number})"
    
    @property
    def full_name(self):
        """Return full name of employee."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_terminated(self):
        """Check if employee is terminated."""
        return self.termination_date is not None
    
    def clean(self):
        """Validate business rules."""
        super().clean()
        
        if self.termination_date and self.hire_date:
            if self.termination_date <= self.hire_date:
                raise ValidationError("Termination date must be after hire date")
        
        if self.termination_date and self.is_active:
            raise ValidationError("Terminated employee cannot be active")
    
    class Meta:
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['employee_number']),
            models.Index(fields=['email']),
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['hire_date']),
        ]

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
    
    @classmethod
    def authenticate_user(cls, username, password):
        """
        Authenticate user credentials and return user with profile information.
        
        Source: DAO-MDE-01-01_v0.1.md - Step 1: Get User Credentials Operation
        
        Arguments:
        - username (str): Username or email for lookup
        - password (str): Raw password for validation
        
        Returns:
        - User instance if authentication successful, None otherwise
        
        Business Rules:
        - Support both username and email for login
        - Check account is active and not deleted
        - Validate password hash
        - Return user with profile information
        """
        try:
            # Support login by username or email
            user = cls.objects.select_related('profile', 'department').get(
                models.Q(username=username) | models.Q(email=username),
                is_active=True,
                is_deleted=False
            )
            
            if user.check_password(password):
                return user
            return None
            
        except cls.DoesNotExist:
            return None
    
    def get_user_with_roles(self):
        """
        Retrieve user with assigned roles and permissions.
        
        Source: DAO-MDE-01-01_v0.1.md - Step 2: Get User Roles Operation
        
        Returns:
        - Dictionary with user info, roles, and permissions
        """
        user_roles = self.userrole_set.filter(
            is_active=True,
            role__is_active=True
        ).select_related('role')
        
        roles_data = []
        all_permissions = set()
        
        for user_role in user_roles:
            role = user_role.role
            # Get permissions through RolePermission junction
            role_permissions = role.role_permissions.filter(
                role__is_active=True
            ).select_related('permission')
            
            permissions = [rp.permission.permission_name for rp in role_permissions]
            
            roles_data.append({
                'role_id': str(role.role_id),
                'role_name': role.role_name,
                'role_description': role.role_description,
                'assigned_date': user_role.assigned_date,
                'permissions': permissions
            })
            
            all_permissions.update(permissions)
        
        return {
            'user': self,
            'roles': roles_data,
            'all_permissions': list(all_permissions)
        }
    
    def set_password(self, raw_password):
        """
        Set password with proper hashing and update timestamp.
        
        Arguments:
        - raw_password (str): Plain text password
        """
        self.password_hash = make_password(raw_password)
        self.password_updated_time = timezone.now()
    
    def check_password(self, raw_password):
        """
        Check password against stored hash.
        
        Arguments:
        - raw_password (str): Plain text password to verify
        
        Returns:
        - bool: True if password matches, False otherwise
        """
        return check_password(raw_password, self.password_hash)
    
    def has_permission(self, permission_name):
        """
        Check if user has a specific permission.
        
        Arguments:
        - permission_name (str): Name of permission to check
        
        Returns:
        - bool: True if user has permission, False otherwise
        """
        user_data = self.get_user_with_roles()
        return permission_name in user_data['all_permissions']
    
    def get_departments_managed(self):
        """
        Get list of departments this user manages.
        
        Returns:
        - QuerySet: Departments managed by this user
        """
        return self.managed_departments.filter(is_active=True)

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

class RolePermission(models.Model):
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
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    
    class Meta:
        db_table = 'role_permissions'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
        unique_together = ('role', 'permission')

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
    
    Custom Methods (from DAO specifications):
        - create_session(): Generate JWT tokens and session
        - validate_session(): Check session validity
        - refresh_session(): Refresh tokens
        - revoke_session(): Invalidate session
        - cleanup_expired_sessions(): Remove expired sessions
        - get_active_sessions(): List user sessions
        - update_session_activity(): Update last activity
    
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
        indexes = [
            models.Index(fields=['user', 'is_valid']),
            models.Index(fields=['access_token_hash']),
            models.Index(fields=['created_time']),
        ]
    
    @property
    def is_expired(self):
        """Check if session is expired."""
        if not self.is_valid:
            return True
        
        expiry_time = self.created_time + timezone.timedelta(seconds=self.expires_in)
        return timezone.now() > expiry_time
    
    @property
    def expires_at(self):
        """Get session expiration timestamp."""
        return self.created_time + timezone.timedelta(seconds=self.expires_in)
    
    def clean(self):
        """Validate business rules."""
        super().clean()
        
        if self.expires_in <= 0:
            raise ValidationError("Expiration time must be positive")
    
    # DAO Methods Implementation
    @classmethod
    def create_session(cls, user, session_data=None, remember_me=False, ip_address=None, user_agent=None):
        """
        Generate JWT tokens and create new session.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-01: Create Session
        
        Arguments:
        - user (User): User instance
        - session_data (dict): Additional session data
        - remember_me (bool): Extended session duration
        - ip_address (str): Client IP address
        - user_agent (str): Client user agent
        
        Returns:
        - Dictionary with session info and tokens
        
        Business Rules:
        - Generate secure access and refresh tokens
        - Set appropriate expiration based on remember_me
        - Store hashed tokens for security
        - Track session metadata
        """
        import hashlib
        import secrets
        
        # Generate secure tokens
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        # Hash tokens for storage
        access_token_hash = hashlib.sha256(access_token.encode()).hexdigest()
        refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        
        # Set expiration based on remember_me
        expires_in = 7 * 24 * 3600 if remember_me else 3600  # 7 days vs 1 hour
        
        # Create session
        session = cls.objects.create(
            user=user,
            access_token_hash=access_token_hash,
            refresh_token_hash=refresh_token_hash,
            expires_in=expires_in,
            remember_me=remember_me,
            ip_address=ip_address or '',
            user_agent=user_agent or '',
            session_data=session_data or {},
            last_activity=timezone.now()
        )
        
        return {
            'session_id': str(session.session_id),
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'expires_at': session.expires_at.isoformat(),
            'user_id': str(user.user_id),
            'remember_me': remember_me
        }
    
    @classmethod
    def validate_session(cls, access_token):
        """
        Check session validity and return session info.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-02: Validate Session
        
        Arguments:
        - access_token (str): Access token to validate
        
        Returns:
        - Dictionary with session info if valid, None otherwise
        
        Business Rules:
        - Verify token hash matches stored value
        - Check session is not expired
        - Check session is still valid
        - Update last activity
        """
        import hashlib
        
        if not access_token:
            return None
        
        try:
            # Hash the token for comparison
            token_hash = hashlib.sha256(access_token.encode()).hexdigest()
            
            # Find session by token hash
            session = cls.objects.select_related('user').get(
                access_token_hash=token_hash,
                is_valid=True
            )
            
            # Check if expired
            if session.is_expired:
                session.is_valid = False
                session.save(update_fields=['is_valid'])
                return None
            
            # Update last activity
            session.last_activity = timezone.now()
            session.save(update_fields=['last_activity'])
            
            return {
                'session_id': str(session.session_id),
                'user': session.user,
                'user_id': str(session.user.user_id),
                'expires_at': session.expires_at.isoformat(),
                'last_activity': session.last_activity.isoformat(),
                'session_data': session.session_data
            }
            
        except cls.DoesNotExist:
            return None
    
    def refresh_session(self, refresh_token):
        """
        Refresh access token using refresh token.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-03: Refresh Session
        
        Arguments:
        - refresh_token (str): Refresh token
        
        Returns:
        - Dictionary with new tokens if successful, None otherwise
        
        Business Rules:
        - Verify refresh token is valid
        - Generate new access token
        - Optionally rotate refresh token
        - Update session expiration
        """
        import hashlib
        import secrets
        
        if not refresh_token or not self.is_valid or self.is_expired:
            return None
        
        # Verify refresh token
        refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        if refresh_token_hash != self.refresh_token_hash:
            return None
        
        # Generate new access token
        new_access_token = secrets.token_urlsafe(32)
        new_access_token_hash = hashlib.sha256(new_access_token.encode()).hexdigest()
        
        # Update session
        self.access_token_hash = new_access_token_hash
        self.last_activity = timezone.now()
        
        # Extend expiration for remember_me sessions
        if self.remember_me:
            self.created_time = timezone.now()  # Reset creation time
        
        self.save(update_fields=['access_token_hash', 'last_activity', 'created_time'])
        
        return {
            'session_id': str(self.session_id),
            'access_token': new_access_token,
            'refresh_token': refresh_token,  # Keep same refresh token
            'expires_in': self.expires_in,
            'expires_at': self.expires_at.isoformat()
        }
    
    def revoke_session(self):
        """
        Invalidate current session.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-04: Revoke Session
        
        Business Rules:
        - Mark session as invalid
        - Clear sensitive data
        - Keep for audit trail
        """
        self.is_valid = False
        self.access_token_hash = ''
        self.refresh_token_hash = ''
        self.save(update_fields=['is_valid', 'access_token_hash', 'refresh_token_hash'])
    
    @classmethod
    def cleanup_expired_sessions(cls, days_old=30):
        """
        Remove old expired sessions.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-05: Cleanup Expired Sessions
        
        Arguments:
        - days_old (int): Remove sessions older than this many days
        
        Returns:
        - Dictionary with cleanup statistics
        
        Business Rules:
        - Remove expired sessions older than specified days
        - Keep recent sessions for audit purposes
        - Return cleanup statistics
        """
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        
        # Find expired sessions to delete
        expired_sessions = cls.objects.filter(
            models.Q(is_valid=False) | models.Q(created_time__lt=cutoff_date - timezone.timedelta(seconds=models.F('expires_in'))),
            created_time__lt=cutoff_date
        )
        
        count = expired_sessions.count()
        expired_sessions.delete()
        
        # Also mark invalid sessions that are expired
        newly_expired = cls.objects.filter(
            is_valid=True,
            created_time__lt=timezone.now() - timezone.timedelta(seconds=models.F('expires_in'))
        )
        newly_expired_count = newly_expired.update(is_valid=False)
        
        return {
            'deleted_sessions': count,
            'newly_expired_sessions': newly_expired_count,
            'cleanup_date': timezone.now().isoformat()
        }
    
    @classmethod
    def get_active_sessions(cls, user):
        """
        List active sessions for a user.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-06: Get Active Sessions
        
        Arguments:
        - user (User): User instance
        
        Returns:
        - List of active session dictionaries
        
        Business Rules:
        - Return only valid, non-expired sessions
        - Include session metadata
        - Order by last activity
        """
        sessions = cls.objects.filter(
            user=user,
            is_valid=True
        ).order_by('-last_activity')
        
        active_sessions = []
        for session in sessions:
            if not session.is_expired:
                active_sessions.append({
                    'session_id': str(session.session_id),
                    'created_time': session.created_time.isoformat(),
                    'last_activity': session.last_activity.isoformat() if session.last_activity else None,
                    'expires_at': session.expires_at.isoformat(),
                    'ip_address': session.ip_address,
                    'user_agent': session.user_agent,
                    'remember_me': session.remember_me,
                    'is_current': False  # Can be set by caller
                })
            else:
                # Mark as invalid if expired
                session.is_valid = False
                session.save(update_fields=['is_valid'])
        
        return active_sessions
    
    def update_session_activity(self, activity_data=None):
        """
        Update session activity and metadata.
        
        Source: DAO-MDE-01-02_v0.1.md - DAO-MDE-01-02-07: Update Session Activity
        
        Arguments:
        - activity_data (dict): Activity data to store
        
        Business Rules:
        - Update last activity timestamp
        - Store additional activity metadata
        - Extend session if needed
        """
        self.last_activity = timezone.now()
        
        if activity_data:
            # Merge activity data with existing session data
            if not self.session_data:
                self.session_data = {}
            
            self.session_data.update({
                'last_activity_data': activity_data,
                'activity_count': self.session_data.get('activity_count', 0) + 1
            })
        
        self.save(update_fields=['last_activity', 'session_data'])

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
        - Support password complexity requirements
        - Configure login attempt limits and lockout policies
    
    Relationships (REQUIRED):
        - Can be referenced by LoginAttempt for policy enforcement
    
    Custom Methods (from DAO specifications):
        - validate_password_strength(): Check password complexity
        - get_lockout_policy(): Get account lockout configuration
        - check_password_expiry(): Password aging policy
        - apply_security_policy(): General policy enforcement
    
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
    
    @classmethod
    def get_default_policy(cls):
        """Get the default security policy."""
        policy, created = cls.objects.get_or_create(
            policy_name='default',
            defaults={
                'config': {
                    'password_min_length': 8,
                    'password_require_uppercase': True,
                    'password_require_lowercase': True,
                    'password_require_numbers': True,
                    'password_require_special': True,
                    'password_expiry_days': 90,
                    'max_failed_attempts': 5,
                    'lockout_duration_minutes': 30,
                    'require_password_change_on_first_login': True
                },
                'is_active': True
            }
        )
        return policy
    
    def validate_password_strength(self, password):
        """
        Validate password against security policy requirements.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-01: Validate Password Strength
        
        Arguments:
        - password (str): Plain text password to validate
        
        Returns:
        - Dictionary with validation result and details
        
        Business Rules:
        - Check minimum length
        - Verify character complexity requirements
        - Check against common passwords
        - Return detailed feedback
        """
        import re
        
        config = self.config
        errors = []
        warnings = []
        
        # Check minimum length
        min_length = config.get('password_min_length', 8)
        if len(password) < min_length:
            errors.append(f"Password must be at least {min_length} characters long")
        
        # Check uppercase requirement
        if config.get('password_require_uppercase', True):
            if not re.search(r'[A-Z]', password):
                errors.append("Password must contain at least one uppercase letter")
        
        # Check lowercase requirement
        if config.get('password_require_lowercase', True):
            if not re.search(r'[a-z]', password):
                errors.append("Password must contain at least one lowercase letter")
        
        # Check numbers requirement
        if config.get('password_require_numbers', True):
            if not re.search(r'\d', password):
                errors.append("Password must contain at least one number")
        
        # Check special characters requirement
        if config.get('password_require_special', True):
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errors.append("Password must contain at least one special character")
        
        # Check for common patterns
        common_patterns = ['123456', 'password', 'qwerty', 'admin']
        if any(pattern in password.lower() for pattern in common_patterns):
            warnings.append("Password contains common patterns")
        
        # Check for sequential characters
        if len(password) >= 3:
            for i in range(len(password) - 2):
                if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i]) + 2:
                    warnings.append("Password contains sequential characters")
                    break
        
        is_valid = len(errors) == 0
        strength_score = self._calculate_password_strength(password)
        
        return {
            'is_valid': is_valid,
            'strength_score': strength_score,
            'errors': errors,
            'warnings': warnings,
            'policy_name': self.policy_name
        }
    
    def _calculate_password_strength(self, password):
        """Calculate password strength score (0-100)."""
        score = 0
        
        # Length bonus
        score += min(len(password) * 4, 25)
        
        # Character diversity bonus
        if any(c.isupper() for c in password):
            score += 10
        if any(c.islower() for c in password):
            score += 10
        if any(c.isdigit() for c in password):
            score += 10
        if any(not c.isalnum() for c in password):
            score += 15
        
        # Length bonus for very long passwords
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Uniqueness bonus
        unique_chars = len(set(password))
        score += min(unique_chars * 2, 20)
        
        return min(score, 100)
    
    def get_lockout_policy(self):
        """
        Get account lockout policy configuration.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-03: Apply Account Lockout
        
        Returns:
        - Dictionary with lockout policy details
        """
        return {
            'max_failed_attempts': self.config.get('max_failed_attempts', 5),
            'lockout_duration_minutes': self.config.get('lockout_duration_minutes', 30),
            'progressive_lockout': self.config.get('progressive_lockout', False),
            'lockout_thresholds': self.config.get('lockout_thresholds', [5, 10, 20]),
            'lockout_durations': self.config.get('lockout_durations', [30, 60, 120])
        }
    
    def check_password_expiry(self, user):
        """
        Check if user's password has expired.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-06: Check Password Expiry
        
        Arguments:
        - user (User): User instance to check
        
        Returns:
        - Dictionary with expiry status and details
        """
        expiry_days = self.config.get('password_expiry_days', 90)
        
        if not user.password_updated_time:
            return {
                'is_expired': True,
                'days_until_expiry': 0,
                'requires_change': True,
                'reason': 'Password never set'
            }
        
        days_since_update = (timezone.now() - user.password_updated_time).days
        days_until_expiry = expiry_days - days_since_update
        
        return {
            'is_expired': days_until_expiry <= 0,
            'days_until_expiry': days_until_expiry,
            'requires_change': days_until_expiry <= 7,  # Warning 7 days before
            'reason': 'Password age policy' if days_until_expiry <= 0 else None
        }
    
    def apply_security_policy(self, user, action='login'):
        """
        Apply general security policy enforcement.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-09: Apply Security Policy
        
        Arguments:
        - user (User): User instance
        - action (str): Action being performed
        
        Returns:
        - Dictionary with policy enforcement result
        """
        policy_checks = {
            'password_expiry': self.check_password_expiry(user),
            'account_status': {
                'is_active': user.is_active,
                'is_deleted': user.is_deleted
            },
            'first_login_check': {
                'is_first_login': user.login_count == 0,
                'requires_password_change': self.config.get('require_password_change_on_first_login', True)
            }
        }
        
        # Determine if access should be allowed
        allow_access = True
        required_actions = []
        
        if not user.is_active or user.is_deleted:
            allow_access = False
            required_actions.append('account_reactivation')
        
        if policy_checks['password_expiry']['is_expired']:
            allow_access = False
            required_actions.append('password_change')
        
        if (policy_checks['first_login_check']['is_first_login'] and 
            policy_checks['first_login_check']['requires_password_change']):
            required_actions.append('initial_password_change')
        
        return {
            'allow_access': allow_access,
            'required_actions': required_actions,
            'policy_checks': policy_checks,
            'policy_name': self.policy_name
        }

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
        - Progressive lockout based on failed attempts
        - IP-based tracking for additional security
    
    Relationships (REQUIRED):
        - Related to User via FK
        - Related to SecurityPolicy via FK
    
    Custom Methods (from DAO specifications):
        - check_login_attempts(): Failed login tracking
        - apply_account_lockout(): Lockout logic implementation
        - reset_failed_attempts(): Clear failed attempts
        - log_security_event(): Security audit logging
    
    Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
    """
    attempt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts')
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=256, blank=True)
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('locked', 'Account Locked'),
            ('blocked', 'IP Blocked'),
            ('pending', 'Pending')
        ]
    )
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
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['lockout_expiry']),
        ]
    
    @property
    def is_locked_out(self):
        """Check if account is currently locked out."""
        if not self.lockout_expiry:
            return False
        return timezone.now() < self.lockout_expiry
    
    @classmethod
    def check_login_attempts(cls, user, ip_address=None):
        """
        Check failed login attempts and determine if account should be locked.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-02: Check Login Attempts
        
        Arguments:
        - user (User): User instance
        - ip_address (str): Client IP address
        
        Returns:
        - Dictionary with attempt status and lockout info
        
        Business Rules:
        - Count failed attempts in recent time window
        - Check for existing lockout
        - Determine if new lockout should be applied
        - Consider IP-based attempts
        """
        policy = SecurityPolicy.get_default_policy()
        lockout_config = policy.get_lockout_policy()
        
        # Get recent attempts (last 24 hours)
        recent_window = timezone.now() - timezone.timedelta(hours=24)
        recent_attempts = cls.objects.filter(
            user=user,
            created_at__gte=recent_window
        ).order_by('-created_at')
        
        # Count failed attempts
        failed_count = recent_attempts.filter(status='failed').count()
        
        # Check for existing lockout
        latest_attempt = recent_attempts.first()
        is_currently_locked = latest_attempt and latest_attempt.is_locked_out if latest_attempt else False
        
        # Check IP-based attempts if provided
        ip_failed_count = 0
        if ip_address:
            ip_failed_count = cls.objects.filter(
                ip_address=ip_address,
                status='failed',
                created_at__gte=recent_window
            ).count()
        
        return {
            'failed_attempts': failed_count,
            'ip_failed_attempts': ip_failed_count,
            'is_locked_out': is_currently_locked,
            'lockout_expiry': latest_attempt.lockout_expiry if latest_attempt else None,
            'max_attempts': lockout_config['max_failed_attempts'],
            'should_lockout': failed_count >= lockout_config['max_failed_attempts'],
            'policy_name': policy.policy_name
        }
    
    def apply_account_lockout(self, policy=None):
        """
        Apply account lockout based on failed attempts.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-03: Apply Account Lockout
        
        Arguments:
        - policy (SecurityPolicy): Security policy to use
        
        Returns:
        - Dictionary with lockout details
        
        Business Rules:
        - Calculate lockout duration based on attempt count
        - Support progressive lockout (increasing duration)
        - Update attempt status and expiry
        """
        if not policy:
            policy = SecurityPolicy.get_default_policy()
        
        lockout_config = policy.get_lockout_policy()
        
        # Calculate lockout duration
        if lockout_config.get('progressive_lockout', False):
            # Progressive lockout - longer duration for repeated violations
            thresholds = lockout_config.get('lockout_thresholds', [5, 10, 20])
            durations = lockout_config.get('lockout_durations', [30, 60, 120])
            
            duration_minutes = lockout_config['lockout_duration_minutes']
            for i, threshold in enumerate(thresholds):
                if self.failed_attempts >= threshold:
                    duration_minutes = durations[i]
        else:
            duration_minutes = lockout_config['lockout_duration_minutes']
        
        # Set lockout expiry
        self.lockout_expiry = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.status = 'locked'
        self.policy = policy
        self.save(update_fields=['lockout_expiry', 'status', 'policy', 'updated_at'])
        
        return {
            'lockout_applied': True,
            'lockout_expiry': self.lockout_expiry.isoformat(),
            'duration_minutes': duration_minutes,
            'failed_attempts': self.failed_attempts,
            'policy_name': policy.policy_name
        }
    
    @classmethod
    def reset_failed_attempts(cls, user):
        """
        Clear failed login attempts for a user.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-05: Reset Failed Attempts
        
        Arguments:
        - user (User): User instance
        
        Returns:
        - Dictionary with reset statistics
        
        Business Rules:
        - Mark all failed attempts as cleared
        - Remove active lockouts
        - Log security event
        """
        # Reset lockouts and failed attempts
        active_attempts = cls.objects.filter(
            user=user,
            status__in=['failed', 'locked']
        )
        
        count = active_attempts.count()
        active_attempts.update(
            status='success',
            lockout_expiry=None,
            updated_at=timezone.now()
        )
        
        # Log security event
        cls.log_security_event(
            user=user,
            event_type='failed_attempts_reset',
            details={'reset_count': count}
        )
        
        return {
            'reset_count': count,
            'user_id': str(user.user_id),
            'reset_time': timezone.now().isoformat()
        }
    
    @classmethod
    def log_security_event(cls, user, event_type, ip_address=None, user_agent=None, details=None):
        """
        Log security-related events for audit trail.
        
        Source: DAO-MDE-01-03_v0.1.md - DAO-MDE-01-03-04: Log Security Event
        
        Arguments:
        - user (User): User instance
        - event_type (str): Type of security event
        - ip_address (str): Client IP address
        - user_agent (str): Client user agent
        - details (dict): Additional event details
        
        Returns:
        - LoginAttempt instance for the logged event
        
        Business Rules:
        - Create audit record for security events
        - Store relevant metadata
        - Support various event types
        """
        # Determine status based on event type
        status_mapping = {
            'login_success': 'success',
            'login_failed': 'failed',
            'account_locked': 'locked',
            'failed_attempts_reset': 'success',
            'password_changed': 'success',
            'suspicious_activity': 'blocked'
        }
        
        status = status_mapping.get(event_type, 'pending')
        
        # Create attempt record
        attempt = cls.objects.create(
            user=user,
            ip_address=ip_address or '',
            user_agent=user_agent or '',
            status=status,
            failed_attempts=user.login_attempts.filter(status='failed').count(),
            policy=SecurityPolicy.get_default_policy()
        )
        
        # Store additional details in session-like tracking
        if details:
            # You could extend this to store in a separate SecurityEvent model
            pass
        
        return attempt
    
    @classmethod
    def record_login_attempt(cls, user, success, ip_address=None, user_agent=None):
        """
        Record a login attempt and handle lockout logic.
        
        Arguments:
        - user (User): User instance
        - success (bool): Whether login was successful
        - ip_address (str): Client IP address
        - user_agent (str): Client user agent
        
        Returns:
        - Dictionary with attempt result and any lockout info
        """
        if success:
            # Reset failed attempts on successful login
            cls.reset_failed_attempts(user)
            
            # Log successful login
            attempt = cls.log_security_event(
                user=user,
                event_type='login_success',
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            return {
                'success': True,
                'lockout_info': None,
                'attempt_id': str(attempt.attempt_id)
            }
        else:
            # Check current attempt status
            attempt_status = cls.check_login_attempts(user, ip_address)
            
            # Create failed attempt record
            failed_attempt = cls.objects.create(
                user=user,
                ip_address=ip_address or '',
                user_agent=user_agent or '',
                status='failed',
                failed_attempts=attempt_status['failed_attempts'] + 1,
                policy=SecurityPolicy.get_default_policy()
            )
            
            # Apply lockout if threshold reached
            lockout_info = None
            if attempt_status['should_lockout']:
                lockout_info = failed_attempt.apply_account_lockout()
                
                # Log lockout event
                cls.log_security_event(
                    user=user,
                    event_type='account_locked',
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details=lockout_info
                )
            
            return {
                'success': False,
                'failed_attempts': failed_attempt.failed_attempts,
                'lockout_info': lockout_info,
                'attempt_id': str(failed_attempt.attempt_id)
            }

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
