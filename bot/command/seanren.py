from bot.command.command import CommandDefault
from bot.valid.default import DefaultValidator
from bot.message.message import Message
from bot.lexer.type import TokenType

class CommandSeanren(CommandDefault):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            TokenType.TOKEN_TEST.name : self.test,
            TokenType.TOKEN_CLEAR.name : self.clear,
            TokenType.TOKEN_WORD.name : self.none,
        }

        self.function.update(additional_function)

    async def test(self, message : Message) -> None:
        if DefaultValidator.creator(message).check():
            await message.channel.send("Command test de Seanren.")

    async def clear(self, message : Message) -> None:
        number = 1 if len(message.parse) <= 1 else message.parse[1].content
        await message.channel.purge(limit = number + 1)

    async def none(self, message : Message) -> None:
        if DefaultValidator.channel(message, [972454299789557860]).check():
            await message.author.send("Command test de Seanren.")
        else:
            super().none(message)
