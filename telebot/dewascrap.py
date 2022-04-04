import telebot


bot = telebot.TeleBot('5122715306:AAHCMOnUNAAgbBYHZdcpSLLPvTdNGhO7sR0')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, 'Hi, welcome to dewa scrap.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()

