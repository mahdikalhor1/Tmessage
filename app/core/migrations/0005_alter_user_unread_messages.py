# Generated by Django 4.2.3 on 2023-11-14 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_message_user_unread_messages_privatechatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='unread_messages',
            field=models.ManyToManyField(to='core.privatechatmessage', verbose_name='unread messages'),
        ),
    ]
