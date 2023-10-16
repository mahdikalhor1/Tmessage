from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from user.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

USER_CREATE_URL=reverse('user:user-list')

class UserApiTest(TestCase):
    """testing the user api fetures."""

    def setUp(self):
        self.client=APIClient()

    def test_signUp(self):
        
        payload={
            'username':'newuser',
            'password':'NewUser52',
            'email':'myemail@emali.com',
            'name':'the name',
            'bio':'test bio',
        }

        response=self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        serializer = UserCreateSerializer(user)
        self.assertEqual(response.data, serializer.data)

        
    def test_signUp_with_blank_username(self):
        "test creating user with blank username"
        payload={
            
            'password':'NewUser52',
            'email':'myemail@emali.com',
            'name':'the name',
            'bio':'test bio',
        }

        response=self.client.post(USER_CREATE_URL, payload)
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signUp_with_invalid_email(self):
        "test creating user with invalid email"
        payload={
            'username':'newuser',
            'password':'NewUser52',
            'email':'user.com',
            'name':'the name',
            'bio':'test bio',
        }

        response=self.client.post(USER_CREATE_URL, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signUp_with_weak_pass(self):
        "test creating user with weak password"
        payload={
            'username':'newuser',
            'password':'NewUser',
            'email':'user@gmeil.com',
            'name':'the name',
            'bio':'test bio',
        }

        response=self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)