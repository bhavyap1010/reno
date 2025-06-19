from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, RegisterSerializer
import jwt
import requests
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views import View

from django.core.exceptions import MultipleObjectsReturned

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        user.send_verification_email(request)

        return Response(
            {"detail": "Verification email sent. Please check your email to activate your account."},
            status=status.HTTP_201_CREATED
        )

class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            # Only allow login if email is verified
            if not user.email_verified:
                return Response(
                    {"error": "Email not verified. Please check your email for verification link."},
                    status=status.HTTP_403_FORBIDDEN
                )

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete token
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            # Handle case where token doesn't exist
            pass

        logout(request)
        return Response(status=status.HTTP_200_OK)

class GoogleLogin(APIView):
    def post(self, request):
        credential = request.data.get('credential')
        if not credential:
            return Response({"error": "Credential is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify Google ID token
            idinfo = self.verify_google_token(credential)

            # Get or create user
            user, created = self.get_or_create_user(idinfo)

            # Create or get token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type
                },
                "token": token.key
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def verify_google_token(self, token):
        # Verify token using Google's certificate
        response = requests.get('https://www.googleapis.com/oauth2/v3/certs')
        jwks = response.json()

        # Verify token signature and claims
        idinfo = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
            options={"verify_signature": True}
        )
        return idinfo

    def get_or_create_user(self, idinfo):
        email = idinfo['email']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')

        try:
            # Existing user
            user = User.objects.get(email=email)
            return user, False
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]  # Simple username from email

            # Ensure username is unique
            i = 1
            base_username = username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{i}"
                i += 1

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                account_type='individual',  # Default account type
                is_active=True
            )
            return user, True


class VerifyEmailView(APIView):
    permission_classes = []

    def get(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)

            # Check if token is expired (24 hours)
            if user.verification_sent < timezone.now() - timezone.timedelta(hours=24):
                return Response({
                    "error": "Verification link has expired",
                    "code": "expired"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Activate user
            user.email_verified = True
            user.verification_token = None
            user.is_active = True
            user.save()

            # Return token for automatic login
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "detail": "Email verified successfully!",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type
                }
            })
        except CustomUser.DoesNotExist:
            return Response({
                "error": "Invalid verification token",
                "code": "invalid_token"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e),
                "code": "server_error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendVerificationEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the most recent unverified user with this email
            user = CustomUser.objects.filter(
                email=email,
                email_verified=False
            ).latest('date_joined')

            # Resend verification email
            user.send_verification_email(request)
            return Response({"detail": "Verification email resent."})

        except CustomUser.DoesNotExist:
            return Response({"error": "No unverified user found with this email."}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned:
            # Handle multiple users by selecting the most recent
            user = CustomUser.objects.filter(
                email=email,
                email_verified=False
            ).latest('date_joined')
            user.send_verification_email(request)
            return Response({"detail": "Verification email resent to the most recent registration."})

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Your account has been activated successfully! You may now log in.")
        else:
            return HttpResponse("Activation link is invalid or has expired.", status=400)
