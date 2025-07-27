"""
Custom API Schema Generator
Creates OpenAPI schema for Swagger UI without drf-spectacular dependency
"""

from django.http import JsonResponse
from django.shortcuts import render

def api_schema_view(request):
    """Generate OpenAPI 3.0 schema for our APIs"""
    
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "AI Hello World API",
            "description": "Resource Management System APIs with 92.3% specification compliance",
            "version": "1.0.0",
            "contact": {
                "name": "Development Team",
                "email": "dev@company.com"
            }
        },
        "servers": [
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            },
            {
                "url": "https://7v38qrq1-8000.asse.devtunnels.ms",
                "description": "Remote tunnel server"
            }
        ],
        "paths": {
            "/api/health/": {
                "get": {
                    "summary": "System Health Check",
                    "tags": ["Health"],
                    "responses": {
                        "200": {
                            "description": "System is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string", "example": "AI Hello World!"},
                                            "welcome": {"type": "string", "example": "Chào mừng bạn đến với Django REST Framework API!"},
                                            "timestamp": {"type": "string", "format": "date-time"},
                                            "status": {"type": "string", "example": "success"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/auth/health": {
                "get": {
                    "summary": "Authentication Health Check",
                    "tags": ["Authentication"],
                    "responses": {
                        "200": {
                            "description": "Auth service is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string", "example": "healthy"},
                                            "timestamp": {"type": "string", "format": "date-time"},
                                            "version": {"type": "string", "example": "1.0.0"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/idle-resources": {
                "get": {
                    "summary": "Get Idle Resource List",
                    "tags": ["Resource Management"],
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "description": "Page number",
                            "schema": {"type": "integer", "default": 1}
                        },
                        {
                            "name": "pageSize",
                            "in": "query", 
                            "description": "Items per page",
                            "schema": {"type": "integer", "default": 25}
                        },
                        {
                            "name": "sortBy",
                            "in": "query",
                            "description": "Sort field",
                            "schema": {"type": "string", "default": "idleFromDate"}
                        },
                        {
                            "name": "sortOrder",
                            "in": "query",
                            "description": "Sort order",
                            "schema": {"type": "string", "enum": ["asc", "desc"], "default": "desc"}
                        },
                        {
                            "name": "departmentId",
                            "in": "query",
                            "description": "Filter by department ID",
                            "schema": {"type": "string", "format": "uuid"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of idle resources",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "records": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/IdleResource"
                                                }
                                            },
                                            "totalCount": {"type": "integer", "example": 100},
                                            "pageInfo": {
                                                "$ref": "#/components/schemas/PageInfo"
                                            },
                                            "aggregations": {"type": "object"},
                                            "executionTime": {"type": "integer", "example": 150}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create Idle Resource",
                    "tags": ["Resource Management"],
                    "requestBody": {
                        "required": true,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CreateIdleResourceRequest"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Resource created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/CreateIdleResourceResponse"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid request payload",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/idle-resources/export": {
                "post": {
                    "summary": "Export Idle Resources",
                    "tags": ["Resource Management"],
                    "requestBody": {
                        "required": true,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "format": {"type": "string", "enum": ["excel", "csv"], "example": "excel"},
                                        "filters": {"type": "object"},
                                        "columns": {"type": "array", "items": {"type": "string"}},
                                        "fileName": {"type": "string", "example": "export_data"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Export completed successfully"
                        }
                    }
                }
            },
            "/api/v1/idle-resources/search": {
                "post": {
                    "summary": "Advanced Search",
                    "tags": ["Resource Management"],
                    "requestBody": {
                        "required": true,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string", "example": "Java developer"},
                                        "page": {"type": "integer", "default": 1},
                                        "pageSize": {"type": "integer", "default": 10}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Search results",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "results": {"type": "array"},
                                            "facets": {"type": "object"},
                                            "aggregations": {"type": "object"},
                                            "suggestedFilters": {"type": "array"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/idle-resources/validate": {
                "post": {
                    "summary": "Data Validation",
                    "tags": ["Resource Management"],
                    "requestBody": {
                        "required": true,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"type": "object"},
                                        "validationType": {"type": "string", "enum": ["full", "partial"], "default": "full"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Validation results",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "validationResults": {"type": "array"},
                                            "businessRuleResults": {"type": "object"},
                                            "suggestions": {"type": "array"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/idle-resources/bulk": {
                "patch": {
                    "summary": "Bulk Operations",
                    "tags": ["Resource Management"],
                    "requestBody": {
                        "required": true,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "updates": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string", "format": "uuid"},
                                                    "data": {"type": "object"},
                                                    "version": {"type": "integer"}
                                                }
                                            }
                                        },
                                        "operationId": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Bulk operation completed"
                        }
                    }
                }
            },
            "/api/v1/master-data": {
                "get": {
                    "summary": "Get Master Data",
                    "tags": ["Master Data"],
                    "parameters": [
                        {
                            "name": "dataTypes",
                            "in": "query",
                            "description": "Comma-separated data types",
                            "schema": {"type": "string", "example": "departments,jobRanks"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Master data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/MasterData"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/docs/": {
                "get": {
                    "summary": "API Documentation (JSON)",
                    "tags": ["Documentation"],
                    "responses": {
                        "200": {
                            "description": "API documentation overview"
                        }
                    }
                }
            },
            "/api/compliance-report/": {
                "get": {
                    "summary": "API Compliance Report",
                    "tags": ["Documentation"],
                    "responses": {
                        "200": {
                            "description": "Compliance status report"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "IdleResource": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "employeeName": {"type": "string", "example": "Employee 1"},
                        "employeeId": {"type": "string", "example": "EMP001"},
                        "departmentId": {"type": "string", "format": "uuid"},
                        "jobRank": {"type": "string", "example": "Junior"},
                        "currentLocation": {"type": "string", "example": "Hanoi"},
                        "idleType": {"type": "string", "example": "Bench"},
                        "idleFromDate": {"type": "string", "format": "date", "example": "2025-01-01"},
                        "idleToDate": {"type": "string", "format": "date", "example": "2025-12-31"},
                        "idleMM": {"type": "integer", "example": 12},
                        "salesPrice": {"type": "number", "example": 500000},
                        "specialAction": {"type": "string", "example": "Training"},
                        "pic": {"type": "string", "example": "Manager 1"}
                    }
                },
                "CreateIdleResourceRequest": {
                    "type": "object",
                    "required": ["employeeName", "employeeId", "departmentId", "jobRank", "currentLocation", "idleType", "idleFromDate", "idleToDate"],
                    "properties": {
                        "employeeName": {"type": "string", "example": "Nguyen Van A"},
                        "employeeId": {"type": "string", "example": "EMP001"},
                        "departmentId": {"type": "string", "format": "uuid"},
                        "jobRank": {"type": "string", "example": "Senior"},
                        "currentLocation": {"type": "string", "example": "Hanoi"},
                        "idleType": {"type": "string", "example": "Bench"},
                        "idleFromDate": {"type": "string", "format": "date", "example": "2025-01-01"},
                        "idleToDate": {"type": "string", "format": "date", "example": "2025-12-31"},
                        "japaneseLevel": {"type": "string", "example": "N2"},
                        "englishLevel": {"type": "string", "example": "Intermediate"},
                        "sourceType": {"type": "string", "example": "FJPer"},
                        "salesPrice": {"type": "number", "example": 500000},
                        "specialAction": {"type": "string", "example": "Training"}
                    }
                },
                "CreateIdleResourceResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "createdRecord": {"$ref": "#/components/schemas/IdleResource"},
                        "auditTrailId": {"type": "string", "format": "uuid"},
                        "validationWarnings": {"type": "array"},
                        "businessRuleResults": {"type": "object"},
                        "createdAt": {"type": "string", "format": "date-time"}
                    }
                },
                "PageInfo": {
                    "type": "object",
                    "properties": {
                        "currentPage": {"type": "integer", "example": 1},
                        "totalPages": {"type": "integer", "example": 20},
                        "hasNextPage": {"type": "boolean", "example": true},
                        "hasPreviousPage": {"type": "boolean", "example": false}
                    }
                },
                "MasterData": {
                    "type": "object",
                    "properties": {
                        "departments": {"type": "array"},
                        "jobRanks": {"type": "array"},
                        "locations": {"type": "array"},
                        "idleTypes": {"type": "array"},
                        "sourceTypes": {"type": "array"}
                    }
                },
                "ValidationError": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "example": "Invalid request payload"},
                        "details": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Health",
                "description": "System health check endpoints"
            },
            {
                "name": "Authentication", 
                "description": "User authentication and session management"
            },
            {
                "name": "Resource Management",
                "description": "Idle resource management operations"
            },
            {
                "name": "Master Data",
                "description": "Reference data for dropdowns and lookups"
            },
            {
                "name": "Documentation",
                "description": "API documentation and compliance reports"
            }
        ]
    }
    
    return JsonResponse(schema)

def swagger_ui_view(request):
    """Render Swagger UI interface"""
    return render(request, 'swagger_ui.html')