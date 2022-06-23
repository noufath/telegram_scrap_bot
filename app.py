import re
import requests
from flask import Flask
import telegram
import applogger
import os
from dotenv import load_dotenv


load_dotenv()

global TOKEN, bot, URL

# get env 
TOKEN = os.environ.get('BOT_TOKEN')
URL = os.environ.get('URL')

# Enable logging
logger = applogger.AppLoger('info_log')

bot = telegram.Bot(token=TOKEN)


app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(requests.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram undestands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    logger.info('Got text message : {}', format(text))

    if text == "/start":
        bot_welcome = """
            Welcome to ShopSeller bot, the bot scrapt item sold from shopee.co.id
            and then processing data for seller analytics.
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,  reply_to_message_id=msg_id)
    else:
        try:
            # Clear the message we got from any non alphabets
            text = re.sub(r"/W", "_", text)
             # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)