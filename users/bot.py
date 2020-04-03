import datetime
import telebot
from telebot import types

import mintersdk
from mintersdk.minterapi import MinterAPI
from mintersdk.sdk.wallet import MinterWallet
from mintersdk.sdk.transactions import MinterTx, MinterSendCoinTx, MinterBuyCoinTx


import requests

from .dice import DiceBot
from .models import *
from dice_time.settings import API_TOKEN, ORIGIN
import re

import time

from .texts import *
from .markups import *

from django.conf import settings


bot = DiceBot(API_TOKEN)
botInfo = bot.get_me()

API = MinterAPI(settings.NODE_API_URL, **settings.TIMEOUTS)


def send(wallet_from, wallet_to, coin, value, gas_coin='BIP', payload=''):
    nonce = API.get_nonce(wallet_from['address'])
    send_tx = MinterSendCoinTx(
        coin,
        wallet_to,
        value,
        nonce=nonce,
        gas_coin=gas_coin,
        payload=payload)
    send_tx.sign(wallet_from['private_key'])
    r = API.send_transaction(send_tx.signed_tx)
    print(f'Send TX response:\n{r}')
    return send_tx


def send_cash(user, value):
    wallet_from = MinterWallet.objects.create(
        mnemonic=Tools.objects.get(pk=1).join)
    wallet_to = MinterWallets.objects.get(user=user).number
    coin = str(Tools.objects.get(pk=1).coin)
    payload = str(Tools.objects.get(pk=1).payload)
    send(
        wallet_from=wallet_from,
        wallet_to=wallet_to,
        coin=coin,
        value=value,
        gas_coin='BIP',
        payload=payload)


def send_message(message, text, markup):
    bot.send_message(
        message.chat.id,
        text=text,
        parse_mode='markdown',
        reply_markup=markup
    )


def check_event(user, event_id, message):
    print(start_winner_text)
    if DiceEvent.objects.filter(pk=event_id).exists():
        event = DiceEvent.objects.get(pk=event_id)
        if event.user == user:

            wallet = MinterWallets.objects.get(user=user)
            bot.send_message(
                message.chat.id,
                start_winner_text.format(
                    user_name=user.first_name,
                    user_wallet_address=wallet.number,
                    user_seed_phrase=wallet.mnemonic),
                parse_mode='markdown')
        else:
            send_message(message, start_no_winner_text, HOME_MARKUP)


def wallet_balance(wallet):
    URL_wallet = f'https://explorer-api.minter.network/api/v1/addresses/' + \
        str(wallet.number)
    r_wallet = requests.get(URL_wallet)
    balances = r_wallet.json()['data']['balances']
    amount = 0
    for b in balances:
        if str(b['coin']) == 'TIME':
            amount = float(b['amount'])
    return amount

# регистрация юзера


def register(message):
    user = User.objects.create(
        id=message.from_user.id,
        is_bot=message.from_user.is_bot,
        last_name=message.from_user.last_name,
        first_name=message.from_user.first_name,
        username=message.from_user.username
    )
    if not MinterWallets.objects.filter(user=user).exists():
        wallet = MinterWallet.create()
        wal=MinterWallets.objects.create(user=user,number=wallet['address'],mnemonic=wallet['mnemonic'])

    return user


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def command_start(message):
    print("start")
    referal_id = int(message.text[12:] or -1)
    print(message.text)
    print(referal_id)
    # Если пользователь уже зарегистрирован

    if User.objects.filter(pk=message.chat.id).exists():
        user = User.objects.get(pk=message.chat.id)
        if referal_id > -1:
            check_event(user, referal_id, message)
        else:
            send_message(message, hello_text, HOME_MARKUP)

    # Иначе регистрируем пользователя
    else:

        user = register(message)
        # Включить, когда будет мультиязичность
        # send_message(message,choose_language_text,language_markup)

        send_message(message, hello_text, HOME_MARKUP)

    if not MinterWallets.objects.filter(user=user).exists():
        wallet = MinterWallet.create()
        wal=MinterWallets.objects.create(user=user,number=wallet['address'],mnemonic=wallet['mnemonic'])

# Обработка кнопки ⚠️ Правила
@bot.message_handler(func=lambda message: message.text == '⚠️ Правила')
def rooles(message):
    user = User.objects.get(pk=message.chat.id)
    send_message(
        message,
        rooles_text.format(
            user_name=user.first_name,
            coin_ticker=str(
                Tools.objects.get(
                    pk=1).coin)),
        None)


# Обработка кнопки 💰 Мой Кошелёк
@bot.message_handler(func=lambda message: message.text == '💰 Мой Кошелёк')
def my_wallet(message):
    user = User.objects.get(pk=message.chat.id)
    wallet = MinterWallets.objects.get(user=user)
    amount = wallet_balance(wallet)
    send_message(
        message,
        my_wallet_text.format(
            user_wallet_address=wallet.number,
            user_seed_phrase=wallet.mnemonic, amount=amount), None)


# Расчет формулы и проверка на выигрыш в данном чате сегодня
def formula_calculation(user, number, chat_id):
    print('dice', number)
    date = datetime.date.today()
    summa = 0
    if number > 3 and not DiceEvent.objects.filter(
            chat_id=chat_id,
            date__date=date,
            is_win=True).exists() and not Exceptions.objects.filter(
            user=user).exists():
        # сумма выигрыша
        summa = number - 3  # формула подсчета выигрыша
    return summa



def reply_to(message, text, markup):
    mes = bot.reply_to(message=message, text=text, reply_markup=markup)
    return mes

# Обработчик всех остальных сообщений ( в группе отлавливаем триггеры)
@bot.message_handler(func=lambda message: message.chat.type != 'private')
def handle_messages(message):

    text = str(message.text)

    for trigger in Triggers.objects.all():
        if text.find(trigger.name) > -1:

            # Письмо, к-ое отправляется ботом ( кидаем кубик )
            dice_msg = bot.send_dice(message.chat.id, disable_notification=True, reply_to_message_id=message.message_id)
            #mes = reply_to(message, text_answer, None)

            if User.objects.filter(pk=message.from_user.id).exists():
                user = User.objects.get(pk=message.from_user.id)
            else:
                user = register(message)
            event = DiceEvent.objects.create(
                user=user,
                chat_id=int(
                    message.chat.id),
                title_chat=message.chat.title,
                link_chat=message.chat.username)
            
            summa = formula_calculation(user, dice_msg.dice_value, int(message.chat.id))
            print(summa)
            if summa > 0:
                url = 'https://telegram.me/commentsTGbot?start=event' + \
                    str(event.id)
                take_money_markup = types.InlineKeyboardMarkup(row_width=1)
                take_money_markup.add(
                    types.InlineKeyboardButton(
                        '😎 Забрать монеты', url=url))
                event.summa = summa
                event.is_win = True
                event.save()
                reply_to(dice_msg, text_winner.format(X=summa, coin_ticker=str(
                    Tools.objects.get(
                        pk=1).coin)), take_money_markup)
            break
