from bot import Id

class Role(Id):
    def check(self, other):
        return any(self == role for role in other.roles)
