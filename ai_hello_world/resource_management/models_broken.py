# --- IMPORT/EXPORT OPERATIONS ---
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from common.models import BaseModel, TimestampedModel

class ImportSession(models.Model):
    """
    MANDATORY DOCSTRING - ImportSession model for tracking import operations.
    Source Information:
    - Database Table: import_sessions
    - Database Design: DD/database_v0.1.md - Section: import_sessions
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Track import session, user, type, status, record counts, error summary
    Relationships:
        - Can be referenced by ImportStaging
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=36)
    import_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    total_records = models.IntegerField(default=0)
    successful_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)
    error_summary = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"ImportSession {self.session_id}"
    class Meta:
        db_table = 'import_sessions'
        verbose_name = 'Import Session'
        verbose_name_plural = 'Import Sessions'

class ImportStaging(models.Model):
    """
    MANDATORY DOCSTRING - ImportStaging model for temporary storage during import.
    Source Information:
    - Database Table: import_staging
    - Database Design: DD/database_v0.1.md - Section: import_staging
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Store raw and transformed data, validation status/errors
    Relationships:
        - Related to ImportSession via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ImportSession, on_delete=models.CASCADE, related_name='staging_records')
    record_index = models.IntegerField()
    raw_data = models.JSONField(default=dict)
    transformed_data = models.JSONField(default=dict, blank=True)
    validation_status = models.CharField(max_length=20, default='pending')
    validation_errors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'import_staging'
        verbose_name = 'Import Staging'
        verbose_name_plural = 'Import Staging'

class ExportSession(models.Model):
    """
    MANDATORY DOCSTRING - ExportSession model for tracking export operations.
    Source Information:
    - Database Table: export_sessions
    - Database Design: DD/database_v0.1.md - Section: export_sessions
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Track export session, user, type, format, criteria, status, file info
    Relationships:
        - Can be referenced by ExportColumnConfig, ExportTemplate
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=36)
    export_type = models.CharField(max_length=50)
    export_format = models.CharField(max_length=20, default='csv')
    criteria = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default='pending')
    total_records = models.IntegerField(default=0)
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"ExportSession {self.session_id}"
    class Meta:
        db_table = 'export_sessions'
        verbose_name = 'Export Session'
        verbose_name_plural = 'Export Sessions'

class ExportColumnConfig(models.Model):
    """
    MANDATORY DOCSTRING - ExportColumnConfig model for export column mapping.
    Source Information:
    - Database Table: export_column_config
    - Database Design: DD/database_v0.1.md - Section: export_column_config
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Store column mapping, display name, data type, format, order, active status
    Relationships:
        - Can be referenced by ExportSession, ExportTemplate
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=100)
    column_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)
    export_format = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'export_column_config'
        verbose_name = 'Export Column Config'
        verbose_name_plural = 'Export Column Configs'

class ExportTemplate(models.Model):
    """
    MANDATORY DOCSTRING - ExportTemplate model for export template configuration.
    Source Information:
    - Database Table: export_templates
    - Database Design: DD/database_v0.1.md - Section: export_templates
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Store template name, type, column config, format config, filter config, status
    Relationships:
        - Can be referenced by ExportSession
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    template_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50)
    column_config = models.JSONField(default=dict)
    format_config = models.JSONField(default=dict, blank=True)
    filter_config = models.JSONField(default=dict, blank=True)
    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='active')
    created_by = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=36, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.CharField(max_length=36, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'export_templates'
        verbose_name = 'Export Template'
        verbose_name_plural = 'Export Templates'

class ImportFieldMapping(models.Model):
    """
    MANDATORY DOCSTRING - ImportFieldMapping model for import field mapping configuration.
    Source Information:
    - Database Table: import_field_mappings
    - Database Design: DD/database_v0.1.md - Section: import_field_mappings
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Store field mapping configuration for import
    Relationships:
        - Can be referenced by ImportSession
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    id = models.AutoField(primary_key=True)
    mapping_config = models.JSONField(default=dict)
    class Meta:
        db_table = 'import_field_mappings'
        verbose_name = 'Import Field Mapping'
        verbose_name_plural = 'Import Field Mappings'

class BusinessValidationRule(models.Model):
    """
    MANDATORY DOCSTRING - BusinessValidationRule model for business logic validation rules.
    Source Information:
    - Database Table: business_validation_rules
    - Database Design: DD/database_v0.1.md - Section: business_validation_rules
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-05_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Store business validation rules for import/export
    Relationships:
        - Can be referenced by ImportSession, ExportSession
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-05_v0.1.md
    """
    id = models.AutoField(primary_key=True)
    rule_config = models.JSONField(default=dict)
    class Meta:
        db_table = 'business_validation_rules'
        verbose_name = 'Business Validation Rule'
        verbose_name_plural = 'Business Validation Rules'
# --- AUDIT TRAIL ---
import uuid
from django.db import models

class AuditEntry(models.Model):
    """
    MANDATORY DOCSTRING - AuditEntry model for audit trail and operation history.
    
    Source Information (REQUIRED):
    - Database Table: audit_trail
    - Database Design: DD/database_v0.1.md - Section: audit_trail
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-04_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track all resource operations for compliance and reporting
        - Store operation type, resource, user context, details, metadata
        - Support filtering, reporting, archiving, integrity check
    
    Relationships (REQUIRED):
        - Related to resource (resource_id)
    
    Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
    """
    audit_entry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit_operation = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=36)
    operation_details = models.JSONField(default=dict, blank=True)
    user_context = models.JSONField(default=dict, blank=True)
    additional_metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"AuditEntry {self.audit_entry_id} - {self.audit_operation}"
    class Meta:
        db_table = 'audit_trail'
        verbose_name = 'Audit Entry'
        verbose_name_plural = 'Audit Entries'
"""
MANDATORY DOCSTRING - IdleResource model for managing idle personnel information and availability.

Source Information (REQUIRED):
- Database Table: idle_resources
- Database Design: DD/database_v0.1.md - Section: idle_resources
- DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
- Business Module: resource_management

Business Rules (REQUIRED):
    - Track resource type, status, skills, experience, availability, and audit info
    - Link to employee and department
    - Support for optimistic locking (version)

Relationships (REQUIRED):
    - Related to Employee via employee_id (FK or CharField)
    - Related to Department via department_id (FK or CharField)

Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
"""
import uuid
from django.db import models

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
    resource_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for idle resource"
    )
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
        return f"IdleResource {self.resource_id} - {self.employee.full_name} ({self.resource_type})"
    
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
    
    # DAO Methods Implementation
    @classmethod
    def create_with_validation(cls, resource_data, user_context):
        """
        Create idle resource with comprehensive validation.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-01: Create Idle Resource
        
        Arguments:
        - resource_data (dict): Complete idle resource data
        - user_context (dict): User context for audit trail
        
        Returns:
        - Created IdleResource instance
        
        Business Rules:
        - Validate all required fields and constraints
        - Check employee exists and is active
        - Generate unique resource ID
        - Create audit trail entry
        """
        # Validate required fields
        required_fields = ['employee_id', 'resource_type']
        for field in required_fields:
            if field not in resource_data or not resource_data[field]:
                raise ValidationError(f"Required field missing: {field}")
        
        # Validate employee exists
        from authentication.models import Employee
        try:
            employee = Employee.objects.get(
                employee_id=resource_data['employee_id'],
                is_active=True
            )
        except Employee.DoesNotExist:
            raise ValidationError("Employee not found or inactive")
        
        # Create resource with audit info
        resource = cls(
            employee=employee,
            resource_type=resource_data['resource_type'],
            status=resource_data.get('status', 'available'),
            availability_start=resource_data.get('availability_start'),
            availability_end=resource_data.get('availability_end'),
            skills=resource_data.get('skills', []),
            experience_years=resource_data.get('experience_years', 0),
            hourly_rate=resource_data.get('hourly_rate'),
            created_by=user_context['user_id'],
            updated_by=user_context['user_id']
        )
        
        resource.full_clean()  # Run model validation
        resource.save()
        
        return resource
    
    def update_with_version_check(self, update_data, user_context, version_check=True):
        """
        Update resource with optimistic locking version check.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-03: Update Idle Resource
        
        Arguments:
        - update_data (dict): Fields to update
        - user_context (dict): User context for audit
        - version_check (bool): Enable optimistic locking check
        
        Returns:
        - Updated resource instance
        
        Business Rules:
        - Check version conflicts if version_check enabled
        - Validate update permissions
        - Update only provided fields
        - Increment version number automatically (BaseModel)
        """
        if version_check and 'version' in update_data:
            if self.version != update_data['version']:
                raise ValidationError("Version conflict: Resource was modified by another user")
        
        # Update fields
        for field, value in update_data.items():
            if field != 'version' and hasattr(self, field):
                setattr(self, field, value)
        
        self.updated_by = user_context['user_id']
        
        self.full_clean()
        self.save()
        
        return self
    
    @classmethod
    def list_with_filters(cls, filter_criteria=None, sort_options=None, pagination_info=None, user_context=None):
        """
        List idle resources with dynamic filtering and pagination.
        
        Source: DAO-MDE-03-01_v0.1.md - DAO-MDE-03-01-05: List Idle Resources
        
        Arguments:
        - filter_criteria (dict): Filtering criteria
        - sort_options (dict): Sorting configuration
        - pagination_info (dict): Pagination parameters
        - user_context (dict): User context for access control
        
        Returns:
        - Dictionary with resources, count, and pagination info
        
        Business Rules:
        - Apply department-based access control
        - Support dynamic filtering on multiple fields
        - Implement pagination for large datasets
        - Include related data for efficiency
        """
        queryset = cls.objects.filter(
            is_deleted=False
        ).select_related('employee__department')
        
        # Apply access control
        if user_context and user_context.get('role') != 'admin':
            user_departments = user_context.get('department_ids', [])
            queryset = queryset.filter(employee__department_id__in=user_departments)
        
        # Apply filters
        if filter_criteria:
            if 'status' in filter_criteria:
                queryset = queryset.filter(status=filter_criteria['status'])
            if 'resource_type' in filter_criteria:
                queryset = queryset.filter(resource_type=filter_criteria['resource_type'])
            if 'department_id' in filter_criteria:
                queryset = queryset.filter(employee__department_id=filter_criteria['department_id'])
            if 'skills' in filter_criteria:
                # JSON field contains search
                for skill in filter_criteria['skills']:
                    queryset = queryset.filter(skills__contains=skill)
        
        # Apply sorting
        if sort_options:
            order_by = sort_options.get('order_by', 'created_at')
            direction = sort_options.get('direction', 'desc')
            if direction == 'desc':
                order_by = f'-{order_by}'
            queryset = queryset.order_by(order_by)
        
        # Get total count
        total_count = queryset.count()
        
        # Apply pagination
        if pagination_info:
            limit = pagination_info.get('limit', 20)
            offset = pagination_info.get('offset', 0)
            queryset = queryset[offset:offset + limit]
        
        return {
            'resources': list(queryset),
            'total_count': total_count,
            'pagination': {
                'limit': pagination_info.get('limit', 20) if pagination_info else 20,
                'offset': pagination_info.get('offset', 0) if pagination_info else 0,
                'has_next': total_count > (pagination_info.get('offset', 0) + pagination_info.get('limit', 20)) if pagination_info else False
            }
        }
    
    def check_availability(self, start_date, end_date):
        """
        Check resource availability for a date range.
        
        Arguments:
        - start_date (datetime): Start of requested period
        - end_date (datetime): End of requested period
        
        Returns:
        - dict: Availability status and details
        """
        if self.status != 'available':
            return {
                'available': False,
                'reason': f'Resource status is {self.status}'
            }
        
        if self.availability_start and start_date < self.availability_start:
            return {
                'available': False,
                'reason': f'Resource not available until {self.availability_start}'
            }
        
        if self.availability_end and end_date > self.availability_end:
            return {
                'available': False,
                'reason': f'Resource not available after {self.availability_end}'
            }
        
        return {
            'available': True,
            'reason': 'Resource is available for the requested period'
        }
    
    # Bulk Operations Methods (from DAO-MDE-03-03)
    @classmethod
    def bulk_create_resources(cls, resources_data, user_context):
        """
        Create multiple idle resources in batch with validation.
        
        Source: DAO-MDE-03-03_v0.1.md - DAO-MDE-03-03-01: Bulk Create
        
        Arguments:
        - resources_data (list): List of resource data dictionaries
        - user_context (dict): User context for audit trail
        
        Returns:
        - Dictionary with creation results and statistics
        
        Business Rules:
        - Validate all resources before creating any
        - Create all or none (atomic operation)
        - Return detailed results for each resource
        - Log bulk operation for audit
        """
        from django.db import transaction
        
        results = {
            'total_requested': len(resources_data),
            'successfully_created': 0,
            'failed_validations': 0,
            'created_resources': [],
            'validation_errors': [],
            'operation_id': str(uuid.uuid4())
        }
        
        try:
            with transaction.atomic():
                # First pass: validate all resources
                validated_resources = []
                
                for i, resource_data in enumerate(resources_data):
                    try:
                        # Validate employee exists
                        from authentication.models import Employee
                        employee = Employee.objects.get(
                            employee_id=resource_data['employee_id'],
                            is_active=True
                        )
                        
                        # Create resource instance for validation
                        resource = cls(
                            employee=employee,
                            resource_type=resource_data['resource_type'],
                            status=resource_data.get('status', 'available'),
                            availability_start=resource_data.get('availability_start'),
                            availability_end=resource_data.get('availability_end'),
                            skills=resource_data.get('skills', []),
                            experience_years=resource_data.get('experience_years', 0),
                            hourly_rate=resource_data.get('hourly_rate'),
                            created_by=user_context['user_id'],
                            updated_by=user_context['user_id']
                        )
                        
                        # Run validation
                        resource.full_clean()
                        validated_resources.append(resource)
                        
                    except Exception as e:
                        results['validation_errors'].append({
                            'index': i,
                            'resource_data': resource_data,
                            'error': str(e)
                        })
                        results['failed_validations'] += 1
                
                # If any validation failed, abort
                if results['failed_validations'] > 0:
                    raise ValidationError(f"Validation failed for {results['failed_validations']} resources")
                
                # Second pass: bulk create all validated resources
                created_resources = cls.objects.bulk_create(validated_resources)
                results['successfully_created'] = len(created_resources)
                results['created_resources'] = [
                    {
                        'resource_id': str(resource.resource_id),
                        'employee_id': str(resource.employee.employee_id),
                        'resource_type': resource.resource_type,
                        'status': resource.status
                    }
                    for resource in created_resources
                ]
                
        except Exception as e:
            results['error'] = str(e)
            results['successfully_created'] = 0
        
        # Log bulk operation
        AuditEntry.objects.create(
            audit_operation='bulk_create_resources',
            resource_id=results['operation_id'],
            operation_details={
                'total_requested': results['total_requested'],
                'successfully_created': results['successfully_created'],
                'failed_validations': results['failed_validations']
            },
            user_context=user_context
        )
        
        return results
    
    @classmethod
    def bulk_update_resources(cls, resource_updates, user_context):
        """
        Update multiple resources in batch with version checking.
        
        Source: DAO-MDE-03-03_v0.1.md - DAO-MDE-03-03-02: Bulk Update
        
        Arguments:
        - resource_updates (list): List of update dictionaries with resource_id and update_data
        - user_context (dict): User context for audit trail
        
        Returns:
        - Dictionary with update results and statistics
        
        Business Rules:
        - Support version checking for optimistic locking
        - Update only provided fields
        - Handle partial failures gracefully
        - Log all updates for audit
        """
        from django.db import transaction
        
        results = {
            'total_requested': len(resource_updates),
            'successfully_updated': 0,
            'failed_updates': 0,
            'updated_resources': [],
            'update_errors': [],
            'operation_id': str(uuid.uuid4())
        }
        
        for i, update_item in enumerate(resource_updates):
            try:
                with transaction.atomic():
                    resource_id = update_item['resource_id']
                    update_data = update_item['update_data']
                    version_check = update_item.get('version_check', True)
                    
                    # Get resource
                    resource = cls.objects.get(
                        resource_id=resource_id,
                        is_deleted=False
                    )
                    
                    # Apply update
                    updated_resource = resource.update_with_version_check(
                        update_data=update_data,
                        user_context=user_context,
                        version_check=version_check
                    )
                    
                    results['updated_resources'].append({
                        'resource_id': str(updated_resource.resource_id),
                        'version': updated_resource.version,
                        'updated_fields': list(update_data.keys())
                    })
                    results['successfully_updated'] += 1
                    
            except Exception as e:
                results['update_errors'].append({
                    'index': i,
                    'resource_id': update_item.get('resource_id'),
                    'error': str(e)
                })
                results['failed_updates'] += 1
        
        # Log bulk operation
        AuditEntry.objects.create(
            audit_operation='bulk_update_resources',
            resource_id=results['operation_id'],
            operation_details={
                'total_requested': results['total_requested'],
                'successfully_updated': results['successfully_updated'],
                'failed_updates': results['failed_updates']
            },
            user_context=user_context
        )
        
        return results
    
    @classmethod
    def bulk_status_update(cls, resource_ids, new_status, user_context, reason=None):
        """
        Update status for multiple resources at once.
        
        Source: DAO-MDE-03-03_v0.1.md - DAO-MDE-03-03-04: Bulk Status Update
        
        Arguments:
        - resource_ids (list): List of resource IDs to update
        - new_status (str): New status to apply
        - user_context (dict): User context for audit trail
        - reason (str): Optional reason for status change
        
        Returns:
        - Dictionary with update results and statistics
        
        Business Rules:
        - Validate new status is allowed
        - Update all resources atomically
        - Log status changes for audit
        - Support department-based access control
        """
        from django.db import transaction
        
        # Validate status
        valid_statuses = [choice[0] for choice in cls._meta.get_field('status').choices]
        if new_status not in valid_statuses:
            raise ValidationError(f"Invalid status: {new_status}")
        
        results = {
            'total_requested': len(resource_ids),
            'successfully_updated': 0,
            'failed_updates': 0,
            'updated_resources': [],
            'operation_id': str(uuid.uuid4())
        }
        
        try:
            with transaction.atomic():
                # Get resources with access control
                queryset = cls.objects.filter(
                    resource_id__in=resource_ids,
                    is_deleted=False
                )
                
                # Apply department-based access control
                if user_context.get('role') != 'admin':
                    user_departments = user_context.get('department_ids', [])
                    queryset = queryset.filter(employee__department_id__in=user_departments)
                
                # Update resources
                updated_count = queryset.update(
                    status=new_status,
                    updated_by=user_context['user_id'],
                    updated_at=timezone.now()
                )
                
                results['successfully_updated'] = updated_count
                
                # Get updated resources for response
                updated_resources = queryset.filter(status=new_status).values(
                    'resource_id', 'employee__first_name', 'employee__last_name', 'status'
                )
                
                results['updated_resources'] = [
                    {
                        'resource_id': str(resource['resource_id']),
                        'employee_name': f"{resource['employee__first_name']} {resource['employee__last_name']}",
                        'new_status': resource['status']
                    }
                    for resource in updated_resources
                ]
                
        except Exception as e:
            results['error'] = str(e)
            results['failed_updates'] = results['total_requested']
        
        # Log bulk operation
        AuditEntry.objects.create(
            audit_operation='bulk_status_update',
            resource_id=results['operation_id'],
            operation_details={
                'new_status': new_status,
                'reason': reason,
                'total_requested': results['total_requested'],
                'successfully_updated': results['successfully_updated']
            },
            user_context=user_context
        )
        
        return results
    
    @classmethod
    def bulk_delete_resources(cls, resource_ids, user_context, hard_delete=False):
        """
        Delete multiple resources (soft or hard delete).
        
        Source: DAO-MDE-03-03_v0.1.md - DAO-MDE-03-03-03: Bulk Delete
        
        Arguments:
        - resource_ids (list): List of resource IDs to delete
        - user_context (dict): User context for audit trail
        - hard_delete (bool): Whether to perform hard delete
        
        Returns:
        - Dictionary with deletion results and statistics
        
        Business Rules:
        - Default to soft delete for audit trail
        - Support hard delete for data cleanup
        - Check permissions before deletion
        - Log all deletions for audit
        """
        from django.db import transaction
        
        results = {
            'total_requested': len(resource_ids),
            'successfully_deleted': 0,
            'failed_deletions': 0,
            'deleted_resources': [],
            'operation_id': str(uuid.uuid4()),
            'delete_type': 'hard' if hard_delete else 'soft'
        }
        
        try:
            with transaction.atomic():
                # Get resources with access control
                queryset = cls.objects.filter(resource_id__in=resource_ids)
                
                if not hard_delete:
                    queryset = queryset.filter(is_deleted=False)
                
                # Apply department-based access control
                if user_context.get('role') != 'admin':
                    user_departments = user_context.get('department_ids', [])
                    queryset = queryset.filter(employee__department_id__in=user_departments)
                
                # Collect resource info before deletion
                resources_info = list(queryset.values(
                    'resource_id', 'employee__first_name', 'employee__last_name', 'resource_type'
                ))
                
                if hard_delete:
                    # Hard delete
                    deleted_count = queryset.count()
                    queryset.delete()
                else:
                    # Soft delete
                    deleted_count = queryset.update(
                        is_deleted=True,
                        deleted_at=timezone.now(),
                        deleted_by=user_context['user_id']
                    )
                
                results['successfully_deleted'] = deleted_count
                results['deleted_resources'] = [
                    {
                        'resource_id': str(resource['resource_id']),
                        'employee_name': f"{resource['employee__first_name']} {resource['employee__last_name']}",
                        'resource_type': resource['resource_type']
                    }
                    for resource in resources_info
                ]
                
        except Exception as e:
            results['error'] = str(e)
            results['failed_deletions'] = results['total_requested']
        
        # Log bulk operation
        AuditEntry.objects.create(
            audit_operation='bulk_delete_resources',
            resource_id=results['operation_id'],
            operation_details={
                'delete_type': results['delete_type'],
                'total_requested': results['total_requested'],
                'successfully_deleted': results['successfully_deleted']
            },
            user_context=user_context
        )
        
        return results
    
    @classmethod
    def bulk_validate_resources(cls, resources_data):
        """
        Validate multiple resource data without creating records.
        
        Source: DAO-MDE-03-03_v0.1.md - DAO-MDE-03-03-05: Bulk Validate
        
        Arguments:
        - resources_data (list): List of resource data dictionaries
        
        Returns:
        - Dictionary with validation results for each resource
        
        Business Rules:
        - Validate all resources without database changes
        - Return detailed validation feedback
        - Check for duplicate employee assignments
        - Validate business rules and constraints
        """
        results = {
            'total_validated': len(resources_data),
            'valid_resources': 0,
            'invalid_resources': 0,
            'validation_results': [],
            'duplicate_employees': []
        }
        
        # Check for duplicate employee assignments
        employee_ids = [data.get('employee_id') for data in resources_data if data.get('employee_id')]
        duplicates = [emp_id for emp_id in employee_ids if employee_ids.count(emp_id) > 1]
        if duplicates:
            results['duplicate_employees'] = list(set(duplicates))
        
        for i, resource_data in enumerate(resources_data):
            validation_result = {
                'index': i,
                'employee_id': resource_data.get('employee_id'),
                'is_valid': True,
                'errors': [],
                'warnings': []
            }
            
            try:
                # Check required fields
                required_fields = ['employee_id', 'resource_type']
                for field in required_fields:
                    if field not in resource_data or not resource_data[field]:
                        validation_result['errors'].append(f"Required field missing: {field}")
                        validation_result['is_valid'] = False
                
                # Validate employee exists
                if resource_data.get('employee_id'):
                    from authentication.models import Employee
                    try:
                        employee = Employee.objects.get(
                            employee_id=resource_data['employee_id'],
                            is_active=True
                        )
                        
                        # Check if employee already has active idle resource
                        existing = cls.objects.filter(
                            employee=employee,
                            status='available',
                            is_deleted=False
                        ).exists()
                        
                        if existing:
                            validation_result['warnings'].append("Employee already has an active idle resource")
                    
                    except Employee.DoesNotExist:
                        validation_result['errors'].append("Employee not found or inactive")
                        validation_result['is_valid'] = False
                
                # Validate resource type
                if resource_data.get('resource_type'):
                    valid_types = [choice[0] for choice in cls._meta.get_field('resource_type').choices]
                    if resource_data['resource_type'] not in valid_types:
                        validation_result['errors'].append(f"Invalid resource type: {resource_data['resource_type']}")
                        validation_result['is_valid'] = False
                
                # Validate date ranges
                if resource_data.get('availability_start') and resource_data.get('availability_end'):
                    start = resource_data['availability_start']
                    end = resource_data['availability_end']
                    if isinstance(start, str):
                        start = timezone.datetime.fromisoformat(start.replace('Z', '+00:00'))
                    if isinstance(end, str):
                        end = timezone.datetime.fromisoformat(end.replace('Z', '+00:00'))
                    
                    if start >= end:
                        validation_result['errors'].append("Availability start must be before end date")
                        validation_result['is_valid'] = False
                
                # Validate hourly rate
                if resource_data.get('hourly_rate') is not None:
                    try:
                        rate = float(resource_data['hourly_rate'])
                        if rate < 0:
                            validation_result['errors'].append("Hourly rate cannot be negative")
                            validation_result['is_valid'] = False
                    except (ValueError, TypeError):
                        validation_result['errors'].append("Invalid hourly rate format")
                        validation_result['is_valid'] = False
                
            except Exception as e:
                validation_result['errors'].append(f"Validation error: {str(e)}")
                validation_result['is_valid'] = False
            
            results['validation_results'].append(validation_result)
            
            if validation_result['is_valid']:
                results['valid_resources'] += 1
            else:
                results['invalid_resources'] += 1
        
        return results
