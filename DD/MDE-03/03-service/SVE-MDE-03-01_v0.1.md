# Service Detailed Design Document

**Document ID**: SVE-MDE-03-01  
**Document Name**: Idle Resource CRUD Service Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | SVE-MDE-03-01 |
| Document Name | Idle Resource CRUD Service Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Idle Resource CRUD Service design |

## Used DAOs

| No | DAO Document | DAO ID | DAO Name |
|----|--------------|--------|----------|
| 1 | DAO-MDE-03-01_Idle Resource Data Access Object_v0.1 | DAO-MDE-03-01-01 | Create Idle Resource Record |
| 2 | DAO-MDE-03-01_Idle Resource Data Access Object_v0.1 | DAO-MDE-03-01-02 | Read Idle Resource Record |
| 3 | DAO-MDE-03-01_Idle Resource Data Access Object_v0.1 | DAO-MDE-03-01-03 | Update Idle Resource Record |
| 4 | DAO-MDE-03-01_Idle Resource Data Access Object_v0.1 | DAO-MDE-03-01-04 | Delete Idle Resource Record |
| 5 | DAO-MDE-03-04_Audit Trail DAO_v0.1 | DAO-MDE-03-04-01 | Create Audit Entry |

## Services

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | SVE-MDE-03-01-01 | Create Idle Resource | Creates new idle resource record with comprehensive validation and audit trail logging |
| 2 | SVE-MDE-03-01-02 | Read Idle Resource | Retrieves idle resource record with role-based access control and data filtering |
| 3 | SVE-MDE-03-01-03 | Update Idle Resource | Updates existing idle resource record with business rule validation and change tracking |
| 4 | SVE-MDE-03-01-04 | Delete Idle Resource | Performs soft or hard delete with dependency checking and audit trail |
| 5 | SVE-MDE-03-01-05 | List Idle Resources | Retrieves paginated list of idle resources with filtering and sorting |

## Logic & Flow

### Service ID: SVE-MDE-03-01-01
### Service Name: Create Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordData | Object | Required | Complete idle resource data |
| 2 | userContext | Object | Required | User information for audit and access control |
| 3 | validationLevel | String | Optional, Default: full | Level of validation to perform |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | createdRecord | Object | Complete created record with generated ID |
| 2 | recordId | String | Generated unique identifier |
| 3 | auditTrailId | String | Audit trail entry identifier |
| 4 | validationResults | Object | Validation results and warnings |

### Steps:

1. **Step 1: Data Validation**
   - **Description**: Validate input data format and business rules
   - **Data Validation**: Check required fields, data types, and business constraints
   - **DAO Call**: None (business logic validation)
   - **Callback**: Return validation errors if data invalid

2. **Step 2: Generate Record ID**
   - **Description**: Generate unique identifier for new record
   - **Data Validation**: Ensure ID uniqueness and format
   - **Callback**: Generate UUID-based identifier

3. **Step 3: Insert Record**
   - **Description**: Insert new record into database
   - **DAO Call**: DAO-MDE-03-01-01 - Create Idle Resource Record
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordData | ARGUMENT.recordData | Complete record data |
       | recordId | STEP2.generatedId | Generated unique ID |
       | createdBy | ARGUMENT.userContext.userId | Creating user ID |
       | createdAt | CURRENT.timestamp | Creation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | insertResult | Database insert result |
       | createdRecord | Complete record with metadata |
     - **Callback**: Return error if insert fails

4. **Step 4: Create Audit Trail**
   - **Description**: Log record creation for audit purposes
   - **DAO Call**: DAO-MDE-03-04-01 - Create Audit Entry
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | STEP2.generatedId | Created record ID |
       | operation | create | Operation type |
       | userId | ARGUMENT.userContext.userId | User performing operation |
       | oldValues | null | No previous values |
       | newValues | STEP3.createdRecord | New record data |
       | timestamp | CURRENT.timestamp | Operation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditId | Generated audit trail ID |
     - **Callback**: Log audit creation failure but continue

5. **Final Step: Return Creation Results**
   - Compile complete response with created record, ID, and audit information

---

### Service ID: SVE-MDE-03-01-02
### Service Name: Read Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordId | String | Required | Unique identifier of record to retrieve |
| 2 | userContext | Object | Required | User information for access control |
| 3 | includeMetadata | Boolean | Optional, Default: false | Include record metadata |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | record | Object | Retrieved idle resource record |
| 2 | accessLevel | String | User's access level to this record |
| 3 | metadata | Object | Record metadata if requested |

### Steps:

1. **Step 1: Access Control Check**
   - **Description**: Verify user has access to requested record
   - **Data Validation**: Check user permissions and department access
   - **Callback**: Return 403 if access denied

2. **Step 2: Retrieve Record**
   - **Description**: Get record from database
   - **DAO Call**: DAO-MDE-03-01-02 - Read Idle Resource Record
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Record identifier |
       | includeDeleted | false | Exclude soft-deleted records |
       | includeMetadata | ARGUMENT.includeMetadata | Metadata inclusion flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | recordData | Retrieved record data |
       | recordMetadata | Record metadata if requested |
     - **Callback**: Return 404 if record not found

3. **Step 3: Apply Data Filtering**
   - **Description**: Filter sensitive data based on user role
   - **Data Validation**: Apply role-based field filtering
   - **Callback**: Return filtered record data

4. **Final Step: Return Record Data**
   - Compile response with record data, access level, and metadata

---

### Service ID: SVE-MDE-03-01-03
### Service Name: Update Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordId | String | Required | Unique identifier of record to update |
| 2 | updateData | Object | Required | Data fields to update |
| 3 | userContext | Object | Required | User information for audit and access control |
| 4 | version | Number | Required | Record version for optimistic locking |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | updatedRecord | Object | Complete updated record |
| 2 | auditTrailId | String | Audit trail entry identifier |
| 3 | changedFields | Array | List of fields that were modified |
| 4 | newVersion | Number | New record version number |

### Steps:

1. **Step 1: Access Control and Validation**
   - **Description**: Verify user has update access and validate input data
   - **Data Validation**: Check permissions and data validation rules
   - **Callback**: Return errors if access denied or data invalid

2. **Step 2: Retrieve Current Record**
   - **Description**: Get current record for comparison and version check
   - **DAO Call**: DAO-MDE-03-01-02 - Read Idle Resource Record
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Record identifier |
       | includeMetadata | true | Include version information |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | currentRecord | Current record state |
       | currentVersion | Current version number |
     - **Callback**: Return 404 if record not found, 409 if version conflict

3. **Step 3: Update Record**
   - **Description**: Apply updates to database record
   - **DAO Call**: DAO-MDE-03-01-03 - Update Idle Resource Record
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Record identifier |
       | updateData | ARGUMENT.updateData | Update data |
       | currentVersion | STEP2.currentVersion | Version for locking |
       | updatedBy | ARGUMENT.userContext.userId | Updating user ID |
       | updatedAt | CURRENT.timestamp | Update timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updateResult | Database update result |
       | updatedRecord | Complete updated record |
       | newVersion | New version number |
     - **Callback**: Return error if update fails

4. **Step 4: Create Audit Trail**
   - **Description**: Log record update for audit purposes
   - **DAO Call**: DAO-MDE-03-04-01 - Create Audit Entry
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Updated record ID |
       | operation | update | Operation type |
       | userId | ARGUMENT.userContext.userId | User performing operation |
       | oldValues | STEP2.currentRecord | Previous record state |
       | newValues | STEP3.updatedRecord | New record state |
       | changedFields | Calculated from comparison | Modified fields |
       | timestamp | CURRENT.timestamp | Operation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditId | Generated audit trail ID |
     - **Callback**: Continue even if audit logging fails

5. **Final Step: Return Update Results**
   - Compile response with updated record, audit ID, and change information

---

### Service ID: SVE-MDE-03-01-04
### Service Name: Delete Idle Resource

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordId | String | Required | Unique identifier of record to delete |
| 2 | userContext | Object | Required | User information for audit and access control |
| 3 | deleteType | String | Optional, Default: soft | Type of deletion (soft/hard) |
| 4 | reason | String | Optional | Reason for deletion |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | deleted | Boolean | Confirmation of successful deletion |
| 2 | deletedRecord | Object | Copy of deleted record |
| 3 | auditTrailId | String | Audit trail entry identifier |
| 4 | deletionType | String | Type of deletion performed |

### Steps:

1. **Step 1: Access Control and Validation**
   - **Description**: Verify user has delete access and check dependencies
   - **Data Validation**: Check permissions and referential integrity
   - **Callback**: Return errors if access denied or dependencies exist

2. **Step 2: Retrieve Record for Deletion**
   - **Description**: Get current record state before deletion
   - **DAO Call**: DAO-MDE-03-01-02 - Read Idle Resource Record
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Record identifier |
       | includeMetadata | true | Include full record data |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | recordToDelete | Complete record data |
     - **Callback**: Return 404 if record not found

3. **Step 3: Perform Deletion**
   - **Description**: Execute deletion operation
   - **DAO Call**: DAO-MDE-03-01-04 - Delete Idle Resource Record
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Record identifier |
       | deleteType | ARGUMENT.deleteType | Deletion type |
       | deletedBy | ARGUMENT.userContext.userId | Deleting user ID |
       | deletedAt | CURRENT.timestamp | Deletion timestamp |
       | reason | ARGUMENT.reason | Deletion reason |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | deleteResult | Database deletion result |
       | finalDeleteType | Actual deletion type performed |
     - **Callback**: Return error if deletion fails

4. **Step 4: Create Audit Trail**
   - **Description**: Log record deletion for audit purposes
   - **DAO Call**: DAO-MDE-03-04-01 - Create Audit Entry
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | recordId | ARGUMENT.recordId | Deleted record ID |
       | operation | delete | Operation type |
       | userId | ARGUMENT.userContext.userId | User performing operation |
       | oldValues | STEP2.recordToDelete | Previous record state |
       | newValues | null | No new values for deletion |
       | deletionType | STEP3.finalDeleteType | Type of deletion |
       | reason | ARGUMENT.reason | Deletion reason |
       | timestamp | CURRENT.timestamp | Operation timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | auditId | Generated audit trail ID |
     - **Callback**: Continue even if audit logging fails

5. **Final Step: Return Deletion Results**
   - Compile response with deletion confirmation, deleted record copy, and audit information

---

### Service ID: SVE-MDE-03-01-05
### Service Name: List Idle Resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | filters | Object | Optional | Filter criteria for records |
| 2 | pagination | Object | Optional | Pagination parameters |
| 3 | sorting | Object | Optional | Sorting parameters |
| 4 | userContext | Object | Required | User information for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | records | Array | Array of idle resource records |
| 2 | totalCount | Number | Total number of matching records |
| 3 | pageInfo | Object | Pagination information |
| 4 | appliedFilters | Object | Actually applied filter criteria |

### Steps:

1. **Step 1: Apply Access Control Filters**
   - **Description**: Apply role-based and department-based filtering
   - **Data Validation**: Ensure user can only access authorized data
   - **Callback**: Apply department and role-based data scope

2. **Step 2: Retrieve Record List**
   - **Description**: Get paginated list of records from database
   - **DAO Call**: DAO-MDE-03-01-02 - Read Idle Resource Record (List variant)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filters | Combined with access filters | Filter criteria |
       | pagination | ARGUMENT.pagination | Pagination parameters |
       | sorting | ARGUMENT.sorting | Sort parameters |
       | userScope | ARGUMENT.userContext | User access scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | recordList | Array of matching records |
       | totalCount | Total matching record count |
       | queryMetadata | Query execution metadata |
     - **Callback**: Return empty result if no matches

3. **Step 3: Apply Data Filtering**
   - **Description**: Filter sensitive fields based on user role
   - **Data Validation**: Apply field-level access control
   - **Callback**: Return filtered record data with pagination info

4. **Final Step: Return List Results**
   - Compile response with records, count, and pagination information
