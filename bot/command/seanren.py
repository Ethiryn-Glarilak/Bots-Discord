from bot import CommandDefault, DefaultValidator, Message, TokenType

class CommandSeanren(CommandDefault):

    def __init__(self) -> None:
        super().__init__()

        additional_function = {
            TokenType.TOKEN_TEST.name : self.test,
            TokenType.TOKEN_CLEAR.name : self.clear,
        }

        self.function.update(additional_function)

    async def test(self, message : Message) -> None:
        if DefaultValidator.creator(message).check():
            await message.message.channel.send("Command test de Seanren.")

    async def clear(self, message : Message) -> None:
        number = 1 if len(message.parse) <= 1 else message.parse[1].content
        await message.message.channel.purge(limit = number + 1)
