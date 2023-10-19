from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from user.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

USER_CREATE_URL=reverse('user:user-list')

def get_user_update_url(user_id):
    return reverse('user:user-detail', args=[user_id,])
class UserApiCreateTest(TestCase):
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
            'password':'NewUserr',
            'email':'user@gmeil.com',
            'name':'the name',
            'bio':'test bio',
        }

        response=self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserApiUpdateTest(TestCase):
    """test for update api of user class"""

    def setUp(self):
        self.user=get_user_model().objects.create_user(
            username='username',
            password='mypassCa45',
            name='user',
            email='my@email.com',
            bio='empty',
        )
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_valid_update(self):

        payload={
            'username':'newusername',
            'name':'newname',
            'email':'mynew@email.com',
            'bio':'mybio'
        }

        url=get_user_update_url(self.user.id)
        response=self.client.patch(url, payload)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()

        for key, value in payload.items():
            self.assertEqual(getattr(self.user, key), value)


    def test_update_password(self):

        payload={
            'password':'newPAss89'
        }

        url=get_user_update_url(self.user.id)
        response=self.client.patch(url, payload)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password(payload['password']))
    
    def test_update_with_weak_password(self):

        payload={
            'password':'newPasssss'
        }

        url=get_user_update_url(self.user.id)
        response=self.client.patch(url, payload)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(payload['password']))
    

    def test_invalid_update(self):
        """test updating with existing username"""
        get_user_model().objects.create_user(
            username='newusername',
            password='NewUsersPAss45',
            name='newname',
            email='mynew@email.com',
        )
        payload={
            'username':'newusername',
            'name':'newname',
            'bio':'mybio'
        }

        url=get_user_update_url(self.user.id)
        response=self.client.patch(url, payload)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
