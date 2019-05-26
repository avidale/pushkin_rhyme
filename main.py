import argparse
import telebot
import os
import logging
from tgalice.dialog_connector import DialogConnector
from tgalice.session_storage import BaseStorage
from dialog_manager import StupidDialogManager
from flask import Flask, request
import json

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ.get('TOKEN', 'no_token_is_avaliable')
bot = telebot.TeleBot(TOKEN)
connector = DialogConnector(StupidDialogManager(), storage=BaseStorage())
app = Flask(__name__)


TELEBOT_URL = 'telebot_webhook/'
BASE_URL = 'https://pushkin-rhyme.herokuapp.com/'


@app.route("/alice/", methods=['POST'])
def alice_response():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Alice request: %r', request.json)
    response = connector.respond(request.json, source='alice')
    logging.info('Alice response: %r', response)
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = connector.respond(message, source='telegram')
    # log_message(message, response)
    print('message was "{}"'.format(message.text))
    bot.reply_to(message, **response)


@app.route('/' + TELEBOT_URL + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/" + TELEBOT_URL)
def telegram_web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + TOKEN)
    return "!", 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the bot')
    parser.add_argument('--poll', action='store_true')
    args = parser.parse_args()
    if args.poll:
        bot.polling()
    else:
        telegram_web_hook()
        app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
