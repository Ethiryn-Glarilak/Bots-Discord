import os
import pathlib
from extension.command_vjn.example import example as example_command
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style
from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator
from extension.command_vjn.vjn_object import VJNObject
from extension.command_vjn.interaction.get_data import get_data

async def refresh(message) -> None:
    if DefaultValidator.creator(message).check():
        message.bot.vjn_object = VJNObject(message.bot)
        await message.delete()

        # Start VJN
        channel = message.bot.get_channel(int(os.getenv("command"))) # channel command
        async for element in channel.history():
            await element.delete()
        components = Interaction().add_button(label = "Commander", style = Style.GREEN, id = "commander")
        await channel.send(components=components)

        # Help VJN
        channel = message.bot.get_channel(int(os.getenv("help"))) # channel command
        async for element in channel.history():
            await element.delete()
        await channel.send(
            content=pathlib.Path("data/guild/689388320815710239-VJN/help.txt").read_text(encoding = "utf-8")
                    .replace("@dev-chef", "@680605398549528613")
                    .replace("#help", f"#{os.getenv('command')}")
                    .replace("#roles", f"#{os.getenv('roles')}")
        )

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

async def data(message) -> None:
    if DefaultValidator.creator(message).add_user(502595083137318912).check():
        await get_data(message)

class CommandCommandVJN:

    additional_function = {
        TokenType.TOKEN_REFRESH.name : refresh,
        TokenType.TOKEN_EXAMPLE.name : example,
        TokenType.TOKEN_DATA.name : data,
        # TokenType.TOKEN_WORD.name : none,
    }
