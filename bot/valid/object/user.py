from bot import Id

class User(Id):
    def check(self, other):
        return self == other.user
