import copy
import random

import telebot as tb
import api_handler as api
import keyboards as kb

from config import TOKEN
from constants import WELCOME_MESSAGE, ERROR_MESSAGE
import constants as const

bot = tb.TeleBot(TOKEN)

artist_set: set = set()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    if not api.user_registered(cid):
        bot.reply_to(message, WELCOME_MESSAGE)
        markup = tb.types.ForceReply(selective=False)
        msg = bot.send_message(cid, "Введи своё имя или '.' если хочешь взять ник", reply_markup=markup)
        bot.register_next_step_handler(msg, get_username)
        return
    if cid not in artist_set and api.is_artist(cid):
        artist_set.add(cid)
    bot.reply_to(message, WELCOME_MESSAGE, reply_markup=kb.get_main_menu(cid in artist_set))


def get_username(message):
    cid = message.chat.id
    if message.content_type == "text":
        text = message.text
        if text == '.':
            text = message.from_user.username
        status_code = api.add_new_user(cid, text)
        if status_code != 201:
            bot.send_message(cid, ERROR_MESSAGE)
        else:
            bot.send_message(cid, f"Здравствуй, {text}")
        api.make_artist(cid)
    else:
        markup = tb.types.ForceReply(selective=False)
        msg = bot.send_message(cid, "Введи своё имя или '.' если хочешь взять ник", reply_markup=markup)
        bot.register_next_step_handler(msg, get_username)


@bot.message_handler(regexp=const.ARTIST_MENU)
def check_access():
    pass


print('Started')
bot.polling()
