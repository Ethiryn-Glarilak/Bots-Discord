import enum
from bot.lexer import *

class Parser(object):

    def __init__(self, mode : TokenMode) -> None:
        self.lexer : Lexer = Lexer(mode)
        self.list : list = []
        self.error : list = []

    rules : dict = {
        "default" : [
            {"next" : "test"},
            {"next" : "clear"},
            {"next" : "reboot"},
            {"next" : "close"},
        ],
        "example" : [
            {"next" : str},
            {"token" : TokenType, "save" : bool, "mandatory" : bool},
        ],
        "test" : [
            {"token" : TokenType.TOKEN_TEST, "save" : True, "mandatory" : 0},
        ],
        "reboot" : [
            {"token" : TokenType.TOKEN_REBOOT, "save" : True, "mandatory" : 0},
        ],
        "close" : [
            {"token" : TokenType.TOKEN_CLOSE, "save" : True, "mandatory" : 0},
        ],
        "clear" : [
            {"token" : TokenType.TOKEN_CLEAR, "save" : True, "mandatory" : 0, "number" : 0},
            {"token" : TokenType.TOKEN_IO_NUMBER, "save" : True, "mandatory" : 0, "number" : 0},
        ],
    }

    def default_parse(self, name : str) -> TokenType:
        for rule in self.rules.get(name, []):
            if rule.get("next") is not None:
                if self.default_parse(rule.get("next", "")) == TokenType.TOKEN_ERROR:
                    return TokenType.TOKEN_ERROR
            elif rule.get("function") is not None:
                if rule.get("function")() == TokenType.TOKEN_ERROR:
                    return TokenType.TOKEN_ERROR
            elif self.check_token(rule) == TokenType.TOKEN_ERROR:
                return TokenType.TOKEN_ERROR
        return TokenType.TOKEN_NO_ERROR

    def check_token(self, rule : list[dict]) -> bool:
        mandatory = rule.get("mandatory", 0)
        number = rule.get("number", 0)
        token = rule.get("token", TokenType.TOKEN_ERROR)
        save = rule.get("save", True)
        lexer = self.lexer
        count = 0
        while True:
            if token == lexer.peek():
                if save:
                    self.list.append(lexer.pop())
                else:
                    lexer.pop()
                count += 1
            else:
                if mandatory < count and mandatory > 0:
                    self.error.append(self.lexer.pop())
                    return TokenType.TOKEN_ERROR
                break
            if number >= count and number > 0:
                break
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

class ParserDefault():
    TOKEN_MODE = TokenMode()

    def __getattribute__(self, __name):
        if "MODE_" in __name:
            return super().__getattribute__(__name)(getattr(self.TOKEN_MODE, __name))
        return super().__getattribute__(__name)

    def __call__(self, prefix):
        self.TOKEN_MODE(prefix)
        return self
