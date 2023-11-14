from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import PrivateChatMessage
from chat.models import PrivateChat

class TestPVMessages(TestCase):
    """test creating messages that are send trougth private chat"""

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

    def test_create_pvmessage_object(self):
        """test createing a valid private chat message"""

        payload={
            'sender':self.user1.username,
            'reciever':self.user2.username,
            'content':'some text for message',
        }
        pvmessage=PrivateChatMessage.objects.create(**payload)

        self.assertTrue(PrivateChatMessage.objects.filter(id=pvmessage.id).exists())
        self.assertIn(pvmessage, self.user2.unread_messages.all())
        
        pv_id=self.user1.username + '*' + self.user2.username

        self.assertTrue(PrivateChat.objects.filter(chatid=pv_id).exists())
        pvchat=PrivateChat.objects.get(chatid=pv_id)

        self.assertIn(pvmessage, pvchat.messages.all())
