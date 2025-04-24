from django.db import models
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField # type: ignore

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

class serviceRequest(models.Model):
    service_choices = [
        ('cleaning', 'cleaning'),
        ('plumbing', 'plumbing'),
        ('electrical', 'electrical'),
        ('landscaping', 'landscaping'),
        ('delivery', 'delivery'),
        ('other', 'other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_requests', default=1)
    title = models.CharField(max_length=100, default='default title')
    services_needed = MultiSelectField(choices=service_choices)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    business = models.ForeignKey('businessProfile', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.business.name}"
    
class chatroom(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(User, related_name="chatrooms")

class Messages(models.Model):
    room = models.ForeignKey(chatroom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
