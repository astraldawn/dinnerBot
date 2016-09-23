# !/usr/bin/env python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import commands
from config import TELEGRAM_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# def echo(bot, update):
#     bot.sendMessage(update.message.chat_id, text='message received')
#     # bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("welcome", commands.welcome))
    dp.add_handler(CommandHandler("help", commands.help))
    dp.add_handler(CommandHandler("info", commands.info))

    # User registration
    dp.add_handler(CommandHandler("register", commands.register))
    dp.add_handler(CommandHandler("register_group", commands.register_group))
    dp.add_handler(CommandHandler("tally", commands.tally_user, pass_args=True))
    dp.add_handler(CommandHandler("tally_group", commands.tally_group, pass_args=True))

    # Meal related
    dp.add_handler(CommandHandler("start", commands.start_meal, pass_args=True))
    dp.add_handler(CommandHandler("end", commands.end_meal, pass_args=True))
    dp.add_handler(CommandHandler("eating", commands.eating, pass_args=True))
    dp.add_handler(CommandHandler("cooking", commands.cooking, pass_args=True))
    dp.add_handler(CommandHandler("meal_info", commands.meal_info, pass_args=True))
    dp.add_handler(CommandHandler("get_meals", commands.get_meals, pass_args=True))

    # # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
