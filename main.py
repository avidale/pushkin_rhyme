import os
import tgalice

from dialog_manager import StupidDialogManager

TOKEN = os.environ.get('TOKEN', 'no_token_is_avaliable')
BASE_URL = 'https://pushkin-rhyme.herokuapp.com/'

if __name__ == '__main__':
    connector = tgalice.dialog_connector.DialogConnector(
        dialog_manager=StupidDialogManager(),
        storage=tgalice.session_storage.BaseStorage()
    )
    server = tgalice.flask_server.FlaskServer(connector=connector, base_url=BASE_URL)
    server.parse_args_and_run()
