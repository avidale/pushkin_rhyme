

class BaseDialogManager:
    def respond(self, user_object, message_text):
        raise NotImplementedError()
        return updated_user_object, response, suggests

class StupidDialogManager(BaseDialogManager):
    def respond(self, user_object, message_text):
        response = "Вы сказали, '{}'".format(message_text.lower())
        suggests = []
        updated_user_object = user_object
        return updated_user_object, response, suggests
