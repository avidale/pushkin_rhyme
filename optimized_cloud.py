import time
# t = time.time()
import threading
import random

TEXT_HELP = (
    'Вы находитесь в навыке "Рифмы Пушкина". На любую вашу фразу я отвечаю строчкой из его поэзии. '
    'Когда вам надоест, скажите "довольно" или "Алиса, хватит". '
    'Возможно, первые несколько секунд я буду загружать базы стихов, зато потом как заговорю!'
)
TEXTS_WAIT = [
    'Пожалуйста, подождите немножко. Я загружаю базы данных. После этого смогу нормально отвечать.',
    'Пожалуйста, подождите. Мне нужно полминутки на загрузку. После этого я заговорю стихами.',
    'Пожалуйста, повремените полминутки. Я перечитываю поэзию. Скоро начну отвечать ей.',
    'Мне нужно несколько секунд для загрузки базы стихов. Пожалуйста, подождите.',
    'Погодите минуточку, сейчас перечитаю стихотворение и поговорю с вами.',
    'Одну секунду, мне надо перечитать одну поэму. Потом я заговорю цитатами.',
]


def fast_handler(event, context):
    input_text = (event.get('request', {}).get('command', '') or '').lower().strip()
    if event.get('session', {}).get('new'):
        text = TEXT_HELP
    elif 'помощь' in input_text or 'что ты умеешь' in input_text or 'что ты можешь' in input_text:
        text = TEXT_HELP
    else:
        text = random.choice(TEXTS_WAIT)
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false',
            'buttons': [{'title': 'хватит', 'hide': 'true'}]
        }
    }


def create_slow_handler():
    import tgalice
    from dialog_manager import StupidDialogManager
    dm = StupidDialogManager()
    connector = tgalice.dialog_connector.DialogConnector(
        dialog_manager=dm,
        storage=tgalice.session_storage.BaseStorage()
    )
    return connector.serverless_alice_handler


class ThreadingResponder(object):
    """ This callable is created very quickly, but after some slow process it changes behavior. """
    def __init__(self, first_responder, second_responder_maker):
        self.responder = first_responder
        self.second_responder_maker = second_responder_maker
        thread = threading.Thread(target=self.replace_responder, args=())
        thread.start()

    def replace_responder(self):
        self.responder = self.second_responder_maker()

    def __call__(self, alice_request, context):
        return self.responder(alice_request, context)


alice_handler = ThreadingResponder(fast_handler, create_slow_handler)

# print('time to load threader is', time.time() - t)
