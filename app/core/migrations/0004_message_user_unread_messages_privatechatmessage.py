# Generated by Django 4.2.3 on 2023-11-14 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        ('core', '0003_user_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='unread_messages',
            field=models.ManyToManyField(to='core.message', verbose_name='unread messages'),
        ),
        migrations.CreateModel(
            name='PrivateChatMessage',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.message')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.privatechat')),
            ],
            bases=('core.message',),
        ),
    ]
