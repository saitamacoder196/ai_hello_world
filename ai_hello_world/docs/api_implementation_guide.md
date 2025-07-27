# API Implementation Guide

## 📋 Overview

This document describes the implemented API endpoints with fixed payload structures. The business logic is commented out and will be implemented later using the service layer architecture.

## 🔐 Authentication APIs

### Base URL: `/api/v1/auth/`

#### 1. User Login
- **Endpoint**: `POST /api/v1/auth/login`
- **Status**: ✅ Implemented with mock response
- **Authentication**: Not required

**Request Body:**
```json
{
    "username": "string",
    "password": "string",
    "language": "en|vi|ja|ko",
    "remember_me": false
}
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "Login successful",
    "is_valid": true,
    "user_id": "uuid",
    "user_profile": {
        "user_id": "uuid",
        "username": "string",
        "email": "email",
        "first_name": "string",
        "last_name": "string",
        "language": "string",
        "phone": "string",
        "avatar_url": "url|null",
        "timezone": "string",
        "date_format": "string",
        "is_active": true,
        "is_verified": true
    },
    "role_info": {
        "roles": [
            {
                "role_id": "uuid",
                "role_name": "string",
                "role_description": "string",
                "is_active": true
            }
        ],
        "permissions": [
            {
                "permission_id": "uuid",
                "permission_name": "string",
                "permission_description": "string",
                "resource_type": "string",
                "action": "string"
            }
        ],
        "department": {
            "department_id": "uuid",
            "department_name": "string",
            "parent_department_id": "uuid|null",
            "is_active": true
        },
        "primary_role": "string"
    },
    "session_id": "uuid",
    "access_token": "string",
    "refresh_token": "string",
    "expires_in": 3600,
    "last_login_time": "datetime|null",
    "login_time": "datetime",
    "authentication_method": "password"
}
```

**Error Response (401):**
```json
{
    "success": false,
    "message": "Authentication failed",
    "errors": ["string"],
    "error_code": "AUTHENTICATION_ERROR",
    "remaining_attempts": 3,
    "lockout_time": null,
    "retry_after": null
}
```

#### 2. User Logout
- **Endpoint**: `POST /api/v1/auth/logout`
- **Status**: ✅ Implemented with mock response
- **Authentication**: Required

**Request Body:**
```json
{
    "session_id": "uuid",
    "access_token": "string"
}
```

**Response (200):**
```json
{
    "success": true,
    "message": "Logout successful",
    "logged_out_at": "datetime"
}
```

#### 3. Validate Session
- **Endpoint**: `POST /api/v1/auth/validate`
- **Status**: ✅ Implemented with mock response

**Request Body:**
```json
{
    "access_token": "string"
}
```

**Response (200):**
```json
{
    "success": true,
    "is_valid": true,
    "message": "Session is valid",
    "user_id": "uuid",
    "session_id": "uuid",
    "expires_in": 3200,
    "user_profile": { /* user profile object */ }
}
```

#### 4. Refresh Token
- **Endpoint**: `POST /api/v1/auth/refresh`
- **Status**: ✅ Implemented with mock response

**Request Body:**
```json
{
    "refresh_token": "string"
}
```

**Response (200):**
```json
{
    "success": true,
    "message": "Token refreshed successfully",
    "access_token": "string",
    "refresh_token": "string",
    "expires_in": 3600,
    "session_id": "uuid",
    "user_id": "uuid"
}
```

#### 5. Health Check
- **Endpoint**: `GET /api/v1/auth/health`
- **Status**: ✅ Implemented

**Response (200):**
```json
{
    "status": "healthy",
    "timestamp": "datetime",
    "version": "1.0.0"
}
```

## 🗂️ Resource Management APIs

### Base URL: `/api/v1/`

#### 1. Get Idle Resource List
- **Endpoint**: `GET /api/v1/idle-resources`
- **Status**: ✅ Implemented with mock response

**Query Parameters:**
```
page=1
page_size=25
sort_by=idle_from_date
sort_order=desc
department_id=uuid
idle_type=string
date_from=2025-01-01
date_to=2025-07-27
special_action=string
search_query=string
urgent_only=false
include_columns[]=field1&include_columns[]=field2
```

**Response (200):**
```json
{
    "records": [
        {
            "id": "uuid",
            "employee_name": "string",
            "employee_id": "string",
            "department_id": "uuid",
            "child_department_id": "uuid|null",
            "job_rank": "string",
            "current_location": "string",
            "expected_working_places": ["string"],
            "idle_type": "string",
            "idle_from_date": "date",
            "idle_to_date": "date",
            "idle_mm": 12,
            "japanese_level": "string|null",
            "english_level": "string|null",
            "source_type": "string|null",
            "sales_price": "decimal|null",
            "special_action": "string|null",
            "change_dept_lending": "string|null",
            "skills_experience": "string|null",
            "progress_notes": "string|null",
            "pic": "string|null",
            "created_at": "datetime",
            "updated_at": "datetime",
            "version": 1
        }
    ],
    "total_count": 100,
    "page_info": {
        "current_page": 1,
        "total_pages": 4,
        "has_next_page": true,
        "has_previous_page": false
    },
    "aggregations": {
        "by_department": {"DEV": 45, "QA": 30, "BA": 25},
        "by_idle_type": {"Bench": 60, "Training": 25, "Available": 15}
    },
    "execution_time": 150
}
```

#### 2. Get Idle Resource Detail
- **Endpoint**: `GET /api/v1/idle-resources/{id}`
- **Status**: ✅ Implemented with mock response

**Query Parameters:**
```
include_audit=true
include_related=false
```

**Response (200):**
```json
{
    // Same structure as list item but with full details
    "id": "uuid",
    // ... all fields from list response
}
```

#### 3. Create Idle Resource
- **Endpoint**: `POST /api/v1/idle-resources/create`
- **Status**: ✅ Implemented with mock response

**Request Body:**
```json
{
    "employee_name": "Nguyen Van A",
    "employee_id": "EMP001",
    "department_id": "uuid",
    "child_department_id": "uuid",
    "job_rank": "Senior",
    "current_location": "Hanoi",
    "expected_working_places": ["Hanoi", "HCMC"],
    "idle_type": "Bench",
    "idle_from_date": "2025-01-01",
    "idle_to_date": "2025-12-31",
    "japanese_level": "N2",
    "english_level": "Intermediate",
    "source_type": "FJPer",
    "sales_price": 500000,
    "special_action": "Training",
    "change_dept_lending": "Not Yet Open",
    "skills_experience": "Java, Spring Boot, React",
    "progress_notes": "Ready for new project",
    "pic": "Manager Name"
}
```

**Response (201):**
```json
{
    "id": "generated-uuid",
    "created_record": {
        // Complete record with all fields including generated ones
    },
    "audit_trail_id": "audit-uuid",
    "validation_warnings": [],
    "business_rule_results": {
        "calculated_fields": ["idle_mm"],
        "applied_rules": ["date_validation", "department_validation"]
    },
    "created_at": "datetime"
}
```

#### 4. Update Idle Resource
- **Endpoint**: `PUT /api/v1/idle-resources/{id}/update`
- **Status**: ✅ Implemented with mock response

**Request Body:**
```json
{
    "employee_name": "Updated Name",
    "department_id": "uuid",
    "idle_to_date": "2025-06-30",
    "progress_notes": "Updated progress",
    "version": 1
}
```

**Response (200):**
```json
{
    "updated_record": {
        // Complete updated record
    },
    "audit_trail_id": "audit-uuid",
    "validation_warnings": [],
    "business_rule_results": {},
    "updated_at": "datetime",
    "changed_fields": ["employee_name", "department_id", "idle_to_date", "progress_notes"]
}
```

#### 5. Delete Idle Resource
- **Endpoint**: `DELETE /api/v1/idle-resources/{id}/delete`
- **Status**: ✅ Implemented with mock response

**Query Parameters:**
```
delete_type=soft
reason=Employee transferred to another department
force=false
```

**Response (200):**
```json
{
    "deleted": true,
    "deleted_record": {
        // Copy of deleted record
    },
    "audit_trail_id": "audit-uuid",
    "deletion_type": "soft",
    "dependency_warnings": [],
    "deleted_at": "datetime"
}
```

#### 6. Bulk Update Idle Resources
- **Endpoint**: `PATCH /api/v1/idle-resources/bulk/update`
- **Status**: ✅ Implemented with mock response

**Request Body:**
```json
{
    "updates": [
        {
            "id": "uuid1",
            "data": {
                "special_action": "Training",
                "progress_notes": "Updated note"
            },
            "version": 1
        },
        {
            "id": "uuid2",
            "data": {
                "idle_to_date": "2025-12-31"
            },
            "version": 2
        }
    ],
    "rollback_on_error": true,
    "validate_all": true,
    "operation_id": "bulk-op-001"
}
```

**Response (200):**
```json
{
    "operation_id": "bulk-op-001",
    "results": [
        {
            "id": "uuid1",
            "success": true,
            "updated_record": { /* complete record */ },
            "error_message": null,
            "changed_fields": ["special_action", "progress_notes"]
        }
    ],
    "summary": {
        "total_requested": 2,
        "successful": 2,
        "failed": 0,
        "errors": 0,
        "warnings": 0
    },
    "execution_time": 500,
    "completed_at": "datetime"
}
```

#### 7. Get Master Data
- **Endpoint**: `GET /api/v1/master-data`
- **Status**: ✅ Implemented with mock response

**Query Parameters:**
```
data_types[]=departments&data_types[]=job_ranks&data_types[]=locations
user_role=RA_DEPT
department_scope=DEPT001
```

**Response (200):**
```json
{
    "departments": [
        {
            "id": "DEPT001",
            "name": "Development Department",
            "code": "DEV"
        }
    ],
    "job_ranks": [
        {
            "id": "SENIOR",
            "name": "Senior Developer",
            "level": 3
        }
    ],
    "locations": [
        {
            "id": "HN",
            "name": "Hanoi",
            "country": "Vietnam"
        }
    ],
    "idle_types": [
        {
            "id": "BENCH",
            "name": "Bench",
            "description": "Waiting for project assignment"
        }
    ],
    "languages": [
        {
            "id": "N2",
            "name": "Japanese N2",
            "level": 4
        }
    ],
    "source_types": [
        {
            "id": "FJPER",
            "name": "FJPer",
            "description": "FJ Personnel system"
        }
    ],
    "special_actions": [
        {
            "id": "TRAINING",
            "name": "Training",
            "description": "Skills training"
        }
    ]
}
```

## 🚀 Testing the APIs

### Using Django Development Server

1. **Start the server:**
```bash
cd "/mnt/d/00. Workshop/ai_hello_world"
python manage.py runserver
```

2. **Test endpoints using curl or Postman:**

```bash
# Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "test_password",
    "language": "en"
  }'

# Test get idle resources
curl -X GET "http://localhost:8000/api/v1/idle-resources?page=1&page_size=10"

# Test get master data
curl -X GET "http://localhost:8000/api/v1/master-data?data_types[]=departments&data_types[]=job_ranks"
```

## 🔧 Implementation Status

### ✅ Completed
- Authentication APIs with full payload structures
- Resource Management APIs with complete CRUD operations
- Master Data API
- Request/Response serializers with validation
- URL routing configuration
- Mock responses with realistic data structures

### 🔄 TODO (Business Logic Implementation)
- Integrate with AuthenticationService for actual authentication
- Implement ResourceCRUDService for database operations
- Add proper user context extraction from JWT tokens
- Implement search and filtering logic
- Add validation service integration
- Implement audit trail logging
- Add proper error handling and business rule validation

### 🎯 Next Steps
1. **Activate service layer logic** by uncommenting the service calls
2. **Implement JWT token parsing** for user authentication
3. **Add database operations** using the existing model methods
4. **Implement search and filtering** using the SearchService
5. **Add validation logic** using the ValidationService
6. **Test with real data** and database operations

## 📚 API Documentation

The APIs follow REST conventions and include:
- Consistent response formats
- Proper HTTP status codes
- Comprehensive error handling
- Pagination support
- Filtering and sorting capabilities
- Bulk operations support
- Audit trail integration (ready for implementation)

All endpoints return structured JSON responses with consistent field naming and data types as specified in the original requirements.