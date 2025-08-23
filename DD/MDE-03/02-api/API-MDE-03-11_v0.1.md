# API Detailed Design Document

**Document ID**: API-MDE-03-11  
**Document Name**: Get Notifications API Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | API-MDE-03-11 |
| Document Name | Get Notifications API Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Get Notifications API design |

## Used Services

| No | Service Document | Service ID | Service Name |
|----|------------------|------------|--------------|
| 1 | SVE-MDE-03-07_Notification Service_v0.1 | SVE-MDE-03-07 | Notification Service |
| 2 | SVE-MDE-03-02_Search and Filter Service_v0.1 | SVE-MDE-03-02 | Search and Filter Service |

## APIs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | API-MDE-03-11 | Get Notifications | Retrieves user-specific notifications related to idle resource management including alerts, deadlines, approvals, system messages, and status updates with filtering and pagination support. |

## Logic & Flow

### API ID: API-MDE-03-11
### API Name: Get Notifications
### HTTP Method: GET
### URI: /api/v1/idle-resources/notifications

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | status | String | Optional | Notification status (unread/read/all) |
| 2 | type | String | Optional | Notification type filter |
| 3 | priority | String | Optional | Priority level (high/medium/low) |
| 4 | fromDate | Date | Optional | Start date for notification range |
| 5 | toDate | Date | Optional | End date for notification range |
| 6 | page | Number | Optional, Default: 1 | Page number for pagination |
| 7 | pageSize | Number | Optional, Default: 20, Max: 50 | Number of notifications per page |
| 8 | markAsRead | Boolean | Optional, Default: false | Mark retrieved notifications as read |
| 9 | includeSystem | Boolean | Optional, Default: true | Include system notifications |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | notifications | Array | Array of notification objects |
| 2 | totalCount | Number | Total number of notifications |
| 3 | unreadCount | Number | Number of unread notifications |
| 4 | pageInfo | Object | Pagination information |
| 5 | notificationSummary | Object | Summary by type and priority |
| 6 | lastChecked | DateTime | Last notification check timestamp |

### Steps:

1. **Step 1: Authentication and Permission Validation**
   - **Description**: Validate user authentication and notification access
   - **Data Validation**: JWT token validation and user context establishment
   - **Service Call**: Authentication and Authorization validation
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | TOKEN.userId | Current user ID from JWT |
       | operation | getNotifications | Operation type |
       | resourceType | notifications | Resource being accessed |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | isAuthorized | Boolean indicating permission status |
       | userContext | User role and department information |
       | notificationScope | User's notification access scope |
     - **Callback**: Proceed if authorized, return 403 if not

2. **Step 2: Validate and Process Filter Parameters**
   - **Description**: Validate notification filter parameters
   - **Data Validation**: Check date ranges, enum values, and parameter combinations
   - **Callback**: Return 400 if invalid parameters

3. **Step 3: Retrieve User Notifications**
   - **Description**: Get notifications based on user and filters
   - **Service Call**: SVE-MDE-03-07 - Notification Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | STEP1.userContext.userId | Target user ID |
       | statusFilter | ARGUMENT.status | Notification status filter |
       | typeFilter | ARGUMENT.type | Notification type filter |
       | priorityFilter | ARGUMENT.priority | Priority level filter |
       | dateRange | From and to dates | Date range for notifications |
       | userScope | STEP1.notificationScope | User's access scope |
       | includeSystemNotifications | ARGUMENT.includeSystem | System notification inclusion |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | notificationList | List of matching notifications |
       | totalCount | Total matching notifications |
       | unreadCount | Count of unread notifications |
       | notificationMetadata | Metadata about notifications |
     - **Callback**: Continue with pagination

4. **Step 4: Apply Pagination**
   - **Description**: Apply pagination to notification results
   - **Service Call**: SVE-MDE-03-02 - Search and Filter Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | dataSet | STEP3.notificationList | Notification list |
       | pageNumber | ARGUMENT.page | Requested page |
       | pageSize | ARGUMENT.pageSize | Page size |
       | sortBy | createdAt | Sort field |
       | sortOrder | desc | Sort order (newest first) |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | paginatedResults | Paginated notification list |
       | paginationInfo | Pagination metadata |
       | totalPages | Total number of pages |
     - **Callback**: Continue with notification processing

5. **Step 5: Enrich Notification Data**
   - **Description**: Enrich notifications with additional context and formatting
   - **Service Call**: SVE-MDE-03-07 - Notification Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | notifications | STEP4.paginatedResults | Paginated notifications |
       | userContext | STEP1.userContext | User context for personalization |
       | enrichmentLevel | full | Level of data enrichment |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | enrichedNotifications | Notifications with full context |
       | actionableItems | Notifications requiring user action |
       | relatedResources | Links to related resources |
     - **Callback**: Continue with read status update if requested

6. **Step 6: Mark as Read (if requested)**
   - **Description**: Mark retrieved notifications as read if requested
   - **Data Validation**: Check markAsRead flag and user permissions
   - **Service Call**: SVE-MDE-03-07 - Notification Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | notificationIds | IDs from enriched notifications | Notification IDs to mark as read |
       | userId | STEP1.userContext.userId | User ID |
       | markAsRead | ARGUMENT.markAsRead | Mark as read flag |
       | timestamp | CURRENT.timestamp | Read timestamp |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updateResult | Read status update result |
       | updatedCount | Number of notifications marked as read |
     - **Callback**: Update notification statuses in response

7. **Step 7: Generate Notification Summary**
   - **Description**: Generate summary statistics for notifications
   - **Service Call**: SVE-MDE-03-07 - Notification Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | allNotifications | STEP3.notificationList | Complete notification list |
       | userContext | STEP1.userContext | User context |
       | summaryType | dashboard | Type of summary to generate |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | notificationSummary | Summary by type and priority |
       | urgentAlerts | Count of urgent notifications |
       | actionRequired | Count of actionable notifications |
       | summaryMetadata | Summary metadata |
     - **Callback**: Include summary in response

8. **Step 8: Update Last Checked Timestamp**
   - **Description**: Update user's last notification check timestamp
   - **Service Call**: SVE-MDE-03-07 - Notification Service
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | userId | STEP1.userContext.userId | User ID |
       | checkTimestamp | CURRENT.timestamp | Current timestamp |
       | notificationCount | Count of notifications retrieved | Number retrieved |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updateResult | Timestamp update confirmation |
       | lastChecked | Updated last checked timestamp |
     - **Callback**: Include timestamp in response

9. **Step 9: Format Notification Response**
   - **Description**: Format comprehensive notification response
   - **Data Validation**: Ensure all response fields are properly formatted
   - **Callback**: Return formatted notification data with metadata

10. **Final Step: Return Notification Results**
    - HTTP 200 OK with notification list
    - Pagination information
    - Unread count and summary statistics
    - Last checked timestamp
    - Actionable items highlighted
