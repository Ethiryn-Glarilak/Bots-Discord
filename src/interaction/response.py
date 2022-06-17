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

    async def error(self, interaction : discord_components.Interaction):
        if interaction.client.bot.user != interaction.user:
            interaction.client.bot.log.get_logger(f"interaction-{interaction.client.bot.name}", "interaction", True).debug(f"Function not found {interaction.custom_id}")
            await interaction.respond(content = f"Function not found `{interaction.custom_id}`")
