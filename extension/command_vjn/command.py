from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

async def refresh(message) -> None:
    if DefaultValidator.creator(message).check():
        channel = message.bot.get_channel(972454299789557860)
        async for element in channel.history():
            await element.delete()
        await channel.send("Futur interactions")

class CommandCommandVJN:

    additional_function = {
        TokenType.TOKEN_REFRESH.name : refresh
    }
