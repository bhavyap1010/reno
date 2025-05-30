from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import BusinessProfile, ServiceRequest, Chatroom, Message, ServiceRequestImage
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

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
        self.assertContains(response, "User2")  # Check for the other user's name instead of "Chit-Chat"

    def test_prevent_chat_with_self(self):
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("chat-start"), {
            "other_user": "user1"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)  # Bad request for chatting with self

    def test_delete_own_service_request(self):
        self.client.login(username="user1", password="password1")
        request_id = self.service_request.id

        response = self.client.post(reverse("delete-service-request", args=[request_id]))

        # Should redirect to home after deletion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        # Check that the service request is deleted
        self.assertFalse(ServiceRequest.objects.filter(id=request_id).exists())

    def test_prevent_deletion_by_other_user(self):
        self.client.login(username="user2", password="password2")
        request_id = self.service_request.id

        response = self.client.post(reverse("delete-service-request", args=[request_id]))

        # Forbidden for non-owners
        self.assertEqual(response.status_code, 403)

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