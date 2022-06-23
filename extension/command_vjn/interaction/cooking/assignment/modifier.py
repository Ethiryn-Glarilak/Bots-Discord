import discord_components
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction
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

async def modifier(interaction : discord_components.Interaction):
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.vjn_object.database
    cooks = database.execute(f"SELECT status FROM command_VJN WHERE id = {id_command}").fetchall()[0, "status"]

    emojis = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    await interaction.edit_origin(
        content = f"{interaction.message.content[:-(4 + 1 + len(emojis[cooks + 1]) + 1)]}",
        components = menu(interaction.client.bot, id_command)
    )
