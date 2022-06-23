import discord_components
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction
from extension.command_vjn.vjn_object import Status
from extension.command_vjn.interaction.default import *

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
    vjn_object = interaction.client.bot.vjn_object
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.vjn_object.database

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
    channel = interaction.client.bot.get_channel(vjn_object.assignment) # channel assignment

    content = f"n°{id_command} <@{user.id}> : {command(interaction, id_command)} -> {price}"
    components = menu(bot, id_command)

    for _ in range(1, quantity + 1):
        await channel.send(content = content, components = components)
    await interaction.message.delete()
