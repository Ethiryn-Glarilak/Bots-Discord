import discord_components
import re
from extension.command_vjn.interaction import *

async def error(interaction : discord_components.Interaction):
    if interaction.client.bot.user != interaction.user:
        interaction.client.bot.log.get_logger(f"interaction-{interaction.client.bot.name}", "interaction", True).debug(f"Function not found {interaction.custom_id}")
        await interaction.respond(content = f"Function not found `{interaction.custom_id}` `{interaction.values}`")

async def menu(interaction : discord_components.Interaction):
    for name, value in {
        "default" : default,
        "other" : other,
        "compose" : compose,
        "ingredient-*" : compose_ingredient,
        "product-*" : choice,
        "quantity-*" : valider_quantity,
    }.items():
        if re.match(name, interaction.values[0]) is not None:
            await value(interaction)
            return
    await error(interaction)

async def valider(interaction : discord_components.Interaction):
    for name, value in {
        "valider-composition-*" : compose_valider,
        "valider-quantity-*" : valider_quantity,
        "valider-commande-*" : confirme,
        "valider-paiement-*" : assignment,
        "valider-assigned-*" : ready,
        "valider-livrer-*" : send,
    }.items():
        if re.match(name, interaction.custom_id):
            await value(interaction)
            return
    await error(interaction)

async def annuler(interaction : discord_components.Interaction) -> None:
    for name, value in {
        "annuler-paiement-*" : annuler_paiement,
    }.items():
        if re.match(name, interaction.custom_id):
            await value(interaction)
            return
    await error(interaction)

class InteractionCommandVJN:

    additional_function = {
        "commander" : commander,
        "menu-*-*" : menu,
        "ingredient-*-*" : menu_ingredient,
        "valider-*-*" : valider,
        "assigned-*" : assigned,
        "modifier-*-*" : modifier,
        # "retour-*" : retour,
        "annuler-*" : annuler,
    }
