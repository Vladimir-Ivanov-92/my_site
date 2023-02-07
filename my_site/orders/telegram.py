# !/usr/bin/python

import telebot

from my_site import settings

bot = telebot.TeleBot(settings.TG_BOT_TOKEN, parse_mode=None)


def send_message_about_order_in_telegram(message):
    bot.send_message(settings.TG_ID, message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
