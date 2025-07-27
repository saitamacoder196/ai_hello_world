"""
Simple URL Configuration for List Screen APIs
Routing cho các API đơn giản không cần xác thực
"""

from django.urls import path
from simple_views import (
    get_idle_resource_list_simple,
    get_master_data_simple,
    get_resource_detail_simple,
    login_simple,
    api_status
)

urlpatterns = [
    # API trạng thái hệ thống
    path('api/v1/status', api_status, name='api_status'),
    
    # Authentication đơn giản
    path('api/v1/auth/simple/login', login_simple, name='login_simple'),
    
    # Idle Resources APIs
    path('api/v1/idle-resources/simple', get_idle_resource_list_simple, name='idle_resources_list_simple'),
    path('api/v1/idle-resources/simple/<str:resource_id>', get_resource_detail_simple, name='idle_resource_detail_simple'),
    
    # Master Data API
    path('api/v1/master-data/simple', get_master_data_simple, name='master_data_simple'),
]