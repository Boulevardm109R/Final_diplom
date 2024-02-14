import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from backend.models import CustomUser

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.change_password_url = reverse('change_password')
        self.request_password_url = reverse('request_password')

    def test_signup_view(self):
        # Test valid signup request
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'type': 'distributor'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse('homepage'))

        # Test invalid signup request
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'type': 'invalid_type'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'This field is required.')

    def test_login_view(self):
        # Test valid login request
        user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse('homepage'))

        # Test invalid login request
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_change_password_view(self):
        # Test valid change password request
        user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        data = {
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Your password has been successfully changed.')

        # Test invalid change password request
        data = {
            'new_password1': 'newpassword',
            'new_password2': 'wrongpassword'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'The two password fields didn&#x27;t match.')

    def test_request_password_view(self):
        # Test valid request password request
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.request_password_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Check your email')

        # Test invalid request password request
        response = self.client.post(self.request_password_url, {'email': 'wrong@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'This field is required.')