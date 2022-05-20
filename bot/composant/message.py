import discord
import typing
from bot.composant.composant import Composant
from bot.parser.token.token_type import TokenType
from bot.parser.mode import Mode

class Message(Composant):

    def __init__(self, bot, message : discord.Message):
        self.bot = bot
        self.discord = message

    def set_parser(self) -> Mode:
        return self.bot.mode.MODE_NORMAL

    def parse(self) -> TokenType:
        parser = self.set_parser()
        parser.set_lexer(self.content)
        code, parse = parser.parse()
        if code == TokenType.TOKEN_ERROR:
            return TokenType.TOKEN_ERROR
        self.parser : list[typing.Type(TokenType)] = parse
        return TokenType.TOKEN_NO_ERROR

    async def command(self) -> None:
        await self.bot.command(self)
