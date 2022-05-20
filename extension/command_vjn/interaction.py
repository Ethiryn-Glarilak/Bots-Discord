import discord_components
from extension.command_vjn.vjn_object import Status

async def commander(interaction : discord_components.Interaction) -> None:
    bot = interaction.client.bot
    database = bot.database.get("default")

    #FIXME Vérifier qu'une command au statu Status.COMMAND n'est pas déjà en cours
    database.execute(f"""INSERT INTO command_VJN (id_user, status) VALUES ({interaction.user.id}, {Status.COMMAND})""")

    await interaction.user.send(components = bot.vjn_object.start_menu)
    await interaction.respond(content = "Check your DM with me.")

async def menu(interaction : discord_components.Interaction) -> None:
    await interaction.respond(content = "Thank you for your choices.")

class InteractionCommandVJN:

    additional_function = {
        "commander" : commander,
        "menu-*" : menu,
    }
