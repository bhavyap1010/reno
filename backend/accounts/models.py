from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('business', 'Business'),
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)