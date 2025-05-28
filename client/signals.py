from django.dispatch import receiver
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def handle_social_signup(request, user, **kwargs):
    # Mark that user must choose an account type
    request.session['post_signup_needs_account_type'] = True