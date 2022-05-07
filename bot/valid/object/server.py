from bot.valid.object.id_default import Id

class Server(Id):
    def check(self, other):
        return self == other.server
