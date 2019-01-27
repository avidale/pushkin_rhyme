import telebot
import pickle
import os
from datetime import datetime
import logging
from dialog_connector import DialogConnector
from dialog_manager import StupidDialogManager
from flask import Flask, request
import json

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)
connector = DialogConnector(StupidDialogManager())
app = Flask(__name__)


@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Alice request: %r', request.json)
    response = connector.respond(request.json, source='alice')
    logging.info('Alice response: %r', response)
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я глупенький болтательный чатбот Матчасти. О моём создании ты можешь прочитать в канале t.me/matchast или группе vk.com/mat.chast.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = connector.respond(message, source='telegram')
    # log_message(message, response)
    print('message was "{}"'.format(message.text))
    bot.reply_to(message, response)


if __name__ == '__main__':
    print('start work')
    bot.polling()
