# API Detailed Design Document

**Document ID**: API-MDE-03-04  
**Document Name**: Update Idle Resource API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-04 |
| Document Name | Update Idle Resource API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Update Idle Resource API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-01_Idle Resource CRUD Service_v0.1 | SVE-MDE-03-01 | Idle Resource CRUD Service |
| 2 | SVE-MDE-03-03_Idle Resource Validation Service_v0.1 | SVE-MDE-03-03 | Idle Resource Validation Service |
| 3 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |
| 4 | SVE-MDE-03-11_Business Rule Engine Service_v0.1 | SVE-MDE-03-11 | Business Rule Engine Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-04 | Update Idle Resource | Updates an existing idle resource record with comprehensive data validation, business rule enforcement, and change tracking. Generates audit trail entry with before/after values. |

## Logic & Flow

### API ID: API-MDE-03-04
### API Name: Update Idle Resource
### HTTP Method: PUT
### URI: /api/v1/idle-resources/{id}

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | id | String | Required, Valid UUID | Unique identifier of the record to update |
| 2 | employeeName | String | Optional, Max 100 chars | Full name of the idle employee |
| 3 | employeeId | String | Optional, Unique | Company employee identifier |
| 4 | departmentId | String | Optional, Valid department ID | Employee's department |
| 5 | childDepartmentId | String | Optional, Valid department ID | Sub-department if applicable |
| 6 | jobRank | String | Optional, Valid job rank | Employee's job rank classification |
| 7 | currentLocation | String | Optional, Valid location | Employee's current location |
| 8 | expectedWorkingPlaces | Array | Optional, Valid locations | Preferred work locations |
| 9 | idleType | String | Optional, Valid idle type | Type of idle status |
| 10 | idleFromDate | Date | Optional, ISO date format | Start date of idle period |
| 11 | idleToDate | Date | Optional, ISO date format | Expected end date of idle period |
| 12 | japaneseLevel | String | Optional, Valid language level | Japanese proficiency level |
| 13 | englishLevel | String | Optional, Valid language level | English proficiency level |
| 14 | sourceType | String | Optional, Valid source type | Source of the resource |
| 15 | salesPrice | Number | Optional, Positive number | Monthly sales price |
| 16 | specialAction | String | Optional, Valid special action | Special action required |
| 17 | changeDeptLending | String | Optional, Valid status | Department change status |
| 18 | skillsExperience | String | Optional, Max 2000 chars | Technical skills and experience |
| 19 | progressNotes | String | Optional, Max 1000 chars | Current progress and notes |
| 20 | pic | String | Optional, Max 100 chars | Person in charge |
| 21 | version | Number | Required, Positive integer | Record version for optimistic locking |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | updatedRecord | Object | Complete updated record with all fields |
| 2 | auditTrailId | String | Audit trail entry identifier |
| 3 | validationWarnings | Array | Non-blocking validation warnings |
| 4 | businessRuleResults | Object | Results of business rule evaluations |
| 5 | updatedAt | DateTime | Record update timestamp |
| 6 | changedFields | Array | List of fields that were modified |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and update permissions
   - **Data Validation**: JWT token validation and role-based permission check for update operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | update | Operation type |
       | resourceType | idleResource | Resource being updated |
       | resourceId | ARGUMENT.id | ID of record being updated |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Retrieve Current Record**
   - **Description**: Get existing record for version check and change comparison
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to retrieve |
       | includeMetadata | true | Include version and audit information |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | currentRecord | Complete current record |
       | recordVersion | Current version number |
       | lastModified | Last modification timestamp |
     - **Callback**: Return 404 if not found, proceed if found

3. **Step 3: Version Conflict Check**
   - **Description**: Check for optimistic locking conflicts
   - **Data Validation**: Compare provided version with current version
   - **Callback**: Return 409 Conflict if versions don't match

4. **Step 4: Input Data Validation**
   - **Description**: Comprehensive validation of all input data
   - **Data Validation**: Required fields, data formats, field lengths, and data types
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | inputData | REQUEST.body | All input data from request |
       | validationType | update | Validation context |
       | currentRecord | STEP2.currentRecord | Existing record for comparison |
       | userRole | STEP1.userContext.role | Current user role |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isValid | Boolean validation result |
       | validationErrors | Array of validation error messages |
       | validationWarnings | Array of warning messages |
       | sanitizedData | Cleaned and processed input data |
       | changedFields | List of fields being modified |
     - **Callback**: Return 400 with errors if validation fails

5. **Step 5: Business Rule Validation**
   - **Description**: Apply business rules and constraints
   - **Data Validation**: Cross-field validation, business logic constraints
   - **Service Call**: SVE-MDE-03-11 - Business Rule Engine Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | STEP4.sanitizedData | Validated input data |
       | currentRecord | STEP2.currentRecord | Current record state |
       | operationType | update | Type of operation |
       | userContext | STEP1.userContext | User role and permissions |
       | changedFields | STEP4.changedFields | Fields being modified |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | ruleResults | Results of business rule evaluations |
       | calculatedFields | Auto-calculated field values |
       | urgentFlags | Urgent case indicators |
       | allowedUpdates | Fields allowed to be updated |
     - **Callback**: Apply calculated values and proceed

6. **Step 6: Update Record**
   - **Description**: Update record in database with new values
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of record to update |
       | updateData | STEP5.enhancedData | Data with business rule results |
       | currentVersion | STEP2.recordVersion | Current version for locking |
       | userContext | STEP1.userContext | User information for audit |
       | changedFields | STEP4.changedFields | Fields being modified |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updatedRecord | Complete record with new values |
       | newVersion | New version number |
       | updateMetadata | Update timestamp and metadata |
     - **Callback**: Proceed to audit trail creation

7. **Step 7: Create Audit Trail**
   - **Description**: Log the update operation for audit purposes
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.id | ID of updated record |
       | operation | update | Type of operation performed |
       | oldValues | STEP2.currentRecord | Previous record values |
       | newValues | STEP6.updatedRecord | New record values |
       | userId | STEP1.userContext.userId | User who performed operation |
       | timestamp | CURRENT.timestamp | Operation timestamp |
       | changedFields | STEP4.changedFields | Fields that were modified |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailId | Generated audit trail entry ID |
       | auditEntry | Complete audit trail record |
     - **Callback**: Include audit ID in response

8. **Step 8: Format Response**
   - **Description**: Format successful response with updated record data
   - **Data Validation**: Ensure all response fields are properly formatted
   - **Callback**: Return 200 OK with complete record information

9. **Final Step: Return Success Response**
   - HTTP 200 OK status
   - Complete updated record in response body
   - Audit trail ID for tracking
   - List of changed fields
   - Any validation warnings
