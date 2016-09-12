# !/usr/bin/env python
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def info(bot, update):
    user = update.message.from_user
    user_name = user.first_name + ' ' + user.last_name
    user_id = str(user.id)
    bot.sendMessage(update.message.chat_id, text=user_name + ' ' + user_id)
