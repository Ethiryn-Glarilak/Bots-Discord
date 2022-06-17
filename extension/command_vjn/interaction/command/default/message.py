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

def menu(id_command, bot):
    vjn_object : VJNObject = bot.vjn_object
    json : dict[dict] = bot.vjn_object.json
    database = vjn_object.database

    # Récupération recette existante
    get_all_product(database)
    menu = [{"label": f"{database[str(product), 'name'].capitalize()} - {database[str(product), 'price'] if database[str(product), 'price'] != '0,00 €' and not bot.args.free else 'Gratuit'}", "value": f"product-{product}"} for product in json.get("default", []).values() if product in database]

    # Création composent
    start_menu = Interaction().add_menu(id = f"menu-default-{id_command}", placeholder = "Choice your product")

    set_menu(start_menu, menu)
    return start_menu\
        # .add_interaction(
        # Interaction()
    # FIXME
            # .add_button(label = "Retour", style = Style.GREY, id = f"retour--start-{id_command}")
    # FIXME
            # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--category_menu-{id_command}")
    # )

async def default(interaction : discord_components.Interaction):
    await interaction.defer(edit_origin = True)
    id_command = interaction.custom_id.split('-')[2]
    bot = interaction.client.bot
    await interaction.edit_origin(components = menu(id_command, bot))
