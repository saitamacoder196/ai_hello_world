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
    page_size = serializers.IntegerField(default=25, min_value=1, max_value=100)
    sort_by = serializers.CharField(default='idle_from_date', required=False)
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], default='desc', required=False)
    
    # Filters
    department_id = serializers.UUIDField(required=False, allow_null=True)
    idle_type = serializers.CharField(required=False, allow_null=True)
    date_from = serializers.DateField(required=False, allow_null=True)
    date_to = serializers.DateField(required=False, allow_null=True)
    special_action = serializers.CharField(required=False, allow_null=True)
    search_query = serializers.CharField(required=False, allow_null=True)
    urgent_only = serializers.BooleanField(default=False, required=False)
    
    # Column selection
    include_columns = serializers.ListField(
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
    job_ranks = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    locations = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    idle_types = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    languages = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    source_types = MasterDataTypeSerializer(many=True, read_only=True, default=list)
    special_actions = MasterDataTypeSerializer(many=True, read_only=True, default=list)