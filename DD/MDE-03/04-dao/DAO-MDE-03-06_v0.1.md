# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-06  
**Document Name**: Analytics and Reporting DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-06 |
| Document Name | Analytics and Reporting DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Analytics and Reporting DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-06-01 | Statistical Analytics | Generate statistical analytics and metrics for reporting |
| 2 | DAO-MDE-03-06-02 | Trend Analysis | Perform trend analysis and historical data comparisons |
| 3 | DAO-MDE-03-06-03 | Department Analytics | Generate department-specific analytics and metrics |
| 4 | DAO-MDE-03-06-04 | Performance Metrics | Calculate performance metrics and KPIs |
| 5 | DAO-MDE-03-06-05 | Custom Report Data | Generate data for custom reports and flexible queries |

## Logic & Flow

### DAO ID: DAO-MDE-03-06-01
### DAO Name: Statistical Analytics

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | analyticsScope | Object | Required | Scope of analytics (timeframe, filters) |
| 2 | metricsRequired | Array | Required | List of metrics to calculate |
| 3 | groupingCriteria | Object | Optional | Criteria for data grouping |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | analyticsResults | Object | Statistical analytics results |
| 2 | metricsData | Array | Calculated metrics data |
| 3 | summaryStatistics | Object | Summary statistics |

### Steps:

1. **Step 1: Validate Analytics Request**
   - **Description**: Validate statistical analytics request and parameters
   - **Data Validation**: 
     - Check analytics scope and metrics requirements
     - Validate grouping criteria and user permissions
     - Ensure user has analytics access rights
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Calculate Basic Resource Statistics**
   - **Description**: Calculate basic idle resource statistics
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(*) as total_resources,
       COUNT(CASE WHEN status = 'available' THEN 1 END) as available_count,
       COUNT(CASE WHEN status = 'partially_allocated' THEN 1 END) as partial_count,
       COUNT(CASE WHEN status = 'allocated' THEN 1 END) as allocated_count,
       COUNT(CASE WHEN status = 'unavailable' THEN 1 END) as unavailable_count,
       COUNT(DISTINCT department_id) as unique_departments,
       COUNT(DISTINCT resource_type) as unique_types,
       COUNT(DISTINCT employee_id) as unique_employees
       FROM idle_resources 
       WHERE status != 'deleted'
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_SCOPE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | scope_params | ARGUMENT.analyticsScope | Dynamic scope parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | basic_statistics | Basic resource statistics |
     - **Callback**: Include in analytics results

3. **Step 3: Calculate Duration and Time-based Analytics**
   - **Description**: Calculate duration and time-based analytics
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       AVG(availability_end - availability_start) as avg_availability_duration,
       MIN(availability_end - availability_start) as min_duration,
       MAX(availability_end - availability_start) as max_duration,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY availability_end - availability_start) as median_duration,
       COUNT(CASE WHEN availability_end - availability_start > INTERVAL '60 days' THEN 1 END) as long_term_count,
       COUNT(CASE WHEN availability_start <= CURRENT_DATE AND availability_end >= CURRENT_DATE THEN 1 END) as currently_available,
       COUNT(CASE WHEN availability_start > CURRENT_DATE THEN 1 END) as future_available,
       COUNT(CASE WHEN availability_end < CURRENT_DATE THEN 1 END) as past_available
       FROM idle_resources 
       WHERE status != 'deleted'
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_SCOPE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | scope_params | ARGUMENT.analyticsScope | Dynamic scope parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | duration_analytics | Duration-based analytics |
     - **Callback**: Include in analytics results

4. **Step 4: Calculate Skill and Experience Analytics**
   - **Description**: Calculate skill and experience-related analytics
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       AVG(experience_years) as avg_experience,
       MIN(experience_years) as min_experience,
       MAX(experience_years) as max_experience,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY experience_years) as median_experience,
       COUNT(CASE WHEN experience_years < 2 THEN 1 END) as junior_count,
       COUNT(CASE WHEN experience_years BETWEEN 2 AND 5 THEN 1 END) as mid_count,
       COUNT(CASE WHEN experience_years > 5 THEN 1 END) as senior_count,
       COUNT(DISTINCT jsonb_array_elements_text(skills)) as unique_skills,
       MODE() WITHIN GROUP (ORDER BY jsonb_array_length(skills)) as common_skill_count
       FROM idle_resources 
       WHERE status != 'deleted'
       AND skills IS NOT NULL
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_SCOPE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | scope_params | ARGUMENT.analyticsScope | Dynamic scope parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | skill_analytics | Skill and experience analytics |
     - **Callback**: Include in analytics results

5. **Step 5: Calculate Rate and Cost Analytics**
   - **Description**: Calculate hourly rate and cost analytics
   - **Data Validation**: Check user permissions for rate data
   - **SQL Call**: 
     - **SQL**: SELECT 
       CASE 
         WHEN ? IN ('admin', 'ra_all') THEN AVG(hourly_rate)
         ELSE NULL
       END as avg_hourly_rate,
       CASE 
         WHEN ? IN ('admin', 'ra_all') THEN MIN(hourly_rate)
         ELSE NULL
       END as min_hourly_rate,
       CASE 
         WHEN ? IN ('admin', 'ra_all') THEN MAX(hourly_rate)
         ELSE NULL
       END as max_hourly_rate,
       CASE 
         WHEN ? IN ('admin', 'ra_all') THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY hourly_rate)
         ELSE NULL
       END as median_hourly_rate,
       COUNT(CASE WHEN hourly_rate IS NOT NULL THEN 1 END) as resources_with_rates
       FROM idle_resources 
       WHERE status != 'deleted'
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_SCOPE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_role_1 | ARGUMENT.userContext.role | User role for rate access |
       | user_role_2 | ARGUMENT.userContext.role | User role for rate access |
       | user_role_3 | ARGUMENT.userContext.role | User role for rate access |
       | user_role_4 | ARGUMENT.userContext.role | User role for rate access |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role_5 | ARGUMENT.userContext.role | User role for admin access |
       | scope_params | ARGUMENT.analyticsScope | Dynamic scope parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | rate_analytics | Rate and cost analytics |
     - **Callback**: Include in analytics results if user has permissions

6. **Final Step: Return Statistical Analytics Results**
   - Return comprehensive statistical analytics with all calculated metrics

---

### DAO ID: DAO-MDE-03-06-02
### DAO Name: Trend Analysis

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | timeSeriesConfig | Object | Required | Time series configuration for trend analysis |
| 2 | trendMetrics | Array | Required | Metrics to analyze for trends |
| 3 | comparisonPeriods | Object | Optional | Periods for comparison analysis |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | trendResults | Object | Trend analysis results |
| 2 | timeSeriesData | Array | Time series data points |
| 3 | trendSummary | Object | Trend summary and insights |

### Steps:

1. **Step 1: Validate Trend Analysis Request**
   - **Description**: Validate trend analysis request and parameters
   - **Data Validation**: 
     - Check time series configuration and trend metrics
     - Validate comparison periods and user permissions
     - Ensure sufficient data for trend analysis
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Generate Time Series Data**
   - **Description**: Generate time series data for trend analysis
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       DATE_TRUNC(?, created_at) as time_period,
       COUNT(*) as total_resources,
       COUNT(CASE WHEN status = 'available' THEN 1 END) as available_resources,
       COUNT(CASE WHEN status = 'allocated' THEN 1 END) as allocated_resources,
       AVG(experience_years) as avg_experience,
       COUNT(DISTINCT department_id) as active_departments
       FROM idle_resources 
       WHERE status != 'deleted'
       AND created_at BETWEEN ? AND ?
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       GROUP BY DATE_TRUNC(?, created_at)
       ORDER BY time_period
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | time_granularity_1 | ARGUMENT.timeSeriesConfig.granularity | Time grouping granularity |
       | start_date | ARGUMENT.timeSeriesConfig.startDate | Analysis start date |
       | end_date | ARGUMENT.timeSeriesConfig.endDate | Analysis end date |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | time_granularity_2 | ARGUMENT.timeSeriesConfig.granularity | Time grouping granularity |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | time_series_data | Time series data points |
     - **Callback**: Use for trend calculation

3. **Step 3: Calculate Trend Indicators**
   - **Description**: Calculate trend indicators and growth rates
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: WITH trend_data AS (
       SELECT 
         time_period,
         total_resources,
         LAG(total_resources) OVER (ORDER BY time_period) as prev_total,
         available_resources,
         LAG(available_resources) OVER (ORDER BY time_period) as prev_available
       FROM time_series_temp 
       ORDER BY time_period
       )
       SELECT 
         time_period,
         total_resources,
         CASE 
           WHEN prev_total > 0 THEN ((total_resources - prev_total) * 100.0 / prev_total)
           ELSE NULL
         END as total_growth_rate,
         available_resources,
         CASE 
           WHEN prev_available > 0 THEN ((available_resources - prev_available) * 100.0 / prev_available)
           ELSE NULL
         END as availability_growth_rate
       FROM trend_data
       ORDER BY time_period
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | Uses temporary table from previous step |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | trend_indicators | Trend indicators and growth rates |
     - **Callback**: Include in trend analysis

4. **Step 4: Perform Seasonal Analysis**
   - **Description**: Perform seasonal analysis on idle resource data
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       EXTRACT(MONTH FROM created_at) as month_number,
       TO_CHAR(created_at, 'Month') as month_name,
       COUNT(*) as monthly_resources,
       AVG(COUNT(*)) OVER () as overall_avg,
       (COUNT(*) - AVG(COUNT(*)) OVER ()) / STDDEV(COUNT(*)) OVER () as seasonal_index
       FROM idle_resources 
       WHERE status != 'deleted'
       AND created_at BETWEEN ? AND ?
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       GROUP BY EXTRACT(MONTH FROM created_at), TO_CHAR(created_at, 'Month')
       ORDER BY month_number
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | analysis_start | ARGUMENT.timeSeriesConfig.startDate | Analysis start date |
       | analysis_end | ARGUMENT.timeSeriesConfig.endDate | Analysis end date |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | seasonal_analysis | Seasonal analysis results |
     - **Callback**: Include in trend summary

5. **Step 5: Calculate Correlation Analysis**
   - **Description**: Calculate correlations between different metrics
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       CORR(total_resources, avg_experience) as resources_experience_corr,
       CORR(available_resources, active_departments) as availability_departments_corr,
       CORR(total_resources, EXTRACT(MONTH FROM time_period)) as resources_seasonality_corr
       FROM time_series_temp
       WHERE total_resources IS NOT NULL 
       AND avg_experience IS NOT NULL
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | Uses temporary table from previous steps |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | correlation_analysis | Correlation analysis results |
     - **Callback**: Include in trend summary

6. **Final Step: Return Trend Analysis Results**
   - Return comprehensive trend analysis with time series data and insights

---

### DAO ID: DAO-MDE-03-06-03
### DAO Name: Department Analytics

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | departmentScope | Object | Required | Department scope for analytics |
| 2 | comparisonMode | String | Optional, Default: 'all' | Comparison mode (all/selected/hierarchical) |
| 3 | metricsLevel | String | Optional, Default: 'summary' | Level of metrics detail |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | departmentResults | Object | Department analytics results |
| 2 | departmentComparison | Array | Department comparison data |
| 3 | hierarchyAnalysis | Object | Department hierarchy analysis |

### Steps:

1. **Step 1: Validate Department Analytics Request**
   - **Description**: Validate department analytics request and scope
   - **Data Validation**: 
     - Check department scope and user access permissions
     - Validate comparison mode and metrics level
     - Ensure user has access to requested departments
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Generate Department Resource Summary**
   - **Description**: Generate resource summary by department
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       d.department_id,
       d.department_name,
       d.parent_department_id,
       COUNT(ir.resource_id) as total_resources,
       COUNT(CASE WHEN ir.status = 'available' THEN 1 END) as available_resources,
       COUNT(CASE WHEN ir.status = 'partially_allocated' THEN 1 END) as partial_resources,
       COUNT(CASE WHEN ir.status = 'allocated' THEN 1 END) as allocated_resources,
       COUNT(DISTINCT ir.employee_id) as unique_employees,
       COUNT(DISTINCT ir.resource_type) as resource_types,
       AVG(ir.experience_years) as avg_experience,
       MIN(ir.availability_start) as earliest_availability,
       MAX(ir.availability_end) as latest_availability
       FROM departments d
       LEFT JOIN idle_resources ir ON d.department_id = ir.department_id AND ir.status != 'deleted'
       WHERE (d.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_DEPARTMENT_FILTERS]
       GROUP BY d.department_id, d.department_name, d.parent_department_id
       ORDER BY d.department_name
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | dept_filters | ARGUMENT.departmentScope | Dynamic department filters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | department_summary | Department resource summary |
     - **Callback**: Use for comparison analysis

3. **Step 3: Calculate Department Performance Metrics**
   - **Description**: Calculate performance metrics for each department
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       department_id,
       department_name,
       total_resources,
       available_resources,
       CASE 
         WHEN total_resources > 0 THEN (available_resources * 100.0 / total_resources)
         ELSE 0
       END as availability_percentage,
       CASE 
         WHEN total_resources > 0 THEN (allocated_resources * 100.0 / total_resources)
         ELSE 0
       END as allocation_percentage,
       avg_experience,
       resource_types,
       DENSE_RANK() OVER (ORDER BY total_resources DESC) as resource_count_rank,
       DENSE_RANK() OVER (ORDER BY availability_percentage DESC) as availability_rank,
       DENSE_RANK() OVER (ORDER BY avg_experience DESC) as experience_rank
       FROM department_summary_temp
       ORDER BY total_resources DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | Uses temporary table from previous step |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | department_metrics | Department performance metrics |
     - **Callback**: Include in comparison results

4. **Step 4: Analyze Department Hierarchy**
   - **Description**: Analyze department hierarchy and rollup metrics
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: WITH RECURSIVE dept_hierarchy AS (
       SELECT 
         department_id,
         department_name,
         parent_department_id,
         1 as level,
         department_id::text as path
       FROM departments 
       WHERE parent_department_id IS NULL
       UNION ALL
       SELECT 
         d.department_id,
         d.department_name,
         d.parent_department_id,
         dh.level + 1,
         dh.path || '>' || d.department_id
       FROM departments d
       INNER JOIN dept_hierarchy dh ON d.parent_department_id = dh.department_id
       )
       SELECT 
         dh.*,
         COALESCE(ds.total_resources, 0) as direct_resources,
         COALESCE(SUM(child_ds.total_resources), 0) as child_resources,
         COALESCE(ds.total_resources, 0) + COALESCE(SUM(child_ds.total_resources), 0) as total_hierarchy_resources
       FROM dept_hierarchy dh
       LEFT JOIN department_summary_temp ds ON dh.department_id = ds.department_id
       LEFT JOIN dept_hierarchy child_dh ON child_dh.path LIKE dh.path || '%' AND child_dh.department_id != dh.department_id
       LEFT JOIN department_summary_temp child_ds ON child_dh.department_id = child_ds.department_id
       GROUP BY dh.department_id, dh.department_name, dh.parent_department_id, dh.level, dh.path, ds.total_resources
       ORDER BY dh.path
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | Uses department data and summary |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | hierarchy_analysis | Department hierarchy analysis |
     - **Callback**: Include in department results

5. **Step 5: Generate Department Comparison Analysis**
   - **Description**: Generate comparative analysis between departments
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       department_name,
       total_resources,
       availability_percentage,
       allocation_percentage,
       avg_experience,
       (total_resources - AVG(total_resources) OVER()) / STDDEV(total_resources) OVER() as resource_zscore,
       (availability_percentage - AVG(availability_percentage) OVER()) / STDDEV(availability_percentage) OVER() as availability_zscore,
       CASE 
         WHEN total_resources > PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_resources) OVER() THEN 'High'
         WHEN total_resources > PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_resources) OVER() THEN 'Medium'
         ELSE 'Low'
       END as resource_category,
       CASE 
         WHEN availability_percentage > PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY availability_percentage) OVER() THEN 'High'
         WHEN availability_percentage > PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY availability_percentage) OVER() THEN 'Medium'
         ELSE 'Low'
       END as availability_category
       FROM department_metrics_temp
       ORDER BY total_resources DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | Uses metrics from previous step |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | comparison_analysis | Department comparison analysis |
     - **Callback**: Include in final results

6. **Final Step: Return Department Analytics Results**
   - Return comprehensive department analytics with comparisons and hierarchy analysis

---

### DAO ID: DAO-MDE-03-06-04
### DAO Name: Performance Metrics

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | performanceScope | Object | Required | Scope for performance metrics calculation |
| 2 | kpiDefinitions | Array | Required | KPI definitions to calculate |
| 3 | benchmarkData | Object | Optional | Benchmark data for comparison |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | performanceResults | Object | Performance metrics results |
| 2 | kpiScores | Array | Calculated KPI scores |
| 3 | performanceSummary | Object | Overall performance summary |

### Steps:

1. **Step 1: Validate Performance Metrics Request**
   - **Description**: Validate performance metrics calculation request
   - **Data Validation**: 
     - Check performance scope and KPI definitions
     - Validate benchmark data and user permissions
     - Ensure user has access to performance data
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Calculate Resource Utilization KPIs**
   - **Description**: Calculate resource utilization Key Performance Indicators
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(*) as total_managed_resources,
       COUNT(CASE WHEN status = 'available' THEN 1 END) as available_resources,
       COUNT(CASE WHEN status = 'allocated' THEN 1 END) as allocated_resources,
       COUNT(CASE WHEN status = 'partially_allocated' THEN 1 END) as partial_resources,
       (COUNT(CASE WHEN status = 'allocated' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as allocation_rate,
       (COUNT(CASE WHEN status = 'available' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as availability_rate,
       (COUNT(CASE WHEN status IN ('allocated', 'partially_allocated') THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as utilization_rate,
       AVG(EXTRACT(DAYS FROM (availability_end - availability_start))) as avg_idle_duration
       FROM idle_resources 
       WHERE status != 'deleted'
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_PERFORMANCE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | perf_filters | ARGUMENT.performanceScope | Dynamic performance filters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | utilization_kpis | Resource utilization KPIs |
     - **Callback**: Include in performance results

3. **Step 3: Calculate Efficiency and Quality KPIs**
   - **Description**: Calculate efficiency and quality Key Performance Indicators
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(CASE WHEN EXTRACT(DAYS FROM (availability_end - availability_start)) > 60 THEN 1 END) as long_term_idle_count,
       (COUNT(CASE WHEN EXTRACT(DAYS FROM (availability_end - availability_start)) > 60 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as long_term_idle_rate,
       COUNT(CASE WHEN skills IS NOT NULL AND jsonb_array_length(skills) > 0 THEN 1 END) as resources_with_skills,
       (COUNT(CASE WHEN skills IS NOT NULL AND jsonb_array_length(skills) > 0 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as skill_completion_rate,
       COUNT(CASE WHEN hourly_rate IS NOT NULL THEN 1 END) as resources_with_rates,
       (COUNT(CASE WHEN hourly_rate IS NOT NULL THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as rate_completion_rate,
       COUNT(CASE WHEN experience_years >= 5 THEN 1 END) as senior_resources,
       (COUNT(CASE WHEN experience_years >= 5 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as senior_resource_rate
       FROM idle_resources 
       WHERE status != 'deleted'
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_PERFORMANCE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | perf_filters | ARGUMENT.performanceScope | Dynamic performance filters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | efficiency_kpis | Efficiency and quality KPIs |
     - **Callback**: Include in performance results

4. **Step 4: Calculate Time-based Performance KPIs**
   - **Description**: Calculate time-based performance indicators
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '7 days' THEN 1 END) as weekly_new_resources,
       COUNT(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as monthly_new_resources,
       COUNT(CASE WHEN updated_at >= CURRENT_DATE - INTERVAL '7 days' THEN 1 END) as weekly_updated_resources,
       COUNT(CASE WHEN updated_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as monthly_updated_resources,
       AVG(EXTRACT(DAYS FROM (updated_at - created_at))) as avg_update_frequency,
       COUNT(CASE WHEN availability_start <= CURRENT_DATE AND availability_end >= CURRENT_DATE THEN 1 END) as currently_available_resources,
       COUNT(CASE WHEN availability_end < CURRENT_DATE THEN 1 END) as expired_resources,
       (COUNT(CASE WHEN availability_end < CURRENT_DATE THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)) as expiration_rate
       FROM idle_resources 
       WHERE status != 'deleted'
       AND (department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_PERFORMANCE_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | perf_filters | ARGUMENT.performanceScope | Dynamic performance filters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | time_based_kpis | Time-based performance KPIs |
     - **Callback**: Include in performance results

5. **Step 5: Calculate Overall Performance Score**
   - **Description**: Calculate overall performance score based on KPIs
   - **Data Validation**: None
   - **Callback**: Aggregate KPIs into overall performance score using weighted averages

6. **Final Step: Return Performance Metrics Results**
   - Return comprehensive performance metrics with KPI scores and overall assessment

---

### DAO ID: DAO-MDE-03-06-05
### DAO Name: Custom Report Data

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | reportDefinition | Object | Required | Custom report definition and structure |
| 2 | queryParameters | Object | Required | Parameters for custom query execution |
| 3 | outputFormat | String | Optional, Default: 'tabular' | Output format for report data |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | reportData | Array | Custom report data results |
| 2 | reportMetadata | Object | Report metadata and structure |
| 3 | executionStatistics | Object | Query execution statistics |

### Steps:

1. **Step 1: Validate Custom Report Request**
   - **Description**: Validate custom report definition and parameters
   - **Data Validation**: 
     - Check report definition structure and validity
     - Validate query parameters and user permissions
     - Ensure user has access to requested data
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Build Dynamic Query Structure**
   - **Description**: Build dynamic SQL query based on report definition
   - **Data Validation**: None
   - **Callback**: Construct dynamic SELECT, FROM, WHERE, and ORDER BY clauses

3. **Step 3: Execute Custom Data Query**
   - **Description**: Execute custom query with security controls
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: [DYNAMIC_CUSTOM_QUERY]
       SELECT [DYNAMIC_COLUMNS]
       FROM idle_resources ir 
       [DYNAMIC_JOINS]
       WHERE ir.status != 'deleted'
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_WHERE_CONDITIONS]
       [DYNAMIC_GROUP_BY]
       [DYNAMIC_ORDER_BY]
       [DYNAMIC_LIMIT]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | query_params | ARGUMENT.queryParameters | Dynamic query parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | custom_report_data | Custom report data results |
     - **Callback**: Format results according to output format

4. **Step 4: Apply Data Transformations**
   - **Description**: Apply data transformations and calculations
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       [DYNAMIC_CALCULATED_FIELDS],
       [DYNAMIC_AGGREGATIONS],
       [DYNAMIC_FORMATTERS]
       FROM custom_report_temp
       [DYNAMIC_HAVING_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | transformation_params | Report transformation parameters | Parameters for data transformation |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | transformed_data | Transformed report data |
     - **Callback**: Apply final formatting

5. **Step 5: Generate Report Metadata**
   - **Description**: Generate metadata for the custom report
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(*) as total_rows,
       COUNT(DISTINCT [DYNAMIC_DISTINCT_COLUMNS]) as unique_values,
       MIN([DYNAMIC_MIN_COLUMNS]) as min_values,
       MAX([DYNAMIC_MAX_COLUMNS]) as max_values
       FROM custom_report_temp
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | metadata_columns | Report columns for metadata | Columns to generate metadata for |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | report_metadata | Report metadata and statistics |
     - **Callback**: Include in final results

6. **Final Step: Return Custom Report Data**
   - Return custom report data with metadata and execution statistics
