import enum

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
        raise TypeError(f"Type error on equality : {other.__class__.__name__}")

    @classmethod
    def example(cls) -> dict:
        return {
            "spc_token_" : {}, # Special token             dict[str : TokenType]
            "esc_token_" : {}, # Escape special character  dict[str : tuple(str, str)]
            "spc_char__" : "", # Special character         str
            "word_token" : {}, # Word token                dict[int : list[tuple(str, TokenType)]]
        }

    @classmethod
    def normal(cls) -> dict:
        return {
            "spc_token_" : {
                "[" : TokenType.TOKEN_L_HOCK,
                "]" : TokenType.TOKEN_R_HOCK,
                "{" : TokenType.TOKEN_L_BRACE,
                "}" : TokenType.TOKEN_R_BRACE,
                "(" : TokenType.TOKEN_L_PAREN,
                ")" : TokenType.TOKEN_R_PAREN,
                },
            "esc_token_" : {},
            "spc_char__" : "{}()[]",
            "word_token" : {
                2 : [
                    ("0t", TokenType.TOKEN_TEST),
                    ],
                6 : [
                    ("0clear", TokenType.TOKEN_CLEAR),
                    ("0clean", TokenType.TOKEN_CLEAR),
                    ("0close", TokenType.TOKEN_CLOSE),
                    ],
                7 : [
                    ("0reboot", TokenType.TOKEN_REBOOT),
                    ],
                },
        }

    @classmethod
    def command_vjn(cls) -> dict:
        return {
            "spc_token_" : None,
            "esc_token_" : None,
            "spc_char__" : None,
            "word_token" : None,
        }

class Token(object):

    def __init__(self, type : TokenType, content : str = None) -> None:
        self.type : TokenType = type
        self.content : str = content

    def __eq__(self, other):
        if not isinstance(other, TokenType):
            raise TypeError(f"Type error on equality : {other.__class__.__name__}")
        return self.type == other

    def __getattr__(self, attr : str):
        if attr == "name":
            return self.type.name
        if attr == "value":
            return self.type.value

    def __repr__(self):
        return f"{self.type.name} : {self.content}"

    def __str__(self):
        return f"{self.type.name} : {self.content}"

class TokenMode(enum.Enum):

    MODE_NORMAL = TokenType.normal()
    MODE_COMMAND_VJN = TokenType.command_vjn()
