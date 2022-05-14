from bot.parser.lexer.lexer import Lexer
from bot.parser.token.token_type import TokenType

class Parser:

    def __init__(self, prefix) -> None:
        self.lexer : Lexer = Lexer(prefix)
        self.list : list = []
        self.error : list = []

    rules : dict = {
        "default" : [
            {"next" : "test"},
            {"next" : "words"},
        ],
        "test" : [
            {"token" : [TokenType.TOKEN_TEST], "save" : True, "mandatory" : 1, "number" : 1},
        ],
        "words" : [
            {"token" : [
                TokenType.TOKEN_WORD,
                TokenType.TOKEN_IO_NUMBER,
                        ], "save" : True, "mandatory" : -1, "number" : -1},
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
        tokens = rule.get("token", TokenType.TOKEN_ERROR)
        save = rule.get("save", True)
        lexer = self.lexer
        count = 0
        while True:
            position = 0
            while position < len(tokens):
                token = tokens[position]
                if token == lexer.peek():
                    if save:
                        self.list.append(lexer.pop())
                    else:
                        lexer.pop()
                    count += 1
                    break
                position += 1
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
                self.error.clear()
                self.lexer.restart()
                self.list.clear()
            if len(self.list) != 0:
                break
        if self.lexer.peek() == TokenType.TOKEN_EOF:
            return TokenType.TOKEN_NO_ERROR, self.list if len(self.list) > 0 else [TokenType.TOKEN_WORD]
        while self.lexer.peek() != TokenType.TOKEN_EOF:
            self.error.append(self.lexer.pop())
        return TokenType.TOKEN_ERROR, self.error
