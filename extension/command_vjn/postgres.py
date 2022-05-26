from extension.command_vjn.vjn_object import VJNObject

class PostgresCommandVJN:

    def __init__(self):
        self.info = None
        self.db = None

    def start(self, bot):
        if self.db is None:
            raise AttributeError("DataBase not initialized")
        bot.vjn_object = VJNObject(bot)
