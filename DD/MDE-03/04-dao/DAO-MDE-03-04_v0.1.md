# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-04  
**Document Name**: Audit Trail DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-04 |
| Document Name | Audit Trail DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Audit Trail DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-04-01 | Create Audit Entry | Create new audit trail entry for resource operations |
| 2 | DAO-MDE-03-04-02 | Query Audit History | Query audit history with filtering and search capabilities |
| 3 | DAO-MDE-03-04-03 | Generate Audit Report | Generate comprehensive audit reports for compliance |
| 4 | DAO-MDE-03-04-04 | Archive Old Audit Records | Archive old audit records for long-term storage |
| 5 | DAO-MDE-03-04-05 | Audit Data Integrity Check | Check and verify audit data integrity |

## Logic & Flow

### DAO ID: DAO-MDE-03-04-01
### DAO Name: Create Audit Entry

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | auditOperation | String | Required | Type of operation being audited |
| 2 | resourceId | String | Required | Resource ID being audited |
| 3 | operationDetails | Object | Required | Detailed information about the operation |
| 4 | userContext | Object | Required | User context for audit trail |
| 5 | additionalMetadata | Object | Optional | Additional metadata for audit |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | auditEntryId | String | Generated audit entry ID |
| 2 | auditRecord | Object | Complete audit record created |
| 3 | operationStatus | Object | Audit creation operation status |

### Steps:

1. **Step 1: Validate Audit Entry Request**
   - **Description**: Validate audit entry creation request and parameters
   - **Data Validation**: 
     - Check audit operation type and resource ID validity
     - Validate operation details and user context
     - Ensure all required audit fields are present
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Generate Audit Entry ID**
   - **Description**: Generate unique audit entry ID for new record
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT NEXTVAL('audit_trail_id_seq') AS next_audit_id
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | next_audit_id | Generated audit entry ID |
     - **Callback**: Use generated ID for audit record creation

3. **Step 3: Insert Audit Trail Record**
   - **Description**: Insert new audit trail record into database
   - **Data Validation**: None (already validated)
   - **SQL Call**: 
     - **SQL**: INSERT INTO audit_trail (audit_id, resource_id, operation_type, operation_details, previous_values, new_values, user_id, user_role, department_id, ip_address, user_agent, session_id, operation_timestamp, compliance_flags, additional_metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?, ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | audit_id | Generated ID | Unique audit identifier |
       | resource_id | ARGUMENT.resourceId | Resource being audited |
       | operation_type | ARGUMENT.auditOperation | Type of operation |
       | operation_details | ARGUMENT.operationDetails | Detailed operation information |
       | previous_values | ARGUMENT.operationDetails.previousValues | Previous data values |
       | new_values | ARGUMENT.operationDetails.newValues | New data values |
       | user_id | ARGUMENT.userContext.userId | User performing operation |
       | user_role | ARGUMENT.userContext.role | User role |
       | department_id | ARGUMENT.userContext.departmentId | User department |
       | ip_address | ARGUMENT.userContext.ipAddress | User IP address |
       | user_agent | ARGUMENT.userContext.userAgent | User agent string |
       | session_id | ARGUMENT.userContext.sessionId | User session ID |
       | compliance_flags | Compliance requirements | Compliance flags |
       | additional_metadata | ARGUMENT.additionalMetadata | Additional metadata |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_rows | Number of affected rows |
     - **Callback**: Confirm successful audit record creation

4. **Step 4: Update Audit Statistics**
   - **Description**: Update audit statistics for monitoring and reporting
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO audit_statistics (operation_date, operation_type, department_id, operation_count) VALUES (CURRENT_DATE, ?, ?, 1) ON CONFLICT (operation_date, operation_type, department_id) DO UPDATE SET operation_count = audit_statistics.operation_count + 1
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | operation_type | ARGUMENT.auditOperation | Type of operation |
       | department_id | ARGUMENT.userContext.departmentId | User department |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | stats_updated | Statistics update status |
     - **Callback**: Update statistics tracking

5. **Step 5: Retrieve Complete Audit Record**
   - **Description**: Retrieve the complete created audit record for response
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT * FROM audit_trail WHERE audit_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | audit_id | Generated ID | Audit ID to retrieve |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | complete_audit_record | Complete audit trail record |
     - **Callback**: Return complete audit record

6. **Final Step: Return Audit Creation Results**
   - Return successful audit creation results with audit ID and complete record

---

### DAO ID: DAO-MDE-03-04-02
### DAO Name: Query Audit History

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | queryFilters | Object | Required | Filters for audit history query |
| 2 | dateRange | Object | Optional | Date range for audit history |
| 3 | paginationInfo | Object | Required | Pagination parameters |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | auditHistory | Array | Filtered audit history records |
| 2 | totalRecords | Integer | Total number of matching audit records |
| 3 | auditSummary | Object | Summary statistics of queried audit data |

### Steps:

1. **Step 1: Validate Audit Query Request**
   - **Description**: Validate audit history query request and parameters
   - **Data Validation**: 
     - Check query filters format and validity
     - Validate date range and pagination parameters
     - Ensure user has audit query permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Build Dynamic Audit Query**
   - **Description**: Build dynamic SQL query based on filters and user access
   - **Data Validation**: None
   - **Callback**: Construct WHERE clause based on user role and department access

3. **Step 3: Get Total Audit Record Count**
   - **Description**: Get total count of matching audit records for pagination
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as total_count FROM audit_trail at WHERE (at.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin') [DYNAMIC_FILTER_CONDITIONS] [DATE_RANGE_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | filter_params | ARGUMENT.queryFilters | Dynamic filter parameters |
       | date_params | ARGUMENT.dateRange | Date range parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | total_count | Total matching audit records |
     - **Callback**: Use count for pagination calculation

4. **Step 4: Retrieve Audit History Records**
   - **Description**: Retrieve paginated audit history records
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT at.*, u.username, u.first_name, u.last_name, d.department_name, ir.employee_id, CONCAT(e.first_name, ' ', e.last_name) as resource_employee_name FROM audit_trail at LEFT JOIN users u ON at.user_id = u.user_id LEFT JOIN departments d ON at.department_id = d.department_id LEFT JOIN idle_resources ir ON at.resource_id = ir.resource_id LEFT JOIN employees e ON ir.employee_id = e.employee_id WHERE (at.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin') [DYNAMIC_FILTER_CONDITIONS] [DATE_RANGE_CONDITIONS] ORDER BY at.operation_timestamp DESC LIMIT ? OFFSET ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | filter_params | ARGUMENT.queryFilters | Dynamic filter parameters |
       | date_params | ARGUMENT.dateRange | Date range parameters |
       | limit | ARGUMENT.paginationInfo.limit | Page size limit |
       | offset | ARGUMENT.paginationInfo.offset | Page offset |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | audit_history | Paginated audit history records |
     - **Callback**: Return formatted audit history

5. **Step 5: Generate Audit Summary Statistics**
   - **Description**: Generate summary statistics for the queried audit data
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT operation_type, COUNT(*) as operation_count, COUNT(DISTINCT user_id) as unique_users, COUNT(DISTINCT resource_id) as unique_resources, MIN(operation_timestamp) as earliest_operation, MAX(operation_timestamp) as latest_operation FROM audit_trail WHERE (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin') [DYNAMIC_FILTER_CONDITIONS] [DATE_RANGE_CONDITIONS] GROUP BY operation_type ORDER BY operation_count DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | filter_params | ARGUMENT.queryFilters | Dynamic filter parameters |
       | date_params | ARGUMENT.dateRange | Date range parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | audit_summary | Audit summary statistics |
     - **Callback**: Include summary in response

6. **Final Step: Return Audit History Results**
   - Return complete audit history results with pagination, totals, and summary statistics

---

### DAO ID: DAO-MDE-03-04-03
### DAO Name: Generate Audit Report

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | reportType | String | Required | Type of audit report (compliance/security/activity) |
| 2 | reportPeriod | Object | Required | Time period for audit report |
| 3 | reportScope | Object | Optional | Scope limitations for report |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | auditReport | Object | Comprehensive audit report data |
| 2 | reportMetadata | Object | Report metadata and generation info |
| 3 | complianceAnalysis | Object | Compliance analysis results |

### Steps:

1. **Step 1: Validate Audit Report Request**
   - **Description**: Validate audit report generation request and parameters
   - **Data Validation**: 
     - Check report type and period validity
     - Validate report scope and user permissions
     - Ensure user has audit report generation rights
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Generate Compliance Audit Report**
   - **Description**: Generate compliance-focused audit report data
   - **Data Validation**: Check if report type is compliance
   - **SQL Call**: 
     - **SQL**: SELECT 
       DATE_TRUNC('day', operation_timestamp) as audit_date,
       operation_type,
       COUNT(*) as operation_count,
       COUNT(DISTINCT user_id) as unique_users,
       COUNT(DISTINCT resource_id) as unique_resources,
       SUM(CASE WHEN compliance_flags ? 'gdpr_relevant' THEN 1 ELSE 0 END) as gdpr_operations,
       SUM(CASE WHEN compliance_flags ? 'sox_relevant' THEN 1 ELSE 0 END) as sox_operations,
       SUM(CASE WHEN compliance_flags ? 'iso_relevant' THEN 1 ELSE 0 END) as iso_operations
       FROM audit_trail 
       WHERE operation_timestamp BETWEEN ? AND ?
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       GROUP BY DATE_TRUNC('day', operation_timestamp), operation_type
       ORDER BY audit_date DESC, operation_count DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | period_start | ARGUMENT.reportPeriod.start | Report period start |
       | period_end | ARGUMENT.reportPeriod.end | Report period end |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | compliance_data | Compliance audit report data |
     - **Callback**: Include in compliance report

3. **Step 3: Generate Security Audit Report**
   - **Description**: Generate security-focused audit report data
   - **Data Validation**: Check if report type is security
   - **SQL Call**: 
     - **SQL**: SELECT 
       user_id,
       user_role,
       ip_address,
       COUNT(*) as access_count,
       COUNT(DISTINCT DATE(operation_timestamp)) as active_days,
       MIN(operation_timestamp) as first_access,
       MAX(operation_timestamp) as last_access,
       COUNT(CASE WHEN operation_type IN ('create', 'update', 'delete') THEN 1 END) as modification_count,
       COUNT(CASE WHEN operation_type = 'read' THEN 1 END) as read_count,
       ARRAY_AGG(DISTINCT operation_type) as operation_types
       FROM audit_trail 
       WHERE operation_timestamp BETWEEN ? AND ?
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       GROUP BY user_id, user_role, ip_address
       ORDER BY access_count DESC, modification_count DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | period_start | ARGUMENT.reportPeriod.start | Report period start |
       | period_end | ARGUMENT.reportPeriod.end | Report period end |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | security_data | Security audit report data |
     - **Callback**: Include in security report

4. **Step 4: Generate Activity Audit Report**
   - **Description**: Generate activity-focused audit report data
   - **Data Validation**: Check if report type is activity
   - **SQL Call**: 
     - **SQL**: SELECT 
       resource_id,
       COUNT(*) as total_operations,
       COUNT(CASE WHEN operation_type = 'create' THEN 1 END) as create_count,
       COUNT(CASE WHEN operation_type = 'read' THEN 1 END) as read_count,
       COUNT(CASE WHEN operation_type = 'update' THEN 1 END) as update_count,
       COUNT(CASE WHEN operation_type = 'delete' THEN 1 END) as delete_count,
       COUNT(DISTINCT user_id) as unique_users,
       MIN(operation_timestamp) as first_operation,
       MAX(operation_timestamp) as last_operation,
       EXTRACT(DAYS FROM MAX(operation_timestamp) - MIN(operation_timestamp)) as activity_span_days
       FROM audit_trail 
       WHERE operation_timestamp BETWEEN ? AND ?
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       GROUP BY resource_id
       ORDER BY total_operations DESC, activity_span_days DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | period_start | ARGUMENT.reportPeriod.start | Report period start |
       | period_end | ARGUMENT.reportPeriod.end | Report period end |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | activity_data | Activity audit report data |
     - **Callback**: Include in activity report

5. **Step 5: Analyze Compliance Violations**
   - **Description**: Analyze potential compliance violations and anomalies
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       'unauthorized_access' as violation_type,
       COUNT(*) as violation_count,
       ARRAY_AGG(DISTINCT user_id) as involved_users,
       ARRAY_AGG(DISTINCT resource_id) as affected_resources
       FROM audit_trail 
       WHERE operation_timestamp BETWEEN ? AND ?
       AND user_role NOT IN ('admin', 'ra_all', 'ra_dept')
       AND operation_type IN ('update', 'delete')
       UNION ALL
       SELECT 
       'after_hours_access' as violation_type,
       COUNT(*) as violation_count,
       ARRAY_AGG(DISTINCT user_id) as involved_users,
       ARRAY_AGG(DISTINCT resource_id) as affected_resources
       FROM audit_trail 
       WHERE operation_timestamp BETWEEN ? AND ?
       AND EXTRACT(HOUR FROM operation_timestamp) NOT BETWEEN 8 AND 18
       AND EXTRACT(DOW FROM operation_timestamp) BETWEEN 1 AND 5
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | period_start_1 | ARGUMENT.reportPeriod.start | Period start for unauthorized access |
       | period_end_1 | ARGUMENT.reportPeriod.end | Period end for unauthorized access |
       | period_start_2 | ARGUMENT.reportPeriod.start | Period start for after hours |
       | period_end_2 | ARGUMENT.reportPeriod.end | Period end for after hours |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | compliance_violations | Compliance violation analysis |
     - **Callback**: Include violations in compliance analysis

6. **Step 6: Generate Report Metadata**
   - **Description**: Generate metadata and summary information for the report
   - **Data Validation**: None
   - **Callback**: Create report metadata including generation time, scope, and summary statistics

7. **Final Step: Return Comprehensive Audit Report**
   - Return comprehensive audit report with data, metadata, and compliance analysis

---

### DAO ID: DAO-MDE-03-04-04
### DAO Name: Archive Old Audit Records

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | archiveCriteria | Object | Required | Criteria for selecting records to archive |
| 2 | archiveMode | String | Optional, Default: 'move' | Archive mode (move/copy) |
| 3 | retentionPeriod | Integer | Required | Retention period in days |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | archiveResults | Object | Archive operation results |
| 2 | archivedCount | Integer | Number of records archived |
| 3 | archiveLocation | String | Location of archived data |

### Steps:

1. **Step 1: Validate Archive Request**
   - **Description**: Validate audit record archive request and parameters
   - **Data Validation**: 
     - Check archive criteria and retention period validity
     - Validate archive mode and user permissions
     - Ensure user has audit archive permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Identify Records for Archiving**
   - **Description**: Identify audit records that meet archiving criteria
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT audit_id, resource_id, operation_timestamp, operation_type, user_id, department_id FROM audit_trail WHERE operation_timestamp < (CURRENT_DATE - INTERVAL ? || ' days') AND archive_status IS NULL ORDER BY operation_timestamp ASC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | retention_days | ARGUMENT.retentionPeriod | Retention period in days |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | archive_candidates | Records eligible for archiving |
     - **Callback**: Proceed with archiving if records found

3. **Step 3: Begin Archive Transaction**
   - **Description**: Begin database transaction for archive operations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: BEGIN TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_id | Transaction identifier |
     - **Callback**: Proceed with archiving operations

4. **Step 4: Copy Records to Archive Table**
   - **Description**: Copy audit records to archive table
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO audit_trail_archive SELECT *, NOW() as archived_at, ? as archived_by FROM audit_trail WHERE operation_timestamp < (CURRENT_DATE - INTERVAL ? || ' days') AND archive_status IS NULL
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | archived_by | ARGUMENT.userContext.userId | User performing archive |
       | retention_days | ARGUMENT.retentionPeriod | Retention period in days |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | archived_count | Number of records archived |
     - **Callback**: Continue with cleanup if move mode

5. **Step 5: Remove Archived Records (if move mode)**
   - **Description**: Remove archived records from main table if move mode
   - **Data Validation**: Check if archive mode is move
   - **SQL Call**: 
     - **SQL**: DELETE FROM audit_trail WHERE operation_timestamp < (CURRENT_DATE - INTERVAL ? || ' days') AND archive_status IS NULL AND audit_id IN (SELECT audit_id FROM audit_trail_archive WHERE archived_at >= ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | retention_days | ARGUMENT.retentionPeriod | Retention period in days |
       | archive_start_time | Archive operation start time | Archive start timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | deleted_count | Number of records removed |
     - **Callback**: Confirm cleanup completion

6. **Step 6: Update Archive Statistics**
   - **Description**: Update archive statistics for monitoring
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO archive_statistics (archive_date, archive_type, records_archived, retention_period, archived_by) VALUES (CURRENT_DATE, 'audit_trail', ?, ?, ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | records_count | Archived record count | Number of archived records |
       | retention_period | ARGUMENT.retentionPeriod | Retention period used |
       | archived_by | ARGUMENT.userContext.userId | User performing archive |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | stats_updated | Statistics update status |
     - **Callback**: Update archive tracking

7. **Step 7: Commit Archive Transaction**
   - **Description**: Commit archive transaction
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: COMMIT TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_status | Transaction completion status |
     - **Callback**: Finalize archive operation

8. **Final Step: Return Archive Results**
   - Return archive operation results with archived count and location

---

### DAO ID: DAO-MDE-03-04-05
### DAO Name: Audit Data Integrity Check

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | integrityScope | Object | Required | Scope of integrity check (full/partial/targeted) |
| 2 | checkType | Array | Required | Types of integrity checks to perform |
| 3 | repairMode | Boolean | Optional, Default: false | Attempt to repair integrity issues |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | integrityResults | Object | Integrity check operation results |
| 2 | integrityIssues | Array | Identified integrity issues |
| 3 | repairResults | Object | Repair results if repair mode enabled |

### Steps:

1. **Step 1: Validate Integrity Check Request**
   - **Description**: Validate audit data integrity check request and parameters
   - **Data Validation**: 
     - Check integrity scope and check type validity
     - Validate repair mode and user permissions
     - Ensure user has integrity check permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Audit Record Completeness**
   - **Description**: Check for missing or incomplete audit records
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       'missing_audit_fields' as issue_type,
       audit_id,
       resource_id,
       operation_type,
       CASE 
         WHEN user_id IS NULL THEN 'missing_user_id'
         WHEN operation_details IS NULL THEN 'missing_operation_details'
         WHEN operation_timestamp IS NULL THEN 'missing_timestamp'
         ELSE 'unknown'
       END as specific_issue
       FROM audit_trail 
       WHERE user_id IS NULL 
       OR operation_details IS NULL 
       OR operation_timestamp IS NULL
       OR resource_id IS NULL
       ORDER BY operation_timestamp DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | completeness_issues | Completeness integrity issues |
     - **Callback**: Collect completeness issues

3. **Step 3: Check Audit Record Consistency**
   - **Description**: Check for consistency issues in audit records
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       'consistency_violation' as issue_type,
       at.audit_id,
       at.resource_id,
       at.operation_type,
       'referenced_resource_not_found' as specific_issue
       FROM audit_trail at 
       LEFT JOIN idle_resources ir ON at.resource_id = ir.resource_id 
       WHERE ir.resource_id IS NULL 
       AND at.operation_type != 'delete'
       UNION ALL
       SELECT 
       'consistency_violation' as issue_type,
       at.audit_id,
       at.resource_id,
       at.operation_type,
       'invalid_user_reference' as specific_issue
       FROM audit_trail at 
       LEFT JOIN users u ON at.user_id = u.user_id 
       WHERE u.user_id IS NULL
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | consistency_issues | Consistency integrity issues |
     - **Callback**: Collect consistency issues

4. **Step 4: Check Audit Timeline Integrity**
   - **Description**: Check for timeline and sequence integrity issues
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       'timeline_violation' as issue_type,
       at1.audit_id as first_audit_id,
       at2.audit_id as second_audit_id,
       at1.resource_id,
       'create_after_delete' as specific_issue
       FROM audit_trail at1 
       JOIN audit_trail at2 ON at1.resource_id = at2.resource_id 
       WHERE at1.operation_type = 'delete' 
       AND at2.operation_type = 'create' 
       AND at1.operation_timestamp < at2.operation_timestamp
       UNION ALL
       SELECT 
       'timeline_violation' as issue_type,
       at1.audit_id,
       at2.audit_id,
       at1.resource_id,
       'duplicate_timestamps' as specific_issue
       FROM audit_trail at1 
       JOIN audit_trail at2 ON at1.resource_id = at2.resource_id 
       WHERE at1.audit_id != at2.audit_id 
       AND at1.operation_timestamp = at2.operation_timestamp
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | timeline_issues | Timeline integrity issues |
     - **Callback**: Collect timeline issues

5. **Step 5: Check Data Value Integrity**
   - **Description**: Check for data value integrity and validation issues
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       'data_integrity_violation' as issue_type,
       audit_id,
       resource_id,
       operation_type,
       CASE 
         WHEN operation_details::text = '{}' THEN 'empty_operation_details'
         WHEN previous_values IS NOT NULL AND new_values IS NULL AND operation_type = 'update' THEN 'missing_new_values'
         WHEN previous_values IS NULL AND new_values IS NOT NULL AND operation_type = 'create' THEN 'unexpected_previous_values'
         ELSE 'unknown_data_issue'
       END as specific_issue
       FROM audit_trail 
       WHERE (operation_details::text = '{}') 
       OR (previous_values IS NOT NULL AND new_values IS NULL AND operation_type = 'update')
       OR (previous_values IS NULL AND new_values IS NOT NULL AND operation_type = 'create')
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | data_integrity_issues | Data integrity issues |
     - **Callback**: Collect data integrity issues

6. **Step 6: Attempt Repairs (if repair mode enabled)**
   - **Description**: Attempt to repair integrity issues if repair mode is enabled
   - **Data Validation**: Check if repair mode is enabled
   - **SQL Call**: 
     - **SQL**: UPDATE audit_trail SET operation_details = '{"repaired": true, "original_issue": "missing_details"}' WHERE operation_details IS NULL; UPDATE audit_trail SET user_id = 'system' WHERE user_id IS NULL AND operation_type = 'system_generated';
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters for repair operations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | repair_results | Results of repair attempts |
     - **Callback**: Document repair actions

7. **Final Step: Return Integrity Check Results**
   - Return comprehensive integrity check results with issues identified and repair results
