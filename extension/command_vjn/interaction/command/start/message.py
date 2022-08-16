import discord_components
from src.interaction.interaction import Interaction
from src.composant.role import Role
from extension.command_vjn.vjn_object import VJNObject
from extension.command_vjn.interaction.default import *

def menu(bot, id_command):
    vjn_object : VJNObject = bot.vjn_object

    # Création interaction
    interaction = Interaction().add_menu(id = f"menu-start-{id_command}", placeholder = "Que voulez-vous ?")

    # Ajout des trois options si non vide
    if vjn_object.json.get("default", {}) != {}:
        interaction.add_option(label = "Crêpes Usuelles", value = "default")
    if vjn_object.json.get("other", {}) != {}:
        interaction.add_option(label = "Autre recettes", value = "other")
    if vjn_object.json.get("ingredient", {}) != {}:
        interaction.add_option(label = "Composer sa crêpe", value = "compose")

    # Erreur dans le fichier json
    if len(interaction.menu.options) == 0:
        interaction.add_option(label = "Erreur du créateur de l’évènement. Le contacter !")

    return interaction\
    # FIXME
            # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--start_menu-{id}")

async def commander(interaction : discord_components.Interaction):
    bot = interaction.client.bot
    database = bot.vjn_object.database

    command = get_command_user_status(database, interaction.user.id)
    if len(command) == 1:
        id_command = command[0, "id"]
    elif len(command) > 1:
        bot.log.get_logger(f"commandVJN-{bot.name}").info(f"User {interaction.user.id} has more than one command")
    else:
        id_command = create_command_user(database, interaction.user.id)

    await interaction.respond(components = menu(bot, id_command))

    # Add role Présent at user
    await interaction.user.add_roles(Role(role = bot.vjn_object.present))
