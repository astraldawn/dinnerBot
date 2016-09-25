def get_info(update):
    user = update.message.from_user
    user_name = user.first_name + ' ' + user.last_name
    group = update.message.chat_id
    user_id = user.id
    return user_name.strip(), user_id, group
