# Service Detailed Design Document

**Document ID**: SVE-MDE-03-03  
**Document Name**: Idle Resource Validation Service Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | SVE-MDE-03-03 |
| Document Name | Idle Resource Validation Service Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Idle Resource Validation Service design |

## Used DAOs

| No | DAO Document | DAO ID | DAO Name |
|----|--------------|--------|----------|
| 1 | DAO-MDE-03-01_Idle Resource Data Access Object_v0.1 | DAO-MDE-03-01-02 | Read Idle Resource Record |
| 2 | DAO-MDE-03-09_Reference Data DAO_v0.1 | DAO-MDE-03-09-01 | Get Reference Data Values |
| 3 | DAO-MDE-03-09_Reference Data DAO_v0.1 | DAO-MDE-03-09-02 | Validate Enumerated Values |

## Services

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | SVE-MDE-03-03-01 | Field Validation | Validates individual field formats, types, and constraints |
| 2 | SVE-MDE-03-03-02 | Cross-Field Validation | Validates relationships and dependencies between fields |
| 3 | SVE-MDE-03-03-03 | Duplicate Detection | Checks for duplicate records based on key fields |
| 4 | SVE-MDE-03-03-04 | Business Rule Validation | Validates against complex business rules and policies |
| 5 | SVE-MDE-03-03-05 | Batch Validation | Validates multiple records efficiently with reporting |

## Logic & Flow

### Service ID: SVE-MDE-03-03-01
### Service Name: Field Validation

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | fieldData | Object | Required | Field values to validate |
| 2 | validationRules | Object | Optional | Specific validation rules to apply |
| 3 | validationContext | String | Optional, Default: standard | Validation context (create/update/import) |
| 4 | strictMode | Boolean | Optional, Default: false | Enable strict validation mode |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | isValid | Boolean | Overall field validation result |
| 2 | fieldResults | Object | Validation results for each field |
| 3 | errors | Array | Validation error messages |
| 4 | warnings | Array | Validation warning messages |
| 5 | suggestions | Array | Correction suggestions |

### Steps:

1. **Step 1: Load Validation Rules**
   - **Description**: Load field validation rules and constraints
   - **DAO Call**: DAO-MDE-03-09-01 - Get Reference Data Values
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataType | validationRules | Type of reference data |
       | context | ARGUMENT.validationContext | Validation context |
       | includeCustomRules | true | Include custom validation rules |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | validationRuleSet | Complete validation rules |
       | fieldConstraints | Field-specific constraints |
       | dataFormats | Expected data formats |
     - **Callback**: Use loaded rules for validation

2. **Step 2: Validate Required Fields**
   - **Description**: Check all required fields are present and not empty
   - **Data Validation**: Verify required field presence and basic format
   - **Callback**: Generate required field errors

3. **Step 3: Validate Data Types and Formats**
   - **Description**: Validate data types, formats, and field-specific constraints
   - **Data Validation**: Check string lengths, number ranges, date formats, etc.
   - **Callback**: Generate format and type validation errors

4. **Step 4: Validate Enumerated Values**
   - **Description**: Validate fields with enumerated values against reference data
   - **DAO Call**: DAO-MDE-03-09-02 - Validate Enumerated Values
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | fieldValues | Enumerated field values | Values to validate |
       | validationContext | ARGUMENT.validationContext | Validation context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | enumerationResults | Validation results for enum fields |
       | invalidValues | Invalid enumerated values |
       | suggestions | Suggested valid values |
     - **Callback**: Add enumeration validation results

5. **Step 5: Generate Correction Suggestions**
   - **Description**: Generate suggestions for fixing validation errors
   - **Data Validation**: Analyze errors and provide helpful suggestions
   - **Callback**: Include suggestions in validation results

6. **Final Step: Return Field Validation Results**
   - Compile comprehensive field validation results with errors, warnings, and suggestions

---

### Service ID: SVE-MDE-03-03-02
### Service Name: Cross-Field Validation

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordData | Object | Required | Complete record data for cross-field validation |
| 2 | validationContext | String | Optional, Default: standard | Validation context |
| 3 | existingRecordId | String | Optional | ID of existing record for update validation |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | isValid | Boolean | Overall cross-field validation result |
| 2 | relationshipErrors | Array | Cross-field relationship errors |
| 3 | dependencyWarnings | Array | Dependency warning messages |
| 4 | integrityResults | Object | Data integrity check results |

### Steps:

1. **Step 1: Validate Date Relationships**
   - **Description**: Validate date field relationships and logical sequences
   - **Data Validation**: Check idleFromDate <= idleToDate, logical date ranges
   - **Callback**: Generate date relationship errors

2. **Step 2: Validate Department Hierarchy**
   - **Description**: Validate department and child department relationships
   - **DAO Call**: DAO-MDE-03-09-01 - Get Reference Data Values
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataType | departmentHierarchy | Department structure data |
       | parentDepartment | ARGUMENT.recordData.departmentId | Parent department |
       | childDepartment | ARGUMENT.recordData.childDepartmentId | Child department |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | hierarchyValid | Department hierarchy validity |
       | hierarchyErrors | Hierarchy validation errors |
     - **Callback**: Add hierarchy validation results

3. **Step 3: Validate Location Consistency**
   - **Description**: Validate current location and expected working places consistency
   - **Data Validation**: Check location relationships and geographical logic
   - **Callback**: Generate location consistency warnings

4. **Step 4: Validate Skill and Experience Alignment**
   - **Description**: Validate job rank alignment with skills and experience
   - **Data Validation**: Check logical consistency between role and capabilities
   - **Callback**: Generate alignment warnings

5. **Step 5: Validate Business Logic Constraints**
   - **Description**: Apply complex business logic validations
   - **Data Validation**: Apply multi-field business rules and constraints
   - **Callback**: Generate business logic validation results

6. **Final Step: Return Cross-Field Validation Results**
   - Compile cross-field validation results with relationship errors and warnings

---

### Service ID: SVE-MDE-03-03-03
### Service Name: Duplicate Detection

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordData | Object | Required | Record data to check for duplicates |
| 2 | duplicateFields | Array | Optional, Default: ['employeeId'] | Fields to check for duplicates |
| 3 | excludeRecordId | String | Optional | Record ID to exclude from duplicate check |
| 4 | duplicateStrategy | String | Optional, Default: error | How to handle duplicates (error/warn/ignore) |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | isDuplicate | Boolean | Whether duplicates were found |
| 2 | duplicateRecords | Array | Found duplicate records |
| 3 | duplicateFields | Array | Fields that caused duplicate detection |
| 4 | duplicateStrategy | String | Applied duplicate handling strategy |

### Steps:

1. **Step 1: Prepare Duplicate Search Criteria**
   - **Description**: Prepare search criteria based on duplicate fields
   - **Data Validation**: Extract values from specified duplicate fields
   - **Callback**: Build search criteria for duplicate detection

2. **Step 2: Search for Duplicate Records**
   - **Description**: Search for existing records with matching key field values
   - **DAO Call**: DAO-MDE-03-01-02 - Read Idle Resource Record (search variant)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchCriteria | Generated criteria | Search criteria for duplicates |
       | excludeId | ARGUMENT.excludeRecordId | Record ID to exclude |
       | fieldsToMatch | ARGUMENT.duplicateFields | Fields for duplicate matching |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | matchingRecords | Records with matching field values |
       | matchDetails | Details of field matches |
     - **Callback**: Analyze matching records

3. **Step 3: Analyze Duplicate Matches**
   - **Description**: Analyze found matches to determine true duplicates
   - **Data Validation**: Compare matching records for true duplicates vs. valid similarities
   - **Callback**: Identify actual duplicate records

4. **Step 4: Apply Duplicate Strategy**
   - **Description**: Apply the specified duplicate handling strategy
   - **Data Validation**: Handle duplicates according to strategy (error/warn/ignore)
   - **Callback**: Generate appropriate response based on strategy

5. **Final Step: Return Duplicate Detection Results**
   - Return duplicate detection results with found duplicates and handling strategy

---

### Service ID: SVE-MDE-03-03-04
### Service Name: Business Rule Validation

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordData | Object | Required | Complete record data for business rule validation |
| 2 | businessRules | Array | Optional | Specific business rules to apply |
| 3 | validationContext | String | Optional | Validation context for rule selection |
| 4 | userRole | String | Optional | User role for role-specific rules |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | isValid | Boolean | Overall business rule validation result |
| 2 | ruleResults | Array | Results for each applied business rule |
| 3 | violations | Array | Business rule violations |
| 4 | calculatedFields | Object | Auto-calculated field values |
| 5 | recommendations | Array | Business rule-based recommendations |

### Steps:

1. **Step 1: Load Applicable Business Rules**
   - **Description**: Load business rules applicable to the record and context
   - **DAO Call**: DAO-MDE-03-09-01 - Get Reference Data Values
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataType | businessRules | Type of reference data |
       | context | ARGUMENT.validationContext | Validation context |
       | userRole | ARGUMENT.userRole | User role for rule filtering |
       | specificRules | ARGUMENT.businessRules | Specific rules if provided |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | applicableRules | Business rules to apply |
       | ruleParameters | Rule execution parameters |
       | ruleHierarchy | Rule priority and dependencies |
     - **Callback**: Use loaded rules for validation

2. **Step 2: Apply Mandatory Business Rules**
   - **Description**: Apply mandatory business rules that must be satisfied
   - **Data Validation**: Execute mandatory business logic validations
   - **Callback**: Generate mandatory rule violations

3. **Step 3: Apply Conditional Business Rules**
   - **Description**: Apply conditional business rules based on data values
   - **Data Validation**: Execute conditional business logic based on field values
   - **Callback**: Generate conditional rule violations

4. **Step 4: Calculate Auto-Generated Fields**
   - **Description**: Calculate field values based on business rules
   - **Data Validation**: Apply business rule calculations for auto-generated fields
   - **Callback**: Return calculated field values

5. **Step 5: Generate Business Recommendations**
   - **Description**: Generate recommendations based on business rule analysis
   - **Data Validation**: Analyze record against business rules for improvement suggestions
   - **Callback**: Provide business rule-based recommendations

6. **Final Step: Return Business Rule Validation Results**
   - Compile business rule validation results with violations, calculations, and recommendations

---

### Service ID: SVE-MDE-03-03-05
### Service Name: Batch Validation

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | recordBatch | Array | Required | Array of records to validate |
| 2 | validationLevel | String | Optional, Default: full | Level of validation (basic/full/strict) |
| 3 | batchSize | Number | Optional, Default: 100 | Processing batch size |
| 4 | continueOnError | Boolean | Optional, Default: true | Continue processing after errors |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | overallValid | Boolean | Whether entire batch is valid |
| 2 | validationSummary | Object | Summary of validation results |
| 3 | recordResults | Array | Validation results for each record |
| 4 | errorSummary | Object | Summary of errors by type |
| 5 | batchMetrics | Object | Batch processing performance metrics |

### Steps:

1. **Step 1: Initialize Batch Processing**
   - **Description**: Initialize batch validation with performance tracking
   - **Data Validation**: Validate batch parameters and size limits
   - **Callback**: Set up batch processing context

2. **Step 2: Process Records in Batches**
   - **Description**: Process records in configured batch sizes
   - **Data Validation**: Apply appropriate validation level to each record
   - **Callback**: 
     - Call field validation for each record
     - Call cross-field validation for each record
     - Call duplicate detection across batch
     - Call business rule validation for each record

3. **Step 3: Aggregate Validation Results**
   - **Description**: Aggregate individual record validation results
   - **Data Validation**: Compile validation statistics and error summaries
   - **Callback**: Generate comprehensive batch validation summary

4. **Step 4: Generate Batch Report**
   - **Description**: Generate detailed batch validation report
   - **Data Validation**: Create error analysis and recommendations
   - **Callback**: Provide batch-level insights and improvement suggestions

5. **Final Step: Return Batch Validation Results**
   - Return comprehensive batch validation results with summary and individual record details
