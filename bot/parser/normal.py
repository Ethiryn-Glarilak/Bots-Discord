from bot.lexer import *
from bot.parser.parser import *

class ParserNormal(Parser):

    def __init__(self, lexer : Lexer = Lexer()) -> None:
        super().__init__(lexer)

        additional_rules = {
            "words" : [
                {"token" : TokenType.TOKEN_WORD, "save" : True, "mandatory" : -1, "number" : -1},
            ],
        }

        additional_default = [
            {"next" : "words"},
        ]

        self.rules.update(additional_rules)
        self.rules.get("default").extend(additional_default)