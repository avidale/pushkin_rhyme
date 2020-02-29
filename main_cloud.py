import os
import tgalice

from dialog_manager import StupidDialogManager

if __name__ == '__main__':
    # local run or server-ful deploy
    TOKEN = os.environ.get('TOKEN', 'no_token_is_avaliable')
    BASE_URL = 'https://pushkin-rhyme.herokuapp.com/'
    connector = tgalice.dialog_connector.DialogConnector(
        dialog_manager=StupidDialogManager(),
        storage=tgalice.session_storage.BaseStorage()
    )
    server = tgalice.flask_server.FlaskServer(connector=connector, base_url=BASE_URL)
    server.parse_args_and_run()
else:
    # serverless deploy
    connector = tgalice.dialog_connector.DialogConnector(
        dialog_manager=StupidDialogManager(),
        storage=tgalice.session_storage.BaseStorage()
    )
    alice_handler = connector.serverless_alice_handler
