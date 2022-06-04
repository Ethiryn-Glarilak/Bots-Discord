import discord_components
from extension.command_vjn.interaction.cooking.livraison.message import livraison

async def ready(interaction : discord_components.Interaction) -> None:
    await livraison(interaction)
