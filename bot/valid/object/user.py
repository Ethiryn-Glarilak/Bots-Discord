from bot.valid.object.id_default import Id

class User(Id):
    def check(self, other):
        return self == other.user
