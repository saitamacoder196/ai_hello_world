"""
MANDATORY DOCSTRING - Performance and Monitoring models for system metrics, monitoring, health checks, optimization, and diagnostics.

Source Information (REQUIRED):
- Database Tables: performance_metrics, metric_thresholds, performance_alerts, performance_summary, system_monitors, monitoring_checks, monitoring_alerts, health_checks, health_check_details, health_check_stats, health_check_schedule, query_optimization_analysis, query_analysis_results, optimization_schedule, diagnostic_sessions, diagnostic_procedures, diagnostic_results, diagnostic_findings, diagnostic_recommendations, diagnostic_logs
- Database Design: DD/database_v0.1.md - Sections: performance, monitoring, health, optimization, diagnostics
- DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-10_v0.1.md
- Business Module: monitoring

Business Rules (REQUIRED):
    - Track system metrics, health, alerts, optimization, diagnostics, logs
    - Store thresholds, status, recommendations, findings, and performance data
    - All models must be traceable to DAO and DB design

Relationships (REQUIRED):
    - performance_metrics → performance_alerts (one-to-many)
    - performance_metrics → performance_summary (many-to-one)
    - system_monitors → monitoring_checks (one-to-many)
    - system_monitors → monitoring_alerts (one-to-many)
    - health_checks → health_check_details (one-to-many)
    - health_checks → health_check_stats (many-to-one)
    - query_optimization_analysis → query_analysis_results (one-to-many)
    - diagnostic_sessions → diagnostic_procedures (one-to-many)
    - diagnostic_sessions → diagnostic_findings (one-to-many)
    - diagnostic_sessions → diagnostic_recommendations (one-to-many)
    - diagnostic_sessions → diagnostic_logs (one-to-many)

Verification Source: DAO-MDE-03-10_v0.1.md, DD/database_v0.1.md
"""
import uuid
from django.db import models

class PerformanceMetric(models.Model):
    metric_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=20, decimal_places=4)
    metric_unit = models.CharField(max_length=20)
    component = models.CharField(max_length=100, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    trend_direction = models.CharField(max_length=10, default='stable')
    alert_level = models.CharField(max_length=20, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'performance_metrics'
        verbose_name = 'Performance Metric'
        verbose_name_plural = 'Performance Metrics'

class MetricThreshold(models.Model):
    id = models.AutoField(primary_key=True)
    metric_name = models.CharField(max_length=100)
    warning_threshold = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    critical_threshold = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    alert_enabled = models.BooleanField(default=True)
    class Meta:
        db_table = 'metric_thresholds'
        verbose_name = 'Metric Threshold'
        verbose_name_plural = 'Metric Thresholds'

class PerformanceAlert(models.Model):
    alert_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(PerformanceMetric, on_delete=models.CASCADE, related_name='alerts')
    alert_level = models.CharField(max_length=20)
    metric_value = models.DecimalField(max_digits=20, decimal_places=4)
    component = models.CharField(max_length=100, blank=True)
    triggered_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'performance_alerts'
        verbose_name = 'Performance Alert'
        verbose_name_plural = 'Performance Alerts'

class PerformanceSummary(models.Model):
    id = models.AutoField(primary_key=True)
    metric_name = models.CharField(max_length=100)
    component = models.CharField(max_length=100, blank=True)
    min_value = models.DecimalField(max_digits=20, decimal_places=4)
    max_value = models.DecimalField(max_digits=20, decimal_places=4)
    avg_value = models.DecimalField(max_digits=20, decimal_places=4)
    sample_count = models.IntegerField(default=1)
    last_updated = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'performance_summary'
        verbose_name = 'Performance Summary'
        verbose_name_plural = 'Performance Summaries'

class SystemMonitor(models.Model):
    monitor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monitor_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=100)
    threshold_config = models.JSONField(default=dict, blank=True)
    alert_contacts = models.JSONField(default=list, blank=True)
    monitoring_interval = models.IntegerField(default=60)
    status = models.CharField(max_length=20, default='active')
    last_check = models.DateTimeField(null=True, blank=True)
    health_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    active_alerts = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'system_monitors'
        verbose_name = 'System Monitor'
        verbose_name_plural = 'System Monitors'

class MonitoringCheck(models.Model):
    check_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monitor = models.ForeignKey(SystemMonitor, on_delete=models.CASCADE, related_name='checks')
    check_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='healthy')
    response_time = models.IntegerField(default=0)
    resource_usage = models.JSONField(default=dict, blank=True)
    errors = models.JSONField(default=dict, blank=True)
    class Meta:
        db_table = 'monitoring_checks'
        verbose_name = 'Monitoring Check'
        verbose_name_plural = 'Monitoring Checks'

class MonitoringAlert(models.Model):
    alert_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monitor = models.ForeignKey(SystemMonitor, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    message = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    resolved_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'monitoring_alerts'
        verbose_name = 'Monitoring Alert'
        verbose_name_plural = 'Monitoring Alerts'

class HealthCheck(models.Model):
    check_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    check_type = models.CharField(max_length=50)
    target_endpoint = models.CharField(max_length=500)
    check_parameters = models.JSONField(default=dict, blank=True)
    timeout_seconds = models.IntegerField(default=30)
    retry_count = models.IntegerField(default=3)
    status = models.CharField(max_length=20, default='running')
    response_time = models.IntegerField(default=0)
    details = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    next_check = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'health_checks'
        verbose_name = 'Health Check'
        verbose_name_plural = 'Health Checks'

class HealthCheckDetail(models.Model):
    id = models.AutoField(primary_key=True)
    health_check = models.ForeignKey(HealthCheck, on_delete=models.CASCADE, related_name='health_check_detail_set')
    attempt_number = models.IntegerField(default=1)
    status = models.CharField(max_length=20)
    response_time = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    details = models.JSONField(default=dict, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'health_check_details'
        verbose_name = 'Health Check Detail'
        verbose_name_plural = 'Health Check Details'

class HealthCheckStat(models.Model):
    id = models.AutoField(primary_key=True)
    check_type = models.CharField(max_length=50)
    target_endpoint = models.CharField(max_length=500)
    total_checks = models.IntegerField(default=0)
    successful_checks = models.IntegerField(default=0)
    failed_checks = models.IntegerField(default=0)
    avg_response_time = models.IntegerField(default=0)
    last_check_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'health_check_stats'
        verbose_name = 'Health Check Stat'
        verbose_name_plural = 'Health Check Stats'

class HealthCheckSchedule(models.Model):
    check_type = models.CharField(max_length=50, primary_key=True)
    target_endpoint = models.CharField(max_length=500)
    next_check = models.DateTimeField()
    frequency = models.CharField(max_length=20, default='every_5_minutes')
    last_check_id = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'health_check_schedule'
        verbose_name = 'Health Check Schedule'
        verbose_name_plural = 'Health Check Schedules'

class QueryOptimizationAnalysis(models.Model):
    analysis_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query_type = models.CharField(max_length=50)
    target_schema = models.CharField(max_length=100, blank=True)
    analysis_period = models.IntegerField(default=24)
    optimization_level = models.CharField(max_length=20, default='basic')
    auto_apply = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='running')
    potential_improvement = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    applied_optimizations = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'query_optimization_analysis'
        verbose_name = 'Query Optimization Analysis'
        verbose_name_plural = 'Query Optimization Analyses'

class QueryAnalysisResult(models.Model):
    id = models.AutoField(primary_key=True)
    analysis = models.ForeignKey(QueryOptimizationAnalysis, on_delete=models.CASCADE, related_name='results')
    query_hash = models.CharField(max_length=64, blank=True)
    query_text = models.TextField(blank=True)
    execution_time = models.IntegerField(default=0)
    call_count = models.IntegerField(default=0)
    optimization_type = models.CharField(max_length=50)
    recommendation = models.TextField(blank=True)
    priority = models.CharField(max_length=20, default='low')
    estimated_benefit = models.CharField(max_length=100, blank=True)
    applied = models.BooleanField(default=False)
    applied_at = models.DateTimeField(null=True, blank=True)
    table_name = models.CharField(max_length=100, blank=True)
    index_name = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'query_analysis_results'
        verbose_name = 'Query Analysis Result'
        verbose_name_plural = 'Query Analysis Results'

class OptimizationSchedule(models.Model):
    analysis_type = models.CharField(max_length=50)
    target_schema = models.CharField(max_length=100)
    next_analysis = models.DateTimeField()
    frequency = models.CharField(max_length=20, default='weekly')
    last_analysis_id = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'optimization_schedule'
        verbose_name = 'Optimization Schedule'
        verbose_name_plural = 'Optimization Schedules'

class DiagnosticSession(models.Model):
    diagnostic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagnostic_type = models.CharField(max_length=50)
    severity_level = models.CharField(max_length=20)
    component_path = models.CharField(max_length=200, blank=True)
    diagnostic_params = models.JSONField(default=dict, blank=True)
    collect_logs = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='running')
    findings = models.JSONField(default=dict, blank=True)
    recommendations = models.JSONField(default=dict, blank=True)
    log_references = models.JSONField(default=list, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'diagnostic_sessions'
        verbose_name = 'Diagnostic Session'
        verbose_name_plural = 'Diagnostic Sessions'

class DiagnosticProcedure(models.Model):
    procedure_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagnostic = models.ForeignKey(DiagnosticSession, on_delete=models.CASCADE, related_name='procedures')
    procedure_name = models.CharField(max_length=100)
    procedure_type = models.CharField(max_length=50)
    execution_order = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='running')
    started_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'diagnostic_procedures'
        verbose_name = 'Diagnostic Procedure'
        verbose_name_plural = 'Diagnostic Procedures'

class DiagnosticResult(models.Model):
    id = models.AutoField(primary_key=True)
    diagnostic = models.ForeignKey(DiagnosticSession, on_delete=models.CASCADE, related_name='results')
    procedure = models.ForeignKey(DiagnosticProcedure, on_delete=models.CASCADE, related_name='results')
    result_type = models.CharField(max_length=50)
    result_data = models.JSONField(default=dict, blank=True)
    severity = models.CharField(max_length=20)
    identified_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'diagnostic_results'
        verbose_name = 'Diagnostic Result'
        verbose_name_plural = 'Diagnostic Results'

class DiagnosticFinding(models.Model):
    finding_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagnostic = models.ForeignKey(DiagnosticSession, on_delete=models.CASCADE, related_name='diagnostic_finding_set')
    finding_type = models.CharField(max_length=50)
    component = models.CharField(max_length=100, blank=True)
    issue_description = models.TextField(blank=True)
    severity = models.CharField(max_length=20)
    impact_level = models.CharField(max_length=20)
    found_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'diagnostic_findings'
        verbose_name = 'Diagnostic Finding'
        verbose_name_plural = 'Diagnostic Findings'

class DiagnosticRecommendation(models.Model):
    recommendation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagnostic = models.ForeignKey(DiagnosticSession, on_delete=models.CASCADE, related_name='diagnostic_recommendation_set')
    recommendation_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    action_description = models.TextField(blank=True)
    estimated_effort = models.CharField(max_length=100, blank=True)
    automated = models.BooleanField(default=False)
    class Meta:
        db_table = 'diagnostic_recommendations'
        verbose_name = 'Diagnostic Recommendation'
        verbose_name_plural = 'Diagnostic Recommendations'

class DiagnosticLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagnostic = models.ForeignKey(DiagnosticSession, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=50)
    log_source = models.CharField(max_length=100)
    log_content = models.JSONField(default=dict, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'diagnostic_logs'
        verbose_name = 'Diagnostic Log'
        verbose_name_plural = 'Diagnostic Logs'
