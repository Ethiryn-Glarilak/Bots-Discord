import discord_components
import os
from extension.command_vjn.vjn_object import Status
from extension.command_vjn.interaction.default import *

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

    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"INSERT INTO product_VJN (name, price) VALUES ('{interaction.user}_{id_command}', 0) RETURNING id").fetchall()[0, "id"]

    database.execute(f"""
        UPDATE command_VJN
        SET id_product = {id_product}
        WHERE id = {id_command}
    """)

    await interaction.user.send(components = interaction.client.bot.vjn_object.set_composition_menu(id_command, True))
    # await interaction.user.send(components = interaction.client.bot.vjn_object.set_compose_menu(id_command, []))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def ingredient(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    type_ingredient = interaction.custom_id.split('-')[1]

    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    database.execute("SELECT * FROM ingredient_VJN").fetchall()
    price = sum(float(database[ingredient.split("-")[1], "price"].replace(" €", "").replace(",", ".")) for ingredient in interaction.values)

    if type_ingredient == "pate":
        type_ingredient = True
    elif type_ingredient == "garniture":
        type_ingredient = False

    database.execute(f"""
        DELETE FROM
            product_ingredient_VJN
        WHERE
            (id_product, id_ingredient) IN 
                (SELECT id_product, id_ingredient FROM product_ingredient_VJN
                    JOIN (SELECT id FROM ingredient_VJN WHERE type = {type_ingredient})
                        AS ingredient_VJN
                    ON id = id_ingredient
                    WHERE id_product = {id_product})
        """).commit()

    database.execute(f"""
        INSERT INTO product_ingredient_VJN (id_product, id_ingredient) VALUES
            {"".join(f"({id_product}, {ingredient.split('-')[1]}), " for ingredient in interaction.values)[:-2]}
        """).commit()

    database.execute(f"""
        UPDATE command_VJN
        SET price = {price}
        WHERE id = {id_command}
    """)

    database.execute(f"""
        UPDATE product_VJN
        SET price = {price}
        WHERE id = {id_product}
    """)

    pate_name = database.execute(f"SELECT name FROM ingredient_VJN JOIN (SELECT id_ingredient FROM product_ingredient_VJN WHERE id_product = {id_product}) AS product_ingredient_VJN ON id_ingredient = id WHERE type = True").fetchall()["name"]
    garniture_name = database.execute(f"SELECT name FROM ingredient_VJN JOIN (SELECT id_ingredient FROM product_ingredient_VJN WHERE id_product = {id_product}) AS product_ingredient_VJN ON id_ingredient = id WHERE type = False").fetchall()["name"]

    valid = len(pate_name) != 1 or not garniture_name
    msg_pate ="Pate : " + "".join(f"{name}, " for name in pate_name)[:-2]
    msg_garniture = "Garniture : " + "".join(f"{name}, " for name in garniture_name)[:-2]
    content = msg_pate + "\n" + msg_garniture + "\nPrice : " + str(price).replace(".", ",") + " €\n"

    await interaction.user.send(content = content, components = interaction.client.bot.vjn_object.set_composition_menu(id_command, valid))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

    # origin = f"""compose_{"_".join(f"{ingredient.split('-')[1]}" for ingredient in interaction.values)}"""
    # await interaction.user.send(content = f"Commande n°{id_command}\n{command(interaction, id_command)}\nConfirmer votre commande.", components = interaction.client.bot.vjn_object.set_check_command(id_command, origin))
    # if interaction.message.channel is None:
    #     interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    # await interaction.message.delete()

function_menu = {
    "crepes-*" : crepes,
    "category-*" : category,
    "compose" : compose,
    "ingredient-*" : ingredient,
}

async def valid(interaction : discord_components.Interaction) -> None:
    database = interaction.client.bot.database.get("default")
    vjn_object = interaction.client.bot.vjn_object
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
        channel = interaction.client.bot.get_channel(vjn_object.paiement) # channel paiement
        await interaction.user.send(content = f"La commande {command(interaction, id_command)} à {price} est envoyée à VJN.\nAllez payer à la caisse pour lancer la préparation.")
        await channel.send(content = f"n°{id_command} {interaction.user} : {command(interaction, id_command)} -> {price}", components = interaction.client.bot.vjn_object.set_paiement_command(id_command))
    else:
        # assigned
        channel = interaction.client.bot.get_channel(vjn_object.assignment) # channel assignment
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
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FILE_ATTENTE.value}
        WHERE id = {id_command}
    """)
    database.execute(f"SELECT * FROM command_VJN WHERE id = {id_command}")
    database.fetchall()
    price = database[0, 'price']
    channel = interaction.client.bot.get_channel(vjn_object.assignment) # channel assignment
    await channel.send(
        content = f"n°{database[0, 'id']} {interaction.user} : {command(interaction, database[0, 'id'])} -> {price}",
        components = interaction.client.bot.vjn_object.set_assignment(id_command)
    )
    await interaction.message.delete()

async def assigned(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.READY.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(vjn_object.livraison) # channel livraison
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
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FINISH.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(vjn_object.log) # channel log
    await channel.send(content = interaction.message.content)
    await interaction.message.delete()

function_valid = {
    "valid-command-*" : valid,
    "valid-paiement-*" : paiement,
    "valid-assigned-*" : assigned,
    "valid-livrer-*" : livrer,
}

async def annuler(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        DELETE FROM command_VJN
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(vjn_object.log) # channel log
    message = interaction.message.content.replace("\n", " ")
    await channel.send(content=f":x: {message or f'n°{id_command} {interaction.user}'} :x:")
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def compose_annuler(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    database.execute(f"""
        UPDATE command_VJN
        SET id_product = NULL
        WHERE id = {id_command}
    """)
    database.execute(f"""
        DELETE FROM product_VJN
        WHERE id = {id_product}
    """)
    await annuler(interaction)

async def check_annuler(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    database.execute(f"""
        DELETE FROM product_ingredient_VJN
        WHERE id_product = {id_product}
    """)
    await compose_annuler(interaction)

function_annuler = {
    "annuler-start_menu-*" : annuler,
    "annuler-category_menu-*" : annuler,
    "annuler-compose_menu-*" : compose_annuler,
    "annuler-start-*" : annuler,
    "annuler-category_*-*" : annuler,
    "annuler-compose_*-*" : check_annuler,
    "annuler-paiement-*" : annuler,
    "annuler-assignment-*" : annuler,
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
    database = interaction.client.bot.database.get("default")
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    database.execute(f"""
        DELETE FROM product_ingredient_VJN
        WHERE id_product = {id_product}
    """)

    selected = interaction.custom_id.split('-')[1].split('_')[1:]
    await interaction.user.send(components = interaction.client.bot.vjn_object.set_compose_menu(id_command, selected))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def retour_composition(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    await interaction.user.send(components = interaction.client.bot.vjn_object.set_composition_menu(id_command))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

function_retour = {
    "retour-start-*" : start,
    "retour-category_*-*" : category_retour,
    "retour-compose_*-*" : compose_retour,
    "retour-composition-*" : retour_composition,
}
