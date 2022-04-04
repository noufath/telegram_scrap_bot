from asyncore import dispatcher
from turtle import update
from flask import Flask
from setuptools import Command
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (Updater, 
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import logging
from consts.settings import BOT_TOKEN


app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

global TOKEN

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation"""
    user = update.message.from_user
    update.message.reply_text(
        'Hi!, I\'m scraper bot, I will give you insight about the products sold at shopee.co.id. \n\n'
        'Send /cancel to stop talking to me.\n\n',
    )

    return user

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main():
    app = Flask(__name__)

    
    TOKEN = BOT_TOKEN

    # Create the updater
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    # start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receive SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully
    updater.idle()


if __name__ == '__main__':

    main()
    