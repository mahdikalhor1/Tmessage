from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model
class Chat(models.Model):

    id=models.CharField('id', max_length=301,unique=True,
                         validators=[UnicodeUsernameValidator,],
                         db_index=True)
#    messages=
    users=models.ManyToManyField(to=get_user_model())

class PrivateChat(Chat):

    id=models.CharField('id', max_length=301,unique=True, db_index=True)
    
    def create_id(self):
        username_1=self.users.get(0).username
        username_2=self.users.get(1).username

        if username_1 > username_2:
            id=username_1 + '*' + username_2
        else: 
            id=username_2 + '*' + username_1

        self.save()