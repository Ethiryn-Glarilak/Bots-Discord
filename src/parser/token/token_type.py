import enum
from src.parser.token.token import Token

class TokenType(enum.Enum):

    # The grammar symbols #
    TOKEN_WORD = 0
    TOKEN_IO_NUMBER = 4
    TOKEN_EOF = 5
    TOKEN_NO_ERROR = 6
    TOKEN_ERROR = 7

    #  Reserved words #
    TOKEN_TEST = 8
    TOKEN_CLEAR = 9
    TOKEN_CLOSE = 10
    TOKEN_REBOOT = 11
    TOKEN_REFRESH = 12
    TOKEN_EXAMPLE = 13
    TOKEN_DATA = 14

    #  Other reserved words #
    TOKEN_L_HOCK = 31 # <'['>
    TOKEN_R_HOCK = 32 # <']'>
    TOKEN_L_BRACE = 31 # <'{'>
    TOKEN_R_BRACE = 32 # <'}'>
    TOKEN_L_PAREN = 35 # <'('>
    TOKEN_R_PAREN = 36 # <')'>

    def __eq__(self, other):
        if isinstance(other, Token):
            return self == other.type
        if isinstance(other, TokenType):
            return self.value == other.value
        raise TypeError(f"Type error on equality : {other}")
