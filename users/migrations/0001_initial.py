# Generated by Django 2.1.7 on 2020-04-02 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiceEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата появления в боте')),
                ('chat_id', models.IntegerField(default=1, verbose_name='Id-чата совершенного event-a')),
                ('summa', models.PositiveIntegerField(default=0, verbose_name='Cумма выигрыша')),
                ('is_win', models.BooleanField(default=False, verbose_name='Выиграл?')),
            ],
            options={
                'verbose_name': 'События',
                'verbose_name_plural': 'События',
            },
        ),
        migrations.CreateModel(
            name='Exceptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Бан-лист',
                'verbose_name_plural': 'Бан-лист',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название языка')),
            ],
            options={
                'verbose_name': 'Языки',
                'verbose_name_plural': 'Языки',
            },
        ),
        migrations.CreateModel(
            name='MinterWallets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=85, null=True, verbose_name='Номер кошелька')),
                ('mnemonic', models.TextField(verbose_name='Сид фраза кошелька')),
            ],
            options={
                'verbose_name': 'М-Кошельки пользователей',
                'verbose_name_plural': 'М-Кошельки пользователей',
            },
        ),
        migrations.CreateModel(
            name='Texts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_ru', models.TextField(verbose_name='Текст сообщения')),
                ('text_eng', models.TextField(verbose_name='Текст сообщения eng')),
            ],
            options={
                'verbose_name': 'Текста',
                'verbose_name_plural': 'Текста в боте',
            },
        ),
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join', models.TextField(verbose_name='Seed-фраза')),
                ('payload', models.CharField(default='-', max_length=80, verbose_name='Payload при выводе средств из бота')),
                ('main_value', models.IntegerField(default=3, verbose_name='Число для расчета в формуле выплат')),
                ('coin', models.CharField(default='-', max_length=10, verbose_name='Монета,в к-ой идет выплата')),
            ],
            options={
                'verbose_name': 'Настройки выплат',
                'verbose_name_plural': 'Настройки выплат',
            },
        ),
        migrations.CreateModel(
            name='Triggers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название метки')),
            ],
            options={
                'verbose_name': 'Триггеры',
                'verbose_name_plural': 'Триггеры',
            },
        ),
        migrations.CreateModel(
            name='Unbond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('summa', models.FloatField(default=0.0, verbose_name='Cумма вывода')),
                ('to_wallet', models.CharField(blank=True, max_length=85, null=True, verbose_name='Номер кошелька, куда вывели')),
                ('from_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.MinterWallets', verbose_name='Кошелек с к-ого выведено')),
            ],
            options={
                'verbose_name': 'Обналичивание выигрышей',
                'verbose_name_plural': 'Обналичивание выигрышей',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID в Телеграм')),
                ('is_bot', models.BooleanField(default=False, verbose_name='Статус бота')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('username', models.CharField(blank=True, max_length=60, null=True, verbose_name='Никнейм пользователя')),
                ('date_reg', models.DateField(auto_now_add=True, verbose_name='Дата появления в боте')),
                ('language', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Language', verbose_name='Язык')),
            ],
            options={
                'verbose_name': 'Пользователь Telegram',
                'verbose_name_plural': 'Пользователи Telegram',
            },
        ),
        migrations.AddField(
            model_name='unbond',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='ТГ пользователь'),
        ),
        migrations.AddField(
            model_name='minterwallets',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='Владелец кошелька'),
        ),
        migrations.AddField(
            model_name='exceptions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='Пользователь ТГ'),
        ),
        migrations.AddField(
            model_name='diceevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='Пользователь ТГ'),
        ),
    ]
