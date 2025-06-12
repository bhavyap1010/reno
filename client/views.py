import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests

# if you want to use Authorization Code Grant, use this
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):
    http_method_names = ['post','get']  # Only allow POST

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        if not code:
            return Response({"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

        # Google token exchange
        token_url = "https://oauth2.googleapis.com/token"
        
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code"
        }


        res = requests.post(token_url, data=token_data)
        tokens = res.json()
            
        if "access_token" in tokens:
            user_info = self.get_user_info(tokens["access_token"])
            email = user_info.get("email", "unknown")
            message = f"hi there, your email is {email}"
            return HttpResponse(message)

        return Response({"error": "OAuth login failed"}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the code just like in POST
        token_url = "https://oauth2.googleapis.com/token"
        
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code"
        }


        res = requests.post(token_url, data=token_data)
        tokens = res.json()

        if "access_token" in tokens:
            user_info = self.get_user_info(tokens["access_token"])
            email = user_info.get("email", "unknown")
            return HttpResponse(f"hi there, your email is {email}")

        return Response({"error": "OAuth login failed"}, status=status.HTTP_400_BAD_REQUEST)


    def get_user_info(self, access_token):
        """Fetch the user's profile info (e.g. email) from Google."""
        try:
            response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return {}



class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
