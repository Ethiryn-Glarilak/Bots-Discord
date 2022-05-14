import enum

class TokenType(enum.Enum):
    pass

class Token(object):

    def __init__(self, type : TokenType, content : str = None) -> None:
        self.type : TokenType = type
        self.content : str = content

    def __getattr__(self, attr : str):
        if attr == "name":
            return self.type.name
        if attr == "value":
            return self.type.value

    def __repr__(self):
        return f"{self.type.name} : {self.content}"

    def __str__(self):
        return f"{self.type.name} : {self.content}"
