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
    path('business-profile/', views.create_or_edit_business_profile, name='business-profile'),
    path('request-service/', views.create_service_request, name='request-service'),
    path('review/<int:business_id>/', views.write_review, name='write-review'),
    path('business/<int:business_id>/', views.business_detail, name='business-detail'),    
    path("chats/", views.chat_home, name="chat-home"),
    path("chats/<str:room_name>/", views.chat_home, name="chat-home"),
    path("start-chat/", views.start_chat, name="chat-start"),  # assuming this view exists

]