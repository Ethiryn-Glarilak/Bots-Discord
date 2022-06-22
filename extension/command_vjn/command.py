import pathlib
from extension.command_vjn.example import example as example_command
from src.interaction.interaction import Interaction
from src.interaction.composent.button import Style
from src.parser.token.token_type import TokenType
from src.valid.default import DefaultValidator
from extension.command_vjn.vjn_object import VJNObject
from extension.command_vjn.interaction.get_data import get_data

async def refresh(message) -> None:
    if not DefaultValidator.creator(message).check():
        return

    message.bot.vjn_object = VJNObject(message.bot)
    vjn_object = message.bot.vjn_object
    await message.delete()

    # Start VJN
    channel = message.bot.get_channel(vjn_object.command) # channel command
    async for element in channel.history():
        await element.delete()
    components = Interaction().add_button(label = "Commander", style = Style.GREEN, id = "commander")
    await channel.send(
        content=pathlib.Path("data/guild/890357045138690108-VJN/command.txt").read_text(encoding = "utf-8")
                .replace("@dev-chef", "@680605398549528613")
                .replace("#help", f"#{vjn_object.command}")
                .replace("#welcome", f"#{vjn_object.welcome}"),
        components=components
    )

    # Help VJN
    channel = message.bot.get_channel(vjn_object.help) # channel command
    async for element in channel.history():
        await element.delete()
    await channel.send(
        content=pathlib.Path("data/guild/890357045138690108-VJN/help.txt").read_text(encoding = "utf-8")
                .replace("@dev-chef", "@680605398549528613")
                .replace("#help", f"#{vjn_object.command}")
                .replace("#welcome", f"#{vjn_object.welcome}")
    )

    await message.bot.vjn_object.start(message.bot)

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
    }
