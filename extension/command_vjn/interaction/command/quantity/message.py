import discord_components
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style
from extension.command_vjn.vjn_object import VJNObject
from extension.command_vjn.interaction.default import *

def menu(id_command, bot):
    vjn_object : VJNObject = bot.vjn_object
    json : dict[dict] = vjn_object.json

    start_menu = Interaction()\
        .add_menu(id = f"menu-quantity-{id_command}", placeholder = "Combien de crêpe souhaitez-vous ?")\
        .add_option(label = "1", value = "quantity-1", default = True)

    for number in range(2, min(24, max(0, json.get("quantity", 1) - 1)) + 2):
        start_menu.add_option(label = f"{number}", value = f"quantity-{number}")

    return start_menu.add_interaction(
        Interaction()
            .add_button(label = "Valider", style = Style.GREEN, id = f"valider-quantity-{id_command}")
    # FIXME
            # .add_button(label = "Retour", style = Style.GREY, id = f"retour--composition-{id_command}")
    # FIXME
            # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--composition-{id_command}")
    )

async def quantity(interaction : discord_components.Interaction):
    id_command = interaction.custom_id.split('-')[2]
    bot = interaction.client.bot
    await interaction.edit_origin(components = menu(id_command, bot))
