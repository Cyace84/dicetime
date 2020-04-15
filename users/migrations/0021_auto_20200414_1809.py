# Generated by Django 2.1.7 on 2020-04-14 18:09

import datetime
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20200414_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default=None, max_length=42, null=True, verbose_name='Адрес (Mx...)')),
                ('mnemonic', encrypted_model_fields.fields.EncryptedTextField(default='', verbose_name='Сид фраза')),
                ('balance', models.DecimalField(decimal_places=6, default=Decimal('0'), max_digits=24, verbose_name='Баланс')),
                ('balance_updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление баланса')),
            ],
            options={
                'verbose_name': 'Кошелек чата',
                'verbose_name_plural': 'Кошельки чатов',
            },
        ),
        migrations.AddField(
            model_name='allowedchat',
            name='chat_limit_day',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24, verbose_name='Лимит таймов на чат, в день'),
        ),
        migrations.AddField(
            model_name='allowedchat',
            name='dice_time_from',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Dice Time (from)'),
        ),
        migrations.AddField(
            model_name='allowedchat',
            name='dice_time_to',
            field=models.TimeField(default=datetime.time(23, 59), verbose_name='Dice Time (to)'),
        ),
        migrations.AddField(
            model_name='allowedchat',
            name='user_limit_day',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=24, verbose_name='Лимит таймов на одного юзера, в день'),
        ),
        migrations.AddField(
            model_name='chatwallet',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.AllowedChat', verbose_name='Чат'),
        ),
    ]