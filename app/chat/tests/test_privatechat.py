from django.test import TestCase
from django.contrib.auth import get_user_model
from chat.models import PrivateChat

class PrivateChatModel(TestCase):
    """testing privatechats model"""

    def setUp(self):

        self.user1=get_user_model().objects.create_user(
            username='firstuser',
            email='yser@email.com',
            name='new user',
            password='Password_12',
            bio=''
        )

        self.user2=get_user_model().objects.create_user(
            username='seconduser',
            email='yyyser@email.com',
            name='new user',
            password='Password_23',
            bio=''
        )

    
    def test_create_private_chat(self):
        """test creating object of private chat"""

        usernames=[self.user1.username, self.user2.username,]

        private_chat=PrivateChat.objects.create(usernames)

        chatid=self.user1.username + '*' + self.user2.username

        self.assertTrue(PrivateChat.objects.filter(chatid=chatid).exists())

        self.assertEqual(private_chat.get_usernames(), usernames)