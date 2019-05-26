import os
import logging
from tgalice.dialog_connector import DialogConnector
from tgalice.session_storage import BaseStorage
from dialog_manager import StupidDialogManager
from flask import Flask, request
import json

logging.basicConfig(level=logging.DEBUG)

connector = DialogConnector(StupidDialogManager(), storage=BaseStorage())
app = Flask(__name__)


@app.route("/pushkin-rhyme/", methods=['POST'])
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
