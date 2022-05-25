import os
from extension.command_vjn.example import example as example_command
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style
from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator
from extension.command_vjn.vjn_object import VJNObject

async def refresh(message) -> None:
    if DefaultValidator.creator(message).check():
        message.bot.vjn_object = VJNObject(message.bot)
        channel = message.bot.get_channel(int(os.getenv("command"))) # channel command
        async for element in channel.history():
            await element.delete()
        components = Interaction().add_button(label = "Commander", style = Style.GREEN, id = "commander", emoji = "✅")
        await channel.send("Clicker et rendez-vous dans tes DM avec moi", components=components)
        message.bot.database.get("default").commit()

# async def none(message) -> None:
#     if DefaultValidator.channel(message, [972454299789557860]).check() \
#         and not DefaultValidator.user(message, [message.bot.user.id]):
#         await message.delete()
#         # Add log
#     else:
#         await Command().none(message)

async def example(message) -> None:
    if not DefaultValidator.creator(message).check():
        return
    example_command(message)

class CommandCommandVJN:

    additional_function = {
        TokenType.TOKEN_REFRESH.name : refresh,
        TokenType.TOKEN_EXAMPLE.name : example,
        # TokenType.TOKEN_WORD.name : none,
    }
