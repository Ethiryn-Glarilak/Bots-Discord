from bot.lexer.lexer_build import *
from bot.lexer.token import *

class Lexer(LexerBuild):

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

    def restart(self) -> None:
        self.reset(self.input)
