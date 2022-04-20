import enum
from bot.lexer.token import *
from bot.message.message import *

class CommandFunction(enum.Enum):

    async def __call__(self, message : Message) -> None:
        if isinstance(self._value_, Command):
            await self._value_(message)

class Command:

    def __init__(self) -> None:
        self.function = {
        TokenType.TOKEN_TEST.name : self.test,
        }

    async def error(self, message : Message):
        if message.bot.user != message.message.author:
            print("Function name not found.")

    async def __call__(self, message : Message) -> None:
        await self.function.get(message.parse[0].name, self.error)(message)

    async def test(self, message : Message) -> None:
        await message.message.channel.send("Command test.")
