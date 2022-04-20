import typing
import re
import termcolor
from bot.lexer.token import *

class Lexer(object):

    def __init__(self, mode : TokenMode = TokenMode.MODE_NORMAL) -> None:
        self.input : str = None
        self.position : int = 0
        self.token : Token = Token(TokenType.TOKEN_ERROR)
        self.mode : TokenMode = mode

    def new_token(self, type : TokenType, length : int, content : bool, buffer = None) -> Token:
        token = Token(type, (self.input[self.position:length] if buffer is None else buffer)) if content else Token(type)
        self.position += length
        return token

    def token_special_characters(self):
        return self.new_token(self.mode.value.get("spc_token_").get(self.input[self.position]), 1, False)

    def token_int(self, position : int):
        buffer = int(self.input[self.position:position])
        return self.new_token(TokenType.TOKEN_IO_NUMBER, position - self.position, True, buffer)

    def token_word(self, position : int, active : bool) -> Token:
        escape : bool = False
        buffer = ""
        for char in self.input[self.position:position]:
            if escape:
                escape_char : typing.Union(tuple(str, str), None) = self.mode.value.get("esc_token_").get(char)
                buffer += char if escape_char is None else escape_char[active]
                escape : bool = False
            elif char == '\\':
                escape : bool = True
            else:
                buffer += char
        return self.new_token(TokenType.TOKEN_WORD, position - self.position, True, buffer)

    def check_special_characters(self, char : str) -> bool:
        return char in self.mode.value.get("spc_char__")

    def next(self) -> Token:
        ''' Return next token '''
        if len(self.input) <= self.position:
            return self.new_token(TokenType.TOKEN_EOF, 0, False)

        while len(self.input) - 1 > self.position and self.input[self.position] == " ":
            self.position += 1

        position : int = self.position

        if self.check_special_characters(self.input[self.position]):
            return self.token_special_characters()

        while len(self.input) > position and not \
                self.check_special_characters(self.input[position]) \
                and self.input[position] != " ":
            position += 1

        return self.token_characters(position)

    def reset(self, input : str = None) -> None:
        ''' Reset the lexer to new input '''
        self.position = 0
        self.input = input
        if input is None:
            self.token = Token(TokenType.TOKEN_ERROR)
        self.token = self.next()

    def peek(self) -> Token:
        ''' Return the next token '''
        return self.token

    def pop(self) -> Token:
        ''' Go to the next token '''
        if self.input is None:
            return self.token
        token = self.token
        self.token = self.next()
        return token

    def token_characters(self, position: int) -> Token:
        tokens : typing.Union[None, list[tuple[str, TokenType]]] = self.mode.value.get("word_token").get(position - self.position)

        if tokens is None:
            if re.match(r'^\-?[0-9]*$', self.input[self.position:position]):
                # print("coucou")
                return self.token_int(position)
            return self.token_word(position, 0)

        for token in tokens:
            if token[0] == self.input[self.position:position]:
                return self.new_token(token[1], position - self.position, 0)
        if re.match(r'^\-?[0-9]*$', self.input[self.position:position]):
            # print("coucou")
            return self.token_int(position)
        return self.token_word(position, 0)

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
