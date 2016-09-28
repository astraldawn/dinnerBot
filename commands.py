from config import API_URL
import requests
import sys
import datetime
import utils
import errors


def welcome(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def info(bot, update):
    user_name, user_id, group = utils.get_info(update)
    bot.sendMessage(group, text=user_name + ' ' + user_id)


# Register group (should automate this though)
def register_group(bot, update):
    user_name, user_id, group = utils.get_info(update)

    # Server request
    data = {
        'group': group
    }
    r = requests.post(API_URL + 'register_group', json=data)

    # Response handling
    if r.status_code == 200:
        bot.sendMessage(group, text='Group registered')
    else:
        bot.sendMessage(group, text='Group already registered / registration failed')


# Registration command
def register(bot, update):
    user_name, user_id, group = utils.get_info(update)

    # Server request
    data = {
        'id': user_id,
        'username': user_name,
        'groupID': group
    }
    r = requests.post(API_URL + 'register', json=data)

    print(r.text)

    # Response handling
    if r.status_code == 200:
        bot.sendMessage(group, text=user_name + ': Successful registration')
    else:
        bot.sendMessage(group, text=user_name + ': Registration failed / already registered')


# Start meal
def start_meal(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    # TODO: Check the number of args
    meal_type = args[0].strip()

    # Request
    data = {
        'group': group,
        'meal_type': meal_type
    }
    r = requests.post(API_URL + 'add_meal', json=data)

    # Response handling
    if r.status_code == 200:
        bot.sendMessage(group, text='Who is eating ' + meal_type + '?')
    else:
        bot.sendMessage(group, text='Another meal is running / unable to start meal')


# End meal
def end_meal(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    # Request
    data = {
        'group': group
    }
    r = requests.post(API_URL + 'end_meal', json=data)

    # Response handling
    # Do not end the meal immediately, should trigger some handlers for warnings
    # E.g. 15min / 10min
    if r.status_code == 200:
        bot.sendMessage(group, text='Meal ended')
    else:
        bot.sendMessage(group, text='Unable to end meal')


def meal_participation(bot, update, args, cooked):
    user_name, user_id, group = utils.get_info(update)

    # Argument handling
    portion = 1
    if len(args) == 1:
        # TODO: Check arg value
        portion = int(args[0])
    else:
        utils.throw_error(bot, group, errors.WRONG_N_ARGS)
        return

    portion_text = str(portion) + (' portion' if portion == 1 else ' portions')

    # Request
    data = {
        'user_id': user_id,
        'group': group,
        'portions': portion,
        'cooked': cooked
    }
    r = requests.post(API_URL + 'eating', json=data)

    if r.status_code == 200:
        if portion == 0:
            bot.sendMessage(group, text=user_name + ' removed from meal')
        elif cooked:
            bot.sendMessage(group, text='Thanks for cooking, ' + user_name + '! You are eating ' + portion_text)
        else:
            bot.sendMessage(group, text=user_name + ' eating ' + portion_text)
    else:
        bot.sendMessage(group, text='Unable to update, is a meal started?')


# Eating
def eating(bot, update, args):
    meal_participation(bot, update, args, cooked=False)


# Cooking
def cooking(bot, update, args):
    meal_participation(bot, update, args, cooked=True)


# Return information for currently running meal
def meal_info(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    # Argument handling
    meal_id = -1
    if len(args) == 1:
        meal_id = args[0]

    # Request
    data = {
        'group': group,
        'meal_id': meal_id
    }
    r = requests.post(API_URL + 'meal_info', json=data)

    if r.status_code == 200:
        meal_participations = r.json()
        output = ''
        total_portions = 0
        if len(meal_participations) == 0:
            bot.sendMessage(group, 'No information to display')
            return

        for mp in meal_participations:
            output += str(mp['user_name']) + ' '
            output += str(mp['portions']) + (' portion' if mp['portions'] == 1 else ' portions')
            output += ' - cooking' if mp['cooked'] else ''
            output += '\n'
            total_portions += mp['portions']
        output += str(total_portions) + (' portion' if total_portions == 1 else ' portions') + ' required'
        bot.sendMessage(group, text=output)
    else:
        bot.sendMessage(group, text='Unable to retrieve meal information')


# Return the last n meals
def get_meals(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    # Argument handling
    number = 5
    if len(args) > 0:
        number = args[0]

    data = {
        'group': group,
        'number': number
    }
    r = requests.post(API_URL + 'meals', json=data)

    if r.status_code == 200:
        meals = r.json()
        output = ''
        if len(meals) == 0:
            bot.sendMessage(group, 'No information to display')
            return

        for meal in meals:
            output += 'ID: ' + str(meal[0]) + '     '
            output += 'Portions: ' + str(meal[1])
            output += '\n'
        output += str(len(meals)) + ' meals retrieved'
        bot.sendMessage(group, text=output)
    else:
        bot.sendMessage(group, text='Unable to retrieve information')


# Tally the last n users
def tally_group(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    data = {
        'group': group,
        'set_date': False if len(args) == 0 else True
    }
    r = requests.post(API_URL + 'tally_group', json=data)

    if r.status_code == 200:
        users = r.json()
        output = ''
        total = 0
        most_social = ''
        least_portions = sys.maxsize
        if len(users) == 0:
            bot.sendMessage(group, 'No information to display')
            return

        for user, portions in users.items():
            output += user + ' - ' + str(portions) + '\n'
            total += portions
            if portions < least_portions:
                # Need to handle the case where multiple people tie
                most_social = user
                least_portions = portions
        output += str(total) + ' portions consumed\n'
        output += most_social + ' has the most life'

        bot.sendMessage(group, text=output)
    else:
        bot.sendMessage(group, text='Unable to retrieve information')


# Tally information for the user
def tally_user(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    data = {
        'group': group,
        'user_id': user_id
    }
    r = requests.post(API_URL + 'tally_user', json=data)

    if r.status_code == 200:
        output = ''
        meals = r.json()
        print(meals)

        for meal in meals:
            output += meal['type'] + ' ' + meal['date'] + '\n'
        output += 'Involved in ' + str(len(meals)) + ' meals'
        bot.sendMessage(group, text=output)
    else:
        bot.sendMessage(group, text='Unable to retrieve information')


# Meal modification routes
def modify_cooking(bot, update, args, cooking):
    user_name, user_id, group = utils.get_info(update)

    meal_id = None
    if len(args) == 1:
        meal_id = int(args[0])
    else:
        utils.throw_error(bot, group, errors.WRONG_N_ARGS)
        return

    data = {
        'user_id': user_id,
        'meal_id': meal_id
    }

    if cooking:
        r = requests.post(API_URL + 'add_chef', json=data)
    else:
        r = requests.post(API_URL + 'remove_chef', json=data)

    if r.status_code == 200:
        bot.sendMessage(group, text='Update successful')
    else:
        bot.sendMessage(group, text='Update unsuccessful')


def add_chef(bot, update, args):
    modify_cooking(bot, update, args, cooking=True)


def remove_chef(bot, update, args):
    modify_cooking(bot, update, args, cooking=False)


# Change number of portions
def change_portions(bot, update, args):
    user_name, user_id, group = utils.get_info(update)

    meal_id = None
    portions = None

    if len(args) == 2:
        meal_id = int(args[0])
        portions = int(args[1])
    else:
        utils.throw_error(bot, group, errors.WRONG_N_ARGS)
        return

    data = {
        'user_id': user_id,
        'meal_id': meal_id,
        'portions': portions
    }

    r = requests.post(API_URL + 'change_portions', json=data)

    if r.status_code == 200:
        bot.sendMessage(group, text='Update successful')
    else:
        bot.sendMessage(group, text='Update unsuccessful')
