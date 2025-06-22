from django.urls import path
from .views import GoogleLogin,UserMe, FormLogin, SignupView
from rest_framework_simplejwt.views import (TokenRefreshView,)
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('users/me/', UserMe.as_view(), name='user_detail'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('formlogin/', FormLogin.as_view(), name='form_login'),
    path('signup/', SignupView.as_view(), name='signup'),
]
