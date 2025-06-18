from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser
import json

# --- API Views ---

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def dispatch(self, request, *args, **kwargs):
        # DRF handles authentication before dispatch, so this works for both session and token
        if request.user.is_authenticated:
            return Response({'detail': 'Already authenticated. Redirecting to home.'}, status=403)
        return super().dispatch(request, *args, **kwargs)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'Already authenticated. Redirecting to home.'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        identifier = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        user = None

        # Try to authenticate by username
        if identifier:
            user = authenticate(username=identifier, password=password)
            if not user:
                # Try to authenticate by email
                try:
                    user_obj = CustomUser.objects.get(email=identifier)
                    user = authenticate(username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Incorrect username / password'}, status=400)

    def get(self, request):
        return Response({'detail': 'Method "GET" not allowed.'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_view(request):
    return Response({'message': 'You are now on the homepage.'})
