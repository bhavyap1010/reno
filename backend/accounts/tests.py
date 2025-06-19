from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'account_type': 'individual'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        """Test new user registration"""
        data = {
            'username': 'newuser',
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'account_type': 'business'
        }
        response = self.client.post('/api/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        """Test user login functionality"""
        data = {
            'username': 'testuser',
            'password': 'TestPassword123!'
        }
        response = self.client.post('/api/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_logout(self):
        """Test user logout functionality"""
        # First login to get token
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!'
        }
        login_response = self.client.post('/api/accounts/login/', login_data)
        token = login_response.data['token']

        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Test logout
        response = self.client.post('/api/accounts/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_validation(self):
        """Test weak password rejection"""
        data = {
            'username': 'weakuser',
            'password': '123',
            'password2': '123',
            'email': 'weak@example.com',
            'first_name': 'Weak',
            'last_name': 'User',
            'account_type': 'individual'
        }
        response = self.client.post('/api/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_account_type_validation(self):
        """Test invalid account type rejection"""
        data = {
            'username': 'invaliduser',
            'password': 'ValidPassword123!',
            'password2': 'ValidPassword123!',
            'email': 'invalid@example.com',
            'first_name': 'Invalid',
            'last_name': 'User',
            'account_type': 'invalid_type'
        }
        response = self.client.post('/api/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('account_type', response.data)