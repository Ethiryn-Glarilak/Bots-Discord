import discord_components
import os
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction

def command(interaction : discord_components.Interaction, id_command : int):
    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    name = database.execute(f"SELECT name FROM product_VJN WHERE id = {id_product}").fetchall()[0, "name"].capitalize() + " :"
    database.execute(f"SELECT name FROM (SELECT id_ingredient FROM (SELECT * FROM product_VJN WHERE id = {id_product}) AS product_VJN JOIN product_ingredient_VJN ON id = id_product) AS product_ingredient_VJN JOIN ingredient_VJN ON id = id_ingredient").fetchall()
    for product in database:
        name += f" {product[0]},"
    return name[:-1]

def menu(bot, id_command : int):
    json = bot.vjn_object.json
    cooks = Interaction()
    for i in range(min(json.get("cooks"), 10)):
        cooks.add_button(label = f"Cuisinier {i + 1}", style = Style.GREY, id = f"assigned-{id_command}-{i}")
    return Interaction()\
        .add_interaction(cooks)\
    # FIXME
        # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--assigned-{id_command}")

async def modifier(interaction : discord_components.Interaction):
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    cooks = database.execute(f"SELECT status FROM command_VJN WHERE id = {id_command}").fetchall()[0, "status"]

    emojis = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    await interaction.edit_origin(
        content = f"{interaction.message.content[:-(4 + 1 + len(emojis[cooks + 1]) + 1)]}",
        components = menu(interaction.client.bot, id_command)
    )
