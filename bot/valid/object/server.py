from bot.valid.object.id_default import *

class Server(Id):
    def check(self, other):
        return self == other.server
