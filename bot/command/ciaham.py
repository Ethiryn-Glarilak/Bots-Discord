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
        valid = Validator()
        valid.add_user(680605398549528613).set_data(message)
        if valid.check():
            await message.message.channel.send("Command test de Seanren.")
