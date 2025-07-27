"""
Resource Management Models

Fixed version without duplicate primary keys.
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from common.models import BaseModel, TimestampedModel


class IdleResource(BaseModel):
    """
    MANDATORY DOCSTRING - IdleResource model for managing idle personnel information and availability.
    
    Source Information (REQUIRED):
    - Database Table: idle_resources
    - Database Design: DD/database_v0.1.md - Section: idle_resources
    - DAO Specification: DD/MDE-03/04-dao/DAO-MDE-03-01_v0.1.md
    - Business Module: resource_management
    
    Business Rules (REQUIRED):
        - Track resource type, status, skills, experience, availability, and audit info
        - Link to employee and department via proper foreign keys
        - Support for optimistic locking (version) from BaseModel
        - Skills stored as JSON array for flexibility
        - Availability date range validation
        - Status choices for better data integrity
    
    Relationships (REQUIRED):
        - Related to Employee via employee FK
        - Related to Department via department FK (through Employee)
        - Inherits audit trails from BaseModel
    
    Custom Methods (from DAO specifications):
        - create_with_validation(): Create resource with business rule validation
        - update_with_version_check(): Update with optimistic locking
        - list_with_filters(): Dynamic filtering with pagination
        - check_availability(): Check resource availability for date range
    
    Verification Source: This information can be verified by checking
        the referenced DAO specification and database design documents.
    """
    # Note: Using inherited 'id' field from BaseModel as primary key
    
    employee = models.ForeignKey(
        'authentication.Employee',
        on_delete=models.CASCADE,
        related_name='idle_resources',
        help_text="Employee associated with this resource"
    )
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('developer', 'Software Developer'),
            ('tester', 'QA Tester'),
            ('analyst', 'Business Analyst'),
            ('designer', 'UI/UX Designer'),
            ('manager', 'Project Manager'),
            ('devops', 'DevOps Engineer'),
            ('architect', 'Solution Architect'),
            ('consultant', 'Technical Consultant'),
        ],
        help_text="Type of resource (developer, tester, analyst, etc.)"
    )
    status = models.CharField(
        max_length=20,
        default='available',
        choices=[
            ('available', 'Available'),
            ('allocated', 'Allocated'),
            ('unavailable', 'Unavailable'),
            ('deleted', 'Deleted')
        ],
        help_text="Current availability status"
    )
    availability_start = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Start date of availability period"
    )
    availability_end = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="End date of availability period"
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of skills and competencies"
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Years of relevant experience"
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Hourly rate for cost calculations"
    )
    
    def __str__(self):
        return f"IdleResource {self.id} - {self.employee.first_name} {self.employee.last_name} ({self.resource_type})"
    
    @property
    def department(self):
        """Get department through employee relationship."""
        return self.employee.department if self.employee else None
    
    @property
    def is_available_now(self):
        """Check if resource is currently available."""
        now = timezone.now()
        if self.status != 'available':
            return False
        
        if self.availability_start and now < self.availability_start:
            return False
        
        if self.availability_end and now > self.availability_end:
            return False
        
        return True
    
    def clean(self):
        """Validate business rules."""
        super().clean()
        
        if self.availability_start and self.availability_end:
            if self.availability_start >= self.availability_end:
                raise ValidationError("Availability start must be before end date")
        
        if self.hourly_rate is not None and self.hourly_rate < 0:
            raise ValidationError("Hourly rate cannot be negative")
        
        if self.experience_years is not None and self.experience_years < 0:
            raise ValidationError("Experience years cannot be negative")
    
    def to_dict(self):
        """Convert model instance to dictionary for API responses."""
        return {
            'id': str(self.id),
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_id': str(self.employee.employee_id) if self.employee else None,
            'department_id': str(self.employee.department.department_id) if self.employee and self.employee.department else None,
            'resource_type': self.resource_type,
            'status': self.status,
            'availability_start': self.availability_start.isoformat() if self.availability_start else None,
            'availability_end': self.availability_end.isoformat() if self.availability_end else None,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'version': self.version
        }
    
    class Meta:
        db_table = 'idle_resources'
        verbose_name = 'Idle Resource'
        verbose_name_plural = 'Idle Resources'
        indexes = [
            models.Index(fields=['status', 'resource_type']),
            models.Index(fields=['employee', 'status']),
            models.Index(fields=['availability_start', 'availability_end']),
            models.Index(fields=['resource_type', 'status']),
        ]