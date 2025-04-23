from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.signIn, name="login"),
    path("verify/", views.verify, name="verify"),
    path("home/", views.home, name="home"),  
    path("logout/", LogoutView.as_view(next_page="register"), name="logout-user"),  # Add this line



]