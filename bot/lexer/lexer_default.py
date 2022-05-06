import typing
import termcolor
from bot import Token, TokenMode, TokenType

class LexerDefault:

    def __init__(self, mode : TokenMode) -> None:
        self.input : typing.Union(str, None) = None
        self.position : int = 0
        self.token : Token = Token(TokenType.TOKEN_ERROR)
        self.mode : TokenMode = mode

    def __str__(self) -> str:
        if self.position == len(self.input):
            return self.input
        return f"{self.input[: self.position]} {termcolor.colored(self.input[self.position], 'red')} {self.input[self.position + 1:]}"

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.token.type == TokenType.TOKEN_EOF:
            raise StopIteration
        return self.pop()
