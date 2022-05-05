from bot.message import *
from bot.valid.validator import *

class DefaultValidator(object):

    @staticmethod
    def creator(message : Message) -> Validator:
        """ Return an object representing validator for developers of the bot. """
        validator = Validator()
        validator.set_data(message).add_user(680605398549528613)
        return validator

    def role(self, message : Message, role : int) -> Validator:
        """ Return an object representing validator for given role """
        validator = Validator()
        validator.set_roles(message.message.author.roles)
        validator.add(role)
        return validator
