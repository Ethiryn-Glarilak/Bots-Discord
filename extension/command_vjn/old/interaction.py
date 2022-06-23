import discord_components
import re
from extension.command_vjn.vjn_object import Status
from extension.command_vjn.option import function_menu, function_valid, function_retour, function_annuler

async def commander(interaction : discord_components.Interaction) -> None:
    bot = interaction.client.bot
    database = bot.vjn_object.database

    # Check si l'utilisateur n'as pas déjà une commande en cours
    if database.execute(f"SELECT count(*) as number FROM command_VJN WHERE id_user = {interaction.user.id} AND status = {Status.COMMAND.value}").fetchall()[0, "number"] != 0:
        await interaction.respond(content = "Tu as une commande non terminer.")
        return

    id_command = database.execute(f"INSERT INTO command_VJN (id_user, status) VALUES ({interaction.user.id}, {Status.COMMAND}) RETURNING id").fetchall()[0, "id"]

    await interaction.user.send(components = bot.vjn_object.set_start_menu(id_command))
    await interaction.respond(content = "Check your DM with me.")

async def error(interaction : discord_components.Interaction):
    if interaction.client.bot.user != interaction.user:
        interaction.client.bot.log.get_logger(f"interaction-{interaction.client.bot.name}", "interaction", True).debug(f"Function not found {interaction.custom_id}")
        await interaction.respond(content = f"Function not found `{interaction.custom_id}`")

async def menu(interaction : discord_components.Interaction) -> None:
    for name, value in function_menu.items():
        if re.match(name, interaction.values[0]):
            await value(interaction)
            return
    await error(interaction)

async def valider(interaction : discord_components.Interaction) -> None:
    for name, value in function_valid.items():
        if re.match(name, interaction.custom_id):
            await value(interaction)
            return
    await error(interaction)

async def assigned(interaction : discord_components.Interaction) -> None:
    id_command, cooks = interaction.custom_id.split('-')[1:]
    database = interaction.client.bot.vjn_object.database
    database.execute(f"""
        UPDATE command_VJN
        SET status = {int(cooks)}
        WHERE id = {id_command}
    """)

    emojis = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    await interaction.edit_origin(
        content = f"{interaction.message.content} to :{emojis[int(cooks)]}:",
        components = interaction.client.bot.vjn_object.set_after_assignment(id_command)
    )

async def modifier(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.vjn_object.database
    cooks = database.execute(f"SELECT status FROM command_VJN WHERE id = {id_command}").fetchall()[0, "status"]
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FILE_ATTENTE.value}
        WHERE id = {id_command}
    """)

    emojis = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    await interaction.edit_origin(
        content = f"{interaction.message.content[:-(4 + 1 + len(emojis[cooks]) + 1)]}",
        components = interaction.client.bot.vjn_object.set_assignment(id_command)
    )

async def retour(interaction : discord_components.Interaction) -> None:
    for name, value in function_retour.items():
        if re.match(name, interaction.custom_id):
            await value(interaction)
            return
    await error(interaction)

async def annuler(interaction : discord_components.Interaction) -> None:
    for name, value in function_annuler.items():
        if re.match(name, interaction.custom_id):
            await value(interaction)
            return
    await error(interaction)

async def pate(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[1]

    database = interaction.client.bot.vjn_object.database
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    database.execute(f"""
        SELECT id FROM ingredient_VJN
        JOIN (SELECT * FROM product_ingredient_VJN WHERE id_product = {id_product}) AS ingredient
        ON id = id_ingredient WHERE type = True
    """).fetchall()

    selected = database["id"]

    await interaction.user.send(components = interaction.client.bot.vjn_object.set_pate(id_command, selected))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

async def garniture(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[1]

    database = interaction.client.bot.vjn_object.database
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]
    database.execute(f"""
        SELECT id FROM ingredient_VJN
        JOIN (SELECT * FROM product_ingredient_VJN WHERE id_product = {id_product}) AS ingredient
        ON id = id_ingredient WHERE type = False
    """).fetchall()

    selected = database["id"]

    await interaction.user.send(components = interaction.client.bot.vjn_object.set_garniture(id_command, selected))
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()

class InteractionCommandVJN:

    additional_function = {
        "commander" : commander,
        "menu-*" : menu,
        "valid-*" : valider,
        "assigned-*" : assigned,
        "modifier-*" : modifier,
        "retour-*" : retour,
        "annuler-*" : annuler,
        "pate-*" : pate,
        "garniture-*" : garniture,
    }
