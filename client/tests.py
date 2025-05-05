from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import BusinessProfile, ServiceRequest, Chatroom, Message
from django.urls import reverse

class ClientAppTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

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
        self.assertRedirects(response, reverse("register"))

    def test_register_user(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "password123",
            "password2": "password123",
            "account_type": "individual"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_user(self):
        response = self.client.post(reverse("login"), {
            "username": "user1",
            "password": "password1"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_create_service_request(self):
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("request-service"), {
            "title": "New Service Request",
            "services_needed": ["plumbing"],
            "location": "New Location",
            "description": "New Description"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(ServiceRequest.objects.filter(title="New Service Request").exists())

    def test_write_review(self):
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("write-review", args=[self.business_profile.id]), {
            "rating": 5,
            "comment": "Great service!"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful review
        self.assertEqual(self.business_profile.reviews.count(), 1)

    def test_chat_with_other_user(self):
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("chat-start"), {
            "other_user": "user2"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("room_name", response.json())

    def test_chat_page_access(self):
        self.client.login(username="user1", password="password1")
        chatroom = Chatroom.objects.create(room_name="testroom")
        chatroom.participants.add(self.user1, self.user2)
        response = self.client.get(reverse("chat-home", args=["testroom"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chit-Chat")

    def test_prevent_chat_with_self(self):
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("chat-start"), {
            "other_user": "user1"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)  # Bad request for chatting with self

