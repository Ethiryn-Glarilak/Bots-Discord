from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

async def test(message) -> None:
    if DefaultValidator.creator(message).check():
        await message.channel.send("Command test de Seanren.")

async def clear(message) -> None:
    number = 1 if len(message.parse) <= 1 else message.parse[1].content
    async for message in message.channel.history(limit = number + 1):
        await message.delete()
class CommandSeanren:

    additional_function = {
        TokenType.TOKEN_TEST.name : test,
        TokenType.TOKEN_CLEAR.name : clear,
    }