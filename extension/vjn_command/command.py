import discord
from src.parser.token.token_type import TokenType
from src.valid.default import DefaultValidator

async def test(message) -> None:
    if DefaultValidator.creator(message).check():
        await message.channel.send("Command test de Seanren.")

async def clear(message) -> None:
    number = 1 if len(message.parser) <= 1 else message.parser[1].content
    async for element in message.channel.history(limit = number + 1):
        if message.channel.type != discord.ChannelType.private or element.author.id == message.bot.user.id:
            await element.delete()

class CommandVJNCommand:

    additional_function = {
        TokenType.TOKEN_TEST.name : test,
        TokenType.TOKEN_CLEAR.name : clear,
    }
