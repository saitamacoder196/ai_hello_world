"""
Resource Management Models

Fixed version without duplicate primary keys.
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from common.models import BaseModel, TimestampedModel


class IdleResource(BaseModel):
    """
    MANDATORY DOCSTRING - IdleResource model for managing idle personnel information and availability.
    
    Source Information (REQUIRED):
    - Database Table: idle_resources
    - Database Design: DD/database_v0.1.md - Section: idle_resources
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track resource type, status, skills, experience, availability, and audit info
        - Link to employee and department via proper foreign keys
        - Support for optimistic locking (version) from BaseModel
        - Skills stored as JSON array for flexibility
        - Availability date range validation
        - Status choices for better data integrity
    
    Relationships (REQUIRED):
        - Related to Employee via employee FK
        - Related to Department via department FK (through Employee)
        - Inherits audit trails from BaseModel
    
    Custom Methods (from DAO specifications):
        - create_with_validation(): Create resource with business rule validation
        - update_with_version_check(): Update with optimistic locking
        - list_with_filters(): Dynamic filtering with pagination
        - check_availability(): Check resource availability for date range
    
    Verification Source: This information can be verified by checking
        the referenced DAO specification and database design documents.
    """
    # Note: Using inherited 'id' field from BaseModel as primary key
    
    employee = models.ForeignKey(
        'authentication.Employee',
        on_delete=models.CASCADE,
        related_name='idle_resources',
        help_text="Employee associated with this resource"
    )
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('developer', 'Software Developer'),
            ('tester', 'QA Tester'),
            ('analyst', 'Business Analyst'),
            ('designer', 'UI/UX Designer'),
            ('manager', 'Project Manager'),
            ('devops', 'DevOps Engineer'),
            ('architect', 'Solution Architect'),
            ('consultant', 'Technical Consultant'),
        ],
        help_text="Type of resource (developer, tester, analyst, etc.)"
    )
    status = models.CharField(
        max_length=20,
        default='available',
        choices=[
            ('available', 'Available'),
            ('allocated', 'Allocated'),
            ('unavailable', 'Unavailable'),
            ('deleted', 'Deleted')
        ],
        help_text="Current availability status"
    )
    availability_start = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Start date of availability period"
    )
    availability_end = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="End date of availability period"
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of skills and competencies"
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Years of relevant experience"
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Hourly rate for cost calculations"
    )
    
    def __str__(self):
        return f"IdleResource {self.id} - {self.employee.first_name} {self.employee.last_name} ({self.resource_type})"
    
    @property
    def department(self):
        """Get department through employee relationship."""
        return self.employee.department if self.employee else None
    
    @property
    def is_available_now(self):
        """Check if resource is currently available."""
        now = timezone.now()
        if self.status != 'available':
            return False
        
        if self.availability_start and now < self.availability_start:
            return False
        
        if self.availability_end and now > self.availability_end:
            return False
        
        return True
    
    def clean(self):
        """Validate business rules."""
        super().clean()
        
        if self.availability_start and self.availability_end:
            if self.availability_start >= self.availability_end:
                raise ValidationError("Availability start must be before end date")
        
        if self.hourly_rate is not None and self.hourly_rate < 0:
            raise ValidationError("Hourly rate cannot be negative")
        
        if self.experience_years is not None and self.experience_years < 0:
            raise ValidationError("Experience years cannot be negative")
    
    def to_dict(self):
        """Convert model instance to dictionary for API responses."""
        return {
            'id': str(self.id),
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_id': str(self.employee.employee_id) if self.employee else None,
            'department_id': str(self.employee.department.department_id) if self.employee and self.employee.department else None,
            'resource_type': self.resource_type,
            'status': self.status,
            'availability_start': self.availability_start.isoformat() if self.availability_start else None,
            'availability_end': self.availability_end.isoformat() if self.availability_end else None,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'version': self.version
        }
    
    # DAO Methods Implementation
    @classmethod
    def create_with_validation(cls, data, created_by=None):
        """
        Create resource with business rule validation.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-01: Create with Validation
        
        Arguments:
        - data (dict): Resource data
        - created_by (str): User who created the resource
        
        Returns:
        - Dictionary with created resource and validation results
        
        Business Rules:
        - Validate employee exists and is not already allocated
        - Check availability date ranges
        - Validate skills format
        - Set proper audit fields
        """
        from django.core.exceptions import ValidationError
        from authentication.models import Employee
        
        errors = []
        warnings = []
        
        # Validate employee exists
        try:
            employee = Employee.objects.get(employee_id=data.get('employee_id'))
        except Employee.DoesNotExist:
            errors.append(f"Employee {data.get('employee_id')} not found")
            return {'success': False, 'errors': errors}
        
        # Check if employee already has active resource
        existing = cls.objects.filter(
            employee=employee,
            status__in=['available', 'allocated']
        ).exists()
        
        if existing:
            warnings.append(f"Employee {employee.employee_id} already has an active resource record")
        
        # Validate date ranges
        availability_start = data.get('availability_start')
        availability_end = data.get('availability_end')
        
        if availability_start and availability_end:
            if availability_start >= availability_end:
                errors.append("Availability start must be before end date")
        
        # Validate skills format
        skills = data.get('skills', [])
        if skills and not isinstance(skills, list):
            errors.append("Skills must be a list")
        
        if errors:
            return {'success': False, 'errors': errors, 'warnings': warnings}
        
        # Create resource
        resource_data = {
            'employee': employee,
            'resource_type': data.get('resource_type', 'developer'),
            'status': data.get('status', 'available'),
            'availability_start': availability_start,
            'availability_end': availability_end,
            'skills': skills,
            'experience_years': data.get('experience_years', 0),
            'hourly_rate': data.get('hourly_rate'),
            'created_by': created_by or 'system'
        }
        
        resource = cls.objects.create(**resource_data)
        
        return {
            'success': True,
            'resource': resource,
            'resource_id': str(resource.id),
            'warnings': warnings,
            'audit_trail_id': str(resource.id)
        }
    
    def update_with_version_check(self, data, updated_by=None):
        """
        Update resource with optimistic locking.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-02: Update with Version Check
        
        Arguments:
        - data (dict): Update data
        - updated_by (str): User who updated the resource
        
        Returns:
        - Dictionary with update results
        
        Business Rules:
        - Check version for optimistic locking
        - Validate update data
        - Update audit fields
        """
        from django.core.exceptions import ValidationError
        
        # Version check for optimistic locking
        current_version = data.get('version')
        if current_version is not None and current_version != self.version:
            return {
                'success': False,
                'error': 'Resource has been modified by another user. Please refresh and try again.',
                'current_version': self.version,
                'provided_version': current_version
            }
        
        # Update fields
        updatable_fields = [
            'resource_type', 'status', 'availability_start', 'availability_end',
            'skills', 'experience_years', 'hourly_rate'
        ]
        
        updated_fields = []
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
                updated_fields.append(field)
        
        # Update audit fields
        if updated_by:
            self.updated_by = updated_by
        
        try:
            self.full_clean()
            self.save(update_fields=updated_fields + ['updated_by', 'updated_at', 'version'])
            
            return {
                'success': True,
                'resource': self,
                'updated_fields': updated_fields,
                'new_version': self.version
            }
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e),
                'validation_errors': e.message_dict if hasattr(e, 'message_dict') else [str(e)]
            }
    
    @classmethod
    def list_with_filters(cls, filters=None, page=1, page_size=25, sort_by='created_at', sort_order='desc'):
        """
        Dynamic filtering with pagination.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-03: List with Filters
        
        Arguments:
        - filters (dict): Filter criteria
        - page (int): Page number
        - page_size (int): Items per page
        - sort_by (str): Sort field
        - sort_order (str): Sort direction
        
        Returns:
        - Dictionary with filtered results and pagination info
        """
        from django.core.paginator import Paginator
        from django.db.models import Q
        
        queryset = cls.objects.select_related('employee', 'employee__department').all()
        
        # Apply filters
        if filters:
            # Status filter
            if 'status' in filters:
                queryset = queryset.filter(status=filters['status'])
            
            # Resource type filter
            if 'resource_type' in filters:
                queryset = queryset.filter(resource_type=filters['resource_type'])
            
            # Department filter
            if 'department_id' in filters:
                queryset = queryset.filter(employee__department__department_id=filters['department_id'])
            
            # Skills filter
            if 'skills' in filters:
                skills = filters['skills'] if isinstance(filters['skills'], list) else [filters['skills']]
                for skill in skills:
                    queryset = queryset.filter(skills__icontains=skill)
            
            # Experience filter
            if 'min_experience' in filters:
                queryset = queryset.filter(experience_years__gte=filters['min_experience'])
            
            # Availability filter
            if 'available_from' in filters:
                queryset = queryset.filter(
                    Q(availability_start__lte=filters['available_from']) |
                    Q(availability_start__isnull=True)
                )
            
            if 'available_until' in filters:
                queryset = queryset.filter(
                    Q(availability_end__gte=filters['available_until']) |
                    Q(availability_end__isnull=True)
                )
        
        # Apply sorting
        sort_field = sort_by
        if sort_order.lower() == 'desc':
            sort_field = f'-{sort_field}'
        
        queryset = queryset.order_by(sort_field)
        
        # Pagination
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        return {
            'records': [resource.to_dict() for resource in page_obj],
            'total_count': paginator.count,
            'page_info': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'page_size': page_size,
                'has_next_page': page_obj.has_next(),
                'has_previous_page': page_obj.has_previous()
            },
            'filters_applied': filters or {},
            'sort_info': {
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }
    
    def check_availability(self, start_date, end_date):
        """
        Check resource availability for date range.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-04: Check Availability
        
        Arguments:
        - start_date (datetime): Availability start
        - end_date (datetime): Availability end
        
        Returns:
        - Dictionary with availability status
        """
        if self.status != 'available':
            return {
                'is_available': False,
                'reason': f'Resource status is {self.status}',
                'conflicts': []
            }
        
        conflicts = []
        
        # Check base availability window
        if self.availability_start and start_date < self.availability_start:
            conflicts.append({
                'type': 'availability_window',
                'message': f'Resource not available before {self.availability_start.date()}'
            })
        
        if self.availability_end and end_date > self.availability_end:
            conflicts.append({
                'type': 'availability_window', 
                'message': f'Resource not available after {self.availability_end.date()}'
            })
        
        # Check existing allocations from ResourceAvailability
        allocated_periods = self.availability_periods.filter(
            is_allocated=True,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        
        for period in allocated_periods:
            conflicts.append({
                'type': 'allocation_conflict',
                'message': f'Resource allocated from {period.start_date.date()} to {period.end_date.date()}',
                'allocation_reference': period.allocation_reference
            })
        
        return {
            'is_available': len(conflicts) == 0,
            'conflicts': conflicts,
            'availability_window': {
                'start': self.availability_start.isoformat() if self.availability_start else None,
                'end': self.availability_end.isoformat() if self.availability_end else None
            }
        }
    
    class Meta:
        db_table = 'idle_resources'
        verbose_name = 'Idle Resource'
        verbose_name_plural = 'Idle Resources'
        indexes = [
            models.Index(fields=['status', 'resource_type']),
            models.Index(fields=['employee', 'status']),
            models.Index(fields=['availability_start', 'availability_end']),
            models.Index(fields=['resource_type', 'status']),
        ]


class ImportSession(BaseModel):
    """
    MANDATORY DOCSTRING - ImportSession model for tracking data import operations.
    
    Source Information (REQUIRED):
    - Database Table: import_sessions
    - Database Design: DD/database_v0.1.md - Section: import_sessions
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track import operations with status, file info, and results
        - Support for batch processing and error reporting
        - Audit trail through BaseModel inheritance
    
    Relationships (REQUIRED):
        - Can be linked to user who initiated import
        - Related to imported resources through metadata
    
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-01_v0.1.md
    """
    session_name = models.CharField(max_length=200, help_text="Name/description of import session")
    file_name = models.CharField(max_length=255, help_text="Original filename of imported data")
    file_path = models.CharField(max_length=500, blank=True, help_text="Storage path of import file")
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        help_text="Current status of import operation"
    )
    total_records = models.PositiveIntegerField(default=0, help_text="Total records to import")
    processed_records = models.PositiveIntegerField(default=0, help_text="Successfully processed records")
    failed_records = models.PositiveIntegerField(default=0, help_text="Failed record count")
    errors = models.JSONField(default=list, blank=True, help_text="List of import errors")
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional import metadata")
    started_at = models.DateTimeField(null=True, blank=True, help_text="Import start timestamp")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Import completion timestamp")
    
    def __str__(self):
        return f"ImportSession {self.session_name} ({self.status})"
    
    class Meta:
        db_table = 'import_sessions'
        verbose_name = 'Import Session'
        verbose_name_plural = 'Import Sessions'
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['started_at', 'completed_at']),
        ]


class ExportSession(BaseModel):
    """
    MANDATORY DOCSTRING - ExportSession model for tracking data export operations.
    
    Source Information (REQUIRED):
    - Database Table: export_sessions
    - Database Design: DD/database_v0.1.md - Section: export_sessions
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track export operations with filters, format, and results
        - Support for different export formats (CSV, Excel, JSON)
        - Audit trail through BaseModel inheritance
    
    Relationships (REQUIRED):
        - Can be linked to user who initiated export
        - Related to exported data through filters and metadata
    
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-01_v0.1.md
    """
    session_name = models.CharField(max_length=200, help_text="Name/description of export session")
    export_format = models.CharField(
        max_length=20,
        choices=[
            ('csv', 'CSV'),
            ('excel', 'Excel'),
            ('json', 'JSON'),
            ('pdf', 'PDF')
        ],
        help_text="Format of exported data"
    )
    filters = models.JSONField(default=dict, blank=True, help_text="Filters applied during export")
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        help_text="Current status of export operation"
    )
    file_path = models.CharField(max_length=500, blank=True, help_text="Path to generated export file")
    total_records = models.PositiveIntegerField(default=0, help_text="Total records exported")
    file_size = models.PositiveIntegerField(default=0, help_text="Size of generated file in bytes")
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional export metadata")
    started_at = models.DateTimeField(null=True, blank=True, help_text="Export start timestamp")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Export completion timestamp")
    
    def __str__(self):
        return f"ExportSession {self.session_name} ({self.export_format})"
    
    class Meta:
        db_table = 'export_sessions'
        verbose_name = 'Export Session'
        verbose_name_plural = 'Export Sessions'
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['export_format', 'status']),
        ]


class ResourceSkill(BaseModel):
    """
    MANDATORY DOCSTRING - ResourceSkill model for detailed skill management and assessment.
    
    Source Information (REQUIRED):
    - Database Table: resource_skills
    - Database Design: DD/database_v0.1.md - Section: resource_skills
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track individual skills with proficiency levels and certifications
        - Support for skill categories and verification status
        - Link to specific resources for detailed skill tracking
    
    Relationships (REQUIRED):
        - Related to IdleResource via FK
        - Can reference skill categories and certifications
    
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-01_v0.1.md
    """
    resource = models.ForeignKey(
        IdleResource,
        on_delete=models.CASCADE,
        related_name='detailed_skills',
        help_text="Resource this skill belongs to"
    )
    skill_name = models.CharField(max_length=100, help_text="Name of the skill")
    skill_category = models.CharField(
        max_length=50,
        choices=[
            ('technical', 'Technical'),
            ('programming', 'Programming Language'),
            ('framework', 'Framework/Library'),
            ('database', 'Database'),
            ('cloud', 'Cloud Platform'),
            ('soft_skill', 'Soft Skill'),
            ('certification', 'Certification'),
            ('tool', 'Tool/Software')
        ],
        help_text="Category of the skill"
    )
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        help_text="Proficiency level in this skill"
    )
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of experience with this skill")
    certification_name = models.CharField(max_length=200, blank=True, help_text="Related certification if any")
    certification_date = models.DateField(null=True, blank=True, help_text="Date of certification")
    is_verified = models.BooleanField(default=False, help_text="Whether skill has been verified")
    verification_date = models.DateField(null=True, blank=True, help_text="Date of skill verification")
    notes = models.TextField(blank=True, help_text="Additional notes about this skill")
    
    def __str__(self):
        return f"{self.resource} - {self.skill_name} ({self.proficiency_level})"
    
    class Meta:
        db_table = 'resource_skills'
        verbose_name = 'Resource Skill'
        verbose_name_plural = 'Resource Skills'
        unique_together = ['resource', 'skill_name']
        indexes = [
            models.Index(fields=['skill_category', 'proficiency_level']),
            models.Index(fields=['resource', 'skill_category']),
            models.Index(fields=['is_verified', 'certification_date']),
        ]


class ResourceAvailability(BaseModel):
    """
    MANDATORY DOCSTRING - ResourceAvailability model for detailed availability scheduling.
    
    Source Information (REQUIRED):
    - Database Table: resource_availability
    - Database Design: DD/database_v0.1.md - Section: resource_availability
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track detailed availability periods with capacity and constraints
        - Support for recurring availability patterns
        - Conflict detection and capacity management
    
    Relationships (REQUIRED):
        - Related to IdleResource via FK
        - Support for booking and allocation references
    
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-01_v0.1.md
    """
    resource = models.ForeignKey(
        IdleResource,
        on_delete=models.CASCADE,
        related_name='availability_periods',
        help_text="Resource this availability period belongs to"
    )
    start_date = models.DateTimeField(help_text="Start of availability period")
    end_date = models.DateTimeField(help_text="End of availability period")
    availability_type = models.CharField(
        max_length=20,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('on_call', 'On Call'),
            ('consulting', 'Consulting'),
            ('project_based', 'Project Based')
        ],
        help_text="Type of availability"
    )
    capacity_percentage = models.PositiveIntegerField(
        default=100,
        help_text="Percentage of capacity available (0-100)"
    )
    hourly_commitment = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Hours per week committed"
    )
    location_constraints = models.CharField(
        max_length=100,
        blank=True,
        choices=[
            ('remote', 'Remote Only'),
            ('onsite', 'On-site Only'),
            ('hybrid', 'Hybrid'),
            ('flexible', 'Flexible')
        ],
        help_text="Location preferences/constraints"
    )
    is_recurring = models.BooleanField(default=False, help_text="Whether this is a recurring availability")
    recurrence_pattern = models.JSONField(
        default=dict,
        blank=True,
        help_text="Pattern for recurring availability (weekly, monthly, etc.)"
    )
    notes = models.TextField(blank=True, help_text="Additional availability notes")
    is_allocated = models.BooleanField(default=False, help_text="Whether this period is already allocated")
    allocation_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to project/client allocation"
    )
    
    def clean(self):
        """Validate business rules."""
        super().clean()
        
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")
        
        if not (0 <= self.capacity_percentage <= 100):
            raise ValidationError("Capacity percentage must be between 0 and 100")
        
        if self.hourly_commitment and self.hourly_commitment > 168:  # 24*7
            raise ValidationError("Hourly commitment cannot exceed 168 hours per week")
    
    def __str__(self):
        return f"{self.resource} - {self.start_date.date()} to {self.end_date.date()} ({self.capacity_percentage}%)"
    
    class Meta:
        db_table = 'resource_availability'
        verbose_name = 'Resource Availability'
        verbose_name_plural = 'Resource Availability'
        indexes = [
            models.Index(fields=['resource', 'start_date', 'end_date']),
            models.Index(fields=['availability_type', 'is_allocated']),
            models.Index(fields=['start_date', 'end_date']),
        ]