import typing
from src.parser.token.token import Token
from src.parser.token.token_type import TokenType

class LexerDefault:

    def __init__(self, prefix : str) -> None:
        self.input : typing.Union(str, None) = None
        self.position : int = 0
        self.token : Token = Token(TokenType.TOKEN_ERROR)
        self.mode = {
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
            "word_token" : {},
        }
        token_list = [
            (f"{prefix}t", TokenType.TOKEN_TEST),
            ("0t", TokenType.TOKEN_TEST),
        ]
        word_token(self, token_list)

    def __str__(self) -> str:
        if self.position == len(self.input):
            return self.input
        return f"{self.input[: self.position]} {self.input[self.position]} {self.input[self.position + 1:]}"

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.token.type == TokenType.TOKEN_EOF:
            raise StopIteration
        return self.pop()

def word_token(lexer : LexerDefault, token_list : list[tuple[str, TokenType]]):
    for token in token_list:
        element = lexer.mode.get("word_token").get(len(token[0]), [])
        element.append(token)
        lexer.mode.get("word_token")[len(token[0])] = element
