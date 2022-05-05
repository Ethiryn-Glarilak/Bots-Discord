from bot.valid.object.id_default import *

class Channel(Id):
    def check(self, other):
        return self == other.server
