


class DialogConnector:
    """ This class provides unified interface for both Telegram and Alice applications """
    def __init__(self, dialog_manager, default_source='telegram'):
        self.dialog_manager = dialog_manager
        self.default_source = default_source

    def respond(self, message, source=None):
        # todo: support different triggers - not only messages, but calendar events as well
        if source is None:
            source = self.default_source
        user_id, message_text = self.standardize_input(source, message)
        user_object = self.get_user_object(user_id)
        updated_user_object, response_text, suggests, response_commands = self.dialog_manager.respond(user_object, message_text)
        # todo: execute response_commands
        if updated_user_object != user_object:
            self.set_user_object(user_id, updated_user_object)
        response = self.standardize_output(source, message, response_text, response_commands, suggests)
        return response

    def get_user_object(self, user_id):
        return {}

    def set_user_object(self, user_id, user_object):
        raise NotImplementedError()

    def standardize_input(self, source, message):
        if source == 'telegram':
            user_id = source + '__' + message.chat.username
            message_text = message.text
        elif source == 'alice':
            user_id = source + '__' + message['session']['user_id']
            message_text = message['request']['original_utterance']
        else:
            raise ValueError('Source must be on of {"telegram", "alice"}')
        return user_id, message_text

    def standardize_output(self, source, original_message, response_text, response_commands=None, suggests=None):
        if response_commands:
            raise NotImplementedError
        if suggests:
            raise NotImplementedError()
        if source == 'telegram':
            return response_text
        elif source == 'alice':
            response = {
                "version": original_message['version'],
                "session": original_message['session'],
                "response": {
                    # todo: handle end_session
                    "end_session": False,
                    "text": response_text
                }
            }
            if suggests:
                response['response']['buttons'] = [{'title': suggest, 'hide': True} for suggest in suggests]
            return response
        else:
            raise ValueError('Source must be on of {"telegram", "alice"}')
