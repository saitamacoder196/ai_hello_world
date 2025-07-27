# API Detailed Design Document

**Document ID**: API-MDE-03-05  
**Document Name**: Delete Idle Resource API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-05 |
| Document Name | Delete Idle Resource API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Delete Idle Resource API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-01_Idle Resource CRUD Service_v0.1 | SVE-MDE-03-01 | Idle Resource CRUD Service |
| 2 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |
| 3 | SVE-MDE-03-12_Data Integrity Service_v0.1 | SVE-MDE-03-12 | Data Integrity Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-05 | Delete Idle Resource | Safely deletes an idle resource record with dependency checking, referential integrity validation, and comprehensive audit trail logging. Supports both soft and hard delete based on business rules. |

## Logic & Flow

### API ID: API-MDE-03-05
### API Name: Delete Idle Resource
### HTTP Method: DELETE
### URI: /api/v1/idle-resources/{id}

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | id | String | Required, Valid UUID | Unique identifier of the record to delete |
| 2 | deleteType | String | Optional, Default: soft | Type of deletion (soft/hard) |
| 3 | reason | String | Optional, Max 500 chars | Reason for deletion |
| 4 | force | Boolean | Optional, Default: false | Force delete even with dependencies |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | deleted | Boolean | Confirmation of successful deletion |
| 2 | deletedRecord | Object | Copy of deleted record for audit |
| 3 | auditTrailId | String | Audit trail entry identifier |
| 4 | deletionType | String | Type of deletion performed |
| 5 | dependencyWarnings | Array | Warnings about related data |
| 6 | deletedAt | DateTime | Deletion timestamp |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and delete permissions
   - **Data Validation**: JWT token validation and role-based permission check for delete operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | delete | Operation type |
       | resourceType | idleResource | Resource being deleted |
       | resourceId | ARGUMENT.id | ID of record being deleted |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | deleteLevel | Level of delete permission (soft/hard) |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Retrieve Record for Deletion**
   - **Description**: Get existing record to validate existence and capture current state
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to retrieve |
       | includeMetadata | true | Include version and audit information |
       | includeSoftDeleted | false | Exclude already soft-deleted records |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | currentRecord | Complete current record |
       | recordStatus | Current record status |
       | lastModified | Last modification timestamp |
     - **Callback**: Return 404 if not found or already deleted

3. **Step 3: Dependency and Integrity Check**
   - **Description**: Check for dependencies and referential integrity constraints
   - **Service Call**: SVE-MDE-03-12 - Data Integrity Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to check |
       | recordType | idleResource | Type of record |
       | deleteType | ARGUMENT.deleteType | Requested deletion type |
       | forceDelete | ARGUMENT.force | Force deletion flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | hasDependencies | Boolean indicating dependent records |
       | dependencyList | List of dependent records |
       | canDelete | Boolean indicating if deletion is allowed |
       | integrityWarnings | Warnings about data integrity |
       | recommendedAction | Recommended deletion approach |
     - **Callback**: Return 409 if dependencies exist and force=false

4. **Step 4: Determine Deletion Strategy**
   - **Description**: Determine appropriate deletion method based on constraints
   - **Data Validation**: Validate deletion type against user permissions and dependencies
   - **Callback**: 
     - Use soft delete if dependencies exist or business rules require
     - Use hard delete only if explicitly requested and authorized
     - Return 400 if deletion type not allowed

5. **Step 5: Execute Deletion**
   - **Description**: Perform the actual deletion operation
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to delete |
       | deletionType | STEP4.finalDeleteType | Determined deletion type |
       | userContext | STEP1.userContext | User information for audit |
       | reason | ARGUMENT.reason | Deletion reason |
       | dependencyAction | STEP3.recommendedAction | How to handle dependencies |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | deletionResult | Result of deletion operation |
       | deletedRecord | Copy of record before deletion |
       | deletionMetadata | Deletion timestamp and metadata |
       | affectedRecords | List of affected dependent records |
     - **Callback**: Proceed to audit trail creation

6. **Step 6: Handle Dependent Records**
   - **Description**: Update or handle dependent records based on deletion strategy
   - **Service Call**: SVE-MDE-03-12 - Data Integrity Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | deletedRecordId | ARGUMENT.id | ID of deleted record |
       | dependentRecords | STEP3.dependencyList | List of dependent records |
       | deletionType | STEP4.finalDeleteType | Type of deletion performed |
       | userContext | STEP1.userContext | User context for updates |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updatedDependencies | List of updated dependent records |
       | integrityActions | Actions taken to maintain integrity |
     - **Callback**: Continue to audit trail

7. **Step 7: Create Audit Trail**
   - **Description**: Log the deletion operation for audit purposes
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of deleted record |
       | operation | delete | Type of operation performed |
       | oldValues | STEP2.currentRecord | Record values before deletion |
       | newValues | null | No new values for deletion |
       | userId | STEP1.userContext.userId | User who performed operation |
       | timestamp | CURRENT.timestamp | Operation timestamp |
       | deletionType | STEP4.finalDeleteType | Type of deletion |
       | reason | ARGUMENT.reason | Deletion reason |
       | affectedRecords | STEP5.affectedRecords | List of affected records |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailId | Generated audit trail entry ID |
       | auditEntry | Complete audit trail record |
     - **Callback**: Include audit ID in response

8. **Step 8: Format Response**
   - **Description**: Format successful response with deletion confirmation
   - **Data Validation**: Ensure all response fields are properly formatted
   - **Callback**: Return 200 OK with deletion confirmation

9. **Final Step: Return Success Response**
   - HTTP 200 OK status (for soft delete) or 204 No Content (for hard delete)
   - Deletion confirmation in response body
   - Audit trail ID for tracking
   - List of dependency warnings
   - Deletion metadata
