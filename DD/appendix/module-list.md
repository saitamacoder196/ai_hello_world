# Module List - Idle Resource Management System

**Document Version**: v0.1  
**Generated Date**: 2025-07-25  
**Source**: Functional Breakdown v0.1, Basic Design v0.1  

## Project Modules

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

## Module Dependencies

### Core Dependencies
- **MDE-01** (Authentication) → Foundation for all other modules
- **MDE-02** (Authorization) → Required by all functional modules for access control
- **MDE-05** (Master Data) → Referenced by MDE-03, MDE-04, MDE-06 for dropdown data

### Functional Dependencies
- **MDE-03** (Idle Resource Data) → Core module used by MDE-04, MDE-06, MDE-07
- **MDE-04** (CV Processing) → Integrates with MDE-03 for skill data
- **MDE-06** (Reporting) → Uses data from MDE-03, MDE-04, MDE-05
- **MDE-07** (System Automation) → Processes data from MDE-03, generates baselines for MDE-06
- **MDE-08** (Audit Trail) → Cross-cutting concern for all modules

## Module Characteristics

### Primary Business Modules
- **MDE-03**: Idle Resource Data Management (Core business functionality)
- **MDE-06**: Reporting and Analytics (Decision support)

### Supporting Infrastructure Modules
- **MDE-01**: Authentication and Session Management
- **MDE-02**: Authorization and Role Management
- **MDE-05**: Master Data Management
- **MDE-08**: Audit Trail and Logging

### Enhancement Modules
- **MDE-04**: CV Processing and File Management (AI-powered features)
- **MDE-07**: System Automation and Configuration (Process automation)

## Technical Implementation Scope

### Frontend Components
Each module includes corresponding React-based user interface components with role-based rendering and responsive design.

### Backend Services
Each module implements Django REST Framework services with appropriate business logic, data validation, and API endpoints.

### Data Layer
Modules share common PostgreSQL database with module-specific tables and relationships, plus file storage for CV management.

---

**Document Status**: Complete  
**Total Modules**: 8  
**Next Review**: Module consolidation analysis  
**Export Location**: output/01-module-list.md
