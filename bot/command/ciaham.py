import os
from bot.command.command import *
from bot.message.message import *

class CommandCiaham(CommandDefault):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            TokenType.TOKEN_TEST.name : self.test,
        }

        self.function.update(additional_function)

    async def test(self, message : Message) -> None:
        await message.message.channel.send("Command test de Seanren.")
