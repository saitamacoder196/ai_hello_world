"""
MANDATORY DOCSTRING - Notification and Alert models for system notification, alert, subscription, and rule management.

Source Information (REQUIRED):
- Database Tables: notifications, notification_recipients, notification_audit_log, alerts, alert_rules, alert_rule_executions, alert_escalations, alert_statistics, notification_subscriptions, user_notification_settings
- Database Design: DD/database_v0.1.md - Sections: notifications, alerts, ...
- DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
- Business Module: monitoring_alerts

Business Rules (REQUIRED):
    - Notification and alert records must track delivery, status, recipients, and audit history
    - Rules and subscriptions must be configurable and traceable
    - Audit and escalation must be linked to notification/alert events

Relationships (REQUIRED):
    - notifications → notification_recipients (one-to-many)
    - notifications → notification_audit_log (one-to-many)
    - alerts → alert_rules (many-to-one)
    - alerts → alert_escalations (one-to-many)
    - alerts → alert_statistics (one-to-many)
    - notification_subscriptions → user_notification_settings (many-to-one)

Verification Source: This information can be verified by checking
    the referenced DAO specification and database design documents.
"""
import uuid
from django.db import models

class Notification(models.Model):
    """
    MANDATORY DOCSTRING - Notification model for system notifications and alerts.
    Source Information:
    - Database Table: notifications
    - Database Design: DD/database_v0.1.md - Section: notifications
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track notification type, title, message, priority, status, delivery method
        - Link to recipients and audit log
    Relationships:
        - Related to NotificationRecipient via FK
        - Related to NotificationAuditLog via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=20, default='medium')
    status = models.CharField(max_length=20, default='pending')
    delivery_method = models.CharField(max_length=50, default='email')
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

class NotificationRecipient(models.Model):
    """
    MANDATORY DOCSTRING - NotificationRecipient model for notification recipients.
    Source Information:
    - Database Table: notification_recipients
    - Database Design: DD/database_v0.1.md - Section: notification_recipients
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Each notification can have multiple recipients
    Relationships:
        - Related to Notification via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    recipient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='recipients')
    user_id = models.CharField(max_length=36)
    delivery_status = models.CharField(max_length=20, default='pending')
    delivered_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'notification_recipients'
        verbose_name = 'Notification Recipient'
        verbose_name_plural = 'Notification Recipients'

class NotificationAuditLog(models.Model):
    """
    MANDATORY DOCSTRING - NotificationAuditLog model for notification delivery audit trail.
    Source Information:
    - Database Table: notification_audit_log
    - Database Design: DD/database_v0.1.md - Section: notification_audit_log
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track delivery attempts, status, and audit info
    Relationships:
        - Related to Notification via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    audit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='audit_logs')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    details = models.JSONField(default=dict, blank=True)
    class Meta:
        db_table = 'notification_audit_log'
        verbose_name = 'Notification Audit Log'
        verbose_name_plural = 'Notification Audit Logs'

class Alert(models.Model):
    """
    MANDATORY DOCSTRING - Alert model for system alerts and warnings.
    Source Information:
    - Database Table: alerts
    - Database Design: DD/database_v0.1.md - Section: alerts
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track alert type, status, escalation, and statistics
    Relationships:
        - Related to AlertRule via FK
        - Related to AlertEscalation via FK
        - Related to AlertStatistic via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    alert_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    triggered_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    rule = models.ForeignKey('AlertRule', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'alerts'
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

class AlertRule(models.Model):
    """
    MANDATORY DOCSTRING - AlertRule model for alert rule configuration.
    Source Information:
    - Database Table: alert_rules
    - Database Design: DD/database_v0.1.md - Section: alert_rules
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Define rule conditions and configuration
    Relationships:
        - Related to Alert via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    rule_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule_name = models.CharField(max_length=100)
    rule_description = models.TextField(blank=True)
    conditions = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'alert_rules'
        verbose_name = 'Alert Rule'
        verbose_name_plural = 'Alert Rules'

class AlertEscalation(models.Model):
    """
    MANDATORY DOCSTRING - AlertEscalation model for alert escalation configuration and history.
    Source Information:
    - Database Table: alert_escalations
    - Database Design: DD/database_v0.1.md - Section: alert_escalations
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track escalation steps and history
    Relationships:
        - Related to Alert via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    escalation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='escalations')
    step = models.IntegerField()
    escalated_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)
    class Meta:
        db_table = 'alert_escalations'
        verbose_name = 'Alert Escalation'
        verbose_name_plural = 'Alert Escalations'

class AlertStatistic(models.Model):
    """
    MANDATORY DOCSTRING - AlertStatistic model for alert performance statistics.
    Source Information:
    - Database Table: alert_statistics
    - Database Design: DD/database_v0.1.md - Section: alert_statistics
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track alert statistics and performance data
    Relationships:
        - Related to Alert via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    statistic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='statistics')
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=15, decimal_places=6)
    recorded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'alert_statistics'
        verbose_name = 'Alert Statistic'
        verbose_name_plural = 'Alert Statistics'

class NotificationSubscription(models.Model):
    """
    MANDATORY DOCSTRING - NotificationSubscription model for user notification subscriptions.
    Source Information:
    - Database Table: notification_subscriptions
    - Database Design: DD/database_v0.1.md - Section: notification_subscriptions
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track user subscriptions and preferences
    Relationships:
        - Related to UserNotificationSetting via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=36)
    notification_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'notification_subscriptions'
        verbose_name = 'Notification Subscription'
        verbose_name_plural = 'Notification Subscriptions'

class UserNotificationSetting(models.Model):
    """
    MANDATORY DOCSTRING - UserNotificationSetting model for global notification preferences per user.
    Source Information:
    - Database Table: user_notification_settings
    - Database Design: DD/database_v0.1.md - Section: user_notification_settings
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-07_v0.1.md
    - Business Module: monitoring_alerts
    Business Rules:
        - Track user notification settings and preferences
    Relationships:
        - Related to NotificationSubscription via FK
    Verification Source: DD/database_v0.1.md, DAO-MDE-03-07_v0.1.md
    """
    setting_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=36)
    preferences = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_notification_settings'
        verbose_name = 'User Notification Setting'
        verbose_name_plural = 'User Notification Settings'
