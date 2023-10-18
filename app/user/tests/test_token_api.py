from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

TOKEN_AUTH_URL=reverse('token-auth')
TOKEN_REFRESH_URL=reverse('token-refresh')
TOKEN_VERIFY_URL=reverse('token-verify')

class TestTokenApi(TestCase):

    def setUp(self):
        self.user=get_user_model().objects.create_user(
            username='username',
            password='mypassCa45',
            name='user',
            email='my@email.com',
            bio='empty',
        )
        self.client=APIClient()

    def test_auth_user(self):
        """test authenticating with user and get token."""

        payload={
            'username':'username',
            'password':'mypassCa45',
        }
        
        response=self.client.post(TOKEN_AUTH_URL, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_access_token(self):
        """test refreshing the access token using refresh token."""

        payload={
            'username':'username',
            'password':'mypassCa45',
        }
        
        response=self.client.post(TOKEN_AUTH_URL, payload)
        
        payload={
            'refresh':response.data['refresh']
        }

        response=self.client.post(TOKEN_REFRESH_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    # def test_varify_access_token(self):
    #     """test verifyinging the access token."""

    #     payload={
    #         'username':'username',
    #         'password':'mypassCa45',
    #     }
        
    #     response=self.client.post(TOKEN_AUTH_URL, payload)
        
    #     payload={
    #         'access':response.data['access']
    #     }

    #     response=self.client.post(TOKEN_VERIFY_URL, payload)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    