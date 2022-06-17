import discord_components
from src.interaction.interaction import Interaction
from src.interaction.composent.button import Style
from extension.command_vjn.vjn_object import VJNObject
from extension.command_vjn.interaction.default import *

def set_menu(menu : Interaction, options : list):
    if len(menu) > 25:
        menu = menu[:25]
        # FIXME: Replace by a second menu
        # raise ValueError("To many options, max options are 25")
    if not menu:
        menu.append({"label": "empty category", "value": "error"})
    for option in options:
        menu.add_option(**option)

def menu(interaction : discord_components.Interaction):
    id_command = interaction.custom_id.split('-')[2]
    bot = interaction.client.bot
    vjn_object : VJNObject = bot.vjn_object
    json : dict[dict] = bot.vjn_object.json
    database = vjn_object.database

    user = interaction.user

    # user.roles
    # price = bot.args.free #or vjn_object.role_free in user.roles
    print(vjn_object.role_free in user.roles)

    promotion = False or bot.args.free

    # Récupération recette existante
    get_all_product(database)
    menu = [{"label": f"{database[str(product), 'name'].capitalize()} - {database[str(product), 'price'] if database[str(product), 'price'] != '0,00 €' and not promotion else 'Gratuit'}", "value": f"product-{product}"} for product in json.get("other", []).values() if product in database]

    # Création composent
    start_menu = Interaction().add_menu(id = f"menu-other-{id_command}", placeholder = "Choice your product")

    set_menu(start_menu, menu)
    return start_menu\
        # .add_interaction(
        # Interaction()
    # FIXME
            # .add_button(label = "Retour", style = Style.GREY, id = f"retour--start-{id_command}")
    # FIXME
            # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--category_menu-{id_command}")
    # )

async def other(interaction : discord_components.Interaction):
    await interaction.defer(edit_origin = True)
    await interaction.edit_origin(components = menu(interaction))
