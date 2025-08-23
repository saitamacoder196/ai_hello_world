# API Detailed Design Document

**Document ID**: API-MDE-03-13  
**Document Name**: Validate Data API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-13 |
| Document Name | Validate Data API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Validate Data API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-03_Idle Resource Validation Service_v0.1 | SVE-MDE-03-03 | Idle Resource Validation Service |
| 2 | SVE-MDE-03-11_Business Rule Engine Service_v0.1 | SVE-MDE-03-11 | Business Rule Engine Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-13 | Validate Data | Performs comprehensive validation of idle resource data without persisting changes. Supports single record, batch validation, and business rule checking with detailed error reporting and suggestions. |

## Logic & Flow

### API ID: API-MDE-03-13
### API Name: Validate Data
### HTTP Method: POST
### URI: /api/v1/idle-resources/validate

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | data | Object or Array | Required | Single record or array of records to validate |
| 2 | validationType | String | Optional, Default: full | Type of validation (basic/full/business) |
| 3 | context | String | Optional, Default: create | Validation context (create/update/import) |
| 4 | strictMode | Boolean | Optional, Default: false | Enable strict validation mode |
| 5 | includeWarnings | Boolean | Optional, Default: true | Include validation warnings |
| 6 | checkDuplicates | Boolean | Optional, Default: true | Check for duplicates |
| 7 | businessRules | Array | Optional | Specific business rules to apply |
| 8 | existingRecordId | String | Optional | ID of existing record (for update validation) |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | isValid | Boolean | Overall validation result |
| 2 | validationResults | Array | Detailed validation results for each record |
| 3 | errorCount | Number | Total number of validation errors |
| 4 | warningCount | Number | Total number of validation warnings |
| 5 | duplicateCount | Number | Number of duplicate records found |
| 6 | businessRuleResults | Object | Business rule validation results |
| 7 | suggestions | Array | Suggested corrections and improvements |
| 8 | validationSummary | Object | Summary of validation process |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and validation permissions
   - **Data Validation**: JWT token validation and role-based permission check
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | validate | Operation type |
       | resourceType | idleResource | Resource being validated |
       | validationType | ARGUMENT.validationType | Type of validation requested |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | validationLevel | Level of validation access |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Parse and Prepare Validation Data**
   - **Description**: Parse input data and prepare for validation
   - **Data Validation**: Check data format, structure, and basic requirements
   - **Callback**: Return 400 if malformed data or invalid structure

3. **Step 3: Perform Basic Field Validation**
   - **Description**: Validate individual field formats, types, and constraints
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | inputData | ARGUMENT.data | Data to validate |
       | validationType | basic | Basic field validation |
       | context | ARGUMENT.context | Validation context |
       | strictMode | ARGUMENT.strictMode | Strict validation flag |
       | userRole | STEP1.userContext.role | User role for context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | fieldValidationResults | Field-level validation results |
       | basicErrors | Basic validation errors |
       | basicWarnings | Basic validation warnings |
       | fieldSuggestions | Field correction suggestions |
     - **Callback**: Continue with cross-field validation

4. **Step 4: Perform Cross-Field Validation**
   - **Description**: Validate relationships and dependencies between fields
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | validatedData | Data from basic validation | Previously validated data |
       | validationType | crossField | Cross-field validation type |
       | context | ARGUMENT.context | Validation context |
       | includeWarnings | ARGUMENT.includeWarnings | Warning inclusion flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | crossFieldResults | Cross-field validation results |
       | relationshipErrors | Relationship validation errors |
       | dependencyWarnings | Dependency warnings |
       | integrityChecks | Data integrity check results |
     - **Callback**: Continue with duplicate checking if requested

5. **Step 5: Check for Duplicates (if requested)**
   - **Description**: Check for duplicate records if checkDuplicates is true
   - **Data Validation**: Skip if checkDuplicates is false
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | validatedData | Data from previous validation | Validated data |
       | duplicateFields | ['employeeId'] | Fields to check for duplicates |
       | context | ARGUMENT.context | Validation context |
       | existingRecordId | ARGUMENT.existingRecordId | Existing record to exclude |
       | userScope | STEP1.userContext.dataScope | User's data access scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | duplicateResults | Duplicate detection results |
       | duplicateRecords | Found duplicate records |
       | duplicateWarnings | Duplicate-related warnings |
     - **Callback**: Continue with business rule validation

6. **Step 6: Apply Business Rules (if requested)**
   - **Description**: Apply business rules validation if validationType includes business rules
   - **Data Validation**: Check if business rule validation is requested
   - **Service Call**: SVE-MDE-03-11 - Business Rule Engine Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | validatedData | Data from previous validations | Previously validated data |
       | businessRules | ARGUMENT.businessRules or default | Rules to apply |
       | validationContext | ARGUMENT.context | Validation context |
       | userContext | STEP1.userContext | User context for rules |
       | strictMode | ARGUMENT.strictMode | Strict enforcement flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | businessRuleResults | Business rule validation results |
       | ruleViolations | Business rule violations |
       | calculatedFields | Auto-calculated field values |
       | ruleRecommendations | Rule-based recommendations |
     - **Callback**: Continue with suggestion generation

7. **Step 7: Generate Validation Suggestions**
   - **Description**: Generate suggestions for fixing validation issues
   - **Service Call**: SVE-MDE-03-03 - Idle Resource Validation Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | allValidationResults | Combined validation results | All validation outcomes |
       | userContext | STEP1.userContext | User context |
       | suggestionLevel | comprehensive | Level of suggestions |
       | autoFixAvailable | true | Include auto-fix suggestions |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | correctionSuggestions | Specific correction suggestions |
       | autoFixOptions | Auto-fixable issues |
       | bestPractices | Best practice recommendations |
       | exampleValues | Example valid values |
     - **Callback**: Continue with summary compilation

8. **Step 8: Compile Validation Summary**
   - **Description**: Compile comprehensive validation summary and statistics
   - **Data Validation**: Aggregate all validation results and statistics
   - **Callback**: Ensure all validation data is properly summarized

9. **Step 9: Format Validation Response**
   - **Description**: Format comprehensive validation response
   - **Data Validation**: Ensure response includes all required validation information
   - **Callback**: Return detailed validation results with suggestions

10. **Final Step: Return Validation Results**
    - HTTP 200 OK with validation results
    - Overall validation status (pass/fail)
    - Detailed error and warning information
    - Duplicate detection results
    - Business rule validation outcomes
    - Correction suggestions and recommendations
