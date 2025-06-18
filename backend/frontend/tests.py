from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser
from django.contrib.admin.sites import site

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('api-register')

    def test_register_user_success(self):
        data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "account_type": "user",
            "password1": "testpassword123",
            "password2": "testpassword123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())

    def test_register_user_password_mismatch(self):
        data = {
            "username": "testuser2",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser2@example.com",
            "account_type": "user",
            "password1": "password123",
            "password2": "differentpassword"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Passwords do not match", str(response.data))

    def test_register_user_duplicate_email(self):
        CustomUser.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="password123",
            account_type="user"
        )
        data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "existing@example.com",
            "account_type": "user",
            "password1": "password123",
            "password2": "password123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", str(response.data))
