# Generated by Django 2.2.12 on 2020-05-14 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_user_conversation_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmember',
            name='downvotes',
            field=models.PositiveIntegerField(default=0, verbose_name='Отрицательные отклики'),
        ),
        migrations.AddField(
            model_name='chatmember',
            name='reply_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество полученных reply'),
        ),
        migrations.AddField(
            model_name='chatmember',
            name='upvotes',
            field=models.PositiveIntegerField(default=0, verbose_name='Положительные отклики'),
        ),
        migrations.AlterField(
            model_name='text',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Название сообщения'),
        ),
    ]