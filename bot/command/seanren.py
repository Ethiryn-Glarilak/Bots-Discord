import os
from bot.command.command import *
from bot.message.message import *

class CommandSeanren(Command):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            "test" : self.test,
        }

        self.function.update(additional_function)

    async def test(self, message : Message) -> None:
        await message.message.channel.send("Command test de Seanren.")

    async def close(self) -> None:
        await self.close()

    async def reboot(self) -> None:
        try:
            await self.close()
        except Exception:
            print("Exception")
        finally:
            os.system("py -3 Seanren.py")

    async def clear(self, number: int) -> None:
        await self.channel.purge(limit = number + 1)
