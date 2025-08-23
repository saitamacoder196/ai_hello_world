# API Detailed Design Document

**Document ID**: API-MDE-03-14  
**Document Name**: Get Configuration API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-14 |
| Document Name | Get Configuration API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Get Configuration API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-08_Configuration Service_v0.1 | SVE-MDE-03-08 | Configuration Service |
| 2 | SVE-MDE-03-15_Cache Service_v0.1 | SVE-MDE-03-15 | Cache Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-14 | Get Configuration | Retrieves system configuration data including dropdown options, validation rules, business parameters, and user-specific settings for idle resource management with caching and role-based filtering. |

## Logic & Flow

### API ID: API-MDE-03-14
### API Name: Get Configuration
### HTTP Method: GET
### URI: /api/v1/idle-resources/configuration

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | configType | String | Optional | Specific configuration type (dropdowns/validation/business/user) |
| 2 | includeCache | Boolean | Optional, Default: true | Use cached configuration if available |
| 3 | language | String | Optional, Default: en | Language for localized values |
| 4 | version | String | Optional | Specific configuration version |
| 5 | departmentId | String | Optional | Department-specific configuration |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | dropdownOptions | Object | All dropdown/select options |
| 2 | validationRules | Object | Field validation rules and constraints |
| 3 | businessRules | Object | Business rule configurations |
| 4 | userSettings | Object | User-specific configuration settings |
| 5 | systemParameters | Object | System-wide parameters |
| 6 | localization | Object | Localized strings and messages |
| 7 | configVersion | String | Current configuration version |
| 8 | lastUpdated | DateTime | Configuration last update timestamp |
| 9 | cacheInfo | Object | Cache information and status |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and configuration access
   - **Data Validation**: JWT token validation and role-based permission check
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | getConfiguration | Operation type |
       | configType | ARGUMENT.configType | Requested configuration type |
       | departmentId | ARGUMENT.departmentId | Department context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | configScope | Allowed configuration access scope |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Check Configuration Cache**
   - **Description**: Check if configuration data is available in cache
   - **Data Validation**: Skip cache if includeCache is false
   - **Service Call**: SVE-MDE-03-15 - Cache Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | cacheKey | Generated from parameters | Configuration cache key |
       | userScope | STEP1.configScope | User configuration scope |
       | language | ARGUMENT.language | Requested language |
       | version | ARGUMENT.version | Specific version if requested |
       | useCache | ARGUMENT.includeCache | Cache usage flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | cacheHit | Boolean indicating cache availability |
       | cachedConfig | Cached configuration data |
       | cacheMetadata | Cache information |
       | configVersion | Cached configuration version |
     - **Callback**: Return cached data if available and current

3. **Step 3: Retrieve Dropdown Options**
   - **Description**: Get all dropdown and select options based on user scope
   - **Service Call**: SVE-MDE-03-08 - Configuration Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | configCategory | dropdowns | Configuration category |
       | userContext | STEP1.userContext | User context for filtering |
       | language | ARGUMENT.language | Language for localization |
       | departmentScope | ARGUMENT.departmentId | Department-specific options |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | dropdownData | All dropdown options |
       | localizedOptions | Localized option labels |
       | hierarchicalOptions | Parent-child relationships |
       | optionMetadata | Option metadata and descriptions |
     - **Callback**: Continue with validation rules

4. **Step 4: Retrieve Validation Rules**
   - **Description**: Get field validation rules and constraints
   - **Service Call**: SVE-MDE-03-08 - Configuration Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | configCategory | validation | Configuration category |
       | userRole | STEP1.userContext.role | User role for rule filtering |
       | configScope | STEP1.configScope | Configuration access scope |
       | language | ARGUMENT.language | Language for messages |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | validationConfig | Field validation rules |
       | errorMessages | Localized error messages |
       | constraintDefinitions | Field constraint definitions |
       | validationMetadata | Validation rule metadata |
     - **Callback**: Continue with business rules

5. **Step 5: Retrieve Business Rules Configuration**
   - **Description**: Get business rule configurations and parameters
   - **Service Call**: SVE-MDE-03-08 - Configuration Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | configCategory | businessRules | Configuration category |
       | userContext | STEP1.userContext | User context |
       | departmentScope | ARGUMENT.departmentId | Department-specific rules |
       | ruleVersion | ARGUMENT.version | Specific rule version |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | businessRuleConfig | Business rule configurations |
       | ruleParameters | Rule execution parameters |
       | ruleHierarchy | Rule priority and hierarchy |
       | ruleMetadata | Rule metadata and descriptions |
     - **Callback**: Continue with user settings

6. **Step 6: Retrieve User-Specific Settings**
   - **Description**: Get user-specific configuration and preferences
   - **Service Call**: SVE-MDE-03-08 - Configuration Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | configCategory | userSettings | Configuration category |
       | userId | STEP1.userContext.userId | Current user ID |
       | userRole | STEP1.userContext.role | User role |
       | departmentId | STEP1.userContext.departmentId | User's department |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | userConfig | User-specific settings |
       | defaultSettings | Default settings for user role |
       | preferences | User preferences |
       | accessPermissions | User access permissions |
     - **Callback**: Continue with system parameters

7. **Step 7: Retrieve System Parameters**
   - **Description**: Get system-wide parameters and global settings
   - **Service Call**: SVE-MDE-03-08 - Configuration Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | configCategory | systemParameters | Configuration category |
       | userRole | STEP1.userContext.role | User role for filtering |
       | parameterScope | STEP1.configScope | Parameter access scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | systemConfig | System-wide parameters |
       | globalSettings | Global application settings |
       | featureFlags | Feature enablement flags |
       | systemMetadata | System configuration metadata |
     - **Callback**: Continue with localization

8. **Step 8: Retrieve Localization Data**
   - **Description**: Get localized strings and messages
   - **Service Call**: SVE-MDE-03-08 - Configuration Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | configCategory | localization | Configuration category |
       | language | ARGUMENT.language | Target language |
       | userContext | STEP1.userContext | User context |
       | moduleScope | idleResourceManagement | Module scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | localizationData | Localized strings |
       | messageTemplates | Message templates |
       | dateTimeFormats | Date/time format patterns |
       | numberFormats | Number format patterns |
     - **Callback**: Continue with configuration compilation

9. **Step 9: Compile Complete Configuration**
   - **Description**: Compile all configuration components into unified response
   - **Data Validation**: Ensure all configuration data is properly formatted and complete
   - **Callback**: Continue with cache update

10. **Step 10: Update Configuration Cache**
    - **Description**: Cache the complete configuration for future requests
    - **Service Call**: SVE-MDE-03-15 - Cache Service
      - **Arguments**:
        | Name | Value | Description |
        |------|-------|-------------|
        | cacheKey | STEP2.cacheKey | Configuration cache key |
        | configData | Compiled configuration | Complete configuration data |
        | userScope | STEP1.configScope | User scope for cache |
        | ttl | 3600 | Cache time-to-live (1 hour) |
      - **Returns**:
        | Name | Description |
        |------|-------------|
        | cacheStatus | Cache update status |
        | cacheExpiry | Cache expiration time |
      - **Callback**: Continue to response formatting

11. **Step 11: Format Configuration Response**
    - **Description**: Format comprehensive configuration response
    - **Data Validation**: Ensure all configuration sections are properly included
    - **Callback**: Return complete configuration data

12. **Final Step: Return Configuration Data**
    - HTTP 200 OK with complete configuration
    - All dropdown options and validation rules
    - Business rule configurations
    - User-specific settings and preferences
    - System parameters and localization data
