# API Detailed Design Document

**Document ID**: API-MDE-03-15  
**Document Name**: Archive Record API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-15 |
| Document Name | Archive Record API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Archive Record API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-09_Archive Service_v0.1 | SVE-MDE-03-09 | Archive Service |
| 2 | SVE-MDE-03-01_Idle Resource CRUD Service_v0.1 | SVE-MDE-03-01 | Idle Resource CRUD Service |
| 3 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |
| 4 | SVE-MDE-03-12_Data Integrity Service_v0.1 | SVE-MDE-03-12 | Data Integrity Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-15 | Archive Record | Archives an idle resource record for long-term storage while maintaining data integrity, compliance requirements, and audit trail. Supports both manual and automated archival with retention policy enforcement. |

## Logic & Flow

### API ID: API-MDE-03-15
### API Name: Archive Record
### HTTP Method: PUT
### URI: /api/v1/idle-resources/{id}/archive

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | id | String | Required, Valid UUID | Unique identifier of the record to archive |
| 2 | archiveReason | String | Required, Max 500 chars | Reason for archiving the record |
| 3 | retentionPeriod | Number | Optional | Retention period in months (overrides default) |
| 4 | archiveCategory | String | Optional, Default: standard | Archive category (standard/compliance/legal) |
| 5 | complianceFlag | Boolean | Optional, Default: false | Mark as compliance-required archive |
| 6 | immediateArchive | Boolean | Optional, Default: false | Skip staging and archive immediately |
| 7 | preserveRelations | Boolean | Optional, Default: true | Preserve related record references |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | archiveId | String | Unique archive operation identifier |
| 2 | archivedRecord | Object | Complete record snapshot before archiving |
| 3 | archiveLocation | String | Archive storage location reference |
| 4 | retentionExpiry | DateTime | When the record can be permanently deleted |
| 5 | complianceMetadata | Object | Compliance and legal metadata |
| 6 | auditTrailId | String | Audit trail entry identifier |
| 7 | archiveStatus | String | Archive operation status |
| 8 | archivedAt | DateTime | Archive timestamp |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and archive permissions
   - **Data Validation**: JWT token validation and role-based permission check for archive operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | archive | Operation type |
       | resourceType | idleResource | Resource being archived |
       | resourceId | ARGUMENT.id | ID of record being archived |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | archiveLevel | Level of archive permission |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Retrieve and Validate Record**
   - **Description**: Get existing record and validate it can be archived
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to archive |
       | includeMetadata | true | Include record metadata |
       | checkStatus | true | Check current record status |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | currentRecord | Complete current record |
       | recordStatus | Current record status |
       | lastModified | Last modification timestamp |
       | recordMetadata | Record metadata and relationships |
     - **Callback**: Return 404 if not found, 409 if already archived

3. **Step 3: Validate Archive Eligibility**
   - **Description**: Check if record meets archival criteria and policies
   - **Service Call**: SVE-MDE-03-09 - Archive Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | STEP2.currentRecord | Record to be archived |
       | archiveReason | ARGUMENT.archiveReason | Reason for archiving |
       | archiveCategory | ARGUMENT.archiveCategory | Archive category |
       | userContext | STEP1.userContext | User context |
       | complianceFlag | ARGUMENT.complianceFlag | Compliance requirement flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | eligibilityStatus | Archive eligibility result |
       | eligibilityReasons | Reasons for eligibility decision |
       | requiredApprovals | Required approvals if any |
       | retentionPeriod | Calculated retention period |
       | archivePolicy | Applicable archive policy |
     - **Callback**: Return 422 if record not eligible for archiving

4. **Step 4: Check Dependencies and References**
   - **Description**: Check for dependencies and related records
   - **Service Call**: SVE-MDE-03-12 - Data Integrity Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to check |
       | recordType | idleResource | Type of record |
       | checkType | archive | Check type for archiving |
       | preserveRelations | ARGUMENT.preserveRelations | Relation preservation flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | dependencyStatus | Dependency check result |
       | relatedRecords | List of related records |
       | referenceHandling | How references will be handled |
       | integrityImpact | Impact on data integrity |
     - **Callback**: Handle dependencies based on preserve relations setting

5. **Step 5: Create Record Snapshot**
   - **Description**: Create complete snapshot of record for archive
   - **Service Call**: SVE-MDE-03-09 - Archive Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | STEP2.currentRecord | Complete record data |
       | metadataInclusion | full | Level of metadata to include |
       | relationshipData | STEP4.relatedRecords | Related record information |
       | snapshotType | archive | Type of snapshot |
       | userContext | STEP1.userContext | User context for snapshot |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | recordSnapshot | Complete record snapshot |
       | snapshotMetadata | Snapshot metadata |
       | snapshotSize | Size of snapshot data |
       | snapshotChecksum | Data integrity checksum |
     - **Callback**: Continue with archive processing

6. **Step 6: Process Archive Operation**
   - **Description**: Execute the actual archive operation
   - **Service Call**: SVE-MDE-03-09 - Archive Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordSnapshot | STEP5.recordSnapshot | Record snapshot |
       | archivePolicy | STEP3.archivePolicy | Archive policy to apply |
       | retentionPeriod | ARGUMENT.retentionPeriod or calculated | Retention period |
       | archiveCategory | ARGUMENT.archiveCategory | Archive category |
       | complianceMetadata | Compliance requirements | Compliance metadata |
       | userContext | STEP1.userContext | User information |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | archiveResult | Archive operation result |
       | archiveLocation | Storage location in archive |
       | archiveId | Unique archive identifier |
       | retentionExpiry | Retention expiration date |
       | complianceData | Compliance metadata |
     - **Callback**: Continue with record status update

7. **Step 7: Update Original Record Status**
   - **Description**: Update original record to archived status
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to update |
       | statusUpdate | archived | New record status |
       | archiveReference | STEP6.archiveId | Reference to archive |
       | archiveMetadata | Archive operation metadata | Archive details |
       | userContext | STEP1.userContext | User context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updateResult | Status update result |
       | updatedRecord | Updated record with archived status |
       | statusChangeTime | Status change timestamp |
     - **Callback**: Continue with audit trail creation

8. **Step 8: Create Archive Audit Trail**
   - **Description**: Log the archive operation for audit purposes
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of archived record |
       | operation | archive | Type of operation performed |
       | oldValues | STEP2.currentRecord | Record before archiving |
       | newValues | Archive metadata | Archive operation details |
       | userId | STEP1.userContext.userId | User who performed operation |
       | timestamp | CURRENT.timestamp | Operation timestamp |
       | archiveDetails | Complete archive information | Archive operation details |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailId | Generated audit trail entry ID |
       | auditEntry | Complete audit trail record |
       | complianceAudit | Compliance-specific audit data |
     - **Callback**: Include audit ID in response

9. **Step 9: Handle Related Records (if preserveRelations=false)**
   - **Description**: Update or handle related records based on preservation setting
   - **Data Validation**: Only execute if preserveRelations is false
   - **Service Call**: SVE-MDE-03-12 - Data Integrity Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | archivedRecordId | ARGUMENT.id | ID of archived record |
       | relatedRecords | STEP4.relatedRecords | Related record information |
       | handlingStrategy | Based on archive policy | How to handle relations |
       | userContext | STEP1.userContext | User context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | relationshipResults | Results of relationship handling |
       | updatedReferences | Updated reference information |
     - **Callback**: Continue to response formatting

10. **Step 10: Format Archive Response**
    - **Description**: Format comprehensive archive response
    - **Data Validation**: Ensure all response fields are properly formatted
    - **Callback**: Return archive operation results with metadata

11. **Final Step: Return Archive Results**
    - HTTP 200 OK for successful archive
    - Archive operation identifier and location
    - Complete record snapshot
    - Retention and compliance metadata
    - Audit trail identifier
    - Archive status and timestamp
