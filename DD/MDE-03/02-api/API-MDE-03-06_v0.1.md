# API Detailed Design Document

**Document ID**: API-MDE-03-06  
**Document Name**: Bulk Update Idle Resources API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-06 |
| Document Name | Bulk Update Idle Resources API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Bulk Update Idle Resources API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-01_Idle Resource CRUD Service_v0.1 | SVE-MDE-03-01 | Idle Resource CRUD Service |
| 2 | SVE-MDE-03-03_Idle Resource Validation Service_v0.1 | SVE-MDE-03-03 | Idle Resource Validation Service |
| 3 | SVE-MDE-03-04_Bulk Operation Service_v0.1 | SVE-MDE-03-04 | Bulk Operation Service |
| 4 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-06 | Bulk Update Idle Resources | Updates multiple idle resource records in a single transaction with batch validation, rollback capability, and comprehensive progress tracking. Supports partial updates and selective field modifications. |

## Logic & Flow

### API ID: API-MDE-03-06
### API Name: Bulk Update Idle Resources
### HTTP Method: PATCH
### URI: /api/v1/idle-resources/bulk

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | updates | Array | Required, Max 100 items | Array of update objects |
| 2 | updates[].id | String | Required, Valid UUID | Record ID to update |
| 3 | updates[].data | Object | Required | Update data fields |
| 4 | updates[].version | Number | Required | Record version for optimistic locking |
| 5 | rollbackOnError | Boolean | Optional, Default: true | Rollback entire operation if any record fails |
| 6 | validateAll | Boolean | Optional, Default: true | Validate all records before processing any |
| 7 | operationId | String | Optional | Client-provided operation identifier |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | operationId | String | Unique operation identifier |
| 2 | totalRequested | Number | Total number of records requested for update |
| 3 | successCount | Number | Number of successfully updated records |
| 4 | failureCount | Number | Number of failed updates |
| 5 | results | Array | Individual update results for each record |
| 6 | auditTrailIds | Array | Audit trail entry identifiers |
| 7 | operationStatus | String | Overall operation status |
| 8 | executionTime | Number | Total execution time in milliseconds |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and bulk update permissions
   - **Data Validation**: JWT token validation and role-based permission check for bulk operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | bulkUpdate | Operation type |
       | resourceType | idleResource | Resource being updated |
       | recordCount | ARGUMENT.updates.length | Number of records to update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | maxBatchSize | Maximum allowed batch size for user |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Validate Batch Size and Format**
   - **Description**: Validate request format and batch size limits
   - **Data Validation**: Check batch size, request format, and required fields
   - **Callback**: Return 400 if batch too large or malformed request

3. **Step 3: Pre-validation of All Records**
   - **Description**: Validate all records before processing if validateAll=true
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | updateRequests | ARGUMENT.updates | All update requests |
       | validationType | bulkUpdate | Validation context |
       | userRole | STEP1.userContext.role | Current user role |
       | preValidation | true | Pre-validation flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | validationResults | Validation results for each record |
       | overallValid | Boolean indicating if all records valid |
       | validationSummary | Summary of validation issues |
     - **Callback**: Return 400 with validation errors if any fail and validateAll=true

4. **Step 4: Initialize Bulk Operation**
   - **Description**: Initialize bulk operation tracking and transaction
   - **Service Call**: SVE-MDE-03-04 - Bulk Operation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | operationType | bulkUpdate | Type of bulk operation |
       | recordCount | ARGUMENT.updates.length | Number of records |
       | userContext | STEP1.userContext | User information |
       | operationId | ARGUMENT.operationId | Client operation ID |
       | rollbackOnError | ARGUMENT.rollbackOnError | Rollback flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | bulkOperationId | Generated operation identifier |
       | transactionId | Database transaction identifier |
       | operationContext | Operation tracking context |
     - **Callback**: Continue with bulk processing

5. **Step 5: Process Individual Updates**
   - **Description**: Process each update request individually
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service (for each record)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.updates[i].id | ID of current record |
       | updateData | ARGUMENT.updates[i].data | Update data |
       | currentVersion | ARGUMENT.updates[i].version | Version for locking |
       | bulkContext | STEP4.operationContext | Bulk operation context |
       | userContext | STEP1.userContext | User information |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updateResult | Result of individual update |
       | updatedRecord | Updated record if successful |
       | errorDetails | Error information if failed |
       | processingTime | Time taken for this update |
     - **Callback**: 
       - Accumulate results
       - If error and rollbackOnError=true, initiate rollback
       - Continue to next record if rollbackOnError=false

6. **Step 6: Handle Transaction Completion**
   - **Description**: Commit or rollback transaction based on results
   - **Service Call**: SVE-MDE-03-04 - Bulk Operation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | bulkOperationId | STEP4.bulkOperationId | Operation identifier |
       | processingResults | STEP5.allResults | All processing results |
       | shouldCommit | Based on errors and rollback policy | Commit decision |
       | transactionId | STEP4.transactionId | Transaction to commit/rollback |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | finalStatus | Final operation status |
       | commitResult | Transaction commit result |
       | affectedRecords | List of successfully updated records |
       | rollbackDetails | Rollback information if applicable |
     - **Callback**: Continue to audit trail creation

7. **Step 7: Create Audit Trail Entries**
   - **Description**: Create audit trail for all successful updates
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | bulkOperationId | STEP4.bulkOperationId | Bulk operation identifier |
       | updateResults | STEP6.affectedRecords | Successfully updated records |
       | userId | STEP1.userContext.userId | User who performed operation |
       | timestamp | CURRENT.timestamp | Operation timestamp |
       | operationType | bulkUpdate | Type of operation |
       | batchMetadata | Operation metadata | Batch processing details |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailIds | List of audit trail entry IDs |
       | auditSummary | Summary of audit entries created |
     - **Callback**: Include audit IDs in response

8. **Step 8: Compile Operation Summary**
   - **Description**: Compile comprehensive operation results
   - **Data Validation**: Ensure all result fields are properly formatted
   - **Callback**: Return operation summary with detailed results

9. **Final Step: Return Bulk Operation Results**
   - HTTP 200 OK for successful completion
   - HTTP 207 Multi-Status for partial success
   - HTTP 400 for validation failures
   - Detailed results for each record
   - Overall operation statistics
   - Audit trail identifiers
