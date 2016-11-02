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

