import discord
import typing
from bot import Bot, ParserMode, TokenType

# Essayer d'hériter de discord.Message mais d'initialiser avec un objet discord.Message
class Message(discord.Message):

    def __init__(self, message : discord.Message, bot : Bot):
        self.bot = bot

        for key, value in message.__dict__.items():
            self.__dict__[key] = value


    def set_parser(self) -> ParserMode:
        # To change prefix just write mode("new prefix") : self.bot.mode("new prefix").MODE_NORMAL
        return self.bot.mode.MODE_NORMAL

    def parse(self) -> TokenType:
        parser = self.set_parser()
        parser.set_lexer(self.content)
        code, parse = parser.parse()
        if code == TokenType.TOKEN_ERROR:
            return TokenType.TOKEN_ERROR
        self.parse : list[typing.Type(TokenType)] = parse
        return TokenType.TOKEN_NO_ERROR

    async def command(self) -> None:
        await self.bot.command(self)
