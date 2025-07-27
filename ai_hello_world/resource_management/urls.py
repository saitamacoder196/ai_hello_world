"""
Resource Management API URL Configuration

Defines URL patterns for idle resource management endpoints.
"""

from django.urls import path
from . import views

app_name = 'resource_management'

urlpatterns = [
    # Idle Resource CRUD endpoints
    path('idle-resources', views.get_idle_resource_list, name='get_idle_resource_list'),
    path('idle-resources/<uuid:resource_id>', views.get_idle_resource_detail, name='get_idle_resource_detail'),
    
    # Create using POST to idle-resources (not /create)
    # This will be handled by views.create_idle_resource when method is POST
    
    # Update/Delete operations
    path('idle-resources/<uuid:resource_id>/update', views.update_idle_resource, name='update_idle_resource'),
    path('idle-resources/<uuid:resource_id>/delete', views.delete_idle_resource, name='delete_idle_resource'),
    
    # Bulk operations
    path('idle-resources/bulk', views.bulk_update_idle_resources, name='bulk_update_idle_resources'),
    
    # Export/Import operations
    path('idle-resources/export', views.export_idle_resources, name='export_idle_resources'),
    path('idle-resources/import', views.import_idle_resources, name='import_idle_resources'),
    
    # Advanced search
    path('idle-resources/search', views.advanced_search_idle_resources, name='advanced_search_idle_resources'),
    
    # Validation
    path('idle-resources/validate', views.validate_data, name='validate_data'),
    
    # Master data
    path('master-data', views.get_master_data, name='get_master_data'),
]