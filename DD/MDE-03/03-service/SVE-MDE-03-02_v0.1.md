# Service Detailed Design Document

**Document ID**: SVE-MDE-03-02  
**Document Name**: Search and Filter Service Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | SVE-MDE-03-02 |
| Document Name | Search and Filter Service Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Search and Filter Service design |

## Used DAOs

| No | DAO Document | DAO ID | DAO Name |
|----|--------------|--------|----------|
| 1 | DAO-MDE-03-02_Idle Resource Search DAO_v0.1 | DAO-MDE-03-02-01 | Advanced Search Query |
| 2 | DAO-MDE-03-02_Idle Resource Search DAO_v0.1 | DAO-MDE-03-02-02 | Full Text Search |
| 3 | DAO-MDE-03-02_Idle Resource Search DAO_v0.1 | DAO-MDE-03-02-03 | Faceted Search |
| 4 | DAO-MDE-03-06_Department Access DAO_v0.1 | DAO-MDE-03-06-01 | Get User Department Scope |

## Services

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | SVE-MDE-03-02-01 | Advanced Search | Performs complex multi-field search with filters and sorting |
| 2 | SVE-MDE-03-02-02 | Full Text Search | Executes full-text search across searchable fields |
| 3 | SVE-MDE-03-02-03 | Faceted Search | Provides faceted search results with aggregated counts |
| 4 | SVE-MDE-03-02-04 | Apply Filters | Applies filter criteria to dataset with validation |
| 5 | SVE-MDE-03-02-05 | Saved Search Management | Manages saved search configurations and execution |

## Logic & Flow

### Service ID: SVE-MDE-03-02-01
### Service Name: Advanced Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | searchCriteria | Object | Required | Complex search criteria with multiple fields |
| 2 | filters | Object | Optional | Additional filter criteria |
| 3 | sortOptions | Object | Optional | Sorting parameters |
| 4 | pagination | Object | Optional | Pagination settings |
| 5 | userContext | Object | Required | User information for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | searchResults | Array | Array of matching records |
| 2 | totalCount | Number | Total number of matching records |
| 3 | facets | Object | Faceted search results |
| 4 | queryMetadata | Object | Search execution metadata |
| 5 | suggestions | Array | Search improvement suggestions |

### Steps:

1. **Step 1: Validate Search Criteria**
   - **Description**: Validate search parameters and user permissions
   - **Data Validation**: Check search criteria format and user access rights
   - **Callback**: Return validation errors if criteria invalid

2. **Step 2: Apply Department Access Control**
   - **Description**: Apply department-based data access restrictions
   - **DAO Call**: DAO-MDE-03-06-01 - Get User Department Scope
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | ARGUMENT.userContext.userId | Current user ID |
       | userRole | ARGUMENT.userContext.role | User role |
       | operation | search | Operation type |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | departmentScope | Allowed department access |
       | dataFilters | Required data filters |
     - **Callback**: Apply department restrictions to search

3. **Step 3: Execute Advanced Search**
   - **Description**: Perform complex search query with all criteria
   - **DAO Call**: DAO-MDE-03-02-01 - Advanced Search Query
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchCriteria | ARGUMENT.searchCriteria | Search criteria |
       | additionalFilters | Combined filters | All filter criteria |
       | departmentScope | STEP2.departmentScope | Department access scope |
       | sortOptions | ARGUMENT.sortOptions | Sorting parameters |
       | pagination | ARGUMENT.pagination | Pagination settings |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | searchResults | Matching records |
       | totalMatches | Total match count |
       | queryStats | Query execution statistics |
     - **Callback**: Return empty results if no matches

4. **Step 4: Generate Faceted Results**
   - **Description**: Generate faceted search aggregations
   - **DAO Call**: DAO-MDE-03-02-03 - Faceted Search
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchResults | STEP3.searchResults | Search result set |
       | facetFields | Standard facet fields | Fields for faceting |
       | userScope | STEP2.departmentScope | User access scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | facetResults | Faceted aggregations |
       | facetCounts | Count per facet value |
     - **Callback**: Include facets in response

5. **Step 5: Generate Search Suggestions**
   - **Description**: Provide search improvement suggestions
   - **Data Validation**: Analyze search results and criteria
   - **Callback**: Generate suggestions for query refinement

6. **Final Step: Return Search Results**
   - Compile comprehensive search response with results, facets, and metadata

---

### Service ID: SVE-MDE-03-02-02
### Service Name: Full Text Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | searchQuery | String | Required | Free-text search query |
| 2 | searchMode | String | Optional, Default: standard | Search mode (standard/fuzzy/exact) |
| 3 | filters | Object | Optional | Additional filter criteria |
| 4 | pagination | Object | Optional | Pagination settings |
| 5 | userContext | Object | Required | User information for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | searchResults | Array | Array of matching records with relevance scores |
| 2 | totalCount | Number | Total number of matching records |
| 3 | searchHighlights | Object | Search term highlights in results |
| 4 | relatedTerms | Array | Related search terms and suggestions |

### Steps:

1. **Step 1: Parse and Validate Query**
   - **Description**: Parse search query and validate search mode
   - **Data Validation**: Check query syntax and search mode validity
   - **Callback**: Return errors if query invalid

2. **Step 2: Apply Access Control**
   - **Description**: Apply user access restrictions to search scope
   - **DAO Call**: DAO-MDE-03-06-01 - Get User Department Scope
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | ARGUMENT.userContext.userId | Current user ID |
       | userRole | ARGUMENT.userContext.role | User role |
       | operation | fullTextSearch | Operation type |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | searchScope | Allowed data scope for search |
       | restrictedFields | Fields excluded from search |
     - **Callback**: Apply access restrictions

3. **Step 3: Execute Full Text Search**
   - **Description**: Perform full-text search across searchable fields
   - **DAO Call**: DAO-MDE-03-02-02 - Full Text Search
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchQuery | ARGUMENT.searchQuery | Search query string |
       | searchMode | ARGUMENT.searchMode | Search mode |
       | searchScope | STEP2.searchScope | User access scope |
       | additionalFilters | ARGUMENT.filters | Additional filters |
       | pagination | ARGUMENT.pagination | Pagination settings |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | searchResults | Matching records with scores |
       | totalMatches | Total match count |
       | searchMetadata | Search execution metadata |
       | highlights | Search term highlights |
     - **Callback**: Return results with relevance ranking

4. **Step 4: Generate Related Terms**
   - **Description**: Generate related search terms and suggestions
   - **Data Validation**: Analyze search results and query patterns
   - **Callback**: Provide search enhancement suggestions

5. **Final Step: Return Full Text Search Results**
   - Compile response with ranked results, highlights, and suggestions

---

### Service ID: SVE-MDE-03-02-03
### Service Name: Faceted Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | baseCriteria | Object | Optional | Base search criteria |
| 2 | facetFields | Array | Optional | Specific fields for faceting |
| 3 | selectedFacets | Object | Optional | Currently selected facet values |
| 4 | userContext | Object | Required | User information for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | facetResults | Object | Faceted search results with counts |
| 2 | filteredCount | Number | Count after applying selected facets |
| 3 | availableFilters | Array | Available filter options |
| 4 | facetHierarchy | Object | Hierarchical facet relationships |

### Steps:

1. **Step 1: Validate Facet Configuration**
   - **Description**: Validate facet fields and selected facets
   - **Data Validation**: Check facet field validity and user permissions
   - **Callback**: Return errors if invalid facet configuration

2. **Step 2: Apply Base Criteria and Access Control**
   - **Description**: Apply base search criteria and user access restrictions
   - **DAO Call**: DAO-MDE-03-06-01 - Get User Department Scope
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | ARGUMENT.userContext.userId | Current user ID |
       | userRole | ARGUMENT.userContext.role | User role |
       | operation | facetedSearch | Operation type |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | accessScope | User data access scope |
       | allowedFacets | Facets user can access |
     - **Callback**: Filter facet fields by user permissions

3. **Step 3: Generate Faceted Aggregations**
   - **Description**: Calculate facet counts and hierarchies
   - **DAO Call**: DAO-MDE-03-02-03 - Faceted Search
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | baseCriteria | ARGUMENT.baseCriteria | Base search criteria |
       | facetFields | Filtered facet fields | Allowed facet fields |
       | selectedFacets | ARGUMENT.selectedFacets | Selected facet values |
       | userScope | STEP2.accessScope | User access scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | facetCounts | Count for each facet value |
       | hierarchicalFacets | Parent-child facet relationships |
       | facetMetadata | Facet calculation metadata |
     - **Callback**: Return facet results with counts

4. **Step 4: Calculate Filter Impact**
   - **Description**: Calculate impact of applying each available filter
   - **Data Validation**: Analyze how filters would affect result counts
   - **Callback**: Provide filter impact information

5. **Final Step: Return Faceted Search Results**
   - Compile facet results with counts, hierarchies, and filter information

---

### Service ID: SVE-MDE-03-02-04
### Service Name: Apply Filters

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | dataset | Array | Required | Dataset to apply filters to |
| 2 | filterCriteria | Object | Required | Filter criteria to apply |
| 3 | userContext | Object | Required | User information for access control |
| 4 | filterMode | String | Optional, Default: and | Filter combination mode (and/or) |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | filteredData | Array | Dataset after applying filters |
| 2 | filterSummary | Object | Summary of applied filters |
| 3 | excludedCount | Number | Number of records excluded |
| 4 | filterPerformance | Object | Filter execution performance metrics |

### Steps:

1. **Step 1: Validate Filter Criteria**
   - **Description**: Validate filter criteria format and permissions
   - **Data Validation**: Check filter syntax and user access to filter fields
   - **Callback**: Return validation errors if filters invalid

2. **Step 2: Apply Access Control Filters**
   - **Description**: Add mandatory access control filters
   - **DAO Call**: DAO-MDE-03-06-01 - Get User Department Scope
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | ARGUMENT.userContext.userId | Current user ID |
       | userRole | ARGUMENT.userContext.role | User role |
       | operation | filter | Operation type |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | mandatoryFilters | Required access control filters |
       | fieldRestrictions | Field-level access restrictions |
     - **Callback**: Combine with user-specified filters

3. **Step 3: Execute Filter Operations**
   - **Description**: Apply all filter criteria to dataset
   - **Data Validation**: Execute filters efficiently with proper data types
   - **Callback**: Return filtered dataset with performance metrics

4. **Step 4: Generate Filter Summary**
   - **Description**: Create summary of applied filters and their impact
   - **Data Validation**: Analyze filter effectiveness and performance
   - **Callback**: Provide filter execution summary

5. **Final Step: Return Filtered Results**
   - Return filtered dataset with summary and performance information

---

### Service ID: SVE-MDE-03-02-05
### Service Name: Saved Search Management

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | operation | String | Required | Operation type (save/load/delete/list) |
| 2 | searchConfig | Object | Optional | Search configuration to save |
| 3 | searchId | String | Optional | Saved search identifier |
| 4 | searchName | String | Optional | Name for saved search |
| 5 | userContext | Object | Required | User information for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | operationResult | Boolean | Success status of operation |
| 2 | savedSearches | Array | List of user's saved searches |
| 3 | searchConfig | Object | Loaded search configuration |
| 4 | searchId | String | Generated or specified search ID |

### Steps:

1. **Step 1: Validate Operation and Parameters**
   - **Description**: Validate operation type and required parameters
   - **Data Validation**: Check operation validity and parameter completeness
   - **Callback**: Return validation errors if parameters invalid

2. **Step 2: Execute Requested Operation**
   - **Description**: Perform the requested saved search operation
   - **DAO Call**: DAO-MDE-03-05-01 - User Preferences DAO (for saved searches)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | ARGUMENT.userContext.userId | Current user ID |
       | operation | ARGUMENT.operation | Operation to perform |
       | searchConfig | ARGUMENT.searchConfig | Search configuration |
       | searchId | ARGUMENT.searchId | Search identifier |
       | searchName | ARGUMENT.searchName | Search name |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | operationResult | Operation execution result |
       | searchData | Search configuration data |
       | searchList | List of saved searches |
     - **Callback**: Return operation-specific results

3. **Final Step: Return Operation Results**
   - Return results based on operation type (saved config, search list, etc.)
