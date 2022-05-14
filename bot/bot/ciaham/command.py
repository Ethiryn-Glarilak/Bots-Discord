from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

async def test(message) -> None:
    if DefaultValidator.creator(message).check():
        await message.channel.send("Command test de Ciaham.")

class CommandCiaham:

    additional_function = {
        TokenType.TOKEN_TEST.name : test,
    }
