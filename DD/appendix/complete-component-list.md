# Complete Project Component List - Idle Resource Management System

**Document Version**: v0.1  
**Generated Date**: 2025-07-25  
**Source**: System Analysis and Design Documents  

## Project Overview

This document provides a comprehensive list of all components in the Idle Resource Management System organized by modules and component types.

---

## Modules

| ID     | Name                                        | Description |
|--------|---------------------------------------------|-------------|
| MDE-01 | Authentication and Session Management       | Handles user authentication, session establishment, and basic security controls. Provides the foundation for secure system access and maintains user session state throughout system interaction. |
| MDE-02 | Authorization and Role Management           | Manages comprehensive role-based access control system with five distinct user roles and department-level data segregation. Controls user permissions across all system functions and data access. |
| MDE-03 | Idle Resource Data Management               | Core business module handling complete lifecycle of idle resource information from initial entry through resolution tracking. Manages comprehensive employee idle data with advanced search, filtering, and batch operations. |
| MDE-04 | CV Processing and File Management           | Handles CV file upload, secure storage, AI-powered content extraction, and role-based file access. Integrates extracted information with idle resource skill fields. |
| MDE-05 | Master Data Management                      | Manages enumerated values, dropdown lists, and reference data used throughout the system. Handles synchronization with external organizational data sources. |
| MDE-06 | Reporting and Analytics                     | Provides comprehensive reporting capabilities including standard reports, analytical reports, and flexible custom reporting. Handles automated report generation and dashboard integration. |
| MDE-07 | System Automation and Configuration        | Manages automated system processes, configuration settings, and background tasks. Handles weekly baseline generation and system maintenance functions. |
| MDE-08 | Audit Trail and Logging                    | Captures and maintains comprehensive audit trail of all system activities, data changes, and user actions for compliance and analysis purposes. |

---

## Screens by Module

### MDE-01: Authentication and Session Management
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-01-01 | Login Screen | Provides user authentication interface with credential input, validation feedback, and language selection. Features username/password input, error messaging, language preference selection, and session initiation. |

### MDE-02: Authorization and Role Management
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-02-01 | User Management Screen | Administrative interface for managing user accounts, role assignments, and access permissions. Features user account creation and modification, role assignment and permission management, department access configuration, user activity monitoring, and bulk user operations. |

### MDE-03: Idle Resource Data Management
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-03-01 | Idle Resource List Screen | Primary data management interface displaying idle resource records in tabular format with comprehensive search, filter, and management capabilities. Features 30+ column data table, advanced search and filtering controls, column management, batch operations, and pagination. |
| SCR-MDE-03-02 | Idle Resource Detail/Edit Screen | Detailed form interface for viewing and editing individual idle resource records with all data fields and validation. Features complete data entry form, dropdown lists with search, date pickers, multi-select controls, and field-level validation. |
| SCR-MDE-03-03 | Import/Export Screen | Interface for bulk data import from Excel files and export operations with format selection. Features Excel file upload and validation, import mapping, export format selection, process monitoring, and error reporting. |

### MDE-04: CV Processing and File Management
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-04-01 | CV Upload and Management Screen | Interface for CV file upload, AI processing management, and skill extraction review. Features file upload with drag-and-drop, AI processing status display, extracted skill data review, CV file preview and download, and processing history. |

### MDE-05: Master Data Management
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-05-01 | Master Data Management Screen | Administrative interface for managing enumerated values, dropdown options, and reference data. Features dropdown value management, custom option addition, organizational chart synchronization, data validation rule configuration, and import/export of master data. |

### MDE-06: Reporting and Analytics
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-06-01 | Dashboard Home Screen | Central landing page displaying key metrics, recent activities, and quick access to primary functions. Features real-time metrics display, quick navigation, notification center, and dashboard widgets. |
| SCR-MDE-06-02 | Standard Reports Screen | Interface for generating and viewing standard idle resource reports with filtering options. Features report type selection, filter configuration, report preview and generation, export format selection, and report history. |
| SCR-MDE-06-03 | Long-term Idle Analysis Screen | Specialized reporting interface for analyzing resources idle for 2+ months with special action tracking. Features automatic filtering, special action analysis, trend visualization, department breakdown, and export capabilities. |
| SCR-MDE-06-04 | Baseline Comparison Screen | Displays weekly baseline comparison reports with departmental progress tracking. Features week-over-week comparison charts, department performance metrics, trend analysis, drill-down capability, and automated report scheduling. |
| SCR-MDE-06-05 | Flexible Report Builder Screen | Advanced reporting interface allowing custom report creation with multiple filter criteria and output options. Features custom filter configuration, field selection, multiple export formats, report template saving, and advanced query builder. |

### MDE-07: System Automation and Configuration
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-07-01 | System Configuration Screen | Administrative interface for managing system settings, automated processes, and configuration parameters. Features baseline generation scheduling, system parameter configuration, automated process monitoring, and system health display. |

### MDE-08: Audit Trail and Logging
| ID | Name | Description |
|----|------|-------------|
| SCR-MDE-08-01 | Audit Trail Screen | Interface for viewing system audit logs, user activities, and data change history. Features audit log search and filtering, user activity tracking, data change history display, export audit reports, and compliance reporting tools. |

---

## APIs by Module

### MDE-01: Authentication and Session Management
| ID | Name | Description |
|----|------|-------------|
| API-MDE-01-01 | User Authentication | Validates user credentials and establishes secure session with JWT token generation. |
| API-MDE-01-02 | Session Management | Manages user session state, token refresh, and session termination. |
| API-MDE-01-03 | Password Management | Handles password changes, resets, and security policy enforcement. |
| API-MDE-01-04 | Security Validation | Validates security policies, monitors login attempts, and enforces account lockout. |

### MDE-02: Authorization and Role Management
| ID | Name | Description |
|----|------|-------------|
| API-MDE-02-01 | User Role Management | Manages user role assignments and permission matrix enforcement. |
| API-MDE-02-02 | Permission Validation | Validates user permissions for specific operations and data access. |
| API-MDE-02-03 | Department Access Control | Enforces department-level data access restrictions based on user roles. |
| API-MDE-02-04 | User Account Management | Handles user account creation, modification, and deactivation. |

### MDE-03: Idle Resource Data Management
| ID | Name | Description |
|----|------|-------------|
| API-MDE-03-01 | Get Idle Resource List | Retrieves paginated list of idle resource records with filtering and sorting. |
| API-MDE-03-02 | Get Idle Resource Detail | Retrieves detailed information for specific idle resource record. |
| API-MDE-03-03 | Create Idle Resource | Creates new idle resource record with validation and audit trail. |
| API-MDE-03-04 | Update Idle Resource | Updates existing idle resource record with business rule enforcement. |
| API-MDE-03-05 | Delete Idle Resource | Soft delete of idle resource record with audit trail logging. |
| API-MDE-03-06 | Batch Update Idle Resources | Performs bulk updates on multiple idle resource records. |
| API-MDE-03-07 | Search Idle Resources | Advanced search functionality with multi-field query support. |
| API-MDE-03-08 | Get Idle Resource Statistics | Retrieves aggregated statistics and metrics for dashboard display. |
| API-MDE-03-09 | Export Idle Resources | Generates export files in various formats with role-based filtering. |
| API-MDE-03-10 | Import Idle Resources | Handles bulk import of data from Excel files with validation. |
| API-MDE-03-11 | Get Column Configuration | Retrieves user-specific column preferences and layout settings. |
| API-MDE-03-12 | Update Column Configuration | Updates user preferences for column visibility and ordering. |
| API-MDE-03-13 | Validate Idle Resource Data | Validates data against business rules and constraints. |
| API-MDE-03-14 | Get Audit Trail | Retrieves audit trail entries for idle resource records. |
| API-MDE-03-15 | Get Department Summary | Provides department-level summary statistics and metrics. |

### MDE-04: CV Processing and File Management
| ID | Name | Description |
|----|------|-------------|
| API-MDE-04-01 | Upload CV File | Handles CV file upload with validation and secure storage. |
| API-MDE-04-02 | Process CV with AI | Initiates AI processing for skill extraction from CV files. |
| API-MDE-04-03 | Get CV Processing Status | Retrieves status of AI processing operations. |
| API-MDE-04-04 | Download CV File | Provides secure CV file download with role-based access control. |
| API-MDE-04-05 | Get Extracted Skills | Retrieves AI-extracted skill data from CV processing. |
| API-MDE-04-06 | Update Extracted Skills | Allows manual editing of AI-extracted skill information. |
| API-MDE-04-07 | Get CV File List | Retrieves list of CV files associated with idle resources. |

### MDE-05: Master Data Management
| ID | Name | Description |
|----|------|-------------|
| API-MDE-05-01 | Get Master Data | Retrieves enumerated values and reference data for dropdowns. |
| API-MDE-05-02 | Update Master Data | Updates enumerated values and reference data with validation. |
| API-MDE-05-03 | Sync Organizational Chart | Synchronizes with FJP organizational chart data. |
| API-MDE-05-04 | Get Department Hierarchy | Retrieves department and child department structure. |
| API-MDE-05-05 | Validate Reference Data | Validates reference data consistency and integrity. |

### MDE-06: Reporting and Analytics
| ID | Name | Description |
|----|------|-------------|
| API-MDE-06-01 | Generate Standard Report | Creates standard idle resource reports with filtering options. |
| API-MDE-06-02 | Generate Long-term Analysis | Creates specialized reports for resources idle 2+ months. |
| API-MDE-06-03 | Generate Baseline Comparison | Creates weekly baseline comparison reports. |
| API-MDE-06-04 | Generate Custom Report | Creates flexible custom reports with user-defined criteria. |
| API-MDE-06-05 | Get Dashboard Metrics | Retrieves real-time metrics and KPIs for dashboard display. |
| API-MDE-06-06 | Export Report | Exports reports in various formats (Excel, PDF, CSV). |
| API-MDE-06-07 | Schedule Report | Manages automated report generation and distribution. |

### MDE-07: System Automation and Configuration
| ID | Name | Description |
|----|------|-------------|
| API-MDE-07-01 | Configure Baseline Generation | Manages weekly baseline generation scheduling and parameters. |
| API-MDE-07-02 | Get System Configuration | Retrieves system configuration parameters and settings. |
| API-MDE-07-03 | Update System Configuration | Updates system configuration with validation. |
| API-MDE-07-04 | Monitor Background Processes | Monitors status of automated processes and background tasks. |
| API-MDE-07-05 | Get System Health Status | Retrieves system health metrics and performance indicators. |

### MDE-08: Audit Trail and Logging
| ID | Name | Description |
|----|------|-------------|
| API-MDE-08-01 | Get Audit Logs | Retrieves audit trail entries with filtering and pagination. |
| API-MDE-08-02 | Create Audit Entry | Creates new audit trail entries for system activities. |
| API-MDE-08-03 | Export Audit Report | Generates audit reports for compliance and analysis. |
| API-MDE-08-04 | Get User Activity | Retrieves user activity logs and session information. |

---

## Services by Module

### MDE-01: Authentication and Session Management
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-01-01 | Authentication Service | Core authentication logic with credential validation and security enforcement. |
| SVE-MDE-01-02 | Session Management Service | Manages user sessions, token lifecycle, and security policies. |
| SVE-MDE-01-03 | Security Policy Service | Enforces password policies, login attempt monitoring, and account lockout. |

### MDE-02: Authorization and Role Management
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-02-01 | Role Management Service | Manages user roles, permissions, and access control matrices. |
| SVE-MDE-02-02 | Permission Enforcement Service | Enforces role-based permissions and department-level access control. |
| SVE-MDE-02-03 | User Account Service | Handles user account lifecycle and profile management. |

### MDE-03: Idle Resource Data Management
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-03-01 | Idle Resource CRUD Service | Core CRUD operations with business rule validation and audit trail. |
| SVE-MDE-03-02 | Idle Resource Search Service | Advanced search with multi-field queries and role-based filtering. |
| SVE-MDE-03-03 | Idle Resource Validation Service | Comprehensive validation of business rules and data integrity. |
| SVE-MDE-03-04 | Batch Operations Service | Bulk operations with transaction management and rollback capabilities. |
| SVE-MDE-03-05 | Data Import Service | Excel import with validation, conflict resolution, and error reporting. |
| SVE-MDE-03-06 | Data Export Service | Multi-format export with role-based filtering and optimization. |
| SVE-MDE-03-07 | Idle Resource Statistics Service | Analytics and metrics calculation for reporting and dashboards. |
| SVE-MDE-03-08 | Department Access Control Service | Department-level data access control and filtering. |
| SVE-MDE-03-09 | Column Configuration Service | User preference management for interface customization. |
| SVE-MDE-03-10 | Audit Trail Service | Change tracking and audit trail maintenance. |
| SVE-MDE-03-11 | Business Rule Engine Service | Complex business logic implementation and validation. |
| SVE-MDE-03-12 | Data Integrity Service | Data consistency and referential integrity enforcement. |
| SVE-MDE-03-13 | Notification Service | Automated notifications for status changes and events. |
| SVE-MDE-03-14 | Integration Orchestration Service | Cross-module integration and data synchronization. |
| SVE-MDE-03-15 | Performance Optimization Service | Caching, query optimization, and performance monitoring. |

### MDE-04: CV Processing and File Management
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-04-01 | CV File Management Service | File upload, storage, and retrieval with security controls. |
| SVE-MDE-04-02 | AI Processing Service | Integration with AI services for skill extraction and processing. |
| SVE-MDE-04-03 | Skill Extraction Service | Processing and integration of AI-extracted skill data. |
| SVE-MDE-04-04 | File Security Service | Access control and security for CV file operations. |

### MDE-05: Master Data Management
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-05-01 | Master Data Service | Management of enumerated values and reference data. |
| SVE-MDE-05-02 | Organizational Chart Service | Synchronization with FJP organizational structure. |
| SVE-MDE-05-03 | Data Validation Service | Validation of master data consistency and integrity. |

### MDE-06: Reporting and Analytics
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-06-01 | Report Generation Service | Standard report creation with filtering and formatting. |
| SVE-MDE-06-02 | Analytics Service | Advanced analytics and trend analysis for long-term idle cases. |
| SVE-MDE-06-03 | Dashboard Service | Real-time metrics and KPI calculation for dashboard display. |
| SVE-MDE-06-04 | Export Service | Multi-format report export with optimization. |
| SVE-MDE-06-05 | Custom Report Service | Flexible report builder with user-defined criteria. |

### MDE-07: System Automation and Configuration
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-07-01 | Automation Service | Background process management and scheduled task execution. |
| SVE-MDE-07-02 | Configuration Management Service | System configuration and parameter management. |
| SVE-MDE-07-03 | Baseline Generation Service | Weekly baseline data snapshot creation and management. |
| SVE-MDE-07-04 | System Monitoring Service | System health monitoring and performance tracking. |

### MDE-08: Audit Trail and Logging
| ID | Name | Description |
|----|------|-------------|
| SVE-MDE-08-01 | Audit Trail Service | Comprehensive audit logging and trail maintenance. |
| SVE-MDE-08-02 | Compliance Service | Compliance reporting and audit data management. |
| SVE-MDE-08-03 | Activity Tracking Service | User activity monitoring and session tracking. |

---

## DAOs by Module

### MDE-01: Authentication and Session Management
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-01-01 | User Authentication DAO | Database operations for user credential validation and authentication data. |
| DAO-MDE-01-02 | Session Management DAO | Session data persistence and retrieval operations. |
| DAO-MDE-01-03 | Security Policy DAO | Security policy data and login attempt tracking operations. |

### MDE-02: Authorization and Role Management
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-02-01 | User Role DAO | User role and permission data access operations. |
| DAO-MDE-02-02 | Permission Matrix DAO | Permission matrix and access control data operations. |
| DAO-MDE-02-03 | User Account DAO | User account data persistence and management operations. |

### MDE-03: Idle Resource Data Management
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-03-01 | Idle Resource Data Access Object | Primary DAO for idle resource record CRUD operations and queries. |
| DAO-MDE-03-02 | Idle Resource Search DAO | Optimized search operations with full-text search and indexing. |
| DAO-MDE-03-03 | Idle Resource Statistics DAO | Aggregated data retrieval and statistical query operations. |
| DAO-MDE-03-04 | Audit Trail DAO | Audit trail data persistence and historical query operations. |
| DAO-MDE-03-05 | User Preferences DAO | User-specific configuration and preference data operations. |
| DAO-MDE-03-06 | Department Access DAO | Department-based data filtering and access control queries. |
| DAO-MDE-03-07 | Batch Operations DAO | Optimized bulk database operations with transaction management. |
| DAO-MDE-03-08 | Import/Export DAO | Database operations for import/export and data transformation. |
| DAO-MDE-03-09 | Reference Data DAO | Lookup and reference data retrieval operations. |
| DAO-MDE-03-10 | Performance Monitoring DAO | Database performance monitoring and optimization operations. |

### MDE-04: CV Processing and File Management
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-04-01 | CV File Metadata DAO | CV file metadata and relationship data operations. |
| DAO-MDE-04-02 | AI Processing Status DAO | AI processing status and result data operations. |
| DAO-MDE-04-03 | Skill Data DAO | Extracted skill data persistence and retrieval operations. |

### MDE-05: Master Data Management
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-05-01 | Master Data DAO | Enumerated values and reference data operations. |
| DAO-MDE-05-02 | Organizational Chart DAO | Department hierarchy and organizational structure data operations. |

### MDE-06: Reporting and Analytics
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-06-01 | Report Data DAO | Report generation data queries and aggregation operations. |
| DAO-MDE-06-02 | Analytics DAO | Advanced analytics and trend analysis data operations. |
| DAO-MDE-06-03 | Dashboard Metrics DAO | Real-time metrics and KPI data retrieval operations. |

### MDE-07: System Automation and Configuration
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-07-01 | System Configuration DAO | System configuration and parameter data operations. |
| DAO-MDE-07-02 | Baseline Data DAO | Baseline snapshot data persistence and retrieval operations. |
| DAO-MDE-07-03 | Process Monitoring DAO | Background process status and monitoring data operations. |

### MDE-08: Audit Trail and Logging
| ID | Name | Description |
|----|------|-------------|
| DAO-MDE-08-01 | Audit Log DAO | Audit trail and logging data persistence operations. |
| DAO-MDE-08-02 | User Activity DAO | User activity and session tracking data operations. |

---

## Component Summary

| Component Type | Total Count | Distribution |
|----------------|-------------|--------------|
| **Modules** | 8 | Core system architecture |
| **Screens** | 14 | User interface components |
| **APIs** | 49 | REST endpoint services |
| **Services** | 35 | Business logic layer |
| **DAOs** | 25 | Data access layer |
| **Grand Total** | **131** | Complete system components |

## Architectural Overview

The Idle Resource Management System follows a layered architecture pattern:

1. **Presentation Layer**: 14 Screens providing user interface
2. **API Layer**: 49 REST endpoints for client-server communication
3. **Business Logic Layer**: 35 Services implementing core business rules
4. **Data Access Layer**: 25 DAOs managing database operations
5. **Data Layer**: Database and file storage systems

This comprehensive component structure ensures complete coverage of all functional requirements with proper separation of concerns, scalability, and maintainability.

---

**Document Status**: Complete  
**Component Analysis**: All modules analyzed and documented  
**Architecture Verification**: Layered architecture confirmed  
**Export Location**: output/01-complete-component-list.md
