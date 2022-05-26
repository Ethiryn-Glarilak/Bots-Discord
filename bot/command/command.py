from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

class Command:

    def __init__(self) -> None:
        self.function = {
            TokenType.TOKEN_TEST.name : self.test,
            TokenType.TOKEN_WORD.name : self.none,
            TokenType.TOKEN_IO_NUMBER.name : self.none,
        }

    async def none(self, message) -> None:
        message.bot.log.get_logger(f"command-{message.bot.name}", "command", True).debug("Message ignore")

    async def error(self, message):
        if message.bot.user != message.author:
            message.bot.log.get_logger(f"command-{message.bot.name}", "command", True).debug(f"Function not found {message.parse[0]}")

    async def __call__(self, message) -> None:
        await self.function.get(message.parser[0].name, self.error)(message)

    async def test(self, message) -> None:
        if DefaultValidator.creator(message).check():
            await message.channel.send("Command test.")
