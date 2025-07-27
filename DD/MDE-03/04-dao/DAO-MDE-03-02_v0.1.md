# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-02  
**Document Name**: Search and Filtering DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-02 |
| Document Name | Search and Filtering DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Search and Filtering DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-02-01 | Advanced Search | Execute advanced search queries with multiple criteria |
| 2 | DAO-MDE-03-02-02 | Quick Search | Execute quick search with simple keyword matching |
| 3 | DAO-MDE-03-02-03 | Filter Resources | Apply filters to resource dataset |
| 4 | DAO-MDE-03-02-04 | Skill-based Search | Search resources based on skill requirements |
| 5 | DAO-MDE-03-02-05 | Availability Search | Search resources based on availability criteria |

## Logic & Flow

### DAO ID: DAO-MDE-03-02-01
### DAO Name: Advanced Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | searchCriteria | Object | Required | Complex search criteria with multiple fields |
| 2 | searchScope | Object | Optional | Scope limitations for search |
| 3 | paginationInfo | Object | Required | Pagination parameters |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | searchResults | Array | Matching idle resource records |
| 2 | totalMatches | Integer | Total number of matching records |
| 3 | searchMetadata | Object | Search metadata and relevance scoring |
| 4 | facetCounts | Object | Facet counts for search refinement |

### Steps:

1. **Step 1: Validate Advanced Search Criteria**
   - **Description**: Validate complex search criteria and parameters
   - **Data Validation**: 
     - Check search criteria format and field validity
     - Validate search operators and value ranges
     - Ensure user has search permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Build Complex Search Query**
   - **Description**: Build complex SQL query with JOIN operations and WHERE conditions
   - **Data Validation**: None
   - **Callback**: Construct dynamic query based on multiple search criteria

3. **Step 3: Execute Search with Relevance Scoring**
   - **Description**: Execute advanced search with relevance scoring
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, e.email, d.department_name, rt.type_description, 
       CASE 
         WHEN ir.skills::text ILIKE ? THEN 10
         WHEN CONCAT(e.first_name, ' ', e.last_name) ILIKE ? THEN 8
         WHEN d.department_name ILIKE ? THEN 6
         ELSE 1
       END as relevance_score
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       LEFT JOIN resource_types rt ON ir.resource_type = rt.type_code 
       WHERE ir.status != 'deleted' 
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_WHERE_CONDITIONS]
       ORDER BY relevance_score DESC, ir.updated_at DESC
       LIMIT ? OFFSET ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | skill_pattern | ARGUMENT.searchCriteria.skillKeyword | Skill search pattern |
       | name_pattern | ARGUMENT.searchCriteria.nameKeyword | Name search pattern |
       | dept_pattern | ARGUMENT.searchCriteria.deptKeyword | Department search pattern |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | search_params | ARGUMENT.searchCriteria | Dynamic search parameters |
       | limit | ARGUMENT.paginationInfo.limit | Page size limit |
       | offset | ARGUMENT.paginationInfo.offset | Page offset |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | search_results | Search results with relevance scores |
     - **Callback**: Return ranked search results

4. **Step 4: Get Total Match Count**
   - **Description**: Get total count of matching records for pagination
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as total_matches FROM idle_resources ir LEFT JOIN employees e ON ir.employee_id = e.employee_id LEFT JOIN departments d ON ir.department_id = d.department_id WHERE ir.status != 'deleted' AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin') [DYNAMIC_WHERE_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | search_params | ARGUMENT.searchCriteria | Dynamic search parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | total_matches | Total matching records |
     - **Callback**: Use count for pagination metadata

5. **Step 5: Calculate Facet Counts**
   - **Description**: Calculate facet counts for search refinement
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       resource_type, COUNT(*) as type_count,
       department_id, COUNT(*) as dept_count,
       status, COUNT(*) as status_count
       FROM idle_resources ir 
       WHERE ir.status != 'deleted' 
       [DYNAMIC_WHERE_CONDITIONS]
       GROUP BY resource_type, department_id, status
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | search_params | ARGUMENT.searchCriteria | Dynamic search parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | facet_data | Facet counts for refinement |
     - **Callback**: Format facets for response

6. **Final Step: Return Advanced Search Results**
   - Return comprehensive search results with relevance scoring, pagination, and facets

---

### DAO ID: DAO-MDE-03-02-02
### DAO Name: Quick Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | searchKeyword | String | Required | Simple keyword for quick search |
| 2 | searchFields | Array | Optional | Fields to search in |
| 3 | limitResults | Integer | Optional, Default: 10 | Maximum results to return |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | quickResults | Array | Quick search results |
| 2 | searchSuggestions | Array | Search suggestions for autocomplete |
| 3 | matchCategories | Object | Categories of matches found |

### Steps:

1. **Step 1: Validate Quick Search**
   - **Description**: Validate quick search parameters
   - **Data Validation**: 
     - Check keyword format and length
     - Validate search fields and result limits
     - Ensure user has search permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Execute Quick Search**
   - **Description**: Execute quick search across multiple fields
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT DISTINCT ir.resource_id, ir.status, CONCAT(e.first_name, ' ', e.last_name) as employee_name, d.department_name, ir.resource_type, ir.skills,
       CASE 
         WHEN CONCAT(e.first_name, ' ', e.last_name) ILIKE ? THEN 'employee'
         WHEN d.department_name ILIKE ? THEN 'department'
         WHEN ir.skills::text ILIKE ? THEN 'skill'
         WHEN rt.type_description ILIKE ? THEN 'type'
         ELSE 'other'
       END as match_category
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       LEFT JOIN resource_types rt ON ir.resource_type = rt.type_code
       WHERE ir.status != 'deleted' 
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       AND (
         CONCAT(e.first_name, ' ', e.last_name) ILIKE ? OR
         d.department_name ILIKE ? OR
         ir.skills::text ILIKE ? OR
         rt.type_description ILIKE ?
       )
       ORDER BY 
         CASE match_category
           WHEN 'employee' THEN 1
           WHEN 'department' THEN 2
           WHEN 'skill' THEN 3
           WHEN 'type' THEN 4
           ELSE 5
         END,
         ir.updated_at DESC
       LIMIT ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | name_pattern_1 | '%' + ARGUMENT.searchKeyword + '%' | Name match pattern |
       | dept_pattern_1 | '%' + ARGUMENT.searchKeyword + '%' | Department match pattern |
       | skill_pattern_1 | '%' + ARGUMENT.searchKeyword + '%' | Skill match pattern |
       | type_pattern_1 | '%' + ARGUMENT.searchKeyword + '%' | Type match pattern |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | name_pattern_2 | '%' + ARGUMENT.searchKeyword + '%' | Name search pattern |
       | dept_pattern_2 | '%' + ARGUMENT.searchKeyword + '%' | Department search pattern |
       | skill_pattern_2 | '%' + ARGUMENT.searchKeyword + '%' | Skill search pattern |
       | type_pattern_2 | '%' + ARGUMENT.searchKeyword + '%' | Type search pattern |
       | limit | ARGUMENT.limitResults | Result limit |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | quick_results | Quick search results with categories |
     - **Callback**: Format results by match category

3. **Step 3: Generate Search Suggestions**
   - **Description**: Generate autocomplete suggestions based on search keyword
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT DISTINCT suggestion, category FROM (
       SELECT CONCAT(e.first_name, ' ', e.last_name) as suggestion, 'employee' as category 
       FROM idle_resources ir JOIN employees e ON ir.employee_id = e.employee_id 
       WHERE CONCAT(e.first_name, ' ', e.last_name) ILIKE ? 
       UNION ALL
       SELECT DISTINCT d.department_name as suggestion, 'department' as category 
       FROM idle_resources ir JOIN departments d ON ir.department_id = d.department_id 
       WHERE d.department_name ILIKE ?
       UNION ALL
       SELECT DISTINCT unnest(string_to_array(ir.skills::text, ',')) as suggestion, 'skill' as category 
       FROM idle_resources ir 
       WHERE ir.skills::text ILIKE ?
       ) suggestions 
       ORDER BY category, suggestion 
       LIMIT 10
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | name_suggestion | ARGUMENT.searchKeyword + '%' | Name suggestion pattern |
       | dept_suggestion | ARGUMENT.searchKeyword + '%' | Department suggestion pattern |
       | skill_suggestion | '%' + ARGUMENT.searchKeyword + '%' | Skill suggestion pattern |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | suggestions | Search suggestions by category |
     - **Callback**: Group suggestions by category

4. **Final Step: Return Quick Search Results**
   - Return quick search results with suggestions and match categories

---

### DAO ID: DAO-MDE-03-02-03
### DAO Name: Filter Resources

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | filterConfig | Object | Required | Filter configuration with field-value pairs |
| 2 | combineLogic | String | Optional, Default: 'AND' | Logic for combining filters (AND/OR) |
| 3 | paginationInfo | Object | Required | Pagination parameters |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | filteredResults | Array | Filtered resource records |
| 2 | filterSummary | Object | Summary of applied filters |
| 3 | availableFilters | Object | Available filter options |

### Steps:

1. **Step 1: Validate Filter Configuration**
   - **Description**: Validate filter configuration and parameters
   - **Data Validation**: 
     - Check filter fields and values validity
     - Validate combine logic and pagination
     - Ensure user has filter permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Get Available Filter Options**
   - **Description**: Get available filter options for dynamic filtering
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       ARRAY_AGG(DISTINCT ir.resource_type) as available_types,
       ARRAY_AGG(DISTINCT ir.status) as available_statuses,
       ARRAY_AGG(DISTINCT d.department_name) as available_departments,
       MIN(ir.hourly_rate) as min_rate, MAX(ir.hourly_rate) as max_rate,
       MIN(ir.experience_years) as min_experience, MAX(ir.experience_years) as max_experience
       FROM idle_resources ir 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       WHERE ir.status != 'deleted'
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | filter_options | Available filter options |
     - **Callback**: Format filter options for response

3. **Step 3: Build Dynamic Filter Query**
   - **Description**: Build dynamic SQL query based on filter configuration
   - **Data Validation**: None
   - **Callback**: Construct WHERE clause based on filter config and combine logic

4. **Step 4: Execute Filtered Query**
   - **Description**: Execute query with applied filters
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, e.email, d.department_name, rt.type_description 
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       LEFT JOIN resource_types rt ON ir.resource_type = rt.type_code 
       WHERE ir.status != 'deleted' 
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       [DYNAMIC_FILTER_CONDITIONS]
       ORDER BY ir.updated_at DESC
       LIMIT ? OFFSET ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | filter_params | ARGUMENT.filterConfig | Dynamic filter parameters |
       | limit | ARGUMENT.paginationInfo.limit | Page size limit |
       | offset | ARGUMENT.paginationInfo.offset | Page offset |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | filtered_results | Filtered resource records |
     - **Callback**: Return filtered results

5. **Step 5: Generate Filter Summary**
   - **Description**: Generate summary of applied filters and result counts
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as total_filtered, 
       COUNT(DISTINCT ir.department_id) as dept_count,
       COUNT(DISTINCT ir.resource_type) as type_count,
       AVG(ir.hourly_rate) as avg_rate
       FROM idle_resources ir 
       WHERE ir.status != 'deleted' 
       [DYNAMIC_FILTER_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | filter_params | ARGUMENT.filterConfig | Dynamic filter parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | filter_summary | Filter summary statistics |
     - **Callback**: Include summary in response

6. **Final Step: Return Filtered Results**
   - Return filtered results with summary and available filter options

---

### DAO ID: DAO-MDE-03-02-04
### DAO Name: Skill-based Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | requiredSkills | Array | Required | List of required skills |
| 2 | optionalSkills | Array | Optional | List of optional/preferred skills |
| 3 | skillMatchMode | String | Optional, Default: 'partial' | Skill matching mode (exact/partial/fuzzy) |
| 4 | experienceRange | Object | Optional | Experience level requirements |
| 5 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | skillMatches | Array | Resources matching skill criteria |
| 2 | skillScoring | Object | Skill match scoring details |
| 3 | recommendedResources | Array | AI-recommended resources based on skills |

### Steps:

1. **Step 1: Validate Skill Search Criteria**
   - **Description**: Validate skill-based search parameters
   - **Data Validation**: 
     - Check skill lists format and validity
     - Validate skill match mode and experience range
     - Ensure user has skill search permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Execute Skill-based Search with Scoring**
   - **Description**: Execute skill-based search with comprehensive scoring
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, d.department_name,
       (
         SELECT COUNT(*) FROM unnest(string_to_array(ir.skills::text, ',')) skill 
         WHERE skill = ANY(?)
       ) as required_skill_matches,
       (
         SELECT COUNT(*) FROM unnest(string_to_array(ir.skills::text, ',')) skill 
         WHERE skill = ANY(?)
       ) as optional_skill_matches,
       (
         (SELECT COUNT(*) FROM unnest(string_to_array(ir.skills::text, ',')) skill WHERE skill = ANY(?)) * 10 +
         (SELECT COUNT(*) FROM unnest(string_to_array(ir.skills::text, ',')) skill WHERE skill = ANY(?)) * 5 +
         CASE 
           WHEN ir.experience_years >= ? AND ir.experience_years <= ? THEN 15
           WHEN ir.experience_years >= ? OR ir.experience_years <= ? THEN 5
           ELSE 0
         END
       ) as skill_score
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       WHERE ir.status IN ('available', 'partially_allocated') 
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       AND (
         EXISTS (SELECT 1 FROM unnest(string_to_array(ir.skills::text, ',')) skill WHERE skill = ANY(?))
       )
       ORDER BY skill_score DESC, required_skill_matches DESC, optional_skill_matches DESC
       LIMIT 50
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | required_skills_1 | ARGUMENT.requiredSkills | Required skills for counting |
       | optional_skills_1 | ARGUMENT.optionalSkills | Optional skills for counting |
       | required_skills_2 | ARGUMENT.requiredSkills | Required skills for scoring |
       | optional_skills_2 | ARGUMENT.optionalSkills | Optional skills for scoring |
       | min_experience | ARGUMENT.experienceRange.min | Minimum experience requirement |
       | max_experience | ARGUMENT.experienceRange.max | Maximum experience requirement |
       | loose_min | ARGUMENT.experienceRange.min - 1 | Loose minimum experience |
       | loose_max | ARGUMENT.experienceRange.max + 1 | Loose maximum experience |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | search_skills | ARGUMENT.requiredSkills | Skills for existence check |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | skill_matches | Resources with skill match scoring |
     - **Callback**: Return ranked skill matches

3. **Step 3: Calculate Detailed Skill Scoring**
   - **Description**: Calculate detailed skill scoring breakdown for each match
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       resource_id,
       string_to_array(skills::text, ',') as resource_skills,
       ARRAY(SELECT unnest(string_to_array(skills::text, ',')) INTERSECT SELECT unnest(?)) as matched_required,
       ARRAY(SELECT unnest(string_to_array(skills::text, ',')) INTERSECT SELECT unnest(?)) as matched_optional,
       ARRAY(SELECT unnest(?) EXCEPT SELECT unnest(string_to_array(skills::text, ','))) as missing_skills
       FROM idle_resources 
       WHERE resource_id = ANY(?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | required_skills | ARGUMENT.requiredSkills | Required skills array |
       | optional_skills | ARGUMENT.optionalSkills | Optional skills array |
       | all_required | ARGUMENT.requiredSkills | All required skills |
       | resource_ids | Result resource IDs | Resource IDs from previous query |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | skill_breakdown | Detailed skill matching breakdown |
     - **Callback**: Merge with main results

4. **Step 4: Generate AI Recommendations**
   - **Description**: Generate AI-based recommendations for skill matching
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, 
       similarity(ir.skills::text, ?) as skill_similarity,
       'ai_recommended' as recommendation_type
       FROM idle_resources ir 
       WHERE ir.status IN ('available', 'partially_allocated')
       AND ir.resource_id NOT IN (?)
       ORDER BY skill_similarity DESC
       LIMIT 10
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | skill_text | Concatenated required skills | Text for similarity matching |
       | excluded_ids | Already matched resource IDs | Resources to exclude |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | ai_recommendations | AI-recommended resources |
     - **Callback**: Add to recommendation list

5. **Final Step: Return Skill-based Search Results**
   - Return skill-based search results with scoring, breakdown, and AI recommendations

---

### DAO ID: DAO-MDE-03-02-05
### DAO Name: Availability Search

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | dateRange | Object | Required | Date range for availability search |
| 2 | durationRequired | Integer | Optional | Duration in days required |
| 3 | availabilityType | String | Optional, Default: 'full' | Type of availability (full/partial) |
| 4 | workloadCapacity | Integer | Optional | Required workload capacity percentage |
| 5 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | availableResources | Array | Resources available in specified period |
| 2 | availabilityDetails | Object | Detailed availability information |
| 3 | conflictAnalysis | Object | Analysis of scheduling conflicts |

### Steps:

1. **Step 1: Validate Availability Search**
   - **Description**: Validate availability search parameters
   - **Data Validation**: 
     - Check date range validity and format
     - Validate duration and capacity parameters
     - Ensure user has availability search permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Search Available Resources**
   - **Description**: Search for resources available in specified date range
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT ir.*, e.first_name, e.last_name, d.department_name,
       CASE 
         WHEN ir.availability_start <= ? AND ir.availability_end >= ? THEN 'fully_available'
         WHEN ir.availability_start <= ? AND ir.availability_end >= ? THEN 'partially_available'
         ELSE 'not_available'
       END as availability_status,
       GREATEST(ir.availability_start, ?) as effective_start,
       LEAST(ir.availability_end, ?) as effective_end,
       (LEAST(ir.availability_end, ?) - GREATEST(ir.availability_start, ?)) as available_days
       FROM idle_resources ir 
       LEFT JOIN employees e ON ir.employee_id = e.employee_id 
       LEFT JOIN departments d ON ir.department_id = d.department_id 
       WHERE ir.status IN ('available', 'partially_allocated')
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       AND ir.availability_start <= ? 
       AND ir.availability_end >= ?
       AND (? IS NULL OR (LEAST(ir.availability_end, ?) - GREATEST(ir.availability_start, ?)) >= ?)
       ORDER BY availability_status, available_days DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | search_start_1 | ARGUMENT.dateRange.start | Search start date for full check |
       | search_end_1 | ARGUMENT.dateRange.end | Search end date for full check |
       | search_start_2 | ARGUMENT.dateRange.start | Search start date for partial check |
       | search_end_2 | ARGUMENT.dateRange.end | Search end date for partial check |
       | effective_start_1 | ARGUMENT.dateRange.start | Effective start calculation |
       | effective_end_1 | ARGUMENT.dateRange.end | Effective end calculation |
       | effective_end_2 | ARGUMENT.dateRange.end | Available days calculation end |
       | effective_start_2 | ARGUMENT.dateRange.start | Available days calculation start |
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | search_end_3 | ARGUMENT.dateRange.end | Availability end constraint |
       | search_start_3 | ARGUMENT.dateRange.start | Availability start constraint |
       | duration | ARGUMENT.durationRequired | Required duration |
       | duration_end | ARGUMENT.dateRange.end | Duration calculation end |
       | duration_start | ARGUMENT.dateRange.start | Duration calculation start |
       | required_duration | ARGUMENT.durationRequired | Duration requirement |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | available_resources | Resources with availability details |
     - **Callback**: Return availability matches

3. **Step 3: Check Existing Allocations and Conflicts**
   - **Description**: Check for existing allocations and potential conflicts
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       ra.resource_id,
       COUNT(*) as allocation_count,
       SUM(ra.allocation_percentage) as total_allocation,
       100 - SUM(ra.allocation_percentage) as remaining_capacity,
       ARRAY_AGG(ra.project_name) as conflicting_projects,
       MIN(ra.start_date) as earliest_conflict,
       MAX(ra.end_date) as latest_conflict
       FROM resource_allocations ra 
       WHERE ra.resource_id = ANY(?)
       AND ra.status IN ('active', 'confirmed')
       AND ra.start_date <= ? 
       AND ra.end_date >= ?
       GROUP BY ra.resource_id
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | resource_ids | Available resource IDs | Resource IDs from previous query |
       | conflict_end | ARGUMENT.dateRange.end | Conflict check end date |
       | conflict_start | ARGUMENT.dateRange.start | Conflict check start date |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | allocation_conflicts | Existing allocation information |
     - **Callback**: Merge conflict data with availability results

4. **Step 4: Calculate Workload Capacity**
   - **Description**: Calculate available workload capacity for each resource
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       ir.resource_id,
       ir.max_workload_percentage,
       COALESCE(SUM(ra.allocation_percentage), 0) as current_workload,
       ir.max_workload_percentage - COALESCE(SUM(ra.allocation_percentage), 0) as available_capacity,
       CASE 
         WHEN ir.max_workload_percentage - COALESCE(SUM(ra.allocation_percentage), 0) >= ? THEN true
         ELSE false
       END as meets_capacity_requirement
       FROM idle_resources ir 
       LEFT JOIN resource_allocations ra ON ir.resource_id = ra.resource_id 
         AND ra.status IN ('active', 'confirmed')
         AND ra.start_date <= ? 
         AND ra.end_date >= ?
       WHERE ir.resource_id = ANY(?)
       GROUP BY ir.resource_id, ir.max_workload_percentage
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | required_capacity | ARGUMENT.workloadCapacity | Required workload capacity |
       | capacity_end | ARGUMENT.dateRange.end | Capacity check end date |
       | capacity_start | ARGUMENT.dateRange.start | Capacity check start date |
       | resource_ids | Available resource IDs | Resource IDs to check |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | capacity_analysis | Workload capacity analysis |
     - **Callback**: Filter resources by capacity requirements

5. **Final Step: Return Availability Search Results**
   - Return availability search results with detailed availability, conflicts, and capacity analysis
