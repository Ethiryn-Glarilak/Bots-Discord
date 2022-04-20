import os
from bot.command.command import *
from bot.message.message import *

class CommandSeanren(Command):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            TokenType.TOKEN_TEST.name : self.test,
            TokenType.TOKEN_CLEAR.name : self.clear,
            TokenType.TOKEN_CLOSE.name : self.close,
            TokenType.TOKEN_REBOOT.name : self.reboot,
        }

        self.function.update(additional_function)

    async def test(self, message : Message) -> None:
        await message.message.channel.send("Command test de Seanren.")

    async def close(self, message : Message) -> None:
        await message.bot.get_channel(966322896014307398).send("Command close de Seanren.")
        await message.bot.close()

    async def reboot(self, message : Message) -> None:
        try:
            await message.bot.get_channel(966322896014307398).send("Command reboot de Seanren.")
            await message.bot.close()
        except Exception:
            print("Exception")
        finally:
            os.system("py -3 Seanren.py")

    async def clear(self, message : Message) -> None:
        number = 1 if len(message.parse) <= 1 else message.parse[1].content
        await message.message.channel.purge(limit = number + 1)
