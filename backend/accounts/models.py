from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from .managers import CustomUserManager

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from .tokens import account_activation_token
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('business', 'Business'),
    )

    email = models.EmailField(unique=True, verbose_name=_("email address"))

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='individual')
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    verification_sent = models.DateTimeField(blank=True, null=True)

    def send_verification_email(self, request):
        # Generate verification token
        import secrets
        self.verification_token = secrets.token_urlsafe(50)
        self.verification_sent = timezone.now()
        self.save()

        # Build FRONTEND verification URL
        frontend_url = request.build_absolute_uri('/').replace(
            'localhost:8000',
            'localhost:5173'  # Replace with your frontend domain
        )
        verification_url = f"{frontend_url}verify-email/{self.verification_token}"

        # Send email
        subject = "Verify your email address"
        message = f"Please click the link to verify your email: {verification_url}"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False
        )