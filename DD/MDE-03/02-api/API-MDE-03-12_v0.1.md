# API Detailed Design Document

**Document ID**: API-MDE-03-12  
**Document Name**: Get Audit Trail API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-12 |
| Document Name | Get Audit Trail API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Get Audit Trail API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |
| 2 | SVE-MDE-03-02_Search and Filter Service_v0.1 | SVE-MDE-03-02 | Search and Filter Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-12 | Get Audit Trail | Retrieves comprehensive audit trail information for idle resource records including all changes, user actions, system events, and compliance tracking with advanced filtering and export capabilities. |

## Logic & Flow

### API ID: API-MDE-03-12
### API Name: Get Audit Trail
### HTTP Method: GET
### URI: /api/v1/idle-resources/audit-trail

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordId | String | Optional | Specific record ID to get audit trail for |
| 2 | userId | String | Optional | Filter by user who made changes |
| 3 | operation | String | Optional | Filter by operation type (create/update/delete) |
| 4 | fromDate | Date | Optional | Start date for audit trail range |
| 5 | toDate | Date | Optional | End date for audit trail range |
| 6 | includeSystemEvents | Boolean | Optional, Default: false | Include automated system events |
| 7 | includeFieldChanges | Boolean | Optional, Default: true | Include detailed field change information |
| 8 | page | Number | Optional, Default: 1 | Page number for pagination |
| 9 | pageSize | Number | Optional, Default: 20, Max: 100 | Number of entries per page |
| 10 | exportFormat | String | Optional | Export format (csv/excel) for compliance reports |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | auditEntries | Array | Array of audit trail entries |
| 2 | totalCount | Number | Total number of audit entries |
| 3 | pageInfo | Object | Pagination information |
| 4 | summaryStatistics | Object | Summary of audit activities |
| 5 | complianceMetrics | Object | Compliance and security metrics |
| 6 | exportUrl | String | Download URL if export requested |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and audit trail access permissions
   - **Data Validation**: JWT token validation and role-based permission check for audit access
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | auditTrail | Operation type |
       | resourceType | idleResource | Resource audit being accessed |
       | requestedRecordId | ARGUMENT.recordId | Specific record if requested |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | auditScope | Allowed audit data access scope |
       | securityLevel | Security clearance level |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Validate Filter Parameters**
   - **Description**: Validate audit trail filter parameters
   - **Data Validation**: Check date ranges, user IDs, operation types, and parameter combinations
   - **Callback**: Return 400 if invalid parameters or unauthorized access to specific records

3. **Step 3: Apply Security Filters**
   - **Description**: Apply security-based filtering based on user permissions
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userContext | STEP1.userContext | Current user context |
       | requestedFilters | All filter arguments | Requested filter criteria |
       | securityLevel | STEP1.securityLevel | User security level |
       | auditScope | STEP1.auditScope | Allowed audit scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | allowedFilters | Security-approved filter criteria |
       | restrictedFields | Fields restricted from view |
       | accessibleRecords | Record IDs user can access |
     - **Callback**: Continue with approved filters

4. **Step 4: Retrieve Audit Trail Entries**
   - **Description**: Get audit trail entries based on filters and permissions
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filters | STEP3.allowedFilters | Security-approved filters |
       | includeSystem | ARGUMENT.includeSystemEvents | System events inclusion |
       | includeFieldDetails | ARGUMENT.includeFieldChanges | Field change details inclusion |
       | userScope | STEP1.auditScope | User access scope |
       | restrictedFields | STEP3.restrictedFields | Fields to exclude |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditEntries | Raw audit trail entries |
       | totalCount | Total matching entries |
       | entryMetadata | Metadata about entries |
     - **Callback**: Continue with pagination

5. **Step 5: Apply Pagination and Sorting**
   - **Description**: Apply pagination and sorting to audit entries
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataSet | STEP4.auditEntries | Audit entries |
       | pageNumber | ARGUMENT.page | Requested page |
       | pageSize | ARGUMENT.pageSize | Page size |
       | sortBy | timestamp | Sort by timestamp |
       | sortOrder | desc | Most recent first |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | paginatedEntries | Paginated audit entries |
       | paginationInfo | Pagination metadata |
       | sortingApplied | Sorting information |
     - **Callback**: Continue with data enrichment

6. **Step 6: Enrich Audit Data**
   - **Description**: Enrich audit entries with additional context and user information
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | auditEntries | STEP5.paginatedEntries | Paginated entries |
       | enrichmentLevel | full | Level of enrichment |
       | includeUserDetails | true | Include user information |
       | includeRecordContext | true | Include record context |
       | userPermissions | STEP1.auditScope | User permissions for filtering |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | enrichedEntries | Audit entries with full context |
       | userMappings | User ID to name mappings |
       | recordContexts | Related record information |
     - **Callback**: Continue with summary generation

7. **Step 7: Generate Summary Statistics**
   - **Description**: Generate audit trail summary and compliance metrics
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | auditData | STEP4.auditEntries | Complete audit dataset |
       | timeRange | From filter parameters | Time range for analysis |
       | summaryType | compliance | Type of summary to generate |
       | userContext | STEP1.userContext | User context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | summaryStats | Summary statistics |
       | complianceMetrics | Compliance indicators |
       | activityPatterns | Usage patterns analysis |
       | riskIndicators | Security risk indicators |
     - **Callback**: Include summary in response

8. **Step 8: Handle Export Request (if applicable)**
   - **Description**: Generate export file if export format requested
   - **Data Validation**: Check if export format specified and user has export permissions
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | auditData | STEP6.enrichedEntries | Enriched audit data |
       | exportFormat | ARGUMENT.exportFormat | Requested format |
       | userContext | STEP1.userContext | User information |
       | complianceLevel | full | Compliance report level |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | exportUrl | Secure download URL |
       | exportMetadata | Export file information |
       | expirationTime | URL expiration time |
     - **Callback**: Include export URL in response if applicable

9. **Step 9: Log Audit Trail Access**
   - **Description**: Log access to audit trail for security monitoring
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | operation | auditTrailAccess | Operation type |
       | userId | STEP1.userContext.userId | User accessing audit trail |
       | accessDetails | Filter and scope information | Access details |
       | recordsAccessed | Count and IDs | Records accessed |
       | timestamp | CURRENT.timestamp | Access timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | accessLogId | Access log entry ID |
       | securityAlert | Security alert if applicable |
     - **Callback**: Continue to response formatting

10. **Step 10: Format Audit Response**
    - **Description**: Format comprehensive audit trail response
    - **Data Validation**: Ensure all response fields properly formatted and security-compliant
    - **Callback**: Return audit trail data with security considerations

11. **Final Step: Return Audit Trail Results**
    - HTTP 200 OK with audit trail entries
    - Pagination and filtering metadata
    - Summary statistics and compliance metrics
    - Export URL if requested
    - Security and access logging confirmation
