import pickle
import copy
from tgalice.dialog_manager import BaseDialogManager
from tgalice import basic_nlu

from pushkin.rhyme import Rhymer

with open('pushkin/pushkin.pkl', 'rb') as f:
    dicts = pickle.load(f)
rhymer = Rhymer(*dicts)

TEXT_HELP = (
    'Вы находитесь в навыке "Рифмы Пушкина". На любую вашу фразу я отвечаю строчкой из его поэзии. '
    'Когда вам надоест, скажите "довольно" или "Алиса, хватит".'
)
TEXT_FAREWELL = 'Всего доброго! Если захотите повторить, скажите "Алиса, включи навык Рифмы Пушкина".'

COMMAND_EXIT = 'exit'


class StupidDialogManager(BaseDialogManager):
    def respond(self, user_object, message_text):
        suggests = ['довольно']
        updated_user_object = copy.deepcopy(user_object)
        commands = []
        text = basic_nlu.fast_normalize(message_text)
        if not text or basic_nlu.like_help(text) or not updated_user_object:
            response = TEXT_HELP
        elif text == 'довольно' or basic_nlu.like_exit(text):
            response = TEXT_FAREWELL
            commands.append(COMMAND_EXIT)
        else:
            response = rhymer.random_rhyme(text)
        updated_user_object['last_dialog'] = [text, response]
        return updated_user_object, response, suggests, commands
