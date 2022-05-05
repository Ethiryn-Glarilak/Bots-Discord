from bot.valid.object.id_default import *

class User(Id):
    def check(self, other):
        return self == other.user
