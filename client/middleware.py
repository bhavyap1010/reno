from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# Middleware to ensure that users have an account type and username set (for when account is made via social app)

class AccountTypeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        # Only redirect if either is missing
        needs_redirect = (
            not hasattr(request.user, 'profile') or not request.user.username
        )

        excluded_paths = [
            reverse('choose_account_type'),
            reverse('admin:login'),
            reverse('account_logout'),
            reverse('account_login'),
            '/admin/',
            '/static/',
        ]
        if needs_redirect and not any(request.path.startswith(p) for p in excluded_paths):
            return redirect('choose_account_type')