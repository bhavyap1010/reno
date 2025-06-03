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
        help_text="Select the type of user account.",
        blank=False
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
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='available',
        help_text="Set your current business status."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Business Profile"
        verbose_name_plural = "Business Profiles"


class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_requests')
    title = models.CharField(max_length=100)
    services_needed = MultiSelectField(choices=SERVICE_CHOICES, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class ServiceRequestImage(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_requests/')

    def __str__(self):
        return f"Image for {self.service_request.title}"


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
    deleted = models.BooleanField(default=False)  # <-- Add this field

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"