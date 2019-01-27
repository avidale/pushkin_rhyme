import telebot
import pickle
import os
from datetime import datetime

CONN = None

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)


def log_message(message, response):
    global CONN
    if CONN is None or CONN.closed:
        try:
            CONN = psycopg2.connect(os.environ['DATABASE_URL'])
        except OperationalError:
            return
    cur = CONN.cursor()
    query = "INSERT INTO dialog VALUES('{}', '{}', '{}', '{}', TIMESTAMP '{}')".format(
        message.chat.id, 
        message.chat.username, 
        message.text, 
        response, 
        datetime.now()
    )
    cur.execute(query)
    CONN.commit()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Я глупенький болтательный чатбот Матчасти. О моём создании ты можешь прочитать в канале t.me/matchast или группе vk.com/mat.chast.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = "Вы сказали, '{}'".format(message.text.lower())
    # log_message(message, response)
    print('message was "{}"'.format(message.text))
    bot.reply_to(message, response)

if __name__ == '__main__':
    print('start work')
    bot.polling()
