# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-01  
**Document Name**: Idle Resource CRUD DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-01 |
| Document Name | Idle Resource CRUD DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Idle Resource CRUD DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-01-01 | Create Idle Resource | Create a new idle resource record in database |
| 2 | DAO-MDE-03-01-02 | Read Idle Resource | Read idle resource record from database |
| 3 | DAO-MDE-03-01-03 | Update Idle Resource | Update existing idle resource record in database |
| 4 | DAO-MDE-03-01-04 | Delete Idle Resource | Delete idle resource record from database |
| 5 | DAO-MDE-03-01-05 | List Idle Resources | List idle resource records with filtering and pagination |

## Logic & Flow

### DAO ID: DAO-MDE-03-01-01
### DAO Name: Create Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | resourceData | Object | Required | Complete idle resource data |
| 2 | userContext | Object | Required | User context for audit trail |
| 3 | transactionId | String | Optional | Transaction ID for data consistency |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | resourceId | String | Generated idle resource ID |
| 2 | createdRecord | Object | Created idle resource record |
| 3 | operationStatus | Object | Database operation status |

### Steps:

1. **Step 1: Validate Resource Data**
   - **Description**: Validate idle resource data before database insertion
   - **Data Validation**: 
     - Check required fields and data types
     - Validate business rules and constraints
     - Ensure data integrity and consistency
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Generate Resource ID**
   - **Description**: Generate unique resource ID for new record
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT NEXTVAL('idle_resource_id_seq') AS next_id
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | next_id | Generated sequence ID |
     - **Callback**: Use generated ID for resource creation

3. **Step 3: Insert Idle Resource Record**
   - **Description**: Insert new idle resource record into database
   - **Data Validation**: None (already validated)
   - **SQL Call**: 
     - **SQL**: INSERT INTO idle_resources (resource_id, employee_id, resource_type, department_id, status, availability_start, availability_end, skills, experience_years, hourly_rate, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?, NOW())
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | Generated ID | Unique resource identifier |
       | employee_id | ARGUMENT.resourceData.employeeId | Employee reference |
       | resource_type | ARGUMENT.resourceData.resourceType | Type of resource |
       | department_id | ARGUMENT.resourceData.departmentId | Department reference |
       | status | ARGUMENT.resourceData.status | Resource status |
       | availability_start | ARGUMENT.resourceData.availabilityStart | Availability start date |
       | availability_end | ARGUMENT.resourceData.availabilityEnd | Availability end date |
       | skills | ARGUMENT.resourceData.skills | JSON skills data |
       | experience_years | ARGUMENT.resourceData.experienceYears | Years of experience |
       | hourly_rate | ARGUMENT.resourceData.hourlyRate | Hourly rate |
       | created_by | ARGUMENT.userContext.userId | Creating user |
       | updated_by | ARGUMENT.userContext.userId | Updating user |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_rows | Number of affected rows |
     - **Callback**: Confirm successful insertion

4. **Step 4: Retrieve Created Record**
   - **Description**: Retrieve the complete created record for response
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT * FROM idle_resources WHERE resource_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | Generated ID | Resource ID to retrieve |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | complete_record | Complete idle resource record |
     - **Callback**: Return complete created record

5. **Final Step: Return Creation Results**
   - Return successful creation results with resource ID and complete record

---

### DAO ID: DAO-MDE-03-01-02
### DAO Name: Read Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | resourceId | String | Required | Idle resource ID to read |
| 2 | includeDetails | Boolean | Optional, Default: true | Include detailed information |
| 3 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | resourceRecord | Object | Idle resource record |
| 2 | accessPermissions | Object | User access permissions for resource |
| 3 | operationStatus | Object | Database operation status |

### Steps:

1. **Step 1: Validate Read Request**
   - **Description**: Validate read request parameters
   - **Data Validation**: 
     - Check resource ID format and validity
     - Validate user permissions for resource access
     - Ensure resource exists and is accessible
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Read Basic Resource Data**
   - **Description**: Read basic idle resource data from database
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT * FROM idle_resources WHERE resource_id = ? AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | ARGUMENT.resourceId | Resource ID to read |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | resource_data | Basic idle resource data |
     - **Callback**: Continue with detailed data if found

3. **Step 3: Read Detailed Resource Information (if requested)**
   - **Description**: Read detailed resource information including related data
   - **Data Validation**: Check if include details is requested
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, e.email, d.department_name, rt.type_description FROM idle_resources ir LEFT JOIN employees e ON ir.employee_id = e.employee_id LEFT JOIN departments d ON ir.department_id = d.department_id LEFT JOIN resource_types rt ON ir.resource_type = rt.type_code WHERE ir.resource_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | ARGUMENT.resourceId | Resource ID to read |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | detailed_data | Detailed resource information with joins |
     - **Callback**: Merge detailed data with basic data

4. **Step 4: Check User Access Permissions**
   - **Description**: Determine user access permissions for this resource
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 'read' as permission UNION SELECT 'write' as permission WHERE ? IN ('admin', 'ra_all') OR (? = 'ra_dept' AND department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?))
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_role_1 | ARGUMENT.userContext.role | User role for admin check |
       | user_role_2 | ARGUMENT.userContext.role | User role for dept check |
       | user_id | ARGUMENT.userContext.userId | User ID for department access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | permissions | User permissions for resource |
     - **Callback**: Include permissions in response

5. **Final Step: Return Resource Data**
   - Return complete resource data with access permissions

---

### DAO ID: DAO-MDE-03-01-03
### DAO Name: Update Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | resourceId | String | Required | Idle resource ID to update |
| 2 | updateData | Object | Required | Updated resource data |
| 3 | userContext | Object | Required | User context for audit trail |
| 4 | versionCheck | Boolean | Optional, Default: true | Enable optimistic locking |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | updatedRecord | Object | Updated idle resource record |
| 2 | updateStatus | Object | Update operation status |
| 3 | conflictInfo | Object | Version conflict information if applicable |

### Steps:

1. **Step 1: Validate Update Request**
   - **Description**: Validate update request and permissions
   - **Data Validation**: 
     - Check resource ID and update data validity
     - Validate user permissions for resource update
     - Ensure resource exists and is modifiable
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Version Conflict (if enabled)**
   - **Description**: Check for version conflicts using optimistic locking
   - **Data Validation**: Compare version timestamps if version check enabled
   - **SQL Call**: 
     - **SQL**: SELECT updated_at, version FROM idle_resources WHERE resource_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | ARGUMENT.resourceId | Resource ID to check |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | current_version | Current version information |
     - **Callback**: Return conflict error if version mismatch

3. **Step 3: Update Resource Record**
   - **Description**: Update idle resource record in database
   - **Data Validation**: None (already validated)
   - **SQL Call**: 
     - **SQL**: UPDATE idle_resources SET employee_id = COALESCE(?, employee_id), resource_type = COALESCE(?, resource_type), department_id = COALESCE(?, department_id), status = COALESCE(?, status), availability_start = COALESCE(?, availability_start), availability_end = COALESCE(?, availability_end), skills = COALESCE(?, skills), experience_years = COALESCE(?, experience_years), hourly_rate = COALESCE(?, hourly_rate), updated_by = ?, updated_at = NOW(), version = version + 1 WHERE resource_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | employee_id | ARGUMENT.updateData.employeeId | Updated employee reference |
       | resource_type | ARGUMENT.updateData.resourceType | Updated resource type |
       | department_id | ARGUMENT.updateData.departmentId | Updated department |
       | status | ARGUMENT.updateData.status | Updated status |
       | availability_start | ARGUMENT.updateData.availabilityStart | Updated start date |
       | availability_end | ARGUMENT.updateData.availabilityEnd | Updated end date |
       | skills | ARGUMENT.updateData.skills | Updated skills |
       | experience_years | ARGUMENT.updateData.experienceYears | Updated experience |
       | hourly_rate | ARGUMENT.updateData.hourlyRate | Updated hourly rate |
       | updated_by | ARGUMENT.userContext.userId | Updating user |
       | resource_id | ARGUMENT.resourceId | Resource ID to update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_rows | Number of affected rows |
     - **Callback**: Confirm successful update

4. **Step 4: Retrieve Updated Record**
   - **Description**: Retrieve the complete updated record for response
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT * FROM idle_resources WHERE resource_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | ARGUMENT.resourceId | Resource ID to retrieve |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updated_record | Complete updated resource record |
     - **Callback**: Return complete updated record

5. **Final Step: Return Update Results**
   - Return successful update results with updated record and status

---

### DAO ID: DAO-MDE-03-01-04
### DAO Name: Delete Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | resourceId | String | Required | Idle resource ID to delete |
| 2 | softDelete | Boolean | Optional, Default: true | Use soft delete (mark as deleted) |
| 3 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | deletionStatus | Object | Deletion operation status |
| 2 | deletedRecord | Object | Deleted resource record (before deletion) |
| 3 | dependencyCheck | Object | Dependency check results |

### Steps:

1. **Step 1: Validate Delete Request**
   - **Description**: Validate delete request and permissions
   - **Data Validation**: 
     - Check resource ID validity
     - Validate user permissions for resource deletion
     - Ensure resource exists and is deletable
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Dependencies**
   - **Description**: Check for dependencies that prevent deletion
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as allocation_count FROM resource_allocations WHERE resource_id = ? AND status IN ('active', 'pending') UNION ALL SELECT COUNT(*) as booking_count FROM resource_bookings WHERE resource_id = ? AND booking_date >= CURRENT_DATE
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id_1 | ARGUMENT.resourceId | Resource ID for allocation check |
       | resource_id_2 | ARGUMENT.resourceId | Resource ID for booking check |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | dependency_counts | Count of dependencies |
     - **Callback**: Return dependency error if conflicts exist

3. **Step 3: Get Resource Record Before Deletion**
   - **Description**: Retrieve resource record before deletion for audit
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT * FROM idle_resources WHERE resource_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id | ARGUMENT.resourceId | Resource ID to retrieve |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | original_record | Original resource record |
     - **Callback**: Store record for response

4. **Step 4: Execute Deletion**
   - **Description**: Execute soft or hard deletion based on parameter
   - **Data Validation**: Check soft delete parameter
   - **SQL Call**: 
     - **SQL**: UPDATE idle_resources SET status = 'deleted', deleted_by = ?, deleted_at = NOW() WHERE resource_id = ? (if soft delete) OR DELETE FROM idle_resources WHERE resource_id = ? (if hard delete)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | deleted_by | ARGUMENT.userContext.userId | Deleting user (soft delete only) |
       | resource_id | ARGUMENT.resourceId | Resource ID to delete |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_rows | Number of affected rows |
     - **Callback**: Confirm successful deletion

5. **Final Step: Return Deletion Results**
   - Return successful deletion results with original record and status

---

### DAO ID: DAO-MDE-03-01-05
### DAO Name: List Idle Resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | filterCriteria | Object | Optional | Filtering criteria for list |
| 2 | sortOptions | Object | Optional | Sorting options |
| 3 | paginationInfo | Object | Required | Pagination information |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | resourceList | Array | List of idle resource records |
| 2 | totalCount | Integer | Total count of matching records |
| 3 | paginationResult | Object | Pagination result information |
| 4 | aggregateData | Object | Aggregate statistics |

### Steps:

1. **Step 1: Validate List Request**
   - **Description**: Validate list request parameters
   - **Data Validation**: 
     - Check filter criteria format and validity
     - Validate sort options and pagination parameters
     - Ensure user has list permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Build Dynamic Query**
   - **Description**: Build dynamic SQL query based on filters and user access
   - **Data Validation**: None
   - **Callback**: Construct WHERE clause based on user role and department access

3. **Step 3: Get Total Count**
   - **Description**: Get total count of matching records for pagination
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as total_count FROM idle_resources ir WHERE ir.status != 'deleted' AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin') [DYNAMIC_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | filter_params | ARGUMENT.filterCriteria | Dynamic filter parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | total_count | Total matching records |
     - **Callback**: Use count for pagination calculation

4. **Step 4: Retrieve Resource List**
   - **Description**: Retrieve paginated list of idle resources
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, d.department_name FROM idle_resources ir LEFT JOIN employees e ON ir.employee_id = e.employee_id LEFT JOIN departments d ON ir.department_id = d.department_id WHERE ir.status != 'deleted' AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin') [DYNAMIC_FILTERS] [DYNAMIC_SORTING] LIMIT ? OFFSET ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | filter_params | ARGUMENT.filterCriteria | Dynamic filter parameters |
       | limit | ARGUMENT.paginationInfo.limit | Page size limit |
       | offset | ARGUMENT.paginationInfo.offset | Page offset |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | resource_list | Paginated resource list |
     - **Callback**: Return formatted resource list

5. **Step 5: Calculate Aggregate Statistics**
   - **Description**: Calculate aggregate statistics for the filtered dataset
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as total_resources, AVG(hourly_rate) as avg_hourly_rate, COUNT(DISTINCT department_id) as department_count, COUNT(DISTINCT resource_type) as type_count FROM idle_resources WHERE status != 'deleted' [DYNAMIC_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filter_params | ARGUMENT.filterCriteria | Dynamic filter parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | aggregate_stats | Aggregate statistics |
     - **Callback**: Include statistics in response

6. **Final Step: Return List Results**
   - Return complete list results with pagination, totals, and aggregates
