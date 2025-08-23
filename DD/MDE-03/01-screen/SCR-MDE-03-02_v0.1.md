# Screen Detailed Design Document

**Document ID**: SCR-MDE-03-02  
**Document Name**: Idle Resource Detail/Edit Screen Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | SCR-MDE-03-02 |
| Document Name | Idle Resource Detail/Edit Screen Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Idle Resource Detail/Edit Screen design |

## Used APIs

| No | API Document | API ID | API Name |
|----|--------------|--------|----------|
| 1 | API-MDE-03-02_Idle Resource Detail API_v0.1 | API-MDE-03-02 | Get Idle Resource Detail |
| 2 | API-MDE-03-03_Idle Resource Create API_v0.1 | API-MDE-03-03 | Create Idle Resource |
| 3 | API-MDE-03-04_Idle Resource Update API_v0.1 | API-MDE-03-04 | Update Idle Resource |
| 4 | API-MDE-03-05_Idle Resource Delete API_v0.1 | API-MDE-03-05 | Delete Idle Resource |
| 5 | API-MDE-03-13_Data Validation API_v0.1 | API-MDE-03-13 | Validate Idle Resource Data |
| 6 | API-MDE-03-14_Audit Trail API_v0.1 | API-MDE-03-14 | Get Audit Trail |

## Screen Layout

| No | ID | Name | Type | Status | Value | Default Value | Data Source | Validations | Description |
|----|----|----|------|--------|-------|---------------|-------------|-------------|-------------|
| 1 | ITEM-01 | Employee Name | Text Field | Enabled | - | Empty | - | Required, Max 100 chars | Full name of the idle employee |
| 2 | ITEM-02 | Employee ID | Text Field | Enabled | - | Empty | - | Required, Unique | Company employee identifier |
| 3 | ITEM-03 | Department | Dropdown | Enabled | - | User's Department | Master Data | Required | Employee's department |
| 4 | ITEM-04 | Child Department | Dropdown | Enabled | - | Empty | Master Data | - | Sub-department if applicable |
| 5 | ITEM-05 | Job Rank | Dropdown | Enabled | - | Empty | Enum_Job_Ranks | Required | Employee's job rank classification |
| 6 | ITEM-06 | Current Location | Dropdown | Enabled | - | Empty | Enum_Locations | Required | Employee's current location |
| 7 | ITEM-07 | Expected Working Places | Multi-select | Enabled | - | Empty | Enum_Locations | - | Preferred work locations |
| 8 | ITEM-08 | Idle Type | Dropdown | Enabled | - | Empty | Enum_Idle_Type | Required | Type of idle status |
| 9 | ITEM-09 | Idle From Date | Date Picker | Enabled | - | Today | - | Required, Valid date | Start date of idle period |
| 10 | ITEM-10 | Idle To Date | Date Picker | Enabled | - | Empty | - | Valid date, >= Idle From | Expected end date of idle period |
| 11 | ITEM-11 | Idle MM | Number | Calculated | - | Auto-calculated | Calculation | - | Months of idle period |
| 12 | ITEM-12 | Japanese Level | Dropdown | Enabled | - | Empty | Enum_Language_Levels | - | Japanese proficiency level |
| 13 | ITEM-13 | English Level | Dropdown | Enabled | - | Empty | Enum_Language_Levels | - | English proficiency level |
| 14 | ITEM-14 | Source Type | Dropdown | Enabled | - | FJPer | Enum_Source_Type | Required | Source of the resource |
| 15 | ITEM-15 | Sales Price | Number | Enabled | - | Empty | - | Positive number | Monthly sales price |
| 16 | ITEM-16 | Special Action | Dropdown | Enabled | - | Empty | Enum_Special_Actions | - | Special action required |
| 17 | ITEM-17 | Change Dept/Lending | Dropdown | Enabled | - | Not Yet Open | Enum_Change_Dept | - | Department change status |
| 18 | ITEM-18 | Skills/Experience | Textarea | Enabled | - | Empty | - | Max 2000 chars | Technical skills and experience |
| 19 | ITEM-19 | Progress Notes | Textarea | Enabled | - | Empty | - | Max 1000 chars | Current progress and notes |
| 20 | ITEM-20 | PIC | Text Field | Enabled | - | Current User | - | Required | Person in charge |
| 21 | ITEM-21 | Last Update | Label | Disabled | - | Dynamic | System | - | Last modification timestamp |
| 22 | ITEM-22 | Save Button | Button | Enabled | - | - | - | - | Save changes to record |
| 23 | ITEM-23 | Cancel Button | Button | Enabled | - | - | - | - | Cancel changes and return |
| 24 | ITEM-24 | Delete Button | Button | Conditional | - | - | - | - | Delete record (role-based) |
| 25 | ITEM-25 | Audit Trail Button | Button | Enabled | - | - | - | - | View change history |

## Events

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | EVT-01 | Screen Initialization | Load record data or initialize for new record creation |
| 2 | EVT-02 | Data Validation | Validate form data on field changes |
| 3 | EVT-03 | Dependent Field Updates | Update dependent fields based on selections |
| 4 | EVT-04 | Save Record | Save new or updated record with validation |
| 5 | EVT-05 | Delete Record | Delete existing record with confirmation |
| 6 | EVT-06 | Cancel Operation | Cancel changes and return to list |
| 7 | EVT-07 | View Audit Trail | Display change history for the record |
| 8 | EVT-08 | Idle Period Calculation | Auto-calculate idle months based on dates |

## Steps & Details

### Event ID: EVT-01
### Event Name: Screen Initialization

#### Steps:
1. **Step 1: Mode Detection**
   - **Trigger**: Screen load
   - **Description**: Determine if screen is for creating new record or editing existing
   - **Data Validation**: Check URL parameters for record ID

2. **Step 2: Load Master Data**
   - **Trigger**: Mode determined
   - **Description**: Load dropdown options and reference data
   - **API Call**: Master Data API for form options
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataTypes | ['departments', 'jobRanks', 'locations', 'idleTypes', 'languageLevels', 'sourceTypes', 'specialActions'] | Required dropdown data |
       | userRole | CONTEXT.userRole | Current user role for filtering |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | masterData | All dropdown options organized by type |
       | userPermissions | Field-level permissions for current user |
     - **Callback**: Populate all dropdown controls with options

3. **Step 3: Load Record Data (Edit Mode)**
   - **Trigger**: Edit mode with valid record ID
   - **Description**: Retrieve existing record data for editing
   - **API Call**: API-MDE-03-02 - Get Idle Resource Detail
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | URL.recordId | ID of record to edit |
       | includeAudit | true | Include audit trail information |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | recordData | Complete record information |
       | auditInfo | Change history and metadata |
       | permissions | User permissions for this specific record |
     - **Callback**: Populate form fields with existing data

4. **Step 4: Apply Field Permissions**
   - **Trigger**: Data loaded or new record mode
   - **Description**: Configure field visibility and editability based on user role
   - **Callback**: Enable/disable fields according to role-based permissions

5. **Final Step: Form Ready**
   - All fields populated and configured
   - Validation rules active
   - Form ready for user interaction

### Event ID: EVT-04
### Event Name: Save Record

#### Steps:
1. **Step 1: Client-side Validation**
   - **Trigger**: User clicks Save button
   - **Description**: Validate all form fields against business rules
   - **Data Validation**: 
     - Required fields completed
     - Date ranges valid
     - Numeric fields within acceptable ranges
     - Text fields within character limits

2. **Step 2: Server-side Validation**
   - **Trigger**: Client validation passed
   - **Description**: Validate data against business rules and constraints
   - **API Call**: API-MDE-03-13 - Validate Idle Resource Data
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | formData | FORM.allFields | All form field values |
       | recordId | CONTEXT.recordId | Record ID for updates (null for new) |
       | validationLevel | full | Complete validation including business rules |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | isValid | Boolean validation result |
       | validationErrors | Array of validation error messages |
       | warnings | Array of warning messages |
     - **Callback**: Display validation errors or proceed to save

3. **Step 3: Save Operation**
   - **Trigger**: Validation successful
   - **Description**: Create new record or update existing record
   - **API Call**: API-MDE-03-03 (Create) or API-MDE-03-04 (Update)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | FORM.validatedData | Validated form data |
       | recordId | CONTEXT.recordId | Record ID for updates |
       | auditInfo | CONTEXT.userInfo | User information for audit trail |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | savedRecord | Complete saved record with generated IDs |
       | auditEntry | Audit trail entry for the operation |
       | success | Operation success confirmation |
     - **Callback**: Show success message and return to list or stay on form

4. **Final Step: Post-save Actions**
   - Update form with saved data (including generated IDs)
   - Show success notification
   - Optional return to list screen

### Event ID: EVT-08
### Event Name: Idle Period Calculation

#### Steps:
1. **Step 1: Date Change Detection**
   - **Trigger**: Change in Idle From or Idle To date fields
   - **Description**: Detect changes in date fields that affect idle period calculation

2. **Step 2: Calculate Idle Months**
   - **Trigger**: Valid dates in both fields
   - **Description**: Calculate the number of months between start and end dates
   - **Callback**: Update ITEM-11 (Idle MM) with calculated value

3. **Step 3: Urgent Case Flagging**
   - **Trigger**: Calculated idle months >= 2
   - **Description**: Apply urgent case visual indicators
   - **Callback**: Highlight relevant fields and show urgent status indicator

4. **Final Step: Update Dependent Fields**
   - Update calculated fields
   - Apply conditional formatting
   - Trigger any dependent validations
