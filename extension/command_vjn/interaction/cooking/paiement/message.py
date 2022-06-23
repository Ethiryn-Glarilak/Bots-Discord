import discord_components
import re
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction
from extension.command_vjn.vjn_object import Status
from extension.command_vjn.interaction.cooking.assignment.message import assignment
from extension.command_vjn.interaction.default import *

def menu(id_command : int):
    return Interaction().add_interaction(
        Interaction()
            .add_button(label = "Valider", style = Style.GREEN, id = f"valider-paiement-{id_command}")
            .add_button(label = "Annuler", style = Style.RED, id = f"annuler-paiement-{id_command}")
        )

async def paiement(interaction : discord_components.Interaction):
    id_command = interaction.custom_id.split('-')[2]
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.database.get("default")

    # FIXME
    price = database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}").fetchall()[0, 'price']
    price = float(re.findall(r"\d+,\d{1,2}", price)[0].replace(",", ".")) * database[0, 'quantity']
    price = f"{price:.2f} €".replace(".", ",")

    if price != "0,00 €":
        # FIXME
        database.execute(f"""
            UPDATE command_VJN
            SET status = {Status.PAYMENT_REQUIRED.value}
            WHERE id = {id_command}
        """)
        channel = interaction.client.bot.get_channel(vjn_object.paiement) # channel paiement
        await interaction.edit_origin(content = f"Commande fini !\nLa commande {command(interaction, id_command)} à {price} est envoyée à VJN.\nAllez payer à la caisse pour lancer la préparation.", components = [])
        await channel.send(content = f"n°{id_command} <@{interaction.user.id}> : {command(interaction, id_command)} -> {price}", components = menu(id_command))
    else:
        await interaction.edit_origin(content = "Commande fini !", components = [])
        await assignment(interaction)
