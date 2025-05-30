from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp
from allauth.account.models import EmailAddress
from django.contrib.sites.models import Site
from django.urls import reverse
from django.conf import settings
from .models import BusinessProfile, ServiceRequest, Chatroom, Message, Profile, ServiceRequestImage
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile

class ClientAppTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="password2", email="user2@example.com")
        Profile.objects.create(user=self.user1, account_type="individual")
        Profile.objects.create(user=self.user2, account_type="business")

        site = Site.objects.get_current()
        social_app = SocialApp.objects.create(
            provider="google",
            name="Google",
            client_id="dummy-client-id",
            secret="dummy-secret",
        )
        social_app.sites.add(site)

        self.business_profile = BusinessProfile.objects.create(
            user=self.user2,
            name="Test Business",
            services=["cleaning", "plumbing"],
            service_location="Test Location"
        )

        self.service_request = ServiceRequest.objects.create(
            user=self.user1,
            title="Test Service Request",
            services_needed=["cleaning"],
            location="Test Location",
            description="Test Description"
        )

        self.client = Client()

    def confirm_email(self, user):
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

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
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        user = User.objects.get(username="newuser")
        self.assertEqual(user.profile.account_type, "individual")
        self.assertContains(response, "Sign In")

    def test_login_with_username(self):
        self.confirm_email(self.user1)
        response = self.client.post(reverse("account_login"), {
            "login": "user1",
            "password": "password1"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertContains(response, "Logout")

    def test_login_with_email(self):
        self.confirm_email(self.user1)
        response = self.client.post(reverse("account_login"), {
            "login": "user1@example.com",
            "password": "password1"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertContains(response, "Logout")

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("account_login"), {
            "login": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The username and/or password you specified are not correct.")

    @unittest.skipIf(getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "") == "mandatory",
                     "Skipping session login test due to mandatory email verification")
    def test_login_sets_session(self):
        self.confirm_email(self.user1)
        response = self.client.post(reverse("account_login"), {
            "login": "user1",
            "password": "password1"
        }, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_optional_verification_login(self):
        user = User.objects.create_user(username="optuser", password="optpass", email="opt@example.com")
        Profile.objects.create(user=user, account_type="individual")
        response = self.client.post(reverse("account_login"), {
            "login": "optuser",
            "password": "optpass"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_redirects_to_next(self):
        self.confirm_email(self.user1)
        some_url = reverse("home")
        login_url = reverse("account_login") + f"?next={some_url}"
        response = self.client.post(login_url, {
            "login": "user1",
            "password": "password1"
        })
        self.assertRedirects(response, some_url)

    def test_signup_missing_password(self):
        response = self.client.post(reverse("account_signup"), {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
            "account_type": "individual"
        })
        form = response.context["form"]
        self.assertIn("This field is required.", form.errors["password1"])

    def test_signup_mismatched_passwords(self):
        response = self.client.post(reverse("account_signup"), {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPass987!",
            "password2": "WrongPass987!",
            "account_type": "individual"
        })
        form = response.context["form"]
        self.assertIn("password2", form.errors)
        self.assertTrue(
            any("same password" in msg.lower() for msg in form.errors["password2"])
        )

    def test_login_inactive_user(self):
        inactive = User.objects.create_user(username="inactive", password="password", email="inactive@example.com", is_active=False)
        Profile.objects.create(user=inactive, account_type="individual")
        response = self.client.post(reverse("account_login"), {
            "login": "inactive",
            "password": "password"
        })
        self.assertContains(response, "Invalid login credentials.")

    def test_logout_clears_session(self):
        self.client.login(username="user1", password="password1")

        response = self.client.post(reverse("account_logout"), follow=True)
        session = self.client.session

        self.assertFalse(response.context["user"].is_authenticated)
        self.assertNotIn("_auth_user_id", session)

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

    def test_signup_invalid_email_format(self):
        response = self.client.post(reverse("account_signup"), {
            "username": "invalidemailuser",
            "email": "not-an-email",
            "password1": "Validpass123!",
            "password2": "Validpass123!",
            "account_type": "individual"
        })
        form = response.context["form"]
        self.assertIn("Enter a valid email address.", form.errors.get("email", []))

    def test_signup_duplicate_username(self):
        User.objects.create_user(username="duplicateuser", email="dupe@example.com", password="somepass123")
        response = self.client.post(reverse("account_signup"), {
            "username": "duplicateuser",
            "email": "new@example.com",
            "password1": "Newpass123!",
            "password2": "Newpass123!",
            "account_type": "individual"
        })
        form = response.context["form"]
        self.assertIn("A user with that username already exists.", form.errors.get("username", []))

    def test_signup_password_too_short(self):
        response = self.client.post(reverse("account_signup"), {
            "username": "shortpassuser",
            "email": "shortpass@example.com",
            "password1": "123",
            "password2": "123",
            "account_type": "individual"
        })
        form = response.context["form"]
        self.assertTrue(any("too short" in msg.lower() for msg in form.errors.get("password1", [])))
        # Ensure the service request still exists
        self.assertTrue(ServiceRequest.objects.filter(id=request_id).exists())

class ServiceRequestImageUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_service_request_image_upload(self):
        self.client.login(username='testuser', password='testpass')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B',
            content_type='image/jpeg'
        )
        service_request = ServiceRequest.objects.create(
            user=self.user,
            title='Test Request',
            services_needed=['cleaning'],
            location='Test Location',
            description='Test Description'
        )
        ServiceRequestImage.objects.create(
            service_request=service_request,
            image=image
        )
        self.assertEqual(service_request.images.count(), 1)
        self.assertTrue(service_request.images.first().image.name.startswith('service_requests/'))

class BusinessProfileImageUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bizuser', password='testpass')

    def test_business_profile_image_upload(self):
        self.client.login(username='bizuser', password='testpass')
        image = SimpleUploadedFile(
            name='biz_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B',
            content_type='image/jpeg'
        )
        profile = BusinessProfile.objects.create(
            user=self.user,
            name='Biz Name',
            services=['cleaning'],
            service_location='Biz Location',
            image=image
        )
        self.assertIsNotNone(profile.image)
        self.assertTrue(profile.image.name.startswith('business_profiles/'))
