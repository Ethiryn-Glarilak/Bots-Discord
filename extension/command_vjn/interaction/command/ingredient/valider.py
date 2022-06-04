import discord_components
from extension.command_vjn.interaction.command.quantity.message import quantity
from extension.command_vjn.interaction.default import *

async def compose_valider(interaction : discord_components.Interaction):
    await quantity(interaction)
