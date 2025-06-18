from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_requests")

    def __str__(self):
        return self.title
