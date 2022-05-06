import enum

class TokenType(enum.Enum):
    pass

class Token(object):

    def __init__(self, type : TokenType, content : str = None) -> None:
        self.type : TokenType = type
        self.content : str = content

    def __eq__(self, other):
        if not isinstance(other, TokenType):
            raise TypeError(f"Type error on equality : {other}")
        return self.type == other

    def __getattr__(self, attr : str):
        if attr == "name":
            return self.type.name
        if attr == "value":
            return self.type.value

    def __repr__(self):
        return f"{self.type.name} : {self.content}"

    def __str__(self):
        return f"{self.type.name} : {self.content}"

from bot import TokenType

class TokenMode:

    MODE_NORMAL = TokenType.normal
    MODE_COMMAND_VJN = TokenType.command_vjn

    def pop_prefix(self):
        prefix = getattr(self, "prefix", None)
        if prefix is None:
            return "0"
        delattr(self, "prefix")
        return prefix

    def __getattribute__(self, __name):
        if "MODE_" in __name:
            return super().__getattribute__(__name)(self.pop_prefix())
        return super().__getattribute__(__name)

    def __call__(self, prefix):
        self.prefix = prefix
        return self
