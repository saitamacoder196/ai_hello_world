"""
Authentication API URL Configuration

Defines URL patterns for authentication endpoints.
"""

from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication endpoints
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('validate', views.validate_session, name='validate_session'),
    path('refresh', views.refresh_token, name='refresh_token'),
    
    # Health check
    path('health', views.health_check, name='health_check'),
]