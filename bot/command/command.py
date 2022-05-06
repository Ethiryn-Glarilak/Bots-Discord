import enum
import os
import platform
from bot import DefaultValidator, Message, TokenType

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
        message.bot.log.get_logger(f"command-{message.bot.name}", "command", True).debug("Message ignore")

    async def error(self, message : Message):
        if message.bot.user != message.message.author:
            message.bot.log.get_logger(f"command-{message.bot.name}", "command", True).debug(f"Function not found {message.parse[0]}")

    async def __call__(self, message : Message) -> None:
        await self.function.get(message.parse[0].name, self.error)(message)

    async def test(self, message : Message) -> None:
        if DefaultValidator.creator(message).check():
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
        if DefaultValidator.creator(message).check():
            await message.bot.get_channel(966322896014307398).send(f"Command close of {message.bot.name}.")
            await message.bot.close()
        else:
            await message.bot.get_channel(966322896014307398).send(f"User {message.message.author} use command close but not authorized.")

    async def reboot(self, message : Message) -> None:
        if DefaultValidator.creator(message).check():
            try:
                await message.bot.get_channel(966322896014307398).send(f"Command reboot of {message.bot.name}.")
                await message.bot.close()
            except Exception:
                print("Exception")
            finally:
                if platform.system() == "Windows":
                    os.system(f"py -3 {message.bot.name}.py")
                elif platform.system() == "Linux":
                    os.system(f"python3 {message.bot.name}.py")
                else:
                    message.bot.log.get("command").error(f"os not supported : {platform.system()}")
        else:
            await message.bot.get_channel(966322896014307398).send(f"User {message.message.author} use command reboot but not authorized.")
