# API Detailed Design Document

**Document ID**: API-MDE-03-01  
**Document Name**: Get Idle Resource List API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-01 |
| Document Name | Get Idle Resource List API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Get Idle Resource List API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-01_Idle Resource CRUD Service_v0.1 | SVE-MDE-03-01 | Idle Resource CRUD Service |
| 2 | SVE-MDE-03-08_Department Access Control Service_v0.1 | SVE-MDE-03-08 | Department Access Control Service |
| 3 | SVE-MDE-03-15_Performance Optimization Service_v0.1 | SVE-MDE-03-15 | Performance Optimization Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-01 | Get Idle Resource List | Retrieves paginated list of idle resource records with advanced filtering, sorting, and search capabilities. Supports role-based data access and customizable column selection. |

## Logic & Flow

### API ID: API-MDE-03-01
### API Name: Get Idle Resource List
### HTTP Method: GET
### URI: /api/v1/idle-resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | page | Integer | Min: 1, Default: 1 | Page number for pagination |
| 2 | pageSize | Integer | Min: 1, Max: 100, Default: 25 | Number of records per page |
| 3 | sortBy | String | Valid field names | Field to sort by (default: idleFrom) |
| 4 | sortOrder | String | 'asc' or 'desc' | Sort order (default: desc) |
| 5 | departmentId | String | Valid department ID | Filter by department |
| 6 | idleType | String | Valid idle type | Filter by idle status type |
| 7 | dateFrom | Date | ISO date format | Filter by idle start date (from) |
| 8 | dateTo | Date | ISO date format | Filter by idle start date (to) |
| 9 | specialAction | String | Valid special action | Filter by special action type |
| 10 | searchQuery | String | Max 100 characters | Global search across multiple fields |
| 11 | includeColumns | Array | Valid column names | Specific columns to return |
| 12 | urgentOnly | Boolean | true/false | Filter for urgent cases (>=2 months) |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | records | Array | Array of idle resource records |
| 2 | totalCount | Integer | Total number of records matching criteria |
| 3 | pageInfo | Object | Pagination information |
| 4 | aggregations | Object | Summary statistics and counts |
| 5 | executionTime | Integer | Query execution time in milliseconds |

### Steps:

1. **Step 1: Authentication and Authorization**
   - **Description**: Validate user authentication and determine access permissions
   - **Data Validation**: JWT token validation and role-based permission check
   - **Service Call**: SVE-MDE-03-08 - Department Access Control Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | ARGUMENT.userId | Current user ID from token |
       | requestedDepartment | ARGUMENT.departmentId | Requested department filter |
       | operation | read | Type of operation being performed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | allowedDepartments | List of departments user can access |
       | dataRestrictions | Any additional data access restrictions |
     - **Callback**: Apply department filtering based on user permissions

2. **Step 2: Input Validation and Sanitization**
   - **Description**: Validate and sanitize all input parameters
   - **Data Validation**: 
     - Page and pageSize within valid ranges
     - Sort fields are valid column names
     - Date formats are correct
     - Search query is safe from injection attacks

3. **Step 3: Build Query Criteria**
   - **Description**: Construct database query based on validated parameters
   - **Service Call**: SVE-MDE-03-01 - Idle Resource CRUD Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filterCriteria | PROCESSED.filters | Validated and processed filter criteria |
       | sortCriteria | PROCESSED.sorting | Validated sorting parameters |
       | paginationInfo | PROCESSED.pagination | Page and size information |
       | userPermissions | STEP1.permissions | User access permissions |
       | columnSelection | ARGUMENT.includeColumns | Requested columns |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | queryResults | Raw database query results |
       | totalCount | Total record count without pagination |
       | queryMetadata | Query execution metadata |
     - **Callback**: Process results for response formatting

4. **Step 4: Apply Performance Optimizations**
   - **Description**: Apply caching and optimization strategies
   - **Service Call**: SVE-MDE-03-15 - Performance Optimization Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | queryKey | GENERATED.cacheKey | Generated cache key for query |
       | queryResults | STEP3.queryResults | Query results to optimize |
       | optimizationLevel | standard | Level of optimization to apply |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | optimizedResults | Performance-optimized results |
       | cacheStatus | Cache hit/miss information |
     - **Callback**: Return optimized results

5. **Step 5: Format Response**
   - **Description**: Format results according to API specification
   - **Data Validation**: Ensure all required fields are present and properly formatted
   - **Callback**: Return formatted JSON response with proper HTTP status

6. **Final Step: Return Response**
   - Successful response with HTTP 200 and formatted data
   - Include pagination metadata and execution metrics
   - Apply any final data filtering based on user role restrictions
