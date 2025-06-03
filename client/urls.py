from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("logout/", LogoutView.as_view(next_page="account_login"), name="logout-user"),
    path('business-profile/', views.create_or_edit_business_profile, name='business-profile'),
    path('request-service/', views.create_service_request, name='request-service'),
    path('review/<int:business_id>/', views.write_review, name='write-review'),
    path('business/<int:business_id>/', views.business_detail, name='business-detail'),
    path("chats/", views.chat_home, name="chat-home"),
    path("chats/<str:room_name>/", views.chat_home, name="chat-home"),
    path("start-chat/", views.start_chat, name="chat-start"),  # assuming this view exists
    path('delete-request/<int:request_id>/', views.delete_service_request, name='delete-service-request'),
    path('choose-account-type/', views.choose_account_type_and_username, name='choose_account_type'),
    path('service-request/<int:request_id>/', views.service_request_detail, name='service-request-detail'),
    path('delete-message/', views.delete_message, name='delete-message'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),  # <-- Add this line
]