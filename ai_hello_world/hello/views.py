from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
from .serializers import HelloWorldSerializer

# Create your views here.
@api_view(['GET'])
def index(request):
    """
    API endpoint để trả về thông điệp AI Hello World
    """
    data = {
        'message': 'AI Hello World!',
        'welcome': 'Chào mừng bạn đến với Django REST Framework API!',
        'timestamp': datetime.now(),
        'status': 'success'
    }
    
    serializer = HelloWorldSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)

class HelloWorldAPIView(APIView):
    """API View for AI Hello World endpoint.
    This class-based view provides a GET endpoint that   
    Class-based API view cho AI Hello World
    """
    def get(self, request, format=None):
        """
        Trả về thông điệp AI Hello World với thông tin chi tiết
        """
        data = {
            'message': 'AI Hello World!',
            'welcome': 'Chào mừng bạn đến với Django REST Framework API!',
            'timestamp': datetime.now(),
            'status': 'success'
        }
        
        serializer = HelloWorldSerializer(data)
        return Response({
            'data': serializer.data,
            'api_version': '1.0',
            'endpoint': '/api/hello-world/',
            'method': 'GET'
        }, status=status.HTTP_200_OK)
