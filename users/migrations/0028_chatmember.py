# Generated by Django 2.2.12 on 2020-04-27 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_auto_20200425_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateTimeField(default=None, null=True, verbose_name='Дата добавления в чат')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.AllowedChat', verbose_name='Чат')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='Чатланин')),
            ],
            options={
                'unique_together': {('chat', 'user')},
            },
        ),
    ]
