from src.parser.parser.parser import Parser
from src.parser.token.token_type import TokenType


class ParserNormal:

    @staticmethod
    def MODE_NORMAL(prefix : str) -> Parser:

        token = {
            "word_token" : [
                (f"{prefix}close", TokenType.TOKEN_CLOSE),
                ("0reboot", TokenType.TOKEN_REBOOT),
                (f"{prefix}reboot", TokenType.TOKEN_REBOOT),
            ],
        }

        additional_rules = {
            "reboot" : [
                {"token" : [TokenType.TOKEN_REBOOT], "save" : True, "mandatory" : 1, "number" : 1},
            ],
            "close" : [
                {"token" : [TokenType.TOKEN_CLOSE], "save" : True, "mandatory" : 1, "number" : 1},
            ],
        }

        additional_default = [
            {"next" : "reboot"},
            {"next" : "close"},
        ]

        return token, additional_rules, additional_default
