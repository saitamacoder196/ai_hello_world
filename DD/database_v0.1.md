# Database Design Document

**Document ID**: database_v0.1  
**Document Name**: Database Design Document for Idle Resource Data Management System

## Cover

**Document ID**: database_v0.1  
**Document Name**: Database Design Document for Idle Resource Data Management System  

## History

| No | Date       | Version | Account | Action     | Impacted Sections                  | Description                           |
|----|------------|---------|---------|------------|-----------------------------------|---------------------------------------|
| 1  | 2024-DEC-26| v0.1    | System  | Initialize | Whole Document                    | Initial creation of database design   |

## Tables

| No | ID                          | Name                           | Description                                                    |
|----|-----------------------------|---------------------------------|----------------------------------------------------------------|
| 1  | idle_resources              | Idle Resources                 | Core table storing idle resource information and availability   |
| 2  | employees                   | Employees                      | Employee master data for resource management                   |
| 3  | departments                 | Departments                    | Department master data and hierarchy                           |
| 4  | user_departments            | User Department Permissions    | User access permissions per department                         |
| 5  | import_sessions            | Import Sessions                | Tracks data import operations and status                       |
| 6  | import_staging             | Import Staging                 | Temporary storage for imported data validation                 |
| 7  | export_sessions            | Export Sessions                | Tracks data export operations and status                       |
| 8  | export_column_config       | Export Column Configuration    | Configuration for data export column mapping                  |
| 9  | export_templates           | Export Templates               | Predefined templates for data export                          |
| 10 | export_data_temp           | Export Data Temporary          | Temporary storage for export data preparation                  |
| 11 | import_field_mappings      | Import Field Mappings          | Field mapping configuration for data imports                   |
| 12 | business_validation_rules  | Business Validation Rules      | Business logic validation rules for data processing           |
| 13 | notifications              | Notifications                  | System notifications and alerts                                |
| 14 | notification_recipients    | Notification Recipients        | Recipients for specific notifications                          |
| 15 | notification_audit_log     | Notification Audit Log         | Audit trail for notification delivery                          |
| 16 | alerts                     | Alerts                         | System alerts and monitoring                                   |
| 17 | alert_rules                | Alert Rules                    | Configuration for alert generation rules                       |
| 18 | alert_rule_executions      | Alert Rule Executions          | Execution history of alert rules                               |
| 19 | alert_escalations          | Alert Escalations              | Alert escalation configuration and history                     |
| 20 | alert_statistics           | Alert Statistics               | Statistical data for alert performance                         |
| 21 | notification_subscriptions | Notification Subscriptions     | User subscription preferences for notifications                |
| 22 | user_notification_settings | User Notification Settings     | Global notification preferences per user                       |
| 23 | monitoring_alerts          | Monitoring Alerts              | Real-time monitoring alerts                                    |
| 24 | automated_actions          | Automated Actions              | Automated response actions for alerts                          |
| 25 | external_integrations      | External Integrations          | Configuration for external system integrations                |
| 26 | sync_jobs                  | Synchronization Jobs           | Background synchronization job tracking                        |
| 27 | sync_batches               | Synchronization Batches        | Batch processing for sync operations                           |
| 28 | api_operations             | API Operations                 | API operation tracking and logging                             |
| 29 | api_statistics             | API Statistics                 | Performance statistics for API endpoints                       |
| 30 | webhooks                   | Webhooks                       | Webhook configuration and management                           |
| 31 | webhook_statistics         | Webhook Statistics             | Performance statistics for webhooks                            |
| 32 | system_connections         | System Connections             | System connectivity configuration and monitoring               |
| 33 | connection_health          | Connection Health              | Health monitoring data for system connections                  |
| 34 | system_configurations      | System Configurations          | System-wide configuration settings                             |
| 35 | configuration_audit        | Configuration Audit            | Audit trail for configuration changes                          |
| 36 | user_preferences           | User Preferences               | Individual user preference settings                            |
| 37 | user_preference_cache      | User Preference Cache          | Cached user preferences for performance                        |
| 38 | preference_validations     | Preference Validations         | Validation rules for user preferences                          |
| 39 | feature_toggles            | Feature Toggles                | Feature flag and rollout management                            |
| 40 | feature_toggle_audit       | Feature Toggle Audit           | Audit trail for feature toggle changes                        |
| 41 | feature_toggle_cache       | Feature Toggle Cache           | Cached feature toggle states                                   |
| 42 | environment_settings       | Environment Settings           | Environment-specific configuration settings                    |
| 43 | environment_hierarchy      | Environment Hierarchy          | Environment inheritance hierarchy                              |
| 44 | environment_constraints    | Environment Constraints        | Validation constraints for environment settings                |
| 45 | environment_config_cache   | Environment Config Cache       | Cached environment configurations                              |
| 46 | configuration_validations  | Configuration Validations      | Configuration validation processes                             |
| 47 | validation_issues          | Validation Issues              | Issues found during configuration validation                   |
| 48 | validation_rules           | Validation Rules               | Rules for configuration validation                             |
| 49 | validation_schedule        | Validation Schedule            | Scheduled validation operations                                |
| 50 | performance_metrics        | Performance Metrics            | System performance monitoring data                             |
| 51 | metric_thresholds          | Metric Thresholds              | Alert thresholds for performance metrics                       |
| 52 | performance_alerts         | Performance Alerts             | Alerts generated from performance monitoring                   |
| 53 | performance_summary        | Performance Summary            | Aggregated performance statistics                              |
| 54 | system_monitors            | System Monitors                | System monitoring configuration                                |
| 55 | monitoring_checks          | Monitoring Checks              | Individual monitoring check results                            |
| 56 | health_checks              | Health Checks                  | System health check operations                                 |
| 57 | health_check_details       | Health Check Details           | Detailed results from health checks                            |
| 58 | health_check_stats         | Health Check Statistics        | Statistical data for health checks                             |
| 59 | health_check_schedule      | Health Check Schedule          | Scheduled health check operations                              |
| 60 | query_optimization_analysis| Query Optimization Analysis    | Database query optimization analysis                           |
| 61 | query_analysis_results     | Query Analysis Results         | Results from query optimization analysis                       |
| 62 | optimization_schedule      | Optimization Schedule          | Scheduled optimization operations                              |
| 63 | diagnostic_sessions        | Diagnostic Sessions            | System diagnostic session tracking                             |
| 64 | diagnostic_procedures      | Diagnostic Procedures          | Individual diagnostic procedures                               |
| 65 | diagnostic_results         | Diagnostic Results             | Results from diagnostic procedures                             |
| 66 | diagnostic_findings        | Diagnostic Findings            | Issues found during diagnostics                                |
| 67 | diagnostic_recommendations | Diagnostic Recommendations     | Recommendations from diagnostic analysis                       |
| 68 | diagnostic_logs            | Diagnostic Logs                | Log data collected during diagnostics                          |
| 69 | default_procedures         | Default Procedures             | Default diagnostic procedures configuration                    |

## Columns & Constraints

### idle_resources
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | resource_id       | Resource ID         | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for idle resource            |
| 2  | employee_id       | Employee ID         | VARCHAR        | 36     | No          | No       | -              | Yes         | employees(employee_id) | Reference to employee record                   |
| 3  | resource_type     | Resource Type       | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of resource (developer, tester, etc.)    |
| 4  | department_id     | Department ID       | VARCHAR        | 36     | No          | No       | -              | Yes         | departments(department_id) | Reference to department                        |
| 5  | status            | Status              | VARCHAR        | 20     | No          | No       | 'available'    | No          | -                 | Current availability status                    |
| 6  | availability_start| Availability Start  | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Start date of availability                     |
| 7  | availability_end  | Availability End    | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | End date of availability                       |
| 8  | skills            | Skills              | JSONB          | -      | No          | Yes      | '[]'           | No          | -                 | JSON array of skills and competencies          |
| 9  | experience_years  | Experience Years    | INTEGER        | -      | No          | Yes      | 0              | No          | -                 | Years of experience                            |
| 10 | hourly_rate       | Hourly Rate         | DECIMAL        | 10,2   | No          | Yes      | -              | No          | -                 | Hourly billing rate                            |
| 11 | created_by        | Created By          | VARCHAR        | 36     | No          | No       | -              | No          | -                 | User who created the record                    |
| 12 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 13 | updated_by        | Updated By          | VARCHAR        | 36     | No          | Yes      | -              | No          | -                 | User who last updated the record               |
| 14 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |
| 15 | version           | Version             | INTEGER        | -      | No          | No       | 1              | No          | -                 | Record version for optimistic locking          |

### employees
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | employee_id       | Employee ID         | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for employee                 |
| 2  | employee_code     | Employee Code       | VARCHAR        | 20     | No          | No       | -              | No          | -                 | Human-readable employee code                   |
| 3  | first_name        | First Name          | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Employee first name                            |
| 4  | last_name         | Last Name           | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Employee last name                             |
| 5  | email             | Email               | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Employee email address                         |
| 6  | department_id     | Department ID       | VARCHAR        | 36     | No          | No       | -              | Yes         | departments(department_id) | Reference to department                        |
| 7  | job_title         | Job Title           | VARCHAR        | 100    | No          | Yes      | -              | No          | -                 | Employee job title                             |
| 8  | hire_date         | Hire Date           | DATE           | -      | No          | Yes      | -              | No          | -                 | Employee hire date                             |
| 9  | status            | Status              | VARCHAR        | 20     | No          | No       | 'active'       | No          | -                 | Employee status (active, inactive, etc.)       |
| 10 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 11 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### departments
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | department_id     | Department ID       | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for department               |
| 2  | department_code   | Department Code     | VARCHAR        | 20     | No          | No       | -              | No          | -                 | Human-readable department code                 |
| 3  | department_name   | Department Name     | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Department name                                |
| 4  | parent_department_id| Parent Department ID| VARCHAR        | 36     | No          | Yes      | -              | Yes         | departments(department_id) | Reference to parent department                 |
| 5  | manager_id        | Manager ID          | VARCHAR        | 36     | No          | Yes      | -              | Yes         | employees(employee_id) | Reference to department manager                |
| 6  | status            | Status              | VARCHAR        | 20     | No          | No       | 'active'       | No          | -                 | Department status                              |
| 7  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 8  | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### user_departments
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | id                | ID                  | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | user_id           | User ID             | VARCHAR        | 36     | No          | No       | -              | No          | -                 | Reference to user                              |
| 3  | department_id     | Department ID       | VARCHAR        | 36     | No          | No       | -              | Yes         | departments(department_id) | Reference to department                        |
| 4  | permission_level  | Permission Level    | VARCHAR        | 20     | No          | No       | 'read'         | No          | -                 | Access permission level                        |
| 5  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |

### import_sessions
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | session_id        | Session ID          | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for import session          |
| 2  | user_id           | User ID             | VARCHAR        | 36     | No          | No       | -              | No          | -                 | User who initiated the import                  |
| 3  | import_type       | Import Type         | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of import operation                       |
| 4  | status            | Status              | VARCHAR        | 20     | No          | No       | 'pending'      | No          | -                 | Current import status                          |
| 5  | total_records     | Total Records       | INTEGER        | -      | No          | Yes      | 0              | No          | -                 | Total number of records to import              |
| 6  | successful_records| Successful Records  | INTEGER        | -      | No          | Yes      | 0              | No          | -                 | Number of successfully imported records        |
| 7  | failed_records    | Failed Records      | INTEGER        | -      | No          | Yes      | 0              | No          | -                 | Number of failed records                       |
| 8  | error_summary     | Error Summary       | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Summary of import errors                       |
| 9  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Session creation timestamp                     |
| 10 | completed_at      | Completed At        | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Session completion timestamp                   |

### import_staging
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | id                | ID                  | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | session_id        | Session ID          | VARCHAR        | 36     | No          | No       | -              | Yes         | import_sessions(session_id) | Reference to import session                    |
| 3  | record_index      | Record Index        | INTEGER        | -      | No          | No       | -              | No          | -                 | Index of record in import batch                |
| 4  | raw_data          | Raw Data            | JSONB          | -      | No          | No       | -              | No          | -                 | Original imported data                         |
| 5  | transformed_data  | Transformed Data    | JSONB          | -      | No          | Yes      | -              | No          | -                 | Transformed/processed data                     |
| 6  | validation_status | Validation Status   | VARCHAR        | 20     | No          | No       | 'pending'      | No          | -                 | Data validation status                         |
| 7  | validation_errors | Validation Errors   | JSONB          | -      | No          | Yes      | '[]'           | No          | -                 | Validation error details                       |
| 8  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |

### export_sessions
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | session_id        | Session ID          | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for export session          |
| 2  | user_id           | User ID             | VARCHAR        | 36     | No          | No       | -              | No          | -                 | User who initiated the export                  |
| 3  | export_type       | Export Type         | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of export operation                       |
| 4  | export_format     | Export Format       | VARCHAR        | 20     | No          | No       | 'csv'          | No          | -                 | Export file format                             |
| 5  | criteria          | Criteria            | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Export filter criteria                         |
| 6  | status            | Status              | VARCHAR        | 20     | No          | No       | 'pending'      | No          | -                 | Current export status                          |
| 7  | total_records     | Total Records       | INTEGER        | -      | No          | Yes      | 0              | No          | -                 | Total number of records to export              |
| 8  | file_path         | File Path           | VARCHAR        | 500    | No          | Yes      | -              | No          | -                 | Path to generated export file                  |
| 9  | file_size         | File Size           | BIGINT         | -      | No          | Yes      | 0              | No          | -                 | Size of generated file in bytes                |
| 10 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Session creation timestamp                     |
| 11 | completed_at      | Completed At        | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Session completion timestamp                   |

### export_column_config
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | id                | ID                  | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | table_name        | Table Name          | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Source table name                              |
| 3  | column_name       | Column Name         | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Source column name                             |
| 4  | display_name      | Display Name        | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Display name for export                        |
| 5  | data_type         | Data Type           | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Column data type                               |
| 6  | export_format     | Export Format       | VARCHAR        | 100    | No          | Yes      | -              | No          | -                 | Format specification for export                |
| 7  | display_order     | Display Order       | INTEGER        | -      | No          | No       | 0              | No          | -                 | Column display order in export                 |
| 8  | is_active         | Is Active           | BOOLEAN        | -      | No          | No       | true           | No          | -                 | Whether column is included in exports          |

### export_templates
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | template_id       | Template ID         | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for export template         |
| 2  | template_name     | Template Name       | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Template name                                  |
| 3  | template_type     | Template Type       | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of export template                        |
| 4  | column_config     | Column Config       | JSONB          | -      | No          | No       | '{}'           | No          | -                 | Column configuration settings                  |
| 5  | format_config     | Format Config       | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Format configuration settings                  |
| 6  | filter_config     | Filter Config       | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Default filter configuration                   |
| 7  | is_public         | Is Public           | BOOLEAN        | -      | No          | No       | false          | No          | -                 | Whether template is publicly available         |
| 8  | status            | Status              | VARCHAR        | 20     | No          | No       | 'active'       | No          | -                 | Template status                                |
| 9  | created_by        | Created By          | VARCHAR        | 36     | No          | No       | -              | No          | -                 | User who created the template                  |
| 10 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Template creation timestamp                    |
| 11 | updated_by        | Updated By          | VARCHAR        | 36     | No          | Yes      | -              | No          | -                 | User who last updated the template             |
| 12 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |
| 13 | deleted_by        | Deleted By          | VARCHAR        | 36     | No          | Yes      | -              | No          | -                 | User who deleted the template                  |
| 14 | deleted_at        | Deleted At          | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Template deletion timestamp                    |

### performance_metrics
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | metric_id         | Metric ID           | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | metric_name       | Metric Name         | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Name of the performance metric                 |
| 3  | metric_value      | Metric Value        | DECIMAL        | 15,6   | No          | No       | -              | No          | -                 | Numeric value of the metric                    |
| 4  | metric_unit       | Metric Unit         | VARCHAR        | 20     | No          | Yes      | -              | No          | -                 | Unit of measurement                            |
| 5  | component         | Component           | VARCHAR        | 100    | No          | No       | -              | No          | -                 | System component being measured                |
| 6  | trend_direction   | Trend Direction     | VARCHAR        | 10     | No          | Yes      | 'stable'       | No          | -                 | Trend direction (up, down, stable)             |
| 7  | alert_level       | Alert Level         | VARCHAR        | 20     | No          | Yes      | 'normal'       | No          | -                 | Current alert level                            |
| 8  | recorded_at       | Recorded At         | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | When the metric was recorded                   |
| 9  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |

### system_monitors
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | monitor_id        | Monitor ID          | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | monitor_type      | Monitor Type        | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of monitoring (CPU, memory, disk, etc.)  |
| 3  | resource_id       | Resource ID         | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Identifier of monitored resource               |
| 4  | threshold_config  | Threshold Config    | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Alert threshold configuration                  |
| 5  | alert_contacts    | Alert Contacts      | JSONB          | -      | No          | Yes      | '[]'           | No          | -                 | Contact list for alerts                        |
| 6  | monitoring_interval| Monitoring Interval| INTEGER        | -      | No          | No       | 60             | No          | -                 | Monitoring check interval in seconds           |
| 7  | status            | Status              | VARCHAR        | 20     | No          | No       | 'inactive'     | No          | -                 | Current monitoring status                      |
| 8  | health_score      | Health Score        | DECIMAL        | 5,2    | No          | Yes      | 100.0          | No          | -                 | Overall health score (0-100)                  |
| 9  | last_check        | Last Check          | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Timestamp of last monitoring check             |
| 10 | active_alerts     | Active Alerts       | INTEGER        | -      | No          | No       | 0              | No          | -                 | Number of active alerts                        |
| 11 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 12 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |
| 13 | last_updated      | Last Updated        | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Last monitoring update timestamp               |

### monitoring_checks
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | check_id          | Check ID            | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | monitor_id        | Monitor ID          | INTEGER        | -      | No          | No       | -              | Yes         | system_monitors(monitor_id) | Reference to system monitor                    |
| 3  | monitor_type      | Monitor Type        | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of monitoring check                       |
| 4  | resource_id       | Resource ID         | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Identifier of monitored resource               |
| 5  | check_timestamp   | Check Timestamp     | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | When the check was performed                   |
| 6  | status            | Status              | VARCHAR        | 20     | No          | No       | -              | No          | -                 | Check result status                            |
| 7  | response_time     | Response Time       | DECIMAL        | 10,3   | No          | Yes      | -              | No          | -                 | Response time in milliseconds                  |
| 8  | resource_usage    | Resource Usage      | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Resource usage metrics                         |
| 9  | errors            | Errors              | JSONB          | -      | No          | Yes      | '[]'           | No          | -                 | Error details if any                           |
| 10 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |

### notifications
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | notification_id   | Notification ID     | VARCHAR        | 36     | Yes         | No       | UUID()         | No          | -                 | Unique identifier for notification             |
| 2  | notification_type | Notification Type   | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of notification                           |
| 3  | title             | Title               | VARCHAR        | 200    | No          | No       | -              | No          | -                 | Notification title                             |
| 4  | message           | Message             | TEXT           | -      | No          | No       | -              | No          | -                 | Notification message content                   |
| 5  | priority          | Priority            | VARCHAR        | 20     | No          | No       | 'medium'       | No          | -                 | Notification priority level                    |
| 6  | status            | Status              | VARCHAR        | 20     | No          | No       | 'pending'      | No          | -                 | Current notification status                    |
| 7  | delivery_method   | Delivery Method     | VARCHAR        | 50     | No          | No       | 'email'        | No          | -                 | Method for notification delivery               |
| 8  | metadata          | Metadata            | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Additional notification metadata               |
| 9  | created_by        | Created By          | VARCHAR        | 36     | No          | No       | -              | No          | -                 | User who created the notification              |
| 10 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Notification creation timestamp                |
| 11 | scheduled_at      | Scheduled At        | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | When notification should be sent               |
| 12 | sent_at           | Sent At             | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | When notification was actually sent            |

### external_integrations
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | integration_id    | Integration ID      | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | system_id         | System ID           | VARCHAR        | 100    | No          | No       | -              | No          | -                 | External system identifier                     |
| 3  | integration_type  | Integration Type    | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of integration                            |
| 4  | endpoint_url      | Endpoint URL        | VARCHAR        | 500    | No          | No       | -              | No          | -                 | Integration endpoint URL                       |
| 5  | auth_config       | Auth Config         | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Authentication configuration                   |
| 6  | mapping_config    | Mapping Config      | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Data mapping configuration                     |
| 7  | status            | Status              | VARCHAR        | 20     | No          | No       | 'inactive'     | No          | -                 | Integration status                             |
| 8  | last_sync         | Last Sync           | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | Last synchronization timestamp                 |
| 9  | error_count       | Error Count         | INTEGER        | -      | No          | No       | 0              | No          | -                 | Number of consecutive errors                   |
| 10 | config_version    | Config Version      | INTEGER        | -      | No          | No       | 1              | No          | -                 | Configuration version number                   |
| 11 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 12 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### system_configurations
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | config_id         | Config ID           | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | config_key        | Config Key          | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Configuration key identifier                   |
| 3  | config_value      | Config Value        | JSONB          | -      | No          | Yes      | -              | No          | -                 | Configuration value                            |
| 4  | config_type       | Config Type         | VARCHAR        | 50     | No          | No       | 'string'       | No          | -                 | Type of configuration value                    |
| 5  | description       | Description         | TEXT           | -      | No          | Yes      | -              | No          | -                 | Configuration description                      |
| 6  | is_encrypted      | Is Encrypted        | BOOLEAN        | -      | No          | No       | false          | No          | -                 | Whether value is encrypted                     |
| 7  | version           | Version             | INTEGER        | -      | No          | No       | 1              | No          | -                 | Configuration version                          |
| 8  | is_active         | Is Active           | BOOLEAN        | -      | No          | No       | true           | No          | -                 | Whether configuration is active                |
| 9  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 10 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### user_preferences
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | preference_id     | Preference ID       | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | user_id           | User ID             | VARCHAR        | 36     | No          | No       | -              | No          | -                 | Reference to user                              |
| 3  | preference_key    | Preference Key      | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Preference key identifier                      |
| 4  | preference_value  | Preference Value    | JSONB          | -      | No          | No       | -              | No          | -                 | Preference value                               |
| 5  | category          | Category            | VARCHAR        | 50     | No          | Yes      | 'general'      | No          | -                 | Preference category                            |
| 6  | is_private        | Is Private          | BOOLEAN        | -      | No          | No       | false          | No          | -                 | Whether preference is private                  |
| 7  | is_valid          | Is Valid            | BOOLEAN        | -      | No          | Yes      | true           | No          | -                 | Whether preference value is valid              |
| 8  | is_active         | Is Active           | BOOLEAN        | -      | No          | No       | true           | No          | -                 | Whether preference is active                   |
| 9  | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 10 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### feature_toggles
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | toggle_id         | Toggle ID           | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | feature_name      | Feature Name        | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Name of the feature toggle                     |
| 3  | is_enabled        | Is Enabled          | BOOLEAN        | -      | No          | No       | false          | No          | -                 | Whether feature is enabled                     |
| 4  | target_audience   | Target Audience     | JSONB          | -      | No          | Yes      | '[]'           | No          | -                 | Target audience for feature rollout            |
| 5  | rollout_percentage| Rollout Percentage  | INTEGER        | -      | No          | No       | 100            | No          | -                 | Percentage of users to receive feature         |
| 6  | environment       | Environment         | VARCHAR        | 50     | No          | No       | 'production'   | No          | -                 | Target environment                             |
| 7  | effective_date    | Effective Date      | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | When feature becomes effective                 |
| 8  | rollout_status    | Rollout Status      | VARCHAR        | 20     | No          | No       | 'planned'      | No          | -                 | Current rollout status                         |
| 9  | is_active         | Is Active           | BOOLEAN        | -      | No          | No       | true           | No          | -                 | Whether toggle is active                       |
| 10 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 11 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### environment_settings
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | setting_id        | Setting ID          | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | environment       | Environment         | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Environment name                               |
| 3  | setting_key       | Setting Key         | VARCHAR        | 100    | No          | No       | -              | No          | -                 | Setting key identifier                         |
| 4  | setting_value     | Setting Value       | JSONB          | -      | No          | Yes      | -              | No          | -                 | Setting value (cleartext)                      |
| 5  | is_sensitive      | Is Sensitive        | BOOLEAN        | -      | No          | No       | false          | No          | -                 | Whether setting contains sensitive data        |
| 6  | inheritance_level | Inheritance Level   | VARCHAR        | 20     | No          | No       | 'env'          | No          | -                 | Setting inheritance level                      |
| 7  | encrypted_value   | Encrypted Value     | BYTEA          | -      | No          | Yes      | -              | No          | -                 | Encrypted setting value                        |
| 8  | is_valid          | Is Valid            | BOOLEAN        | -      | No          | Yes      | true           | No          | -                 | Whether setting value is valid                 |
| 9  | validation_result | Validation Result   | VARCHAR        | 20     | No          | Yes      | 'passed'       | No          | -                 | Result of last validation                      |
| 10 | is_active         | Is Active           | BOOLEAN        | -      | No          | No       | true           | No          | -                 | Whether setting is active                      |
| 11 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
| 12 | updated_at        | Updated At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Last update timestamp                          |

### health_checks
| No | ID                | Name                | Data Type      | Length | Primary Key | Nullable | Default Value  | Foreign Key | References        | Description                                    |
|----|-------------------|---------------------|----------------|---------|-------------|----------|----------------|-------------|-------------------|------------------------------------------------|
| 1  | check_id          | Check ID            | SERIAL         | -      | Yes         | No       | -              | No          | -                 | Auto-increment primary key                     |
| 2  | check_type        | Check Type          | VARCHAR        | 50     | No          | No       | -              | No          | -                 | Type of health check                           |
| 3  | target_endpoint   | Target Endpoint     | VARCHAR        | 500    | No          | No       | -              | No          | -                 | Endpoint or resource being checked             |
| 4  | check_parameters  | Check Parameters    | JSONB          | -      | No          | Yes      | '{}'           | No          | -                 | Parameters for the health check                |
| 5  | timeout_seconds   | Timeout Seconds     | INTEGER        | -      | No          | No       | 30             | No          | -                 | Timeout for health check in seconds            |
| 6  | retry_count       | Retry Count         | INTEGER        | -      | No          | No       | 3              | No          | -                 | Number of retries on failure                   |
| 7  | status            | Status              | VARCHAR        | 20     | No          | No       | 'pending'      | No          | -                 | Current check status                           |
| 8  | response_time     | Response Time       | DECIMAL        | 10,3   | No          | Yes      | -              | No          | -                 | Response time in milliseconds                  |
| 9  | attempts_made     | Attempts Made       | INTEGER        | -      | No          | Yes      | 0              | No          | -                 | Number of attempts made                        |
| 10 | started_at        | Started At          | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | When check was started                         |
| 11 | completed_at      | Completed At        | TIMESTAMP      | -      | No          | Yes      | -              | No          | -                 | When check was completed                       |
| 12 | created_at        | Created At          | TIMESTAMP      | -      | No          | No       | NOW()          | No          | -                 | Record creation timestamp                      |
