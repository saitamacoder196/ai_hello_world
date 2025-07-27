"""
MANDATORY DOCSTRING - Configuration and Settings models for system configuration, user preferences, feature toggles, environment settings, and validation.

Source Information (REQUIRED):
- Database Tables: system_configurations, configuration_audit, user_preferences, user_preference_cache, feature_toggles, feature_toggle_audit, feature_toggle_cache, environment_settings, environment_config_cache, configuration_validations, validation_issues, validation_schedule
- Database Design: DD/database_v0.1.md - Sections: configuration, settings, validation
- DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-09_v0.1.md
- Business Module: config

Business Rules (REQUIRED):
    - Track config values, versioning, audit, user preferences, feature toggles, environment settings, validation sessions
    - Store encrypted/sensitive values, cache, and validation results
    - All models must be traceable to DAO and DB design

Relationships (REQUIRED):
    - system_configurations → configuration_audit (one-to-many)
    - user_preferences → user_preference_cache (many-to-one)
    - feature_toggles → feature_toggle_audit (one-to-many)
    - environment_settings → environment_config_cache (many-to-one)
    - configuration_validations → validation_issues (one-to-many)

Verification Source: DAO-MDE-03-09_v0.1.md, DD/database_v0.1.md
"""
import uuid
from django.db import models

class SystemConfiguration(models.Model):
    config_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    config_key = models.CharField(max_length=100, unique=True)
    config_value = models.JSONField(default=dict)
    config_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_encrypted = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'system_configurations'
        verbose_name = 'System Configuration'
        verbose_name_plural = 'System Configurations'

class ConfigurationAudit(models.Model):
    audit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    config = models.ForeignKey(SystemConfiguration, on_delete=models.CASCADE, related_name='audits')
    old_value = models.JSONField(default=dict)
    new_value = models.JSONField(default=dict)
    change_type = models.CharField(max_length=20)
    changed_by = models.CharField(max_length=36)
    changed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'configuration_audit'
        verbose_name = 'Configuration Audit'
        verbose_name_plural = 'Configuration Audits'

class UserPreference(models.Model):
    preference_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=36)
    preference_key = models.CharField(max_length=100)
    preference_value = models.JSONField(default=dict)
    category = models.CharField(max_length=50, blank=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_preferences'
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'

class UserPreferenceCache(models.Model):
    user = models.OneToOneField(UserPreference, on_delete=models.CASCADE, related_name='cache')
    preferences_json = models.JSONField(default=dict)
    cache_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_preference_cache'
        verbose_name = 'User Preference Cache'
        verbose_name_plural = 'User Preference Caches'

class FeatureToggle(models.Model):
    toggle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feature_name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)
    target_audience = models.JSONField(default=dict, blank=True)
    rollout_percentage = models.IntegerField(default=100)
    environment = models.CharField(max_length=50, default='production')
    effective_date = models.DateTimeField(auto_now_add=True)
    rollout_status = models.CharField(max_length=20, default='complete')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'feature_toggles'
        verbose_name = 'Feature Toggle'
        verbose_name_plural = 'Feature Toggles'

class FeatureToggleAudit(models.Model):
    audit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    toggle = models.ForeignKey(FeatureToggle, on_delete=models.CASCADE, related_name='audits')
    old_enabled = models.BooleanField(default=True)
    new_enabled = models.BooleanField(default=True)
    old_rollout = models.IntegerField(default=100)
    new_rollout = models.IntegerField(default=100)
    change_reason = models.CharField(max_length=200)
    changed_by = models.CharField(max_length=36)
    changed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'feature_toggle_audit'
        verbose_name = 'Feature Toggle Audit'
        verbose_name_plural = 'Feature Toggle Audits'

class FeatureToggleCache(models.Model):
    environment = models.CharField(max_length=50, primary_key=True)
    toggles_json = models.JSONField(default=dict)
    cache_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'feature_toggle_cache'
        verbose_name = 'Feature Toggle Cache'
        verbose_name_plural = 'Feature Toggle Caches'

class EnvironmentSetting(models.Model):
    setting_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    environment = models.CharField(max_length=50)
    setting_key = models.CharField(max_length=100)
    setting_value = models.JSONField(default=dict)
    is_sensitive = models.BooleanField(default=False)
    inheritance_level = models.CharField(max_length=20, default='env')
    encrypted_value = models.TextField(blank=True)
    is_valid = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'environment_settings'
        verbose_name = 'Environment Setting'
        verbose_name_plural = 'Environment Settings'

class EnvironmentConfigCache(models.Model):
    environment = models.CharField(max_length=50, primary_key=True)
    config_json = models.JSONField(default=dict)
    sensitive_count = models.IntegerField(default=0)
    cache_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'environment_config_cache'
        verbose_name = 'Environment Config Cache'
        verbose_name_plural = 'Environment Config Caches'

class ConfigurationValidation(models.Model):
    validation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    validation_scope = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100)
    validation_rules = models.JSONField(default=dict, blank=True)
    repair_mode = models.BooleanField(default=False)
    notification_level = models.CharField(max_length=20, default='warning')
    status = models.CharField(max_length=20, default='running')
    issues_found = models.IntegerField(default=0)
    issues_repaired = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'configuration_validations'
        verbose_name = 'Configuration Validation'
        verbose_name_plural = 'Configuration Validations'

class ValidationIssue(models.Model):
    id = models.AutoField(primary_key=True)
    validation = models.ForeignKey(ConfigurationValidation, on_delete=models.CASCADE, related_name='issues')
    rule_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='identified')
    identified_at = models.DateTimeField(auto_now_add=True)
    repaired_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'validation_issues'
        verbose_name = 'Validation Issue'
        verbose_name_plural = 'Validation Issues'

class ValidationSchedule(models.Model):
    validation_scope = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100)
    next_validation = models.DateTimeField()
    frequency = models.CharField(max_length=20, default='daily')
    last_validation_id = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'validation_schedule'
        verbose_name = 'Validation Schedule'
        verbose_name_plural = 'Validation Schedules'
