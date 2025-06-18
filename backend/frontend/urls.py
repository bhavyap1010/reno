from django.urls import path
from .views import RegisterAPIView, LoginAPIView, home_view

urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('home/', home_view, name='api-home'),
]
