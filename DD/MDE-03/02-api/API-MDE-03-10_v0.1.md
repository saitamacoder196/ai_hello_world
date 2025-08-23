# API Detailed Design Document

**Document ID**: API-MDE-03-10  
**Document Name**: Get Analytics Dashboard API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-10 |
| Document Name | Get Analytics Dashboard API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Get Analytics Dashboard API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-13_Analytics Service_v0.1 | SVE-MDE-03-13 | Analytics Service |
| 2 | SVE-MDE-03-02_Search and Filter Service_v0.1 | SVE-MDE-03-02 | Search and Filter Service |
| 3 | SVE-MDE-03-15_Cache Service_v0.1 | SVE-MDE-03-15 | Cache Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-10 | Get Analytics Dashboard | Retrieves comprehensive analytics dashboard data including idle resource statistics, trends, distributions, and key performance indicators with customizable time ranges and department filtering. |

## Logic & Flow

### API ID: API-MDE-03-10
### API Name: Get Analytics Dashboard
### HTTP Method: GET
### URI: /api/v1/idle-resources/analytics/dashboard

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | timeRange | String | Optional, Default: last30days | Time range for analytics (last7days/last30days/last90days/custom) |
| 2 | startDate | Date | Optional, Required if timeRange=custom | Start date for custom range |
| 3 | endDate | Date | Optional, Required if timeRange=custom | End date for custom range |
| 4 | departmentId | String | Optional | Filter by specific department |
| 5 | includeSubDepartments | Boolean | Optional, Default: true | Include sub-departments in analysis |
| 6 | metrics | Array | Optional | Specific metrics to include |
| 7 | groupBy | String | Optional, Default: department | Grouping dimension (department/location/jobRank) |
| 8 | refreshCache | Boolean | Optional, Default: false | Force refresh of cached analytics |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | summary | Object | High-level summary statistics |
| 2 | trends | Object | Trend analysis over time |
| 3 | distributions | Object | Data distributions by various dimensions |
| 4 | comparisons | Object | Period-over-period comparisons |
| 5 | kpis | Object | Key performance indicators |
| 6 | alerts | Array | Notable trends and anomalies |
| 7 | recommendations | Array | Data-driven recommendations |
| 8 | lastUpdated | DateTime | Last data update timestamp |
| 9 | dataFreshness | Object | Data freshness indicators |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and analytics access permissions
   - **Data Validation**: JWT token validation and role-based permission check
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | analytics | Operation type |
       | resourceType | idleResource | Resource for analytics |
       | requestedScope | ARGUMENT.departmentId | Requested data scope |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | dataScope | Allowed data access scope |
       | analyticsLevel | Level of analytics access |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Validate and Process Parameters**
   - **Description**: Validate time ranges and filter parameters
   - **Data Validation**: Check date ranges, department access, and parameter validity
   - **Callback**: Return 400 if invalid parameters or date ranges

3. **Step 3: Check Analytics Cache**
   - **Description**: Check if analytics data is available in cache
   - **Service Call**: SVE-MDE-03-15 - Cache Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | cacheKey | Generated from parameters | Analytics cache key |
       | userScope | STEP1.dataScope | User data scope |
       | maxAge | 3600 | Maximum cache age (1 hour) |
       | refreshRequested | ARGUMENT.refreshCache | Force refresh flag |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | cacheHit | Boolean indicating cache availability |
       | cachedAnalytics | Cached analytics data |
       | cacheAge | Age of cached data |
       | dataFreshness | Freshness indicators |
     - **Callback**: Return cached data if available and fresh enough

4. **Step 4: Retrieve Base Dataset**
   - **Description**: Get base dataset for analytics calculation
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | timeRange | Processed time range | Date range for data |
       | departmentFilter | ARGUMENT.departmentId | Department filtering |
       | includeSubDepts | ARGUMENT.includeSubDepartments | Sub-department inclusion |
       | userScope | STEP1.dataScope | User access scope |
       | fieldsRequired | Analytics fields | Required fields for calculations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | baseDataset | Raw data for analytics |
       | recordCount | Total records in dataset |
       | dataQuality | Data quality indicators |
     - **Callback**: Continue with analytics calculations

5. **Step 5: Calculate Summary Statistics**
   - **Description**: Calculate high-level summary statistics
   - **Service Call**: SVE-MDE-03-13 - Analytics Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataset | STEP4.baseDataset | Base data for calculations |
       | calculationType | summary | Type of calculation |
       | groupingDimension | ARGUMENT.groupBy | Grouping dimension |
       | userContext | STEP1.userContext | User context |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | summaryStats | Summary statistics |
       | totalCounts | Count aggregations |
       | distributionSummary | Basic distribution data |
     - **Callback**: Continue to trend analysis

6. **Step 6: Generate Trend Analysis**
   - **Description**: Calculate trends and time-series analytics
   - **Service Call**: SVE-MDE-03-13 - Analytics Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataset | STEP4.baseDataset | Base data for trends |
       | timeRange | Processed time range | Time range for trends |
       | trendMetrics | Key trend indicators | Metrics to trend |
       | aggregationPeriod | Auto-determined | Time aggregation period |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | trendData | Time-series trend data |
       | trendDirection | Trend directions (up/down/stable) |
       | seasonalPatterns | Seasonal pattern analysis |
       | growthRates | Period-over-period growth rates |
     - **Callback**: Continue to distribution analysis

7. **Step 7: Calculate Distributions**
   - **Description**: Calculate data distributions across various dimensions
   - **Service Call**: SVE-MDE-03-13 - Analytics Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataset | STEP4.baseDataset | Base data for distributions |
       | distributionDimensions | Key dimensions | Dimensions to analyze |
       | groupingField | ARGUMENT.groupBy | Primary grouping field |
       | includePercentages | true | Include percentage calculations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | distributionData | Distribution breakdowns |
       | topCategories | Top categories by various metrics |
       | diversityMetrics | Distribution diversity indicators |
     - **Callback**: Continue to KPI calculations

8. **Step 8: Calculate Key Performance Indicators**
   - **Description**: Calculate business KPIs and metrics
   - **Service Call**: SVE-MDE-03-13 - Analytics Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataset | STEP4.baseDataset | Base data for KPIs |
       | kpiDefinitions | Standard KPI definitions | KPI calculation rules |
       | benchmarkData | Historical benchmarks | Comparison benchmarks |
       | userRole | STEP1.userContext.role | User role for KPI filtering |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | kpiValues | Calculated KPI values |
       | kpiTrends | KPI trends over time |
       | performanceIndicators | Performance status indicators |
       | benchmarkComparisons | Comparisons against benchmarks |
     - **Callback**: Continue to alerts and recommendations

9. **Step 9: Generate Alerts and Recommendations**
   - **Description**: Generate insights, alerts, and recommendations
   - **Service Call**: SVE-MDE-03-13 - Analytics Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | analyticsResults | Combined analytics data | All calculated analytics |
       | alertThresholds | System thresholds | Alert trigger thresholds |
       | historicalContext | Historical data | Context for comparisons |
       | userRole | STEP1.userContext.role | User role for recommendations |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | alertsList | Generated alerts and warnings |
       | recommendations | Data-driven recommendations |
       | actionItems | Suggested action items |
       | priorityInsights | High-priority insights |
     - **Callback**: Compile final analytics response

10. **Step 10: Cache Analytics Results**
    - **Description**: Cache calculated analytics for future requests
    - **Service Call**: SVE-MDE-03-15 - Cache Service
      - **Arguments**:
        | Name | Value | Description |
        |------|-------|-------------|
        | cacheKey | STEP3.cacheKey | Analytics cache key |
        | analyticsData | Compiled analytics results | Complete analytics dataset |
        | userScope | STEP1.dataScope | User scope for cache |
        | ttl | 3600 | Cache time-to-live (1 hour) |
      - **Returns**:
        | Name | Description |
        |------|-------------|
        | cacheStatus | Cache storage confirmation |
        | cacheExpiry | Cache expiration time |
      - **Callback**: Continue to response formatting

11. **Step 11: Format Analytics Response**
    - **Description**: Format comprehensive analytics dashboard response
    - **Data Validation**: Ensure all response fields are properly formatted
    - **Callback**: Return complete analytics dashboard data

12. **Final Step: Return Analytics Dashboard**
    - HTTP 200 OK with complete analytics data
    - Summary statistics and KPIs
    - Trend analysis and distributions
    - Alerts and recommendations
    - Data freshness indicators
