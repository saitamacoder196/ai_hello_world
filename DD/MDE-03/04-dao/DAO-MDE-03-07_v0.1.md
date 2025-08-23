# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-07  
**Document Name**: Notification and Alert DAO Design  

## Cover

| Field | Value |
|-------|-------|
| Document ID | DAO-MDE-03-07 |
| Document Name | Notification and Alert DAO Design |
| Module | MDE-03 - Idle Resource Data Management |
| Version | v0.1 |
| Date | 2025-07-25 |
| Author | System Designer |

## History

| No | Date | Version | Account | Action | Impacted Sections | Description |
|----|------|---------|---------|--------|-------------------|-------------|
| 1 | 2025-07-25 | v0.1 | System Designer | Initialize | Whole Document | Initial creation of Notification and Alert DAO design |

## DAOs

| No | ID | Name | Description |
|----|----|----|-------------|
| 1 | DAO-MDE-03-07-01 | Notification Management | Manage notification creation, delivery, and tracking |
| 2 | DAO-MDE-03-07-02 | Alert Processing | Process and manage system alerts and warnings |
| 3 | DAO-MDE-03-07-03 | Subscription Management | Manage user notification subscriptions and preferences |
| 4 | DAO-MDE-03-07-04 | Notification History | Track notification history and delivery status |
| 5 | DAO-MDE-03-07-05 | Alert Rules Engine | Manage alert rules and trigger conditions |

## Logic & Flow

### DAO ID: DAO-MDE-03-07-01
### DAO Name: Notification Management

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | notificationData | Object | Required | Notification content and metadata |
| 2 | recipients | Array | Required | List of notification recipients |
| 3 | deliveryOptions | Object | Optional | Delivery method and timing options |
| 4 | userContext | Object | Required | User context for audit and authorization |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | notificationId | String | Generated notification ID |
| 2 | deliveryStatus | Object | Initial delivery status |
| 3 | operationResult | Object | Operation result status |

### Steps:

1. **Step 1: Validate Notification Request**
   - **Description**: Validate notification data and recipient information
   - **Data Validation**: 
     - Check notification content and type validity
     - Validate recipient list and permissions
     - Ensure user has notification sending rights
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Create Notification Record**
   - **Description**: Create primary notification record in database
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO notifications (
       notification_id,
       notification_type,
       title,
       content,
       priority,
       created_by,
       created_at,
       scheduled_at,
       expiry_at,
       status,
       notification_data
       ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, 'pending', ?)
       RETURNING notification_id, created_at
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | notification_id | Generated UUID | Generated notification identifier |
       | notification_type | ARGUMENT.notificationData.type | Type of notification |
       | title | ARGUMENT.notificationData.title | Notification title |
       | content | ARGUMENT.notificationData.content | Notification content |
       | priority | ARGUMENT.notificationData.priority | Notification priority |
       | created_by | ARGUMENT.userContext.userId | User creating notification |
       | scheduled_at | ARGUMENT.deliveryOptions.scheduledAt | Scheduled delivery time |
       | expiry_at | ARGUMENT.deliveryOptions.expiryAt | Notification expiry time |
       | notification_data | ARGUMENT.notificationData.metadata | Additional notification data |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | notification_record | Created notification record |
     - **Callback**: Use notification ID for recipient records

3. **Step 3: Create Recipient Records**
   - **Description**: Create notification recipient records
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO notification_recipients (
       notification_id,
       recipient_id,
       recipient_type,
       delivery_method,
       status,
       created_at
       ) 
       SELECT ?, recipient_id, recipient_type, delivery_method, 'pending', CURRENT_TIMESTAMP
       FROM json_to_recordset(?) AS recipients(
         recipient_id text,
         recipient_type text,
         delivery_method text
       )
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | notification_id | Previous step result | Notification ID |
       | recipients_json | ARGUMENT.recipients | Recipients data as JSON |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | recipient_records | Created recipient records |
     - **Callback**: Set up delivery tracking

4. **Step 4: Update Notification Status**
   - **Description**: Update notification status to ready for delivery
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: UPDATE notifications 
       SET status = 'ready', 
           updated_at = CURRENT_TIMESTAMP,
           recipient_count = (
             SELECT COUNT(*) 
             FROM notification_recipients 
             WHERE notification_id = ?
           )
       WHERE notification_id = ?
       RETURNING status, recipient_count
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | notification_id_1 | Previous step result | Notification ID for count |
       | notification_id_2 | Previous step result | Notification ID for update |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | updated_status | Updated notification status |
     - **Callback**: Prepare delivery status response

5. **Step 5: Log Notification Creation**
   - **Description**: Log notification creation for audit trail
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO notification_audit_log (
       log_id,
       notification_id,
       action,
       performed_by,
       performed_at,
       details
       ) VALUES (?, ?, 'created', ?, CURRENT_TIMESTAMP, ?)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | log_id | Generated UUID | Audit log identifier |
       | notification_id | Previous step result | Notification ID |
       | performed_by | ARGUMENT.userContext.userId | User performing action |
       | details | JSON audit details | Creation details and metadata |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | audit_record | Created audit record |
     - **Callback**: Complete notification creation

6. **Final Step: Return Notification Creation Results**
   - Return notification ID, delivery status, and operation result

---

### DAO ID: DAO-MDE-03-07-02
### DAO Name: Alert Processing

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | alertData | Object | Required | Alert information and trigger data |
| 2 | alertRules | Array | Required | Applicable alert rules |
| 3 | escalationConfig | Object | Optional | Escalation configuration |
| 4 | systemContext | Object | Required | System context for alert processing |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | alertId | String | Generated alert ID |
| 2 | processingResult | Object | Alert processing result |
| 3 | escalationStatus | Object | Escalation status and next steps |

### Steps:

1. **Step 1: Validate Alert Data**
   - **Description**: Validate alert data and processing rules
   - **Data Validation**: 
     - Check alert data completeness and validity
     - Validate alert rules and escalation configuration
     - Ensure system has alert processing rights
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Alert Suppression Rules**
   - **Description**: Check if alert should be suppressed based on existing alerts
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT COUNT(*) as similar_alerts_count,
       MAX(created_at) as last_similar_alert
       FROM alerts 
       WHERE alert_type = ?
       AND source_resource_id = ?
       AND status IN ('active', 'acknowledged')
       AND created_at > CURRENT_TIMESTAMP - INTERVAL '1 hour'
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | alert_type | ARGUMENT.alertData.type | Type of alert |
       | source_resource_id | ARGUMENT.alertData.sourceResourceId | Source resource identifier |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | suppression_check | Alert suppression check results |
     - **Callback**: Determine if alert should be created or suppressed

3. **Step 3: Create Alert Record**
   - **Description**: Create alert record if not suppressed
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO alerts (
       alert_id,
       alert_type,
       severity,
       title,
       description,
       source_resource_id,
       source_module,
       trigger_data,
       status,
       created_at,
       acknowledged_by,
       resolved_by
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', CURRENT_TIMESTAMP, NULL, NULL)
       RETURNING alert_id, created_at
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | alert_id | Generated UUID | Generated alert identifier |
       | alert_type | ARGUMENT.alertData.type | Type of alert |
       | severity | ARGUMENT.alertData.severity | Alert severity level |
       | title | ARGUMENT.alertData.title | Alert title |
       | description | ARGUMENT.alertData.description | Alert description |
       | source_resource_id | ARGUMENT.alertData.sourceResourceId | Source resource ID |
       | source_module | ARGUMENT.systemContext.module | Source module identifier |
       | trigger_data | ARGUMENT.alertData.triggerData | Data that triggered alert |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | alert_record | Created alert record |
     - **Callback**: Use alert ID for further processing

4. **Step 4: Process Alert Rules**
   - **Description**: Process applicable alert rules and actions
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO alert_rule_executions (
       execution_id,
       alert_id,
       rule_id,
       rule_name,
       execution_result,
       executed_at
       )
       SELECT 
         gen_random_uuid(),
         ?,
         rule_id,
         rule_name,
         'executed',
         CURRENT_TIMESTAMP
       FROM json_to_recordset(?) AS rules(
         rule_id text,
         rule_name text,
         rule_actions jsonb
       )
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | alert_id | Previous step result | Alert ID |
       | rules_json | ARGUMENT.alertRules | Alert rules as JSON |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | rule_executions | Executed alert rules |
     - **Callback**: Process rule actions

5. **Step 5: Setup Alert Escalation**
   - **Description**: Setup alert escalation if configured
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO alert_escalations (
       escalation_id,
       alert_id,
       escalation_level,
       target_users,
       escalation_time,
       status,
       created_at
       ) VALUES (?, ?, ?, ?, ?, 'scheduled', CURRENT_TIMESTAMP)
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | escalation_id | Generated UUID | Escalation identifier |
       | alert_id | Previous step result | Alert ID |
       | escalation_level | ARGUMENT.escalationConfig.level | Escalation level |
       | target_users | ARGUMENT.escalationConfig.targetUsers | Users to escalate to |
       | escalation_time | ARGUMENT.escalationConfig.escalationTime | When to escalate |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | escalation_setup | Escalation setup result |
     - **Callback**: Include in processing result

6. **Step 6: Update Alert Statistics**
   - **Description**: Update system alert statistics
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO alert_statistics (
       stat_date,
       alert_type,
       total_count,
       active_count,
       resolved_count
       ) VALUES (CURRENT_DATE, ?, 1, 1, 0)
       ON CONFLICT (stat_date, alert_type) 
       DO UPDATE SET 
         total_count = alert_statistics.total_count + 1,
         active_count = alert_statistics.active_count + 1,
         updated_at = CURRENT_TIMESTAMP
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | alert_type | ARGUMENT.alertData.type | Type of alert for statistics |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | statistics_update | Updated statistics |
     - **Callback**: Complete alert processing

7. **Final Step: Return Alert Processing Results**
   - Return alert ID, processing result, and escalation status

---

### DAO ID: DAO-MDE-03-07-03
### DAO Name: Subscription Management

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | subscriptionData | Object | Required | Subscription details and preferences |
| 2 | operation | String | Required | Operation type (create/update/delete) |
| 3 | userPreferences | Object | Optional | User preference settings |
| 4 | userContext | Object | Required | User context for authorization |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | subscriptionId | String | Subscription ID |
| 2 | operationResult | Object | Operation result status |
| 3 | activeSubscriptions | Array | User's active subscriptions |

### Steps:

1. **Step 1: Validate Subscription Request**
   - **Description**: Validate subscription operation and user permissions
   - **Data Validation**: 
     - Check subscription data and operation type
     - Validate user preferences and permissions
     - Ensure user can manage subscriptions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Check Existing Subscriptions**
   - **Description**: Check user's existing subscriptions for conflicts
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       subscription_id,
       subscription_type,
       resource_filter,
       delivery_method,
       frequency,
       status,
       created_at
       FROM notification_subscriptions 
       WHERE user_id = ?
       AND status = 'active'
       AND subscription_type = ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID |
       | subscription_type | ARGUMENT.subscriptionData.type | Subscription type |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | existing_subscriptions | User's existing subscriptions |
     - **Callback**: Check for duplicates or conflicts

3. **Step 3: Create/Update Subscription Record**
   - **Description**: Create new or update existing subscription
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO notification_subscriptions (
       subscription_id,
       user_id,
       subscription_type,
       subscription_name,
       resource_filter,
       delivery_method,
       frequency,
       notification_template,
       preferences,
       status,
       created_at,
       created_by
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', CURRENT_TIMESTAMP, ?)
       ON CONFLICT (user_id, subscription_type, resource_filter) 
       DO UPDATE SET 
         delivery_method = EXCLUDED.delivery_method,
         frequency = EXCLUDED.frequency,
         notification_template = EXCLUDED.notification_template,
         preferences = EXCLUDED.preferences,
         updated_at = CURRENT_TIMESTAMP,
         updated_by = EXCLUDED.created_by
       RETURNING subscription_id, created_at
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | subscription_id | Generated UUID | Subscription identifier |
       | user_id | ARGUMENT.userContext.userId | User ID |
       | subscription_type | ARGUMENT.subscriptionData.type | Type of subscription |
       | subscription_name | ARGUMENT.subscriptionData.name | Subscription name |
       | resource_filter | ARGUMENT.subscriptionData.resourceFilter | Resource filter criteria |
       | delivery_method | ARGUMENT.subscriptionData.deliveryMethod | Delivery method |
       | frequency | ARGUMENT.subscriptionData.frequency | Notification frequency |
       | notification_template | ARGUMENT.subscriptionData.template | Notification template |
       | preferences | ARGUMENT.userPreferences | User preferences |
       | created_by | ARGUMENT.userContext.userId | User creating subscription |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | subscription_record | Created/updated subscription |
     - **Callback**: Use for result preparation

4. **Step 4: Update User Notification Settings**
   - **Description**: Update user's global notification settings if needed
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO user_notification_settings (
       user_id,
       email_notifications,
       in_app_notifications,
       notification_frequency,
       quiet_hours_start,
       quiet_hours_end,
       updated_at
       ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
       ON CONFLICT (user_id) 
       DO UPDATE SET 
         email_notifications = COALESCE(EXCLUDED.email_notifications, user_notification_settings.email_notifications),
         in_app_notifications = COALESCE(EXCLUDED.in_app_notifications, user_notification_settings.in_app_notifications),
         notification_frequency = COALESCE(EXCLUDED.notification_frequency, user_notification_settings.notification_frequency),
         quiet_hours_start = COALESCE(EXCLUDED.quiet_hours_start, user_notification_settings.quiet_hours_start),
         quiet_hours_end = COALESCE(EXCLUDED.quiet_hours_end, user_notification_settings.quiet_hours_end),
         updated_at = CURRENT_TIMESTAMP
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID |
       | email_notifications | ARGUMENT.userPreferences.emailEnabled | Email notification preference |
       | in_app_notifications | ARGUMENT.userPreferences.inAppEnabled | In-app notification preference |
       | notification_frequency | ARGUMENT.userPreferences.frequency | Overall frequency preference |
       | quiet_hours_start | ARGUMENT.userPreferences.quietHoursStart | Quiet hours start time |
       | quiet_hours_end | ARGUMENT.userPreferences.quietHoursEnd | Quiet hours end time |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | settings_update | Updated notification settings |
     - **Callback**: Complete subscription setup

5. **Step 5: Retrieve Active Subscriptions**
   - **Description**: Retrieve user's active subscriptions after operation
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       subscription_id,
       subscription_type,
       subscription_name,
       resource_filter,
       delivery_method,
       frequency,
       status,
       created_at,
       updated_at
       FROM notification_subscriptions 
       WHERE user_id = ?
       AND status = 'active'
       ORDER BY created_at DESC
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | active_subscriptions | User's active subscriptions |
     - **Callback**: Include in final result

6. **Final Step: Return Subscription Management Results**
   - Return subscription ID, operation result, and active subscriptions list

---

### DAO ID: DAO-MDE-03-07-04
### DAO Name: Notification History

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | historyQuery | Object | Required | Query parameters for notification history |
| 2 | timeRange | Object | Optional | Time range for history query |
| 3 | filterCriteria | Object | Optional | Additional filter criteria |
| 4 | userContext | Object | Required | User context for access control |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | notificationHistory | Array | Notification history records |
| 2 | deliveryStatistics | Object | Delivery statistics summary |
| 3 | queryMetadata | Object | Query execution metadata |

### Steps:

1. **Step 1: Validate History Query**
   - **Description**: Validate notification history query parameters
   - **Data Validation**: 
     - Check history query parameters and time range
     - Validate filter criteria and user permissions
     - Ensure user has access to notification history
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Query Notification History**
   - **Description**: Query notification history with filters and pagination
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       n.notification_id,
       n.notification_type,
       n.title,
       n.content,
       n.priority,
       n.status as notification_status,
       n.created_at,
       n.scheduled_at,
       n.expiry_at,
       n.created_by,
       u.full_name as created_by_name,
       COUNT(nr.recipient_id) as total_recipients,
       COUNT(CASE WHEN nr.status = 'delivered' THEN 1 END) as delivered_count,
       COUNT(CASE WHEN nr.status = 'failed' THEN 1 END) as failed_count,
       COUNT(CASE WHEN nr.status = 'pending' THEN 1 END) as pending_count
       FROM notifications n
       LEFT JOIN notification_recipients nr ON n.notification_id = nr.notification_id
       LEFT JOIN users u ON n.created_by = u.user_id
       WHERE (n.created_by = ? OR ? IN ('admin', 'ra_all'))
       AND n.created_at BETWEEN ? AND ?
       [DYNAMIC_FILTER_CONDITIONS]
       GROUP BY n.notification_id, n.notification_type, n.title, n.content, 
                n.priority, n.status, n.created_at, n.scheduled_at, n.expiry_at, 
                n.created_by, u.full_name
       ORDER BY n.created_at DESC
       LIMIT ? OFFSET ?
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | start_date | ARGUMENT.timeRange.startDate | Query start date |
       | end_date | ARGUMENT.timeRange.endDate | Query end date |
       | limit | ARGUMENT.historyQuery.limit | Query result limit |
       | offset | ARGUMENT.historyQuery.offset | Query result offset |
       | filter_params | ARGUMENT.filterCriteria | Dynamic filter parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | notification_history | Notification history records |
     - **Callback**: Process for detailed view

3. **Step 3: Get Delivery Details**
   - **Description**: Get detailed delivery information for notifications
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       nr.notification_id,
       nr.recipient_id,
       nr.recipient_type,
       nr.delivery_method,
       nr.status as delivery_status,
       nr.delivered_at,
       nr.read_at,
       nr.error_message,
       CASE 
         WHEN nr.recipient_type = 'user' THEN u.full_name
         WHEN nr.recipient_type = 'group' THEN g.group_name
         ELSE nr.recipient_id
       END as recipient_name
       FROM notification_recipients nr
       LEFT JOIN users u ON nr.recipient_id = u.user_id AND nr.recipient_type = 'user'
       LEFT JOIN user_groups g ON nr.recipient_id = g.group_id AND nr.recipient_type = 'group'
       WHERE nr.notification_id IN (
         SELECT notification_id FROM notification_history_temp
       )
       ORDER BY nr.notification_id, nr.created_at
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | None | None | Uses temporary table from previous step |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | delivery_details | Detailed delivery information |
     - **Callback**: Combine with history records

4. **Step 4: Calculate Delivery Statistics**
   - **Description**: Calculate overall delivery statistics for the query period
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(DISTINCT n.notification_id) as total_notifications,
       COUNT(nr.recipient_id) as total_deliveries,
       COUNT(CASE WHEN nr.status = 'delivered' THEN 1 END) as successful_deliveries,
       COUNT(CASE WHEN nr.status = 'failed' THEN 1 END) as failed_deliveries,
       COUNT(CASE WHEN nr.status = 'pending' THEN 1 END) as pending_deliveries,
       ROUND(
         COUNT(CASE WHEN nr.status = 'delivered' THEN 1 END) * 100.0 / 
         NULLIF(COUNT(nr.recipient_id), 0), 2
       ) as delivery_success_rate,
       AVG(EXTRACT(EPOCH FROM (nr.delivered_at - n.created_at))) as avg_delivery_time_seconds
       FROM notifications n
       LEFT JOIN notification_recipients nr ON n.notification_id = nr.notification_id
       WHERE (n.created_by = ? OR ? IN ('admin', 'ra_all'))
       AND n.created_at BETWEEN ? AND ?
       [DYNAMIC_FILTER_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | start_date | ARGUMENT.timeRange.startDate | Query start date |
       | end_date | ARGUMENT.timeRange.endDate | Query end date |
       | filter_params | ARGUMENT.filterCriteria | Dynamic filter parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | delivery_statistics | Overall delivery statistics |
     - **Callback**: Include in final results

5. **Step 5: Get Query Metadata**
   - **Description**: Generate metadata about the query execution
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: SELECT 
       COUNT(*) as total_matching_records,
       MIN(created_at) as earliest_notification,
       MAX(created_at) as latest_notification,
       COUNT(DISTINCT notification_type) as unique_types,
       COUNT(DISTINCT created_by) as unique_senders
       FROM notifications 
       WHERE (created_by = ? OR ? IN ('admin', 'ra_all'))
       AND created_at BETWEEN ? AND ?
       [DYNAMIC_FILTER_CONDITIONS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | start_date | ARGUMENT.timeRange.startDate | Query start date |
       | end_date | ARGUMENT.timeRange.endDate | Query end date |
       | filter_params | ARGUMENT.filterCriteria | Dynamic filter parameters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | query_metadata | Query execution metadata |
     - **Callback**: Include in final results

6. **Final Step: Return Notification History Results**
   - Return notification history, delivery statistics, and query metadata

---

### DAO ID: DAO-MDE-03-07-05
### DAO Name: Alert Rules Engine

### Arguments:

| No | Name | Data Type | Constraint | Description |
|----|------|-----------|------------|-------------|
| 1 | ruleDefinition | Object | Required | Alert rule definition and conditions |
| 2 | ruleAction | String | Required | Action type (create/update/delete/evaluate) |
| 3 | evaluationContext | Object | Optional | Context for rule evaluation |
| 4 | userContext | Object | Required | User context for authorization |

### Returns:

| No | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | ruleId | String | Alert rule ID |
| 2 | evaluationResult | Object | Rule evaluation result |
| 3 | triggeredActions | Array | Actions triggered by rule |

### Steps:

1. **Step 1: Validate Rule Request**
   - **Description**: Validate alert rule definition and user permissions
   - **Data Validation**: 
     - Check rule definition structure and conditions
     - Validate rule action and evaluation context
     - Ensure user has rule management permissions
   - **SQL Call**: None
   - **Callback**: Return validation errors if invalid

2. **Step 2: Create/Update Alert Rule**
   - **Description**: Create new or update existing alert rule
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO alert_rules (
       rule_id,
       rule_name,
       rule_description,
       rule_conditions,
       severity_level,
       notification_actions,
       escalation_rules,
       status,
       created_by,
       created_at
       ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, CURRENT_TIMESTAMP)
       ON CONFLICT (rule_name, created_by) 
       DO UPDATE SET 
         rule_description = EXCLUDED.rule_description,
         rule_conditions = EXCLUDED.rule_conditions,
         severity_level = EXCLUDED.severity_level,
         notification_actions = EXCLUDED.notification_actions,
         escalation_rules = EXCLUDED.escalation_rules,
         updated_at = CURRENT_TIMESTAMP,
         updated_by = EXCLUDED.created_by
       RETURNING rule_id, created_at
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | rule_id | Generated UUID | Rule identifier |
       | rule_name | ARGUMENT.ruleDefinition.name | Rule name |
       | rule_description | ARGUMENT.ruleDefinition.description | Rule description |
       | rule_conditions | ARGUMENT.ruleDefinition.conditions | Rule conditions JSON |
       | severity_level | ARGUMENT.ruleDefinition.severity | Alert severity level |
       | notification_actions | ARGUMENT.ruleDefinition.actions | Notification actions JSON |
       | escalation_rules | ARGUMENT.ruleDefinition.escalation | Escalation rules JSON |
       | created_by | ARGUMENT.userContext.userId | User creating rule |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | rule_record | Created/updated rule record |
     - **Callback**: Use rule ID for evaluation

3. **Step 3: Evaluate Rule Conditions**
   - **Description**: Evaluate rule conditions against current data
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: WITH rule_evaluation AS (
       SELECT 
         ir.resource_id,
         ir.status,
         ir.availability_end,
         ir.created_at,
         ir.updated_at,
         EXTRACT(DAYS FROM (CURRENT_DATE - ir.updated_at)) as days_since_update,
         EXTRACT(DAYS FROM (ir.availability_end - CURRENT_DATE)) as days_until_expiry
       FROM idle_resources ir 
       WHERE ir.status != 'deleted'
       AND (ir.department_id IN (SELECT department_id FROM user_departments WHERE user_id = ?) OR ? = 'admin')
       )
       SELECT 
         resource_id,
         status,
         availability_end,
         CASE 
           WHEN [DYNAMIC_RULE_CONDITIONS] THEN true
           ELSE false
         END as condition_met
       FROM rule_evaluation
       WHERE [DYNAMIC_EVALUATION_FILTERS]
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | user_id | ARGUMENT.userContext.userId | User ID for access control |
       | user_role | ARGUMENT.userContext.role | User role for admin access |
       | rule_conditions | ARGUMENT.ruleDefinition.conditions | Dynamic rule conditions |
       | evaluation_filters | ARGUMENT.evaluationContext | Evaluation context filters |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | evaluation_results | Rule evaluation results |
     - **Callback**: Process condition matches

4. **Step 4: Log Rule Execution**
   - **Description**: Log rule execution and results
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO alert_rule_executions (
       execution_id,
       rule_id,
       executed_at,
       execution_result,
       conditions_met,
       resources_affected,
       actions_triggered
       ) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?)
       RETURNING execution_id
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | execution_id | Generated UUID | Execution identifier |
       | rule_id | Previous step result | Rule ID |
       | execution_result | Evaluation summary | Overall execution result |
       | conditions_met | Condition results | Number of conditions met |
       | resources_affected | Affected resources | Resources matching conditions |
       | actions_triggered | Triggered actions | Actions that were triggered |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | execution_record | Rule execution record |
     - **Callback**: Track rule performance

5. **Step 5: Trigger Automated Actions**
   - **Description**: Trigger automated actions based on rule evaluation
   - **Data Validation**: None
   - **SQL Call**: 
     - **SQL**: INSERT INTO automated_actions (
       action_id,
       rule_id,
       action_type,
       target_resources,
       action_parameters,
       status,
       scheduled_at,
       created_at
       )
       SELECT 
         gen_random_uuid(),
         ?,
         action_type,
         target_resources,
         action_parameters,
         'pending',
         CURRENT_TIMESTAMP + COALESCE(delay_interval, INTERVAL '0 seconds'),
         CURRENT_TIMESTAMP
       FROM json_to_recordset(?) AS actions(
         action_type text,
         target_resources jsonb,
         action_parameters jsonb,
         delay_interval interval
       )
       RETURNING action_id, action_type, scheduled_at
     - **Arguments**:
       | Name | Value | Description |
       |------|-------|-------------|
       | rule_id | Previous step result | Rule ID |
       | actions_json | Rule actions to trigger | Automated actions as JSON |
     - **Returns**:
       | Name | Description |
       |------|-------------|
       | triggered_actions | Triggered automated actions |
     - **Callback**: Include in final results

6. **Final Step: Return Alert Rule Results**
   - Return rule ID, evaluation result, and triggered actions
