from bot.parser.token.token_type import TokenType

class ParserCommandVJN:

    @staticmethod
    def MODE_NORMAL(prefix : str) -> tuple[list, dict]:

        prefix = "VJN"

        token = {
            "word_token" : [
                (f"{prefix}refresh", TokenType.TOKEN_REFRESH),
                ("test", TokenType.TOKEN_EXAMPLE),
            ]
        }

        additional_rules = {
            "refresh" : [
                {"token" : [TokenType.TOKEN_REFRESH], "save": True, "mandatory" : 1, "number" : 1},
            ],
            "example" : [
                {"token" : [TokenType.TOKEN_EXAMPLE], "save": True, "mandatory" : 1, "number" : 1},
            ],
        }

        additional_default = [
            {"next" : "refresh"},
            {"next" : "example"},
        ]

        return token, additional_rules, additional_default
