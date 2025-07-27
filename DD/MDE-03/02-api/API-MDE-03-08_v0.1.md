# API Detailed Design Document

**Document ID**: API-MDE-03-08  
**Document Name**: Import Idle Resources API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-08 |
| Document Name | Import Idle Resources API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Import Idle Resources API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-06_Import Service_v0.1 | SVE-MDE-03-06 | Import Service |
| 2 | SVE-MDE-03-03_Idle Resource Validation Service_v0.1 | SVE-MDE-03-03 | Idle Resource Validation Service |
| 3 | SVE-MDE-03-04_Bulk Operation Service_v0.1 | SVE-MDE-03-04 | Bulk Operation Service |
| 4 | SVE-MDE-03-14_File Management Service_v0.1 | SVE-MDE-03-14 | File Management Service |
| 5 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-08 | Import Idle Resources | Imports idle resource data from uploaded files (Excel, CSV) with comprehensive validation, duplicate detection, error reporting, and rollback capabilities. Supports both immediate and staged import modes. |

## Logic & Flow

### API ID: API-MDE-03-08
### API Name: Import Idle Resources
### HTTP Method: POST
### URI: /api/v1/idle-resources/import

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | file | File | Required, Max 10MB | Import file (Excel/CSV format) |
| 2 | importMode | String | Optional, Default: validate | Import mode (validate/immediate/staged) |
| 3 | duplicateHandling | String | Optional, Default: skip | How to handle duplicates (skip/update/error) |
| 4 | validateOnly | Boolean | Optional, Default: false | Only validate without importing |
| 5 | columnMapping | Object | Optional | Custom column mapping configuration |
| 6 | templateId | String | Optional | Predefined import template |
| 7 | rollbackOnError | Boolean | Optional, Default: true | Rollback entire import on any error |
| 8 | batchSize | Number | Optional, Default: 100 | Processing batch size |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | importId | String | Unique import operation identifier |
| 2 | status | String | Import status (completed/processing/failed/validated) |
| 3 | totalRows | Number | Total rows in import file |
| 4 | validRows | Number | Number of valid rows |
| 5 | invalidRows | Number | Number of invalid rows |
| 6 | processedRows | Number | Number of rows processed |
| 7 | duplicateRows | Number | Number of duplicate rows found |
| 8 | errorReport | Array | Detailed error information for invalid rows |
| 9 | warningReport | Array | Warning information for processed rows |
| 10 | importSummary | Object | Summary of import operation |
| 11 | auditTrailId | String | Audit trail entry identifier |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and import permissions
   - **Data Validation**: JWT token validation and role-based permission check for import operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | import | Operation type |
       | resourceType | idleResource | Resource being imported |
       | importMode | ARGUMENT.importMode | Requested import mode |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | maxImportSize | Maximum file size allowed |
       | allowedModes | List of allowed import modes |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: File Upload and Validation**
   - **Description**: Process uploaded file and validate format
   - **Data Validation**: Check file size, format, and basic structure
   - **Service Call**: SVE-MDE-03-14 - File Management Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | uploadedFile | ARGUMENT.file | Uploaded import file |
       | allowedFormats | ['xlsx', 'csv'] | Supported file formats |
       | maxFileSize | STEP1.maxImportSize | Maximum file size |
       | scanForVirus | true | Security scanning flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | fileMetadata | File information and metadata |
       | fileIsValid | Boolean file validity status |
       | securityScanResult | Virus scan results |
       | tempFilePath | Temporary file storage path |
     - **Callback**: Return 400 if file invalid or unsafe

3. **Step 3: Parse and Extract Data**
   - **Description**: Parse file content and extract data rows
   - **Service Call**: SVE-MDE-03-06 - Import Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filePath | STEP2.tempFilePath | Path to uploaded file |
       | fileFormat | Detected from file extension | File format |
       | columnMapping | ARGUMENT.columnMapping | Custom column mapping |
       | templateId | ARGUMENT.templateId | Import template |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | extractedData | Parsed data rows |
       | columnHeaders | Detected column headers |
       | totalRowCount | Total number of data rows |
       | parseErrors | Parsing error information |
     - **Callback**: Return 400 if critical parsing errors

4. **Step 4: Data Validation and Cleansing**
   - **Description**: Validate each row of imported data
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | importData | STEP3.extractedData | Extracted data rows |
       | validationType | import | Validation context |
       | userRole | STEP1.userContext.role | Current user role |
       | batchSize | ARGUMENT.batchSize | Processing batch size |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | validationResults | Validation results for each row |
       | validRows | List of valid rows |
       | invalidRows | List of invalid rows with errors |
       | warningRows | List of rows with warnings |
       | cleanedData | Validated and cleaned data |
     - **Callback**: Continue with validation results

5. **Step 5: Duplicate Detection**
   - **Description**: Check for duplicates within import data and against existing records
   - **Service Call**: SVE-MDE-03-06 - Import Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | validData | STEP4.validRows | Valid rows from validation |
       | duplicateStrategy | ARGUMENT.duplicateHandling | How to handle duplicates |
       | duplicateFields | ['employeeId'] | Fields to check for duplicates |
       | userContext | STEP1.userContext | User context for filtering |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | duplicateAnalysis | Duplicate detection results |
       | uniqueRows | Rows without duplicates |
       | duplicateRows | Identified duplicate rows |
       | conflictResolution | Resolved conflicts based on strategy |
     - **Callback**: Handle duplicates according to specified strategy

6. **Step 6: Process Import Based on Mode**
   - **Description**: Execute import based on selected mode (validate/immediate/staged)
   - **Data Validation**: Check import mode and process accordingly
   - **Service Call**: SVE-MDE-03-04 - Bulk Operation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | processMode | ARGUMENT.importMode | Import processing mode |
       | importData | STEP5.uniqueRows | Final data to import |
       | duplicateData | STEP5.conflictResolution | Duplicate handling results |
       | userContext | STEP1.userContext | User information |
       | rollbackOnError | ARGUMENT.rollbackOnError | Error handling policy |
       | validateOnly | ARGUMENT.validateOnly | Validation only flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | processingResults | Results of import processing |
       | successfulImports | Successfully imported records |
       | failedImports | Failed import attempts |
       | processingMetadata | Processing statistics |
     - **Callback**: Continue to completion handling

7. **Step 7: Generate Import Report**
   - **Description**: Compile comprehensive import report
   - **Service Call**: SVE-MDE-03-06 - Import Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | importResults | STEP6.processingResults | Processing results |
       | validationResults | STEP4.validationResults | Validation results |
       | duplicateResults | STEP5.duplicateAnalysis | Duplicate analysis |
       | importMetadata | Operation metadata | Import operation details |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | importReport | Comprehensive import report |
       | errorDetails | Detailed error information |
       | warningDetails | Warning information |
       | successSummary | Success statistics |
     - **Callback**: Include report in response

8. **Step 8: Create Audit Trail**
   - **Description**: Log the import operation for audit purposes
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | operation | import | Type of operation performed |
       | userId | STEP1.userContext.userId | User who performed import |
       | importDetails | Operation details | Import parameters and results |
       | fileName | STEP2.fileMetadata.name | Import filename |
       | recordCount | STEP6.successfulImports.length | Number of records imported |
       | timestamp | CURRENT.timestamp | Operation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailId | Generated audit trail entry ID |
       | auditEntry | Complete audit trail record |
     - **Callback**: Include audit ID in response

9. **Step 9: Cleanup Temporary Files**
   - **Description**: Clean up temporary files and resources
   - **Service Call**: SVE-MDE-03-14 - File Management Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | tempFilePath | STEP2.tempFilePath | Temporary file to clean |
       | importId | Generated import ID | Import operation identifier |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | cleanupResult | File cleanup confirmation |
     - **Callback**: Continue to response formatting

10. **Step 10: Format Response**
    - **Description**: Format comprehensive import response
    - **Data Validation**: Ensure all response fields are properly formatted
    - **Callback**: Return detailed import results and statistics

11. **Final Step: Return Import Results**
    - HTTP 200 OK for successful validation or import
    - HTTP 202 Accepted for staged import
    - HTTP 400 for validation failures
    - Comprehensive import report
    - Error and warning details
    - Processing statistics
