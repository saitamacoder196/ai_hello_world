from rest_framework import serializers

class HelloWorldSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    welcome = serializers.CharField(max_length=200)
    timestamp = serializers.DateTimeField()
    status = serializers.CharField(max_length=50)
