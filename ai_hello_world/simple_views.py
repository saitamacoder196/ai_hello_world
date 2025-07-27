"""
Simple API Views for List Screens - No Authentication Required
Trả về mock data cố định cho các màn hình list
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import uuid
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    operation_id='get_idle_resource_list_simple',
    summary='Get Idle Resources List (Simple)',
    description='Lấy danh sách Idle Resources với mock data, không cần authentication',
    tags=['Resource Management'],
    parameters=[
        OpenApiParameter('page', OpenApiTypes.INT, description='Page number', default=1),
        OpenApiParameter('page_size', OpenApiTypes.INT, description='Number of items per page', default=20),
        OpenApiParameter('department', OpenApiTypes.STR, description='Filter by department'),
    ],
    examples=[
        OpenApiExample(
            'Success Response',
            value={
                "records": [
                    {
                        "id": "uuid",
                        "employee_name": "Nguyễn Văn A",
                        "employee_id": "EMP001",
                        "department_name": "Development",
                        "job_rank": "Senior",
                        "idle_type": "Bench"
                    }
                ],
                "total_count": 100,
                "page_info": {
                    "current_page": 1,
                    "total_pages": 5,
                    "has_next_page": True
                }
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_idle_resource_list_simple(request):
    """
    API đơn giản cho danh sách Idle Resources
    GET /api/v1/idle-resources/simple
    """
    
    # Mock data cho màn hình list
    mock_records = []
    for i in range(1, 21):  # Tạo 20 records mẫu
        record = {
            "id": str(uuid.uuid4()),
            "employee_name": f"Nguyễn Văn {chr(65 + i)}",
            "employee_id": f"EMP{i:03d}",
            "department_id": str(uuid.uuid4()),
            "department_name": "Development" if i % 2 == 0 else "QA Testing",
            "job_rank": ["Junior", "Senior", "Expert", "Manager"][i % 4],
            "current_location": "Hanoi" if i % 3 == 0 else "HCMC",
            "expected_working_places": ["Hanoi", "HCMC"],
            "idle_type": ["Bench", "Training", "Available"][i % 3],
            "idle_from_date": "2025-01-01",
            "idle_to_date": "2025-12-31",
            "idle_mm": i % 12 + 1,
            "japanese_level": ["N5", "N4", "N3", "N2", "N1"][i % 5] if i % 2 == 0 else None,
            "english_level": ["Basic", "Intermediate", "Advanced"][i % 3],
            "source_type": "FJPer" if i % 2 == 0 else "Other",
            "sales_price": (i + 10) * 50000,
            "special_action": "Training" if i % 3 == 0 else None,
            "change_dept_lending": "Not Yet Open",
            "skills_experience": f"Java, Spring Boot" if i % 2 == 0 else "Python, Django",
            "progress_notes": f"Progress note {i}",
            "pic": f"Manager {i}",
            "created_at": timezone.now().isoformat(),
            "updated_at": timezone.now().isoformat(),
            "version": 1
        }
        mock_records.append(record)
    
    # Response theo format yêu cầu
    response_data = {
        "records": mock_records,
        "total_count": 100,
        "page_info": {
            "current_page": int(request.GET.get('page', 1)),
            "total_pages": 5,
            "has_next_page": True,
            "has_previous_page": False
        },
        "aggregations": {
            "by_department": {"Development": 45, "QA Testing": 30, "BA": 25},
            "by_idle_type": {"Bench": 60, "Training": 25, "Available": 15}
        },
        "execution_time": 150
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_master_data_simple(request):
    """
    API đơn giản cho Master Data
    GET /api/v1/master-data/simple
    """
    
    response_data = {
        "departments": [
            {"id": "DEPT001", "name": "Development Department", "code": "DEV"},
            {"id": "DEPT002", "name": "QA Testing Department", "code": "QA"},
            {"id": "DEPT003", "name": "Business Analysis Department", "code": "BA"},
            {"id": "DEPT004", "name": "Project Management Department", "code": "PM"}
        ],
        "job_ranks": [
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
        "idle_types": [
            {"id": "BENCH", "name": "Bench", "description": "Waiting for project assignment"},
            {"id": "TRAINING", "name": "Training", "description": "Skills training period"},
            {"id": "AVAILABLE", "name": "Available", "description": "Ready for assignment"}
        ],
        "languages": [
            {"id": "N5", "name": "Japanese N5", "level": 1},
            {"id": "N4", "name": "Japanese N4", "level": 2},
            {"id": "N3", "name": "Japanese N3", "level": 3},
            {"id": "N2", "name": "Japanese N2", "level": 4},
            {"id": "N1", "name": "Japanese N1", "level": 5}
        ],
        "source_types": [
            {"id": "FJPER", "name": "FJPer", "description": "FJ Personnel system"},
            {"id": "OTHER", "name": "Other", "description": "Other sources"}
        ],
        "special_actions": [
            {"id": "TRAINING", "name": "Training", "description": "Skills training"},
            {"id": "WAITING", "name": "Waiting", "description": "Waiting for assignment"}
        ]
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_resource_detail_simple(request, resource_id):
    """
    API đơn giản cho chi tiết Resource
    GET /api/v1/idle-resources/simple/{id}
    """
    
    # Mock chi tiết resource
    detail_data = {
        "id": resource_id,
        "employee_name": "Nguyễn Văn A",
        "employee_id": "EMP001",
        "department_id": str(uuid.uuid4()),
        "department_name": "Development Department",
        "child_department_id": None,
        "job_rank": "Senior",
        "current_location": "Hanoi",
        "expected_working_places": ["Hanoi", "HCMC"],
        "idle_type": "Bench",
        "idle_from_date": "2025-01-01",
        "idle_to_date": "2025-12-31",
        "idle_mm": 12,
        "japanese_level": "N2",
        "english_level": "Intermediate",
        "source_type": "FJPer",
        "sales_price": 500000,
        "special_action": "Training",
        "change_dept_lending": "Not Yet Open",
        "skills_experience": "Java, Spring Boot, React, PostgreSQL",
        "progress_notes": "Ready for new project assignment",
        "pic": "Manager Name",
        "created_at": timezone.now().isoformat(),
        "updated_at": timezone.now().isoformat(),
        "version": 1
    }
    
    return Response(detail_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='login_simple',
    summary='Simple Login (Mock)',
    description='Login đơn giản với mock response, không kiểm tra thực tế',
    tags=['Authentication'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'test_user'},
                'password': {'type': 'string', 'example': 'any_password'}
            }
        }
    },
    examples=[
        OpenApiExample(
            'Login Success',
            value={
                "success": True,
                "message": "Login successful",
                "user_id": "uuid",
                "username": "test_user",
                "access_token": "mock_token_12345",
                "expires_in": 3600
            }
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_simple(request):
    """
    API login đơn giản - luôn trả về thành công
    POST /api/v1/auth/simple/login
    """
    
    # Chỉ cần username từ request
    username = request.data.get('username', 'test_user')
    
    # Mock response đơn giản
    response_data = {
        "success": True,
        "message": "Login successful",
        "user_id": str(uuid.uuid4()),
        "username": username,
        "access_token": "mock_token_" + str(uuid.uuid4()),
        "expires_in": 3600,
        "login_time": timezone.now().isoformat()
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    API kiểm tra trạng thái hệ thống
    GET /api/v1/status
    """
    
    response_data = {
        "status": "running",
        "timestamp": timezone.now().isoformat(),
        "version": "1.0.0",
        "environment": "development",
        "apis_available": [
            "GET /api/v1/idle-resources/simple - Danh sách Idle Resources",
            "GET /api/v1/idle-resources/simple/{id} - Chi tiết Resource",
            "GET /api/v1/master-data/simple - Master Data",
            "POST /api/v1/auth/simple/login - Login đơn giản",
            "GET /api/v1/status - API Status"
        ]
    }
    
    return Response(response_data, status=status.HTTP_200_OK)