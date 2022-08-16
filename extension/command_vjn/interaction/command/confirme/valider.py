import discord_components
from extension.command_vjn.interaction.default import *
from extension.command_vjn.interaction.cooking.paiement.message import paiement

async def confirme(interaction : discord_components.Interaction):
    await paiement(interaction)
