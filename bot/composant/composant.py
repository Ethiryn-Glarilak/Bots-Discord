class Composant:

    def __init__(self, good = True):
        self.good = good

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other and self.good or self.id != other and not self.good
        return super().__eq__(other)

    def check(self, other):
        return False

    def __getattribute__(self, __name: str) -> None:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            return self.discord.__getattribute__(__name)
