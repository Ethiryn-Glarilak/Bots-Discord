import discord_components
from src.interaction.interaction import Interaction
from src.interaction.composent.button import Style

def menu(id_command : int):
    return Interaction()\
        .add_interaction(
            Interaction()
                .add_button(label = "Valider", style = Style.GREEN, id = f"valider-commande-{id_command}")
    # FIXME
                # .add_button(label = "Retour", style = Style.GREY, id = f"retour--valider-{id_command}")
    # FIXME
                # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--valider-{id_command}")
        )

async def valider_quantity(interaction : discord_components.Interaction):
    await interaction.defer(edit_origin = True)
    quantity = 1 if interaction.values == [] else interaction.values[0].split('-')[1]
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")

    database.execute(f"""
        UPDATE command_VJN
        SET quantity = {quantity}
        WHERE id = {id_command}
    """)

    await interaction.edit_origin(
        content = f"Commande n°{id_command}\n{command(interaction, id_command)}\nConfirmer votre commande.",
        components = menu(id_command)
    )
