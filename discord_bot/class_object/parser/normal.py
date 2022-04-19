from discord_bot.class_object.lexer import *
from discord_bot.class_object.parser.parser import *

class ParserNormal(Parser):

    def __init__(self, lexer : Lexer = Lexer()) -> None:
        super().__init__(lexer)

        additional_rules = {
            "words" : [
                {"token" : TokenType.TOKEN_WORD, "save" : True, "mandatory" : False},
            ],
        }

        additional_default = [
            {"next" : "words"},
        ]

        self.rules.update(additional_rules)
        self.rules.get("default").extend(additional_default)
