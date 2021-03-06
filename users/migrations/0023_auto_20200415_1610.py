# Generated by Django 2.2.12 on 2020-04-15 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20200415_1016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tools',
            options={'verbose_name': 'Конфиг: выплаты, константы, параметры'},
        ),
        migrations.AddField(
            model_name='tools',
            name='members_limit',
            field=models.PositiveIntegerField(default=1000, verbose_name='Число участников, при котором можно считать чат "большим"'),
        ),
    ]
