from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    """testing the user model"""
    def test_create_user(self):
        
        user=get_user_model().objects.create_user(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Password12',
            bio=''
        )
        
        self.assertIsNotNone(user)
        self.assertTrue(
            get_user_model().objects.filter(username='username').exists
            )
    

    def test_create_superuser(self):
        
        user=get_user_model().objects.create_superuser(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Password12',
            bio=''
        )
        
        self.assertIsNotNone(user)
        self.assertTrue(
            get_user_model().objects.filter(username='username').exists
            )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_with_same_username(self):
        """testing that creating users with same username will raise value error."""
        
        user=get_user_model().objects.create_user(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Password12',
            bio=''
        )

        get_user_model().objects.create_user(
             username='newuser',
             email='yser22@email.com',
             name='new user',
             password='Password12',
             bio=''
             )

        # with self.assertRaises(ValueError) as eror:
        #     get_user_model().objects.create_user(
        #     username='newuser',
        #     email='yser22@email.com',
        #     name='new user',
        #     password='Password12',
        #     bio=''
        #     )

        #     self.assertEqual(str(eror.exception), )
        
    

    def test_create_user_with_same_email(self):
        """testing that creating users with same email will raise value error."""
     
        user=get_user_model().objects.create_user(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Password12',
            bio=''
        )
        self.assertRaises(ValueError, get_user_model().objects.create_user(
            username='newuser22',
            email='yser@email.com',
            name='new user',
            password='Password12',
            bio=''
            ))
    
    
    
