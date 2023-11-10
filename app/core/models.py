from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
import uuid
import os
from chat.models import PrivateChat

# Minimum eight characters, at least one upper case English letter, 
# one lower case English letter,
# and one number.
PASSWORD_REGEX='^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'

def password_validator(password):
    if not re.fullmatch(PASSWORD_REGEX, password):

        raise ValidationError(
            "Minimum eight characters, at least one upper case English letter, one lower case English letter, and one number."
        )

def get_image_path(instance, filename):
    
    id=uuid.uuid4()

    suffix=os.path.split(filename)[1]

    return os.path.join('images', 'userprofile', (str(id) + suffix))


class UserManager(BaseUserManager):

    def _create_user(self, username, email, name, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        if not name:
            raise ValueError("The name attribute is required.")

        
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        
        user = self.model(username=username, email=email, name=name, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_user(self, username, email, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, name, password, **extra_fields)

    def create_superuser(self, username, email, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
        db_index=True,
    )
    password = models.CharField(
        "password", max_length=128, validators=[password_validator]
        )

    name = models.CharField('name', max_length=250, blank=False, null=False)

    email = models.EmailField('email address',unique=True, blank=False, db_index=True)
    bio = models.CharField('bio', max_length=500, blank=True)
    image = models.ImageField(null=True, upload_to=get_image_path)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ,
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Message(models.Model):
    
    sender=models.ForeignKey(to=User, blank=False, null=False)
    content=models.TextField()
    date=models.DateTimeField(auto_now_add=True)


class PrivateChatMessageManager(models.Manager):
    """manager class for private chat message"""

    def create(self, sender, recierver, content):
        
        instance=self.model(sender, recierver, content)
        instance.save()

        privatechat=instance.reciever 

        privatechat.messages.add(instance)
        #a proccess must be done here to add this
        # message to unread messages of user


class PrivateChatMessage(Message):
    """message object that is being used in private chats."""

    reciever=models.ForeignKey(to=PrivateChat, related_name='messages', blank=False, null=False)
    objects=PrivateChatMessageManager()