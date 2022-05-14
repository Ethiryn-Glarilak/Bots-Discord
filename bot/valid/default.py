from bot.composant.message import Message
from bot.valid.validator import Validator

class DefaultValidator(object):

    @staticmethod
    def creator(message : Message) -> Validator:
        """ Return an object representing validator for developers of the bot. """
        validator = Validator()
        validator.set_data(message).add_user(680605398549528613)
        return validator

    @staticmethod
    def channel(message : Message, channels : list[int]) -> Validator:
        """ Return an object representing validator for given channel """
        validator = Validator()
        validator.set_data(message)
        validator.add(*list(map(lambda channel : (channel, "c"), channels)))
        return validator

    @staticmethod
    def role(message : Message, roles : list[int]) -> Validator:
        """ Return an object representing validator for given role """
        validator = Validator()
        validator.set_data(message)
        validator.add(*list(map(lambda role : (role, "r"), roles)))
        return validator

    @staticmethod
    def server(message : Message, servers : list[int]) -> Validator:
        """ Return an object representing validator for given server """
        validator = Validator()
        validator.set_data(message)
        validator.add(*list(map(lambda server : (server, "s"), servers)))
        return validator

    @staticmethod
    def user(message : Message, users : list[int]) -> Validator:
        """ Return an object representing validator for given user """
        validator = Validator()
        validator.set_data(message)
        validator.add(*list(map(lambda user : (user, "s"), users)))
        return validator
