from bot.valid.validator import *

class Id:

    def __init__(self, id : int, good = True):
        if not isinstance(id, int):
            raise TypeError("Type must be int")
        self.id = id
        self.good = good

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other and self.good or self.id != other and not self.good
        raise TypeError(f"Type error on equality : {other}")

    def check(self, other):
        return False
