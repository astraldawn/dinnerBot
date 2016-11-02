from config import API_URL
import requests
import sys
import datetime
import utils
import errors


# check bathing
def check_bathing(bot, update, args):
    user_name, user_id, chat_id = utils.get_info(update)
    data = {"user_id": user_id}
    r = requests.post(API_URL + 'check_bathing', json=data)
    if r.status_code == 200:
        status = r.json()
        if status['bathing']:
            username, start_time = status['username'], status['start']
            output = "Oh no! You're unlucky. {} has been bathing since {}. ".format(username, start_time)
            bot.sendMessage(chat_id, text=output)
        else:
            bot.sendMessage(chat_id, text="You've hit the jackpot! No one is bathing now, as far as I know.")
    else:
        bot.sendMessage(chat_id, text='Unable to check. Are you sure you are registered with a group?')


def start_bathing(bot, update, args):
    user_name, user_id, chat_id = utils.get_info(update)
    data = {"user_id": user_id}
    r = requests.post(API_URL + 'start_bathing', json=data)
    if r.status_code == 200:
        message = "You have started bathing, {}. The bathroom is yours!".format(user_name)
        bot.sendMessage(chat_id, text=message)
    else:
        bot.sendMessage(chat_id, text="Oh no, something went wrong. Please try again later.")


def stop_bathing(bot, update, args):
    user_name, user_id, chat_id = utils.get_info(update)
    data = {"user_id": user_id}
    r = requests.post(API_URL + 'stop_bathing', json=data)
    if r.status_code == 200:
        response = r.json()
        if response['correct_person']:
            bot.sendMessage(chat_id, text="Thanks for telling me. Hope you had a good bath!")
        else:
            bot.sendMessage(chat_id, text="Sorry, you can't end a bathing session on behalf of someone else.")
    elif r.status_code == 400:
        bot.sendMessage(chat_id, text="Unable to process request. Are you sure you even started bathing?")
    else:
        bot.sendMessage(chat_id, text="Oh no, something went wrong. Please try again later.")
