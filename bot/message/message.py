import discord
from bot.bot.bot import *
from bot.lexer.token import *
from bot.parser.constructor import *

# Essayer d'hériter de discord.Message mais d'initialiser avec un objet discord.Message
class Message():

    def __init__(self, message : discord.Message, bot : Bot):
        self.message = message
        self.bot = bot

    def set_parser(self) -> ParserMode:
        return ParserMode.MODE_NORMAL()

    def parse(self) -> TokenType:
        parser = self.set_parser()
        parser.set_lexer(self.message.content)
        code, parse = parser.parse()
        if code == TokenType.TOKEN_ERROR:
            return TokenType.TOKEN_ERROR
        self.parse : list[TokenType] = parse
        return TokenType.TOKEN_NO_ERROR

    async def command(self) -> None:
        await self.bot.command(self)
