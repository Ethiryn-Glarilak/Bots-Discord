from bot.parser.token.token_type import TokenType

class ParserSeanren:

    @staticmethod
    def MODE_NORMAL(prefix : str) -> tuple[list, dict]:

        token = {
            "word_token" : [
                (f"{prefix}clear", TokenType.TOKEN_CLEAR),
                (f"{prefix}clean", TokenType.TOKEN_CLEAR),
            ],
        }

        additional_rules = {
            "clear" : [
                {"token" : [TokenType.TOKEN_CLEAR], "save" : True, "mandatory" : 1, "number" : 1},
                {"token" : [TokenType.TOKEN_IO_NUMBER], "save" : True, "mandatory" : 0, "number" : 1},
            ],
        }

        additional_default = [
            {"next" : "clear"},
        ]

        return token, additional_rules, additional_default
