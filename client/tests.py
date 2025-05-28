from django.test import TestCase, Client
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.urls import reverse
from .models import BusinessProfile, ServiceRequest, Chatroom, Message, Profile
from django.conf import settings
import unittest

class ClientAppTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password1", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="password2", email="user2@example.com")

        # Set account types
        Profile.objects.create(user=self.user1, account_type="individual")
        Profile.objects.create(user=self.user2, account_type="business")

        # Create a dummy social app to satisfy template logic
        site = Site.objects.get_current()
        social_app = SocialApp.objects.create(
            provider="google",
            name="Google",
            client_id="dummy-client-id",
            secret="dummy-secret",
        )
        social_app.sites.add(site)

        # Create a business profile for user2
        self.business_profile = BusinessProfile.objects.create(
            user=self.user2,
            name="Test Business",
            services=["cleaning", "plumbing"],
            service_location="Test Location"
        )

        # Create a service request for user1
        self.service_request = ServiceRequest.objects.create(
            user=self.user1,
            title="Test Service Request",
            services_needed=["cleaning"],
            location="Test Location",
            description="Test Description"
        )

        # Set up the test client
        self.client = Client()

    def test_home_redirects_for_anonymous_user(self):
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, reverse("account_login"))

    def test_register_user(self):
        response = self.client.post(reverse("account_signup"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Uncommon$Password987",
            "password2": "Uncommon$Password987",
            "account_type": "individual"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertEqual(User.objects.get(username="newuser").profile.account_type, "individual")

    def test_login_with_username(self):
        response = self.client.post(reverse("account_login"), {
            "login": "user1",
            "password": "password1"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_email(self):
        response = self.client.post(reverse("account_login"), {
            "login": "user1@example.com",
            "password": "password1"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("account_login"), {
            "login": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The username and/or password you specified are not correct.")

    # NOTE: This test assumes email verification is OFF.
    # If email verification is mandatory, user must confirm email before login is allowed.
    @unittest.skipIf(getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "") == "mandatory",
                     "Skipping session login test due to mandatory email verification")
    def test_login_sets_session(self):
        response = self.client.post(reverse("account_login"), {
            "login": "user1",
            "password": "password1"
        }, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_create_service_request(self):
        self.client.login(username="user1", password="password1")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        response = self.client.post(reverse("request-service"), {
            "title": "New Service Request",
            "services_needed": ["plumbing"],
            "location": "New Location",
            "description": "New Description"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ServiceRequest.objects.filter(title="New Service Request").exists())

    def test_write_review(self):
        self.client.login(username="user1", password="password1")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        response = self.client.post(reverse("write-review", args=[self.business_profile.id]), {
            "rating": 5,
            "comment": "Great service!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.business_profile.reviews.count(), 1)

    def test_chat_with_other_user(self):
        self.client.login(username="user1", password="password1")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        response = self.client.post(reverse("chat-start"), {
            "other_user": "user2"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("room_name", response.json())

    def test_chat_page_access(self):
        self.client.login(username="user1", password="password1")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        chatroom = Chatroom.objects.create(room_name="testroom")
        chatroom.participants.add(self.user1, self.user2)
        response = self.client.get(reverse("chat-home", args=["testroom"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User2")

    def test_prevent_chat_with_self(self):
        self.client.login(username="user1", password="password1")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        response = self.client.post(reverse("chat-start"), {
            "other_user": "user1"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_own_service_request(self):
        self.client.login(username="user1", password="password1")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        request_id = self.service_request.id
        response = self.client.post(reverse("delete-service-request", args=[request_id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(ServiceRequest.objects.filter(id=request_id).exists())

    def test_prevent_deletion_by_other_user(self):
        self.client.login(username="user2", password="password2")
        session = self.client.session
        session['post_signup_needs_account_type'] = False
        session.save()
        request_id = self.service_request.id
        response = self.client.post(reverse("delete-service-request", args=[request_id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(ServiceRequest.objects.filter(id=request_id).exists())