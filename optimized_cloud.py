import time
#t = time.time()
import threading

TEXT_HELP = (
    'Вы находитесь в навыке "Рифмы Пушкина". На любую вашу фразу я отвечаю строчкой из его поэзии. '
    'Когда вам надоест, скажите "довольно" или "Алиса, хватит".'
)


def fast_handler(event, context):
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': TEXT_HELP,
            'end_session': 'false',
            'buttons': [{'title': 'хватит'}]
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

#print('time to load threader is', time.time() - t)
