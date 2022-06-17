import discord_components
import os
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction
from extension.command_vjn.vjn_object import Status

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

async def assignment(interaction : discord_components.Interaction):
    bot = interaction.client.bot
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")

    # FIXME
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FILE_ATTENTE.value}
        WHERE id = {id_command}
    """)

    # FIXME
    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}").fetchall()
    value = database.value

    user = bot.get_user(database[0, "id_user"])
    if user is not None:
        await user.send(content = f"La commande {command(interaction, id_command)} est envoyée à VJN.")

    database.value = value

    quantity = database[0, "quantity"]
    price = database[0, "price"]
    user = bot.get_user(database[0, "id_user"])
    channel = interaction.client.bot.get_channel(int(os.getenv("assignment"))) # channel assignment

    content = f"n°{id_command} {user} : {command(interaction, id_command)} -> {price}"
    components = menu(bot, id_command)

    for _ in range(1, quantity + 1):
        await channel.send(content = content, components = components)
    await interaction.message.delete()
