# API Detailed Design Document

**Document ID**: API-MDE-03-09  
**Document Name**: Advanced Search Idle Resources API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-09 |
| Document Name | Advanced Search Idle Resources API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Advanced Search Idle Resources API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-02_Search and Filter Service_v0.1 | SVE-MDE-03-02 | Search and Filter Service |
| 2 | SVE-MDE-03-13_Analytics Service_v0.1 | SVE-MDE-03-13 | Analytics Service |
| 3 | SVE-MDE-03-15_Cache Service_v0.1 | SVE-MDE-03-15 | Cache Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-09 | Advanced Search Idle Resources | Performs advanced search and filtering of idle resources with support for complex queries, full-text search, faceted search, saved searches, and real-time filtering with performance optimization. |

## Logic & Flow

### API ID: API-MDE-03-09
### API Name: Advanced Search Idle Resources
### HTTP Method: POST
### URI: /api/v1/idle-resources/search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | query | String | Optional, Max 500 chars | Free-text search query |
| 2 | filters | Object | Optional | Advanced filter criteria |
| 3 | facets | Array | Optional | Requested facet fields |
| 4 | sortBy | String | Optional, Default: updatedAt | Field to sort by |
| 5 | sortOrder | String | Optional, Default: desc | Sort order (asc/desc) |
| 6 | page | Number | Optional, Default: 1 | Page number for pagination |
| 7 | pageSize | Number | Optional, Default: 20, Max: 100 | Number of records per page |
| 8 | includeCount | Boolean | Optional, Default: true | Include total count in response |
| 9 | includeAggregations | Boolean | Optional, Default: false | Include statistical aggregations |
| 10 | searchMode | String | Optional, Default: standard | Search mode (standard/fuzzy/exact) |
| 11 | savedSearchId | String | Optional | ID of saved search to execute |
| 12 | exportFormat | String | Optional | Format for export (if requested) |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | results | Array | Array of matching idle resource records |
| 2 | totalCount | Number | Total number of matching records |
| 3 | pageInfo | Object | Pagination information |
| 4 | facets | Object | Faceted search results |
| 5 | aggregations | Object | Statistical aggregations |
| 6 | searchMetadata | Object | Search execution metadata |
| 7 | suggestedFilters | Array | Suggested additional filters |
| 8 | executionTime | Number | Search execution time in milliseconds |
| 9 | cacheInfo | Object | Cache hit/miss information |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and search permissions
   - **Data Validation**: JWT token validation and role-based permission check
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | search | Operation type |
       | resourceType | idleResource | Resource being searched |
       | searchScope | Determined from user role | Search scope limitations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | searchPermissions | Allowed search fields and filters |
       | dataScope | Data access limitations |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Load Saved Search (if applicable)**
   - **Description**: Load saved search configuration if savedSearchId provided
   - **Data Validation**: Validate saved search ID and user access
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | savedSearchId | ARGUMENT.savedSearchId | Saved search identifier |
       | userId | STEP1.userContext.userId | Current user ID |
       | validateAccess | true | Check user access to saved search |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | savedSearchConfig | Saved search configuration |
       | mergedQuery | Query merged with current request |
       | searchMetadata | Saved search metadata |
     - **Callback**: Merge saved search with current parameters if found

3. **Step 3: Parse and Validate Search Parameters**
   - **Description**: Parse and validate all search parameters
   - **Data Validation**: Validate query syntax, filter formats, and parameter ranges
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchQuery | ARGUMENT.query or STEP2.mergedQuery | Search query |
       | filterCriteria | ARGUMENT.filters | Filter criteria |
       | userPermissions | STEP1.searchPermissions | User search permissions |
       | searchMode | ARGUMENT.searchMode | Search mode |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | parsedQuery | Parsed and validated query |
       | optimizedFilters | Optimized filter criteria |
       | queryComplexity | Query complexity score |
       | estimatedResultCount | Estimated number of results |
     - **Callback**: Return 400 if invalid parameters

4. **Step 4: Check Cache for Similar Queries**
   - **Description**: Check if similar query results are cached
   - **Service Call**: SVE-MDE-03-15 - Cache Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | querySignature | Generated from query parameters | Unique query signature |
       | userContext | STEP1.userContext | User context for cache key |
       | cacheScope | search | Cache scope identifier |
       | maxAge | 300 | Maximum cache age in seconds |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | cacheHit | Boolean indicating cache hit |
       | cachedResults | Cached search results if available |
       | cacheMetadata | Cache information |
     - **Callback**: Return cached results if valid cache hit

5. **Step 5: Execute Search Query**
   - **Description**: Execute the search query against the database
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchQuery | STEP3.parsedQuery | Parsed search query |
       | filterCriteria | STEP3.optimizedFilters | Optimized filters |
       | sortOptions | Sort by and order | Sorting parameters |
       | paginationOptions | Page and page size | Pagination parameters |
       | userScope | STEP1.dataScope | Data access scope |
       | includeCount | ARGUMENT.includeCount | Count inclusion flag |
       | facetFields | ARGUMENT.facets | Requested facets |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | searchResults | Matching records |
       | totalCount | Total matching records |
       | facetResults | Faceted search results |
       | queryMetadata | Query execution metadata |
     - **Callback**: Continue to aggregations if requested

6. **Step 6: Generate Aggregations (if requested)**
   - **Description**: Generate statistical aggregations for search results
   - **Service Call**: SVE-MDE-03-13 - Analytics Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | searchResults | STEP5.searchResults | Search result set |
       | aggregationTypes | Standard aggregations | Types of aggregations to compute |
       | groupByFields | Key fields for grouping | Fields for grouping data |
       | userContext | STEP1.userContext | User context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | aggregationResults | Statistical aggregations |
       | distributionData | Data distribution information |
       | trendAnalysis | Trend analysis if applicable |
     - **Callback**: Include aggregations in response

7. **Step 7: Generate Search Suggestions**
   - **Description**: Generate suggested filters and improvements
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | currentQuery | STEP3.parsedQuery | Current search query |
       | searchResults | STEP5.searchResults | Current results |
       | userHistory | Search history | User's search patterns |
       | facetResults | STEP5.facetResults | Facet information |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | suggestedFilters | Recommended additional filters |
       | queryImprovements | Query refinement suggestions |
       | relatedSearches | Related search suggestions |
     - **Callback**: Include suggestions in response

8. **Step 8: Cache Results**
   - **Description**: Cache search results for future queries
   - **Service Call**: SVE-MDE-03-15 - Cache Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | querySignature | STEP4.querySignature | Query signature |
       | searchResults | STEP5.searchResults | Search results to cache |
       | facetResults | STEP5.facetResults | Facet results to cache |
       | userContext | STEP1.userContext | User context |
       | ttl | 300 | Time to live in seconds |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | cacheStatus | Cache storage status |
       | cacheKey | Generated cache key |
     - **Callback**: Continue to response formatting

9. **Step 9: Format Search Response**
   - **Description**: Format comprehensive search response
   - **Data Validation**: Ensure all response fields are properly formatted
   - **Callback**: Include all search results, metadata, and suggestions

10. **Final Step: Return Search Results**
    - HTTP 200 OK for successful search
    - Paginated search results
    - Faceted search information
    - Statistical aggregations (if requested)
    - Search suggestions and improvements
    - Performance and cache metadata
