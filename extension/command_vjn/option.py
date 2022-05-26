import discord_components
import os
from extension.command_vjn.vjn_object import Status

def command(interaction : discord_components.Interaction, id_command : int):
    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    name = database.execute(f"SELECT name FROM product_VJN WHERE id = {id_product}").fetchall()[0, "name"].capitalize() + " :"
    database.execute(f"SELECT name FROM (SELECT id_ingredient FROM (SELECT * FROM product_VJN WHERE id = {id_product}) AS product_VJN JOIN product_ingredient_VJN ON id = id_product) AS product_ingredient_VJN JOIN ingredient_VJN ON id = id_ingredient").fetchall()
    for product in database:
        name += f" {product[0]},"
    return name[:-1]

async def crepes(interaction : discord_components.Interaction) -> None:
    database = interaction.client.bot.database.get("default")
    origin = interaction.custom_id.split('-')[1]
    id_command = interaction.custom_id.split('-')[2]
    id_product = interaction.values[0].split('-')[1]
    database.execute(f"SELECT price FROM product_VJN WHERE id = {id_product}")
    database.fetchall()
    database.execute(f"""
        UPDATE command_VJN
        SET id_product = {id_product},
            price = '{database[0, "price"]}'
        WHERE id = {id_command}
    """)
    await interaction.user.send(content = f"Commande n°{id_command}\n{command(interaction, id_command)}\nConfirmer votre commande.", components = interaction.client.bot.vjn_object.set_check_command(id_command, origin))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def category(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    id_product = interaction.values[0].split('-')[1]

    await interaction.user.send(components = interaction.client.bot.vjn_object.set_category_menu(id_command, id_product))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def compose(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]

    await interaction.user.send(components = interaction.client.bot.vjn_object.set_compose_menu(id_command, []))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def ingredient(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]

    database = interaction.client.bot.database.get("default")
    database.execute("SELECT * FROM ingredient_VJN")
    database.fetchall()
    price = sum(float(database[ingredient.split("-")[1], "price"].replace(" €", "").replace(",", ".")) for ingredient in interaction.values)

    id_product = database.execute(f"INSERT INTO product_VJN (name, price) VALUES ('{interaction.user}_{id_command}', {price}) RETURNING id").fetchall()[0, "id"]
    database.execute(f"""
        INSERT INTO product_ingredient_VJN (id_product, id_ingredient) VALUES
            {"".join(f"({id_product}, {ingredient.split('-')[1]}), " for ingredient in interaction.values)[:-2]}
        """)

    database.execute(f"""
        UPDATE command_VJN
        SET id_product = {id_product},
            price = {price}
        WHERE id = {id_command}
    """)

    origin = f"""compose_{"_".join(f"{ingredient.split('-')[1]}" for ingredient in interaction.values)}"""
    await interaction.user.send(content = f"Commande n°{id_command}\n{command(interaction, id_command)}\nConfirmer votre commande.", components = interaction.client.bot.vjn_object.set_check_command(id_command, origin))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

function_menu = {
    "crepes-*" : crepes,
    "category-*" : category,
    "compose" : compose,
    "ingredient-*" : ingredient,
}

async def valid(interaction : discord_components.Interaction) -> None:
    database = interaction.client.bot.database.get("default")
    id_command = interaction.custom_id.split('-')[2]
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.PAYMENT_REQUIRED.value}
        WHERE id = {id_command}
    """)
    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}")
    database.fetchall()
    price = database[0, 'price']
    if price != "0,00 €":
        # paid
        channel = interaction.client.bot.get_channel(int(os.getenv("paiement"))) # channel paiement
        await interaction.user.send(content = f"La commande {command(interaction, id_command)} à {price} est envoyée à VJN.\nAllez payer à la caisse pour lancer la préparation.")
        await channel.send(content = f"n°{id_command} {interaction.user} : {command(interaction, id_command)} -> {price}", components = interaction.client.bot.vjn_object.set_paiement_command(id_command))
    else:
        # assigned
        channel = interaction.client.bot.get_channel(int(os.getenv("assignment"))) # channel assignment
        await interaction.user.send(content = f"La commande {command(interaction, id_command)} est envoyée à VJN.")
        await channel.send(
            content = f"n°{id_command} {interaction.user} : {command(interaction, id_command)} -> {price}",
            components = interaction.client.bot.vjn_object.set_assignment(id_command)
        )
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def paiement(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FILE_ATTENTE.value}
        WHERE id = {id_command}
    """)
    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}")
    database.fetchall()
    price = database[0, 'price']
    channel = interaction.client.bot.get_channel(int(os.getenv("assignment"))) # channel assignment
    await channel.send(
        content = f"n°{database[0, 'id']} {interaction.user} : {command(interaction, database[0, 'id'])} -> {price}",
        components = interaction.client.bot.vjn_object.set_assignment(id_command)
    )
    await interaction.message.delete()

async def assigned(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.READY.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(int(os.getenv("livraison"))) # channel livraison
    database.execute(f"SELECT id_user FROM command_VJN WHERE id = {id_command}")
    database.fetchall()
    await channel.send(
        content = interaction.message.content,
        components = interaction.client.bot.vjn_object.set_livrer(id_command)
    )
    user = interaction.client.bot.get_user(database[0, "user"])
    await user.send(content = f"Votre commande n°{id_command} est prête. Il s'agit de la commande {command(interaction, id_command)}")
    await interaction.message.delete()

async def livrer(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FINISH.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(int(os.getenv("log"))) # channel log
    await channel.send(content = interaction.message.content)
    await interaction.message.delete()

function_valid = {
    "valid-command-*" : valid,
    "valid-paiement-*" : paiement,
    "valid-assigned-*" : assigned,
    "valid-livrer-*" : livrer,
}

async def start(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    await interaction.user.send(components = interaction.client.bot.vjn_object.set_start_menu(id_command))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def category_retour(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    id_product = interaction.custom_id.split('-')[1].split('_')[1]
    await interaction.user.send(components = interaction.client.bot.vjn_object.set_category_menu(id_command, id_product))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def compose_retour(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]

    selected = interaction.custom_id.split('-')[1].split('_')[1:]

    await interaction.user.send(components = interaction.client.bot.vjn_object.set_compose_menu(id_command, selected))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

function_retour = {
    "retour-start-*" : start,
    "retour-category_*-*" : category_retour,
    "retour-compose*-*" : compose_retour,
}
