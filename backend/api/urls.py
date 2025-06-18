from django.urls import path
from . import views

urlpatterns = [
    path("service-requests/", views.ServiceRequestListCreate.as_view(), name="service-request-list"),
    path("service-requests/delete/<int:pk>/", views.ServiceRequestDelete.as_view(), name="delete-service-request"),
]