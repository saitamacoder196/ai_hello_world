# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-05  
**Document Name**: Import/Export Operations DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-05 |
| Document Name | Import/Export Operations DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Import/Export Operations DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-05-01 | Excel Import Data Processing | Process Excel import data with validation and transformation |
| 2 | DAO-MDE-03-05-02 | Data Export Generation | Generate export data in various formats with filtering |
| 3 | DAO-MDE-03-05-03 | Import Validation and Mapping | Validate import data and handle field mapping |
| 4 | DAO-MDE-03-05-04 | Export Template Management | Manage export templates and format configurations |
| 5 | DAO-MDE-03-05-05 | Import/Export History Tracking | Track import/export operations and maintain history |

## Logic & Flow

### DAO ID: DAO-MDE-03-05-01
### DAO Name: Excel Import Data Processing

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | importData | Array | Required | Array of records from Excel import |
| 2 | importMapping | Object | Required | Field mapping configuration |
| 3 | validationRules | Object | Required | Validation rules for import data |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | importResults | Object | Import processing results |
| 2 | validRecords | Array | Successfully validated records |
| 3 | invalidRecords | Array | Records with validation errors |
| 4 | importSummary | Object | Summary of import operation |

### Steps:

1. **Step 1: Validate Import Data Structure**
   - **Description**: Validate Excel import data structure and format
   - **Data Validation**: 
     - Check import data format and column structure
     - Validate field mapping configuration
     - Ensure user has import permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Create Import Session**
   - **Description**: Create import session for tracking and rollback
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO import_sessions (session_id, user_id, import_type, status, created_at, total_records) VALUES (?, ?, 'excel_import', 'processing', NOW(), ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | session_id | Generated UUID | Unique session identifier |
       | user_id | ARGUMENT.userContext.userId | User performing import |
       | record_count | ARGUMENT.importData.length | Total records to import |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | session_created | Import session creation status |
     - **Callback**: Proceed with import processing

3. **Step 3: Process and Transform Import Data**
   - **Description**: Transform Excel data according to field mapping
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO import_staging (session_id, record_index, raw_data, transformed_data, validation_status) VALUES (unnest(?), unnest(?), unnest(?), unnest(?), 'pending')
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | session_ids | Repeated session ID | Session ID for each record |
       | record_indices | Record index array | Index of each record |
       | raw_data_array | Raw Excel data | Original Excel data |
       | transformed_data_array | Transformed data | Mapped and transformed data |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | staging_count | Number of records staged |
     - **Callback**: Continue with validation

4. **Step 4: Validate Staged Import Data**
   - **Description**: Validate staged import data against business rules
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: UPDATE import_staging SET 
       validation_status = CASE 
         WHEN (transformed_data->>'employee_id')::text IN (SELECT employee_id FROM employees) THEN 'valid'
         ELSE 'invalid'
       END,
       validation_errors = CASE 
         WHEN (transformed_data->>'employee_id')::text NOT IN (SELECT employee_id FROM employees) THEN '["Invalid employee ID"]'::jsonb
         WHEN (transformed_data->>'department_id')::text NOT IN (SELECT department_id FROM departments) THEN '["Invalid department ID"]'::jsonb
         WHEN (transformed_data->>'availability_start')::date > (transformed_data->>'availability_end')::date THEN '["Invalid date range"]'::jsonb
         ELSE NULL
       END
       WHERE session_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | session_id | Import session ID | Session ID to validate |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | validation_count | Number of records validated |
     - **Callback**: Separate valid and invalid records

5. **Step 5: Insert Valid Records into Main Table**
   - **Description**: Insert valid records into idle_resources table
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO idle_resources (resource_id, employee_id, resource_type, department_id, status, availability_start, availability_end, skills, experience_years, hourly_rate, created_by, created_at, updated_by, updated_at) 
       SELECT 
         'IMP-' || session_id || '-' || record_index,
         (transformed_data->>'employee_id')::text,
         (transformed_data->>'resource_type')::text,
         (transformed_data->>'department_id')::text,
         (transformed_data->>'status')::text,
         (transformed_data->>'availability_start')::date,
         (transformed_data->>'availability_end')::date,
         (transformed_data->>'skills')::jsonb,
         (transformed_data->>'experience_years')::integer,
         (transformed_data->>'hourly_rate')::decimal,
         ?,
         NOW(),
         ?,
         NOW()
       FROM import_staging 
       WHERE session_id = ? AND validation_status = 'valid'
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | created_by | ARGUMENT.userContext.userId | User importing data |
       | updated_by | ARGUMENT.userContext.userId | User importing data |
       | session_id | Import session ID | Session ID to process |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | imported_count | Number of records successfully imported |
     - **Callback**: Update import session status

6. **Step 6: Update Import Session Status**
   - **Description**: Update import session with final results
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: UPDATE import_sessions SET 
       status = 'completed',
       completed_at = NOW(),
       successful_records = (SELECT COUNT(*) FROM import_staging WHERE session_id = ? AND validation_status = 'valid'),
       failed_records = (SELECT COUNT(*) FROM import_staging WHERE session_id = ? AND validation_status = 'invalid'),
       error_summary = (SELECT jsonb_agg(DISTINCT validation_errors) FROM import_staging WHERE session_id = ? AND validation_status = 'invalid')
       WHERE session_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | session_id_1 | Import session ID | Session ID for success count |
       | session_id_2 | Import session ID | Session ID for failure count |
       | session_id_3 | Import session ID | Session ID for error summary |
       | session_id_4 | Import session ID | Session ID to update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | session_updated | Session update status |
     - **Callback**: Generate import results

7. **Final Step: Return Import Processing Results**
   - Return comprehensive import processing results with success/failure details

---

### DAO ID: DAO-MDE-03-05-02
### DAO Name: Data Export Generation

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | exportCriteria | Object | Required | Criteria for selecting data to export |
| 2 | exportFormat | String | Required | Export format (excel/csv/json) |
| 3 | columnSelection | Array | Optional | Specific columns to include in export |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | exportData | Array | Data formatted for export |
| 2 | exportMetadata | Object | Export metadata and statistics |
| 3 | columnHeaders | Array | Column headers for export file |

### Steps:

1. **Step 1: Validate Export Request**
   - **Description**: Validate export request and user permissions
   - **Data Validation**: 
     - Check export criteria and format validity
     - Validate column selection and user permissions
     - Ensure user has export access for requested data
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Create Export Session**
   - **Description**: Create export session for tracking and auditing
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO export_sessions (session_id, user_id, export_type, export_format, criteria, status, created_at) VALUES (?, ?, 'idle_resources', ?, ?, 'processing', NOW())
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | session_id | Generated UUID | Unique session identifier |
       | user_id | ARGUMENT.userContext.userId | User performing export |
       | export_format | ARGUMENT.exportFormat | Requested export format |
       | criteria | ARGUMENT.exportCriteria | Export criteria JSON |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | export_session_created | Export session creation status |
     - **Callback**: Proceed with data extraction

3. **Step 3: Extract Export Data with Access Control**
   - **Description**: Extract data based on criteria and user access permissions
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, e.email, d.department_name, rt.type_description, 
       CASE 
         WHEN ? = 'admin' THEN ir.hourly_rate
         WHEN ? IN ('ra_all', 'ra_dept') THEN ir.hourly_rate
         ELSE NULL
       END as filtered_hourly_rate
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       LEFT JOIN resource_types rt ON ir.resource_type = rt.type_code 
       WHERE ir.status != 'deleted' 
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_EXPORT_CRITERIA]
       ORDER BY ir.updated_at DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_role_1 | ARGUMENT.userContext.role | User role for rate visibility |
       | user_role_2 | ARGUMENT.userContext.role | User role for rate access |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role_3 | ARGUMENT.userContext.role | User role for admin access |
       | export_params | ARGUMENT.exportCriteria | Dynamic export parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | export_data | Extracted data for export |
     - **Callback**: Format data according to export format

4. **Step 4: Apply Column Selection and Formatting**
   - **Description**: Apply column selection and format data for export
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT column_name, display_name, data_type, export_format FROM export_column_config WHERE table_name = 'idle_resources' AND column_name = ANY(?) ORDER BY display_order
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | selected_columns | ARGUMENT.columnSelection | Selected columns for export |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | column_config | Column configuration for export |
     - **Callback**: Format data with proper column headers

5. **Step 5: Generate Export Statistics**
   - **Description**: Generate statistics for export metadata
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(*) as total_records,
       COUNT(DISTINCT department_id) as unique_departments,
       COUNT(DISTINCT resource_type) as unique_types,
       MIN(availability_start) as earliest_start,
       MAX(availability_end) as latest_end,
       AVG(CASE WHEN hourly_rate IS NOT NULL THEN hourly_rate END) as avg_rate
       FROM idle_resources 
       WHERE resource_id IN (SELECT resource_id FROM export_data_temp WHERE session_id = ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | export_session_id | Export session ID | Session ID for statistics |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | export_statistics | Export data statistics |
     - **Callback**: Include statistics in metadata

6. **Step 6: Update Export Session**
   - **Description**: Update export session with completion status
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: UPDATE export_sessions SET 
       status = 'completed',
       completed_at = NOW(),
       record_count = ?,
       file_size_bytes = ?
       WHERE session_id = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | record_count | Export data count | Number of exported records |
       | file_size | Estimated file size | Estimated export file size |
       | session_id | Export session ID | Session ID to update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | session_updated | Session update status |
     - **Callback**: Complete export process

7. **Final Step: Return Export Data and Metadata**
   - Return formatted export data with metadata and column headers

---

### DAO ID: DAO-MDE-03-05-03
### DAO Name: Import Validation and Mapping

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | rawImportData | Array | Required | Raw data from import source |
| 2 | mappingConfig | Object | Required | Field mapping configuration |
| 3 | validationMode | String | Optional, Default: 'strict' | Validation mode (strict/lenient) |
| 4 | userContext | Object | Required | User context for validation |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | validationResults | Object | Validation and mapping results |
| 2 | mappedData | Array | Successfully mapped data records |
| 3 | validationErrors | Array | Validation errors and issues |
| 4 | mappingStatistics | Object | Mapping success statistics |

### Steps:

1. **Step 1: Validate Mapping Configuration**
   - **Description**: Validate field mapping configuration and rules
   - **Data Validation**: 
     - Check mapping configuration format and completeness
     - Validate field mappings against database schema
     - Ensure required fields are mapped
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Validate Reference Data Integrity**
   - **Description**: Validate that referenced data exists in the database
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       e.employee_id, 
       d.department_id, 
       rt.type_code as resource_type,
       'exists' as status
       FROM (
         SELECT DISTINCT 
           unnest(?) as employee_id,
           unnest(?) as department_id,
           unnest(?) as resource_type
       ) input_refs
       LEFT JOIN employees e ON input_refs.employee_id = e.employee_id
       LEFT JOIN departments d ON input_refs.department_id = d.department_id
       LEFT JOIN resource_types rt ON input_refs.resource_type = rt.type_code
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | employee_ids | Mapped employee IDs | Array of employee IDs to validate |
       | department_ids | Mapped department IDs | Array of department IDs to validate |
       | resource_types | Mapped resource types | Array of resource types to validate |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | reference_validation | Reference data validation results |
     - **Callback**: Mark invalid references

3. **Step 3: Apply Field Mapping Rules**
   - **Description**: Apply field mapping rules and data transformations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       field_name, 
       mapping_rule, 
       data_type, 
       validation_pattern, 
       default_value 
       FROM import_field_mappings 
       WHERE mapping_set = ? AND active = true 
       ORDER BY mapping_order
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | mapping_set_name | ARGUMENT.mappingConfig.setName | Mapping configuration set |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | field_mappings | Field mapping rules |
     - **Callback**: Apply mappings to raw data

4. **Step 4: Validate Business Rules**
   - **Description**: Validate mapped data against business rules
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       validation_rule,
       rule_description,
       error_message,
       severity_level
       FROM business_validation_rules 
       WHERE rule_category = 'import_validation' 
       AND active = true 
       ORDER BY validation_order
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | No parameters needed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | business_rules | Business validation rules |
     - **Callback**: Apply business rule validation

5. **Step 5: Check for Duplicate Records**
   - **Description**: Check for duplicate records in import data and existing database
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       employee_id,
       availability_start,
       availability_end,
       COUNT(*) as duplicate_count,
       'duplicate_in_import' as issue_type
       FROM (
         SELECT 
           unnest(?) as employee_id,
           unnest(?) as availability_start,
           unnest(?) as availability_end
       ) import_data
       GROUP BY employee_id, availability_start, availability_end
       HAVING COUNT(*) > 1
       UNION ALL
       SELECT 
       ir.employee_id,
       ir.availability_start,
       ir.availability_end,
       1 as duplicate_count,
       'duplicate_in_database' as issue_type
       FROM idle_resources ir
       WHERE (ir.employee_id, ir.availability_start, ir.availability_end) IN (
         SELECT unnest(?), unnest(?), unnest(?)
       )
       AND ir.status != 'deleted'
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | emp_ids_1 | Mapped employee IDs | Employee IDs from import |
       | start_dates_1 | Mapped start dates | Start dates from import |
       | end_dates_1 | Mapped end dates | End dates from import |
       | emp_ids_2 | Mapped employee IDs | Employee IDs for DB check |
       | start_dates_2 | Mapped start dates | Start dates for DB check |
       | end_dates_2 | Mapped end dates | End dates for DB check |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | duplicate_analysis | Duplicate record analysis |
     - **Callback**: Flag duplicate records

6. **Step 6: Generate Validation Summary**
   - **Description**: Generate comprehensive validation summary and statistics
   - **Data Validation**: None
   - **Callback**: Compile validation results and mapping statistics

7. **Final Step: Return Validation and Mapping Results**
   - Return comprehensive validation results with mapped data and error details

---

### DAO ID: DAO-MDE-03-05-04
### DAO Name: Export Template Management

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | operation | String | Required | Template operation (create/update/delete/list) |
| 2 | templateData | Object | Conditional | Template data for create/update operations |
| 3 | templateId | String | Conditional | Template ID for update/delete operations |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | operationResult | Object | Template operation result |
| 2 | templateInfo | Object | Template information |
| 3 | availableTemplates | Array | List of available templates |

### Steps:

1. **Step 1: Validate Template Operation**
   - **Description**: Validate template management operation and parameters
   - **Data Validation**: 
     - Check operation type and required parameters
     - Validate template data format and structure
     - Ensure user has template management permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Execute Template Operation**
   - **Description**: Execute the requested template operation
   - **Data Validation**: Check operation type
   - **SQL Call**: 
     - **SQL**: 
       CREATE: INSERT INTO export_templates (template_id, template_name, template_type, column_config, format_config, filter_config, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, NOW())
       UPDATE: UPDATE export_templates SET template_name = ?, column_config = ?, format_config = ?, filter_config = ?, updated_by = ?, updated_at = NOW() WHERE template_id = ?
       DELETE: UPDATE export_templates SET status = 'deleted', deleted_by = ?, deleted_at = NOW() WHERE template_id = ?
       LIST: SELECT * FROM export_templates WHERE status = 'active' AND (created_by = ? OR is_public = true)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | template_params | ARGUMENT.templateData | Template data parameters |
       | user_id | ARGUMENT.userContext.userId | User performing operation |
       | template_id | ARGUMENT.templateId | Template ID for operations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | operation_result | Template operation result |
     - **Callback**: Process operation results

3. **Step 3: Validate Template Configuration**
   - **Description**: Validate template configuration for consistency
   - **Data Validation**: Check if operation is create or update
   - **SQL Call**: 
     - **SQL**: SELECT column_name FROM information_schema.columns WHERE table_name = 'idle_resources' AND column_name = ANY(?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | template_columns | Template column configuration | Columns defined in template |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | column_validation | Column existence validation |
     - **Callback**: Ensure template columns exist

4. **Final Step: Return Template Management Results**
   - Return template management results with operation status and template information

---

### DAO ID: DAO-MDE-03-05-05
### DAO Name: Import/Export History Tracking

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | operationType | String | Required | Type of operation (import/export) |
| 2 | sessionId | String | Required | Session ID for history tracking |
| 3 | historyAction | String | Required | Action to perform (create/update/query) |
| 4 | userContext | Object | Required | User context for audit trail |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | historyResults | Object | History tracking operation results |
| 2 | sessionHistory | Array | Session history records |
| 3 | operationSummary | Object | Summary of import/export operations |

### Steps:

1. **Step 1: Validate History Request**
   - **Description**: Validate history tracking request and parameters
   - **Data Validation**: 
     - Check operation type and session ID validity
     - Validate history action and user permissions
     - Ensure user has access to session history
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Query Operation History**
   - **Description**: Query import/export operation history
   - **Data Validation**: Check if history action is query
   - **SQL Call**: 
     - **SQL**: SELECT 
       ies.session_id,
       ies.user_id,
       ies.import_type as operation_type,
       ies.status,
       ies.created_at,
       ies.completed_at,
       ies.total_records,
       ies.successful_records,
       ies.failed_records,
       u.username,
       CONCAT(u.first_name, ' ', u.last_name) as user_name
       FROM import_sessions ies
       LEFT JOIN users u ON ies.user_id = u.user_id
       WHERE (ies.user_id = ? OR ? = 'admin')
       AND (? IS NULL OR ies.session_id = ?)
       UNION ALL
       SELECT 
       ees.session_id,
       ees.user_id,
       ees.export_type as operation_type,
       ees.status,
       ees.created_at,
       ees.completed_at,
       ees.record_count as total_records,
       ees.record_count as successful_records,
       0 as failed_records,
       u.username,
       CONCAT(u.first_name, ' ', u.last_name) as user_name
       FROM export_sessions ees
       LEFT JOIN users u ON ees.user_id = u.user_id
       WHERE (ees.user_id = ? OR ? = 'admin')
       AND (? IS NULL OR ees.session_id = ?)
       ORDER BY created_at DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id_1 | ARGUMENT.userContext.userId | User ID for import history |
       | user_role_1 | ARGUMENT.userContext.role | User role for admin access |
       | session_filter_1 | ARGUMENT.sessionId | Session ID filter (optional) |
       | session_id_1 | ARGUMENT.sessionId | Specific session ID |
       | user_id_2 | ARGUMENT.userContext.userId | User ID for export history |
       | user_role_2 | ARGUMENT.userContext.role | User role for admin access |
       | session_filter_2 | ARGUMENT.sessionId | Session ID filter (optional) |
       | session_id_2 | ARGUMENT.sessionId | Specific session ID |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | operation_history | Complete operation history |
     - **Callback**: Format history results

3. **Step 3: Get Detailed Session Information**
   - **Description**: Get detailed information for specific session
   - **Data Validation**: Check if session ID is provided
   - **SQL Call**: 
     - **SQL**: SELECT 
       ist.session_id,
       ist.record_index,
       ist.raw_data,
       ist.transformed_data,
       ist.validation_status,
       ist.validation_errors,
       ist.created_at
       FROM import_staging ist
       WHERE ist.session_id = ?
       ORDER BY ist.record_index
       LIMIT 100
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | session_id | ARGUMENT.sessionId | Session ID for detailed info |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | session_details | Detailed session information |
     - **Callback**: Include detailed session data

4. **Step 4: Generate Operation Summary Statistics**
   - **Description**: Generate summary statistics for import/export operations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       DATE_TRUNC('day', created_at) as operation_date,
       'import' as operation_type,
       COUNT(*) as total_operations,
       SUM(total_records) as total_records_processed,
       SUM(successful_records) as total_successful,
       SUM(failed_records) as total_failed,
       AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_processing_time
       FROM import_sessions
       WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
       AND (user_id = ? OR ? = 'admin')
       GROUP BY DATE_TRUNC('day', created_at)
       UNION ALL
       SELECT 
       DATE_TRUNC('day', created_at) as operation_date,
       'export' as operation_type,
       COUNT(*) as total_operations,
       SUM(record_count) as total_records_processed,
       SUM(record_count) as total_successful,
       0 as total_failed,
       AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_processing_time
       FROM export_sessions
       WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
       AND (user_id = ? OR ? = 'admin')
       GROUP BY DATE_TRUNC('day', created_at)
       ORDER BY operation_date DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id_1 | ARGUMENT.userContext.userId | User ID for import summary |
       | user_role_1 | ARGUMENT.userContext.role | User role for admin access |
       | user_id_2 | ARGUMENT.userContext.userId | User ID for export summary |
       | user_role_2 | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | operation_summary | Operation summary statistics |
     - **Callback**: Include summary in response

5. **Final Step: Return History Tracking Results**
   - Return comprehensive history tracking results with session details and summary statistics
