


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
        updated_user_object, response_text, suggests = self.dialog_manager.respond(user_object, message_text)
        if updated_user_object != user_object:
            self.set_user_object(user_id, updated_user_object)
        response = self.standardize_output(source, response_text, suggests)
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
            raise NotImplementedError()
        else:
            raise ValueError('Source must be on of {"telegram", "alice"}')
        return user_id, message_text
    def standardize_output(self, source, response_text, suggests=None):
        if suggests is not None and len(suggests) > 0:
            raise NotImplementedError()
        if source == 'telegram':
            return response_text
        elif source == 'alice':
            raise NotImplementedError()
        else:
            raise ValueError('Source must be on of {"telegram", "alice"}')
