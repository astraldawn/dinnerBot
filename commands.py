from config import API_URL
import requests
import json


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def info(bot, update):
    user = update.message.from_user
    user_name = user.first_name + ' ' + user.last_name
    user_id = str(user.id)
    bot.sendMessage(update.message.chat_id, text=user_name + ' ' + user_id)


# Registration command
def register(bot, update):
    user = update.message.from_user
    user_name = user.first_name + ' ' + user.last_name
    user_id = str(user.id)
    data = {
        'id': user_id,
        'username': user_name
    }
    r = requests.post(API_URL + 'register', json=data)

    response = r.json()

    if response['result'] == 'success':
        bot.sendMessage(update.message.chat_id, text='Successful registration')
    else:
        bot.sendMessage(update.message.chat_id, text='Registration failed / already registered')
