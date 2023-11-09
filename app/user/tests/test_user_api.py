from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from user.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from user.serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import os


USER_CREATE_URL=reverse('user:user-list')
MY_PROFILE_URL=reverse('user:my-profile')
PROFILE_IMAGE_URL=reverse('user:profileimage')
# USER_PROFILE_URL=reverse('user:userprofile-detail')

def get_other_user_profile_url(username):
    return reverse('user:userprofile-detail', args=[username,])

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

class UserApiDetailTest(TestCase):
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

        response=self.client.patch(MY_PROFILE_URL, payload)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()

        for key, value in payload.items():
            self.assertEqual(getattr(self.user, key), value)


    def test_update_password(self):

        payload={
            'password':'newPAss89'
        }

        
        response=self.client.patch(MY_PROFILE_URL, payload)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password(payload['password']))
    
    def test_update_with_weak_password(self):

        payload={
            'password':'newPasssss'
        }

        response=self.client.patch(MY_PROFILE_URL, payload)

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

        response=self.client.patch(MY_PROFILE_URL, payload)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_my_profile(self):
        """test getting authenticated users profile"""

        response=self.client.get(MY_PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for key,value in response.data.items():
            self.assertEqual(value, getattr(self.user, key))

    def test_get_user_profile(self):
        """test getting other users profile"""

        newuser=get_user_model().objects.create_user(
            username='newusername',
            password='NewUsersPAss45',
            name='newname',
            email='mynew@email.com',
        )

        url = get_other_user_profile_url(newuser.username)
        
        response=self.client.get(url)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        
        for key , value in response.data.items():
            self.assertEqual(getattr(newuser, key), value) 

class UserApiPublicTest(TestCase):
    """requesting with unauthorized user to endpionts"""

    def setUp(self):
        self.client=APIClient()

    def test_update_user(self):
        """test request to updating with an unauthorized user."""
        payload={
            'name':'mynewname'
        }

        response=self.client.patch(MY_PROFILE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_myprofile(self):
        """test requesting with unauthorized user."""

        response=self.client.get(MY_PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_other_users_profile(self):
        """test requesting with unauthorized user."""

        newuser=get_user_model().objects.create_user(
            username='newusername',
            password='NewUsersPAss45',
            name='newname',
            email='mynew@email.com',
        )

        url = get_other_user_profile_url(newuser.username)
            
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_get_my_profile(self):
    #     """test getting other users profile"""

    #     newuser=get_user_model().objects.create_user(
    #         username='newusername',
    #         password='NewUsersPAss45',
    #         name='newname',
    #         email='mynew@email.com',
    #     )

    #     url=get_user_update_url(newuser.username)
    #     response=self.client.get(url)

    #     self.assertTrue(response.data, status.HTTP_200_OK)

    #     serializer=UserSerializer(data=newuser)
    #     serializer.is_valid()

    #     self.assertEqual(serializer.data, response.data)


class TestUserImageAPI(TestCase):
    """tests for user's profile image."""

    def setUp(self):
        self.user=get_user_model().objects.create(
            username='newuser',
            email='myuser@gmail.com',
            password='MyPass7878',
            name='iamtheuser',
        )

        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        """deleting user image after tests are done."""
        self.user.image.delete()
    
    def test_set_image(self):
        """test setting image of user."""


        image = SimpleUploadedFile(name='test_image.png', content=open('user/tests/test_files/test_image.png', 'rb').read(), content_type='image/png')
        
        payload={
            'image': image
        }

        response=self.client.patch(PROFILE_IMAGE_URL, payload, format='multipart')
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
        self.assertTrue(os.path.exists(self.user.image.path))
    
    def test_send_invalid_image(self):
        """test sending invalid data as image."""

        payload={
            'image':'invalid data',
        }

        response=self.client.patch(PROFILE_IMAGE_URL, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_delete_image(self):
        """test deleting users image"""

        "send image"
        image = SimpleUploadedFile(name='test_image.png', content=open('user/tests/test_files/test_image.png', 'rb').read(), content_type='image/png')
        
        payload={
            'image': image
        }

        response=self.client.patch(PROFILE_IMAGE_URL, payload, format='multipart')

        path = self.user.image.path

        response=self.client.delete(PROFILE_IMAGE_URL)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(os.path.exists(path))
    

    def test_get_my_image(self):
        """test getting authenticated users profile image."""

        response=self.client.get(PROFILE_IMAGE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('image' ,response.data)

    def test_get_another_user_image(self):
        """test getting another users profile image."""

        newuser=get_user_model().objects.create_user(
            username='newusername',
            password='NewUsersPAss45',
            name='newname',
            email='mynew@email.com',
        )

        url = get_other_user_profile_url(newuser.uysername)
        
        response=self.client.get(url)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)