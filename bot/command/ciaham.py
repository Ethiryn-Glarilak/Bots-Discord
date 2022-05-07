from bot.command.command import CommandDefault
from bot.lexer.type import TokenType
from bot.message.message import Message
from bot.valid.default import DefaultValidator

class CommandCiaham(CommandDefault):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            TokenType.TOKEN_TEST.name : self.test,
        }

        self.function.update(additional_function)

    async def test(self, message : Message) -> None:
        if DefaultValidator.creator(message).check():
            await message.channel.send("Command test de Seanren.")
