from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
        }

    def test_signup(self):
        """Test user signup"""
        response = self.client.post('/api/auth/signup/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('user', response.data)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_login(self):
        """Test user login"""
        # Create user first
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            name='Test User',
            password='testpass123'
        )
        
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_current_user(self):
        """Test getting current user profile"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            name='Test User',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
