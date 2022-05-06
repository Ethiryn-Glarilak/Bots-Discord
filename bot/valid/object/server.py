from bot import Id

class Server(Id):
    def check(self, other):
        return self == other.server
