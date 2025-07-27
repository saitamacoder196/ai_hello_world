# --- IMPORT/EXPORT OPERATIONS ---
import uuid
from django.db import models

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

class IdleResource(models.Model):
    """
    MANDATORY DOCSTRING - IdleResource model for managing idle personnel information and availability.
    Source Information:
    - Database Table: idle_resources
    - Database Design: DD/database_v0.1.md - Section: idle_resources
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    Business Rules:
        - Track resource type, status, skills, experience, availability, and audit info
        - Link to employee and department
        - Support for optimistic locking (version)
    Relationships:
        - Related to Employee via employee_id (FK or CharField)
        - Related to Department via department_id (FK or CharField)
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-01_v0.1.md
    """
    resource_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.CharField(max_length=36)
    resource_type = models.CharField(max_length=50)
    department_id = models.CharField(max_length=36)
    status = models.CharField(max_length=20, default='available')
    availability_start = models.DateTimeField(null=True, blank=True)
    availability_end = models.DateTimeField(null=True, blank=True)
    skills = models.JSONField(default=list, blank=True)
    experience_years = models.IntegerField(default=0, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)
    def __str__(self):
        return f"IdleResource {self.resource_id} ({self.resource_type})"
    class Meta:
        db_table = 'idle_resources'
        verbose_name = 'Idle Resource'
        verbose_name_plural = 'Idle Resources'
