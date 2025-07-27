"""
Resource Management API Views

Implements idle resource management endpoints with fixed payload structures.
Business logic is commented and will be implemented later using the service layer.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

from .serializers import (
    GetIdleResourceListRequestSerializer,
    GetIdleResourceListResponseSerializer,
    GetIdleResourceDetailRequestSerializer,
    GetIdleResourceDetailResponseSerializer,
    CreateIdleResourceRequestSerializer,
    CreateIdleResourceResponseSerializer,
    UpdateIdleResourceRequestSerializer,
    UpdateIdleResourceResponseSerializer,
    DeleteIdleResourceRequestSerializer,
    DeleteIdleResourceResponseSerializer,
    BulkUpdateIdleResourcesRequestSerializer,
    BulkUpdateIdleResourcesResponseSerializer,
    GetMasterDataRequestSerializer,
    GetMasterDataResponseSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: Change to IsAuthenticated when auth is implemented
def get_idle_resource_list(request):
    """
    Get Idle Resource List API
    
    Endpoint: GET /api/v1/idle-resources
    
    Query Parameters: GetIdleResourceListRequestSerializer
    Response: GetIdleResourceListResponseSerializer
    """
    
    # Parse and validate query parameters
    serializer = GetIdleResourceListRequestSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid query parameters',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract validated parameters
    page = serializer.validated_data.get('page', 1)
    page_size = serializer.validated_data.get('page_size', 25)
    sort_by = serializer.validated_data.get('sort_by', 'idle_from_date')
    sort_order = serializer.validated_data.get('sort_order', 'desc')
    
    # Filter parameters
    filters = {
        'department_id': serializer.validated_data.get('department_id'),
        'idle_type': serializer.validated_data.get('idle_type'),
        'date_from': serializer.validated_data.get('date_from'),
        'date_to': serializer.validated_data.get('date_to'),
        'special_action': serializer.validated_data.get('special_action'),
        'search_query': serializer.validated_data.get('search_query'),
        'urgent_only': serializer.validated_data.get('urgent_only', False)
    }
    
    # TODO: Implement business logic using ResourceCRUDService
    # user_context = _extract_user_context(request)
    # 
    # from services.resource_management.crud_service import ResourceCRUDService
    # crud_service = ResourceCRUDService(user_context)
    # 
    # result = crud_service.list_resources(
    #     filters={k: v for k, v in filters.items() if v is not None},
    #     pagination={'page': page, 'page_size': page_size},
    #     sorting={'field': sort_by, 'order': sort_order}
    # )
    #
    # if not result.success:
    #     return Response({
    #         'error': 'Failed to retrieve resources',
    #         'details': result.errors
    #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # MOCK RESPONSE - Fixed payload for testing
    mock_records = []
    for i in range(min(page_size, 5)):  # Generate up to 5 mock records
        mock_records.append({
            'id': str(uuid.uuid4()),
            'employee_name': f'Employee {i+1}',
            'employee_id': f'EMP{str(i+1).zfill(3)}',
            'department_id': str(uuid.uuid4()),
            'child_department_id': str(uuid.uuid4()) if i % 2 == 0 else None,
            'job_rank': ['Junior', 'Senior', 'Lead', 'Manager'][i % 4],
            'current_location': ['Hanoi', 'HCMC', 'Da Nang'][i % 3],
            'expected_working_places': ['Hanoi', 'HCMC'],
            'idle_type': ['Bench', 'Training', 'Available'][i % 3],
            'idle_from_date': '2025-01-01',
            'idle_to_date': '2025-12-31',
            'idle_mm': 12,
            'japanese_level': ['N1', 'N2', 'N3', None][i % 4],
            'english_level': ['Advanced', 'Intermediate', 'Basic', None][i % 4],
            'source_type': 'FJPer',
            'sales_price': 500000 + (i * 100000),
            'special_action': ['Training', 'Certification', None][i % 3],
            'change_dept_lending': 'Not Yet Open',
            'skills_experience': f'Java, Spring Boot, React - {i+1} years',
            'progress_notes': f'Progress note for employee {i+1}',
            'pic': f'Manager {i+1}',
            'created_at': timezone.now().isoformat(),
            'updated_at': timezone.now().isoformat(),
            'version': 1
        })
    
    mock_response_data = {
        'records': mock_records,
        'total_count': 100,  # Mock total count
        'page_info': {
            'current_page': page,
            'total_pages': (100 + page_size - 1) // page_size,
            'has_next_page': page < ((100 + page_size - 1) // page_size),
            'has_previous_page': page > 1
        },
        'aggregations': {
            'by_department': {'DEV': 45, 'QA': 30, 'BA': 25},
            'by_idle_type': {'Bench': 60, 'Training': 25, 'Available': 15}
        },
        'execution_time': 150
    }
    
    response_serializer = GetIdleResourceListResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_idle_resource_detail(request, resource_id):
    """
    Get Idle Resource Detail API
    
    Endpoint: GET /api/v1/idle-resources/{id}
    
    Query Parameters: GetIdleResourceDetailRequestSerializer
    Response: GetIdleResourceDetailResponseSerializer
    """
    
    # Parse and validate query parameters
    serializer = GetIdleResourceDetailRequestSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid query parameters',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    include_audit = serializer.validated_data.get('include_audit', True)
    include_related = serializer.validated_data.get('include_related', False)
    
    # TODO: Implement business logic using ResourceCRUDService
    # user_context = _extract_user_context(request)
    # 
    # from services.resource_management.crud_service import ResourceCRUDService
    # crud_service = ResourceCRUDService(user_context)
    # 
    # result = crud_service.read_resource(
    #     record_id=resource_id,
    #     include_metadata=include_audit
    # )
    #
    # if not result.success:
    #     return Response({
    #         'error': 'Resource not found',
    #         'details': result.errors
    #     }, status=status.HTTP_404_NOT_FOUND)
    
    # MOCK RESPONSE
    mock_response_data = {
        'id': resource_id,
        'employee_name': 'Nguyen Van A',
        'employee_id': 'EMP001',
        'department_id': str(uuid.uuid4()),
        'child_department_id': str(uuid.uuid4()),
        'job_rank': 'Senior',
        'current_location': 'Hanoi',
        'expected_working_places': ['Hanoi', 'HCMC'],
        'idle_type': 'Bench',
        'idle_from_date': '2025-01-01',
        'idle_to_date': '2025-12-31',
        'idle_mm': 12,
        'japanese_level': 'N2',
        'english_level': 'Intermediate',
        'source_type': 'FJPer',
        'sales_price': 500000,
        'special_action': 'Training',
        'change_dept_lending': 'Not Yet Open',
        'skills_experience': 'Java, Spring Boot, React',
        'progress_notes': 'Currently learning new technologies',
        'pic': 'Manager Name',
        'created_at': timezone.now().isoformat(),
        'updated_at': timezone.now().isoformat(),
        'version': 1
    }
    
    response_serializer = GetIdleResourceDetailResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_idle_resource(request):
    """
    Create Idle Resource API
    
    Endpoint: POST /api/v1/idle-resources
    
    Request Body: CreateIdleResourceRequestSerializer
    Response: CreateIdleResourceResponseSerializer
    """
    
    # Validate request body
    serializer = CreateIdleResourceRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid request payload',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract validated data
    validated_data = serializer.validated_data
    
    # TODO: Implement business logic using ResourceCRUDService
    # user_context = _extract_user_context(request)
    # 
    # from services.resource_management.crud_service import ResourceCRUDService
    # crud_service = ResourceCRUDService(user_context)
    # 
    # result = crud_service.create_resource(
    #     record_data=validated_data,
    #     validation_level='full'
    # )
    #
    # if not result.success:
    #     return Response({
    #         'error': 'Failed to create resource',
    #         'details': result.errors
    #     }, status=status.HTTP_400_BAD_REQUEST)
    
    # MOCK RESPONSE
    generated_id = str(uuid.uuid4())
    mock_created_record = {
        'id': generated_id,
        **validated_data,
        'idle_mm': _calculate_idle_months(
            validated_data.get('idle_from_date'),
            validated_data.get('idle_to_date')
        ),
        'created_at': timezone.now().isoformat(),
        'updated_at': timezone.now().isoformat(),
        'version': 1
    }
    
    mock_response_data = {
        'id': generated_id,
        'created_record': mock_created_record,
        'audit_trail_id': str(uuid.uuid4()),
        'validation_warnings': [],
        'business_rule_results': {
            'calculated_fields': ['idle_mm'],
            'applied_rules': ['date_validation', 'department_validation']
        },
        'created_at': timezone.now().isoformat()
    }
    
    response_serializer = CreateIdleResourceResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_idle_resource(request, resource_id):
    """
    Update Idle Resource API
    
    Endpoint: PUT /api/v1/idle-resources/{id}
    
    Request Body: UpdateIdleResourceRequestSerializer
    Response: UpdateIdleResourceResponseSerializer
    """
    
    # Validate request body
    serializer = UpdateIdleResourceRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid request payload',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract validated data
    validated_data = serializer.validated_data
    version = validated_data.pop('version')
    
    # TODO: Implement business logic using ResourceCRUDService
    # user_context = _extract_user_context(request)
    # 
    # from services.resource_management.crud_service import ResourceCRUDService
    # crud_service = ResourceCRUDService(user_context)
    # 
    # result = crud_service.update_resource(
    #     record_id=resource_id,
    #     update_data=validated_data,
    #     version=version
    # )
    #
    # if not result.success:
    #     return Response({
    #         'error': 'Failed to update resource',
    #         'details': result.errors
    #     }, status=status.HTTP_400_BAD_REQUEST)
    
    # MOCK RESPONSE
    mock_updated_record = {
        'id': resource_id,
        'employee_name': validated_data.get('employee_name', 'Updated Name'),
        'employee_id': 'EMP001',
        'department_id': validated_data.get('department_id', str(uuid.uuid4())),
        'child_department_id': str(uuid.uuid4()),
        'job_rank': validated_data.get('job_rank', 'Senior'),
        'current_location': validated_data.get('current_location', 'Hanoi'),
        'expected_working_places': ['Hanoi', 'HCMC'],
        'idle_type': 'Bench',
        'idle_from_date': '2025-01-01',
        'idle_to_date': validated_data.get('idle_to_date', '2025-06-30'),
        'idle_mm': 6,  # Recalculated
        'japanese_level': 'N2',
        'english_level': 'Intermediate',
        'source_type': 'FJPer',
        'sales_price': 500000,
        'special_action': validated_data.get('special_action', 'Training'),
        'change_dept_lending': 'Not Yet Open',
        'skills_experience': 'Java, Spring Boot, React',
        'progress_notes': validated_data.get('progress_notes', 'Updated progress'),
        'pic': validated_data.get('pic', 'Manager Name'),
        'created_at': (timezone.now() - timedelta(days=30)).isoformat(),
        'updated_at': timezone.now().isoformat(),
        'version': version + 1
    }
    
    changed_fields = list(validated_data.keys())
    
    mock_response_data = {
        'updated_record': mock_updated_record,
        'audit_trail_id': str(uuid.uuid4()),
        'validation_warnings': [],
        'business_rule_results': {
            'calculated_fields': ['idle_mm'],
            'applied_rules': ['date_validation', 'version_check']
        },
        'updated_at': timezone.now().isoformat(),
        'changed_fields': changed_fields
    }
    
    response_serializer = UpdateIdleResourceResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_idle_resource(request, resource_id):
    """
    Delete Idle Resource API
    
    Endpoint: DELETE /api/v1/idle-resources/{id}
    
    Query Parameters: DeleteIdleResourceRequestSerializer
    Response: DeleteIdleResourceResponseSerializer
    """
    
    # Parse and validate query parameters
    serializer = DeleteIdleResourceRequestSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid query parameters',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    delete_type = serializer.validated_data.get('delete_type', 'soft')
    reason = serializer.validated_data.get('reason')
    force = serializer.validated_data.get('force', False)
    
    # TODO: Implement business logic using ResourceCRUDService
    # user_context = _extract_user_context(request)
    # 
    # from services.resource_management.crud_service import ResourceCRUDService
    # crud_service = ResourceCRUDService(user_context)
    # 
    # result = crud_service.delete_resource(
    #     record_id=resource_id,
    #     delete_type=delete_type,
    #     reason=reason
    # )
    #
    # if not result.success:
    #     return Response({
    #         'error': 'Failed to delete resource',
    #         'details': result.errors
    #     }, status=status.HTTP_400_BAD_REQUEST)
    
    # MOCK RESPONSE
    mock_deleted_record = {
        'id': resource_id,
        'employee_name': 'Nguyen Van A',
        'employee_id': 'EMP001',
        'department_id': str(uuid.uuid4()),
        'child_department_id': str(uuid.uuid4()),
        'job_rank': 'Senior',
        'current_location': 'Hanoi',
        'expected_working_places': ['Hanoi', 'HCMC'],
        'idle_type': 'Bench',
        'idle_from_date': '2025-01-01',
        'idle_to_date': '2025-12-31',
        'idle_mm': 12,
        'japanese_level': 'N2',
        'english_level': 'Intermediate',
        'source_type': 'FJPer',
        'sales_price': 500000,
        'special_action': 'Training',
        'change_dept_lending': 'Not Yet Open',
        'skills_experience': 'Java, Spring Boot, React',
        'progress_notes': 'Ready for new project',
        'pic': 'Manager Name',
        'created_at': (timezone.now() - timedelta(days=30)).isoformat(),
        'updated_at': timezone.now().isoformat(),
        'version': 1
    }
    
    mock_response_data = {
        'deleted': True,
        'deleted_record': mock_deleted_record,
        'audit_trail_id': str(uuid.uuid4()),
        'deletion_type': delete_type,
        'dependency_warnings': [],
        'deleted_at': timezone.now().isoformat()
    }
    
    response_serializer = DeleteIdleResourceResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def bulk_update_idle_resources(request):
    """
    Bulk Update Idle Resources API
    
    Endpoint: PATCH /api/v1/idle-resources/bulk
    
    Request Body: BulkUpdateIdleResourcesRequestSerializer
    Response: BulkUpdateIdleResourcesResponseSerializer
    """
    
    # Validate request body
    serializer = BulkUpdateIdleResourcesRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid request payload',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    updates = serializer.validated_data['updates']
    rollback_on_error = serializer.validated_data.get('rollback_on_error', True)
    validate_all = serializer.validated_data.get('validate_all', True)
    operation_id = serializer.validated_data.get('operation_id', str(uuid.uuid4()))
    
    # TODO: Implement business logic using ResourceCRUDService
    # user_context = _extract_user_context(request)
    # 
    # from services.resource_management.crud_service import ResourceCRUDService
    # crud_service = ResourceCRUDService(user_context)
    # 
    # result = crud_service.bulk_update_resources(
    #     updates=updates,
    #     options={
    #         'rollback_on_error': rollback_on_error,
    #         'validate_all': validate_all,
    #         'operation_id': operation_id
    #     }
    # )
    
    # MOCK RESPONSE
    mock_results = []
    successful = 0
    failed = 0
    
    for update in updates:
        is_success = True  # Mock success for most items
        if is_success:
            successful += 1
            mock_updated_record = {
                'id': update['id'],
                'employee_name': 'Updated Name',
                'employee_id': 'EMP001',
                'department_id': str(uuid.uuid4()),
                'job_rank': 'Senior',
                'current_location': 'Hanoi',
                'expected_working_places': ['Hanoi'],
                'idle_type': 'Bench',
                'idle_from_date': '2025-01-01',
                'idle_to_date': '2025-12-31',
                'idle_mm': 12,
                'created_at': timezone.now().isoformat(),
                'updated_at': timezone.now().isoformat(),
                'version': update['version'] + 1
            }
            
            mock_results.append({
                'id': update['id'],
                'success': True,
                'updated_record': mock_updated_record,
                'error_message': None,
                'changed_fields': list(update['data'].keys())
            })
        else:
            failed += 1
            mock_results.append({
                'id': update['id'],
                'success': False,
                'updated_record': None,
                'error_message': 'Version conflict or validation error',
                'changed_fields': []
            })
    
    mock_response_data = {
        'operation_id': operation_id,
        'results': mock_results,
        'summary': {
            'total_requested': len(updates),
            'successful': successful,
            'failed': failed,
            'errors': failed,
            'warnings': 0
        },
        'execution_time': 500,
        'completed_at': timezone.now().isoformat()
    }
    
    response_serializer = BulkUpdateIdleResourcesResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_master_data(request):
    """
    Get Master Data API
    
    Endpoint: GET /api/v1/master-data
    
    Query Parameters: GetMasterDataRequestSerializer
    Response: GetMasterDataResponseSerializer
    """
    
    # Parse and validate query parameters
    serializer = GetMasterDataRequestSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid query parameters',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data_types = serializer.validated_data.get('data_types', [])
    user_role = serializer.validated_data.get('user_role')
    department_scope = serializer.validated_data.get('department_scope')
    
    # TODO: Implement business logic using MasterDataService
    # user_context = _extract_user_context(request)
    # 
    # from services.common.master_data_service import MasterDataService
    # master_data_service = MasterDataService(user_context)
    # 
    # result = master_data_service.get_reference_data(
    #     data_types=data_types,
    #     user_role=user_role,
    #     department_scope=department_scope
    # )
    
    # MOCK RESPONSE
    mock_response_data = {
        'departments': [
            {'id': 'DEPT001', 'name': 'Development Department', 'code': 'DEV'},
            {'id': 'DEPT002', 'name': 'Quality Assurance', 'code': 'QA'},
            {'id': 'DEPT003', 'name': 'Business Analysis', 'code': 'BA'}
        ],
        'job_ranks': [
            {'id': 'JUNIOR', 'name': 'Junior Developer', 'level': 1},
            {'id': 'SENIOR', 'name': 'Senior Developer', 'level': 3},
            {'id': 'LEAD', 'name': 'Technical Lead', 'level': 4},
            {'id': 'MANAGER', 'name': 'Engineering Manager', 'level': 5}
        ],
        'locations': [
            {'id': 'HN', 'name': 'Hanoi', 'country': 'Vietnam'},
            {'id': 'HCMC', 'name': 'Ho Chi Minh City', 'country': 'Vietnam'},
            {'id': 'DN', 'name': 'Da Nang', 'country': 'Vietnam'}
        ],
        'idle_types': [
            {'id': 'BENCH', 'name': 'Bench', 'description': 'Waiting for project assignment'},
            {'id': 'TRAINING', 'name': 'Training', 'description': 'In training or certification'},
            {'id': 'AVAILABLE', 'name': 'Available', 'description': 'Ready for immediate assignment'}
        ],
        'languages': [
            {'id': 'N1', 'name': 'Japanese N1', 'level': 5},
            {'id': 'N2', 'name': 'Japanese N2', 'level': 4},
            {'id': 'N3', 'name': 'Japanese N3', 'level': 3}
        ],
        'source_types': [
            {'id': 'FJPER', 'name': 'FJPer', 'description': 'FJ Personnel system'},
            {'id': 'EXTERNAL', 'name': 'External', 'description': 'External recruitment'}
        ],
        'special_actions': [
            {'id': 'TRAINING', 'name': 'Training', 'description': 'Skills training'},
            {'id': 'CERT', 'name': 'Certification', 'description': 'Professional certification'},
            {'id': 'TRANSFER', 'name': 'Transfer', 'description': 'Department transfer'}
        ]
    }
    
    # Filter based on requested data types if specified
    if data_types:
        filtered_data = {key: value for key, value in mock_response_data.items() if key in data_types}
        mock_response_data = filtered_data
    
    response_serializer = GetMasterDataResponseSerializer(data=mock_response_data)
    response_serializer.is_valid()
    return Response(response_serializer.data, status=status.HTTP_200_OK)


def _extract_user_context(request):
    """Extract user context from request for service layer."""
    # TODO: Implement proper user context extraction from JWT token
    return {
        'user_id': getattr(request.user, 'user_id', None),
        'username': getattr(request.user, 'username', 'anonymous'),
        'role': getattr(request.user, 'role', 'user'),
        'department_id': getattr(request.user, 'department_id', None),
        'permissions': getattr(request.user, 'permissions', []),
        'ip_address': request.META.get('REMOTE_ADDR'),
        'user_agent': request.META.get('HTTP_USER_AGENT')
    }


def _calculate_idle_months(from_date, to_date):
    """Helper function to calculate idle months between two dates."""
    if not from_date or not to_date:
        return None
    
    # Convert string dates to datetime objects if needed
    if isinstance(from_date, str):
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    if isinstance(to_date, str):
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    
    # Calculate difference in months
    months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
    return max(0, months)