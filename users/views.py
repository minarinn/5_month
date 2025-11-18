from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserCreateSerializer, UserAuthSerializer, ConfirmationSerializer
from .models import ConfirmationCode
import random

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )
        
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        ConfirmationCode.objects.create(
            user=user,
            code=code
        )
        
        return Response({
            'user_id': user.id,
            'code': code
        }, status=status.HTTP_201_CREATED)

class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(**serializer.validated_data)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})
        
        return Response({'error': 'User not authorized'}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmationAPIView(APIView):
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        
        try:
            confirmation = ConfirmationCode.objects.get(code=code)
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete()
            return Response({'message': 'User confirmed successfully'})
        except ConfirmationCode.DoesNotExist:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)