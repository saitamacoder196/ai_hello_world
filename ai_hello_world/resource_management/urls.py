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
    path('idle-resources/create', views.create_idle_resource, name='create_idle_resource'),
    path('idle-resources/<uuid:resource_id>/update', views.update_idle_resource, name='update_idle_resource'),
    path('idle-resources/<uuid:resource_id>/delete', views.delete_idle_resource, name='delete_idle_resource'),
    
    # Bulk operations
    path('idle-resources/bulk/update', views.bulk_update_idle_resources, name='bulk_update_idle_resources'),
    
    # Master data
    path('master-data', views.get_master_data, name='get_master_data'),
]