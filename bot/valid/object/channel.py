from bot import Id

class Channel(Id):
    def check(self, other):
        return self == other.server
