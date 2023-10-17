from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from core.models import User
class UserModelTest(TestCase):
    """testing the user model"""
    def test_create_user(self):
        
        user=get_user_model().objects.create_user(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Password90',
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
            password='Password_12',
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
            password='Password_12',
            bio=''
        )

        # self.assertRaises(get_user_model().objects.create_user(
        #      username='newuser',
        #      email='yser22@email.com',
        #      name='new user',
        #      password='Password_12',
        #      bio=''
        #      )
        #      )

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
            username='newuser',
            email='yser22@email.com',
            name='new user',
            password='Password12',
            bio=''
            )
        
    

    def test_create_user_with_same_email(self):
        """testing that creating users with same email will raise value error."""
     
        user=get_user_model().objects.create_user(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Password_12',
            bio=''
        )

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username='newuser22',
                email='yser@email.com',
                name='new user',
                password='Password_12',
                bio=''
                )
    
    def test_create_user_invalid_password(self):
        """test crating user with weak password"""
        
        with self.assertRaises(ValidationError):
            user=User(
            username='newuser',
            email='yser@email.com',
            name='new user',
            password='Passwort',
            bio=''
            )
            user.full_clean()
            user.save()
            
