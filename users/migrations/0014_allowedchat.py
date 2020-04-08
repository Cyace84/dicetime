# Generated by Django 2.1.7 on 2020-04-08 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20200407_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(verbose_name='Chat ID')),
                ('title_chat', models.CharField(blank=True, max_length=40, null=True, verbose_name='Имя чата')),
                ('link_chat', models.CharField(blank=True, max_length=40, null=True, verbose_name='Линк на чат')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата первого сообщения')),
                ('activated_at', models.DateTimeField(default=None, null=True, verbose_name='Дата активации')),
            ],
        ),
    ]
