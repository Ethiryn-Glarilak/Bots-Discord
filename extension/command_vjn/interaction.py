import discord_components
import re
from extension.command_vjn.vjn_object import Status
from extension.command_vjn.option import function_menu, function_valid

async def commander(interaction : discord_components.Interaction) -> None:
    bot = interaction.client.bot
    database = bot.database.get("default")

    # Check si l'utilisateur n'as pas déjà une commande en cours
    if database.execute(f"SELECT count(*) as number FROM command_VJN WHERE id_user = {interaction.user.id} AND status = {Status.COMMAND.value}").fetchall()[0, "number"] != 0:
        await interaction.respond(content = "Tu as une commande non terminer.")
        return

    database.execute(f"""INSERT INTO command_VJN (id_user, status) VALUES ({interaction.user.id}, {Status.COMMAND})""")

    await interaction.user.send(components = bot.vjn_object.start_menu)
    await interaction.respond(content = "Check your DM with me.")

async def error(interaction : discord_components.Interaction):
    if interaction.client.bot.user != interaction.user:
        interaction.client.bot.log.get_logger(f"interaction-{interaction.client.bot.name}", "interaction", True).debug(f"Function not found {interaction.custom_id}")
        await interaction.respond(content = f"Function not found {interaction.custom_id}")

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
    database = interaction.client.bot.database.get("default")
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

class InteractionCommandVJN:

    additional_function = {
        "commander" : commander,
        "menu-*" : menu,
        "valid-*" : valider,
        "assigned-*" : assigned,
    }
