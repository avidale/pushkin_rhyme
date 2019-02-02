# coding: utf-8
from main import app

import logging
logging.basicConfig(level=logging.DEBUG)
logging.info('i am within wsgi.py and there is high pressure')

if __name__ == "__main__":
    app.run()

