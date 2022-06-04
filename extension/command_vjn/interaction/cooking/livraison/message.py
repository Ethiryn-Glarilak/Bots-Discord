import discord_components
import os
from bot.interaction.composent.button import Style
from bot.interaction.interaction import Interaction
from extension.command_vjn.vjn_object import Status

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
        .add_button(label = "Livrer", style = Style.GREEN, id = f"valider-livrer-{id_command}")

async def livraison(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")

    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}").fetchall()
    if database[0, "quantity"] == database[0, "ready"] + 1:
        database.execute(f"""
            UPDATE command_VJN
            SET ready = ready + 1,
                status = {Status.READY.value}
            WHERE id = {id_command}
        """)
        channel = interaction.client.bot.get_channel(int(os.getenv("livraison"))) # channel livraison
        database.execute(f"SELECT id_user FROM command_VJN WHERE id = {id_command}").fetchall()
        await channel.send(content = interaction.message.content, components = menu(id_command))
        user = interaction.client.bot.get_user(database[0, "user"])
        await user.send(content = f"Votre commande n°{id_command} est prête. Il s'agit de la commande {command(interaction, id_command)}")
    else:
        database.execute(f"""
            UPDATE command_VJN
            SET ready = ready + 1
            WHERE id = {id_command}
        """)
    await interaction.message.delete()
