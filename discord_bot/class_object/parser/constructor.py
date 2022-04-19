from discord_bot.class_object.lexer import *
from discord_bot.class_object.parser.parser import *

# Import parser
from discord_bot.class_object.parser.normal import *
from discord_bot.class_object.parser.command_vjn import *

class ParserMode(ParserFunction):
    MODE_NORMAL = ParserNormal(Lexer(TokenMode.MODE_NORMAL))
    MODE_COMMAND_VJN = ParserCommandJVN(Lexer(TokenMode.MODE_COMMAND_VJN))

class ParserExample(Parser):

    def __init__(self, lexer : Lexer = Lexer()) -> None:
        print("""
        # To create a new ParserClass you must to write function this code :

        super().__init__(lexer)

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