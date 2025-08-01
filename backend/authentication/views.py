from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction, IntegrityError
from authentication.serializers import (
    LoginSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(email=serializer.data['email'], password=serializer.data['password'])

        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        access = refresh.access_token

        return Response({
            "access_token": str(access),
            "refresh_token": str(refresh),
            "msg": "Login Successful"
        }, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=serializer.data['email'],
                    password=serializer.data['password'],
                    full_name=serializer.data['full_name']
                )
                user.save()
        except IntegrityError:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = CustomTokenObtainPairSerializer.get_token(user)
        access = refresh.access_token

        return Response({
            "access_token": str(access),
            "refresh_token": str(refresh),
            "msg": "Register Successful"
        }, status=status.HTTP_200_OK)