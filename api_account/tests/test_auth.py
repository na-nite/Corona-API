from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient


class AuthTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        """Test register a new user"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'password2': 'testpass',
            'first_name': 'Amir',
            'last_name': 'AEK',

        }
        url = reverse("user:register")
        res = self.client.post(url, payload)
        user = get_user_model().objects.get(**res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    def test_login(self):
        get_user_model().objects.create_user(email='test@gmail.com',
                                             password='testpass')
        url = reverse("user:login")
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)
