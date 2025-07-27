# Screen Detailed Design Document

**Document ID**: SCR-MDE-03-01  
**Document Name**: Idle Resource List Screen Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | SCR-MDE-03-01 |
| Document Name | Idle Resource List Screen Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Idle Resource List Screen design |

## Used APIs

| No | API Document | API ID | API Name |
|----|--------------|--------|----------|
| 1 | API-MDE-03-01_Idle Resource List API_v0.1 | API-MDE-03-01 | Get Idle Resource List |
| 2 | API-MDE-03-07_Idle Resource Search API_v0.1 | API-MDE-03-07 | Search Idle Resources |
| 3 | API-MDE-03-08_Idle Resource Statistics API_v0.1 | API-MDE-03-08 | Get Idle Resource Statistics |
| 4 | API-MDE-03-11_Column Configuration API_v0.1 | API-MDE-03-11 | Get Column Configuration |
| 5 | API-MDE-03-12_Column Configuration Update API_v0.1 | API-MDE-03-12 | Update Column Configuration |
| 6 | API-MDE-03-06_Batch Operations API_v0.1 | API-MDE-03-06 | Batch Update Idle Resources |

## Screen Layout

| No | ID | Name | Type | Status | Value | Default Value | Data Source | Validations | Description |
|----|----|----|------|--------|-------|---------------|-------------|-------------|-------------|
| 1 | ITEM-01 | Search Input Field | Text Field | Enabled | - | Empty | - | Max 100 characters | Global search input for all fields |
| 2 | ITEM-02 | Filter Panel Toggle | Button | Enabled | - | Collapsed | - | - | Toggle button to show/hide advanced filters |
| 3 | ITEM-03 | Department Filter | Dropdown | Enabled | - | All Departments | Master Data API | Required | Filter by department based on user role |
| 4 | ITEM-04 | Idle Type Filter | Dropdown | Enabled | - | All Types | Enum_Idle_Type | - | Filter by idle status type |
| 5 | ITEM-05 | Date Range From | Date Picker | Enabled | - | 30 days ago | - | Valid date format | Start date for idle period filter |
| 6 | ITEM-06 | Date Range To | Date Picker | Enabled | - | Today | - | Valid date format, >= From date | End date for idle period filter |
| 7 | ITEM-07 | Special Action Filter | Dropdown | Enabled | - | All Actions | Enum_Special_Actions | - | Filter by special action type |
| 8 | ITEM-08 | Apply Filters Button | Button | Enabled | - | - | - | - | Apply selected filter criteria |
| 9 | ITEM-09 | Clear Filters Button | Button | Enabled | - | - | - | - | Reset all filters to default |
| 10 | ITEM-10 | Column Manager Button | Button | Enabled | - | - | - | - | Open column visibility/order configuration |
| 11 | ITEM-11 | Export Button | Button | Enabled | - | - | - | - | Export filtered data to Excel/CSV |
| 12 | ITEM-12 | Add New Button | Button | Conditional | - | - | - | - | Create new idle resource record (role-based) |
| 13 | ITEM-13 | Batch Action Selector | Dropdown | Enabled | - | Select Action | Predefined actions | - | Select action for multiple records |
| 14 | ITEM-14 | Data Table | Table | Enabled | - | - | API Data | - | Main data table with 30+ columns |
| 15 | ITEM-15 | Select All Checkbox | Checkbox | Enabled | - | Unchecked | - | - | Select/deselect all visible records |
| 16 | ITEM-16 | Pagination Controls | Component | Enabled | - | Page 1 | - | - | Navigate between data pages |
| 17 | ITEM-17 | Records Per Page | Dropdown | Enabled | - | 25 | Fixed values | - | Number of records to display per page |
| 18 | ITEM-18 | Total Records Counter | Label | Disabled | - | Dynamic | Calculated | - | Display total number of records |
| 19 | ITEM-19 | Loading Indicator | Component | Dynamic | - | Hidden | - | - | Show during data loading operations |
| 20 | ITEM-20 | Row Action Menu | Menu | Enabled | - | - | - | - | Context menu for individual record actions |

## Events

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | EVT-01 | Screen Initialization | Load initial data and configure screen based on user role |
| 2 | EVT-02 | Search Input Change | Trigger search when user types in search field |
| 3 | EVT-03 | Filter Application | Apply selected filters to data query |
| 4 | EVT-04 | Column Configuration | Manage column visibility and ordering |
| 5 | EVT-05 | Data Export | Export filtered data to selected format |
| 6 | EVT-06 | Record Selection | Handle individual and batch record selection |
| 7 | EVT-07 | Batch Action Execution | Execute selected action on multiple records |
| 8 | EVT-08 | Row Action Selection | Handle actions on individual records |
| 9 | EVT-09 | Pagination Navigation | Handle page navigation and data loading |
| 10 | EVT-10 | Data Refresh | Refresh data based on user request or timer |

## Steps & Details

### Event ID: EVT-01
### Event Name: Screen Initialization

#### Steps:
1. **Step 1: User Authentication Check**
   - **Trigger**: Page load
   - **Description**: Verify user authentication and retrieve user role information
   - **API Call**: Authentication validation through session
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | sessionToken | HEADER.authorization | Current user session token |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | userRole | User's role (Admin, RA All, RA Dept, Manager, Viewer) |
       | departmentId | User's department ID for filtering |
       | permissions | Available permissions for current user |
     - **Callback**: Store user context and proceed to data loading

2. **Step 2: Load Column Configuration**
   - **Trigger**: User context available
   - **Description**: Retrieve user's saved column preferences
   - **API Call**: API-MDE-03-11 - Get Column Configuration
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | CONTEXT.userId | Current user identifier |
       | screenId | SCR-MDE-03-01 | Screen identifier for preferences |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | columnConfig | Column visibility and order preferences |
       | savedLayouts | User's saved layout configurations |
     - **Callback**: Apply column configuration to table

3. **Step 3: Load Initial Data**
   - **Trigger**: Column configuration loaded
   - **Description**: Load first page of idle resource data with default filters
   - **API Call**: API-MDE-03-01 - Get Idle Resource List
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | page | 1 | Initial page number |
       | pageSize | ITEM-17.value | Records per page from dropdown |
       | departmentFilter | CONTEXT.departmentId | Department filter based on role |
       | sortBy | idleFrom | Default sort field |
       | sortOrder | desc | Default sort order |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | records | Array of idle resource records |
       | totalCount | Total number of records |
       | pageInfo | Pagination information |
     - **Callback**: Populate data table and update pagination controls

4. **Step 4: Load Filter Options**
   - **Trigger**: Initial data loaded
   - **Description**: Load dropdown options for filter controls
   - **API Call**: Master Data API for filter options
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataTypes | ['departments', 'idleTypes', 'specialActions'] | Required dropdown data |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | departments | Available departments for filtering |
       | idleTypes | Available idle type options |
       | specialActions | Available special action options |
     - **Callback**: Populate filter dropdown options

5. **Final Step: Screen Ready**
   - All data loaded and screen fully functional
   - User can interact with all controls
   - Real-time search and filtering enabled

### Event ID: EVT-02
### Event Name: Search Input Change

#### Steps:
1. **Step 1: Input Validation**
   - **Trigger**: User input in search field
   - **Description**: Validate search input and apply debouncing
   - **Data Validation**: Input length between 0-100 characters, no special SQL characters

2. **Step 2: Execute Search**
   - **Trigger**: Valid input after 500ms delay
   - **Description**: Perform search across all searchable fields
   - **API Call**: API-MDE-03-07 - Search Idle Resources
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchQuery | ITEM-01.value | User input from search field |
       | departmentFilter | CONTEXT.departmentId | Department filter based on role |
       | activeFilters | SCREEN.activeFilters | Currently applied filters |
       | page | 1 | Reset to first page for new search |
       | pageSize | ITEM-17.value | Current page size setting |
     - **Response**:
       | Name | Description |
       |------|-------------|
       | searchResults | Filtered and ranked search results |
       | totalCount | Total number of matching records |
       | searchTime | Query execution time for performance monitoring |
     - **Callback**: Update data table with search results and reset pagination

3. **Final Step: Update UI**
   - Display search results in table
   - Update pagination controls
   - Show search result count

### Event ID: EVT-06
### Event Name: Record Selection

#### Steps:
1. **Step 1: Selection State Update**
   - **Trigger**: User clicks checkbox or select all
   - **Description**: Update selection state for individual or multiple records
   - **Data Validation**: Verify user has permission to select records

2. **Step 2: Update Batch Actions**
   - **Trigger**: Selection state changed
   - **Description**: Enable/disable batch action controls based on selection
   - **Callback**: Update batch action dropdown availability and button states

3. **Final Step: Visual Feedback**
   - Highlight selected rows
   - Update selection counter
   - Enable appropriate batch action options
