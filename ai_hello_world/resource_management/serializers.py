"""
Resource Management API Serializers

Defines request/response serializers for idle resource management endpoints
with fixed payload structures as specified.
"""

from rest_framework import serializers
from typing import List, Dict, Any


class IdleResourceSerializer(serializers.Serializer):
    """
    Base idle resource data serializer
    """
    id = serializers.UUIDField(read_only=True)
    employee_name = serializers.CharField(max_length=100)
    employee_id = serializers.CharField(max_length=50)
    department_id = serializers.UUIDField()
    child_department_id = serializers.UUIDField(required=False, allow_null=True)
    job_rank = serializers.CharField(max_length=50)
    current_location = serializers.CharField(max_length=100)
    expected_working_places = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list
    )
    idle_type = serializers.CharField(max_length=50)
    idle_from_date = serializers.DateField()
    idle_to_date = serializers.DateField()
    idle_mm = serializers.IntegerField(required=False, allow_null=True)
    japanese_level = serializers.CharField(max_length=20, required=False, allow_null=True)
    english_level = serializers.CharField(max_length=20, required=False, allow_null=True)
    source_type = serializers.CharField(max_length=20, required=False, allow_null=True)
    sales_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    special_action = serializers.CharField(max_length=100, required=False, allow_null=True)
    change_dept_lending = serializers.CharField(max_length=50, required=False, allow_null=True)
    skills_experience = serializers.CharField(required=False, allow_null=True)
    progress_notes = serializers.CharField(required=False, allow_null=True)
    pic = serializers.CharField(max_length=100, required=False, allow_null=True)
    
    # Metadata fields (read-only)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    version = serializers.IntegerField(read_only=True)


class GetIdleResourceListRequestSerializer(serializers.Serializer):
    """
    GET /api/v1/idle-resources request parameters
    """
    page = serializers.IntegerField(default=1, min_value=1)
    pageSize = serializers.IntegerField(default=25, min_value=1, max_value=100)
    sortBy = serializers.CharField(default='idleFrom', required=False)
    sortOrder = serializers.ChoiceField(choices=['asc', 'desc'], default='desc', required=False)
    
    # Filters
    departmentId = serializers.CharField(required=False, allow_null=True)
    idleType = serializers.CharField(required=False, allow_null=True)
    dateFrom = serializers.DateField(required=False, allow_null=True)
    dateTo = serializers.DateField(required=False, allow_null=True)
    specialAction = serializers.CharField(required=False, allow_null=True)
    searchQuery = serializers.CharField(required=False, allow_null=True)
    urgentOnly = serializers.BooleanField(default=False, required=False)
    
    # Column selection
    includeColumns = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )


class PageInfoSerializer(serializers.Serializer):
    """
    Pagination information
    """
    current_page = serializers.IntegerField(read_only=True)
    total_pages = serializers.IntegerField(read_only=True)
    has_next_page = serializers.BooleanField(read_only=True)
    has_previous_page = serializers.BooleanField(read_only=True)


class GetIdleResourceListResponseSerializer(serializers.Serializer):
    """
    GET /api/v1/idle-resources response
    """
    records = IdleResourceSerializer(many=True, read_only=True)
    total_count = serializers.IntegerField(read_only=True)
    page_info = PageInfoSerializer(read_only=True)
    aggregations = serializers.DictField(read_only=True, default=dict)
    execution_time = serializers.IntegerField(read_only=True)


class GetIdleResourceDetailRequestSerializer(serializers.Serializer):
    """
    GET /api/v1/idle-resources/{id} request parameters
    """
    include_audit = serializers.BooleanField(default=True, required=False)
    include_related = serializers.BooleanField(default=False, required=False)


class GetIdleResourceDetailResponseSerializer(IdleResourceSerializer):
    """
    GET /api/v1/idle-resources/{id} response
    Extends IdleResourceSerializer with additional detail fields
    """
    pass  # All fields inherited from IdleResourceSerializer


class CreateIdleResourceRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources request body
    """
    employee_name = serializers.CharField(max_length=100)
    employee_id = serializers.CharField(max_length=50)
    department_id = serializers.UUIDField()
    child_department_id = serializers.UUIDField(required=False, allow_null=True)
    job_rank = serializers.CharField(max_length=50)
    current_location = serializers.CharField(max_length=100)
    expected_working_places = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list
    )
    idle_type = serializers.CharField(max_length=50)
    idle_from_date = serializers.DateField()
    idle_to_date = serializers.DateField()
    japanese_level = serializers.CharField(max_length=20, required=False, allow_null=True)
    english_level = serializers.CharField(max_length=20, required=False, allow_null=True)
    source_type = serializers.CharField(max_length=20, required=False, allow_null=True)
    sales_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    special_action = serializers.CharField(max_length=100, required=False, allow_null=True)
    change_dept_lending = serializers.CharField(max_length=50, required=False, allow_null=True)
    skills_experience = serializers.CharField(required=False, allow_null=True)
    progress_notes = serializers.CharField(required=False, allow_null=True)
    pic = serializers.CharField(max_length=100, required=False, allow_null=True)


class CreateIdleResourceResponseSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources response
    """
    id = serializers.UUIDField(read_only=True)
    created_record = IdleResourceSerializer(read_only=True)
    audit_trail_id = serializers.UUIDField(read_only=True)
    validation_warnings = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        default=list
    )
    business_rule_results = serializers.DictField(read_only=True, default=dict)
    created_at = serializers.DateTimeField(read_only=True)


class UpdateIdleResourceRequestSerializer(serializers.Serializer):
    """
    PUT /api/v1/idle-resources/{id} request body
    """
    employee_name = serializers.CharField(max_length=100, required=False)
    department_id = serializers.UUIDField(required=False)
    idle_to_date = serializers.DateField(required=False)
    progress_notes = serializers.CharField(required=False, allow_null=True)
    version = serializers.IntegerField(required=True)
    
    # Add other fields that can be updated
    job_rank = serializers.CharField(max_length=50, required=False)
    current_location = serializers.CharField(max_length=100, required=False)
    special_action = serializers.CharField(max_length=100, required=False, allow_null=True)
    pic = serializers.CharField(max_length=100, required=False, allow_null=True)


class UpdateIdleResourceResponseSerializer(serializers.Serializer):
    """
    PUT /api/v1/idle-resources/{id} response
    """
    updated_record = IdleResourceSerializer(read_only=True)
    audit_trail_id = serializers.UUIDField(read_only=True)
    validation_warnings = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        default=list
    )
    business_rule_results = serializers.DictField(read_only=True, default=dict)
    updated_at = serializers.DateTimeField(read_only=True)
    changed_fields = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )


class DeleteIdleResourceRequestSerializer(serializers.Serializer):
    """
    DELETE /api/v1/idle-resources/{id} request parameters
    """
    delete_type = serializers.ChoiceField(choices=['soft', 'hard'], default='soft', required=False)
    reason = serializers.CharField(required=False, allow_null=True)
    force = serializers.BooleanField(default=False, required=False)


class DeleteIdleResourceResponseSerializer(serializers.Serializer):
    """
    DELETE /api/v1/idle-resources/{id} response
    """
    deleted = serializers.BooleanField(read_only=True)
    deleted_record = IdleResourceSerializer(read_only=True)
    audit_trail_id = serializers.UUIDField(read_only=True)
    deletion_type = serializers.CharField(read_only=True)
    dependency_warnings = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        default=list
    )
    deleted_at = serializers.DateTimeField(read_only=True)


class BulkUpdateItemSerializer(serializers.Serializer):
    """
    Individual item in bulk update request
    """
    id = serializers.UUIDField()
    data = serializers.DictField()
    version = serializers.IntegerField()


class BulkUpdateIdleResourcesRequestSerializer(serializers.Serializer):
    """
    PATCH /api/v1/idle-resources/bulk request body
    """
    updates = BulkUpdateItemSerializer(many=True)
    rollback_on_error = serializers.BooleanField(default=True)
    validate_all = serializers.BooleanField(default=True)
    operation_id = serializers.CharField(required=False, allow_null=True)


class BulkUpdateResultSerializer(serializers.Serializer):
    """
    Individual result in bulk update response
    """
    id = serializers.UUIDField(read_only=True)
    success = serializers.BooleanField(read_only=True)
    updated_record = IdleResourceSerializer(read_only=True, allow_null=True)
    error_message = serializers.CharField(read_only=True, allow_null=True)
    changed_fields = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        default=list
    )


class BulkUpdateSummarySerializer(serializers.Serializer):
    """
    Summary statistics for bulk update
    """
    total_requested = serializers.IntegerField(read_only=True)
    successful = serializers.IntegerField(read_only=True)
    failed = serializers.IntegerField(read_only=True)
    errors = serializers.IntegerField(read_only=True)
    warnings = serializers.IntegerField(read_only=True)


class BulkUpdateIdleResourcesResponseSerializer(serializers.Serializer):
    """
    PATCH /api/v1/idle-resources/bulk response
    """
    operation_id = serializers.CharField(read_only=True)
    results = BulkUpdateResultSerializer(many=True, read_only=True)
    summary = BulkUpdateSummarySerializer(read_only=True)
    execution_time = serializers.IntegerField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)


class MasterDataTypeSerializer(serializers.Serializer):
    """
    Master data item structure
    """
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True, required=False)
    level = serializers.IntegerField(read_only=True, required=False)
    description = serializers.CharField(read_only=True, required=False)
    country = serializers.CharField(read_only=True, required=False)


class GetMasterDataRequestSerializer(serializers.Serializer):
    """
    GET /api/v1/master-data request parameters
    """
    data_types = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'departments', 'job_ranks', 'locations', 'idle_types',
            'languages', 'source_types', 'special_actions'
        ]),
        required=False,
        default=list
    )
    user_role = serializers.CharField(required=False, allow_null=True)
    department_scope = serializers.CharField(required=False, allow_null=True)


class GetMasterDataResponseSerializer(serializers.Serializer):
    """
    GET /api/v1/master-data response
    """
    departments = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    jobRanks = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    locations = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    idleTypes = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    languages = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    sourceTypes = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    specialActions = MasterDataTypeSerializer(many=True, read_only=True, default=list)


# Export/Import Serializers
class ExportIdleResourcesRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/export request body
    """
    format = serializers.ChoiceField(choices=['excel', 'csv'], default='excel')
    filters = serializers.DictField(required=False, default=dict)
    columns = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    sortBy = serializers.CharField(required=False, default='idleFromDate')
    sortOrder = serializers.ChoiceField(choices=['asc', 'desc'], default='desc', required=False)
    fileName = serializers.CharField(required=False, default='idle_resources_export')
    includeMetadata = serializers.BooleanField(default=True, required=False)
    asyncMode = serializers.BooleanField(default=False, required=False)


class ExportIdleResourcesResponseSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/export response
    """
    exportId = serializers.CharField(read_only=True)
    fileUrl = serializers.URLField(read_only=True)
    fileName = serializers.CharField(read_only=True)
    fileSize = serializers.IntegerField(read_only=True)
    recordCount = serializers.IntegerField(read_only=True)
    format = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    expiresAt = serializers.DateTimeField(read_only=True)
    downloadToken = serializers.CharField(read_only=True)


class ImportIdleResourcesRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/import request body (multipart/form-data)
    """
    file = serializers.FileField()
    importMode = serializers.ChoiceField(
        choices=['validate', 'import', 'update'],
        default='validate'
    )
    duplicateHandling = serializers.ChoiceField(
        choices=['skip', 'update', 'error'],
        default='skip'
    )
    validateOnly = serializers.BooleanField(default=False, required=False)
    columnMapping = serializers.DictField(required=False, default=dict)
    rollbackOnError = serializers.BooleanField(default=True, required=False)
    batchSize = serializers.IntegerField(default=100, min_value=1, max_value=1000)


class ImportErrorReportSerializer(serializers.Serializer):
    """
    Individual error in import report
    """
    row = serializers.IntegerField(read_only=True)
    field = serializers.CharField(read_only=True)
    error = serializers.CharField(read_only=True)


class ImportSummarySerializer(serializers.Serializer):
    """
    Import operation summary
    """
    created = serializers.IntegerField(read_only=True)
    updated = serializers.IntegerField(read_only=True)
    skipped = serializers.IntegerField(read_only=True)


class ImportIdleResourcesResponseSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/import response
    """
    importId = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    totalRows = serializers.IntegerField(read_only=True)
    validRows = serializers.IntegerField(read_only=True)
    invalidRows = serializers.IntegerField(read_only=True)
    processedRows = serializers.IntegerField(read_only=True)
    duplicateRows = serializers.IntegerField(read_only=True)
    errorReport = ImportErrorReportSerializer(many=True, read_only=True, default=list)
    warningReport = serializers.ListField(
        child=serializers.DictField(),
        read_only=True,
        default=list
    )
    importSummary = ImportSummarySerializer(read_only=True)
    auditTrailId = serializers.CharField(read_only=True)


# Advanced Search Serializers
class AdvancedSearchFiltersSerializer(serializers.Serializer):
    """
    Filters for advanced search
    """
    departmentId = serializers.CharField(required=False, allow_null=True)
    idleType = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    dateRange = serializers.DictField(required=False, default=dict)


class AdvancedSearchRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/search request body
    """
    query = serializers.CharField(required=False, default='')
    filters = AdvancedSearchFiltersSerializer(required=False, default=dict)
    facets = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    sortBy = serializers.CharField(required=False, default='updatedAt')
    sortOrder = serializers.ChoiceField(choices=['asc', 'desc'], default='desc', required=False)
    page = serializers.IntegerField(default=1, min_value=1)
    pageSize = serializers.IntegerField(default=20, min_value=1, max_value=100)
    includeCount = serializers.BooleanField(default=True, required=False)
    includeAggregations = serializers.BooleanField(default=True, required=False)
    searchMode = serializers.ChoiceField(
        choices=['standard', 'advanced', 'fuzzy'],
        default='standard'
    )


class SearchMetadataSerializer(serializers.Serializer):
    """
    Search operation metadata
    """
    query = serializers.CharField(read_only=True)
    searchTime = serializers.IntegerField(read_only=True)


class CacheInfoSerializer(serializers.Serializer):
    """
    Cache information for search results
    """
    hit = serializers.BooleanField(read_only=True)
    ttl = serializers.IntegerField(read_only=True)


class AdvancedSearchResponseSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/search response
    """
    results = serializers.ListField(
        child=serializers.DictField(),
        read_only=True,
        default=list
    )
    totalCount = serializers.IntegerField(read_only=True)
    pageInfo = PageInfoSerializer(read_only=True)
    facets = serializers.DictField(read_only=True, default=dict)
    aggregations = serializers.DictField(read_only=True, default=dict)
    searchMetadata = SearchMetadataSerializer(read_only=True)
    suggestedFilters = serializers.ListField(
        child=serializers.DictField(),
        read_only=True,
        default=list
    )
    executionTime = serializers.IntegerField(read_only=True)
    cacheInfo = CacheInfoSerializer(read_only=True)


# Validation Serializers
class ValidateDataRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/validate request body
    """
    data = serializers.DictField()
    validationType = serializers.ChoiceField(
        choices=['basic', 'full', 'business'],
        default='full'
    )
    context = serializers.ChoiceField(
        choices=['create', 'update', 'import'],
        default='create'
    )
    strictMode = serializers.BooleanField(default=False, required=False)
    includeWarnings = serializers.BooleanField(default=True, required=False)
    checkDuplicates = serializers.BooleanField(default=True, required=False)
    businessRules = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )


class ValidationResultSerializer(serializers.Serializer):
    """
    Individual validation result
    """
    field = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)


class ValidationSuggestionSerializer(serializers.Serializer):
    """
    Validation suggestion
    """
    field = serializers.CharField(read_only=True)
    suggestion = serializers.CharField(read_only=True)


class ValidationSummarySerializer(serializers.Serializer):
    """
    Validation summary
    """
    overall = serializers.CharField(read_only=True)
    criticalErrors = serializers.IntegerField(read_only=True)
    warnings = serializers.IntegerField(read_only=True)


class ValidateDataResponseSerializer(serializers.Serializer):
    """
    POST /api/v1/idle-resources/validate response
    """
    isValid = serializers.BooleanField(read_only=True)
    validationResults = ValidationResultSerializer(many=True, read_only=True, default=list)
    errorCount = serializers.IntegerField(read_only=True)
    warningCount = serializers.IntegerField(read_only=True)
    duplicateCount = serializers.IntegerField(read_only=True)
    businessRuleResults = serializers.DictField(read_only=True, default=dict)
    suggestions = ValidationSuggestionSerializer(many=True, read_only=True, default=list)
    validationSummary = ValidationSummarySerializer(read_only=True)