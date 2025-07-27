"""
Resource Management API Views - Following API Specification Exactly
Views đúng theo tài liệu API Design specification với đúng request/response format
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
import uuid
import json
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    operation_id='get_idle_resource_list_v1',
    summary='API-MDE-03-01: Get Idle Resource List',
    description='Get paginated list of idle resources with filtering and sorting',
    tags=['Resource Management V1'],
    parameters=[
        OpenApiParameter('page', OpenApiTypes.INT, description='Page number', default=1),
        OpenApiParameter('pageSize', OpenApiTypes.INT, description='Page size', default=25),
        OpenApiParameter('sortBy', OpenApiTypes.STR, description='Sort field', default='idleFrom'),
        OpenApiParameter('sortOrder', OpenApiTypes.STR, description='Sort order', default='desc'),
        OpenApiParameter('departmentId', OpenApiTypes.STR, description='Filter by department'),
        OpenApiParameter('idleType', OpenApiTypes.STR, description='Filter by idle type'),
        OpenApiParameter('dateFrom', OpenApiTypes.STR, description='Filter from date'),
        OpenApiParameter('dateTo', OpenApiTypes.STR, description='Filter to date'),
        OpenApiParameter('specialAction', OpenApiTypes.STR, description='Filter by special action'),
        OpenApiParameter('searchQuery', OpenApiTypes.STR, description='Search query'),
        OpenApiParameter('urgentOnly', OpenApiTypes.BOOL, description='Show urgent only'),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_idle_resource_list(request):
    """
    API-MDE-03-01: Get Idle Resource List
    GET /api/v1/idle-resources
    """
    
    # Extract query parameters với đúng naming convention
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('pageSize', 25))
    sort_by = request.GET.get('sortBy', 'idleFrom')
    sort_order = request.GET.get('sortOrder', 'desc')
    department_id = request.GET.get('departmentId')
    idle_type = request.GET.get('idleType')
    date_from = request.GET.get('dateFrom')
    date_to = request.GET.get('dateTo')
    special_action = request.GET.get('specialAction')
    search_query = request.GET.get('searchQuery')
    urgent_only = request.GET.get('urgentOnly', 'false').lower() == 'true'
    include_columns = request.GET.getlist('includeColumns[]')
    
    # Mock data theo đúng format specification
    mock_records = []
    total_records = 100
    
    for i in range(1, min(page_size + 1, 21)):  # Generate up to page_size records
        record = {
            "id": str(uuid.uuid4()),
            "employeeName": f"Nguyễn Văn {chr(65 + i)}",
            "employeeId": f"EMP{i:03d}",
            "departmentId": str(uuid.uuid4()),
            "childDepartmentId": str(uuid.uuid4()) if i % 3 == 0 else None,
            "jobRank": ["Junior", "Senior", "Expert", "Manager"][i % 4],
            "currentLocation": "Hanoi" if i % 3 == 0 else "HCMC",
            "expectedWorkingPlaces": ["Hanoi", "HCMC"],
            "idleType": ["Bench", "Training", "Available"][i % 3],
            "idleFromDate": "2025-01-01",
            "idleToDate": "2025-12-31",
            "idleMM": i % 12 + 1,
            "japaneseLevel": ["N5", "N4", "N3", "N2", "N1"][i % 5] if i % 2 == 0 else None,
            "englishLevel": ["Basic", "Intermediate", "Advanced"][i % 3],
            "sourceType": "FJPer" if i % 2 == 0 else "Other",
            "salesPrice": (i + 10) * 50000,
            "specialAction": "Training" if i % 3 == 0 else None,
            "changeDeptLending": "Not Yet Open",
            "skillsExperience": f"Java, Spring Boot" if i % 2 == 0 else "Python, Django",
            "progressNotes": f"Progress note {i}",
            "pic": f"Manager {i}",
            "createdAt": timezone.now().isoformat(),
            "updatedAt": timezone.now().isoformat(),
            "version": 1
        }
        mock_records.append(record)
    
    # Response theo đúng specification format
    response_data = {
        "records": mock_records,
        "totalCount": total_records,
        "pageInfo": {
            "currentPage": page,
            "totalPages": (total_records + page_size - 1) // page_size,
            "hasNextPage": page * page_size < total_records,
            "hasPreviousPage": page > 1
        },
        "aggregations": {
            "byDepartment": {"DEV": 45, "QA": 30, "BA": 25},
            "byIdleType": {"Bench": 60, "Training": 25, "Available": 15}
        },
        "executionTime": 150
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='get_idle_resource_detail_v1',
    summary='API-MDE-03-02: Get Idle Resource Detail',
    description='Get detailed information for a specific idle resource',
    tags=['Resource Management V1'],
    parameters=[
        OpenApiParameter('includeAudit', OpenApiTypes.BOOL, description='Include audit information'),
        OpenApiParameter('includeRelated', OpenApiTypes.BOOL, description='Include related data'),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_idle_resource_detail(request, id):
    """
    API-MDE-03-02: Get Idle Resource Detail
    GET /api/v1/idle-resources/{id}
    """
    
    include_audit = request.GET.get('includeAudit', 'false').lower() == 'true'
    include_related = request.GET.get('includeRelated', 'false').lower() == 'true'
    
    # Mock detail data theo specification
    detail_data = {
        "id": str(id),
        "employeeName": "Nguyễn Văn A",
        "employeeId": "EMP001",
        "departmentId": str(uuid.uuid4()),
        "childDepartmentId": str(uuid.uuid4()),
        "jobRank": "Senior",
        "currentLocation": "Hanoi",
        "expectedWorkingPlaces": ["Hanoi", "HCMC"],
        "idleType": "Bench",
        "idleFromDate": "2025-01-01",
        "idleToDate": "2025-12-31",
        "idleMM": 12,
        "japaneseLevel": "N2",
        "englishLevel": "Intermediate",
        "sourceType": "FJPer",
        "salesPrice": 500000,
        "specialAction": "Training",
        "changeDeptLending": "Not Yet Open",
        "skillsExperience": "Java, Spring Boot, React",
        "progressNotes": "Currently learning new technologies",
        "pic": "Manager Name",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": timezone.now().isoformat(),
        "version": 1
    }
    
    if include_audit:
        detail_data["auditInfo"] = {
            "createdBy": "system",
            "updatedBy": "admin",
            "auditTrail": []
        }
    
    if include_related:
        detail_data["relatedData"] = {
            "department": {"name": "Development Department"},
            "employee": {"fullName": "Nguyễn Văn A"}
        }
    
    return Response(detail_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='create_idle_resource_v1',
    summary='API-MDE-03-03: Create Idle Resource',
    description='Create a new idle resource record',
    tags=['Resource Management V1'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'employeeName': {'type': 'string'},
                'employeeId': {'type': 'string'},
                'departmentId': {'type': 'string'},
                'idleFromDate': {'type': 'string', 'format': 'date'},
                'idleToDate': {'type': 'string', 'format': 'date'},
                'idleType': {'type': 'string'},
                'salesPrice': {'type': 'number'},
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_idle_resource(request):
    """
    API-MDE-03-03: Create Idle Resource
    POST /api/v1/idle-resources
    """
    
    # TODO: Validate request data
    request_data = request.data
    
    # Generate new ID
    new_id = str(uuid.uuid4())
    audit_trail_id = str(uuid.uuid4())
    
    # Mock created record with all fields
    created_record = {
        "id": new_id,
        "employeeName": request_data.get('employeeName'),
        "employeeId": request_data.get('employeeId'),
        "departmentId": request_data.get('departmentId'),
        "childDepartmentId": request_data.get('childDepartmentId'),
        "jobRank": request_data.get('jobRank'),
        "currentLocation": request_data.get('currentLocation'),
        "expectedWorkingPlaces": request_data.get('expectedWorkingPlaces', []),
        "idleType": request_data.get('idleType'),
        "idleFromDate": request_data.get('idleFromDate'),
        "idleToDate": request_data.get('idleToDate'),
        "idleMM": 12,  # Calculated field
        "japaneseLevel": request_data.get('japaneseLevel'),
        "englishLevel": request_data.get('englishLevel'),
        "sourceType": request_data.get('sourceType'),
        "salesPrice": request_data.get('salesPrice'),
        "specialAction": request_data.get('specialAction'),
        "changeDeptLending": request_data.get('changeDeptLending'),
        "skillsExperience": request_data.get('skillsExperience'),
        "progressNotes": request_data.get('progressNotes'),
        "pic": request_data.get('pic'),
        "createdAt": timezone.now().isoformat(),
        "updatedAt": timezone.now().isoformat(),
        "version": 1
    }
    
    # Response theo specification
    response_data = {
        "id": new_id,
        "createdRecord": created_record,
        "auditTrailId": audit_trail_id,
        "validationWarnings": [],
        "businessRuleResults": {
            "calculatedFields": ["idleMM"],
            "appliedRules": ["date_validation", "department_validation"]
        },
        "createdAt": timezone.now().isoformat()
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@extend_schema(
    operation_id='update_idle_resource_v1',
    summary='API-MDE-03-04: Update Idle Resource',
    description='Update an existing idle resource record',
    tags=['Resource Management V1']
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_idle_resource(request, id):
    """
    API-MDE-03-04: Update Idle Resource
    PUT /api/v1/idle-resources/{id}
    """
    
    request_data = request.data
    audit_trail_id = str(uuid.uuid4())
    
    # Mock updated record
    updated_record = {
        "id": str(id),
        "employeeName": request_data.get('employeeName', 'Updated Name'),
        "departmentId": request_data.get('departmentId'),
        "idleToDate": request_data.get('idleToDate'),
        "progressNotes": request_data.get('progressNotes'),
        "version": request_data.get('version', 1) + 1,
        "updatedAt": timezone.now().isoformat()
    }
    
    # Find changed fields
    changed_fields = list(request_data.keys())
    
    response_data = {
        "updatedRecord": updated_record,
        "auditTrailId": audit_trail_id,
        "validationWarnings": [],
        "businessRuleResults": {},
        "updatedAt": timezone.now().isoformat(),
        "changedFields": changed_fields
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='delete_idle_resource_v1',
    summary='API-MDE-03-05: Delete Idle Resource',
    description='Delete an idle resource record',
    tags=['Resource Management V1'],
    parameters=[
        OpenApiParameter('deleteType', OpenApiTypes.STR, description='Type of deletion', default='soft'),
        OpenApiParameter('reason', OpenApiTypes.STR, description='Reason for deletion'),
        OpenApiParameter('force', OpenApiTypes.BOOL, description='Force delete', default=False),
    ]
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_idle_resource(request, id):
    """
    API-MDE-03-05: Delete Idle Resource
    DELETE /api/v1/idle-resources/{id}
    """
    
    delete_type = request.GET.get('deleteType', 'soft')
    reason = request.GET.get('reason', '')
    force = request.GET.get('force', 'false').lower() == 'true'
    
    audit_trail_id = str(uuid.uuid4())
    
    # Mock deleted record
    deleted_record = {
        "id": str(id),
        "employeeName": "Deleted Employee",
        "employeeId": "EMP001",
        "deletedAt": timezone.now().isoformat()
    }
    
    response_data = {
        "deleted": True,
        "deletedRecord": deleted_record,
        "auditTrailId": audit_trail_id,
        "deletionType": delete_type,
        "dependencyWarnings": [],
        "deletedAt": timezone.now().isoformat()
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='bulk_update_idle_resources_v1',
    summary='API-MDE-03-06: Bulk Update Idle Resources',
    description='Update multiple idle resource records in a single operation',
    tags=['Resource Management V1']
)
@api_view(['PATCH'])
@permission_classes([AllowAny])
def bulk_update_idle_resources(request):
    """
    API-MDE-03-06: Bulk Update Idle Resources
    PATCH /api/v1/idle-resources/bulk
    """
    
    request_data = request.data
    updates = request_data.get('updates', [])
    operation_id = request_data.get('operationId', str(uuid.uuid4()))
    
    # Process each update
    results = []
    audit_trail_ids = []
    
    for update in updates:
        resource_id = update.get('id')
        update_data = update.get('data', {})
        version = update.get('version', 1)
        
        # Mock successful update
        result = {
            "id": resource_id,
            "status": "success",
            "updatedRecord": {
                "id": resource_id,
                "version": version + 1,
                "updatedAt": timezone.now().isoformat(),
                **update_data
            }
        }
        results.append(result)
        audit_trail_ids.append(str(uuid.uuid4()))
    
    response_data = {
        "operationId": operation_id,
        "totalRequested": len(updates),
        "successCount": len(results),
        "failureCount": 0,
        "results": results,
        "auditTrailIds": audit_trail_ids,
        "operationStatus": "completed",
        "executionTime": 1500
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def export_idle_resources(request):
    """API-MDE-03-07: Export Idle Resources"""
    
    request_data = request.data
    export_id = str(uuid.uuid4())
    
    response_data = {
        "exportId": export_id,
        "fileUrl": f"https://storage.example.com/exports/{export_id}.xlsx",
        "fileName": f"idle_resources_export_{timezone.now().strftime('%Y%m%d')}.xlsx",
        "fileSize": 2048576,
        "recordCount": 150,
        "format": request_data.get('format', 'excel'),
        "status": "completed",
        "createdAt": timezone.now().isoformat(),
        "expiresAt": (timezone.now() + timedelta(days=1)).isoformat(),
        "downloadToken": str(uuid.uuid4())
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def import_idle_resources(request):
    """API-MDE-03-08: Import Idle Resources"""
    
    response_data = {
        "importId": str(uuid.uuid4()),
        "totalRows": 100,
        "validRows": 95,
        "invalidRows": 5,
        "processedRows": 95,
        "duplicateRows": 2,
        "errorReport": [
            {
                "row": 3,
                "field": "employeeId",
                "error": "Required field missing"
            }
        ],
        "warningReport": [],
        "importSummary": {
            "created": 90,
            "updated": 5,
            "skipped": 5
        },
        "auditTrailId": str(uuid.uuid4())
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def search_idle_resources(request):
    """API-MDE-03-09: Advanced Search Idle Resources"""
    
    request_data = request.data
    
    # Mock search results
    mock_results = []
    for i in range(1, 11):
        mock_results.append({
            "id": str(uuid.uuid4()),
            "employeeName": f"Search Result {i}",
            "employeeId": f"EMP{i:03d}",
            "departmentId": str(uuid.uuid4()),
            "idleType": "Bench",
            "relevanceScore": 0.9 - (i * 0.05)
        })
    
    response_data = {
        "results": mock_results,
        "totalCount": 50,
        "pageInfo": {
            "currentPage": 1,
            "totalPages": 3,
            "hasNextPage": True
        },
        "facets": {
            "departmentId": {"DEPT001": 30, "DEPT002": 20},
            "idleType": {"Bench": 35, "Training": 15}
        },
        "aggregations": {},
        "searchMetadata": {
            "query": request_data.get('query', ''),
            "searchTime": 120
        },
        "suggestedFilters": [],
        "executionTime": 120,
        "cacheInfo": {
            "hit": False,
            "ttl": 300
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def validate_idle_resource_data(request):
    """API-MDE-03-13: Validate Data"""
    
    request_data = request.data
    data_to_validate = request_data.get('data', {})
    
    # Mock validation results
    validation_results = []
    
    # Example validation: Check date range
    idle_from = data_to_validate.get('idleFromDate')
    idle_to = data_to_validate.get('idleToDate')
    
    if idle_from and idle_to and idle_from >= idle_to:
        validation_results.append({
            "field": "idleToDate",
            "type": "error",
            "message": "Idle To Date must be greater than or equal to Idle From Date",
            "code": "INVALID_DATE_RANGE"
        })
    
    is_valid = len(validation_results) == 0
    
    response_data = {
        "isValid": is_valid,
        "validationResults": validation_results,
        "errorCount": len([r for r in validation_results if r['type'] == 'error']),
        "warningCount": len([r for r in validation_results if r['type'] == 'warning']),
        "duplicateCount": 0,
        "businessRuleResults": {},
        "suggestions": [
            {
                "field": "idleToDate",
                "suggestion": "Set date to 2025-12-31 or later"
            }
        ] if not is_valid else [],
        "validationSummary": {
            "overall": "passed" if is_valid else "failed",
            "criticalErrors": 1 if not is_valid else 0,
            "warnings": 0
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='get_master_data_v1',
    summary='Get Master Data',
    description='Get reference data for dropdowns and lookups',
    tags=['Master Data V1'],
    parameters=[
        OpenApiParameter('dataTypes', OpenApiTypes.STR, description='Comma-separated list of data types'),
        OpenApiParameter('userRole', OpenApiTypes.STR, description='User role for filtering'),
        OpenApiParameter('departmentScope', OpenApiTypes.STR, description='Department scope'),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_master_data(request):
    """
    Get Master Data
    GET /api/v1/master-data
    """
    
    data_types = request.GET.get('dataTypes', '').split(',')
    user_role = request.GET.get('userRole')
    department_scope = request.GET.get('departmentScope')
    
    response_data = {
        "departments": [
            {"id": "DEPT001", "name": "Development Department", "code": "DEV"},
            {"id": "DEPT002", "name": "QA Testing Department", "code": "QA"},
            {"id": "DEPT003", "name": "Business Analysis Department", "code": "BA"},
            {"id": "DEPT004", "name": "Project Management Department", "code": "PM"}
        ],
        "jobRanks": [
            {"id": "JUNIOR", "name": "Junior Developer", "level": 1},
            {"id": "SENIOR", "name": "Senior Developer", "level": 2},
            {"id": "EXPERT", "name": "Expert Developer", "level": 3},
            {"id": "MANAGER", "name": "Team Manager", "level": 4}
        ],
        "locations": [
            {"id": "HN", "name": "Hanoi", "country": "Vietnam"},
            {"id": "HCMC", "name": "Ho Chi Minh City", "country": "Vietnam"},
            {"id": "DN", "name": "Da Nang", "country": "Vietnam"}
        ],
        "idleTypes": [
            {"id": "BENCH", "name": "Bench", "description": "Waiting for project assignment"},
            {"id": "TRAINING", "name": "Training", "description": "Skills training period"},
            {"id": "AVAILABLE", "name": "Available", "description": "Ready for assignment"}
        ]
    }
    
    # Filter based on requested data types
    if data_types and data_types[0]:
        filtered_response = {}
        for data_type in data_types:
            data_type = data_type.strip()
            if data_type in response_data:
                filtered_response[data_type] = response_data[data_type]
        response_data = filtered_response
    
    return Response(response_data, status=status.HTTP_200_OK)