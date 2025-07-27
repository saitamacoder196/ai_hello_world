from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/health/', views.index, name='api_hello')
]
