import discord_components
from extension.command_vjn.interaction.cooking.log.message import livrer

async def send(interaction : discord_components.Interaction) -> None:
    await livrer(interaction)
