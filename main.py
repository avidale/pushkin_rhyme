import telebot
import pickle
import os
from datetime import datetime
from dialog_connector import DialogConnector
from dialog_manager import StupidDialogManager

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)
connector = DialogConnector(StupidDialogManager())

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Я глупенький болтательный чатбот Матчасти. О моём создании ты можешь прочитать в канале t.me/matchast или группе vk.com/mat.chast.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = connector.respond(message)
    # log_message(message, response)
    print('message was "{}"'.format(message.text))
    bot.reply_to(message, response)

if __name__ == '__main__':
    print('start work')
    bot.polling()
