"""
MANDATORY DOCSTRING - Integration and Synchronization models for external system integration, sync jobs, API operations, webhook management, and system connectivity.

Source Information (REQUIRED):
- Database Tables: external_integrations, sync_jobs, sync_batches, api_operations, api_statistics, webhooks, webhook_statistics, system_connections, connection_health
- Database Design: DD/database_v0.1.md - Sections: integration, sync, api, webhook, connectivity
- DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-08_v0.1.md
- Business Module: integration

Business Rules (REQUIRED):
    - Track integration configs, sync jobs, API calls, webhook registrations, system connections
    - Store error counts, status, health, and performance metrics
    - All models must be traceable to DAO and DB design

Relationships (REQUIRED):
    - external_integrations → sync_jobs (one-to-many)
    - sync_jobs → sync_batches (one-to-many)
    - webhooks → webhook_statistics (one-to-one)
    - system_connections → connection_health (one-to-many)

Verification Source: DAO-MDE-03-08_v0.1.md, DD/database_v0.1.md
"""
import uuid
from django.db import models

class ExternalIntegration(models.Model):
    """
    External system integration configuration
    """
    integration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_id = models.CharField(max_length=100)
    integration_type = models.CharField(max_length=50)
    endpoint_url = models.CharField(max_length=500)
    auth_config = models.JSONField(default=dict)
    mapping_config = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default='active')
    last_sync = models.DateTimeField(null=True, blank=True)
    error_count = models.IntegerField(default=0)
    config_version = models.CharField(max_length=20, default='v1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'external_integrations'
        verbose_name = 'External Integration'
        verbose_name_plural = 'External Integrations'

class SyncJob(models.Model):
    """
    Data synchronization job
    """
    sync_job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    integration = models.ForeignKey(ExternalIntegration, on_delete=models.CASCADE, related_name='sync_jobs')
    sync_type = models.CharField(max_length=20)
    entity_type = models.CharField(max_length=50)
    filters = models.JSONField(default=dict, blank=True)
    batch_size = models.IntegerField(default=1000)
    status = models.CharField(max_length=20, default='running')
    records_processed = models.IntegerField(default=0)
    errors_count = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'sync_jobs'
        verbose_name = 'Sync Job'
        verbose_name_plural = 'Sync Jobs'

class SyncBatch(models.Model):
    """
    Synchronization batch for a sync job
    """
    batch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sync_job = models.ForeignKey(SyncJob, on_delete=models.CASCADE, related_name='sync_batches')
    batch_number = models.IntegerField()
    records_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='completed')
    processed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'sync_batches'
        verbose_name = 'Sync Batch'
        verbose_name_plural = 'Sync Batches'

class APIOperation(models.Model):
    """
    API operation log for external service calls
    """
    operation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation_type = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=500)
    headers = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    timeout = models.IntegerField(default=30)
    status = models.CharField(max_length=20, default='pending')
    status_code = models.IntegerField(null=True, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    execution_time = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'api_operations'
        verbose_name = 'API Operation'
        verbose_name_plural = 'API Operations'

class APIStatistic(models.Model):
    """
    API statistics and performance metrics
    """
    id = models.AutoField(primary_key=True)
    endpoint = models.CharField(max_length=500)
    operation_type = models.CharField(max_length=10)
    call_count = models.IntegerField(default=0)
    avg_execution_time = models.FloatField(default=0.0)
    last_call_at = models.DateTimeField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'api_statistics'
        verbose_name = 'API Statistic'
        verbose_name_plural = 'API Statistics'

class Webhook(models.Model):
    """
    Webhook registration and configuration
    """
    webhook_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    webhook_url = models.CharField(max_length=500)
    event_types = models.JSONField(default=list)
    secret_key = models.CharField(max_length=100, blank=True)
    retry_config = models.JSONField(default=dict, blank=True)
    headers = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default='active')
    last_triggered = models.DateTimeField(null=True, blank=True)
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'webhooks'
        verbose_name = 'Webhook'
        verbose_name_plural = 'Webhooks'

class WebhookStatistic(models.Model):
    """
    Webhook statistics and monitoring
    """
    id = models.AutoField(primary_key=True)
    webhook = models.OneToOneField(Webhook, on_delete=models.CASCADE, related_name='statistics')
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    last_triggered = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'webhook_statistics'
        verbose_name = 'Webhook Statistic'
        verbose_name_plural = 'Webhook Statistics'

class SystemConnection(models.Model):
    """
    System connection and health monitoring
    """
    connection_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_name = models.CharField(max_length=100)
    connection_type = models.CharField(max_length=20)
    endpoint = models.CharField(max_length=500)
    credentials = models.JSONField(default=dict)
    health_check_interval = models.IntegerField(default=5)
    status = models.CharField(max_length=20, default='pending')
    last_check = models.DateTimeField(null=True, blank=True)
    uptime_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    avg_response_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'system_connections'
        verbose_name = 'System Connection'
        verbose_name_plural = 'System Connections'

class ConnectionHealth(models.Model):
    """
    Connection health check and statistics
    """
    id = models.AutoField(primary_key=True)
    connection = models.ForeignKey(SystemConnection, on_delete=models.CASCADE, related_name='health_checks')
    check_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    response_time = models.IntegerField(default=0)
    class Meta:
        db_table = 'connection_health'
        verbose_name = 'Connection Health'
        verbose_name_plural = 'Connection Health'
