from bot.command.command import Command
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style
from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

async def refresh(message) -> None:
    if DefaultValidator.creator(message).check():
        channel = message.bot.get_channel(972454299789557860)
        async for element in channel.history():
            await element.delete()
        components = Interaction().add_button(label  = "Commander", style = Style.GREEN, id = "commander")
        await channel.send("Clicker et rendez-vous dans tes DM avec moi", components=components)
        message.bot.vjn_object.set_start_menu(message.bot)

# async def none(message) -> None:
#     if DefaultValidator.channel(message, [972454299789557860]).check() \
#         and not DefaultValidator.user(message, [message.bot.user.id]):
#         await message.delete()
#         # Add log
#     else:
#         await Command().none(message)

class CommandCommandVJN:

    additional_function = {
        TokenType.TOKEN_REFRESH.name : refresh,
        # TokenType.TOKEN_WORD.name : none,
    }
