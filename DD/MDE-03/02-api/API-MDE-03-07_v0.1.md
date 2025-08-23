# API Detailed Design Document

**Document ID**: API-MDE-03-07  
**Document Name**: Export Idle Resources API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-07 |
| Document Name | Export Idle Resources API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Export Idle Resources API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-05_Export Service_v0.1 | SVE-MDE-03-05 | Export Service |
| 2 | SVE-MDE-03-02_Search and Filter Service_v0.1 | SVE-MDE-03-02 | Search and Filter Service |
| 3 | SVE-MDE-03-14_File Management Service_v0.1 | SVE-MDE-03-14 | File Management Service |
| 4 | SVE-MDE-03-10_Audit Trail Service_v0.1 | SVE-MDE-03-10 | Audit Trail Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-07 | Export Idle Resources | Exports idle resource data in various formats (Excel, CSV, PDF) with custom field selection, filtering options, and secure file generation. Supports both synchronous and asynchronous export for large datasets. |

## Logic & Flow

### API ID: API-MDE-03-07
### API Name: Export Idle Resources
### HTTP Method: POST
### URI: /api/v1/idle-resources/export

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | format | String | Required, Valid format | Export format (excel, csv, pdf) |
| 2 | filters | Object | Optional | Filter criteria for data selection |
| 3 | columns | Array | Optional | Specific columns to include in export |
| 4 | sortBy | String | Optional | Field to sort by |
| 5 | sortOrder | String | Optional, Default: asc | Sort order (asc/desc) |
| 6 | fileName | String | Optional | Custom filename for export |
| 7 | includeMetadata | Boolean | Optional, Default: true | Include export metadata |
| 8 | asyncMode | Boolean | Optional, Default: false | Use asynchronous processing for large exports |
| 9 | templateId | String | Optional | Predefined export template |
| 10 | password | String | Optional | Password protection for file |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | exportId | String | Unique export operation identifier |
| 2 | fileUrl | String | Download URL for exported file (sync mode) |
| 3 | fileName | String | Generated filename |
| 4 | fileSize | Number | File size in bytes |
| 5 | recordCount | Number | Number of records exported |
| 6 | format | String | Export format used |
| 7 | status | String | Export status (completed/processing/failed) |
| 8 | createdAt | DateTime | Export creation timestamp |
| 9 | expiresAt | DateTime | File expiration timestamp |
| 10 | downloadToken | String | Secure download token |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and export permissions
   - **Data Validation**: JWT token validation and role-based permission check for export operations
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | export | Operation type |
       | resourceType | idleResource | Resource being exported |
       | requestedFormat | ARGUMENT.format | Requested export format |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | allowedFormats | List of allowed export formats |
       | maxRecordLimit | Maximum records user can export |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Validate Export Parameters**
   - **Description**: Validate export format, filters, and column selections
   - **Data Validation**: Check format support, filter syntax, column names
   - **Callback**: Return 400 if invalid parameters

3. **Step 3: Apply Filters and Get Record Count**
   - **Description**: Apply filters to determine scope of export
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filters | ARGUMENT.filters | Filter criteria |
       | countOnly | true | Only return record count |
       | userContext | STEP1.userContext | User role and department |
       | includePermissionFilter | true | Apply role-based filtering |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | totalRecords | Total records matching filters |
       | filteredQuery | Optimized query for export |
       | estimatedSize | Estimated export file size |
     - **Callback**: Check if record count exceeds limits

4. **Step 4: Determine Processing Mode**
   - **Description**: Decide between synchronous and asynchronous processing
   - **Data Validation**: Check record count against thresholds
   - **Callback**: 
     - Use sync mode for small datasets (< 1000 records)
     - Use async mode for large datasets or if explicitly requested
     - Return 413 if exceeds maximum allowed records

5. **Step 5: Initialize Export Operation**
   - **Description**: Create export job and initialize processing
   - **Service Call**: SVE-MDE-03-05 - Export Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | exportFormat | ARGUMENT.format | Export format |
       | dataQuery | STEP3.filteredQuery | Query for data selection |
       | columnSelection | ARGUMENT.columns | Columns to include |
       | sortingOptions | ARGUMENT.sortBy, sortOrder | Sorting preferences |
       | userContext | STEP1.userContext | User information |
       | processingMode | STEP4.mode | Sync or async mode |
       | templateId | ARGUMENT.templateId | Export template if provided |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | exportOperationId | Unique export operation ID |
       | processingContext | Export processing context |
       | estimatedDuration | Estimated completion time |
     - **Callback**: Continue with data export

6. **Step 6: Extract and Process Data**
   - **Description**: Extract data and format according to export specifications
   - **Service Call**: SVE-MDE-03-05 - Export Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | exportOperationId | STEP5.exportOperationId | Operation identifier |
       | dataQuery | STEP3.filteredQuery | Data selection query |
       | formatOptions | Export format settings | Format-specific options |
       | includeMetadata | ARGUMENT.includeMetadata | Metadata inclusion flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | processedData | Formatted export data |
       | recordCount | Actual records processed |
       | processingMetadata | Processing statistics |
     - **Callback**: Continue to file generation

7. **Step 7: Generate Export File**
   - **Description**: Create physical export file with specified format
   - **Service Call**: SVE-MDE-03-14 - File Management Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | exportData | STEP6.processedData | Processed export data |
       | fileName | ARGUMENT.fileName or generated | Target filename |
       | format | ARGUMENT.format | File format |
       | password | ARGUMENT.password | Password protection |
       | exportMetadata | Processing and user metadata | File metadata |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | fileUrl | Secure download URL |
       | filePath | Internal file path |
       | fileSize | Generated file size |
       | downloadToken | Security token for download |
       | expirationTime | File expiration timestamp |
     - **Callback**: File ready for download

8. **Step 8: Create Audit Trail**
   - **Description**: Log the export operation for audit purposes
   - **Service Call**: SVE-MDE-03-10 - Audit Trail Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | operation | export | Type of operation performed |
       | userId | STEP1.userContext.userId | User who performed export |
       | exportDetails | Operation details | Export parameters and results |
       | recordCount | STEP6.recordCount | Number of records exported |
       | fileName | Generated filename | Export filename |
       | timestamp | CURRENT.timestamp | Operation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditTrailId | Generated audit trail entry ID |
       | auditEntry | Complete audit trail record |
     - **Callback**: Include audit ID in response

9. **Step 9: Format Response**
   - **Description**: Format response based on processing mode
   - **Data Validation**: Ensure all response fields are properly formatted
   - **Callback**: 
     - Return immediate download link for sync mode
     - Return operation ID and status for async mode

10. **Final Step: Return Export Results**
    - HTTP 200 OK for successful synchronous export
    - HTTP 202 Accepted for asynchronous export initiation
    - Download URL and security token
    - Export metadata and statistics
    - Operation tracking information
