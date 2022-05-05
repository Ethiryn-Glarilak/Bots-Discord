from bot.valid.object.id_default import *

class Role(Id):
    def check(self, other):
        return any(self == role for role in other.roles)
