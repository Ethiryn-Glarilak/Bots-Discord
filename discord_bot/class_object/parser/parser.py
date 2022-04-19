import enum
from discord_bot.class_object.lexer import *

class ParserFunction(enum.Enum):
    def set_lexer(self, string : str) -> None:
        self.value.set_lexer(string)

    def parse(self) -> None:
        return self.value.parse()

class Parser(object):

    def __init__(self, lexer : Lexer = Lexer()) -> None:
        self.lexer : Lexer = lexer
        self.list : list = []
        self.error : list = []

    rules : dict = {
        "default" : [
            {"next" : "test"},
        ],
        "example" : [
            {"next" : str},
            {"token" : TokenType, "save" : bool, "mandatory" : bool},
        ],
        "test" : [
            {"token" : TokenType.TOKEN_TEST, "save" : True, "mandatory" : False},
        ],
    }

    def default_parse(self, name : str) -> TokenType:
        for rule in self.rules.get(name, []):
            if rule.get("next") is not None and self.default_parse(rule.get("next", "")) == TokenType.TOKEN_ERROR:
                return TokenType.TOKEN_ERROR
            if rule.get("function") is not None:
                if rule.get("function")() == TokenType.TOKEN_ERROR:
                    return TokenType.TOKEN_ERROR
            elif rule.get("token") == self.lexer.peek():
                if rule.get("save"):
                    self.list.append(self.lexer.pop())
            elif rule.get("mandatory"):
                self.error.append(self.lexer.pop())
                return TokenType.TOKEN_ERROR
        return TokenType.TOKEN_NO_ERROR

    def set_lexer(self, string : str) -> None:
        self.lexer.reset(string)

    def parse(self):
        for rule in self.rules.get("default", []):
            if self.default_parse(rule.get("next", "")) == TokenType.TOKEN_ERROR:
                return TokenType.TOKEN_ERROR, self.error
            if len(self.list) != 0:
                break
        if self.lexer.peek() == TokenType.TOKEN_EOF:
            return TokenType.TOKEN_NO_ERROR, self.list
        while self.lexer.peek() != TokenType.TOKEN_EOF:
            self.error.append(self.lexer.pop())
        return TokenType.TOKEN_ERROR, self.error
