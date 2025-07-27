# DAO Detailed Design Document

**Document ID**: DAO-MDE-03-10  
**Document Name**: Performance and Monitoring DAO Design

---

## Cover

**Document ID**: DAO-MDE-03-10  
**Document Name**: Performance and Monitoring DAO Design  
**Version**: v0.1  
**Date**: 2025-Jan-25  
**Prepared by**: System Analyst  

---

## History

| No | Date        | Version | Account        | Action     | Impacted Sections | Description                                    |
|----|-------------|---------|----------------|------------|-------------------|------------------------------------------------|
| 1  | 2025-Jan-25 | v0.1    | System Analyst | Initialize | Whole Document    | Initial creation of Performance and Monitoring DAO Design |

---

## DAOs

| No | ID                 | Name                           | Description                                           |
|----|--------------------|---------------------------------|-------------------------------------------------------|
| 1  | DAO-MDE-03-10-01   | Performance Metrics DAO        | Collects and manages system performance metrics      |
| 2  | DAO-MDE-03-10-02   | System Monitoring DAO          | Handles system health monitoring and alerts         |
| 3  | DAO-MDE-03-10-03   | Health Check DAO               | Performs comprehensive system health checks          |
| 4  | DAO-MDE-03-10-04   | Optimization Query DAO         | Manages database and query optimization              |
| 5  | DAO-MDE-03-10-05   | Diagnostic Operations DAO      | Handles system diagnostics and troubleshooting      |

---

## Logic & Flow

### DAO ID: DAO-MDE-03-10-01
### DAO Name: Performance Metrics DAO

#### Arguments:
| No | Name           | Data Type | Constraint | Description                              |
|----|----------------|-----------|------------|------------------------------------------|
| 1  | metric_name    | String    | Required   | Performance metric name                  |
| 2  | metric_value   | Decimal   | Required   | Metric value                             |
| 3  | metric_unit    | String    | Required   | Unit of measurement                      |
| 4  | component      | String    | Optional   | System component being measured          |
| 5  | timestamp      | DateTime  | Optional   | Metric collection timestamp              |

#### Returns:
| No | Name           | Data Type | Description                              |
|----|----------------|-----------|------------------------------------------|
| 1  | metric_id      | String    | Performance metric identifier            |
| 2  | metric_name    | String    | Metric name                              |
| 3  | current_value  | Decimal   | Current metric value                     |
| 4  | trend_direction| String    | Trend direction (up, down, stable)      |
| 5  | alert_level    | String    | Alert level based on thresholds         |

#### Steps:

1. **Step 1:**
   - Description: Validate and store performance metric with timestamp
   - Data Validation: Validate metric_name format, verify metric_value range, validate metric_unit values
   - SQL Call:
     - SQL: `INSERT INTO performance_metrics (metric_name, metric_value, metric_unit, component, recorded_at, created_at) VALUES ($1, $2, $3, $4, COALESCE($5, NOW()), NOW()) RETURNING metric_id, metric_name, metric_value, recorded_at`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | metric_name    | ARGUMENT.metric_name     | Performance metric name                  |
       | metric_value   | ARGUMENT.metric_value    | Metric value                             |
       | metric_unit    | ARGUMENT.metric_unit     | Unit of measurement                      |
       | component      | ARGUMENT.component       | System component                         |
       | timestamp      | ARGUMENT.timestamp       | Collection timestamp                     |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | metric_id      | Performance metric identifier            |
       | metric_name    | Metric name                              |
       | metric_value   | Recorded metric value                    |
       | recorded_at    | Recording timestamp                      |
     - Callback: Calculate trend analysis and check thresholds

2. **Step 2:**
   - Description: Calculate trend analysis and compare with historical data
   - SQL Call:
     - SQL: `WITH trend_analysis AS (SELECT metric_name, metric_value, LAG(metric_value, 1) OVER (PARTITION BY metric_name ORDER BY recorded_at) as prev_value, LAG(metric_value, 5) OVER (PARTITION BY metric_name ORDER BY recorded_at) as prev_5_value FROM performance_metrics WHERE metric_name = $1 AND recorded_at >= NOW() - INTERVAL '1 hour' ORDER BY recorded_at DESC LIMIT 1), trend_calc AS (SELECT ta.metric_value as current_value, (CASE WHEN ta.prev_value IS NULL THEN 'stable' WHEN ta.metric_value > ta.prev_value * 1.1 THEN 'up' WHEN ta.metric_value < ta.prev_value * 0.9 THEN 'down' ELSE 'stable' END) as trend_direction FROM trend_analysis ta) UPDATE performance_metrics SET trend_direction = tc.trend_direction WHERE metric_id = $2 FROM trend_calc tc RETURNING metric_id, metric_value as current_value, trend_direction`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | metric_name    | metric_name              | Metric name for trend analysis           |
       | metric_id      | metric_id                | Metric ID from step 1                    |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | metric_id      | Metric identifier                        |
       | current_value  | Current metric value                     |
       | trend_direction| Calculated trend direction               |
     - Callback: Check alert thresholds

3. **Step 3:**
   - Description: Check metric against defined thresholds and generate alerts
   - SQL Call:
     - SQL: `WITH threshold_check AS (SELECT mt.warning_threshold, mt.critical_threshold, mt.alert_enabled FROM metric_thresholds mt WHERE mt.metric_name = $1), alert_level_calc AS (SELECT (CASE WHEN tc.critical_threshold IS NOT NULL AND $2 >= tc.critical_threshold THEN 'critical' WHEN tc.warning_threshold IS NOT NULL AND $2 >= tc.warning_threshold THEN 'warning' ELSE 'normal' END) as alert_level, tc.alert_enabled FROM threshold_check tc) UPDATE performance_metrics SET alert_level = alc.alert_level WHERE metric_id = $3 FROM alert_level_calc alc RETURNING metric_id, alert_level`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | metric_name    | metric_name              | Metric name for threshold check          |
       | metric_value   | current_value            | Current metric value                     |
       | metric_id      | metric_id                | Metric ID                                |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | metric_id      | Metric identifier                        |
       | alert_level    | Calculated alert level                   |
     - Callback: Update performance summary and return results

4. **Step 4:**
   - Description: Update performance summary statistics and create alerts if needed
   - SQL Call:
     - SQL: `WITH alert_creation AS (INSERT INTO performance_alerts (metric_id, metric_name, alert_level, metric_value, component, triggered_at) SELECT $1, $2, $3, $4, $5, NOW() WHERE $3 IN ('warning', 'critical') RETURNING alert_id), summary_update AS (INSERT INTO performance_summary (metric_name, component, min_value, max_value, avg_value, sample_count, last_updated) VALUES ($2, $5, $4, $4, $4, 1, NOW()) ON CONFLICT (metric_name, component, DATE(last_updated)) DO UPDATE SET min_value = LEAST(performance_summary.min_value, $4), max_value = GREATEST(performance_summary.max_value, $4), avg_value = (performance_summary.avg_value * performance_summary.sample_count + $4) / (performance_summary.sample_count + 1), sample_count = performance_summary.sample_count + 1, last_updated = NOW() RETURNING metric_name, avg_value) SELECT COALESCE(ac.alert_id, 'no_alert') as alert_id, su.avg_value FROM alert_creation ac FULL OUTER JOIN summary_update su ON true`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | metric_id      | metric_id                | Metric identifier                        |
       | metric_name    | metric_name              | Metric name                              |
       | alert_level    | alert_level              | Alert level from step 3                  |
       | metric_value   | current_value            | Current metric value                     |
       | component      | component                | System component                         |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | alert_id       | Alert ID if created                      |
       | avg_value      | Average value for component              |
     - Callback: Return complete performance metric details

5. **Final Step:** Return complete performance metric analysis with trend direction, alert level assessment, threshold monitoring, and automated alerting for system performance tracking.

---

### DAO ID: DAO-MDE-03-10-02
### DAO Name: System Monitoring DAO

#### Arguments:
| No | Name           | Data Type | Constraint | Description                              |
|----|----------------|-----------|------------|------------------------------------------|
| 1  | monitor_type   | String    | Required   | Type of monitoring (CPU, memory, disk, network) |
| 2  | resource_id    | String    | Required   | Resource identifier being monitored      |
| 3  | threshold_config| JSON     | Optional   | Custom threshold configuration          |
| 4  | alert_contacts | Array     | Optional   | Contact list for alerts                 |
| 5  | monitoring_interval| Integer| Optional   | Monitoring interval in seconds          |

#### Returns:
| No | Name           | Data Type | Description                              |
|----|----------------|-----------|------------------------------------------|
| 1  | monitor_id     | String    | System monitor identifier                |
| 2  | status         | String    | Current monitoring status                |
| 3  | last_check     | DateTime  | Last monitoring check timestamp          |
| 4  | health_score   | Decimal   | Overall health score (0-100)            |
| 5  | active_alerts  | Integer   | Number of active alerts                  |

#### Steps:

1. **Step 1:**
   - Description: Create system monitor configuration and validate parameters
   - Data Validation: Validate monitor_type values, verify resource_id exists, validate threshold_config JSON
   - SQL Call:
     - SQL: `INSERT INTO system_monitors (monitor_type, resource_id, threshold_config, alert_contacts, monitoring_interval, status, created_at, updated_at) VALUES ($1, $2, $3, $4, COALESCE($5, 60), 'active', NOW(), NOW()) RETURNING monitor_id, status, created_at`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | monitor_type   | ARGUMENT.monitor_type    | Type of monitoring                       |
       | resource_id    | ARGUMENT.resource_id     | Resource identifier                      |
       | threshold_config| ARGUMENT.threshold_config| Threshold configuration JSON            |
       | alert_contacts | ARGUMENT.alert_contacts  | Alert contact list                       |
       | monitoring_interval| ARGUMENT.monitoring_interval| Monitoring interval                  |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | monitor_id     | System monitor identifier                |
       | status         | Monitor status                           |
       | created_at     | Creation timestamp                       |
     - Callback: Initialize monitoring baseline and start monitoring

2. **Step 2:**
   - Description: Perform initial monitoring check and establish baseline
   - SQL Call:
     - SQL: `WITH baseline_check AS (INSERT INTO monitoring_checks (monitor_id, monitor_type, resource_id, check_timestamp, status, response_time, resource_usage, created_at) VALUES ($1, $2, $3, NOW(), 'healthy', 0, '{}', NOW()) RETURNING check_id, check_timestamp), health_calc AS (SELECT 100.0 as initial_health_score) UPDATE system_monitors SET last_check = bc.check_timestamp, health_score = hc.initial_health_score FROM baseline_check bc, health_calc hc WHERE monitor_id = $1 RETURNING monitor_id, last_check, health_score`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | monitor_id     | monitor_id               | Monitor ID from step 1                   |
       | monitor_type   | monitor_type             | Monitor type                             |
       | resource_id    | resource_id              | Resource identifier                      |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | monitor_id     | Monitor identifier                       |
       | last_check     | Last check timestamp                     |
       | health_score   | Initial health score                     |
     - Callback: Set up monitoring schedule and alerts

3. **Step 3:**
   - Description: Execute comprehensive monitoring checks and update health metrics
   - SQL Call:
     - SQL: `WITH current_check AS (INSERT INTO monitoring_checks (monitor_id, monitor_type, resource_id, check_timestamp, status, response_time, resource_usage, errors, created_at) VALUES ($1, $2, $3, NOW(), $4, $5, $6, $7, NOW()) RETURNING check_id, status, response_time), health_update AS (SELECT (CASE WHEN cc.status = 'healthy' THEN LEAST(100.0, sm.health_score + 1) WHEN cc.status = 'warning' THEN GREATEST(sm.health_score - 5, 50.0) WHEN cc.status = 'critical' THEN GREATEST(sm.health_score - 20, 0.0) ELSE sm.health_score END) as new_health_score FROM current_check cc, system_monitors sm WHERE sm.monitor_id = $1) UPDATE system_monitors SET last_check = NOW(), health_score = hu.new_health_score FROM health_update hu WHERE monitor_id = $1 RETURNING monitor_id, last_check, health_score`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | monitor_id     | monitor_id               | Monitor identifier                       |
       | monitor_type   | monitor_type             | Monitor type                             |
       | resource_id    | resource_id              | Resource identifier                      |
       | check_status   | monitoring_result_status | Result of monitoring check               |
       | response_time  | check_response_time      | Response time from check                 |
       | resource_usage | resource_usage_data      | Resource usage data JSON                 |
       | errors         | error_details            | Error details if any                     |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | monitor_id     | Monitor identifier                       |
       | last_check     | Last check timestamp                     |
       | health_score   | Updated health score                     |
     - Callback: Check for alert conditions

4. **Step 4:**
   - Description: Evaluate alert conditions and manage active alerts
   - SQL Call:
     - SQL: `WITH alert_evaluation AS (SELECT COUNT(*) as alert_count FROM monitoring_alerts WHERE monitor_id = $1 AND status = 'active'), new_alerts AS (INSERT INTO monitoring_alerts (monitor_id, alert_type, severity, message, triggered_at, status) SELECT $1, 'health_degraded', CASE WHEN $2 < 30 THEN 'critical' WHEN $2 < 60 THEN 'warning' ELSE 'info' END, 'Health score dropped to ' || $2::text, NOW(), 'active' WHERE $2 < 80 AND NOT EXISTS (SELECT 1 FROM monitoring_alerts WHERE monitor_id = $1 AND alert_type = 'health_degraded' AND status = 'active') RETURNING alert_id), resolved_alerts AS (UPDATE monitoring_alerts SET status = 'resolved', resolved_at = NOW() WHERE monitor_id = $1 AND alert_type = 'health_degraded' AND status = 'active' AND $2 >= 80 RETURNING alert_id) SELECT COALESCE(ae.alert_count + COALESCE((SELECT COUNT(*) FROM new_alerts), 0) - COALESCE((SELECT COUNT(*) FROM resolved_alerts), 0), 0) as active_alerts FROM alert_evaluation ae`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | monitor_id     | monitor_id               | Monitor identifier                       |
       | health_score   | health_score             | Current health score                     |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | active_alerts  | Number of active alerts                  |
     - Callback: Update monitoring status and return results

5. **Step 5:**
   - Description: Update overall monitoring status and generate summary
   - SQL Call:
     - SQL: `UPDATE system_monitors SET status = (CASE WHEN $1 >= 80 THEN 'healthy' WHEN $1 >= 50 THEN 'warning' ELSE 'critical' END), active_alerts = $2, last_updated = NOW() WHERE monitor_id = $3 RETURNING monitor_id, status, last_check, health_score, active_alerts`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | health_score   | health_score             | Current health score                     |
       | active_alerts  | active_alerts            | Number of active alerts                  |
       | monitor_id     | monitor_id               | Monitor identifier                       |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | monitor_id     | Monitor identifier                       |
       | status         | Current monitoring status                |
       | last_check     | Last check timestamp                     |
       | health_score   | Current health score                     |
       | active_alerts  | Number of active alerts                  |
     - Callback: Return monitoring status details

6. **Final Step:** Return complete system monitoring status with health scoring, alert management, baseline tracking, and automated monitoring for comprehensive system health oversight.

---

### DAO ID: DAO-MDE-03-10-03
### DAO Name: Health Check DAO

#### Arguments:
| No | Name           | Data Type | Constraint | Description                              |
|----|----------------|-----------|------------|------------------------------------------|
| 1  | check_type     | String    | Required   | Health check type (database, api, service, external) |
| 2  | target_endpoint| String    | Required   | Target endpoint or service to check      |
| 3  | check_parameters| JSON     | Optional   | Check-specific parameters               |
| 4  | timeout_seconds| Integer   | Optional   | Check timeout in seconds                |
| 5  | retry_count    | Integer   | Optional   | Number of retries on failure            |

#### Returns:
| No | Name           | Data Type | Description                              |
|----|----------------|-----------|------------------------------------------|
| 1  | check_id       | String    | Health check identifier                  |
| 2  | status         | String    | Health check status                      |
| 3  | response_time  | Integer   | Response time in milliseconds            |
| 4  | details        | JSON      | Detailed check results                   |
| 5  | next_check     | DateTime  | Next scheduled check time                |

#### Steps:

1. **Step 1:**
   - Description: Initialize health check session and validate parameters
   - Data Validation: Validate check_type values, verify target_endpoint format, validate check_parameters JSON
   - SQL Call:
     - SQL: `INSERT INTO health_checks (check_type, target_endpoint, check_parameters, timeout_seconds, retry_count, status, started_at, created_at) VALUES ($1, $2, $3, COALESCE($4, 30), COALESCE($5, 3), 'running', NOW(), NOW()) RETURNING check_id, started_at`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | check_type     | ARGUMENT.check_type      | Health check type                        |
       | target_endpoint| ARGUMENT.target_endpoint | Target endpoint                          |
       | check_parameters| ARGUMENT.check_parameters| Check parameters JSON                   |
       | timeout_seconds| ARGUMENT.timeout_seconds | Check timeout                            |
       | retry_count    | ARGUMENT.retry_count     | Retry count                              |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | check_id       | Health check identifier                  |
       | started_at     | Check start timestamp                    |
     - Callback: Execute health check based on type

2. **Step 2:**
   - Description: Execute health check with retry logic and measure response time
   - SQL Call:
     - SQL: `WITH check_execution AS (UPDATE health_checks SET status = $1, response_time = $2, attempts_made = $3, completed_at = NOW() WHERE check_id = $4 RETURNING check_id, status, response_time, completed_at), check_details AS (INSERT INTO health_check_details (check_id, attempt_number, status, response_time, error_message, details, checked_at) VALUES ($4, $3, $1, $2, $5, $6, NOW()) RETURNING check_id, details) SELECT ce.check_id, ce.status, ce.response_time, ce.completed_at, cd.details FROM check_execution ce JOIN check_details cd ON ce.check_id = cd.check_id`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | final_status   | check_result_status      | Final check status                       |
       | response_time  | check_response_time      | Response time in milliseconds            |
       | attempts_made  | retry_attempts           | Number of attempts made                  |
       | check_id       | check_id                 | Check ID from step 1                     |
       | error_message  | error_details            | Error message if check failed            |
       | details        | check_result_details     | Detailed check results JSON              |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | check_id       | Check identifier                         |
       | status         | Final check status                       |
       | response_time  | Response time                            |
       | completed_at   | Completion timestamp                     |
       | details        | Detailed results                         |
     - Callback: Update health check statistics

3. **Step 3:**
   - Description: Update health check statistics and calculate availability metrics
   - SQL Call:
     - SQL: `WITH stats_update AS (INSERT INTO health_check_stats (check_type, target_endpoint, total_checks, successful_checks, failed_checks, avg_response_time, last_check_at) VALUES ($1, $2, 1, CASE WHEN $3 = 'healthy' THEN 1 ELSE 0 END, CASE WHEN $3 = 'healthy' THEN 0 ELSE 1 END, $4, NOW()) ON CONFLICT (check_type, target_endpoint, DATE(last_check_at)) DO UPDATE SET total_checks = health_check_stats.total_checks + 1, successful_checks = health_check_stats.successful_checks + CASE WHEN $3 = 'healthy' THEN 1 ELSE 0 END, failed_checks = health_check_stats.failed_checks + CASE WHEN $3 = 'healthy' THEN 0 ELSE 1 END, avg_response_time = (health_check_stats.avg_response_time * health_check_stats.total_checks + $4) / (health_check_stats.total_checks + 1), last_check_at = NOW() RETURNING total_checks, successful_checks, avg_response_time), availability_calc AS (SELECT ROUND((su.successful_checks::decimal / su.total_checks * 100), 2) as availability_percentage FROM stats_update su) SELECT ac.availability_percentage FROM availability_calc ac`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | check_type     | check_type               | Health check type                        |
       | target_endpoint| target_endpoint          | Target endpoint                          |
       | status         | status                   | Check status                             |
       | response_time  | response_time            | Response time                            |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | availability_percentage| Service availability percentage      |
     - Callback: Schedule next health check

4. **Step 4:**
   - Description: Schedule next health check and update monitoring schedule
   - SQL Call:
     - SQL: `INSERT INTO health_check_schedule (check_type, target_endpoint, next_check, frequency, last_check_id) VALUES ($1, $2, NOW() + INTERVAL '5 minutes', 'every_5_minutes', $3) ON CONFLICT (check_type, target_endpoint) DO UPDATE SET next_check = NOW() + INTERVAL '5 minutes', last_check_id = $3, updated_at = NOW() RETURNING check_type, next_check`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | check_type     | check_type               | Health check type                        |
       | target_endpoint| target_endpoint          | Target endpoint                          |
       | check_id       | check_id                 | Current check ID                         |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | check_type     | Check type                               |
       | next_check     | Next scheduled check time                |
     - Callback: Return health check results

5. **Final Step:** Return complete health check results with status assessment, response time measurement, availability calculation, and automated scheduling for continuous health monitoring.

---

### DAO ID: DAO-MDE-03-10-04
### DAO Name: Optimization Query DAO

#### Arguments:
| No | Name           | Data Type | Constraint | Description                              |
|----|----------------|-----------|------------|------------------------------------------|
| 1  | query_type     | String    | Required   | Query optimization type (slow_queries, index_usage, table_stats) |
| 2  | target_schema  | String    | Optional   | Target database schema                   |
| 3  | analysis_period| Integer   | Optional   | Analysis period in hours                 |
| 4  | optimization_level| String | Optional   | Optimization level (basic, advanced, aggressive) |
| 5  | auto_apply     | Boolean   | Optional   | Whether to auto-apply safe optimizations |

#### Returns:
| No | Name           | Data Type | Description                              |
|----|----------------|-----------|------------------------------------------|
| 1  | analysis_id    | String    | Query analysis identifier                |
| 2  | recommendations| JSON      | Optimization recommendations             |
| 3  | potential_improvement| Decimal| Estimated performance improvement %   |
| 4  | applied_optimizations| Integer| Number of optimizations applied      |
| 5  | next_analysis  | DateTime  | Next recommended analysis time           |

#### Steps:

1. **Step 1:**
   - Description: Initialize query optimization analysis and gather baseline metrics
   - Data Validation: Validate query_type values, verify target_schema exists, validate optimization_level values
   - SQL Call:
     - SQL: `INSERT INTO query_optimization_analysis (query_type, target_schema, analysis_period, optimization_level, auto_apply, status, started_at, created_at) VALUES ($1, $2, COALESCE($3, 24), COALESCE($4, 'basic'), COALESCE($5, false), 'running', NOW(), NOW()) RETURNING analysis_id, started_at`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | query_type     | ARGUMENT.query_type      | Query optimization type                  |
       | target_schema  | ARGUMENT.target_schema   | Target schema                            |
       | analysis_period| ARGUMENT.analysis_period | Analysis period                          |
       | optimization_level| ARGUMENT.optimization_level| Optimization level                    |
       | auto_apply     | ARGUMENT.auto_apply      | Auto-apply flag                          |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | analysis_id    | Analysis identifier                      |
       | started_at     | Analysis start timestamp                 |
     - Callback: Collect query performance metrics

2. **Step 2:**
   - Description: Analyze slow queries and identify optimization opportunities
   - SQL Call:
     - SQL: `WITH slow_queries AS (SELECT query, total_time, mean_time, calls, rows FROM pg_stat_statements WHERE mean_time > 1000 AND calls > 10 ORDER BY total_time DESC LIMIT 50), query_analysis AS (INSERT INTO query_analysis_results (analysis_id, query_hash, query_text, execution_time, call_count, optimization_type, recommendation, priority) SELECT $1, md5(sq.query), sq.query, sq.mean_time, sq.calls, 'slow_query', 'Consider adding index or rewriting query', CASE WHEN sq.mean_time > 5000 THEN 'high' WHEN sq.mean_time > 2000 THEN 'medium' ELSE 'low' END FROM slow_queries sq RETURNING analysis_id, COUNT(*) as recommendations_count) SELECT qa.recommendations_count FROM query_analysis qa`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | analysis_id    | analysis_id              | Analysis ID from step 1                  |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | recommendations_count| Number of recommendations generated   |
     - Callback: Analyze index usage and table statistics

3. **Step 3:**
   - Description: Analyze index usage and generate index optimization recommendations
   - SQL Call:
     - SQL: `WITH index_analysis AS (SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes WHERE idx_scan < 10 AND schemaname = COALESCE($2, 'public')), unused_indexes AS (INSERT INTO query_analysis_results (analysis_id, table_name, index_name, optimization_type, recommendation, priority, estimated_benefit) SELECT $1, ia.tablename, ia.indexname, 'unused_index', 'Consider dropping unused index: ' || ia.indexname, 'medium', 'Storage savings' FROM index_analysis ia RETURNING analysis_id, COUNT(*) as index_recommendations), table_stats AS (SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del, n_dead_tup FROM pg_stat_user_tables WHERE n_dead_tup > 1000), maintenance_recs AS (INSERT INTO query_analysis_results (analysis_id, table_name, optimization_type, recommendation, priority, estimated_benefit) SELECT $1, ts.tablename, 'maintenance', 'VACUUM/ANALYZE recommended for table: ' || ts.tablename, 'high', 'Query performance improvement' FROM table_stats ts RETURNING analysis_id, COUNT(*) as maintenance_count) SELECT ui.index_recommendations + mr.maintenance_count as total_recommendations FROM unused_indexes ui, maintenance_recs mr`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | analysis_id    | analysis_id              | Analysis identifier                      |
       | target_schema  | target_schema            | Target schema for analysis               |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | total_recommendations| Total optimization recommendations    |
     - Callback: Calculate potential improvements and apply safe optimizations

4. **Step 4:**
   - Description: Calculate potential performance improvements and apply safe optimizations
   - SQL Call:
     - SQL: `WITH improvement_calc AS (SELECT analysis_id, COUNT(*) as total_recs, COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_priority, COUNT(CASE WHEN optimization_type = 'maintenance' THEN 1 END) as maintenance_recs FROM query_analysis_results WHERE analysis_id = $1 GROUP BY analysis_id), potential_improvement AS (SELECT CASE WHEN ic.high_priority > 0 THEN 25.0 + (ic.maintenance_recs * 5.0) WHEN ic.total_recs > 0 THEN 10.0 + (ic.total_recs * 2.0) ELSE 0.0 END as improvement_percentage FROM improvement_calc ic), applied_optimizations AS (UPDATE query_analysis_results SET applied = true, applied_at = NOW() WHERE analysis_id = $1 AND $2 = true AND optimization_type = 'maintenance' AND priority = 'high' RETURNING COUNT(*) as applied_count) UPDATE query_optimization_analysis SET potential_improvement = pi.improvement_percentage, applied_optimizations = COALESCE(ao.applied_count, 0), completed_at = NOW(), status = 'completed' FROM potential_improvement pi, applied_optimizations ao WHERE analysis_id = $1 RETURNING analysis_id, potential_improvement, applied_optimizations`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | analysis_id    | analysis_id              | Analysis identifier                      |
       | auto_apply     | auto_apply               | Auto-apply flag                          |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | analysis_id    | Analysis identifier                      |
       | potential_improvement| Estimated improvement percentage       |
       | applied_optimizations| Number of applied optimizations        |
     - Callback: Generate optimization recommendations report

5. **Step 5:**
   - Description: Generate comprehensive optimization recommendations and schedule next analysis
   - SQL Call:
     - SQL: `WITH recommendations_summary AS (SELECT jsonb_object_agg(optimization_type, jsonb_build_object('count', type_count, 'recommendations', recommendations)) as recommendations_json FROM (SELECT optimization_type, COUNT(*) as type_count, jsonb_agg(jsonb_build_object('table', table_name, 'recommendation', recommendation, 'priority', priority, 'benefit', estimated_benefit)) as recommendations FROM query_analysis_results WHERE analysis_id = $1 GROUP BY optimization_type) grouped), next_analysis_schedule AS (INSERT INTO optimization_schedule (analysis_type, target_schema, next_analysis, frequency, last_analysis_id) VALUES ($2, $3, NOW() + INTERVAL '7 days', 'weekly', $1) ON CONFLICT (analysis_type, target_schema) DO UPDATE SET next_analysis = NOW() + INTERVAL '7 days', last_analysis_id = $1, updated_at = NOW() RETURNING next_analysis) SELECT rs.recommendations_json, nas.next_analysis FROM recommendations_summary rs, next_analysis_schedule nas`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | analysis_id    | analysis_id              | Analysis identifier                      |
       | query_type     | query_type               | Analysis type                            |
       | target_schema  | target_schema            | Target schema                            |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | recommendations_json| Comprehensive recommendations JSON       |
       | next_analysis  | Next scheduled analysis time             |
     - Callback: Return optimization analysis results

6. **Final Step:** Return complete query optimization analysis with performance recommendations, potential improvement estimates, applied optimizations tracking, and automated analysis scheduling for database performance management.

---

### DAO ID: DAO-MDE-03-10-05
### DAO Name: Diagnostic Operations DAO

#### Arguments:
| No | Name           | Data Type | Constraint | Description                              |
|----|----------------|-----------|------------|------------------------------------------|
| 1  | diagnostic_type| String    | Required   | Diagnostic type (system, database, application, network) |
| 2  | severity_level | String    | Required   | Issue severity (info, warning, error, critical) |
| 3  | component_path | String    | Optional   | Specific component or path to diagnose   |
| 4  | diagnostic_params| JSON    | Optional   | Diagnostic-specific parameters          |
| 5  | collect_logs   | Boolean   | Optional   | Whether to collect related logs          |

#### Returns:
| No | Name           | Data Type | Description                              |
|----|----------------|-----------|------------------------------------------|
| 1  | diagnostic_id  | String    | Diagnostic session identifier            |
| 2  | status         | String    | Diagnostic status                        |
| 3  | findings       | JSON      | Diagnostic findings and issues           |
| 4  | recommendations| JSON      | Recommended actions                      |
| 5  | log_references | Array     | References to collected logs             |

#### Steps:

1. **Step 1:**
   - Description: Initialize diagnostic session and validate parameters
   - Data Validation: Validate diagnostic_type values, verify severity_level values, validate diagnostic_params JSON
   - SQL Call:
     - SQL: `INSERT INTO diagnostic_sessions (diagnostic_type, severity_level, component_path, diagnostic_params, collect_logs, status, started_at, created_at) VALUES ($1, $2, $3, $4, COALESCE($5, false), 'running', NOW(), NOW()) RETURNING diagnostic_id, started_at`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | diagnostic_type| ARGUMENT.diagnostic_type | Diagnostic type                          |
       | severity_level | ARGUMENT.severity_level  | Issue severity level                     |
       | component_path | ARGUMENT.component_path  | Component path                           |
       | diagnostic_params| ARGUMENT.diagnostic_params| Diagnostic parameters JSON             |
       | collect_logs   | ARGUMENT.collect_logs    | Log collection flag                      |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | diagnostic_id  | Diagnostic session identifier            |
       | started_at     | Session start timestamp                  |
     - Callback: Execute diagnostic procedures based on type

2. **Step 2:**
   - Description: Execute diagnostic procedures and collect system information
   - SQL Call:
     - SQL: `WITH diagnostic_execution AS (INSERT INTO diagnostic_procedures (diagnostic_id, procedure_name, procedure_type, execution_order, status, started_at) SELECT $1, dp.procedure_name, dp.procedure_type, dp.execution_order, 'running', NOW() FROM default_procedures dp WHERE dp.diagnostic_type = $2 ORDER BY dp.execution_order RETURNING procedure_id, procedure_name), procedure_results AS (INSERT INTO diagnostic_results (diagnostic_id, procedure_id, result_type, result_data, severity, identified_at) SELECT $1, de.procedure_id, 'finding', '{"status": "executed", "timestamp": "' || NOW() || '"}', $3, NOW() FROM diagnostic_execution de RETURNING procedure_id, result_data) SELECT COUNT(*) as procedures_executed FROM procedure_results`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | diagnostic_id  | diagnostic_id            | Diagnostic ID from step 1                |
       | diagnostic_type| diagnostic_type          | Diagnostic type                          |
       | severity_level | severity_level           | Severity level                           |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | procedures_executed| Number of procedures executed          |
     - Callback: Analyze diagnostic results and identify issues

3. **Step 3:**
   - Description: Analyze diagnostic results and identify system issues
   - SQL Call:
     - SQL: `WITH issue_analysis AS (SELECT dr.result_data, dr.severity, dp.procedure_name FROM diagnostic_results dr JOIN diagnostic_procedures dp ON dr.procedure_id = dp.procedure_id WHERE dr.diagnostic_id = $1), findings_summary AS (INSERT INTO diagnostic_findings (diagnostic_id, finding_type, component, issue_description, severity, impact_level, found_at) SELECT $1, 'system_issue', $2, 'Diagnostic finding: ' || ia.procedure_name, ia.severity, CASE WHEN ia.severity = 'critical' THEN 'high' WHEN ia.severity = 'error' THEN 'medium' ELSE 'low' END, NOW() FROM issue_analysis ia RETURNING finding_id, finding_type, severity), recommendations_gen AS (INSERT INTO diagnostic_recommendations (diagnostic_id, recommendation_type, priority, action_description, estimated_effort, automated) SELECT $1, 'corrective_action', CASE WHEN fs.severity = 'critical' THEN 'urgent' WHEN fs.severity = 'error' THEN 'high' ELSE 'medium' END, 'Address ' || fs.finding_type || ' identified in diagnostics', 'medium', false FROM findings_summary fs RETURNING recommendation_id, priority) SELECT COUNT(*) as findings_count, COUNT(DISTINCT rg.recommendation_id) as recommendations_count FROM findings_summary fs LEFT JOIN recommendations_gen rg ON true`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | diagnostic_id  | diagnostic_id            | Diagnostic identifier                    |
       | component_path | component_path           | Component being diagnosed                |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | findings_count | Number of findings identified            |
       | recommendations_count| Number of recommendations generated    |
     - Callback: Collect logs if requested

4. **Step 4:**
   - Description: Collect relevant logs and system information if requested
   - SQL Call:
     - SQL: `WITH log_collection AS (INSERT INTO diagnostic_logs (diagnostic_id, log_type, log_source, log_content, collected_at) SELECT $1, 'system_log', 'application', '{"log_entries": "Sample log data for diagnostic ID ' || $1 || '"}', NOW() WHERE $2 = true RETURNING log_id, log_type), log_references AS (SELECT jsonb_agg(jsonb_build_object('log_id', lc.log_id, 'type', lc.log_type, 'timestamp', NOW())) as log_refs FROM log_collection lc) UPDATE diagnostic_sessions SET log_references = COALESCE(lr.log_refs, '[]'::jsonb) FROM log_references lr WHERE diagnostic_id = $1 RETURNING diagnostic_id, log_references`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | diagnostic_id  | diagnostic_id            | Diagnostic identifier                    |
       | collect_logs   | collect_logs             | Log collection flag                      |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | diagnostic_id  | Diagnostic identifier                    |
       | log_references | References to collected logs             |
     - Callback: Generate comprehensive diagnostic report

5. **Step 5:**
   - Description: Generate comprehensive diagnostic report and finalize session
   - SQL Call:
     - SQL: `WITH findings_report AS (SELECT jsonb_object_agg(finding_type, jsonb_build_object('count', type_count, 'findings', findings_list)) as findings_json FROM (SELECT finding_type, COUNT(*) as type_count, jsonb_agg(jsonb_build_object('component', component, 'description', issue_description, 'severity', severity, 'impact', impact_level)) as findings_list FROM diagnostic_findings WHERE diagnostic_id = $1 GROUP BY finding_type) grouped), recommendations_report AS (SELECT jsonb_object_agg(priority, jsonb_build_object('count', priority_count, 'actions', actions_list)) as recommendations_json FROM (SELECT priority, COUNT(*) as priority_count, jsonb_agg(jsonb_build_object('type', recommendation_type, 'description', action_description, 'effort', estimated_effort, 'automated', automated)) as actions_list FROM diagnostic_recommendations WHERE diagnostic_id = $1 GROUP BY priority) grouped) UPDATE diagnostic_sessions SET status = 'completed', findings = fr.findings_json, recommendations = rr.recommendations_json, completed_at = NOW() FROM findings_report fr, recommendations_report rr WHERE diagnostic_id = $1 RETURNING diagnostic_id, status, findings, recommendations, log_references`
     - Arguments:
       | Name           | Value                    | Description                              |
       |----------------|--------------------------|------------------------------------------|
       | diagnostic_id  | diagnostic_id            | Diagnostic identifier                    |
     - Returns:
       | Name           | Description                              |
       |----------------|------------------------------------------|
       | diagnostic_id  | Diagnostic identifier                    |
       | status         | Final diagnostic status                  |
       | findings       | Comprehensive findings report            |
       | recommendations| Recommended actions report               |
       | log_references | Log references array                     |
     - Callback: Return diagnostic session results

6. **Final Step:** Return complete diagnostic analysis with comprehensive findings, actionable recommendations, log collection references, and detailed system health assessment for troubleshooting and system maintenance.

---
