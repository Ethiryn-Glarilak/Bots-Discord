import enum
import os
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
            TokenType.TOKEN_WORD.name : self.none,
            TokenType.TOKEN_IO_NUMBER.name : self.none,
        }

    async def none(self, message : Message) -> None:
        message.bot.log.getLogger(f"command-{message.bot.name}").start(filename = "command").debug("Message ignore")

    async def error(self, message : Message):
        if message.bot.user != message.message.author:
            print("Function name not found.")

    async def __call__(self, message : Message) -> None:
        await self.function.get(message.parse[0].name, self.error)(message)

    async def test(self, message : Message) -> None:
        await message.message.channel.send("Command test.")

class CommandDefault(Command):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            TokenType.TOKEN_CLOSE.name : self.close,
            TokenType.TOKEN_REBOOT.name : self.reboot,
        }

        self.function.update(additional_function)

    async def close(self, message : Message) -> None:
        await message.bot.get_channel(966322896014307398).send(f"Command close de {message.bot.name}.")
        await message.bot.close()

    async def reboot(self, message : Message) -> None:
        try:
            await message.bot.get_channel(966322896014307398).send(f"Command reboot de {message.bot.name}.")
            await message.bot.close()
        except Exception:
            print("Exception")
        finally:
            os.system(f"py -3 {message.bot.name}.py")
