from bot.lexer import *
from bot.parser.parser import *

class ParserNormal(Parser):

    def __init__(self, mode : TokenMode) -> None:
        super().__init__(mode)

        additional_rules = {
            "words" : [
                {"token" : [
                    TokenType.TOKEN_WORD,
                    TokenType.TOKEN_IO_NUMBER,
                            ], "save" : True, "mandatory" : -1, "number" : -1},
            ],
        }

        additional_default = [
            {"next" : "words"},
        ]

        self.rules.update(additional_rules)
        self.rules.get("default").extend(additional_default)
