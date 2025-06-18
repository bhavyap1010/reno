from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, ServiceRequestSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ServiceRequest

# can list all SRs created by user or create a new one
class ServiceRequestListCreate(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceRequest.objects.filter(client=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(client=self.request.user)
        else:
            print(serializer.errors)

class ServiceRequestDelete(generics.DestroyAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceRequest.objects.filter(client=user)

# generic view built into django which auto handles creating new user/object
class CreateUserView(generics.CreateAPIView):
    # list of all different objects to ensure we dont create an already existing user
    queryset = User.objects.all()
    # tells view what kind of data to accept to make new user
    serializer_class = UserSerializer
    # specifies who can call this (allow anyone (even if unauthenticated))
    permission_classes = [AllowAny]