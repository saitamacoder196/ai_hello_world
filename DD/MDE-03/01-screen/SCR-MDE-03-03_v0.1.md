# Screen Detailed Design Document

**Document ID**: SCR-MDE-03-03  
**Document Name**: Import/Export Screen Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | SCR-MDE-03-03 |
| Document Name | Import/Export Screen Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Import/Export Screen design |

## Used APIs

| No | API Document | API ID | API Name |
|----|--------------|--------|----------|
| 1 | API-MDE-03-09_Data Export API_v0.1 | API-MDE-03-09 | Export Idle Resources |
| 2 | API-MDE-03-10_Data Import API_v0.1 | API-MDE-03-10 | Import Idle Resources |
| 3 | API-MDE-03-13_Data Validation API_v0.1 | API-MDE-03-13 | Validate Idle Resource Data |
| 4 | API-MDE-03-01_Idle Resource List API_v0.1 | API-MDE-03-01 | Get Idle Resource List |

## Screen Layout

| No | ID | Name | Type | Status | Value | Default Value | Data Source | Validations | Description |
|----|----|----|------|--------|-------|---------------|-------------|-------------|-------------|
| 1 | ITEM-01 | Operation Tab Selector | Tab | Enabled | - | Export | Fixed options | - | Switch between Export and Import operations |
| 2 | ITEM-02 | Export Format Selector | Radio | Enabled | - | Excel | Fixed options | Required | Select export file format (Excel, CSV) |
| 3 | ITEM-03 | Export Filter Panel | Panel | Enabled | - | Collapsed | - | - | Panel containing export filter options |
| 4 | ITEM-04 | Department Filter | Dropdown | Enabled | - | User's Department | Master Data | - | Filter records by department |
| 5 | ITEM-05 | Date Range From | Date Picker | Enabled | - | 30 days ago | - | Valid date | Start date for export range |
| 6 | ITEM-06 | Date Range To | Date Picker | Enabled | - | Today | - | Valid date, >= From date | End date for export range |
| 7 | ITEM-07 | Idle Type Filter | Multi-select | Enabled | - | All Selected | Enum_Idle_Type | - | Filter by idle status types |
| 8 | ITEM-08 | Column Selector | Checklist | Enabled | - | All Selected | Field definitions | - | Select columns to include in export |
| 9 | ITEM-09 | Preview Button | Button | Enabled | - | - | - | - | Preview data to be exported |
| 10 | ITEM-10 | Export Button | Button | Enabled | - | - | - | - | Generate and download export file |
| 11 | ITEM-11 | Preview Table | Table | Dynamic | - | Hidden | API Data | - | Preview of data to be exported |
| 12 | ITEM-12 | Import File Selector | File Upload | Enabled | - | Empty | - | Excel/CSV files only | Select file for import |
| 13 | ITEM-13 | Import Template Download | Link | Enabled | - | - | - | - | Download import template file |
| 14 | ITEM-14 | Import Options Panel | Panel | Enabled | - | Visible | - | - | Panel with import configuration options |
| 15 | ITEM-15 | Update Existing Records | Checkbox | Enabled | - | Unchecked | - | - | Option to update existing records |
| 16 | ITEM-16 | Skip Invalid Records | Checkbox | Enabled | - | Checked | - | - | Continue import despite validation errors |
| 17 | ITEM-17 | Import Preview Button | Button | Enabled | - | - | - | - | Preview imported data before processing |
| 18 | ITEM-18 | Start Import Button | Button | Enabled | - | - | - | - | Begin import process |
| 19 | ITEM-19 | Import Status Panel | Panel | Dynamic | - | Hidden | - | - | Panel showing import progress and results |
| 20 | ITEM-20 | Progress Bar | Progress | Dynamic | - | 0% | - | - | Import progress indicator |
| 21 | ITEM-21 | Status Message | Label | Dynamic | - | Ready | System | - | Current operation status |
| 22 | ITEM-22 | Error Log | Textarea | Dynamic | - | Empty | System | - | Display validation errors and warnings |
| 23 | ITEM-23 | Success Counter | Label | Dynamic | - | 0 | System | - | Number of successfully processed records |
| 24 | ITEM-24 | Error Counter | Label | Dynamic | - | 0 | System | - | Number of records with errors |
| 25 | ITEM-25 | Download Error Report | Button | Dynamic | - | Hidden | - | - | Download detailed error report |

## Events

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | EVT-01 | Screen Initialization | Load initial configuration and user permissions |
| 2 | EVT-02 | Export Tab Selection | Configure screen for export operations |
| 3 | EVT-03 | Import Tab Selection | Configure screen for import operations |
| 4 | EVT-04 | Export Preview | Preview data to be exported based on filters |
| 5 | EVT-05 | Export Execution | Generate and download export file |
| 6 | EVT-06 | File Upload | Handle import file selection and validation |
| 7 | EVT-07 | Import Preview | Preview and validate import data |
| 8 | EVT-08 | Import Execution | Process import file and update database |
| 9 | EVT-09 | Error Handling | Handle and display import/export errors |

## Steps & Details

### Event ID: EVT-01
### Event Name: Screen Initialization

#### Steps:
1. **Step 1: User Permission Check**
   - **Trigger**: Screen load
   - **Description**: Verify user has import/export permissions
   - **Data Validation**: Check user role permissions for import/export operations

2. **Step 2: Load Configuration Data**
   - **Trigger**: Permission validated
   - **Description**: Load dropdown options and default settings
   - **API Call**: Master Data API for filter options
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataTypes | ['departments', 'idleTypes'] | Required filter options |
       | userRole | CONTEXT.userRole | Current user role |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | filterOptions | Available filter values |
       | columnDefinitions | Available columns for export |
       | userPermissions | Import/export permissions |
     - **Callback**: Configure filter controls and column selector

3. **Step 3: Initialize Default Settings**
   - **Trigger**: Configuration loaded
   - **Description**: Set default values based on user preferences and role
   - **Callback**: Configure default filters and export settings

4. **Final Step: Screen Ready**
   - Export tab active by default
   - All controls configured and ready
   - User can begin export/import operations

### Event ID: EVT-04
### Event Name: Export Preview

#### Steps:
1. **Step 1: Validate Export Filters**
   - **Trigger**: User clicks Preview button
   - **Description**: Validate export filter criteria
   - **Data Validation**: 
     - Date range validity
     - At least one column selected
     - Department filter appropriate for user role

2. **Step 2: Generate Preview Data**
   - **Trigger**: Filters validated
   - **Description**: Retrieve preview of data matching export criteria
   - **API Call**: API-MDE-03-01 - Get Idle Resource List (Preview mode)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | departmentFilter | ITEM-04.value | Selected department filter |
       | dateRangeFrom | ITEM-05.value | Export start date |
       | dateRangeTo | ITEM-06.value | Export end date |
       | idleTypeFilter | ITEM-07.value | Selected idle types |
       | selectedColumns | ITEM-08.value | Columns to include |
       | previewMode | true | Limit results for preview |
       | maxRecords | 100 | Preview record limit |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | previewData | Sample of records to be exported |
       | totalCount | Total number of records matching criteria |
       | estimatedSize | Estimated export file size |
     - **Callback**: Display preview table and record count

3. **Final Step: Display Preview**
   - Show preview table with sample data
   - Display total record count
   - Enable export button

### Event ID: EVT-05
### Event Name: Export Execution

#### Steps:
1. **Step 1: Validate Export Request**
   - **Trigger**: User clicks Export button
   - **Description**: Final validation before export generation
   - **Data Validation**: All export parameters valid and user has permission

2. **Step 2: Generate Export File**
   - **Trigger**: Validation passed
   - **Description**: Create export file with all matching records
   - **API Call**: API-MDE-03-09 - Export Idle Resources
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | exportFormat | ITEM-02.value | Selected file format (Excel/CSV) |
       | departmentFilter | ITEM-04.value | Department filter |
       | dateRangeFrom | ITEM-05.value | Export start date |
       | dateRangeTo | ITEM-06.value | Export end date |
       | idleTypeFilter | ITEM-07.value | Selected idle types |
       | selectedColumns | ITEM-08.value | Columns to include |
       | includeHeaders | true | Include column headers |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | exportFileUrl | Download URL for generated file |
       | fileName | Generated file name |
       | recordCount | Number of records exported |
       | fileSize | Export file size |
     - **Callback**: Initiate file download and show success message

3. **Final Step: Complete Export**
   - Download file automatically starts
   - Show export success message with record count
   - Log export activity for audit trail

### Event ID: EVT-07
### Event Name: Import Preview

#### Steps:
1. **Step 1: Validate Import File**
   - **Trigger**: User clicks Import Preview button
   - **Description**: Validate uploaded file format and structure
   - **Data Validation**: 
     - File format is Excel or CSV
     - File size within limits
     - Required columns present

2. **Step 2: Parse and Validate Data**
   - **Trigger**: File validation passed
   - **Description**: Parse file content and validate data
   - **API Call**: API-MDE-03-10 - Import Idle Resources (Preview mode)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | importFile | ITEM-12.file | Uploaded file |
       | updateExisting | ITEM-15.checked | Allow updates to existing records |
       | skipInvalid | ITEM-16.checked | Skip records with validation errors |
       | previewMode | true | Validation only, no data changes |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | validRecords | Records that passed validation |
       | invalidRecords | Records with validation errors |
       | validationSummary | Summary of validation results |
       | previewData | Sample of records to be imported |
     - **Callback**: Display validation results and preview data

3. **Step 3: Display Validation Results**
   - **Trigger**: Validation completed
   - **Description**: Show validation summary and errors
   - **Callback**: 
     - Update success/error counters
     - Display error details in error log
     - Enable/disable import button based on results

4. **Final Step: Import Ready**
   - Show validation summary
   - Display any errors that need correction
   - Enable Start Import button if validation successful

### Event ID: EVT-08
### Event Name: Import Execution

#### Steps:
1. **Step 1: Final Confirmation**
   - **Trigger**: User clicks Start Import button
   - **Description**: Confirm import operation with user
   - **Data Validation**: User has confirmed import with current settings

2. **Step 2: Process Import**
   - **Trigger**: Confirmation received
   - **Description**: Execute import operation with progress tracking
   - **API Call**: API-MDE-03-10 - Import Idle Resources (Execute mode)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | importFile | ITEM-12.file | Uploaded file |
       | updateExisting | ITEM-15.checked | Allow updates to existing records |
       | skipInvalid | ITEM-16.checked | Skip records with validation errors |
       | executeMode | true | Perform actual data import |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | importResults | Final import results and statistics |
       | processedRecords | Number of successfully processed records |
       | errorRecords | Number of records with errors |
       | errorReport | Detailed error report |
     - **Callback**: Update progress bar and show final results

3. **Step 3: Complete Import**
   - **Trigger**: Import processing finished
   - **Description**: Display final import results and cleanup
   - **Callback**: 
     - Show final success/error counts
     - Provide error report download if needed
     - Reset form for next operation

4. **Final Step: Post-Import Actions**
   - Display import completion message
   - Provide error report download link if errors occurred
   - Log import activity for audit trail
   - Optional navigation back to main screen
