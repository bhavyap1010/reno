from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, GoogleLogin, VerifyEmailView, ResendVerificationEmail, ActivateAccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('social/google/', GoogleLogin.as_view(), name='google_login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmail.as_view(), name='resend-verification'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

]
