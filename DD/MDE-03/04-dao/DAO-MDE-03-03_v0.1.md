# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-03  
**Document Name**: Bulk Operations DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-03 |
| Document Name | Bulk Operations DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Bulk Operations DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-03-01 | Bulk Create Resources | Create multiple idle resource records in single transaction |
| 2 | DAO-MDE-03-03-02 | Bulk Update Resources | Update multiple idle resource records in single transaction |
| 3 | DAO-MDE-03-03-03 | Bulk Delete Resources | Delete multiple idle resource records in single transaction |
| 4 | DAO-MDE-03-03-04 | Batch Status Update | Update status for multiple resources based on criteria |
| 5 | DAO-MDE-03-03-05 | Bulk Validation | Validate multiple resource records before bulk operations |

## Logic & Flow

### DAO ID: DAO-MDE-03-03-01
### DAO Name: Bulk Create Resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | resourceDataList | Array | Required | Array of resource data objects to create |
| 2 | batchSize | Integer | Optional, Default: 100 | Number of records to process per batch |
| 3 | continueOnError | Boolean | Optional, Default: false | Continue processing if individual record fails |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | creationResults | Object | Bulk creation operation results |
| 2 | successfulCreations | Array | Successfully created resource records |
| 3 | failedCreations | Array | Failed creation records with error details |
| 4 | operationSummary | Object | Summary statistics of bulk operation |

### Steps:

1. **Step 1: Validate Bulk Creation Request**
   - **Description**: Validate bulk creation request and resource data list
   - **Data Validation**: 
     - Check resource data list format and size limits
     - Validate batch size and processing options
     - Ensure user has bulk creation permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Begin Transaction**
   - **Description**: Begin database transaction for bulk operations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: BEGIN TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_id | Transaction identifier |
     - **Callback**: Proceed with bulk operations

3. **Step 3: Generate Resource IDs in Batch**
   - **Description**: Generate unique resource IDs for all new records
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT NEXTVAL('idle_resource_id_seq') AS next_id FROM generate_series(1, ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | record_count | ARGUMENT.resourceDataList.length | Number of records to create |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | generated_ids | Array of generated resource IDs |
     - **Callback**: Assign IDs to resource records

4. **Step 4: Execute Bulk Insert**
   - **Description**: Execute bulk insert operation using batch processing
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO idle_resources (resource_id, employee_id, resource_type, department_id, status, availability_start, availability_end, skills, experience_years, hourly_rate, created_by, created_at, updated_by, updated_at) VALUES 
       (unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), unnest(?), NOW(), unnest(?), NOW())
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_ids | Generated IDs array | Array of resource IDs |
       | employee_ids | ARGUMENT.resourceDataList[].employeeId | Array of employee IDs |
       | resource_types | ARGUMENT.resourceDataList[].resourceType | Array of resource types |
       | department_ids | ARGUMENT.resourceDataList[].departmentId | Array of department IDs |
       | statuses | ARGUMENT.resourceDataList[].status | Array of statuses |
       | start_dates | ARGUMENT.resourceDataList[].availabilityStart | Array of start dates |
       | end_dates | ARGUMENT.resourceDataList[].availabilityEnd | Array of end dates |
       | skills_data | ARGUMENT.resourceDataList[].skills | Array of skills JSON |
       | experience_values | ARGUMENT.resourceDataList[].experienceYears | Array of experience years |
       | hourly_rates | ARGUMENT.resourceDataList[].hourlyRate | Array of hourly rates |
       | created_by_list | Repeated user ID | Array of creating user IDs |
       | updated_by_list | Repeated user ID | Array of updating user IDs |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_rows | Number of successfully inserted rows |
     - **Callback**: Process insertion results

5. **Step 5: Handle Partial Failures (if continue on error enabled)**
   - **Description**: Handle partial failures and retry individual records
   - **Data Validation**: Check continue on error setting
   - **SQL Call**: 
     - **SQL**: INSERT INTO idle_resources (resource_id, employee_id, resource_type, department_id, status, availability_start, availability_end, skills, experience_years, hourly_rate, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?, NOW()) ON CONFLICT DO NOTHING
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | individual_record | Failed record data | Individual record retry |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | retry_result | Individual retry result |
     - **Callback**: Collect successful and failed records

6. **Step 6: Commit or Rollback Transaction**
   - **Description**: Commit transaction if successful, rollback if critical failures
   - **Data Validation**: Check overall operation success
   - **SQL Call**: 
     - **SQL**: COMMIT TRANSACTION (if successful) OR ROLLBACK TRANSACTION (if failed)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_status | Transaction completion status |
     - **Callback**: Finalize bulk operation

7. **Final Step: Return Bulk Creation Results**
   - Return bulk creation results with success/failure details and operation summary

---

### DAO ID: DAO-MDE-03-03-02
### DAO Name: Bulk Update Resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | updateOperations | Array | Required | Array of update operations with resource IDs and data |
| 2 | updateMode | String | Optional, Default: 'merge' | Update mode (merge/replace/patch) |
| 3 | versionCheck | Boolean | Optional, Default: true | Enable optimistic locking for updates |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | updateResults | Object | Bulk update operation results |
| 2 | successfulUpdates | Array | Successfully updated resource records |
| 3 | failedUpdates | Array | Failed update records with error details |
| 4 | versionConflicts | Array | Records with version conflicts |

### Steps:

1. **Step 1: Validate Bulk Update Request**
   - **Description**: Validate bulk update request and update operations
   - **Data Validation**: 
     - Check update operations format and data validity
     - Validate update mode and version check settings
     - Ensure user has bulk update permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Begin Transaction for Bulk Updates**
   - **Description**: Begin database transaction for bulk update operations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: BEGIN TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_id | Transaction identifier |
     - **Callback**: Proceed with bulk updates

3. **Step 3: Check Version Conflicts (if enabled)**
   - **Description**: Check for version conflicts using optimistic locking
   - **Data Validation**: Check if version check is enabled
   - **SQL Call**: 
     - **SQL**: SELECT resource_id, updated_at, version FROM idle_resources WHERE resource_id = ANY(?) FOR UPDATE
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_ids | Update operation resource IDs | Array of resource IDs to update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | current_versions | Current version information |
     - **Callback**: Compare with provided versions and identify conflicts

4. **Step 4: Execute Bulk Update Using CASE Statements**
   - **Description**: Execute bulk update using conditional CASE statements
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: UPDATE idle_resources SET 
       employee_id = CASE resource_id 
         WHEN ? THEN COALESCE(?, employee_id)
         WHEN ? THEN COALESCE(?, employee_id)
         ELSE employee_id END,
       resource_type = CASE resource_id 
         WHEN ? THEN COALESCE(?, resource_type)
         WHEN ? THEN COALESCE(?, resource_type)
         ELSE resource_type END,
       department_id = CASE resource_id 
         WHEN ? THEN COALESCE(?, department_id)
         WHEN ? THEN COALESCE(?, department_id)
         ELSE department_id END,
       status = CASE resource_id 
         WHEN ? THEN COALESCE(?, status)
         WHEN ? THEN COALESCE(?, status)
         ELSE status END,
       skills = CASE resource_id 
         WHEN ? THEN COALESCE(?, skills)
         WHEN ? THEN COALESCE(?, skills)
         ELSE skills END,
       hourly_rate = CASE resource_id 
         WHEN ? THEN COALESCE(?, hourly_rate)
         WHEN ? THEN COALESCE(?, hourly_rate)
         ELSE hourly_rate END,
       updated_by = ?,
       updated_at = NOW(),
       version = version + 1
       WHERE resource_id = ANY(?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_id_cases | Update operation resource IDs | Resource IDs for CASE conditions |
       | update_values | Update operation values | Values for each CASE condition |
       | updated_by | ARGUMENT.userContext.userId | Updating user |
       | resource_ids | Update operation resource IDs | Array of resource IDs to update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_rows | Number of successfully updated rows |
     - **Callback**: Process update results

5. **Step 5: Retrieve Updated Records**
   - **Description**: Retrieve complete updated records for response
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT * FROM idle_resources WHERE resource_id = ANY(?) ORDER BY updated_at DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | updated_ids | Successfully updated resource IDs | Resource IDs that were updated |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updated_records | Complete updated resource records |
     - **Callback**: Include in successful updates response

6. **Step 6: Handle Individual Update Failures**
   - **Description**: Handle individual update failures and collect error details
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT resource_id, 'not_found' as error_type FROM (VALUES (?)) AS requested(resource_id) WHERE resource_id NOT IN (SELECT resource_id FROM idle_resources)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | requested_ids | All requested resource IDs | Resource IDs from update operations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | failed_updates | Failed update details |
     - **Callback**: Collect failure information

7. **Step 7: Commit Transaction**
   - **Description**: Commit bulk update transaction
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: COMMIT TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_status | Transaction completion status |
     - **Callback**: Finalize bulk update operation

8. **Final Step: Return Bulk Update Results**
   - Return bulk update results with success/failure details, version conflicts, and operation summary

---

### DAO ID: DAO-MDE-03-03-03
### DAO Name: Bulk Delete Resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | resourceIds | Array | Required | Array of resource IDs to delete |
| 2 | softDelete | Boolean | Optional, Default: true | Use soft delete (mark as deleted) |
| 3 | forceDeletion | Boolean | Optional, Default: false | Force deletion despite dependencies |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | deletionResults | Object | Bulk deletion operation results |
| 2 | successfulDeletions | Array | Successfully deleted resource IDs |
| 3 | failedDeletions | Array | Failed deletion records with error details |
| 4 | dependencyBlocked | Array | Records blocked due to dependencies |

### Steps:

1. **Step 1: Validate Bulk Deletion Request**
   - **Description**: Validate bulk deletion request and resource IDs
   - **Data Validation**: 
     - Check resource IDs format and validity
     - Validate deletion options and permissions
     - Ensure user has bulk deletion permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Bulk Dependencies**
   - **Description**: Check for dependencies that prevent bulk deletion
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       ra.resource_id,
       COUNT(ra.allocation_id) as allocation_count,
       COUNT(rb.booking_id) as booking_count,
       ARRAY_AGG(DISTINCT ra.project_name) as conflicting_projects,
       ARRAY_AGG(DISTINCT rb.booking_reference) as active_bookings
       FROM resource_allocations ra 
       FULL OUTER JOIN resource_bookings rb ON ra.resource_id = rb.resource_id
       WHERE (ra.resource_id = ANY(?) OR rb.resource_id = ANY(?))
       AND (ra.status IN ('active', 'pending') OR rb.booking_date >= CURRENT_DATE)
       GROUP BY COALESCE(ra.resource_id, rb.resource_id)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_ids_1 | ARGUMENT.resourceIds | Resource IDs for allocation check |
       | resource_ids_2 | ARGUMENT.resourceIds | Resource IDs for booking check |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | dependency_analysis | Dependency analysis per resource |
     - **Callback**: Identify resources that can be safely deleted

3. **Step 3: Begin Transaction for Bulk Deletion**
   - **Description**: Begin database transaction for bulk deletion operations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: BEGIN TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_id | Transaction identifier |
     - **Callback**: Proceed with bulk deletion

4. **Step 4: Backup Records Before Deletion**
   - **Description**: Backup resource records before deletion for audit purposes
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO idle_resources_audit SELECT *, ?, NOW(), 'bulk_deleted' FROM idle_resources WHERE resource_id = ANY(?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | deleted_by | ARGUMENT.userContext.userId | User performing deletion |
       | resource_ids | ARGUMENT.resourceIds | Resource IDs to backup |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | backup_count | Number of records backed up |
     - **Callback**: Confirm backup completion

5. **Step 5: Execute Bulk Deletion**
   - **Description**: Execute bulk soft or hard deletion based on parameter
   - **Data Validation**: Check soft delete parameter
   - **SQL Call**: 
     - **SQL**: UPDATE idle_resources SET status = 'deleted', deleted_by = ?, deleted_at = NOW() WHERE resource_id = ANY(?) AND resource_id NOT IN (SELECT resource_id FROM resource_allocations WHERE status IN ('active', 'pending') UNION SELECT resource_id FROM resource_bookings WHERE booking_date >= CURRENT_DATE) (if soft delete) OR DELETE FROM idle_resources WHERE resource_id = ANY(?) AND resource_id NOT IN (...dependencies...) (if hard delete)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | deleted_by | ARGUMENT.userContext.userId | Deleting user (soft delete only) |
       | resource_ids | Deletable resource IDs | Resource IDs without dependencies |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | deleted_count | Number of successfully deleted rows |
     - **Callback**: Collect successful deletion results

6. **Step 6: Force Delete Dependencies (if force deletion enabled)**
   - **Description**: Force delete dependencies if force deletion is enabled
   - **Data Validation**: Check force deletion parameter
   - **SQL Call**: 
     - **SQL**: DELETE FROM resource_allocations WHERE resource_id = ANY(?) AND status IN ('pending', 'draft'); UPDATE resource_allocations SET status = 'cancelled' WHERE resource_id = ANY(?) AND status = 'active'; DELETE FROM resource_bookings WHERE resource_id = ANY(?) AND booking_date >= CURRENT_DATE; DELETE FROM idle_resources WHERE resource_id = ANY(?);
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | force_resource_ids | Resource IDs for force deletion | Resource IDs with dependencies |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | force_deletion_result | Force deletion results |
     - **Callback**: Include in successful deletions

7. **Step 7: Identify Failed Deletions**
   - **Description**: Identify resources that could not be deleted
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT resource_id, 'dependency_blocked' as error_type, 'Has active allocations or bookings' as error_message FROM idle_resources WHERE resource_id = ANY(?) AND status != 'deleted'
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | requested_ids | ARGUMENT.resourceIds | All requested resource IDs |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | failed_deletions | Failed deletion details |
     - **Callback**: Collect failure information

8. **Step 8: Commit Transaction**
   - **Description**: Commit bulk deletion transaction
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: COMMIT TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_status | Transaction completion status |
     - **Callback**: Finalize bulk deletion operation

9. **Final Step: Return Bulk Deletion Results**
   - Return bulk deletion results with success/failure details, dependency analysis, and operation summary

---

### DAO ID: DAO-MDE-03-03-04
### DAO Name: Batch Status Update

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | statusUpdateCriteria | Object | Required | Criteria for selecting resources to update |
| 2 | newStatus | String | Required | New status to set for matching resources |
| 3 | conditionMode | String | Optional, Default: 'AND' | Logic for combining criteria (AND/OR) |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | statusUpdateResults | Object | Batch status update operation results |
| 2 | updatedResourceIds | Array | Resource IDs that were successfully updated |
| 3 | updateSummary | Object | Summary of status changes by previous status |

### Steps:

1. **Step 1: Validate Batch Status Update**
   - **Description**: Validate batch status update criteria and parameters
   - **Data Validation**: 
     - Check status update criteria format and validity
     - Validate new status value and condition mode
     - Ensure user has batch update permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Preview Status Update Impact**
   - **Description**: Preview which resources will be affected by status update
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       ir.resource_id, 
       ir.status as current_status,
       CONCAT(e.first_name, ' ', e.last_name) as employee_name,
       d.department_name
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       WHERE ir.status != 'deleted' 
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_CRITERIA_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | criteria_params | ARGUMENT.statusUpdateCriteria | Dynamic criteria parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | affected_resources | Resources that will be affected |
     - **Callback**: Verify impact and proceed with update

3. **Step 3: Begin Transaction for Status Update**
   - **Description**: Begin database transaction for batch status update
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: BEGIN TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_id | Transaction identifier |
     - **Callback**: Proceed with status update

4. **Step 4: Execute Batch Status Update**
   - **Description**: Execute batch status update based on criteria
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: UPDATE idle_resources SET 
       status = ?,
       updated_by = ?,
       updated_at = NOW(),
       version = version + 1
       FROM (
         SELECT ir.resource_id 
         FROM idle_resources ir 
         WHERE ir.status != 'deleted' 
         AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
         [DYNAMIC_CRITERIA_CONDITIONS]
       ) AS matching_resources
       WHERE idle_resources.resource_id = matching_resources.resource_id
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | new_status | ARGUMENT.newStatus | New status value |
       | updated_by | ARGUMENT.userContext.userId | Updating user |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | criteria_params | ARGUMENT.statusUpdateCriteria | Dynamic criteria parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updated_count | Number of successfully updated rows |
     - **Callback**: Process update results

5. **Step 5: Generate Update Summary**
   - **Description**: Generate summary of status changes by previous status
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       ira.previous_status,
       COUNT(*) as change_count,
       ? as new_status,
       ARRAY_AGG(ira.resource_id) as affected_resource_ids
       FROM idle_resources_audit ira 
       WHERE ira.operation_type = 'status_update' 
       AND ira.operation_timestamp >= ?
       AND ira.updated_by = ?
       GROUP BY ira.previous_status
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | new_status | ARGUMENT.newStatus | New status value |
       | operation_start | Transaction start timestamp | Operation start time |
       | updated_by | ARGUMENT.userContext.userId | Updating user |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | status_summary | Status change summary |
     - **Callback**: Include summary in response

6. **Step 6: Commit Status Update Transaction**
   - **Description**: Commit batch status update transaction
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: COMMIT TRANSACTION
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transaction_status | Transaction completion status |
     - **Callback**: Finalize batch status update

7. **Final Step: Return Batch Status Update Results**
   - Return batch status update results with affected resources and change summary

---

### DAO ID: DAO-MDE-03-03-05
### DAO Name: Bulk Validation

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | validationDataList | Array | Required | Array of resource data to validate |
| 2 | validationRules | Object | Required | Validation rules configuration |
| 3 | validationMode | String | Optional, Default: 'strict' | Validation mode (strict/lenient) |
| 4 | userContext | Object | Required | User context for validation |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | validationResults | Object | Bulk validation operation results |
| 2 | validRecords | Array | Records that passed all validations |
| 3 | invalidRecords | Array | Records with validation errors |
| 4 | validationSummary | Object | Summary of validation results |

### Steps:

1. **Step 1: Validate Bulk Validation Request**
   - **Description**: Validate bulk validation request and parameters
   - **Data Validation**: 
     - Check validation data list format and size
     - Validate validation rules configuration
     - Ensure user has validation permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Reference Data Integrity**
   - **Description**: Check if referenced entities exist in database
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       e.employee_id, 
       d.department_id, 
       rt.type_code,
       'valid' as status
       FROM (
         SELECT DISTINCT unnest(?) as employee_id,
                unnest(?) as department_id,
                unnest(?) as resource_type
       ) input_data
       LEFT JOIN employees e ON input_data.employee_id = e.employee_id
       LEFT JOIN departments d ON input_data.department_id = d.department_id
       LEFT JOIN resource_types rt ON input_data.resource_type = rt.type_code
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | employee_ids | ARGUMENT.validationDataList[].employeeId | Array of employee IDs to validate |
       | department_ids | ARGUMENT.validationDataList[].departmentId | Array of department IDs to validate |
       | resource_types | ARGUMENT.validationDataList[].resourceType | Array of resource types to validate |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | reference_validation | Reference data validation results |
     - **Callback**: Mark records with invalid references

3. **Step 3: Check Business Rule Violations**
   - **Description**: Check for business rule violations in bulk data
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       input_data.*,
       CASE 
         WHEN input_data.availability_start >= input_data.availability_end THEN 'invalid_date_range'
         WHEN input_data.hourly_rate < 0 THEN 'negative_rate'
         WHEN input_data.experience_years < 0 THEN 'negative_experience'
         WHEN input_data.hourly_rate > ? THEN 'rate_too_high'
         ELSE 'valid'
       END as business_rule_status
       FROM (
         SELECT 
           unnest(?) as employee_id,
           unnest(?) as availability_start,
           unnest(?) as availability_end,
           unnest(?) as hourly_rate,
           unnest(?) as experience_years
       ) input_data
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | max_hourly_rate | ARGUMENT.validationRules.maxHourlyRate | Maximum allowed hourly rate |
       | employee_ids | ARGUMENT.validationDataList[].employeeId | Array of employee IDs |
       | start_dates | ARGUMENT.validationDataList[].availabilityStart | Array of start dates |
       | end_dates | ARGUMENT.validationDataList[].availabilityEnd | Array of end dates |
       | hourly_rates | ARGUMENT.validationDataList[].hourlyRate | Array of hourly rates |
       | experience_values | ARGUMENT.validationDataList[].experienceYears | Array of experience years |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | business_rule_validation | Business rule validation results |
     - **Callback**: Mark records with business rule violations

4. **Step 4: Check Data Uniqueness and Conflicts**
   - **Description**: Check for data uniqueness violations and conflicts
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       input_data.employee_id,
       input_data.availability_start,
       input_data.availability_end,
       COUNT(existing.resource_id) as conflict_count,
       ARRAY_AGG(existing.resource_id) as conflicting_resources
       FROM (
         SELECT 
           unnest(?) as employee_id,
           unnest(?) as availability_start,
           unnest(?) as availability_end
       ) input_data
       LEFT JOIN idle_resources existing ON input_data.employee_id = existing.employee_id
         AND existing.status != 'deleted'
         AND (
           (input_data.availability_start BETWEEN existing.availability_start AND existing.availability_end) OR
           (input_data.availability_end BETWEEN existing.availability_start AND existing.availability_end) OR
           (existing.availability_start BETWEEN input_data.availability_start AND input_data.availability_end)
         )
       GROUP BY input_data.employee_id, input_data.availability_start, input_data.availability_end
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | employee_ids | ARGUMENT.validationDataList[].employeeId | Array of employee IDs |
       | start_dates | ARGUMENT.validationDataList[].availabilityStart | Array of start dates |
       | end_dates | ARGUMENT.validationDataList[].availabilityEnd | Array of end dates |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | uniqueness_validation | Uniqueness and conflict validation |
     - **Callback**: Mark records with conflicts

5. **Step 5: Validate Skills and Experience Consistency**
   - **Description**: Validate skills and experience data consistency
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       input_data.*,
       CASE 
         WHEN jsonb_array_length(input_data.skills::jsonb) = 0 AND input_data.experience_years > 0 THEN 'skills_experience_mismatch'
         WHEN jsonb_array_length(input_data.skills::jsonb) > 0 AND input_data.experience_years = 0 THEN 'experience_skills_mismatch'
         WHEN NOT EXISTS (SELECT 1 FROM skill_master sm WHERE sm.skill_name = ANY(string_to_array(input_data.skills::text, ','))) THEN 'invalid_skills'
         ELSE 'valid'
       END as consistency_status
       FROM (
         SELECT 
           unnest(?) as employee_id,
           unnest(?) as skills,
           unnest(?) as experience_years
       ) input_data
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | employee_ids | ARGUMENT.validationDataList[].employeeId | Array of employee IDs |
       | skills_data | ARGUMENT.validationDataList[].skills | Array of skills JSON |
       | experience_values | ARGUMENT.validationDataList[].experienceYears | Array of experience years |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | consistency_validation | Skills and experience consistency validation |
     - **Callback**: Mark records with consistency issues

6. **Step 6: Aggregate Validation Results**
   - **Description**: Aggregate all validation results and categorize records
   - **Data Validation**: None
   - **Callback**: Combine all validation results and categorize records as valid or invalid

7. **Final Step: Return Bulk Validation Results**
   - Return comprehensive bulk validation results with valid/invalid categorization and detailed error information
