from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField  # type: ignore


SERVICE_CHOICES = [
    ('cleaning', 'Cleaning'),
    ('plumbing', 'Plumbing'),
    ('electrical', 'Electrical'),
    ('landscaping', 'Landscaping'),
    ('delivery', 'Delivery'),
    ('other', 'Other'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(
        max_length=10,
        choices=[('individual', 'Individual'), ('business', 'Business')],
        help_text="Select the type of user account."
    )
    email_is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    name = models.CharField(max_length=100, help_text="Enter your business name.")
    services = MultiSelectField(
        choices=SERVICE_CHOICES,
        help_text="Select all services your business offers.",
        blank=True
    )
    service_location = models.CharField(max_length=255, help_text="Where is your business based?")
    image = models.ImageField(upload_to='business_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Business Profile"
        verbose_name_plural = "Business Profiles"


class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_requests', default=1)
    title = models.CharField(max_length=100, help_text="Brief title for the request.")
    services_needed = MultiSelectField(
        choices=SERVICE_CHOICES,
        help_text="Select all services your business offers.",
        blank=True
    )
    location = models.CharField(max_length=100, help_text="Where should the service be delivered?")
    description = models.TextField(help_text="Additional details about the request.")
    image = models.ImageField(upload_to='service_requests/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Service Request"
        verbose_name_plural = "Service Requests"


class Review(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.business.name}"


class Chatroom(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(User, related_name="Chatrooms")

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"