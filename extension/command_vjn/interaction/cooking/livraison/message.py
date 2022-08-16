import discord_components
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction
from extension.command_vjn.vjn_object import Status
from extension.command_vjn.interaction.default import *

def menu(id_command : int):
    return Interaction()\
        .add_button(label = "Livrer", style = Style.GREEN, id = f"valider-livrer-{id_command}")

async def livraison(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.vjn_object.database

    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}").fetchall()
    if database[0, "quantity"] == database[0, "ready"] + 1:
        database.execute(f"""
            UPDATE command_VJN
            SET ready = ready + 1,
                status = {Status.READY.value}
            WHERE id = {id_command}
        """)
        channel = interaction.client.bot.get_channel(vjn_object.livraison) # channel livraison
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
