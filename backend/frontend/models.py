from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('user', 'User'),
        ('provider', 'Service Provider'),
    ]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

