from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('business', 'Business')])
    email_is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
