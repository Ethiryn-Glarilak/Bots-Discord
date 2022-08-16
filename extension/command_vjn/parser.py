from src.parser.token.token_type import TokenType

class ParserCommandVJN:

    @staticmethod
    def MODE_NORMAL(prefix : str) -> tuple[list, dict]:

        prefix_default = prefix
        prefix = "VJN"

        token = {
            "word_token" : [
                (f"{prefix_default}refresh", TokenType.TOKEN_REFRESH),
                ("test", TokenType.TOKEN_EXAMPLE),
                (f"{prefix_default}data", TokenType.TOKEN_DATA),
            ]
        }

        additional_rules = {
            "data" : [
                {"token" : [TokenType.TOKEN_DATA], "save": True, "mandatory" : 1, "number" : 1},
            ],
            "refresh" : [
                {"token" : [TokenType.TOKEN_REFRESH], "save": True, "mandatory" : 1, "number" : 1},
            ],
            "example" : [
                {"token" : [TokenType.TOKEN_EXAMPLE], "save": True, "mandatory" : 1, "number" : 1},
            ],
        }

        additional_default = [
            {"next" : "data"},
            {"next" : "refresh"},
            {"next" : "example"},
        ]

        return token, additional_rules, additional_default
