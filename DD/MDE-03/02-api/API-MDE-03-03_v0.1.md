# API Detailed Design Document

**Document ID**: API-MDE-03-03  
**Document Name**: Create Idle Resource API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-03 |
| Document Name | Create Idle Resource API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Create Idle Resource API design |

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
| 1 | API-MDE-03-03 | Create Idle Resource | Creates a new idle resource record with comprehensive data validation, business rule enforcement, and mandatory field checking. Generates audit trail entry upon successful creation. |

## Logic & Flow

### API ID: API-MDE-03-03
### API Name: Create Idle Resource
### HTTP Method: POST
### URI: /api/v1/idle-resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | employeeName | String | Required, Max 100 chars | Full name of the idle employee |
| 2 | employeeId | String | Required, Unique | Company employee identifier |
| 3 | departmentId | String | Required, Valid department ID | Employee's department |
| 4 | childDepartmentId | String | Optional, Valid department ID | Sub-department if applicable |
| 5 | jobRank | String | Required, Valid job rank | Employee's job rank classification |
| 6 | currentLocation | String | Required, Valid location | Employee's current location |
| 7 | expectedWorkingPlaces | Array | Optional, Valid locations | Preferred work locations |
| 8 | idleType | String | Required, Valid idle type | Type of idle status |
| 9 | idleFromDate | Date | Required, ISO date format | Start date of idle period |
| 10 | idleToDate | Date | Optional, ISO date format | Expected end date of idle period |
| 11 | japaneseLevel | String | Optional, Valid language level | Japanese proficiency level |
| 12 | englishLevel | String | Optional, Valid language level | English proficiency level |
| 13 | sourceType | String | Required, Valid source type | Source of the resource |
| 14 | salesPrice | Number | Optional, Positive number | Monthly sales price |
| 15 | specialAction | String | Optional, Valid special action | Special action required |
| 16 | changeDeptLending | String | Optional, Valid status | Department change status |
| 17 | skillsExperience | String | Optional, Max 2000 chars | Technical skills and experience |
| 18 | progressNotes | String | Optional, Max 1000 chars | Current progress and notes |
| 19 | pic | String | Required, Max 100 chars | Person in charge |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | id | String | Generated unique identifier for the new record |
| 2 | createdRecord | Object | Complete created record with all fields |
| 3 | auditTrailId | String | Audit trail entry identifier |
| 4 | validationWarnings | Array | Non-blocking validation warnings |
| 5 | businessRuleResults | Object | Results of business rule evaluations |
| 6 | createdAt | DateTime | Record creation timestamp |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and create permissions
   - **Data Validation**: JWT token validation and role-based permission check for create operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | create | Operation type |
       | resourceType | idleResource | Resource being created |
       | departmentId | ARGUMENT.departmentId | Target department for new record |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Input Data Validation**
   - **Description**: Comprehensive validation of all input data
   - **Data Validation**: Required fields, data formats, field lengths, and data types
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | inputData | REQUEST.body | All input data from request |
       | validationType | create | Validation context |
       | userRole | STEP1.userContext.role | Current user role |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isValid | Boolean validation result |
       | validationErrors | Array of validation error messages |
       | validationWarnings | Array of warning messages |
       | sanitizedData | Cleaned and processed input data |
     - **Callback**: Return 400 with errors if validation fails

3. **Step 3: Business Rule Validation**
   - **Description**: Apply business rules and constraints
   - **Data Validation**: Cross-field validation, business logic constraints
   - **Service Call**: SVE-MDE-03-11 - Business Rule Engine Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | STEP2.sanitizedData | Validated input data |
       | operationType | create | Type of operation |
       | userContext | STEP1.userContext | User role and permissions |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | ruleResults | Results of business rule evaluations |
       | calculatedFields | Auto-calculated field values |
       | urgentFlags | Urgent case indicators |
     - **Callback**: Apply calculated values and proceed

4. **Step 4: Create Record**
   - **Description**: Insert new record into database
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | STEP3.enhancedData | Data with business rule results |
       | userContext | STEP1.userContext | User information for audit |
       | operationType | create | Operation type |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | createdRecord | Complete record with generated ID |
       | recordId | Generated unique identifier |
       | creationMetadata | Creation timestamp and metadata |
     - **Callback**: Proceed to audit trail creation

5. **Step 5: Create Audit Trail**
   - **Description**: Log the create operation for audit purposes
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | STEP4.recordId | ID of created record |
       | operation | create | Type of operation performed |
       | oldValues | null | No previous values for new record |
       | newValues | STEP4.createdRecord | Complete new record data |
       | userId | STEP1.userContext.userId | User who performed operation |
       | timestamp | CURRENT.timestamp | Operation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailId | Generated audit trail entry ID |
       | auditEntry | Complete audit trail record |
     - **Callback**: Include audit ID in response

6. **Step 6: Format Response**
   - **Description**: Format successful response with created record data
   - **Data Validation**: Ensure all response fields are properly formatted
   - **Callback**: Return 201 Created with complete record information

7. **Final Step: Return Success Response**
   - HTTP 201 Created status
   - Complete created record in response body
   - Audit trail ID for tracking
   - Any validation warnings
   - Location header with new resource URL
