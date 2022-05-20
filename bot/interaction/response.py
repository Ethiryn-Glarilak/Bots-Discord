import discord_components
import re

class Response:

    def __init__(self) -> None:
        self.function = {
        }

    async def __call__(self, interaction : discord_components.Interaction) -> None:
        for function, value in self.function.items():
            if re.match(function, interaction.custom_id):
                await value(interaction)
                return
        await self.error(interaction)

    async def error(self, message):
        if message.bot.user != message.author:
            message.bot.log.get_logger(f"interaction-{message.bot.name}", "interaction", True).debug(f"Function not found {message.parse[0]}")
