import copy
import pickle
import tgalice

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


class StupidDialogManager(tgalice.dialog_manager.BaseDialogManager):
    def respond(self, ctx: tgalice.dialog_manager.Context):
        suggests = ['довольно']
        updated_user_object = copy.deepcopy(ctx.user_object)
        commands = []
        text = tgalice.basic_nlu.fast_normalize(ctx.message_text)
        if isinstance(ctx.raw_message, dict):
            new_session = ctx.raw_message.get('session', {}).get('new')
        else:
            new_session = False
        if not text or tgalice.basic_nlu.like_help(text) or new_session or text == 'start':
            response = TEXT_HELP
        elif text == 'довольно' or tgalice.basic_nlu.like_exit(text):
            response = TEXT_FAREWELL
            commands.append(COMMAND_EXIT)
        else:
            response = rhymer.random_rhyme(text)
        updated_user_object['last_dialog'] = [text, response]
        return tgalice.dialog_manager.Response(
            response, user_object=updated_user_object, suggests=suggests, commands=commands
        )
