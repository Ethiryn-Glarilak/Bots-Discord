from bot.lexer import *
from bot.parser.parser import *

# Import parser
from bot.parser.normal import *
from bot.parser.command_vjn import *

class ParserMode():#ParserFunction):
    MODE_NORMAL = ParserNormal
    # MODE_COMMAND_VJN = ParserCommandJVN

    TOKEN_MODE = TokenMode()

    def __getattribute__(self, __name):
        if "MODE_" in __name:
            return super().__getattribute__(__name)(getattr(self.TOKEN_MODE, __name))
        return super().__getattribute__(__name)

    def __call__(self, prefix):
        self.TOKEN_MODE(prefix)
        return self

class ParserExample(Parser):

    def __init__(self, mode : TokenMode) -> None:
        print("""
        # To create a new ParserClass you must to write function this code :

        super().__init__(mode)

        additional_rules = {}

        additional_default = {}

        self.rules.update(self.additional_rules)
        self.rules.get("default").extend(self.additional_default)

        # And write rule :
        additional_rules = {}
        additional_default = {}
        """)

    def special_parser(self):
        print("""
        # Write a specific rule :

        # Talk an other rule use to launch and test return value
        if self.default_parse("name_rule") == TokenType.TOKEN_ERROR:
            # To return an error
            return TokenType.TOKEN_ERROR

        # To return successful
        return TokenType.TOKEN_NO_ERROR
        """)