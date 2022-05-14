from bot.parser.token.token_type import TokenType

class ParserCommandVJN:

    @staticmethod
    def MODE_NORMAL(prefix : str) -> tuple[list, dict]:

        prefix = "VJN"

        token = {
            "word_token" : [
                (f"{prefix}refresh", TokenType.TOKEN_REFRESH),
            ]
        }

        additional_rules = {
            "refresh" : [
                {"token" : [TokenType.TOKEN_REFRESH], "save": True, "mandatory" : 1, "number" : 1},
            ]
        }

        additional_default = [
            {"next" : "refresh"},
        ]

        return token, additional_rules, additional_default
