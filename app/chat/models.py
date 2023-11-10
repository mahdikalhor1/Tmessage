from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model



class Chat(models.Model):

    pass
    # id=models.CharField('id', max_length=301, unique=True, primary_key=True,
    #                      validators=[UnicodeUsernameValidator,],
    #                      db_index=True)
#    messages=
#    users=models.ManyToManyField(to=get_user_model())

class PrivateChatManager(models.Manager):
    
    def create(self, usernames, **kwargs):

        chatid=self.create_chatid(usernames)
        instance=self.model(chatid=chatid)
        instance.save()

        return instance
    
    def create_chatid(self, usernames):

        if usernames[0] < usernames[1]:
            id=usernames[0] + '*' + usernames[1]
        else: 
            id=usernames[1] + '*' + usernames[0]
        return id
    
class PrivateChat(models.Model):

    chatid=models.CharField('id', max_length=301, unique=True,
                         primary_key=True, db_index=True)
    
    objects=PrivateChatManager()

    def get_usernames(self):
        usernames=self.chatid.split('*')
        return usernames
    
    """messages list can be accessed using instance.messages"""