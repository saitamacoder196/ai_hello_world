"""
Common Django model abstractions and base classes.

This module provides reusable base models that implement common patterns
across the application, including audit trails, soft deletion, versioning,
and UUID primary keys.

Source: IMPLEMENTATION_ROADMAP.md - Phase 1: Foundation Setup

Business Rules:
    - All models should inherit from appropriate base classes
    - UUID primary keys for better security and distribution
    - Automatic audit trails for all operations
    - Soft deletion to preserve data integrity
    - Optimistic locking through versioning
    - Consistent timestamp tracking
"""
import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class TimestampedModel(models.Model):
    """
    Abstract base model providing automatic timestamp fields.
    
    Provides:
    - created_at: Automatically set on model creation
    - updated_at: Automatically updated on model save
    
    Usage:
        class MyModel(TimestampedModel):
            name = models.CharField(max_length=100)
    """
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="Timestamp when record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text="Timestamp when record was last updated"
    )
    
    class Meta:
        abstract = True


class UUIDBaseModel(models.Model):
    """
    Abstract base model providing UUID primary key.
    
    Uses UUID4 for better security and distribution across systems.
    Prevents ID enumeration attacks and enables better data distribution.
    
    Usage:
        class MyModel(UUIDBaseModel):
            name = models.CharField(max_length=100)
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for this record"
    )
    
    class Meta:
        abstract = True


class AuditableModel(TimestampedModel):
    """
    Abstract base model providing audit trail functionality.
    
    Tracks who created and last updated the record along with timestamps.
    Essential for compliance and data governance.
    
    Usage:
        class MyModel(AuditableModel):
            name = models.CharField(max_length=100)
            
            def save(self, *args, **kwargs):
                if not self.created_by:
                    self.created_by = request.user.id  # Get from context
                self.updated_by = request.user.id
                super().save(*args, **kwargs)
    """
    created_by = models.CharField(
        max_length=36, 
        help_text="ID of user who created this record"
    )
    updated_by = models.CharField(
        max_length=36, 
        null=True, 
        blank=True,
        help_text="ID of user who last updated this record"
    )
    
    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model providing soft deletion functionality.
    
    Records are marked as deleted rather than physically removed from database.
    This preserves data integrity and enables audit trails.
    
    Usage:
        class MyModel(SoftDeleteModel):
            name = models.CharField(max_length=100)
            
            objects = SoftDeleteManager()  # Custom manager
    """
    is_deleted = models.BooleanField(
        default=False,
        help_text="Whether this record is soft-deleted"
    )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Timestamp when record was soft-deleted"
    )
    deleted_by = models.CharField(
        max_length=36, 
        null=True, 
        blank=True,
        help_text="ID of user who soft-deleted this record"
    )
    
    def soft_delete(self, user_id=None):
        """
        Perform soft deletion of the record.
        
        Args:
            user_id (str): ID of user performing the deletion
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user_id:
            self.deleted_by = user_id
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])
    
    def restore(self):
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])
    
    class Meta:
        abstract = True


class VersionedModel(models.Model):
    """
    Abstract base model providing optimistic locking through versioning.
    
    Version field is incremented on each update to prevent concurrent 
    modification issues in high-concurrency environments.
    
    Usage:
        def update_with_version_check(self, data, expected_version):
            if self.version != expected_version:
                raise ValidationError("Record was modified by another user")
            
            for key, value in data.items():
                setattr(self, key, value)
            self.version += 1
            self.save()
    """
    version = models.PositiveIntegerField(
        default=1,
        help_text="Version number for optimistic locking"
    )
    
    def save(self, *args, **kwargs):
        """Override save to increment version on updates."""
        if self.pk:  # Existing record
            self.version += 1
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True


class BaseModel(UUIDBaseModel, AuditableModel, SoftDeleteModel, VersionedModel):
    """
    Complete base model combining all common functionality.
    
    Provides:
    - UUID primary key for security
    - Audit trail (created_by, updated_by, created_at, updated_at)
    - Soft deletion (is_deleted, deleted_at, deleted_by)
    - Optimistic locking (version)
    
    Use this as the base for most models in the application where
    you need complete functionality.
    
    Usage:
        class IdleResource(BaseModel):
            resource_type = models.CharField(max_length=50)
            status = models.CharField(max_length=20)
            
            class Meta:
                db_table = 'idle_resources'
    """
    
    class Meta:
        abstract = True


# Custom Managers for handling soft deletion

class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that handles soft deletion."""
    
    def active(self):
        """Return only non-deleted records."""
        return self.filter(is_deleted=False)
    
    def deleted(self):
        """Return only soft-deleted records."""
        return self.filter(is_deleted=True)
    
    def soft_delete(self, user_id=None):
        """Soft delete all records in queryset."""
        return self.update(
            is_deleted=True,
            deleted_at=timezone.now(),
            deleted_by=user_id
        )


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""
    
    def get_queryset(self):
        """Return queryset excluding soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db).active()
    
    def all_with_deleted(self):
        """Return all records including soft-deleted ones."""
        return SoftDeleteQuerySet(self.model, using=self._db)
    
    def deleted_only(self):
        """Return only soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()


# Utility Functions

def get_user_context():
    """
    Get current user context for audit trails.
    This should be implemented to work with your authentication system.
    
    Returns:
        dict: User context with user_id, username, etc.
    """
    # TODO: Implement based on your authentication system
    # This could use Django's threading.local or similar
    return {
        'user_id': 'system',  # Default fallback
        'username': 'system'
    }


def validate_business_rules(instance, rules):
    """
    Generic business rule validation helper.
    
    Args:
        instance: Model instance to validate
        rules (dict): Dictionary of validation rules
        
    Raises:
        ValidationError: If any validation rule fails
    """
    errors = []
    
    for field_name, rule_config in rules.items():
        field_value = getattr(instance, field_name, None)
        
        # Required field validation
        if rule_config.get('required', False) and not field_value:
            errors.append(f"{field_name} is required")
        
        # Range validation
        if 'min_value' in rule_config and field_value is not None:
            if field_value < rule_config['min_value']:
                errors.append(f"{field_name} must be >= {rule_config['min_value']}")
        
        if 'max_value' in rule_config and field_value is not None:
            if field_value > rule_config['max_value']:
                errors.append(f"{field_name} must be <= {rule_config['max_value']}")
        
        # Custom validation function
        if 'validator' in rule_config and field_value is not None:
            try:
                rule_config['validator'](field_value)
            except ValidationError as e:
                errors.append(f"{field_name}: {e.message}")
    
    if errors:
        raise ValidationError(errors)