from config import API_URL
import requests
import json


def welcome(bot, update):
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
    data = {
        'id': user.id,
        'username': user_name
    }
    r = requests.post(API_URL + 'register', json=data)

    response = r.json()

    group = update.message.chat_id
    if response['result'] == 'success':
        bot.sendMessage(group, text=user_name + ': Successful registration')
    else:
        bot.sendMessage(group, text=user_name + ': Registration failed / already registered')


# Start meal
def start_meal(bot, update, args):
    group = update.message.chat_id
    user = update.message.from_user
    user_name = user.first_name + ' ' + user.last_name

    # TODO: Check the number of args
    meal_type = args[0]

    # Server verification that current group does not have a running meal

    bot.sendMessage(group, text='start ' + meal_type)


# End meal
def end_meal(bot, update, args):
    group = update.message.chat_id

    # Server verification that group has a running meal

    # Do not end the meal immediately, should trigger some handlers for warnings
    # E.g. 15min / 10min
    bot.sendMessage(group, text='meal closed')


# Eating
def eating(bot, update, args):
    group = update.message.chat_id
    user = update.message.from_user
    user_name = user.first_name + ' ' + user.last_name

    portion = '1'

    if len(args) > 0:
        # TODO: Check arg value
        portion = args[0]

    portion_text = portion + (' portion' if portion == '1' else ' portions')

    bot.sendMessage(group, text=user_name + ' eating ' + portion_text)
