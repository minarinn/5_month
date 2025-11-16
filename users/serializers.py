from rest_framework import serializers
from django.contrib.auth.models import User

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise serializers.ValidationError("Username already exists")

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)