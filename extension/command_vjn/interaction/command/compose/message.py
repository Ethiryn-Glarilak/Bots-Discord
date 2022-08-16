import discord_components
from src.interaction.interaction import Interaction
from src.interaction.composent.button import Style
from extension.command_vjn.interaction.default import *

def menu(id_command : int, disabled : bool):
        return Interaction()\
            .add_button(label = "Pate", id = f"ingredient-pate-{id_command}")\
            .add_button(label = "Garniture", id = f"ingredient-garniture-{id_command}")\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = f"valider-composition-{id_command}", disabled = disabled)
    # FIXME
                    # .add_button(label = "Retour", style = Style.GREY, id = f"retour-start-{id_command}")
    # FIXME
                    # .add_button(label = "Annuler", style = Style.RED, id = f"annuler-composition-{id_command}")
            )

async def compose(interaction : discord_components.Interaction):
    await interaction.defer(edit_origin = True)
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.vjn_object.database

    id_product = insert_product(database, f"{interaction.user}_{id_command}")
    update_command_product(database, id_command, id_product)

    await interaction.edit_origin(components = menu(id_command, True))
