from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ServiceRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields we want to use when accepting new user and returning a user
        fields = ["id", "username", "password"]
        # tells django we want to accept password when creating new user
        # but dont want to return password when giving user info
        extra_kwargs = {"password": {"write_only": True}}

    # create new version of user
    # we do this by accepting validated_data (data thats passed checks by seriliazer (see above))
    # if data is valid, it will pass data here
    def create(self, validated_data):
        # once data passed, we create new user using unpacked passed data
        user = User.objects.create_user(**validated_data)
        return user

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ["id", "title", "description", "created_at", "client"]
        # client is auto set by backend, not manually
        extra_kwargs = {"client": {"read_only": True}}