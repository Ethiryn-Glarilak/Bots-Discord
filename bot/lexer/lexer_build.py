import typing
import re
from bot import LexerDefault, Token, TokenType

class LexerBuild(LexerDefault):

    def new_token(self, type : TokenType, length : int, content : bool, buffer = None) -> Token:
        buffer = self.input[self.position:length] if buffer is None else buffer
        token = Token(type, (buffer)) if content else Token(type)
        self.position += length
        return token

    def token_special_characters(self):
        return self.new_token(self.mode.get("spc_token_").get(self.input[self.position]), 1, False)

    def token_int(self, position : int):
        buffer = int(self.input[self.position:position])
        return self.new_token(TokenType.TOKEN_IO_NUMBER, position - self.position, True, buffer)

    def token_word(self, position : int, active : bool) -> Token:
        escape : bool = False
        buffer = ""
        for char in self.input[self.position:position]:
            if escape:
                escape_char : typing.Union(tuple(str, str), None) = self.mode.get("esc_token_").get(char)
                buffer += char if escape_char is None else escape_char[active]
                escape : bool = False
            elif char == '\\':
                escape : bool = True
            else:
                buffer += char
        return self.new_token(TokenType.TOKEN_WORD, position - self.position, True, buffer)

    def token_characters(self, position: int) -> Token:
        tokens : typing.Union[None, list[tuple[str, typing.Type(TokenType)]]] = self.mode.get("word_token").get(position - self.position)

        if tokens is None:
            if re.match(r'^\-?[0-9]*$', self.input[self.position:position]):
                return self.token_int(position)
            return self.token_word(position, 0)

        for token in tokens:
            if token[0] == self.input[self.position:position]:
                return self.new_token(token[1], position - self.position, False)
        if re.match(r'^\-?[0-9]*$', self.input[self.position:position]):
            return self.token_int(position)
        return self.token_word(position, 0)

    def check_special_characters(self, char : str) -> bool:
        return char in self.mode.get("spc_char__")
