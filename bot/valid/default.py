from bot.message import *
from bot.valid.validator import *

class DefaultValidator(object):

    def creator(self, message : Message):
        """ Return an object representing validator for developers of the bot. """
        validator = Validator()
        validator.set_data(message).add_user(680605398549528613)
        return validator

    def role(self, message : Message, role : int):
        """ Return an object representing validator for given role """
        validator = Validator()
        validator.set_role(map(lambda role : (role, "r"), message.message.author.roles))
        validator.add(role)
        return validator
