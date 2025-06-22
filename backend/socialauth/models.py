from django.db import models
from django.contrib.auth.models import User

def profile_path(instance, filename): 
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):   # need to update the model to as a normal user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
