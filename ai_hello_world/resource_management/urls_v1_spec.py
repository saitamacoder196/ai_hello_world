"""
Resource Management API URL Configuration - Following API Specification Exactly
URLs đúng theo tài liệu API Design specification
"""

from django.urls import path
from . import views_v1_spec

app_name = 'resource_management_v1'

urlpatterns = [
    # Basic CRUD - Matching API Specification Exactly
    
    # API-MDE-03-01: Get Idle Resource List
    path('idle-resources', views_v1_spec.get_idle_resource_list, name='get_idle_resource_list'),
    
    # API-MDE-03-02: Get Idle Resource Detail  
    path('idle-resources/<uuid:id>', views_v1_spec.get_idle_resource_detail, name='get_idle_resource_detail'),
    
    # API-MDE-03-03: Create Idle Resource
    path('idle-resources', views_v1_spec.create_idle_resource, name='create_idle_resource'),
    
    # API-MDE-03-04: Update Idle Resource
    path('idle-resources/<uuid:id>', views_v1_spec.update_idle_resource, name='update_idle_resource'),
    
    # API-MDE-03-05: Delete Idle Resource
    path('idle-resources/<uuid:id>', views_v1_spec.delete_idle_resource, name='delete_idle_resource'),
    
    # API-MDE-03-06: Bulk Update Idle Resources
    path('idle-resources/bulk', views_v1_spec.bulk_update_idle_resources, name='bulk_update_idle_resources'),
    
    # API-MDE-03-07: Export Idle Resources
    path('idle-resources/export', views_v1_spec.export_idle_resources, name='export_idle_resources'),
    
    # API-MDE-03-08: Import Idle Resources
    path('idle-resources/import', views_v1_spec.import_idle_resources, name='import_idle_resources'),
    
    # API-MDE-03-09: Advanced Search Idle Resources
    path('idle-resources/search', views_v1_spec.search_idle_resources, name='search_idle_resources'),
    
    # API-MDE-03-13: Validate Data
    path('idle-resources/validate', views_v1_spec.validate_idle_resource_data, name='validate_idle_resource_data'),
    
    # Master Data API
    path('master-data', views_v1_spec.get_master_data, name='get_master_data'),
]

# Note: Django URL routing will handle method differentiation:
# - GET /idle-resources -> get_idle_resource_list
# - POST /idle-resources -> create_idle_resource  
# - GET /idle-resources/{id} -> get_idle_resource_detail
# - PUT /idle-resources/{id} -> update_idle_resource
# - DELETE /idle-resources/{id} -> delete_idle_resource