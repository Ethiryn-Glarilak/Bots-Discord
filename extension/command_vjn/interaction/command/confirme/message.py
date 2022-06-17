import discord_components
from src.interaction.interaction import Interaction
from src.interaction.composent.button import Style
from extension.command_vjn.interaction.default import *

def command(interaction : discord_components.Interaction, id_command : int):
    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    name = database.execute(f"SELECT name FROM product_VJN WHERE id = {id_product}").fetchall()[0, "name"].capitalize() + " :"
    database.execute(f"SELECT name FROM (SELECT id_ingredient FROM (SELECT * FROM product_VJN WHERE id = {id_product}) AS product_VJN JOIN product_ingredient_VJN ON id = id_product) AS product_ingredient_VJN JOIN ingredient_VJN ON id = id_ingredient").fetchall()
    for product in database:
        name += f" {product[0]},"
    return name[:-1]

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
