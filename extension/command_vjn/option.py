import discord_components
from extension.command_vjn.vjn_object import Status

def command(id):
    return "name + content"

async def crepes(interaction : discord_components.Interaction) -> None:
    database = interaction.client.bot.database.get("default")
    database.execute(f"SELECT price FROM product_VJN WHERE id = {interaction.values[0][7:]}")
    database.fetchall()
    database.execute(f"""
        UPDATE command_VJN
        SET id_product = {interaction.values[0][7:]},
            price = '{database[0, "price"]}'
        WHERE id_user = {interaction.user.id}
            AND status = {Status.COMMAND.value}
    """)
    database.commit()
    await interaction.user.send(content = f"Commande n°{interaction.values[0][7:]}\n{command(interaction.values[0][7:])}\nConfirmer votre commande.", components = interaction.client.bot.vjn_object.check_command)
    await interaction.message.delete()

async def category(interaction : discord_components.Interaction) -> None:
    if interaction.client.bot.user != interaction.user:
        interaction.client.bot.log.get_logger(f"interaction-{interaction.client.bot.name}", "interaction", True).debug(f"Function not found {interaction.custom_id}")
        await interaction.respond(content = f"Les catégories ne sont pas développer {interaction.custom_id}:{interaction.values[0]}")

function_menu = {
    "crepes-*" : crepes,
    "category-*" : category,
    "compose" : category,
}

async def valid(interaction : discord_components.Interaction) -> None:
    database = interaction.client.bot.database.get("default")
    database.execute(f"SELECT * FROM command_VJN WHERE id_user = {interaction.user.id} AND status = {Status.COMMAND.value}")
    database.fetchall()
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.PAYMENT_REQUIRED.value}
        WHERE id_user = {interaction.user.id}
            AND status = {Status.COMMAND.value}
    """)

    id_command = database[0, "id"]
    if database["price"] != 0:
        # paid
        channel = interaction.client.bot.get_channel(978670079224975410)
        await interaction.user.send(content = f"La commande {command(id_command)} est envoyée à VJN.\nAllez payer à la caisse pour lancer la préparation.")
        await channel.send(content = f"n°{id_command} {interaction.user} : {command(id_command)} -> {database[0, 'price']}", components = interaction.client.bot.vjn_object.set_paiement_command(id_command))
    else:
        # assigned
        channel = interaction.client.bot.get_channel(978708109189074964)
        await interaction.user.send(content = f"La commande {command(id_command)} est envoyée à VJN.")
        await channel.send(
            content = f"n°{id_command} {interaction.user} : {command(id_command)} -> {database[0, 'price']}",
            components = interaction.client.bot.vjn_object.set_assignment(id_command)
        )
        return
    await interaction.message.delete()

async def paiement(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}")
    database.fetchall()
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FILE_ATTENTE.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(978708109189074964)
    await channel.send(
        content = f"n°{database[0, 'id']} {interaction.user} : {command(database[0, 'id'])} -> {database[0, 'price']}",
        components = interaction.client.bot.vjn_object.set_assignment(id_command)
    )
    await interaction.message.delete()

async def assigned(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"SELECT id_user FROM command_VJN WHERE id = {id_command}")
    database.fetchall()
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.READY.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(978727142781231114)
    await channel.send(
        content = interaction.message.content,
        components = interaction.client.bot.vjn_object.set_livrer(id_command)
    )
    user = interaction.client.bot.get_user(database[0, "user"])
    await user.send(content = f"Votre commande n°{id_command} est prête.")
    await interaction.message.delete()

async def livrer(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FINISH.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(978735565795127316)
    await channel.send(content = interaction.message.content)
    await interaction.message.delete()

function_valid = {
    "valid-command" : valid,
    "valid-paiement-*" : paiement,
    "valid-assigned-*" : assigned,
    "valid-livrer-*" : livrer,
}
