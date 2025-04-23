from django.db import models
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('business', 'Business')])
    email_is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class businessProfile(models.Model):
    service_choices = [
        ('cleaning', 'cleaning'),
        ('plumbing', 'plumbing'),
        ('electrical', 'electrical'),
        ('landscaping', 'landscaping'),
        ('delivery', 'delivery'),
        ('other', 'other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    name = models.CharField(max_length=100)
    services = MultiSelectField(choices=service_choices)

    service_location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
